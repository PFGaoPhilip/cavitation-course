# Independent post-model review

**Verdict: the two native 3D files and the stated conditional theory calculations are accepted within the scopes below. An unqualified uniform-population limit, a jet-velocity maximum, and actual repeatable intact-transfer compatibility are not accepted conclusions. No critical equation or numerical discrepancy remains in the reviewed accepted branches.**

Reviewer: independent post-model subagent `/root/independent_model_verifier`, separately launched after both native models were built and solved. Review date: 8 October 2026. This is an independent computational/theoretical review, not experimental validation or a material/device certification.

## Evidence and independence

I inspected [THEORY_REPORT.md](../THEORY_REPORT.md), the actual Java builders and finalizers, independent reference code, the numerical CSVs, both final MPH archives, native complete settings reports, and selected bundled primary-source PDFs. I did **not** use `data/final_native_verification.json` to establish acceptance. The independent audit program [independent_audit.py](independent_audit.py) reassembles conservation sums, measures waveform discrepancies and refinement changes, evaluates a separate finite-phase EOS root, and tests archive integrity. Results and input hashes are recorded in [INDEPENDENT_AUDIT.json](INDEPENDENT_AUDIT.json). The additional coefficient/heat/source-page check is in [SOURCE_AND_CONTROL_AUDIT.json](SOURCE_AND_CONTROL_AUDIT.json).

A separate dimensional Radau solve of the radius/outgoing-potential equations, a 20 × 12 spatial receiver quadrature, and an independently integrated continuous low-pass response produced [DIMENSIONAL_GAS_REFERENCE.json](DIMENSIONAL_GAS_REFERENCE.json). It does not ingest a COMSOL radius trajectory. The independent PFP/gel root and radial perturbations use CoolProp 8 HEOS directly, without importing the primary reference root functions or imposing a native radius.

### Native files and archive integrity

