> Public lesson edition: saved native files and complete COMSOL-generated settings are in the local delivery; this site provides the exact rebuild recipe, sources, numerical evidence and field exports.

# Two native 3D theory models — scientific verification

Numerical checks complete; independent review accepts the conditional pressure and equilibrium theories. The uniform-population physical limit is rejected; actual device compatibility remains undetermined.

These models were built and solved in COMSOL 6.4.0.429 for this assignment. They answer a conditional pressure question and a finite-PFP/gel equilibrium compatibility question. They do not establish a universal laser-cavitation maximum or a certified repeated transfer process. [Independent post-model review](verification/INDEPENDENT_REVIEW.md).

## Pressure result and its definition

The strongest sampled polytropic-gas reference gives **89.610 kPa** filtered gauge pressure. A separate spherical progressive-wave energy/response bound is **318.156 kPa** if all the declared initial available energy could radiate. The bound is not a predicted attainable value. It does not cover arbitrary directional focusing, jet impact or wall shock loading.

The observer is a water volume cylinder of radius 50 μm and thickness 5 μm centered 0.5 mm from the source origin. Its volume mean gauge pressure passes through a causal first-order 1 MHz low-pass response (time constant 159.155 ns). Peaks are taken only in the first 8 μs. Ambient pressure is 100 kPa absolute. PFP phase pressures and gas pressure are absolute; wave/receiver pressures are gauge. A real hydrophone or film traction is not inferred without its response and coupling.

The gas study samples two total available energies, 8.74672 and 67.71179 nJ, at initial pressure ratios β=0.05, 0.1, 0.2, plus a 55 nJ β=0.1 comparison. Radius adjusts at fixed energy; the sampled radii span 23.585–51.745 μm. The maximum is over these seven samples, not a proven continuous optimization. Constant κ=1.4 is a mathematical polytropic reference; high-temperature gas heat capacity, heat transport, real-gas and reaction effects are not verified. Those uncertainties are additional to the matching-radius comparison.

| Gas case | E₀ (nJ) | β | a (μm) | peak p_f (kPa) | energy residual | waveform error/reference peak | numerical gate |
|---|---|---|---|---|---|---|---|
| 0 | 8.74672 | 0.05 | 25.8522 | 31.1535 | 0.13229% | 1.3934% | pass |
| 1 | 8.74672 | 0.10 | 25.0000 | 21.8057 | 0.14427% | 1.8087% | pass |
| 2 | 8.74672 | 0.20 | 23.5854 | 12.1610 | 0.01767% | 0.7203% | pass |
| 3 | 67.71179 | 0.05 | 51.7448 | 89.5870 | 0.32271% | 2.7033% | pass |
| 4 | 67.71179 | 0.10 | 50.0000 | 53.2339 | 0.02922% | 0.5145% | pass |
| 5 | 67.71179 | 0.20 | 47.1125 | 25.7122 | 0.00284% | 0.8018% | pass |
| 6 | 55.00000 | 0.10 | 46.6142 | 48.8578 | 0.04514% | 0.5876% | pass |

The baseline gas case 0 at 25 ns failed the pressure-waveform gate (7.72%) and is excluded from the authoritative case list. The separately stored `smallGasRefinement` study uses 6.25 ns internal spacing and 12.5 ns outputs. All other baseline gas samples are retained only if their listed gates pass. The worst-case time control uses 12.5 ns; its peak differs from the 25 ns value by 0.02594%, its waveform error is 0.6304% and its energy residual 0.1029%. The independent finer mesh changes the worst peak by 0.00684%. The original single-source mesh control also showed a 0.0143% peak change, but it is not substituted for the strongest-case check.

At fixed source energy and β, the independently solved outgoing-wave/radius equations give 85.54–93.16 kPa as the matching radius changes from 150 to 75 μm. A low-Mach Keller–Miksis alternative gives 96.33 kPa. These are model comparisons, not numerical error bars and not a complete uncertainty interval. The strongest refined wall Mach is about 0.0303; the bubble interior pressure is around 9.55 MPa and is a different observable from the 89.6 kPa receiver value.

## Model A equations and energy check

