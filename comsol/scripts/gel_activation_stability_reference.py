"""Independent radial stability and heat-only precursor checks for Model B.

These are conditional theory checks, not additional COMSOL simulations. They
test whether a supplied equilibrium can be accessed/stabilized by a cold-liquid
heating path. Existing reference exports are preserved.
"""
from pathlib import Path
import json
from math import pi,log,exp
import numpy as np
from scipy.optimize import least_squares,brentq,root

ROOT=Path(__file__).resolve().parents[1]
defs=(ROOT/'scripts/core_shell_reference.py').read_text(encoding='utf8').split('\nrows=[]',1)[0]
space={'__file__':str(ROOT/'scripts/core_shell_reference.py')}
exec(compile(defs,'core_shell_reference.py','exec'),space)
state=space['state'];mechanical=space['mechanical'];CP=space['CP']
a,G,T0,p0,sll,slv,mass,u0,fluid=[space[k] for k in ['a','G','T0','p0','sigmaLL','sigmaLV','mass','u0','fluid']]

def energy_state(qdep,seed):
    def residual(x):
        q=state(x[0],x[1],exp(x[2]))
        return [q['chemical_residual_J_kg']/1e5,q['volume_relative_residual'],(q['Q_J']-qdep)/qdep]
    ans=least_squares(residual,seed,bounds=([1.2,300,log(a*.05)],[4,390,log(a*4)]),xtol=2e-13,ftol=2e-13,gtol=2e-13)
    if np.linalg.norm(residual(ans.x))>1e-8:raise RuntimeError('Unclosed independent baseline root')
    return state(ans.x[0],ans.x[1],exp(ans.x[2])),ans.x

def restoring(q,closure,eps):
    net=[]
    for lam in [q['stretch']-eps,q['stretch']+eps]:
        if closure=='isothermal':
            def residual(x):
                z=state(lam,q['T_K'],exp(x[0]),exp(x[1]))
                return [z['chemical_residual_J_kg']/1e5,z['volume_relative_residual']]
            seed=[log(q['Rgas_m']),log(q['p_liquid_Pa'])]
        else:
            def residual(x):
                z=state(lam,x[0],exp(x[1]),exp(x[2]))
                return [z['chemical_residual_J_kg']/1e5,z['volume_relative_residual'],(z['Q_J']-q['Q_J'])/q['Q_J']]
            seed=[q['T_K'],log(q['Rgas_m']),log(q['p_liquid_Pa'])]
        ans=root(residual,seed,tol=1e-10)
        if np.linalg.norm(residual(ans.x))>1e-7:raise RuntimeError('Unclosed stability perturbation')
        pressure=exp(ans.x[-1])
        net.append(pressure-p0-mechanical(lam)[0]-2*sll/(a*lam))
    return -(net[1]-net[0])/(2*eps)

def liquid_precursor(T):
    def residual(lam):
        pressure=p0+mechanical(lam)[0]+2*sll/(a*lam)
        rho=CP.PropsSI('Dmass','T|liquid',T,'P',pressure,fluid)
        return rho*4*pi*(a*lam)**3/3/mass-1
    lam=brentq(residual,.95,1.3,xtol=1e-13)
    pressure=p0+mechanical(lam)[0]+2*sll/(a*lam)
    u=CP.PropsSI('Umass','T|liquid',T,'P',pressure,fluid)
    ws=mechanical(lam)[1]
    Q=mass*(u-u0)+ws+p0*4*pi*a**3*(lam**3-1)/3+4*pi*sll*a*a*(lam*lam-1)
    return dict(T_K=float(T),stretch=float(lam),p_liquid_Pa=float(pressure),Q_J=float(Q),
                flat_saturation_pressure_Pa=float(CP.PropsSI('P','T',T,'Q',0,fluid)))

def main():
    rows=[];seed=[1.91,340.,log(a*1.85)]
    for qdep in np.array([11.55,11.65,11.75,11.82,11.9])*1e-12:
        q,seed=energy_state(qdep,seed)
        for closure in ['isothermal','closed_energy']:
            k1=restoring(q,closure,1e-4);k2=restoring(q,closure,5e-5)
            q[closure+'_restoring_stiffness_Pa_per_stretch']=float(k2)
            q[closure+'_difference_step_change_relative']=float(abs(k2/k1-1))
            q[closure+'_radially_stable']=bool(k2>0)
        rows.append(q)
    T_lower=brentq(lambda T:liquid_precursor(T)['flat_saturation_pressure_Pa']-liquid_precursor(T)['p_liquid_Pa'],T0+1,390,xtol=1e-9)
    onset=liquid_precursor(T_lower)
    # Solve the phase state whose equivalent stretch is the cited proxy.
    def fail_residual(x):
        q=state(2.1,x[0],exp(x[1]));return [q['chemical_residual_J_kg']/1e5,q['volume_relative_residual']]
    ans=root(fail_residual,[338.,log(a*2.02)],tol=1e-11)
    if np.linalg.norm(fail_residual(ans.x))>1e-8:raise RuntimeError('Failure-proxy reference did not close')
    qlimit=state(2.1,ans.x[0],exp(ans.x[1]))
    times=dict(assumed_waterlike_gel_thermal_diffusivity_m2_s=.6/(1006.5*4180),
        cold_radius_thermal_time_s=a*a/(.6/(1006.5*4180)),
        elastic_inertial_time_s=float(a*np.sqrt(1006.5/G)),
        draft_20ms_over_cold_radius_thermal_time=float(.02/(a*a/(.6/(1006.5*4180)))))
    result=dict(reference_equilibria=rows,heat_only_precursor_bulk_saturation_lower_bound=onset,
        equivalent_stretch_proxy_state=qlimit,
        lower_bound_onset_energy_exceeds_equivalent_proxy_energy=bool(onset['Q_J']>qlimit['Q_J']),
        timescale_reference=times,
        conclusions=[
         'Activated upper-branch states are radially stable under the declared closed-energy/instant-equilibrium closure, but unstable if temperature is clamped.',
         'The uniform pure-liquid thermal precursor needs at least the bulk-saturation lower-bound energy; a finite nucleus adds a capillary/nucleation barrier. This is not a measured optical threshold.',
         'If this lower-bound energy exceeds the reference intact-equilibrium energy, the low-energy equilibria do not demonstrate an intact cold-liquid heat-only activation path. Heterogeneous nuclei, local absorber heating, heat loss, rate-dependent mechanics and actual failure properties require measurement.',
         'The 20 ms stamp is far longer than the waterlike nanoscale diffusion time; an insulated steady inclusion is not established for that pulse.'
        ],
        limitations=['Constant room-temperature effective interface energies; actual gel interface stress and temperature dependence unknown.',
                     'Spherical infinite Neo-Hookean host for the independent reference; native 3D radius/energy refinements quantify its comparison.',
                     'Radial local stability only; no shape/damage/transport stability or reset proof.'])
    (ROOT/'data/gel_activation_stability_reference.json').write_text(json.dumps(result,indent=2),encoding='utf8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
