"""Solve a finite, uniformly forced bubble cloud in the conditional linear limit.

Time convention: Re[p_hat exp(-i omega t)]. The inside and outside carrier
density are equal. A measured PFC susceptibility can replace the illustrative
fixed-mass gas law. This does NOT simulate optical activation or collapse.
Run: python -B analysis/finite_uniform_cloud.py (NumPy, SciPy required).
"""
from pathlib import Path
import csv
import json
import math
import numpy as np
from scipy.integrate import quad
from scipy.special import spherical_jn

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'analysis/extension-results'
M = json.loads((OUT/'metrics.json').read_text(encoding='utf-8'))
C = json.loads((ROOT/'reading/extension-sources/Inherited_Baseline_20261006.json').read_text(encoding='utf-8'))
rho = C['carrier']['density_kg_m3']['value']
c = C['carrier']['sound_speed_m_s']['value']
sigma = C['carrier']['surface_tension_N_m']['value']
pv = C['carrier']['equilibrium_vapor_pressure_Pa']['value']
Re = C['bubble_source']['maximum_radius_m']['value']
Rc = M['array_equivalent_sphere_Rc_um']*1e-6
nb = 1/(40e-6)**3
pg = 101325-pv+2*sigma/Re
kappa = 1.4
omega0 = math.sqrt((3*kappa*pg-2*sigma/Re)/(rho*Re**2))
beta_loss = 0.1*omega0  # Declared teaching damping, not measured PFC data.
alpha_drive = 1e-7  # Small, imposed harmonic void perturbation, not nucleation.
observer = 1e-3


def solution(omega, chi=0j):
    """Inside p=p0+A*j0(kin*r); outside pb*Rc/r*exp(ikl*(r-Rc))."""
    kl = omega/c
    kin = np.sqrt(complex(kl**2-rho*nb*omega**2*chi))
    z = kin*Rc
    j0 = spherical_jn(0,z)
    dj = kin*spherical_jn(0,z,derivative=True)
    q = 1j*kl-1/Rc
    D = dj-q*j0
    p0 = rho*omega**2*alpha_drive/(kin**2)
    A = q*p0/D
    pb = p0*dj/D
    pobs = pb*Rc/observer*np.exp(1j*kl*(observer-Rc))
    return pobs, p0, A, pb, kin, j0, dj, q


def gas_susceptibility(omega):
    return -4*math.pi*Re/(rho*(omega0**2-omega**2-2j*beta_loss*omega))


def direct_green(omega):
    """Independent volume quadrature for zero bubble-pressure feedback."""
    k = omega/c
    def integrand(s):
        if s == 0:
            return 0j
        a = observer-s
        b = observer+s
        inner = (np.exp(1j*k*b)-np.exp(1j*k*a))/(1j*k*observer*s)
        return 2*math.pi*s*s*inner
    real = quad(lambda s:integrand(s).real,0,Rc,epsabs=1e-18,epsrel=1e-10)[0]
    imag = quad(lambda s:integrand(s).imag,0,Rc,epsabs=1e-18,epsrel=1e-10)[0]
    return -rho*omega**2*alpha_drive*(real+1j*imag)/(4*math.pi)


def main():
    rows=[]
    matching=[]
    amplitudes=[]
    for f in np.geomspace(1e4,5e6,801):
        w=2*math.pi*f
        chi=gas_susceptibility(w)
        p,p0,A,pb,kin,j0,dj,q=solution(w,chi)
        pfree=solution(w)[0]
        matching.append(abs(A*dj-q*pb)/max(1e-30,abs(A*dj)))
        matching.append(abs(p0+A*j0-pb)/max(1e-30,abs(pb)))
        # Verify that the largest local volume perturbation is small.
        radii=np.linspace(0,Rc,201)
        p_inside=p0+A*spherical_jn(0,kin*radii)
        volume_hat=chi*p_inside+alpha_drive/nb
        fractional_wall_hat=np.abs(volume_hat)/(4*math.pi*Re**3)
        amplitudes.append(float(fractional_wall_hat.max()))
        rows.append({'frequency_Hz':float(f),'observer_distance_m':observer,
                     'pressure_amplitude_Pa':float(abs(p)),
                     'pressure_phase_rad':float(np.angle(p)),
                     'prescribed_no_feedback_amplitude_Pa':float(abs(pfree)),
                     'largest_fractional_radius_perturbation':amplitudes[-1]})
    with (OUT/'finite_uniform_cloud_frequency_response.csv').open('w',encoding='utf-8',newline='') as dest:
        writer=csv.DictWriter(dest,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    quadrature_errors=[]
    for f in [1e4,1e5,5e5,2e6,5e6]:
        w=2*math.pi*f
        actual=solution(w)[0]; expected=direct_green(w)
        quadrature_errors.append(abs(actual-expected)/abs(expected))
    peak=max(rows,key=lambda x:x['pressure_amplitude_Pa'])
    checks={'time_convention':'exp(-i omega t)',
            'closure':'illustrative fixed-mass equilibrium gas; NOT calibrated PFC',
            'alpha_drive_amplitude':alpha_drive,
            'gas_equilibrium_frequency_Hz':omega0/(2*math.pi),
            'assumed_beta_over_omega0':0.1,
            'same_carrier_density_inside_and_outside':True,
            'zero_feedback_direct_Green_quadrature_max_relative_error':float(max(quadrature_errors)),
            'pressure_and_normal_velocity_matching_max_relative_error':float(max(matching)),
            'largest_fractional_radius_perturbation':max(amplitudes),
            'sampled_maximum':peak}
    assert max(quadrature_errors)<1e-8
    assert max(matching)<1e-8
    assert max(amplitudes)<0.01
    (OUT/'finite_uniform_cloud_verification.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
    print(json.dumps(checks,indent=2))


if __name__=='__main__':main()
