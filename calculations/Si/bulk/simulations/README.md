# Bulk-silicon simulation plan

## Status

**Provisional qualification evidence exists; no accepted production parent exists.**
This directory owns pristine bulk-silicon simulation declarations, authorized
execution records, compact outputs, and experiment verification. The retained
right-handed finite-setting campaigns and one successful FCC-native zero-pressure
relaxation remain provisional inputs to the stable-pair qualification sequence.

Nothing in this directory establishes an accepted silicon parent, production-converged
numerical settings, a qualified Wannier representation, effective masses, scientific
validation, or authority for another calculator execution.

## Objective

Prepare a separately authorized route that:

1. qualifies a scalar-relativistic, non-spin-polarized, non-SOC PBE bulk-silicon
   parent;
2. retains an identity-bound SCF state and constructs a full-grid NSCF state;
3. passes the verified NSCF state through `wannier90.x -pp`,
   `pw2wannier90.x`, and Wannier90 localization;
4. compares direct-parent and Wannier representations on declared construction and
   withheld sets; and
5. preserves exact evidence for later valley, effective-mass, and reduced-model
   analysis without treating software or process success as scientific acceptance.

## Ownership

This calculation root owns scientific selection, exact campaign declarations,
execution evidence, numerical acceptance, and experiment verification. Reusable
calculator-neutral records, workflow-domain composition, provider integrations,
native parsers, exact artifact handoffs, and single-calculator execution mechanics
belong to
[`projectkoios-simulations`](https://github.com/eragasa/projectkoios-simulations).
Project Koios must not select this calculation's scientific values or own its retained
results.

The local scientific authority remains:

- [`../development-plan.md`](../development-plan.md) — gated calculation sequence;
- [`../provisional-use-disposition.md`](../provisional-use-disposition.md) — limits on
  historical C48/K8 evidence;
- [`../evidence-crosswalk.md`](../evidence-crosswalk.md) — predecessor evidence status
  and non-transfer rules; and
- [`../../../../specification/dft-pseudopotential-library/v1/index.md`](../../../../specification/dft-pseudopotential-library/v1/index.md)
  — accepted pseudopotential-family decision; and
- [`../../../../docs/computational/Si-bulk/wannier-component-locality/index.md`](../../../../docs/computational/Si-bulk/wannier-component-locality/index.md)
  — authoritative Si-VC component-operator campaign planning.

These simulation documents bind future Project Koios consumption and execution
readiness across those authorities. They do not supersede the physical or numerical
specifications or create a competing Si-VC campaign definition.

## Upstream software authority

| Field | Binding |
| --- | --- |
| Repository | [`eragasa/projectkoios-simulations`](https://github.com/eragasa/projectkoios-simulations) |
| Inspected implementation baseline | `bbb9f1d8110ed9fe3ea1873c2366073c98f48c71` |
| Reviewed documentation-only architecture | `7ad5cad6576338945959a683f3cd407759e7c37c` |
| Existing authorities | `projectkoios.simulations.execution`, `calculator_input`, `evidence`; QE SCF/NSCF/saved-state and `pw2wannier90` integrations; Wannier90 native parsers |
| Planned bulk-qualification route | `projectkoios.simulations.workflows.pw_dft_bulk_qualification` |
| Planned Wannier route | `projectkoios.simulations.workflows.pw_dft_wannierization` |
| Planned neutral architecture | `docs/architecture/projectkoios/simulations/workflows/pw_dft_bulk_qualification/` and `pw_dft_wannierization/` |
| Planned provider architecture | `integrations/wannier90/preprocessing/`, `integrations/wannier90/localization/`, and `integrations/quantumespresso/pw2wannier90/artifacts/` under the upstream architecture tree |
| Planned first-party composition | Outward `projectkoios.adapters` mappings plus `tools/pw_dft_bulk_qualification` and `tools/pw_dft_wannierization` for provider selection, operational configuration, and route invocation |
| Current status | Implementation baseline plus reviewed architecture pin only; all listed end-to-end, provider, adapter, and tool additions remain unimplemented and are not an accepted dependency |

The architecture pin is documentation-only. Publication or review does not add
`src/` implementation or grant acquisition or execution authority. Normative baseline
links and the future dependency/conformance procedure are recorded
in [`architecture-plan.md`](architecture-plan.md). When an implemented upstream
capability is reviewed and actually imported, this project must pin its exact revision
through the declared dependency files. Adding or replacing that dependency requires
explicit human authorization. No copied description in this directory supersedes the
upstream software contract.

## Existing predecessor

The completed direct bootstrap remains at
[`calculations/bulk-silicon/production-convergence-preflight/`](../../../bulk-silicon/production-convergence-preflight/).
It contains nine SCF and nine linked diagnostic NSCF executions. Its inputs, compact
records, checksums, external-run identities, and embedded repository paths remain under
that immutable historical owner.

## Current finite-setting evidence

The authorized right-handed Gamma-centered K6/K8/K10/K12 campaign is retained under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-right-handed-gamma-kpoint/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-right-handed-gamma-kpoint/).
Applying `kpoints_convergence_atol = 1.0 meV/atom` against K12 selects K10 as the
smallest passing sampled mesh.

The subsequent cutoff campaign is retained under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-right-handed-gamma-k10-encut/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-right-handed-gamma-k10-encut/).
Applying `encut_convergence_atol = 1.0 meV/atom` against 60 Ry selects 42 Ry for the
wavefunction cutoff and 336 Ry for the density cutoff. These are finite sampled-setting
selections, not production acceptance. Every occurrence retained four IEEE warning
flags. These are retained as native QE diagnostics and are not automatic blockers when
an occurrence completes, converges, and produces finite observations.

