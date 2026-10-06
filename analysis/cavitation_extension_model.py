"""Conditional teaching calculations for Chapters 4-5; no target calibration.

Uses inherited optics/carrier/PFH examples. Cluster runs are ideal, fixed-centre,
well-separated monopoles stopped at a declared low Mach number. They have no
PFC phase exchange, boundaries, jets, or shock resolution. Run with Python,
NumPy and SciPy: python -B analysis/cavitation_extension_model.py
"""
from pathlib import Path
import csv
import json
import math
import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.special import beta

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'analysis' / 'extension-results'
OUT.mkdir(exist_ok=True)
CONFIG = json.loads((ROOT/'reading/extension-sources/Inherited_Baseline_20261006.json').read_text(encoding='utf-8'))
def value(group, key):
    return CONFIG[group][key]['value']

rho = value('carrier', 'density_kg_m3')
c = value('carrier', 'sound_speed_m_s')
mu = value('carrier', 'dynamic_viscosity_Pa_s')
sigma = value('carrier', 'surface_tension_N_m')
pv = value('carrier', 'equilibrium_vapor_pressure_Pa')
pinf = 101325.0
dp = pinf-pv
Rmax = value('bubble_source', 'maximum_radius_m')
u_scale = math.sqrt(dp/rho)
t_scale = Rmax/u_scale

def write_csv(name, rows):
    if rows:
        with (OUT/name).open('w', encoding='utf-8', newline='') as f:
            writer=csv.DictWriter(f, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)

def geometries(pitch=40e-6):
    tri = np.array([[0,0,0],[1,0,0],[0.5,math.sqrt(3)/2,0]])*pitch
    tetra=np.array([[0,0,0],[1,0,0],[0.5,math.sqrt(3)/2,0],[0.5,math.sqrt(3)/6,math.sqrt(2/3)]])*pitch
    angle=np.arange(5)*2*math.pi/5
    pent=np.column_stack([np.cos(angle),np.sin(angle),np.zeros(5)])*(pitch/(2*math.sin(math.pi/5)))
    cube=np.array([(i,j,k) for i in [-1,0,1] for j in [-1,0,1] for k in [-1,0,1]],float)*pitch
    result={'single':np.zeros((1,3)),'three_triangle':tri,'four_tetrahedron':tetra,'five_pentagon':pent,'array_3x3x3':cube}
    return {name:xyz-xyz.mean(axis=0) for name,xyz in result.items()}

def cluster_run(xyz, rtol=2e-10, max_step=0.0015, samples=2401):
    n=len(xyz)
    distances=np.linalg.norm(xyz[:,None,:]-xyz[None,:,:],axis=-1)/Rmax
    inv=np.divide(1,distances,out=np.zeros_like(distances),where=distances>0)
    def rhs(t,y):
        x,v=y[:n],y[n:]
        A=inv*x[None,:]**2
        np.fill_diagonal(A,x)
        b=-np.ones(n)-1.5*v*v-inv@(2*x*v*v)
        acc=np.linalg.solve(A,b)
        return np.r_[v,acc]
    mach_cut=0.05
    def cut(t,y): return mach_cut*c/u_scale-np.max(np.abs(y[n:]))
    cut.terminal=True; cut.direction=-1
    sol=solve_ivp(rhs,(0,3),np.r_[np.ones(n),np.zeros(n)],rtol=rtol,atol=rtol/20,max_step=max_step,events=cut,dense_output=True,method='DOP853')
    assert sol.success and len(sol.t_events[0])==1
    ts=np.linspace(0,sol.t[-1],samples)
    ys=sol.sol(ts); x,v=ys[:n],ys[n:]
    acc=np.column_stack([rhs(t,ys[:,i])[n:] for i,t in enumerate(ts)])
    E=0.5*np.sum(x**3*v*v,axis=0)+np.sum(x**3,axis=0)/3
    for i in range(n):
        for j in range(i+1,n): E += inv[i,j]*x[i]**2*x[j]**2*v[i]*v[j]
    residual=float(np.max(np.abs(E-n/3))/(n/3))
    observer=np.array([0,0,1e-3])
    d=np.linalg.norm(observer-xyz,axis=1)
    delays=d/c
    # A common valid arrival interval; no extrapolation past the Mach cutoff.
    obs_times=np.linspace(float(delays.max()),float(sol.t[-1]*t_scale+delays.min()),samples)
    pressure=np.zeros(samples)
    for i in range(n):
        source_t=(obs_times-delays[i])/t_scale
        Ri=x[i]*Rmax; Ui=v[i]*u_scale; Ai=acc[i]*(u_scale*u_scale/Rmax)
        ddV=4*math.pi*(2*Ri*Ui*Ui+Ri*Ri*Ai)
        pressure += rho/(4*math.pi*d[i])*np.interp(source_t,ts,ddV)
    rows=[{'time_us':float(t*t_scale*1e6),'R_min_um':float(x[:,k].min()*Rmax*1e6),'R_max_um':float(x[:,k].max()*Rmax*1e6),'wall_Mach_max':float(np.max(np.abs(v[:,k]))*u_scale/c)} for k,t in enumerate(ts)]
    summary={'count':n,'cutoff_Mach':mach_cut,'time_to_cutoff_us':float(sol.t[-1]*t_scale*1e6),'energy_residual_relative':residual,'R_min_at_cutoff_um':float(x[:,-1].min()*Rmax*1e6),'R_max_at_cutoff_um':float(x[:,-1].max()*Rmax*1e6),'observer_distance_m':1e-3,'far_linear_pressure_min_Pa':float(pressure.min()),'far_linear_pressure_max_Pa':float(pressure.max()),'assumptions':'Ideal empty cavities, fixed centres, instantaneous monopole coupling, low-Mach cutoff, unbounded water-like liquid; conditional far-field wiring only.'}
    return summary, rows

