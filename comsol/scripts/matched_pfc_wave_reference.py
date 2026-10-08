"""Independent matched-wave PFP reference on the exact finite-entropy isentrope."""
from pathlib import Path
import json
import numpy as np
from scipy.interpolate import PchipInterpolator
import matched_wave_reference as ref

root=Path(__file__).resolve().parents[1]
q=json.loads((root/'data/pfc_pressure_source_reference.json').read_text())
init=q['initial'];rows=sorted(q['rows'],key=lambda r:r['radius_ratio'])
pl=PchipInterpolator([r['radius_ratio']for r in rows],[r['p_liquid_Pa']for r in rows],extrapolate=True)
ref.A=init['a_m'];ref.B=2.;ref.SIG=init['sigma_outer_N_m'];ref.TAU=ref.A*np.sqrt(ref.RHO/ref.DP)

def rhs(x,y):
    r,w,h=y
    dh=-(ref.TAU*ref.C/(ref.B*ref.A))*(h+r*r*w/ref.B)
    pb=(float(pl(r))-2*ref.SIG/(ref.A*r)-4*ref.MU*w/(ref.TAU*r))/ref.DP
    dw=(pb-1+dh-(1.5-2*r/ref.B)*w*w)/(r-r*r/ref.B)
    return [w,dw,dh]

ref.rhs=rhs
ref.run(prefix='matched_pfc_wave_analytic',end=3.,pressure_function=pl)