The first authorized volume-only bulk-relaxation attempt is retained under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-right-handed-gamma-k10-c42-vc-relax-failed-volume/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-right-handed-gamma-k10-c42-vc-relax-failed-volume/).
QE rejected `ibrav=0` with `cell_dofree='volume'` before SCF startup. No relaxed
structure or scientific observation was produced by that occurrence.

A subsequent separately authorized occurrence used a verified FCC-native `ibrav=2`
basis with `cell_dofree='ibrav'` and is retained under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-right-handed-gamma-k10-c42-vc-relax-ibrav2/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-right-handed-gamma-k10-c42-vc-relax-ibrav2/).
It completed with return code zero and converged in three BFGS steps. The parsed final
conventional lattice parameter is `5.469182093640207 angstrom`; optimizer-terminal and
final-SCF pressures are `0.01 kbar` and `0.09 kbar`, respectively. The resulting exact
[`Si.PrimitiveUnitCell.RightHanded.RelaxedS1`](structures/Si.PrimitiveUnitCell.RightHanded.RelaxedS1.json)
record is provisional and requires fresh setting confirmation. Compact preflight
material for the first, fixed-C42 k-point stage is retained under
[`preflight/s1-gamma-c42-kpoint-confirmation/`](preflight/s1-gamma-c42-kpoint-confirmation/).
The exact four-occurrence packet was subsequently authorized and completed without
retries. Compact evidence is retained under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-right-handed-s1-gamma-c42-kpoint-confirmation/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-right-handed-s1-gamma-c42-kpoint-confirmation/).
The calculation-owned K12-reference rule again selects K10. Compact preflight for the
conditional K10 cutoff axis is retained under
[`preflight/s1-gamma-k10-cutoff-confirmation/`](preflight/s1-gamma-k10-cutoff-confirmation/).
The exact five-new-occurrence packet was authorized and completed without retries; the
authenticated C42/K10 SCF was reused and not rerun. Evidence is retained under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-right-handed-s1-gamma-k10-cutoff-confirmation/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-right-handed-s1-gamma-k10-cutoff-confirmation/).
The calculation-owned C60-reference rule again selects 42/336 Ry. Together with the
confirmed K10 axis, this defines the exact pair accepted under the calculation-owned
rules in [`accepted-stable-pair.json`](accepted-stable-pair.json). The separate generic
ProjectKoios sustained-tail policy remains a non-transferable software-policy result.
Acceptance emits a new parent-SCF requirement; no confirmation occurrence is reused.
Compact material for that one-occurrence gate is retained under
[`preflight/accepted-s1-parent-scf-gamma-k10-c42/`](preflight/accepted-s1-parent-scf-gamma-k10-c42/)
and was separately authorized and completed without retries. Compact evidence is
retained under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-parent-scf-gamma-k10-c42/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-parent-scf-gamma-k10-c42/).
Its authenticated saved state is the prospective source for a separately declared and
authorized NSCF. The required human scientific choices and the non-transfer boundary
are recorded in
[`wannier-interface-decision.md`](wannier-interface-decision.md). The recommended
first candidate was approved and preflight is retained under
[`preflight/accepted-s1-wannier-nscf-4x4x4-b12/`](preflight/accepted-s1-wannier-nscf-4x4x4-b12/).
The one authorized NSCF occurrence returned zero and produced finite 64-point,
12-band QEXSD data, but 41 explicit `c_bands` warning lines reported 44 unconverged
eigenvalues. Its evidence is retained under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier-nscf-4x4x4-b12/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier-nscf-4x4x4-b12/),
and it is blocked from downstream use. The separately authorized single-variable
Davidson occurrence returned zero with no `c_bands` diagnostic and is retained under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier-nscf-4x4x4-b12-david/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier-nscf-4x4x4-b12-david/).
It is eligible only as a candidate handoff. The first Wannier90 preprocessing
candidate was executed once under bounded authorization. Its verified rank-10 NNKP
topology is retained under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-preprocess-sp3sstar/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-preprocess-sp3sstar/).
The separately authorized converter produced correlated AMN/MMN/EIG artifacts retained
under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-pw2wannier90-sp3sstar/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-pw2wannier90-sp3sstar/).
The provider-generated localization preflight is retained under
[`preflight/accepted-s1-wannier90-localization-sp3sstar-provider/`](preflight/accepted-s1-wannier90-localization-sp3sstar-provider/).
Its first authorized occurrence returned zero but failed both declared optimization
convergence gates and is retained as blocked under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-sp3sstar-blocked/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-sp3sstar-blocked/).
The conditioned and damped revision converged Wannierisation but not disentanglement;
it is retained separately under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conditioned-damped-blocked/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conditioned-damped-blocked/).
The earlier no-runner preparation remains retained as superseded without execution.
The native dimensionless disentanglement criterion and its scale-dependent equivalent
absolute tolerance are clarified in
[`disentanglement-convergence-tolerance.md`](disentanglement-convergence-tolerance.md).
The operator-selected next candidate froze all eight conduction bands, while leaving
the remaining two rank-10 dimensions to be selected from four valence bands, as defined
in [`conduction-frozen-window-decision.md`](conduction-frozen-window-decision.md). Its
single authorized occurrence converged disentanglement at iteration 531 but exhausted
500 Wannierisation iterations without that stage's convergence message. It is retained
as blocked evidence under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-blocked/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-blocked/).
No retry of that occurrence was authorized. At operator direction, a fresh one-variable
successor increased only `num_iter` from 500 to 1000, as defined in
[`conduction-frozen-iteration-extension-decision.md`](conduction-frozen-iteration-extension-decision.md).
It reproduced disentanglement convergence at iteration 531 but again failed
Wannierisation convergence after the enlarged budget. It is retained under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-iter1000-blocked/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-iter1000-blocked/).
Its authorization is consumed and no retry is authorized. The authorized execution-free
comparison of the two blocked operators is retained under
[`../analysis/conduction-frozen-gauge-sensitivity/`](../analysis/conduction-frozen-gauge-sensitivity/).
It finds small source-mesh reconstruction differences but large between-mesh spectral,
edge, and curvature sensitivity, so the failure is not an innocuous stopping-criterion
technicality and further iteration-only extension is not supported. The operator then
authorized the one-variable `guiding_centres = .true.` recommendation documented in
[`conduction-frozen-guiding-centres-decision.md`](conduction-frozen-guiding-centres-decision.md).
The single authorized occurrence reproduced disentanglement convergence at iteration
531 but again failed Wannierisation convergence after 1000 iterations; its final spread
was higher than the unguided comparator. It is retained under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-guiding-centres-blocked/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-guiding-centres-blocked/).
The authorization is consumed and no retry is authorized. At operator direction, the
next one-variable candidate returns to the unguided input and halves Wannier90's
parabolic line-search trial step from its default `2.0` to `1.0`, as documented in
[`conduction-frozen-trial-step-decision.md`](conduction-frozen-trial-step-decision.md).
The single authorized occurrence verified that the predecessor used native default
`trial_step = 2.0`, explicitly tested dimensionless `trial_step = 1.0`, reproduced
disentanglement convergence at iteration 531, and again failed Wannierisation after
1000 iterations. Its final spread exceeded the default-step comparator. It is retained
under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-trial-step1-blocked/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-trial-step1-blocked/).
The authorization is consumed and no retry is authorized. The subsequent authorized
optimizer branch replaced the failed parabolic line search with dimensionless
`fixed_step = 1.0`, as defined in
[`conduction-frozen-fixed-step-decision.md`](conduction-frozen-fixed-step-decision.md).
It reproduced disentanglement convergence but again failed Wannierisation after 1000
iterations, with a higher final spread than the native line-search comparator. It is
retained under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-fixed-step1-blocked/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-fixed-step1-blocked/).
Its authorization is consumed and no retry is authorized. The final narrowly scoped
optimizer diagnostic changed only the CG reset cadence from verified default
`num_cg_steps = 5` to `1`, as defined in
[`conduction-frozen-cg-reset-decision.md`](conduction-frozen-cg-reset-decision.md).
It reproduced disentanglement convergence but again failed Wannierisation after 1000
iterations and produced a substantially higher final spread than the default-CG
comparator. It is retained under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-cg-reset1-blocked/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-cg-reset1-blocked/).
Its authorization is consumed and no retry is authorized. A subsequent literature review
found that the current AiiDA high-throughput Wannier90 moderate and precise protocols use
`num_cg_steps = 200`. The resulting one-variable diagnostic is defined in
[`conduction-frozen-cg200-decision.md`](conduction-frozen-cg200-decision.md). It lowered
the final spread relative to the native-default-CG comparator, but failed Wannierisation
after 1000 iterations and did not meet even the literature-associated moderate two-atom
spread-change threshold. It is retained under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-cg200-blocked/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-cg200-blocked/).
Its authorization is consumed and no retry is authorized. The final one-variable
4000-iteration diagnostic defined in
[`conduction-frozen-cg200-iter4000-decision.md`](conduction-frozen-cg200-iter4000-decision.md)
also failed the strict gate. It briefly met the comparison AiiDA moderate two-atom
threshold but not the comparison precise or campaign thresholds, and large excursions
continued through iteration 3934. It is retained under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-cg200-iter4000-blocked/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-conduction-frozen-cg200-iter4000-blocked/).
Its authorization is consumed and no retry is authorized. Iteration-only and
optimizer-combination studies now stop under the prospective rule. The explicit
[`localization-convergence-policy-review.md`](localization-convergence-policy-review.md)
finds that the exact historical `1.0e-10 angstrom^2`/three-iteration pair lacks a
calculation-specific observable justification, while also finding that a moderate
threshold would not make the present construction robust. The scientific owner accepted
the prospective precise operational gate in
[`localization-convergence-policy-decision.md`](localization-convergence-policy-decision.md):
`2.0e-9 angstrom^2`, window 6 for the exact two-atom cell, separated from downstream
scientific acceptance and without retroactive reclassification. The first successor
scientific construction is defined in
[`lower-energy-frozen-window-decision.md`](lower-energy-frozen-window-decision.md). It
retains rank 10 and the `sp3s*` projections but freezes all four valence states plus only
sampled low-energy conduction states. Exact preflight is under
[`preflight/accepted-s1-wannier90-localization-lower-energy-frozen/`](preflight/accepted-s1-wannier90-localization-lower-energy-frozen/).
The occurrence solved Wannierisation at iteration 265 but exhausted 1000
disentanglement iterations with a smoothly decreasing final fractional delta
`-2.091e-9`. It is retained under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-lower-energy-frozen-blocked/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-lower-energy-frozen-blocked/).
Its authorization is consumed and no retry is authorized. The operator authorized the
recommendation to prepare one evidence-based, one-variable disentanglement-budget
successor. It is defined in
[`lower-energy-frozen-disentanglement-extension-decision.md`](lower-energy-frozen-disentanglement-extension-decision.md),
with exact preflight under
[`preflight/accepted-s1-wannier90-localization-lower-energy-frozen-dis2000/`](preflight/accepted-s1-wannier90-localization-lower-energy-frozen-dis2000/).
The authorized occurrence converged disentanglement at iteration 1290 and
Wannierisation at iteration 189. It is retained as provider-eligible evidence under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-lower-energy-frozen-dis2000-eligible/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-lower-energy-frozen-dis2000-eligible/).
Its authorization is consumed. Execution-free characterization subsequently verified
source reconstruction and recorded candidate interpolation, valley, curvature, and
locality observations without converting candidate-only quantities into failures. A
prospectively frozen 408-point direct-parent comparison was then executed once and is
retained under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-withheld-parent-nscf-408-david/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-withheld-parent-nscf-408-david/).
All valley-position targets were met, but the `14.5009%` indirect-gap error, two failed
longitudinal-mass comparisons, and all failed transverse-mass comparisons establish
that this provider-eligible candidate is not adequate for the declared SSSP-pilot
intended use. The research protocol now recommends a one-variable Gamma-origin
`6 x 6 x 6` construction-mesh successor with every other scientific and optimizer
coordinate held fixed. The prior 408-point parent set becomes revealed development
evidence, while a disjoint 402-point successor-confirmation geometry has been frozen
with its parent values unobserved. `8 x 8 x 8` remains conditional rather than
automatic. `12 x 12 x 12` is a bounded upper diagnostic only after `C8` still supports
the mesh-density hypothesis; its point count does not establish infinite-mesh
convergence. The exact `C6` NSCF preflight is retained under
[`preflight/accepted-s1-wannier-nscf-6x6x6-b12-david-c6/`](preflight/accepted-s1-wannier-nscf-6x6x6-b12-david-c6/).
A later exact authorization permitted one 216-point Davidson invocation with zero
retries; eligible handoff evidence is retained under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier-nscf-6x6x6-b12-david-c6/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier-nscf-6x6x6-b12-david-c6/).
The unchanged outer window selects 10--12 of the 12 parent bands over the refined mesh,
while the frozen window selects 4--6; this mesh-induced inventory consequence is retained
for attribution. The exact preprocessing preflight is retained under
[`preflight/accepted-s1-wannier90-preprocess-c6-lower-energy-frozen/`](preflight/accepted-s1-wannier90-preprocess-c6-lower-energy-frozen/).
One later bounded authorization produced a verified 216-point, eight-neighbor NNKP with
ten expanded projections; compact evidence is retained under
[`evidence/sssp-1.3.0-pbe-efficiency-wannier90-3.1.0-accepted-s1-preprocess-c6-lower-energy-frozen/`](evidence/sssp-1.3.0-pbe-efficiency-wannier90-3.1.0-accepted-s1-preprocess-c6-lower-energy-frozen/).
The exact converter preflight is retained under
[`preflight/accepted-s1-pw2wannier90-c6-lower-energy-frozen/`](preflight/accepted-s1-pw2wannier90-c6-lower-energy-frozen/).
One later bounded authorization produced finite, shape-consistent, source-correlated
AMN/MMN/EIG artifacts; compact evidence is retained under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-pw2wannier90-c6-lower-energy-frozen/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-pw2wannier90-c6-lower-energy-frozen/).
The exact localization preflight is retained under
[`preflight/accepted-s1-wannier90-localization-c6-lower-energy-frozen-dis2000/`](preflight/accepted-s1-wannier90-localization-c6-lower-energy-frozen-dis2000/).
One later bounded authorization completed natively but failed the provider eligibility
gate: disentanglement reached iteration 2000 with absolute fractional change
`4.679e-8`, 467.9 times the unchanged dimensionless tolerance. The blocked occurrence is
retained under
[`evidence/sssp-1.3.0-pbe-efficiency-wannier90-3.1.0-accepted-s1-localization-c6-lower-energy-frozen-dis2000-blocked/`](evidence/sssp-1.3.0-pbe-efficiency-wannier90-3.1.0-accepted-s1-localization-c6-lower-energy-frozen-dis2000-blocked/).
There is no provider-eligible `C6` operator. The operator subsequently authorized one
fresh optimizer-eligibility occurrence changing only `dis_num_iter` from 2000 to 4000;
its exact preflight is retained under
[`preflight/accepted-s1-wannier90-localization-c6-lower-energy-frozen-dis4000/`](preflight/accepted-s1-wannier90-localization-c6-lower-energy-frozen-dis4000/).
Disentanglement converged at iteration 3068, but Wannierisation remained unconverged at
iteration 4000 and the provider rejected the output. Evidence is retained under
[`evidence/sssp-1.3.0-pbe-efficiency-wannier90-3.1.0-accepted-s1-localization-c6-lower-energy-frozen-dis4000-blocked/`](evidence/sssp-1.3.0-pbe-efficiency-wannier90-3.1.0-accepted-s1-localization-c6-lower-energy-frozen-dis4000-blocked/).
The prospective stop rule now applies. A separate target-space review found that the
inherited outer window selected only 10--12 parent states across `C6`; the operator
therefore authorized preparation only of candidate `C6-T1`, whose `[-6.0, 21.0] eV`
outer window includes all 12 authenticated parent bands at every construction point.
Its no-execution preflight is retained under
[`preflight/accepted-s1-wannier90-localization-c6-t1-full-parent-outer-dis4000/`](preflight/accepted-s1-wannier90-localization-c6-t1-full-parent-outer-dis4000/),
but that localization is unexecuted and is no longer the selected next occurrence.
The subsequent parent-band decision adopted only the factor-two moderate band-count
heuristic from pinned `aiida-wannier90-workflows` 3.1.0 and selected `C6-B20`. Its exact
derivation, citation, adaptation limits, and conditional 30-band upper diagnostic are
recorded in
[`c6-b20-aiida-moderate-parent-band-decision.md`](c6-b20-aiida-moderate-parent-band-decision.md).
One separately authorized 20-band C6 NSCF then completed successfully with finite
values and an authenticated saved state. The enlarged inventory shows that bands 13
and 14 enter both investigated outer windows: the inherited `[-5.85, 19.02] eV`
window contains 10--14 states per point, while `[-6.0, 21.0] eV` contains 12--14.
Compact evidence and the full state-count analysis are retained under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier-nscf-6x6x6-b20-david-c6-b20/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier-nscf-6x6x6-b20-david-c6-b20/).
The separate
[`C6-B20-W21` decision](c6-b20-w21-outer-window-decision.md) selects outer window
`[-6.0, 21.0] eV` while retaining rank 10, the frozen window, and the projections. It
admits 12--14 states per point and therefore at least two excess outer-space dimensions
everywhere; this is an eligibility design, not evidence of convergence or adequacy.
The subsequent
[`AiiDA-precise convergence adaptation`](aiida-precise-convergence-adaptation-decision.md)
adopts the pinned two-atom convergence tuple: `conv_tol = 2.0e-9 angstrom^2`,
dimensionless `dis_conv_tol = 2.0e-9`, `conv_window = 6`, `num_cg_steps = 200`, and
40000-step ceilings for both optimizations. The earlier ungranted hybrid 4000-step
preprocessing request is superseded and must not be authorized. The distinct regenerated
[`AiiDA-precise preprocessing preflight`](preflight/accepted-s1-wannier90-preprocess-c6-b20-w21-aiida-precise/)
binds the precise-derived tuple. One separately authorized `wannier90.x -pp silicon`
occurrence then returned zero and produced an eligible, authenticated 216-point NNKP;
compact evidence is retained under
[`evidence/sssp-1.3.0-pbe-efficiency-wannier90-3.1.0-accepted-s1-preprocess-c6-b20-w21-aiida-precise/`](evidence/sssp-1.3.0-pbe-efficiency-wannier90-3.1.0-accepted-s1-preprocess-c6-b20-w21-aiida-precise/).
Its authorization is consumed. A deterministic no-execution
[`20-band conversion preflight`](preflight/accepted-s1-pw2wannier90-c6-b20-w21-aiida-precise/)
bound that NNKP to the authenticated `C6-B20` saved state. One separately authorized
`pw2wannier90.x` occurrence then returned zero and produced an eligible authenticated
20-band AMN/MMN/EIG interface; compact evidence is retained under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-pw2wannier90-c6-b20-w21-aiida-precise/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-pw2wannier90-c6-b20-w21-aiida-precise/).
Its authorization is consumed. The deterministic
[`precise-profile localization preflight`](preflight/accepted-s1-wannier90-localization-c6-b20-w21-aiida-precise/)
and the complete conditional
[`full-operator-to-reduction series`](preflight/c6-b20-w21-gated-series/) were then
prepared. One separately authorized localization converged natively at disentanglement
iteration 1517 and Wannierisation iteration 378. An initial provider rejection was a
false negative caused by comparing ten-decimal matrix coordinates with lossy
eight-decimal NNKP values. No-calculator reverification against the canonical WIN block
measured `3.300004713935323e-11`, passing the unchanged `1.0e-10` gate. Compact eligible
evidence is retained under
[`evidence/sssp-1.3.0-pbe-efficiency-wannier90-3.1.0-accepted-s1-localization-c6-b20-w21-aiida-precise-eligible/`](evidence/sssp-1.3.0-pbe-efficiency-wannier90-3.1.0-accepted-s1-localization-c6-b20-w21-aiida-precise-eligible/).
S10 and S20 are complete. The
[`provider reference-space correction`](localization-provider-reference-correction.md)
records the exact technical and evidence disposition. The separately authorized
[`S30 full untruncated characterization`](../analysis/c6-b20-w21-untruncated-characterization/)
is also complete: source reconstruction, pair Hermiticity, valleys, curvatures, masses,
and locality were retained without spatial truncation. The separately authorized
[`S40 revealed-408 comparison`](../analysis/c6-b20-w21-revealed-408-development/) is
complete without a calculator invocation. All valley positions pass, while the indirect
gap and 17 of 18 direction-matched effective masses fail their parent-fidelity
criteria. These revealed values are development-oracle labels, not operational
reduction diagnostics. They limit physical claims but do not block controlled reduction
from the structurally eligible S30 source. The separately authorized no-calculator
[`S90 spatial-truncation design`](../analysis/c6-b20-w21-spatial-truncation-design/) is
complete. It freezes all 18 complete physical-radius shells and selects no radius. The
separately authorized no-calculator
[`S100 complete-family evaluation`](../analysis/c6-b20-w21-spatial-truncation-evaluation/)
is also complete. All masks preserve pair closure and pair Hermiticity, the full-support
control is exact, and all frozen diagnostics are retained without accepting a radius or
fitting a model. The separately authorized no-calculator
[`S105 disposition`](../analysis/c6-b20-w21-spatial-truncation-disposition/) retains
full support, defining `H_T = H_W` and zero selected spatial-truncation error without
creating a post-observation threshold. The separately authorized no-calculator
[`S110 definition and fit`](../analysis/c6-b20-w21-slater-koster-definition-fit/)
stopped at the mandatory common-space gate: the projected ten-orbital `sp3s*` frame is
rank deficient at two C6 points under the native-format bound. No fit ran and S50
remains blocked pending a separate scientific decision. The current
[post-S110 protocol](../research-protocol/controlled-reduction-protocol-post-s110.tex)
orders the separately authorized continuation levels. The 402-point parent values remain
unobserved.