def km_gas_bracket(pg_max):
    kappa=1.4 # Declared pedagogical gas, NOT PFH calibration.
    def rhs(t,y):
        R,U=y
        pg=pg_max*(Rmax/R)**(3*kappa)
        pw=pg+pv-2*sigma/R-4*mu*U/R
        noA=-3*kappa*pg*U/R+2*sigma*U/R**2+4*mu*U**2/R**2
        A=((1+U/c)*(pw-pinf)/rho+R*noA/(rho*c)-1.5*(1-U/(3*c))*U*U)/((1-U/c)*R+4*mu/(rho*c))
        return [U,A]
    def mach(t,y):return 0.1*c-abs(y[1])
    mach.terminal=True; mach.direction=-1
    def rebound(t,y):return y[1] if t>1e-14 else -1e-9
    rebound.terminal=True; rebound.direction=1
    sol=solve_ivp(rhs,(0,4e-6),[Rmax,0],rtol=2e-10,atol=[1e-14,1e-7],max_step=1e-9,events=[mach,rebound],method='DOP853')
    assert sol.success
    status='Mach_0.1_stop' if len(sol.t_events[0]) else ('first_rebound' if len(sol.t_events[1]) else 'time_limit')
    return {'gas_pressure_at_Rmax_Pa':pg_max,'kappa_assumed':kappa,'endpoint':status,'endpoint_time_us':float(sol.t[-1]*1e6),'minimum_radius_um':float(sol.y[0].min()*1e6),'maximum_inward_wall_speed_m_s':float(-sol.y[1].min()),'bubble_pressure_at_endpoint_Pa':float(pg_max*(Rmax/sol.y[0,-1])**(3*kappa)+pv),'scope':'Constant-mass polytropic gas with constant water vapor; no PFC heat/mass transfer; first-order compressibility.'}

