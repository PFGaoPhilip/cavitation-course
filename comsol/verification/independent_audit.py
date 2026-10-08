"""Post-model verifier's independent archive, CSV and EOS calculations.

Owns verification/ only. Does not import the primary generated gate checker,
consume the gate JSON, change a model, or read a native radius into an ODE.
Run with Python -B; CoolProp is loaded from the project-owned installation.
"""
from pathlib import Path
import argparse, csv, hashlib, json, math, sys, zipfile
import xml.etree.ElementTree as ET
import numpy as np
from scipy.optimize import root, brentq
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.tools/coolprop'))
import CoolProp.CoolProp as CP


def load(name):
    return np.loadtxt(ROOT / 'data' / name, delimiter=',', comments='%')


def gas_metrics(a, ref):
    t, p, r = a[:, 3], a[:, 8], a[:, 10]
    ip = np.interp(t, ref[:, 0], ref[:, 4])
    ir = np.interp(t, ref[:, 0], ref[:, 1])
    # Reassemble energy from individual export columns, not the reported residual.
    total = np.sum(a[:, 14:20], axis=1)
    residual = (total - a[:, 7]) / a[:, 7]
    return {
        'rows': len(a), 'peak_Pa': float(p.max()), 'peak_time_s': float(t[p.argmax()]),
        'radius_min': float(r.min()), 'wall_Mach_max': float(np.abs(a[:, 11]).max()/1480),
        'max_energy_relative_residual_reassembled': float(np.abs(residual).max()),
        'reported_energy_residual_consistency': float(np.max(np.abs(residual-a[:, 20]))),
        'wave_error_over_reference_peak': float(np.abs(p-ip).max()/ref[:, 4].max()),
        'radius_error_over_initial_radius': float(np.abs(r-ir).max()),
        'reference_peak_error_relative': float(abs(p.max()/ref[:, 4].max()-1)),
        'gas_pressure_max_Pa': float(a[:, 12].max()),
    }