Each resolved source has nonlinear spherical cavity dynamics, coupled by flux and pressure work to a genuinely spatial 3D coefficient-form acoustic-potential PDE. No radius time history is imposed. Water density, sound speed and viscosity are 1000 kg/m³, 1480 m/s and 0.001 Pa·s. The fixed matching radius is 110 μm for gas and twice the initial radius for each resolved PFP source. The outer domain radius is 0.9 mm with a spherical Sommerfeld boundary. The receiver is partitioned into the geometry.

$$
\ddot\phi/c^2-\nabla^2\phi=0,\quad p_{ac}=-\rho\dot\phi,\quad \partial_n\phi=-Q/A_b,\quad Q=4\pi R^2\dot R.
$$

$$
(R-R^2/b)\ddot R+(3/2-2R/b)\dot R^2=(p_B-p_\infty)/\rho+\langle\dot\phi\rangle_b.
$$

The domain normal on a source hole points toward its center. Expansion therefore has negative domain-normal potential flux. The near kinetic energy is 2πρR³Ṙ²(1−R/b). Wave energy integrates ρ[(∇φ)²+φ̇²/c²]/2 over the actual 3D water mesh. Source/wave exchange cancels between the two ledgers. Viscous loss is integrated from 16πμRṘ²; the outward wave-energy flux is tracked at the far boundary. Ambient-volume work, both interface energies and internal phase energy are included once. A separate radiation loss is not added to the source radius law.

For PFP, the finite mass is conserved by the phase-volume relation. The EOS supplies p(T,ρ), u(T,ρ), g(T,ρ); liquid and vapor chemical potentials match at different pressures with the inner Laplace jump. The PFP entropy is constant for the declared short, internally equilibrated adiabatic collapse reference. Inner/outer tensions are held constant at 9.41/54 mN/m. No latent-heat term is added on top of phase internal energy. The 1 nm vapor-radius floor is inactive in all accepted transient states; it supplies no pressure maximum.

## PFP bubble and population results

Each PFP study holds the **total** retained source energy at 55 nJ relative to its cold liquid reference. Initial vapor mass fraction is 0.5 and temperature 293.15 K; source mass and radius come from the exact finite-phase source card. These initial states are supplied after activation. They are not generated by an inferred optical efficiency. Cold PFP liquid radii per source are 5.497/3.806/3.208/1.172 μm for N=1/3/5/100. Model A is a micrometer-scale inventory reference and is **not** the same 300 nm-radius particle as Model B or an audited nanodroplet formulation. The pressure comparison must not be transferred between those inventories without rebuilding the source ledger.

| PFP scenario | peak p_f (kPa) | peak time (μs) | min R/a | energy residual | capillary-jump residual | numerical gate |
|---|---|---|---|---|---|---|
| cP | 1.87014 | 5.0250 | 0.632870 | 0.000175% | 2.2723% | pass |
| c3 | 3.48519 | 3.7000 | 0.612833 | 0.000372% | 3.2373% | pass |
| c5 | 4.67854 | 3.2750 | 0.601704 | 0.000512% | 3.9393% | pass |
| cU refined diagnostic | 16.65140 | 1.9750 | 0.460877 | 0.046196% | 1.8631% | pass |

The three/five source centers lie on a 200 μm radius circle, with separate dynamic/phase states and matching holes. They interact through the solved wave field. All are activated together. Their capillary-jump output residuals are disclosed, about 3.24%/3.94%, although their liquid-pressure residuals remain below 0.056%. This is finite-accuracy phase closure, not machine precision.

The phase shell is thin even in these micrometer-inventory references: native minimum PFP liquid-shell thickness is approximately 44.78/31.01/26.13 nm for one/three/five sources and 9.54 nm in the uniform diagnostic. Bulk EOS, constant tensions and instantaneous phase equilibrium remain limiting assumptions; coating, disjoining-pressure and shell-rupture physics are omitted. The pressure values are conditional on those assumptions.

The uniform N=100 scenario uses a 200 μm population sphere and distributed flux −nQ in the wave equation, coupled to one common representative bubble via the population-average pressure. Its initial void fraction is about 0.00187. It is a common-state diagnostic, not 100 independently resolved interfaces or a fully local bubble-state continuum. The refined field deviates from its population mean by up to **62.26 kPa** (62.3% of ambient pressure), and its minimum local gauge pressure is −118.97 kPa (absolute −18.97 kPa, a tensile reference state). These actual outputs do not support equal local bubble dynamics. Secondary water cavitation and a physically appropriate local-state population model are unresolved. **The 16.651 kPa uniform-mode result is therefore not accepted as a physical uniform-population pressure limit**, even though the discretized common-mode equations pass their numerical gates. Diluteness alone is insufficient; finite-spacing/self corrections, disorder and discrete-to-continuum equivalence are also unvalidated.