| Native deliverable | Bytes | Actual geometry and solved state |
|---|---:|---|
| [Model A](../reference/rebuild.html#model-a) | 5,182,658,325 | COMSOL 6.4.0.429; `nodeType=solved`; five geometry tags, all dimension 3; five built mesh binaries; seven native solution objects |
| [Model B](../reference/rebuild.html#model-b) | 16,740,342 | COMSOL 6.4.0.429; `nodeType=solved`; geometry `g`, dimension 3; built mesh; five baseline and four valid sensitivity state vectors, each stored length 77,481 |

**Every member CRC passed in both MPH archives.** SHA256:

```text
A  7f8a1f33668056aa98043d18bacf4edfd69c131f28d9d8e2ac1b66fd7eefcad7
B  38b18f98c6f11a56da2ba306d354760ec63c0ca00b9132a8d5406a7f42886280
```

The seven A native state counts are 321, 2,247, 321, 321, 321, 641 and 641. Its final gas sweep includes the excluded coarse case 0; the separately stored small-gas study supplies its replacement. Its refined population study is also separately stored. The strongest gas time/mesh refinements are additional COMSOL verification controls represented by their CSVs and rebuild scripts, rather than additional final MPH deliverables. Consequently, the saved main A gas case 3 peak is 89.587 kPa; the headline 89.610 kPa is the independently verified finer-time control.

All actual `SolutionNative` parameter arrays are finite. B's legacy `SolutionInfo` contains a NaN list for one coordinate of its unstructured two-parameter sweep; the actual native solution array and native `getPVals()` contain the four real `(13 pJ, caseIndex 0–3)` pairs. This metadata presentation is not an invalid fifth solution. I did not treat `getSizeMulti()`'s first A dimension as a PDE degree-of-freedom count.

The explicit A result datasets reference the correct components and solvers. Model A is a spatial **3D wave field coupled to spherical scalar source dynamics**, with fixed matching holes; it does not resolve a moving nonspherical liquid interface. Model B solves unconstrained 3D solid deformation. The inspected native five-source image displays five matching regions, and the gel image displays the deformed cavity at the stated energy. These are genuine COMSOL exports, **not Desktop GUI screenshots**. The disabled Desktop bridge limitation remains disclosed.

## Equations, signs and thermodynamic bookkeeping

The acoustic potential has units m²/s, its time derivative m²/s², and `−ρ φ̇` is gauge pressure. On the interior hole the water-domain normal points toward the source, so the negative normal flux `−Q/A_b` is correct for positive outward expansion.

Differentiating `K_near = 2πρR³Ṙ²(1−R/b)` gives

```text
dK_near/dt = Q [p_B − p∞] + ρ Q <φ̇>_b.
```

The wave energy receives `−ρ Q <φ̇>_b` at that same boundary. Gas/phase internal energy, ambient work and surface energy remove the remaining reversible work; `16πμRṘ²` is the dissipated power. This verifies source-work cancellation and the sign of the coupling. No second radiation-loss term is included. The spherical far condition and its exported energy flux are consistent; it is approximate for noncentral sources, which is why the enlarged-domain comparison matters.

The finite PFP phase-volume relation conserves mass. Gibbs equality is evaluated at different liquid/vapor pressures with the inner Laplace jump. The EOS internal energy already contains phase conversion; adding latent enthalpy separately would double-count energy. Both internal and external interface energies and ambient-volume work appear once. The transient model's entropy constraint and constant interface coefficients define an instantaneous-equilibrium, short-collapse reference, not measured condensation kinetics.

For B, the follower load is the actual `pLP−p0`. The 3D model contains rigid-motion suppression, not prescribed cavity radius or displacement. The surface weak contribution is the variation of constant isotropic surface energy, using the cofactor, deformed normal and reference-area Jacobian. `Vfree=−∫x·cof(F)N dA/3` has the correct cavity-normal sign. The deformation-gradient largest-eigenvalue formula gives a local principal stretch distinct from equivalent-radius stretch.

I additionally inspected the raw saved XML after the complete native HTML report displayed simplified derivative rows. All nine bulk definitions remain exactly `δij+d(ui,Xj)`, and all nine surface definitions remain `δij+mean(d(ui,Xj))`; they were not overwritten by identity constants. [NATIVE_EXPRESSION_AUDIT.json](NATIVE_EXPRESSION_AUDIT.json) records the actual expressions. **Rebuild these expressions from the expanded imports/source; do not copy simplified derivative constants from the native HTML table.**

## Independently recomputed numerical results

| Check | Independent result | Interpretation |
|---|---:|---|
| Strongest gas, separate dimensional theory solve | 89,668.463 Pa | Matches the primary independent reference 89,668.192 Pa to about 0.00030% |
| Native strongest gas, finer time control | 89,610.251 Pa | Reference-peak difference about 0.06462%; waveform error 0.63036% |
| Strongest native gas time / mesh peak change | 0.025944% / 0.006840% | Numerical controls pass the stated scope |
| Excluded coarse gas case 0 | Energy 1.04515%; waveform 7.71816%; radius 2.14755% | Correctly excluded; refined replacement passes |
| PFP N=1 / 3 / 5 filtered peaks | 1.87014 / 3.48519 / 4.67854 kPa | Fixed total 55 nJ, supplied activated-state references |
| PFP N=1 / 3 / 5 reassembled energy residual | 0.000175% / 0.000372% / 0.000512% | All source-phase state columns included |
| PFP N=3 / 5 maximum capillary-jump residual | 3.23727% / 3.93934% | Finite-accuracy phase closure, not machine precision |
| Five-source enlarged-domain peak change | 0.25155% | Supports the reported noncentral pressure field at this observer |
| Refined uniform diagnostic | 16.65140 kPa; energy 0.046196%; capillary 1.86312% | Numerical common-mode equations pass; physical closure does not |
| B independent root at 11.65 pJ | λ=2.0012466, T=339.19752 K | Native equivalent λ=2.0012763 agrees within finite-domain/discretization differences |
| B equivalent / local-maximum stretch mesh change | 0.033555% / 1.753817% | Local gradients need more caution than volume radius |
| B elastic pressure / work vs analytic radial reference | 0.018455% / 0.027706% | Free 3D deformation and energy agree with independent mechanics |

Independently recomposing B's phase densities, phase masses, internal energy, elastic work, ambient work and both surface energies reproduces its source budget. The worst relative recomposition energy residual for its five baseline states is below `5×10⁻¹³`; phase density differences are near floating-point precision. Independently recomposing the four 13 pJ sensitivity states gives a maximum relative energy residual of `2.24×10⁻¹²`, with all four still exceeding both stretch proxies. The fresh radial perturbation at 11.65 pJ gives restoring stiffness **+46.052 kPa/stretch at closed total energy**, but **−103.744 kPa/stretch at fixed temperature**. The stability conclusions are therefore correctly distinguished, and apply only to radial local perturbations.

The separate liquid-only bulk-saturation construction reproduces **11.549639 pJ at 350.522863 K**. A finite nucleus/barrier was not computed, so this is a necessary lower-bound construction, not a demonstrated activation threshold. A small mathematical interval below the equivalent-stretch proxy energy can exist; the evidence does not justify declaring that every possible intact activation interval is absent.

The 72-state / 216-value native EOS coefficient check was independently repeated against forced-phase HEOS evaluation. Maximum normalized differences are about `5.45×10⁻¹²` for pressure, `7.51×10⁻¹⁵` for internal energy and `2.14×10⁻¹²` for Gibbs energy. This checks implementation, not phase stability or experimental EOS uncertainty. The fresh 3D heat control integrates 11.376 W, gives about 0.22752 J after 20 ms, and improves analytic field RMS discrepancy from 0.00541 to 0.00183 K with spatial refinement. It validates the imposed source/control equations, not optical absorption in the user's apparatus.

## Physical acceptance, rejection and unresolved scope

**Accepted conditionally:** the source equations, finite-phase energy ledger, and numerically verified emitted-pressure samples; the separate spherical progressive-wave receiver bound; and the supplied PFP/gel equilibrium screen. Under the declared uniaxial λf=2.1 proxy, the 11.55/11.65 pJ states are below with numerical margin, 11.75 pJ is borderline, 11.82/11.90 pJ exceed even equivalent stretch, and all four 13 pJ sensitivity states exceed the proxy. This does not turn the cited ultimate stretch into a measured equibiaxial/high-rate/high-temperature criterion for the current gel.

The **318.156 kPa** bound follows independently from `E ≥ [4πr²/(ρc)]∫p²dt` and Cauchy–Schwarz for the causal first-order filter, whose squared kernel norm is `1/(2τf)`. Using the nearest receiver radius gives a conservative volume-average bound. Its isotropic spherical progressive-wave and all-source-energy assumptions are essential; it is not an attainable prediction, a directional-population bound, or a wall/jet-impact limit.

**Rejected as an unqualified physical prediction:** the N=100 common bubble state. The refined native field deviates from its population mean by **62,257.058 Pa** and reaches **−18,966.609 Pa absolute** locally. The pressure variation does not support equal local bubble dynamics. The tensile reference state also requires water-cavitation/nucleation physics before an experimental interpretation. Numerical convergence and small void fraction do not establish this physical closure. The 16.651 kPa common-mode result must remain diagnostic.

**Unresolved:** laser-to-inclusion energy absorption, the intact activation path, finite-droplet/meniscus and nonspherical jet motion, liquid-to-film versus liquid→PVC→film traction, local-state/disordered populations, target gel interface laws, damage, viscosity/rate effects, permeability/diffusion, cooling/reset and repeated transfer. The 20 ms pulse exceeds the assumed 300 nm thermal diffusion time by roughly 31,692. The insulated closed-energy equilibrium therefore cannot certify that pulse. The intact embedded cavity has no defined exterior liquid pathway; it provides neither an exterior jet prediction nor evidence of jet stabilization. The full optical-to-transfer experimental chain remains open.

Model A's cold per-source PFP radii are 5.497/3.806/3.208/1.172 μm. Model B's cold radius is 0.300 μm, mass `1.8359×10⁻¹⁶ kg`. These inventories cannot be exchanged without rebuilding the source ledger. Model A's minimum liquid-shell thicknesses are 44.776/31.006/26.130 nm for N=1/3/5 and 9.544 nm for its uniform diagnostic. Constant bulk tensions, omitted coating/disjoining/rupture physics, and instantaneous phase equilibrium remain conditions even for its larger outer bubbles. Patchy stretch colors on B's otherwise homogeneous spherical reference are discretization variation, not physical heterogeneity or stabilization evidence.

## Source provenance and corrections

I directly checked the bundled Kandadai dissertation, PDF pp. 127–133: 9.41 mN/m is a room-temperature PFP/saturated-air measurement and 54 mN/m is PFP/distilled-water. Neither is a measured warmed PFP/gel interface law. Movahed, PDF pp. 5/7, supports the illustrative 30 kPa PAAm modulus, 1006.5 kg/m³ density and λf=2.1 ultimate-stretch model; it also discusses viscosity and damage that B does not include. Li, PDF pp. 4/9, uses 808 nm hydrogel/water transfer and an 80 kPa, ν=0.48 Mooney–Rivlin material. Its use is correctly limited to a reference; the G-only sensitivity is not its full formulation. Zhao's approximately 309 nm is a **diameter** with conditioning/cooled repeated activation, not a measured retained-energy threshold for this 300 nm-radius inclusion.

Review-requested corrections addressed by the primary agent: distinguish the refined uniform numerical gate from physical acceptance; correct B's unused interface alias description; disclose A's thin-shell and B's mesh-patch interpretation; provide exact expanded derivative imports with a native-report simplification warning. The initially suggested source-JSON filename change was withdrawn after checking the actual existing `resources/source_inputs.json`; its correct link is retained. None required a new physical solve.

The failed ALE/BDF late-collapse attempts, invalid recovered gel vectors, coarse gas case 0, coarse uniform phase closure and unresolved coated-interface equilibria supply no accepted pressure/jet/damage limit. The prepared rebuild material is a reproducible learning resource, not proof of new learner mastery. No accepted course credit or shared Goal 1 files were modified in this review.

**Signed:** `/root/independent_model_verifier` — independent post-model review of the archived files and stated conditional conclusions; provenance and integrity values recorded in the linked machine-readable audits.
