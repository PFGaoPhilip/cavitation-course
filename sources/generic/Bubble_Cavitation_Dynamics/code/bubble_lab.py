"""Reproducible teaching models for Bubble Cavitation Dynamics.

SI units at the public interface; dimensionless integration internally.
Models: incompressible Rayleigh--Plesset (RP), constant-ambient
Keller--Miksis (KM), and an empty-cavity Rayleigh benchmark.
NOT a nucleation, thermal phase-change, jetting, shock-resolving, or FSI solver.
"""
from __future__ import annotations
from dataclasses import dataclass, replace, asdict
from pathlib import Path
import argparse
import json
import platform
import numpy as np
import scipy
from scipy.integrate import solve_ivp, quad, cumulative_trapezoid
from scipy.interpolate import CubicSpline

@dataclass(frozen=True)
class Parameters:
    rho: float = 998.0
    mu: float = 1.0e-3
    sigma: float = 0.072
    p0: float = 101325.0
    pv: float = 2339.0
    c: float = 1481.0
    kappa: float = 1.4
    R0: float = 10.0e-6

    def validate(self) -> None:
        if not all(np.isfinite(v) for v in asdict(self).values()):
            raise ValueError('All parameters must be finite.')
        if min(self.rho, self.c, self.kappa, self.R0) <= 0:
            raise ValueError('rho, c, kappa and R0 must be positive.')
        if min(self.mu, self.sigma, self.pv) < 0 or self.p0 <= self.pv:
            raise ValueError('Require mu,sigma,pv >= 0 and p0 > pv.')
        if 3*self.kappa*self.pg0-2*self.sigma/self.R0 <= 0:
            raise ValueError('Reference equilibrium must have positive radial stiffness.')

    @property
    def pg0(self) -> float:
        return self.p0 - self.pv + 2.0*self.sigma/self.R0

    @property
    def speed_scale(self) -> float:
        return np.sqrt((self.p0-self.pv)/self.rho)

    @property
    def omega0(self) -> float:
        return np.sqrt((3*self.kappa*self.pg0-2*self.sigma/self.R0)
                       /(self.rho*self.R0**2))


def acceleration(R: float | np.ndarray, U: float | np.ndarray,
                 p: Parameters, model: str = 'RP') -> float | np.ndarray:
    """Constant-ambient radial acceleration; no radius or pressure clipping.

    pL is the LIQUID pressure immediately outside the interface.
    The viscous acceleration term in dpL/dt is moved to the KM denominator.
    """
    if np.any(np.asarray(R) <= 0):
        raise ValueError('Nonpositive trial radius: outside model domain. '
                         'Increase the stop radius or reduce the step size.')
    pg = p.pg0*(p.R0/R)**(3*p.kappa)
    pL = pg+p.pv-2*p.sigma/R-4*p.mu*U/R
    if model.upper() == 'RP':
        return ((pL-p.p0)/p.rho-1.5*U**2)/R
    if model.upper() != 'KM':
        raise ValueError('model must be RP or KM')
    # dpL/dt = D - (4 mu/R) dU/dt, for constant pv and material properties.
    D = -3*p.kappa*pg*U/R + 2*p.sigma*U/R**2 + 4*p.mu*U**2/R**2
    denominator = R*(1-U/p.c)+4*p.mu/(p.rho*p.c)
    if np.any(np.asarray(denominator) <= 0):
        raise ValueError('KM denominator is nonpositive; approximation invalid.')
    numerator = ((1+U/p.c)*(pL-p.p0)/p.rho + R*D/(p.rho*p.c)
                 -1.5*(1-U/(3*p.c))*U**2)
    return numerator/denominator


