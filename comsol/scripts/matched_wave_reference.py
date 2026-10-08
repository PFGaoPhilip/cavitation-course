"""Independent outgoing-spherical-wave solution of the matched near-field model.

The matching sphere is fixed. Its exact radiation impedance is a first-order
ODE; no COMSOL field or imposed radius trajectory enters this calculation.
"""
from pathlib import Path
import json
import numpy as np
from scipy.integrate import solve_ivp
from numpy.polynomial.legendre import leggauss

ROOT=Path(__file__).resolve().parents[1]
A=50e-6; B=2.; RHO=1000.; C=1480.; MU=1e-3; DP=1e5
BETA=.1; KAP=1.4; SIG=.072; ROBS=.5e-3; ADET=50e-6; HDET=5e-6
TAU=A*np.sqrt(RHO/DP); TF=1/(2*np.pi*1e6)

def rhs(x,y):
    r,w,h=y
    dh=-(TAU*C/(B*A))*(h+r*r*w/B)
    pb=BETA*r**(-3*KAP)-2*SIG/(A*DP*r)-4*MU*w/(TAU*DP*r)
    dw=(pb-1+dh-(1.5-2*r/B)*w*w)/(r-r*r/B)
    return [w,dw,dh]

def run(prefix='matched_wave_analytic_control',end=2.2,pressure_function=None):
    sol=solve_ivp(rhs,[0,end],[1,0,0],method='Radau',rtol=2e-10,
                  atol=1e-12,max_step=.002,dense_output=True)
    if not sol.success: raise RuntimeError(sol.message)
    gr,wr=leggauss(16); gz,wz=leggauss(8)
    # Map r^2 rather than r: normalized cylindrical-volume weights are uniform.
    rr2=ADET**2*(gr+1)/2
    zz=ROBS+HDET*gz/2
    dist=np.sqrt(rr2[:,None]+zz[None,:]**2).ravel()
    weight=(wr[:,None]*wz[None,:]/4).ravel()
    delay=(dist-B*A)/(C*TAU)
    def raw(x):
        earlier=x-delay
        y=sol.sol(np.maximum(0,earlier))
        hd=-(TAU*C/(B*A))*(y[2]+y[0]*y[0]*y[1]/B)
        pressure=-RHO*A*A/(TAU*TAU)*B*A/dist*hd
        return float(np.dot(weight,np.where(earlier>=0,pressure,0)))
    filt=solve_ivp(lambda x,y:[TAU/TF*(raw(x)-y[0])],[0,end],[0.],
                   rtol=1e-9,atol=1e-7,max_step=.001,dense_output=True)
    xx=np.linspace(0,end,int(end*10000)+1); r,w,h=sol.sol(xx)
    pg=BETA*DP*r**(-3*KAP) if pressure_function is None else pressure_function(r); pfilter=filt.sol(xx)[0]
    summary={'method':'independent exact spherical radiation impedance + nonlinear radius ODE',
      'a_m':A,'matching_radius_m':B*A,'receiver_center_m':ROBS,
      'receiver_radius_m':ADET,'receiver_thickness_m':HDET,'receiver_filter_s':TF,
      'minimum_radius_ratio':float(r.min()),'maximum_wall_speed_m_s':float(np.max(np.abs(A/TAU*w))),
      'maximum_wall_Mach':float(np.max(np.abs(A/TAU*w))/C),
      'maximum_internal_gas_pressure_Pa':float(pg.max()),
      'maximum_filtered_receiver_pressure_Pa':float(pfilter.max()),
      'filtered_peak_time_s':float(xx[np.argmax(pfilter)]*TAU)}
    samples=np.arange(0,end+1e-6,.02)
    r,w,h=sol.sol(samples)
    pg=BETA*DP*r**(-3*KAP) if pressure_function is None else pressure_function(r)
    np.savetxt(ROOT/('data/'+prefix+'.csv'),
      np.column_stack([samples,r,A/TAU*w,pg,filt.sol(samples)[0],[raw(q)for q in samples]]),
      delimiter=',',header='time_over_tau,radius_ratio,wall_speed_m_s,gas_pressure_Pa,filtered_pressure_Pa,raw_pressure_Pa',comments='')
    (ROOT/('data/'+prefix+'.json')).write_text(json.dumps(summary,indent=2),encoding='utf8')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':run()
