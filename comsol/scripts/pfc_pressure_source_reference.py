"""Independent finite PFP core-shell isentrope for the pressure-source model.

The PFP phases equilibrate internally without exchanging heat with water.
This limiting closure is distinct from a fixed vapor pressure and from a gas
polytrope. Temperature, phase mass and both pressure jumps are calculated.
"""
from pathlib import Path
import sys,json
import numpy as np
from math import pi
from scipy.optimize import root as root_solve,brentq
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.tools/coolprop'))
import CoolProp.CoolProp as CP

FLUID='n-Perfluoropentane'; T0=293.15; P0=1e5; SIGLL=.054; SIGLV=.00941
F0=.5; EBUDGET=55e-9
liquid=CP.AbstractState('HEOS',FLUID);vapor=CP.AbstractState('HEOS',FLUID)
liquid.specify_phase(CP.iphase_liquid);vapor.specify_phase(CP.iphase_gas)
RLREF=CP.PropsSI('Dmass','T',T0,'Q',0,FLUID)
RVREF=CP.PropsSI('Dmass','T',T0,'Q',1,FLUID)

def props(T,rl,rv):
    liquid.update(CP.DmassT_INPUTS,rl,T);vapor.update(CP.DmassT_INPUTS,rv,T)
    return (liquid.p(),vapor.p(),liquid.gibbsmass(),vapor.gibbsmass(),
            liquid.umass(),vapor.umass(),liquid.smass(),vapor.smass())

def initial(a):
    def fun(q):
        rl,rv=RLREF*np.exp(q[0]),RVREF*np.exp(q[1])
        pl,pv,gl,gv,*_=props(T0,rl,rv)
        rho=1/((1-F0)/rl+F0/rv)
        rg=a*(F0*rho/rv)**(1/3)
        return [(pv-pl-2*SIGLV/rg)/P0,(gl-gv)/1e5]
    rr=root_solve(fun,[0,0],tol=1e-11)
    if np.linalg.norm(fun(rr.x))>1e-8:raise RuntimeError('Initial core-shell phase residual.')
    rl,rv=RLREF*np.exp(rr.x[0]),RVREF*np.exp(rr.x[1])
    pl,pv,gl,gv,ul,uv,sl,sv=props(T0,rl,rv)
    rho=1/((1-F0)/rl+F0/rv);mass=rho*4*pi*a**3/3
    rg=a*(F0*rho/rv)**(1/3)
    rd=a*(rho/1621.23)**(1/3)
    for _ in range(8):
        pc=P0+2*SIGLL/rd
        rdc=CP.PropsSI('Dmass','T|liquid',T0,'P',pc,FLUID)
        rd=(mass/(4*pi*rdc/3))**(1/3)
    ud=CP.PropsSI('Umass','T|liquid',T0,'P',P0+2*SIGLL/rd,FLUID)
    ui=mass*((1-F0)*ul+F0*uv)+4*pi*SIGLV*rg**2
    energy=ui-mass*ud+P0*(4*pi*a**3/3-mass/rdc)+4*pi*SIGLL*(a*a-rd*rd)
    return dict(a_m=a,mass_kg=mass,initial_liquid_density_kg_m3=rl,initial_vapor_density_kg_m3=rv,
      initial_T_K=T0,initial_vapor_fraction=F0,initial_outer_pressure_Pa=pl,initial_core_pressure_Pa=pv,
      initial_specific_entropy_J_kg_K=(1-F0)*sl+F0*sv,cold_liquid_radius_m=rd,
      cold_density_kg_m3=rdc,cold_specific_u_J_kg=ud,
      phase_and_inner_surface_initial_energy_J=ui,source_energy_relative_cold_J=energy,
      seed_theta=1.,seed_qL=float(rr.x[0]),seed_qV=float(rr.x[1]))

def run():
    a=brentq(lambda a:initial(a)['source_energy_relative_cold_J']-EBUDGET,5e-6,100e-6,xtol=1e-14)
    init=initial(a);mass=init['mass_kg'];s0=init['initial_specific_entropy_J_kg_K']
    def state(r,x):
        T=T0*x[0];rl=RLREF*np.exp(x[1]);rv=RVREF*np.exp(x[2])
        pl,pv,gl,gv,ul,uv,sl,sv=props(T,rl,rv)
        V=4*pi*(a*r)**3/3
        fv=(V-mass/rl)/(mass*(1/rv-1/rl))
        if fv<=0:raise ValueError('Two-phase closure exhausted its vapor inventory.')
        rg=(3*fv*mass/(4*pi*rv))**(1/3)
        S=mass*((1-fv)*sl+fv*sv)
        ui=mass*((1-fv)*ul+fv*uv)+4*pi*SIGLV*rg**2
        e=ui-mass*init['cold_specific_u_J_kg']+P0*(V-mass/init['cold_density_kg_m3'])+4*pi*SIGLL*((a*r)**2-init['cold_liquid_radius_m']**2)
        return dict(radius_ratio=r,T_K=T,p_liquid_Pa=pl,p_vapor_Pa=pv,rho_liquid_kg_m3=rl,
          rho_vapor_kg_m3=rv,vapor_mass_fraction=fv,Rgas_m=rg,energy_potential_relative_cold_J=e,
          entropy_residual_relative=(S-mass*s0)/(mass*100),chemical_residual_J_kg=gl-gv,
          capillary_residual_Pa=pv-pl-2*SIGLV/rg)
    rows=[];seed=np.array([1.,init['seed_qL'],init['seed_qV']])
    for r in np.linspace(1,.2,161):
        def fun(x):
            q=state(r,x)
            return [q['capillary_residual_Pa']/P0,q['chemical_residual_J_kg']/1e5,q['entropy_residual_relative']]
        try:
            solved=root_solve(fun,seed,tol=1e-11)
            if np.linalg.norm(fun(solved.x))>1e-8:raise RuntimeError(solved.message)
            seed=solved.x;row=state(r,seed);rows.append(row)
            # Once potential energy exceeds the initial energy the inviscid source
            # must already have turned; no extrapolation to full condensation.
            if row['energy_potential_relative_cold_J']>1.2*EBUDGET and r<.9:break
        except (ValueError,RuntimeError) as exc:
            init['manifold_stop_reason']=str(exc);break
    init['manifold_min_radius_ratio']=rows[-1]['radius_ratio']
    init['manifold_min_vapor_mass_fraction']=min(q['vapor_mass_fraction']for q in rows)
    init['liquid_reference_density_kg_m3']=RLREF;init['vapor_reference_density_kg_m3']=RVREF
    init['sigma_outer_N_m']=SIGLL;init['sigma_inner_N_m']=SIGLV
    init['limitations']=['Supplied post-activation maximum-radius state',
      'Uniform internal temperature and instantaneous chemical equilibrium',
      'No external heat flux or optical absorption calibration',
      'Room-temperature constant interface tensions',
      'Source is spherical; outer wave propagation is weakly compressible']
    out=dict(initial=init,rows=rows)
    (ROOT/'data/pfc_pressure_source_reference.json').write_text(json.dumps(out,indent=2),encoding='utf8')
    names=list(rows[0]);np.savetxt(ROOT/'data/pfc_pressure_source_reference.csv',
      np.array([[q[n]for n in names]for q in rows]),delimiter=',',header=','.join(names),comments='')
    print(json.dumps(init,indent=2))
if __name__=='__main__':run()