def simulate(p: Parameters = Parameters(), model: str = 'RP',
             radius_factor: float = 1.5, cycles: float = 6.0,
             rtol: float = 1e-9, atol: float = 1e-11,
             min_radius_factor: float = 0.05,
             mach_stop: float = 0.10, points: int = 8001) -> dict:
    """Free oscillations starting at R=radius_factor*R0 and U=0.

    A radius guard and a conservative Mach-number guard terminate integration.
    The 0.10 Mach guard is a teaching diagnostic, NOT a universal error bound.
    It deliberately limits both RP and KM rather than trusting violent collapse.
    """
    p.validate()
    if radius_factor <= min_radius_factor or cycles <= 0 or points < 3:
        raise ValueError('Invalid initial radius, duration, or sample count.')
    if not (0 < min_radius_factor < 1 and 0 < mach_stop < 1):
        raise ValueError('Radius and Mach guards must lie between zero and one.')
    if min(rtol, atol) <= 0:
        raise ValueError('Tolerances must be positive.')
    T0 = 2*np.pi/p.omega0
    ts = p.R0/p.speed_scale
    tau_end = cycles*T0/ts
    def rhs(tau, z):
        R, U = z[0]*p.R0, z[1]*p.speed_scale
        return [z[1], acceleration(R, U, p, model)*p.R0/p.speed_scale**2]
    def radius_guard(tau, z):
        return z[0]-min_radius_factor
    def mach_guard(tau, z):
        return mach_stop-abs(z[1]*p.speed_scale)/p.c
    radius_guard.terminal = True
    radius_guard.direction = -1
    mach_guard.terminal = True
    mach_guard.direction = -1
    sol = solve_ivp(rhs, (0, tau_end), [radius_factor, 0.0], method='DOP853',
                    rtol=rtol, atol=atol, dense_output=True,
                    events=(radius_guard, mach_guard),
                    max_step=(T0/ts)/120)
    if not sol.success:
        raise RuntimeError(sol.message)
    tau = np.linspace(0, sol.t[-1], points)
    z = sol.sol(tau)
    R, U, t = z[0]*p.R0, z[1]*p.speed_scale, tau*ts
    A = acceleration(R, U, p, model)
    stop = 'completed'
    if len(sol.t_events[0]):
        stop = 'radius_guard'
    if len(sol.t_events[1]):
        stop = 'mach_guard'
    return dict(t=t, R=R, U=U, A=A, max_mach=float(np.max(np.abs(U)/p.c)),
                stop=stop, nfev=int(sol.nfev), period_linear=T0,
                parameters=asdict(p), model=model.upper())


def conservative_energy(R, U, p: Parameters):
    """RP mechanical energy for a reversible fixed-polytrope gas closure.

    The gas term equals ideal-gas internal energy only for an adiabatic gas
    with kappa equal to its heat-capacity ratio. Additive constants are arbitrary.
    """
    V = 4*np.pi*R**3/3
    V0 = 4*np.pi*p.R0**3/3
    pg = p.pg0*(p.R0/R)**(3*p.kappa)
    if np.isclose(p.kappa, 1.0):
        Wgas = -p.pg0*V0*np.log(V/V0)
    else:
        Wgas = pg*V/(p.kappa-1)
    return 2*np.pi*p.rho*R**3*U**2 + (p.p0-p.pv)*V + 4*np.pi*p.sigma*R**2 + Wgas


def rayleigh_benchmark(cutoff: float = 0.05) -> dict:
    """Dimensionless empty-cavity collapse, tau=t sqrt(Delta p/rho)/Rmax."""
    if not 0.005 <= cutoff < 1:
        raise ValueError('Use 0.005 <= cutoff < 1; never integrate to R=0.')
    integrand = lambda x: np.sqrt(1.5)*x**1.5/np.sqrt(1-x**3)
    tc, _ = quad(integrand, 0, 1, epsabs=1e-12)
    tcut, _ = quad(integrand, cutoff, 1, epsabs=1e-12)
    def rhs(t, z):
        x, v = z
        if x <= 0:
            raise ValueError('Rayleigh benchmark left its domain.')
        return [v, (-1-1.5*v*v)/x]
    def guard(t, z):
        return z[0]-cutoff
    guard.terminal = True
    guard.direction = -1
    sol = solve_ivp(rhs, (0, 1), [1, 0], method='DOP853', rtol=1e-10,
                    atol=1e-12, max_step=0.002, dense_output=True, events=guard)
    if not sol.success or not len(sol.t_events[0]):
        raise RuntimeError('Rayleigh benchmark failed to reach the cutoff.')
    t = np.linspace(0, sol.t[-1], 3001)
    x, v = sol.sol(t)
    return dict(tau=t, x=x, v=v, collapse_constant=tc, cutoff=cutoff,
                exact_cutoff_time=tcut, numerical_cutoff_time=sol.t[-1],
                relative_cutoff_error=abs(sol.t[-1]-tcut)/tcut)