The population baseline at 25 ns failed the phase gate: capillary-jump residual 18.0%, despite energy residual only 0.0155%. It is retained as a diagnostic study and excluded from authoritative phase claims. The finer `uniformPfpRefinement` study is the numerically accepted common-state diagnostic; its peak changes by 0.80662%. Its physical population interpretation remains rejected. A separately enlarged outer domain (1.2 mm, otherwise baseline settings) changes the five-source receiver peak by 0.25155%. This tests the noncentral source field, where a spherical first-order radiation boundary is approximate. The centered spherical common-state population has an exact outgoing monopole Sommerfeld condition at the continuum level; the gas propagation/mesh and population time controls still address its discretization. No claim of a separately solved local-state continuum is made.

Gas and PFP peaks at different energies must not be compared as material performance. At the matched 55 nJ gas sample, the receiver peak is about 48.86 kPa, versus the single-PFP 1.870 kPa reference. Phase condensation softens collapse in these particular supplied states. This is not evidence that PFC always reduces useful loading or that a low-onset formulation cannot improve energy efficiency.

## Model B: conditional PFP–hydrogel compatibility

Model B uses a 300 nm **radius** PFP liquid inclusion (600 nm diameter) in a 3D nearly incompressible neo-Hookean gel. Its cold liquid mass is fixed using EOS density at p₀+2σ_LL/a. The gel shell extends to 20a=6 μm, G=10 kPa, K/G=1000, density 1006.5 kg/m³. The outer traction is free and rigid motion alone is suppressed. A follower pressure and variational constant surface energy act on the cavity; no cavity radius, shape or displacement is imposed.

$$
p_{el}=G(5-4/\lambda-\lambda^{-4})/2,\qquad W_s=2\pi Ga^3(5\lambda^3/3-2\lambda^2+\lambda^{-1}-2/3).
$$

The infinite incompressible radial formulas are independent references for the finite, nearly incompressible 3D solution. The free deformed volume is computed from the surface/cofactor integral; equivalent radius is (3V/4π)^(1/3). Local principal stretch is independently computed from the deformation gradient, not replaced by equivalent radius. The phase closure solves Gibbs equality, inner Laplace jump and total retained energy:

The material and geometry are homogeneous and initially spherical. Patchy colors in a principal-stretch export reflect finite-element discretization variation; they do not establish material heterogeneity or jet stabilization. Local-max stretch remains subject to the disclosed mesh difference.

$$
Q_{dep}=\Delta U+W_s+p_0\Delta V+\sigma_{LL}\Delta A+4\pi\sigma_{LV}R_g^2.
$$

The gel/PFP outer coefficient 54 mN/m is assumed from a **liquid PFP/water** reference; the actual gel interface was not measured. A constant isotropic surface stress equal to surface energy is an explicit constitutive assumption. The inner 9.41 mN/m room-temperature reference is also held fixed at the warmer states. These choices do not claim a target hydrogel card or a measured σ(T,strain).

| Q_dep (pJ) | equivalent λ | local λ_max | T (K) | vapor mass fraction | shell (nm) | reference classification |
|---|---|---|---|---|---|---|
| 11.55 | 1.9087705 | 1.9458646 | 340.288 | 0.146722 | 27.495 | below with numerical margin |
| 11.65 | 2.0012763 | 2.0406787 | 339.197 | 0.168132 | 24.117 | below with numerical margin |
| 11.75 | 2.0701142 | 2.1109254 | 338.437 | 0.184950 | 21.929 | borderline |
| 11.82 | 2.1112877 | 2.1528057 | 338.002 | 0.195383 | 20.733 | exceeds proxy even by equivalent stretch |
| 11.90 | 2.1537190 | 2.1974532 | 337.568 | 0.206432 | 19.579 | exceeds proxy even by equivalent stretch |

Fine/coarse native meshes have 77,481/48,277 solved DOFs. Equivalent-radius mesh change is 0.03356%; local-maximum stretch changes by up to 1.7538%. The fine elastic-pressure law differs from the analytic reference by at most 0.01846% and elastic work by 0.02771%. Energy relative residual is at most 5.48e-13; mass residual 3.36e-17; capillary residual 6.11e-06 Pa; Gibbs residual 2.4e-09 J/kg.