## Documentation set

| Document | Purpose |
| --- | --- |
| [`scientific-contract.md`](scientific-contract.md) | Physical branches, state spaces, unresolved decisions, and non-transfer rules |
| [`seed-structure-decision.md`](seed-structure-decision.md) | Exact selected provisional \(S_0\), identity, role, rationale, and non-transfer boundary |
| [`architecture-plan.md`](architecture-plan.md) | Existing Project Koios capability, missing capability, package ownership, and documentation-first work packages |
| [`execution-contract.md`](execution-contract.md) | Fail-closed preflight, stage boundaries, artifact policy, authorization packets, and failure behavior |
| [`verification-plan.md`](verification-plan.md) | Software, numerical, scientific, and independent-verification evidence and gates |
| [`readiness.md`](readiness.md) | Inspected repository and local-resource inventory, exact known identities, and current blockers |
| [`wannier90-localization-convergence-controls.md`](wannier90-localization-convergence-controls.md) | Central inventory of disentanglement, Wannierisation, optimizer, scientific-target, default, unit, and tested-branch controls |

## Scientific campaign order

The predecessor campaign is not part of the later five-occurrence Wannier route. Its
fixed order is:

1. joint coupled-cutoff and k-point qualification on the exact, explicitly provisional
   [`Si.PrimitiveUnitCell.RightHanded` seed \(S_0\)](seed-structure-decision.md),
   yielding only \(Q_0@S_0\);