def verification() -> dict:
    """Run deterministic checks. Failure raises AssertionError."""
    p = Parameters()
    reports = {}
    for model in ('RP', 'KM'):
        r = simulate(p, model, radius_factor=1, cycles=3)
        err = float(np.max(abs(r['R']/p.R0-1)))
        assert err < 1e-9, (model, err)
        reports[f'{model}_equilibrium_max_relative_radius_error'] = err
    q = replace(p, mu=0)
    r = simulate(q, 'RP', radius_factor=1.001, cycles=8, points=16001)
    spline = CubicSpline(r['t'], r['U'])
    roots = spline.roots(extrapolate=False)
    maxima = roots[(roots > 0.05*r['period_linear']) & (spline(roots, 1) < 0)]
    T = float(np.mean(np.diff(maxima)))
    err = abs(T/(2*np.pi/q.omega0)-1)
    assert err < 8e-4, err
    reports['small_amplitude_period_relative_error'] = err
    r = simulate(q, 'RP', radius_factor=1.5, cycles=5)
    E = conservative_energy(r['R'], r['U'], q)
    err = float(np.max(abs(E-E[0]))/abs(E[0]))
    assert err < 1e-7, err
    reports['inviscid_RP_energy_relative_drift'] = err
    r = simulate(p, 'RP', radius_factor=1.5, cycles=5, points=24001)
    E = conservative_energy(r['R'], r['U'], p)
    dissip = cumulative_trapezoid(16*np.pi*p.mu*r['R']*r['U']**2, r['t'], initial=0)
    err = float(np.max(abs(E-E[0]+dissip))/abs(E[0]))
    assert err < 1e-6, err
    reports['viscous_RP_energy_balance_relative_residual'] = err
    q = replace(p, c=1e12)
    a = simulate(q, 'RP', radius_factor=1.5, cycles=3)
    b = simulate(q, 'KM', radius_factor=1.5, cycles=3)
    err = float(np.max(abs(a['R']-b['R']))/q.R0)
    assert err < 1e-6, err
    reports['KM_infinite_sound_speed_max_radius_difference_over_R0'] = err
    a = simulate(p, 'KM', radius_factor=1.8, cycles=6, rtol=1e-7, atol=1e-9)
    b = simulate(p, 'KM', radius_factor=1.8, cycles=6, rtol=1e-10, atol=1e-12)
    err = float(np.max(abs(a['R']-b['R']))/p.R0)
    assert err < 1e-5, err
    reports['KM_tolerance_refinement_max_radius_difference_over_R0'] = err
    rb = rayleigh_benchmark()
    assert rb['relative_cutoff_error'] < 1e-7
    reports['Rayleigh_collapse_constant'] = rb['collapse_constant']
    reports['Rayleigh_cutoff_time_relative_error'] = rb['relative_cutoff_error']
    strong = simulate(p, 'KM', radius_factor=10, cycles=20)
    assert strong['stop'] == 'mach_guard', strong['stop']
    reports['strong_collapse_stop_reason'] = strong['stop']
    reports['strong_collapse_terminal_Mach'] = strong['max_mach']
    reports['environment'] = dict(python=platform.python_version(),
                                  numpy=np.__version__, scipy=scipy.__version__)
    reports['all_checks_passed'] = True
    return reports