The λ_f=2.1 criterion is the cited PAAm **uniaxial** ultimate-stretch proxy. A spherical cavity has equibiaxial extension; rate, temperature, formulation, interface fracture and flaws may change failure. The two low-energy states pass the proxy with numerical margin. The 11.75 pJ state is borderline under mesh gradient error. The two higher-energy states fail even using equivalent stretch. This is an elastic equilibrium screen, not a certified cavity-damage threshold.

| 13 pJ case | G (kPa) | σ_LV (mN/m) | equivalent λ | local λ_max | result |
|---|---|---|---|---|---|
| 0 | 10.0000 | 9.41 | 2.5442167 | 2.6287056 | exceeds proxy |
| 1 | 10.0000 | 8.00 | 2.5857574 | 2.6759812 | exceeds proxy |
| 2 | 10.0000 | 14.00 | 2.3992102 | 2.4657074 | exceeds proxy |
| 3 | 27.0270 | 9.41 | 2.2544858 | 2.3184589 | exceeds proxy |

The stronger-gel sensitivity changes G to 27.027 kPa but keeps K/G=1000; it is not a full reproduction of Li's E=80 kPa, ν=0.48 material. The 8–14 mN/m inner-tension range is a modeling sensitivity bracket, not a measured confidence interval. Coated outer-interface alternatives have independent EOS/elastic roots but failed native equilibrium convergence; their remaining liquid shells are only roughly 3–4 nm. Those cases are unresolved and excluded, not declared physically impossible.

## Activation, stability and repeated operation

An independent exact-EOS radial perturbation check gives restoring stiffness ∂[p_el+2σ_LL/R−(p_l−p₀)]/∂λ positive at constant closed energy (about +32 to +65 kPa per unit stretch) and negative at constant temperature (about −115 to −89 kPa per unit stretch). A converged equilibrium is therefore locally stable in the closed-energy reference but radially unstable if temperature is clamped. This tests radial stability only; no shape/jet stabilization is established.

The cold liquid heating precursor reaches the flat bulk-saturation criterion at approximately 350.523 K and 11.54964 pJ; the equivalent-stretch proxy λ=2.1 corresponds to about 11.80013 pJ. A small mathematical energy interval exists. The precursor is a necessary lower-bound construction: a finite nucleus, a heterogeneous nucleation barrier, shell chemistry and the intact thermal path are uncomputed. It does not prove activation at 11.55 pJ, and it does not prove that no safe interval can exist.

With assumed water-like gel thermal properties k=0.6 W/(m·K), ρ=1006.5 kg/m³ and C_p=4180 J/(kg·K), a²/α≈0.631 μs and the elastic-inertial scale≈0.095 μs. The draft's 20 ms pulse is about 31,692 diffusion times at this length. An insulated, rate-free equilibrium cannot certify this long-pulse experiment. Heat loss, transient gel viscosity, phase kinetics, damage, gas diffusion/condensation, cooling/reset and repeated-pulse conditioning must be established for an actual intact repeatable operating envelope.

**Reportable verdict:** low-energy supplied post-activation equilibria pass a stated elastic stretch proxy; 13 pJ reference/sensitivity states fail it; the fixed-temperature bare-interface equilibrium branch is radially unstable. Actual laser-activated and repeatable PFC-in-hydrogel transfer remains undetermined from available material/source evidence. A closed intact embedded cavity has no specified exterior liquid pathway, so an exterior jet or its stabilization cannot be claimed from Model B.

## Optical and material provenance

The supplied v4 manuscript reports 808 nm and milliseconds (20 ms on Si, 80 ms on steel), with a 6 A calibration P_inc=4.5053I−5.1904=21.8414 W. Its three-zone integrated thermal source gives 11.376 W. The 20 ms energies are respectively 0.436828 J and 0.22752 J. Neither resolves the PFC absorber cross section or local retained energy. The native 3D heat control separately verified an imposed 11.376 W source integral and constant-property insulated heat/energy evolution; it did not calibrate this apparatus.