def pfp_metrics(a):
    # Every resolved source contributes twelve exported dynamic/phase columns.
    # The uniform population appends extra spatial diagnostics after the ledger.
    count=max(1,int((a.shape[1]-13)//12))
    ledger=6+12*count
    total = np.sum(a[:, ledger:ledger+6], axis=1)
    er = (total-a[:, 3])/a[:, 3]
    jump = 2*.00941/a[:, [12+12*j for j in range(count)]]
    cap=a[:, [16+12*j for j in range(count)]]
    return dict(rows=len(a),resolved_phase_states=count, peak_Pa=float(a[:, 4].max()),
                peak_time_s=float(a[a[:, 4].argmax(), 1]),
                energy_relative_residual=float(np.abs(er).max()),
                reported_energy_consistency=float(np.abs(er-a[:, ledger+6]).max()),
                capillary_jump_relative_error=float(np.abs(cap/jump).max()),
                liquid_pressure_relative_error=float(np.abs(cap/a[:, [8+12*j for j in range(count)]]).max()),
                max_scaled_entropy_error=float(np.abs(a[:, [15+12*j for j in range(count)]]).max()),
                max_Gibbs_residual_J_kg=float(np.abs(a[:, [17+12*j for j in range(count)]]).max()),
                min_radius_ratio=float(a[:, [6+12*j for j in range(count)]].min()),
                min_vapor_radius_over_floor=float(a[:, [12+12*j for j in range(count)]].min()/1e-9),
                min_shell_thickness_nm=float(a[:, [13+12*j for j in range(count)]].min()*1e9),
                max_T_K=float(a[:, [10+12*j for j in range(count)]].max()),
                min_fv=float(a[:, [11+12*j for j in range(count)]].min()),
                max_fv=float(a[:, [11+12*j for j in range(count)]].max()))


def archive_metadata(p, crc=False):
    with zipfile.ZipFile(p) as z:
        mi = ET.fromstring(z.read('modelinfo.xml'))
        dm = ET.fromstring(z.read('dmodel.xml'))
        sequences = []
        for s in dm.iter('SolverSequence'):
            info = s.find('SolutionInfo')
            lists = []
            for v in info.findall('pLists'):
                values = np.fromstring(v.text or '', sep=',')
                lists.append(dict(count=len(values), first=float(values[0]), last=float(values[-1]),
                                  all_finite=bool(np.isfinite(values).all())))
            sequences.append(dict(tag=s.get('tag'), study=s.findtext('study'),
                                  native=s.findtext('solutionnative'), names=info.findtext('pNames'),
                                  parameter_lists=lists))
        params = {p.get('param'): dict(value=p.get('value'), description=p.get('reference'))
                  for group in dm.iter('ModelParamGroup') for p in group.findall('param') if p.get('T') == '33'}
        ds = []
        for d in dm.iter('DatasetFeature'):
            if d.get('op') == 'Solution':
                props = {v.get('name'): v.get('Reference') or v.get('value') for v in d.findall('propertyValue')}
                if d.get('tag') in ['datacP', 'datacG', 'datac3', 'datac5', 'datacU', 'smallGasData',
                                    'uniformRefinedData', 'dset1', 'sensitivityData']:
                    ds.append(dict(tag=d.get('tag'), solution=props.get('p:solution'), comp=props.get('p:comp')))
        categories = {}
        for label, prefix in [('geometry', 'geometry'), ('mesh', 'mesh'), ('solution', 'solution'), ('xmesh', 'xmesh')]:
            f = [i for i in z.infolist() if i.filename.startswith(prefix) and i.filename.endswith('.mphbin')]
            categories[label] = dict(entries=len(f), total_bytes=sum(i.file_size for i in f))
        native_solutions=[]
        for n in dm.iter('SolutionNative'):
            names=n.findtext('pName')
            values=np.fromstring(n.findtext('tListReal') or '',sep=',')
            native_solutions.append(dict(tag=n.get('tag'), names=names,
                                        state_count=int((n.findtext('solnumDescriptions') or '0').split(',')[0]),
                                        degree_of_freedom_count=n.findtext('totalSize'),
                                        all_parameter_values_finite=bool(np.isfinite(values).all()),
                                        parameter_first_values=values[:10].tolist(),
                                        parameter_last_values=values[-4:].tolist(),
                                        actual_solution_block_count=len(n.findall('solutionBlock'))))
        crc_bad = z.testzip() if crc else 'not_requested'
        print('Archive metadata checked:',p.name,'CRC:',crc_bad,flush=True)
        sha=hashlib.sha256()
        if crc:
            with p.open('rb') as inp:
                for chunk in iter(lambda:inp.read(4*1024*1024),b''):sha.update(chunk)
        return dict(file=p.name, bytes=p.stat().st_size, mtime_ns=p.stat().st_mtime_ns,
                    sha256=sha.hexdigest() if crc else 'not_requested', comsol_version=mi.get('comsolVersion'),
                    node_type=mi.get('nodeType'), geometry=[g.attrib for g in mi.findall('./geometryInfo/geom')],
                    physics=mi.find('physicsInfo').attrib, archive_blocks=categories,
                    sequences=sequences, native_solutions=native_solutions, explicit_result_datasets=ds,
                    parameter_subset={k:params.get(k) for k in ['a','B','G','sig','sigLL','sigLV','kap','DP','tf','robs','adet','hdet','jetResolved']},
                    crc_bad_entry=crc_bad)


def independent_gas_ode(a, beta):
    """Separate dimensional Radau solve and independently integrated receiver response."""
    rho, c, p0, mu, sigma, kappa, b = 1000., 1480., 1e5, .001, .072, 1.4, 110e-6
    # f(t)=r*phi(r,t+(r-b)/c) and f' + c f/b = -c Q/(4*pi*b).
    # States R, U, f; dimensional form avoids the primary's nondimensional code.
    def rhs(t, y):
        R, U, f = y
        Q = 4*math.pi*R*R*U
        fd = -c*f/b - c*Q/(4*math.pi*b)
        phi_dt = fd/b
        pB = beta*p0*(a/R)**(3*kappa)-2*sigma/R-4*mu*U/R
        accel = ((pB-p0)/rho + phi_dt-(1.5-2*R/b)*U*U)/(R-R*R/b)
        return [U, accel, fd]
    sol = solve_ivp(rhs, (0, 8e-6), [a, 0., 0.], method='Radau',
                    rtol=2e-10, atol=[1e-15,1e-8,1e-15], max_step=1e-9, dense_output=True)
    if not sol.success:
        raise RuntimeError(sol.message)
    xx, wx = np.polynomial.legendre.leggauss(20)
    zz, wz = np.polynomial.legendre.leggauss(12)
    dist = np.sqrt(50e-6**2*(xx[:, None]+1)/2+(0.5e-3+2.5e-6*zz[None, :])**2).ravel()
    weights = (wx[:, None]*wz[None, :]/4).ravel()
    tau_f = 1/(2*math.pi*1e6)
    def obs(t):
        delay = t-(dist-b)/c
        y = sol.sol(np.maximum(delay, 0))
        fd = -c*y[2]/b-c*y[0]**2*y[1]/b
        return float(np.sum(weights*np.where(delay >= 0, -rho*fd/dist, 0.)))
    filt = solve_ivp(lambda t,y: [(obs(t)-y[0])/tau_f], (0,8e-6), [0.],
                     rtol=1e-9, atol=1e-6, max_step=1e-9, dense_output=True)
    ts=np.arange(0,8e-6+.1e-9,.5e-9)
    pr=filt.sol(ts)[0]
    return dict(method='Independent dimensional Radau + continuous filtered volume-quadrature receiver',
                peak_Pa=float(pr.max()), peak_time_s=float(ts[pr.argmax()]),
                radius_min=float(sol.sol(ts)[0].min()/a), success=bool(sol.success and filt.success))


def eos_checks(fine):
    fluid='n-Perfluoropentane'; a=300e-9; G=1e4; p0=1e5; ll=.054; lv=.00941
    rho0=CP.PropsSI('Dmass','T|liquid',293.15,'P',p0+2*ll/a,fluid)
    u0=CP.PropsSI('Umass','T|liquid',293.15,'P',p0+2*ll/a,fluid)
    mass=rho0*4*math.pi*a**3/3
    rows=[]
    for row in fine:
        _,q,lam,T,pl,pv,rl,rv,fv,rg,shell,_,_,_,_,_,_,_,ws,_,area_ratio,*_ = row
        calc_rl=CP.PropsSI('Dmass','T|liquid',T,'P',pl,fluid)
        calc_rv=CP.PropsSI('Dmass','T|gas',T,'P',pv,fluid)
        gl=CP.PropsSI('Gmass','T|liquid',T,'P',pl,fluid)
        gv=CP.PropsSI('Gmass','T|gas',T,'P',pv,fluid)
        ul=CP.PropsSI('Umass','T|liquid',T,'P',pl,fluid)
        uv=CP.PropsSI('Umass','T|gas',T,'P',pv,fluid)
        vol=4*math.pi*(a*lam)**3/3
        A=area_ratio*4*math.pi*(a*lam)**2
        energy=mass*((1-fv)*ul+fv*uv-u0)+ws+p0*(vol-4*math.pi*a**3/3)+ll*(A-4*math.pi*a*a)+4*math.pi*lv*rg*rg
        rows.append(dict(Q_pJ=q*1e12, densityL_relative_difference=calc_rl/rl-1,
                         densityV_relative_difference=calc_rv/rv-1, Gibbs_residual_J_kg=gl-gv,
                         mass_volume_residual_relative=(mass*((1-fv)/calc_rl+fv/calc_rv)-vol)/vol,
                         energy_relative_residual_reassembled=energy/q-1,
                         gas_volume_mass_relative=4*math.pi*rg**3*calc_rv/(3*mass*fv)-1,
                         capillary_residual_Pa=pv-pl-2*lv/rg,
                         stretch_local_max=float(row[21]),
                         equivalent_proxy_pass=bool(lam<2.1), local_proxy_pass=bool(row[21]<2.1)))
    # Separate finite-phase equilibrium root; none of the native stretches seeds/constraints this solve.
    def calc_state(x):
        lam,T,logrg=x;rg=math.exp(logrg)
        pgel=G/2*(5-4/lam-lam**-4)
        pl=p0+pgel+2*ll/(a*lam);pv=pl+2*lv/rg
        rl=CP.PropsSI('Dmass','T|liquid',T,'P',pl,fluid)
        rv=CP.PropsSI('Dmass','T|gas',T,'P',pv,fluid)
        vl=(mass-rv*4*math.pi*rg**3/3)/rl
        ul=CP.PropsSI('Umass','T|liquid',T,'P',pl,fluid)
        uv=CP.PropsSI('Umass','T|gas',T,'P',pv,fluid)
        gl=CP.PropsSI('Gmass','T|liquid',T,'P',pl,fluid)
        gv=CP.PropsSI('Gmass','T|gas',T,'P',pv,fluid)
        ws=2*math.pi*G*a**3*(5*lam**3/3-2*lam*lam+1/lam-2/3)
        Q=(mass-rv*4*math.pi*rg**3/3)*ul+(rv*4*math.pi*rg**3/3)*uv-mass*u0+ws+p0*4*math.pi*a**3*(lam**3-1)/3+4*math.pi*(ll*a*a*(lam*lam-1)+lv*rg*rg)
        return [(vl+4*math.pi*rg**3/3)/(4*math.pi*(a*lam)**3/3)-1,(gl-gv)/1e5,(Q-11.65e-12)/11.65e-12]
    ans=root(calc_state,[2.,340.,math.log(570e-9)],tol=1e-10)
    if np.linalg.norm(calc_state(ans.x))>1e-8:
        raise RuntimeError('Independent gel phase root did not close')
    def phase_at(lam,T,rg,pl):
        pv=pl+2*lv/rg
        rl=CP.PropsSI('Dmass','T|liquid',T,'P',pl,fluid)
        rv=CP.PropsSI('Dmass','T|gas',T,'P',pv,fluid)
        gl=CP.PropsSI('Gmass','T|liquid',T,'P',pl,fluid)
        gv=CP.PropsSI('Gmass','T|gas',T,'P',pv,fluid)
        ul=CP.PropsSI('Umass','T|liquid',T,'P',pl,fluid)
        uv=CP.PropsSI('Umass','T|gas',T,'P',pv,fluid)
        vg=4*math.pi*rg**3/3
        ws=2*math.pi*G*a**3*(5*lam**3/3-2*lam*lam+1/lam-2/3)
        vol=4*math.pi*(a*lam)**3/3
        energy=(mass-rv*vg)*ul+rv*vg*uv-mass*u0+ws+p0*(vol-4*math.pi*a**3/3)+4*math.pi*(ll*a*a*(lam*lam-1)+lv*rg*rg)
        return [(gl-gv)/1e5,((mass-rv*vg)/rl+vg)/vol-1,(energy-11.65e-12)/11.65e-12]
    lam0,T0,logrg=ans.x
    pl0=p0+G/2*(5-4/lam0-lam0**-4)+2*ll/(a*lam0)
    slopes={}
    for mode in ['fixed_temperature','closed_total_energy']:
        net=[]
        for lm in [lam0-2e-5,lam0+2e-5]:
            def perturb(x):
                if mode=='fixed_temperature': return phase_at(lm,T0,math.exp(x[0]),math.exp(x[1]))[:2]
                return phase_at(lm,x[0],math.exp(x[1]),math.exp(x[2]))
            seed=[logrg,math.log(pl0)] if mode=='fixed_temperature' else [T0,logrg,math.log(pl0)]
            p=root(perturb,seed,tol=1e-10)
            if np.linalg.norm(perturb(p.x))>1e-8:raise RuntimeError('Independent perturbation failed')
            net.append(math.exp(p.x[-1])-p0-G/2*(5-4/lm-lm**-4)-2*ll/(a*lm))
        slopes[mode+'_restoring_Pa_per_unit_stretch']=float(-(net[1]-net[0])/4e-5)
    def liquid(T):
        def mass_eq(lam):
            pp=p0+G/2*(5-4/lam-lam**-4)+2*ll/(a*lam)
            rho=CP.PropsSI('Dmass','T|liquid',T,'P',pp,fluid)
            return rho*4*math.pi*(a*lam)**3/(3*mass)-1
        lm=brentq(mass_eq,.98,1.2,xtol=1e-13)
        pp=p0+G/2*(5-4/lm-lm**-4)+2*ll/(a*lm)
        ul=CP.PropsSI('Umass','T|liquid',T,'P',pp,fluid)
        ws=2*math.pi*G*a**3*(5*lm**3/3-2*lm*lm+1/lm-2/3)
        Q=mass*(ul-u0)+ws+p0*4*math.pi*a**3*(lm**3-1)/3+4*math.pi*ll*a*a*(lm*lm-1)
        return pp,Q,lm
    onset=brentq(lambda T: CP.PropsSI('P','T',T,'Q',0,fluid)-liquid(T)[0],300,380,xtol=1e-9)
    pp,Q,lm=liquid(onset)
    sensitivities=[]
    for row in load('gel_sensitivity3d_valid_control.csv'):
        case,q,Gs,sl,sv,lm,T,fv,rg,pl,pv,ws,ar,loc=[row[k] for k in [2,3,4,5,6,7,8,9,10,15,16,21,22,23]]
        rl=CP.PropsSI('Dmass','T|liquid',T,'P',pl,fluid)
        rv=CP.PropsSI('Dmass','T|gas',T,'P',pv,fluid)
        ul=CP.PropsSI('Umass','T|liquid',T,'P',pl,fluid)
        uv=CP.PropsSI('Umass','T|gas',T,'P',pv,fluid)
        gl=CP.PropsSI('Gmass','T|liquid',T,'P',pl,fluid)
        gv=CP.PropsSI('Gmass','T|gas',T,'P',pv,fluid)
        V=4*math.pi*(a*lm)**3/3; A=ar*4*math.pi*(a*lm)**2
        energy=mass*((1-fv)*ul+fv*uv-u0)+ws+p0*(V-4*math.pi*a**3/3)+sl*(A-4*math.pi*a*a)+4*math.pi*sv*rg*rg
        sensitivities.append(dict(case=int(case),Q_pJ=q*1e12,equivalent_stretch=lm,local_max_stretch=loc,
                                 complete_energy_relative_residual=energy/q-1,
                                 volume_mass_relative_residual=mass*((1-fv)/rl+fv/rv)/V-1,
                                 Gibbs_residual_J_kg=gl-gv,capillary_residual_Pa=pv-pl-2*sv/rg,
                                 equivalent_proxy_pass=bool(lm<2.1),local_proxy_pass=bool(loc<2.1)))
    return dict(CoolProp_version=CP.get_global_param_string('version'), cold_mass_kg=mass,
                cold_liquid_density_kg_m3=rho0, rows=rows,
                independent_11_65pJ_root=dict(stretch=float(ans.x[0]), T_K=float(ans.x[1]),
                                             vapor_radius_m=float(math.exp(ans.x[2])), residual_norm=float(np.linalg.norm(calc_state(ans.x)))),
                independent_11_65pJ_radial_stability=slopes,
                independent_liquid_bulk_saturation_lower_bound=dict(T_K=onset,Q_pJ=Q*1e12,stretch=liquid(onset)[2],pressure_Pa=pp),
                independently_recomposed_13pJ_sensitivity_states=sensitivities)


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--crc',action='store_true'); parser.add_argument('--ode',action='store_true')
    args=parser.parse_args()
    cases=json.loads((ROOT/'data/pressure_native_source_cases.json').read_text())
    gas=load('pressure_envelope_cG.csv');gasrows=[]
    for k in range(7):
        original=gas[np.isclose(gas[:,0],k)]
        authoritative=load('refined_gas_small.csv') if k==0 else original
        ref=np.loadtxt(ROOT/f'data/gas_reference_case_{k}.csv',delimiter=',',skiprows=1)
        info=gas_metrics(authoritative,ref);info['case_index']=k
        if k==0: info['excluded_coarse_result']=gas_metrics(original,ref)
        gasrows.append(info)
    ref=np.loadtxt(ROOT/'data/gas_reference_case_3.csv',delimiter=',',skiprows=1)
    worst_time=gas_metrics(load('worst_gas_time.csv'),ref)
    worst_mesh=gas_metrics(load('worst_gas_mesh.csv'),ref)
    pfp={name:pfp_metrics(load(file)) for name,file in [('single','pressure_envelope_cP.csv'),('three','pressure_envelope_c3.csv'),('five','pressure_envelope_c5.csv'),('uniform_coarse_excluded','pressure_envelope_cU.csv'),('uniform_refined_diagnostic','refined_phase_uniform.csv'),('five_enlarged_domain','five_pfp_domain.csv')]}
    u=load('refined_phase_uniform.csv');deviation=np.maximum(np.abs(u[:,27]-u[:,26]),np.abs(u[:,28]-u[:,26]))
    uniform_physical=dict(max_local_deviation_from_mean_Pa=float(deviation.max()),
                          minimum_gauge_pressure_Pa=float(u[:,28].min()),
                          minimum_absolute_pressure_Pa=float(u[:,28].min()+1e5),
                          verdict='REJECT unqualified common-state population prediction')
    fine=load('free_coreshell3d_fine_control.csv');coarse=load('free_coreshell3d_control.csv')
    # Rows have explicit paired source energies; same five cases on each mesh.
    mesh=dict(equivalent_stretch_max_relative_change=float(np.max(np.abs(fine[:,2]/coarse[:,2]-1))),
              local_stretch_max_relative_change=float(np.max(np.abs(fine[:,21]/coarse[:,21]-1))),
              elastic_pressure_vs_analytic_max_relative=float(np.max(np.abs(fine[:,16]/fine[:,17]-1))),
              elastic_work_vs_analytic_max_relative=float(np.max(np.abs(fine[:,18]/fine[:,19]-1))))
    tf=1/(2*math.pi*1e6);energy=max(q['energy_J'] for q in cases['gas'])
    bound=math.sqrt(1000*1480*energy/(8*math.pi*(.5e-3-2.5e-6)**2*tf))
    # Derivation: E >= 4*pi*r^2/(rho*c) integral p^2 dt,
    # |h*p| <= ||h||_2 ||p||_2; ||h||_2^2=1/(2*tau_f).
    changes=dict(worst_time_peak=float(abs(worst_time['peak_Pa']/gasrows[3]['peak_Pa']-1)),
                 worst_mesh_peak=float(abs(worst_mesh['peak_Pa']/gasrows[3]['peak_Pa']-1)),
                 five_outer_domain_peak=float(abs(pfp['five_enlarged_domain']['peak_Pa']/pfp['five']['peak_Pa']-1)),
                 uniform_time_peak=float(abs(pfp['uniform_refined_diagnostic']['peak_Pa']/pfp['uniform_coarse_excluded']['peak_Pa']-1)))
    result=dict(reviewer='Independent post-model subagent /root/independent_model_verifier',
                no_primary_gate_JSON_consumed=True,
                model_archives=[archive_metadata(p,args.crc) for p in sorted((ROOT/'final').glob('*.mph'))],
                authoritative_gas_cases=gasrows,worst_time=worst_time,worst_mesh=worst_mesh,
                PFP=pfp,uniform_physical=uniform_physical,gel_mesh=mesh,
                gel_independent_EOS=eos_checks(fine),refinement_peak_changes=changes,
                spherical_progressive_wave_filtered_bound_Pa=bound,
                input_inventory_comparison=dict(Model_A_cold_PFP_radii_um=[q['cold_liquid_radius_m']*1e6 for q in cases['PFP']],
                                                Model_A_PFP_per_source_mass_kg=[q['mass_kg'] for q in cases['PFP']],
                                                Model_B_cold_radius_um=.3),
                thermal_times=dict(thermal_s=(300e-9)**2/(.6/(1006.5*4180)),
                                   inertial_s=300e-9*math.sqrt(1006.5/1e4)))
    # Metadata and CRCs do not change when only this verifier fixes a CSV parser.
    # Preserve earlier CRC/SHA results only if the corresponding file sizes and
    # modification timestamps have not changed since the full audit.
    old_path=ROOT/'verification/INDEPENDENT_AUDIT.json'
    if not args.crc and old_path.exists():
        old=json.loads(old_path.read_text())
        for record in result['model_archives']:
            previous=next((q for q in old.get('model_archives',[]) if q['file']==record['file']),None)
            if previous and previous['bytes']==record['bytes'] and previous.get('mtime_ns')==record['mtime_ns'] and previous.get('crc_bad_entry') is None:
                record['crc_bad_entry']=None
                record['sha256']=previous['sha256']
                record['CRC_provenance']='Preserved earlier full-member CRC run; no final MPH file changes during verifier-only CSV parser correction.'
    gas_path=ROOT/'verification/DIMENSIONAL_GAS_REFERENCE.json'
    if args.ode:
        result['independent_dimensional_gas_solution']=independent_gas_ode(cases['gas'][3]['a_m'],.05)
        gas_path.write_text(json.dumps(result['independent_dimensional_gas_solution'],indent=2),encoding='utf8')
    elif gas_path.exists():
        result['independent_dimensional_gas_solution']=json.loads(gas_path.read_text())
    input_files=[*sorted((ROOT/'data').glob('pressure_envelope_c*.csv')),ROOT/'data/free_coreshell3d_fine_control.csv',
                 ROOT/'data/free_coreshell3d_control.csv',ROOT/'data/gel_sensitivity3d_valid_control.csv',
                 ROOT/'data/refined_gas_small.csv',ROOT/'data/refined_phase_uniform.csv',
                 ROOT/'data/worst_gas_time.csv',ROOT/'data/worst_gas_mesh.csv',ROOT/'data/five_pfp_domain.csv']
    result['input_SHA256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in input_files}
    (ROOT/'verification/INDEPENDENT_AUDIT.json').write_text(json.dumps(result,indent=2),encoding='utf8')
    print(json.dumps({k:result[k] for k in ['refinement_peak_changes','uniform_physical','gel_mesh','spherical_progressive_wave_filtered_bound_Pa','thermal_times']},indent=2))
    print('Independent result saved:',ROOT/'verification/INDEPENDENT_AUDIT.json')


if __name__=='__main__': main()