def main():
    w=value('optics','beam_radius_1e2_m'); F=value('optics','peak_fluence_J_m2')
    eta=value('optics','absorbed_fraction'); depth=value('optics','deposition_depth_m')
    Ep=math.pi*w*w*F/2; Eabs=eta*Ep
    a=value('illustrative_PFH_core','droplet_radius_m')
    rp=value('illustrative_PFH_core','liquid_density_kg_m3')
    M=value('illustrative_PFH_core','molar_mass_kg_mol')
    Tb=value('illustrative_PFH_core','normal_boiling_temperature_K')
    T0=value('optics','initial_temperature_K')
    cp=value('illustrative_PFH_core','liquid_heat_capacity_J_kgK')
    Lv=value('illustrative_PFH_core','latent_heat_J_kg'); Ru=8.31446261815324
    vd=4*math.pi*a**3/3; md=rp*vd
    vv=md/M*Ru*Tb/pinf; av=(3*vv/(4*math.pi))**(1/3)
    phase=md*(cp*(Tb-T0)+Lv); Nb=(Rmax/av)**3
    Veff=math.pi*w*w*depth/2
    Egel=80e3; nu=.48; G=Egel/(2*(1+nu)); rho_g=1000
    Rgel0=1e-6
    pel=G/2*(5-4*Rgel0/Rmax-(Rgel0/Rmax)**4)
    Wgel=2*math.pi*G*(5/3*(Rmax**3-Rgel0**3)-2*Rgel0*(Rmax**2-Rgel0**2)+Rgel0**4*(1/Rmax-1/Rgel0))
    pref=math.sqrt(3/2)*quad(lambda x:x**1.5/math.sqrt(1-x**3),0,1,epsabs=2e-12)[0]
    pref_beta=math.sqrt(3/2)/3*beta(5/6,1/2)
    tR=pref*t_scale
    metrics={
        'scope':'Scenario calculations and numerical verification, not target predictions or physical maximum records.',
        'rho_kg_m3':rho,'c_m_s':c,'pinf_Pa':pinf,'pv_water_Pa':pv,'Delta_p_Pa':dp,'sigma_N_m':sigma,'mu_Pa_s':mu,
        'Rmax_m':Rmax,'pulse_energy_J':Ep,'absorbed_energy_J':Eabs,'ideal_collapse_coefficient_quadrature':pref,'ideal_collapse_coefficient_beta':pref_beta,'ideal_collapse_time_us':tR*1e6,
        'one_droplet_mass_kg':md,'one_droplet_phase_energy_pJ':phase*1e12,'ideal_vapor_radius_1atm_um':av*1e6,'PFH_droplet_equivalents_8um':Nb,'PFH_phase_energy_8um_nJ':Nb*phase*1e9,'required_number_density_m3':Nb/Veff,'required_liquid_fraction':Nb*vd/Veff,'ideal_vapor_fraction_in_effective_volume':4*math.pi*Rmax**3/(3*Veff),
        'gel_G_kPa':G/1e3,'gel_G_over_Delta_p':G/dp,'gel_neoHookean_elastic_pressure_8um_kPa':pel/1e3,'gel_large_expansion_pressure_kPa':2.5*G/1e3,'gel_elastic_work_1_to_8um_nJ':Wgel*1e9,'gel_shear_speed_m_s':math.sqrt(G/rho_g),'gel_shear_crossing_8um_us':Rmax/math.sqrt(G/rho_g)*1e6,
        'paper_input_energy_20ms_mJ':3.64*.020*1e3,'paper_absorbed_energy_20ms_mJ':(.34+.26)*.020*1e3,'paper_absorbed_to_project_ratio':(.34+.26)*.020/Eabs,
        'PDMS_Si_complete_area_work_nJ':.98*(400e-6)**2*1e9,'project_energy_at_10percent_use_nJ':.1*Eabs*1e9,
        'Laplace_250nm_kPa':2*sigma/a/1e3,'ideal_wall_speed_half_radius_m_s':math.sqrt(2*dp/(3*rho)*(2**3-1)), 'ideal_wall_speed_tenth_radius_m_s':math.sqrt(2*dp/(3*rho)*(10**3-1)),
        'ideal_R_fraction_at_Mach_0p1':(1+3*rho*(.1*c)**2/(2*dp))**(-1/3),
        'PV_energy_radius_ceiling_eta_0p01_um':(3*.01*Eabs/(4*math.pi*dp))**(1/3)*1e6,
        'rectangular_linear_pressure_energy_ceiling_1mm_50ns_eta_0p01_kPa':math.sqrt(.01*Eabs*rho*c/(4*math.pi*(1e-3)**2*50e-9))/1e3,
        'dynamic_pressure_U1400_MPa':.5*rho*1400**2/1e6,'linear_waterhammer_U1400_MPa':rho*c*1400/1e6,'U1400_water_Mach':1400/c,
        'array_pitch_um':40.,'array_void_fraction_at_8um':(4*math.pi*Rmax**3/3)/(40e-6)**3,
        'array_equivalent_sphere_Rc_um':(3*27*(40e-6)**3/(4*math.pi))**(1/3)*1e6,
        'Gaussian_relative_fluence_axis40um':math.exp(-2*(40e-6)**2/w**2),'Gaussian_relative_fluence_corner40_40um':math.exp(-2*2*(40e-6)**2/w**2),
    }
    alpha=metrics['array_void_fraction_at_8um']; rc=metrics['array_equivalent_sphere_Rc_um']*1e-6
    metrics['array_cloud_interaction_B']=alpha*(rc/Rmax)**2
    Kl=rho*c*c; kappa=1.4
    # A constant-mass equilibrium gas example. Not a phase-changing PFC wave speed.
    pg_eq=pinf-pv+2*sigma/Rmax
    rho_mix=(1-alpha)*rho
    Keff=1/((1-alpha)/Kl+alpha/(kappa*pg_eq))
    metrics['Wood_equilibrium_example_sound_speed_m_s']=math.sqrt(Keff/rho_mix)
    (OUT/'metrics.json').write_text(json.dumps(metrics,indent=2,ensure_ascii=False),encoding='utf-8')
    geometries_data=geometries()
    coupled=[]; verification=[]
    for name, xyz in geometries_data.items():
        row, times=cluster_run(xyz)
        coarse,_=cluster_run(xyz,rtol=1e-8,max_step=.003,samples=1201)
        row['geometry']=name
        if len(xyz)<6:
            dists=np.linalg.norm(xyz[0]-xyz[1:],axis=1)
            chi=float(np.sum(Rmax/dists)) if len(xyz)>1 else 0
            coefficient=math.sqrt(3/2)*quad(lambda x:x**1.5*math.sqrt((1+chi*x)/(1-x**3)),0,1,epsabs=2e-12)[0]
            row.update({'chi_at_Rmax':chi,'formal_ideal_collapse_coefficient':coefficient,'formal_ideal_collapse_time_us':coefficient*t_scale*1e6})
        write_csv(name+'_radius_history.csv',times)
        coupled.append(row)
        verification.append({'geometry':name,'energy_residual_relative':row['energy_residual_relative'],'cutoff_time_relative_change':abs(row['time_to_cutoff_us']-coarse['time_to_cutoff_us'])/row['time_to_cutoff_us'],'pressure_peak_relative_change':abs(row['far_linear_pressure_max_Pa']-coarse['far_linear_pressure_max_Pa'])/max(1,abs(row['far_linear_pressure_max_Pa']))})
    write_csv('coupled_bubble_summary.csv',coupled)
    write_csv('convergence_and_energy.csv',verification)
    gas=[km_gas_bracket(pg) for pg in [1000.,10000.,50000.]]
    write_csv('pedagogical_gas_brackets.csv',gas)
    energy=[{'effective_8um_bubbles':n,'required_PFH_droplet_equivalents':n*Nb,'phase_energy_nJ':n*Nb*phase*1e9,'phase_energy_fraction_of_Eabs':n*Nb*phase/Eabs} for n in [1,3,4,5,27]]
    write_csv('fixed_total_energy_inventory.csv',energy)
    checks={
        'Rayleigh_quadrature_beta_relative_error':abs(pref-pref_beta)/pref_beta,
        'optical_expected_Eabs_relative_error':abs(Eabs-2.945243112740431e-7)/Eabs,
        'maximum_cluster_energy_residual':max(q['energy_residual_relative'] for q in verification),
        'maximum_cluster_cutoff_convergence':max(q['cutoff_time_relative_change'] for q in verification),
        'maximum_cluster_pressure_sample_convergence':max(q['pressure_peak_relative_change'] for q in verification),
        'three_to_five_formal_collapse_slower_than_single':all(q['formal_ideal_collapse_time_us']>tR*1e6 for q in coupled if 3<=q['count']<=5),
    }
    assert checks['Rayleigh_quadrature_beta_relative_error']<1e-9
    assert checks['optical_expected_Eabs_relative_error']<1e-9
    assert checks['maximum_cluster_energy_residual']<1e-7
    assert checks['maximum_cluster_cutoff_convergence']<1e-6
    assert checks['maximum_cluster_pressure_sample_convergence']<.01
    assert checks['three_to_five_formal_collapse_slower_than_single']
    (OUT/'verification.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
    print(json.dumps({'metrics':metrics,'clusters':coupled,'gas_brackets':gas,'verification':checks},indent=2,ensure_ascii=False))

if __name__=='__main__': main()