The material research distinguishes PFP from PFH, radius from diameter, pulse duration from threshold fluence, and conditioning history from single-shot onset. Hannah's PFP/AuNR/Zonyl system, Wei's 9 ns PFH/gold-bead system, Strohm's 700 ps PFP/PbS system and Zhao's 5 ns lipid/dye PFP system do not supply an interchangeable absorption efficiency. Zhao's roughly 309 nm is a diameter; the model's 300 nm is a radius. For illustration, 18.6 mJ/cm² times a geometric disk is 52.6 pJ for a 300 nm radius and 13.1 pJ for a 300 nm diameter, but neither is absorbed energy without an absorption cross section.

PFP EOS source: Gao et al., DOI 10.1021/acs.iecr.1c02969, represented by the archived CoolProp 8 HEOS coefficients. A native p/u/g evaluator was checked at 72 states against independent HEOS evaluation. Accepted PFP states are within 293–340 K and pressures below the reported EOS upper range; no transport property or interfacial tension is supplied by that EOS. Kandadai's thesis gives the room-temperature PFP liquid/saturated-air and liquid-water tension references. Movahed et al., DOI 10.1121/1.4961364, supplies the PAAm reference/proxy. Li et al., DOI 10.1073/pnas.2318739121, is a water-vapor hydrogel transfer reference, not embedded-PFP jet validation. Detailed source conditions and limitations are in the local source ledger and original PDFs.

## Architecture and force-path coverage

The three architectures are retained as different physical branches. The supplied water-droplet draft is not an audited PFC stamp experiment. A primary PFC-containing liquid layer can load a film directly or load PVC which transmits traction to the film; those loads are not interchangeable. A bulk-gel inclusion, liquid pocket and interfacial blister have different liquid pathways and mechanical constraints. Model A supplies conditional emitted liquid pressure; Model B supplies conditional embedded-gel phase/deformation states. Finite droplet boundaries, meniscus/azimuthal jets, film/PVC transmission, release traction, venting and reset are unresolved here. No branch is discarded as nonexistent.

Potential PFC benefits include lower activation threshold, thermal burden, pressure, jet mass/momentum, transfer quality and reset. These two files do not establish all those benefits simultaneously. The single-shot reference pressure and proxy equilibrium screen are reportable; a maximum jet velocity, repeated intact-transfer limit and material-specific full-process yes/no are not verified outputs.

## Native evidence, exclusions and reproduction

The `final/` directory holds exactly two theory files. Each has actual 3D geometry, tetrahedral mesh, supported COMSOL physics, solved numerical state vectors and result datasets. Native field and mesh PNGs are genuine COMSOL exports, and `native-config/` contains complete COMSOL-generated settings reports. They are **not Desktop GUI screen captures**: the Desktop bridge status was disabled. Do not describe them as an attached GUI session.

Supplied benchmark P0/H0 and follow-on controls were built and solved earlier in this same assignment; their copied specification/register/numerical audit are in `resources/benchmark-evidence/`. They are controls, not reused earlier-project results. Three-dimensional free-gel, heat and exact-EOS controls supply fresh independent checks. Failed ALE/flow and BDF attempts are recorded as failed/incomplete; they do not supply a late-collapse pressure. Invalid recovered gel vectors and unresolved coated-interface calculations are excluded. All causal logs/checkpoints are preserved in the working project.

The acceptance gates are in `data/final_native_verification.json`. Gas energy residual must be below 1%, pressure waveform error below 5% of independent reference peak, radius waveform error below 2% of initial radius, and wall Mach below 0.1. For PFP output states, require capillary residual below 5% of the jump and 0.1% of liquid pressure, scaled entropy residual below 1e−4, Gibbs residual below 0.1 J/kg, physical mass fraction and temperature, and energy residual below 1%. Numerical time/mesh/domain peak changes are assessed against a 2% reference-study target. These numerical tolerances are not material uncertainty bounds.

Use `reference/rebuild.html`, the parameter/expression files, the complete native reports and `rebuild/Run-Rebuild.ps1`. Model B defaults to the original baseline guesses; use the documented alternate initial guesses before recomputing its sensitivity study. Independent analytical references never consume native radius histories. Reproduction requires COMSOL 6.4 and the listed licensed interfaces. Portable HTML/PDF/plot assets are local; original private draft content stays in this local package.

Four bilingual teach-mattcc chapters are prepared. Existing course credit is preserved as a read-only context snapshot. No new learner mastery is claimed until an explanation/rebuild and a meaningful changed-parameter test have been demonstrated.