def export_data(output_dir: str | Path) -> dict:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    results = verification()
    (out/'verification.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
    p = Parameters()
    for model in ('RP', 'KM'):
        r = simulate(p, model, radius_factor=1.8, cycles=6)
        data = np.column_stack([r['t'],r['R'],r['U'],r['A']])
        np.savetxt(out/f'{model.lower()}_ringdown.csv', data, delimiter=',',
                   header='time_s,radius_m,wall_velocity_m_per_s,wall_acceleration_m_per_s2', comments='')
        results[f'{model}_ringdown_max_Mach'] = r['max_mach']
    rb = rayleigh_benchmark()
    np.savetxt(out/'rayleigh_dimensionless.csv',
               np.column_stack([rb['tau'],rb['x'],rb['v']]), delimiter=',',
               header='tau,R_over_Rmax,velocity_over_sqrt_DeltaP_over_rho', comments='')
    (out/'verification.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
    return results


def make_plots(root: str | Path) -> None:
    """Independent Matplotlib figures using its default colors, no subplots."""
    import matplotlib.pyplot as plt
    root = Path(root)
    out = root/'figures'
    out.mkdir(parents=True, exist_ok=True)
    p = Parameters()
    def finish(name):
        plt.tight_layout()
        plt.savefig(out/f'{name}.pdf', bbox_inches='tight')
        plt.savefig(out/f'{name}.png', dpi=190, bbox_inches='tight')
        plt.close()
    rb = rayleigh_benchmark()
    plt.figure(figsize=(6.6,3.9))
    plt.plot(rb['tau']/rb['collapse_constant'], rb['x'])
    plt.xlabel(r'$t/t_c$')
    plt.ylabel(r'$R/R_{\max}$')
    plt.title('Empty-cavity collapse: stop before the singularity')
    plt.grid(True, alpha=0.3)
    finish('rayleigh_collapse')
    plt.figure(figsize=(6.6,3.9))
    for model in ('RP','KM'):
        r = simulate(p, model, radius_factor=1.8, cycles=6)
        plt.plot(r['t']/r['period_linear'],r['R']/p.R0,label=model)
    plt.xlabel(r'$t/T_0$')
    plt.ylabel(r'$R/R_0$')
    plt.title('Free nonlinear ringdown: identical initial states')
    plt.legend(); plt.grid(True, alpha=0.3)
    finish('rp_km_ringdown')
    x = np.linspace(0.75,20,1600)
    q = replace(p,R0=5e-6,kappa=1)
    peq = q.pv+q.pg0*x**(-3)-2*q.sigma/(q.R0*x)
    xb = np.sqrt(3*q.pg0*q.R0/(2*q.sigma))
    pb = q.pv-4*q.sigma/(3*q.R0*xb)
    plt.figure(figsize=(6.6,3.9))
    plt.plot(x,peq/1000,label='Isothermal equilibrium curve')
    plt.plot([xb],[pb/1000],marker='o',linestyle='none',label='Blake turning point')
    plt.axhline(q.pv/1000,linestyle=':',label='Vapor pressure')
    plt.ylim(-6,30); plt.xlabel(r'$R/R_0$'); plt.ylabel('Absolute pressure (kPa)')
    plt.title('A gas nucleus has a stability limit, not just a boiling point')
    plt.legend(); plt.grid(True, alpha=0.3)
    finish('blake_equilibrium')
    ratio = np.linspace(0.05,2.5,1200)
    plt.figure(figsize=(6.6,3.9))
    for zeta in (0.05,0.10,0.20):
        response = 1/np.sqrt((1-ratio**2)**2+(2*zeta*ratio)**2)
        plt.plot(ratio,response,label=rf'$\zeta={zeta:.2f}$')
    plt.xlabel(r'$\omega/\omega_0$'); plt.ylabel('Amplitude / static displacement')
    plt.title('Linear radial resonance: illustrative damping ratios')
    plt.legend(); plt.grid(True, alpha=0.3)
    finish('linear_resonance')
    R = np.geomspace(1e-6,1e-3,400)
    plt.figure(figsize=(6.6,3.9))
    plt.loglog(R*1e6,0.914681*R/p.speed_scale*1e6,label='Rayleigh collapse')
    plt.loglog(R*1e6,np.sqrt(p.rho*R**3/p.sigma)*1e6,label='Capillary time')
    plt.loglog(R*1e6,R/p.c*1e6,label='Acoustic transit')
    plt.xlabel('Radius (micrometers)'); plt.ylabel('Time (microseconds)')
    plt.title('Competing times: teaching water parameter set')
    plt.legend(); plt.grid(True, which='both', alpha=0.3)
    finish('time_scales')
    r = simulate(p,'KM',radius_factor=1.8,cycles=3)
    observer_distance = 1e-2
    prad = p.rho/observer_distance*(r['R']**2*r['A']+2*r['R']*r['U']**2)
    plt.figure(figsize=(6.6,3.9))
    plt.plot((r['t']+observer_distance/p.c)*1e6,prad)
    plt.xlabel('Approximate observer time (microseconds)')
    plt.ylabel('Acoustic pressure perturbation (Pa)')
    plt.title('Leading monopole estimate at 10 mm; not a resolved shock')
    plt.grid(True, alpha=0.3)
    finish('monopole_pressure')
    tau = np.linspace(0,14,1500)
    plt.figure(figsize=(6.6,3.9))
    for theta in (0.2,1.0,5.0):
        response = np.where(tau<theta,(1-np.cos(tau))/theta,
                           (np.cos(tau-theta)-np.cos(tau))/theta)
        plt.plot(tau,response,label=rf'$\omega_n\tau_p={theta:g}$')
    plt.xlabel(r'$\omega_n t$'); plt.ylabel(r'$\omega_n q/(I_n/M_n)$')
    plt.title('One structural mode: equal impulse, different pulse durations')
    plt.legend(); plt.grid(True, alpha=0.3)
    finish('modal_impulse')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path(__file__).resolve().parents[1]/'data')
    parser.add_argument('--plots',action='store_true')
    args = parser.parse_args()
    report = export_data(args.output)
    if args.plots:
        make_plots(args.output.parent)
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