2. zero-pressure structural convergence under \(Q_0\), yielding a mechanically
   qualified structure \(S_1\);
3. fresh joint setting confirmation on \(S_1\); and
4. re-relaxation and reconfirmation whenever the selected setting changes, until an
   exact stable pair \((S_*,Q_*)\) is accepted or the frozen budget ends
   inconclusively.

Only the accepted pair may emit a new, separately authorized parent-SCF requirement
for the separate SCF→NSCF→preprocessing→converter→localization route. A confirmation
SCF is not reused as that parent under this architecture.

## Admission rule for a successor

A numerical-qualification version may use an exact seed structure only when its
provisional status and non-transfer boundary are explicit. A production-parent version
requires the accepted pair \((S_*,Q_*)\). Every simulation version additionally
requires:

1. an accepted physical branch for its declared purpose;
2. exact executable and pseudopotential identities;
3. frozen inputs, numerical settings, warning policy, and stop policy;
4. a declared external workspace and compact-artifact policy;
5. expected runtime and resource bounds;
6. explicit authorization for the bounded QE or Wannier90 execution; and
7. an independent experiment-verification contract.

No empty stage scripts are provided. A stage is created only when its input, output,
failure, provenance, and verification contracts exist.

## Required order of work

1. Review and correct this documentation set.
2. Resolve every scientific decision assigned to this calculation owner.
3. Implement only accepted reusable capability in Project Koios.
4. Add deterministic tests and render-only demonstrations; do not execute a
   calculator.
5. Materialize exact declarations here and verify all identities.
6. Prepare one bounded execution authorization packet.
7. Execute only after explicit authorization, then retain evidence without automatic
   promotion.

The expected simulation families are historical-parent comparison, production-parent
setting qualification, conduction-valley characterization, Wannier
construction/qualification, and prospectively declared sensitivity controls. They
remain distinct versions. A later stage may consume only a verified predecessor and
must not overwrite it.

## Nonclaims

This plan does not:

- accept the 5.43 Å Project Koios example structure as a production PBE lattice;
- relabel the historical PseudoDojo v0.4.1 Si UPF as v0.5/stringent;
- accept the retained SSSP/QE 7.5 observations as production numerical settings;
- declare locally available QE or Wannier90 executables scientifically accepted;
- authorize pseudopotential acquisition or calculator execution;
- define publication-grade numerical tolerances; or
- commit the retained wavefunctions, charge densities, or other large saved-state
  files.
