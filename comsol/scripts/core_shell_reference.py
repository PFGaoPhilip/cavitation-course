"""Independent exact EOS root for a PFP vapor core / liquid shell in an elastic host."""
from pathlib import Path
import sys,json,csv
from math import pi,log,exp
import numpy as np
from scipy.optimize import root as solve_root
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'.tools/coolprop'))
import CoolProp.CoolProp as CP

fluid='n-Perfluoropentane';a=300e-9;G=10000.;p0=100000.;sigmaLL=.054;sigmaLV=.00941;T0=293.15
rho0=CP.PropsSI('Dmass','T|liquid',T0,'P',p0+2*sigmaLL/a,fluid)
u0=CP.PropsSI('Umass','T|liquid',T0,'P',p0+2*sigmaLL/a,fluid)
mass=rho0*4*pi*a**3/3

def mechanical(lam):
    pG=G/2*(5-4/lam-lam**-4)
    ws=2*pi*G*a**3*(5*lam**3/3-2*lam**2+1/lam-2/3)
    return pG,ws

def state(lam,T,Rg,p_liquid=None):
    pg,ws=mechanical(lam)
    pL=p0+pg+2*sigmaLL/(a*lam) if p_liquid is None else p_liquid
    pV=pL+2*sigmaLV/Rg
    rl=CP.PropsSI('Dmass','T|liquid',T,'P',pL,fluid);rv=CP.PropsSI('Dmass','T|gas',T,'P',pV,fluid)
    gl=CP.PropsSI('Gmass','T|liquid',T,'P',pL,fluid);gv=CP.PropsSI('Gmass','T|gas',T,'P',pV,fluid)
    ul=CP.PropsSI('Umass','T|liquid',T,'P',pL,fluid);uv=CP.PropsSI('Umass','T|gas',T,'P',pV,fluid)
    V=4*pi*(a*lam)**3/3;Vg=4*pi*Rg**3/3
    phi=rv*Vg/mass
    vol=(mass-rv*Vg)/rl+Vg
    Q=(mass-rv*Vg)*ul+rv*Vg*uv-mass*u0+ws+p0*(V-4*pi*a**3/3)+4*pi*(sigmaLL*((a*lam)**2-a*a)+sigmaLV*Rg**2)
    return dict(stretch=lam,T_K=T,Rgas_m=Rg,shell_thickness_m=a*lam-Rg,
                p_liquid_Pa=pL,p_vapor_Pa=pV,rho_liquid_kg_m3=rl,rho_vapor_kg_m3=rv,
                vapor_mass_fraction=phi,Q_J=Q,chemical_residual_J_kg=gl-gv,
                volume_relative_residual=vol/V-1,gel_pressure_Pa=pg,gel_energy_J=ws)

rows=[]
seed=np.array([350.,log(a*.9)])
for lam in [1.2,1.5,1.8,2.1]:
    def eq(x):
        q=state(lam,x[0],exp(x[1]))
        return [q['chemical_residual_J_kg']/100000,q['volume_relative_residual']]
    solved=solve_root(eq,seed,tol=1e-10)
    if not solved.success or np.linalg.norm(eq(solved.x))>1e-7:
        raise RuntimeError(f'Independent phase root did not pass at {lam}: {solved.message}')
    seed=solved.x
    row=state(lam,seed[0],exp(seed[1]));row['reference_only']=True;rows.append(row)
    slopes={}
    for closure in ['fixed_temperature','closed_total_energy']:
        net=[]
        for lm in [lam-1e-4,lam+1e-4]:
            if closure=='fixed_temperature':
                def perturb_eq(x):
                    q=state(lm,row['T_K'],exp(x[0]),exp(x[1]))
                    return [q['chemical_residual_J_kg']/100000,q['volume_relative_residual']]
                pert=solve_root(perturb_eq,[log(row['Rgas_m']),log(row['p_liquid_Pa'])],tol=1e-10)
                if not pert.success and np.linalg.norm(perturb_eq(pert.x))>1e-7:
                    raise RuntimeError('Isothermal perturbation failed.')
                pressure=exp(pert.x[1])
            else:
                def perturb_eq(x):
                    q=state(lm,x[0],exp(x[1]),exp(x[2]))
                    return [q['chemical_residual_J_kg']/100000,q['volume_relative_residual'],(q['Q_J']-row['Q_J'])/row['Q_J']]
                pert=solve_root(perturb_eq,[row['T_K'],log(row['Rgas_m']),log(row['p_liquid_Pa'])],tol=1e-10)
                if not pert.success and np.linalg.norm(perturb_eq(pert.x))>1e-7:
                    raise RuntimeError('Closed-energy perturbation failed.')
                pressure=exp(pert.x[2])
            net.append(pressure-(p0+mechanical(lm)[0]+2*sigmaLL/(a*lm)))
        slopes[closure+'_restoring_stiffness_Pa_per_stretch']=-(net[1]-net[0])/2e-4
    row.update(slopes)
with (root/'data/core_shell_analytic_reference.csv').open('w',newline='',encoding='utf8') as out:
    w=csv.DictWriter(out,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(root/'data/core_shell_analytic_reference.json').write_text(json.dumps(dict(
    rows=rows,mass_kg=mass,
    interface_reference=dict(PFP_water_N_m=sigmaLL,PFP_saturated_air_N_m=sigmaLV),
    limitations=['Concentric liquid shell, uniform PFC temperature, continuum capillarity',
                 'Room-temperature tensions; no measured shell/gas-gel law',
                 'Metastable-liquid branch explicitly imposed for phase comparison',
                 'No nucleation probability or laser-to-inclusion energy calibration']),indent=2),encoding='utf8')
print(json.dumps(rows,indent=2))
