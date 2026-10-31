# Bulk-silicon calculation development plan

## Objective

Construct and qualify one scalar-relativistic, non-spin-polarized, non-SOC bulk-silicon
parent; build a compatible ten-spatial-orbital Wannier representation; and determine
whether a frozen finite hierarchy contains a common witness satisfying both spectral
and aligned-operator tolerances.

Every conclusion is bounded by the declared pseudopotential, exchange--correlation
approximation, geometry, meshes, retained manifold, alignment family, candidate
inventory, and verification tolerances.

## Stage 0 — close the audited-bootstrap disposition

Inputs:

- the retained direct-results audit;
- the finite-setting analysis and decision packet;
- the setting-disposition record; and
- the IEEE-warning investigations.

Completed decisions and diagnoses:

1. C48/K8 (48/192 Ry and a shifted $8\times8\times8$ mesh) was selected as a
   provisional finite-setting parameter pair;
2. the first instrumented trap was localized to external OpenCL discovery during
   startup; and
3. a separate cross-BLAS, cross-MPI `ZHEGVX` operation during initial-wavefunction
   subspace diagonalization was classified as IEEE divide-by-zero.

Remaining production-acceptance gates:

1. compare C48/K8 observables and residuals through an independently identified
   established QE/toolchain path;
2. retain or further classify the invalid, overflow, and underflow flags according to
   the comparator evidence;
3. freeze the exact mixed cutoff--mesh interaction corner implied by C48/K8; and
4. authorize every bounded successor execution separately.

These items do not block explicitly labelled downstream development or exploratory
analysis under the [provisional-use disposition](provisional-use-disposition.md). They
do block production-parent and publication-grade acceptance. The provisional selection
is not an infinite-setting result.

## Stage 1 — freeze the seed-bound numerical-qualification contract

Before the first successor execution, bind:

- the selected 692-byte `Si.PrimitiveUnitCell.RightHanded` seed \(S_0\), SHA-256
  `7bef37dfe20ce58a137de942ec1fa0aa50d6e7049b0265790f12171bc834529a`, explicitly
  labelled as a qualification geometry rather than an accepted production lattice;
- the intended physical branch;
- exact Quantum ESPRESSO executable and input identities;
- exact pseudopotential content identity and redistribution boundary;
- exchange--correlation approximation, occupations, solver policy, and warning policy;
- a prospectively declared coupled wavefunction/charge-density cutoff inventory;
- a prospectively declared k-point inventory, offset, symmetry policy, and mixed-corner
  checks;
- observables, selection rules, extension budget, retry/stop policy, and expected
  compact and external native artifacts; and
- separate bounded execution authorization for every admitted occurrence.

A failed identity or authority gate stops the calculation. No result on \(S_0\) is a
transferable cutoff or k-point certificate for another structure.

## Stage 2 — qualify settings, then structure, then confirm the pair

The execution order is fixed:

1. **Cutoff and k-point qualification on \(S_0\).** Evaluate the declared coupled
   cutoff, reciprocal-sampling, and required mixed-corner controls with independent SCF
   occurrences. Produce only a structure-scoped provisional setting
   \(Q_0@S_0\).
2. **Structural convergence.** Use \(Q_0@S_0\) for a separately authorized
   zero-pressure structural route and assess final-cell validity, force criteria,
   pressure residual, allowed cell-mode changes, and exact artifact lineage. A
   provider-reported relaxation success is not by itself an accepted lattice. A
   mechanically qualified result produces \(S_1\).
3. **Final-setting confirmation on \(S_1\).** Repeat a prospectively declared joint
   cutoff/k-point confirmation stencil, including sufficient stricter high-side
   context, and produce \(Q_1@S_1\). A single SCF at the earlier candidate is not a
   convergence confirmation.
4. **Stable-pair decision.** Accept only an exact structure/settings pair
   \((S_*,Q_*)\). If confirmation changes the selected setting, re-relax under the new
   setting and reconfirm on the resulting structure. Continue only within a frozen
   iteration budget; otherwise retain an inconclusive or budget-exhausted result.

Steps 1 and 2 have now produced provisional Gamma-centered K10/42/336 Ry
\(Q_0@S_0\) and provisional
`Si.PrimitiveUnitCell.RightHanded.RelaxedS1`, respectively. The successful
FCC-native relaxation does not transfer \(Q_0\) to \(S_1\). The authorized
Gamma-centered K6/K8/K10/K12 stage at fixed 42/336 Ry has now repeated the declared
K12-reference rule on the exact 758-byte \(S_1\), SHA-256
`d131107753512c53dc0a32b9e07e0081f8277d8eeafcb9fad5f1fc7f153ded03`, and again
selects K10. The separately authorized cutoff stage then reused C42 without rerunning
it, evaluated C30/C36/C48/C54/C60, and again selected 42/336 Ry by the declared
C60-reference rule. Step 3 is complete under the calculation-owned sampled-setting
rules. The operator accepted the resulting exact pair under those rules. A new parent
SCF, construction NSCF, Wannier preprocessing, converter, and provider-eligible
localization occurrence subsequently completed with authenticated lineage. A separately
authorized 408-point direct-parent NSCF then completed the prospective intended-use
comparison. The rank-10 candidate met every valley-position target but did not meet the
indirect-gap or effective-mass targets. The research protocol now selects a
one-variable `C6` construction-mesh successor: Gamma-origin `6 x 6 x 6` with structure,
parent, bands, rank, windows, projections, and optimizer controls held fixed. The prior
408-point parent data become revealed development evidence; a separate 402-point
parent-informed confirmation geometry is frozen with parent values still unobserved.
`C8` is conditional rather than automatic, and `C12` is only a bounded upper diagnostic
after a completed `C8` review; its size alone cannot establish mesh convergence. At
that stage, component-operator and reduction work remained blocked pending a converged,
structurally eligible full source. The exact `C6` NSCF preflight
specified 216 points, 12 bands, one process, zero retries, a 600-second timeout, and a
512 MiB retention ceiling. A later exact authorization permitted one successful
invocation. Its verified saved state was an eligible preprocessing handoff. The fixed
outer window selects 10--12 states per point rather than all 12 everywhere, an
attributable consequence of the refined mesh. One separately authorized
`wannier90.x -pp` occurrence then produced a source-correlated 216-point NNKP with eight
neighbors per point and ten expanded projections. One separately authorized
`pw2wannier90.x` occurrence then produced finite, shape-consistent AMN/MMN/EIG artifacts
with exact NNKP and QEXSD correlations. One separately authorized exact `C6`
localization occurrence then completed natively but did not meet the unchanged
`dis_conv_tol = 1.0e-10` gate by the fixed 2000-iteration budget. Its final absolute
fractional change was `4.679e-8`. The branch is an optimizer-convergence failure with no
provider-eligible operator. One fresh 4000-step disentanglement-budget occurrence then
changed no other coordinate and consumed no failed checkpoint. Disentanglement converged
at iteration 3068, but Wannierisation did not meet its six-step gate by iteration 4000;
the provider rejected the output. The prospective stop rule now forbids automatic
budget extension or `C8` escalation. A separate target-space review identified that the
inherited outer window selected only 10--12 parent states across `C6`. Candidate
`C6-T1` was prepared with outer window `[-6.0, 21.0] eV`, selecting all 12 authenticated
parent states at every construction point, but it remains unexecuted and is no longer
the selected next occurrence. The selected broader-parent stage `C6-B20` changed only
the NSCF parent-band count from 12 to 20, following the factor-two moderate
band-inventory heuristic in pinned `aiida-wannier90-workflows` 3.1.0. One exact,
separately authorized NSCF completed successfully. Its authenticated inventory shows
10--14 states under `[-5.85, 19.02] eV` and 12--14 under `[-6.0, 21.0] eV`; bands 13
and 14 enter both windows, while band 15 remains above `21.0 eV` everywhere. The
separate target-space decision selects `C6-B20-W21` with outer window
`[-6.0, 21.0] eV`, retaining rank 10, the frozen window, and the projection family.
This provides at least two excess outer-space dimensions at every point but does not
establish optimizer convergence or adequacy. The prospective route adopts the pinned
AiiDA precise convergence-derived tuple for the two-atom cell: `conv_tol = 2.0e-9
angstrom^2`, dimensionless `dis_conv_tol = 2.0e-9`, `conv_window = 6`,
`num_cg_steps = 200`, and 40000-step ceilings for both optimizations. This supersedes
the unexecuted hybrid 4000-step preprocessing request. One newly rendered 20-band
preprocessing input was separately authorized and executed exactly once. Wannier90
returned zero, emitted its native NNKP completion line, and the maintained verifier
confirmed the 216 ordered points, lattices, excluded-band inventory, and rank-10
projections. Its authorization is consumed. A deterministic no-execution conversion
preflight now binds the authenticated 20-band saved state and eligible NNKP to fresh
AMN/MMN/EIG output requirements, a 300-second timeout, and a 256 MiB retained-byte
ceiling. One separately authorized conversion returned zero and produced finite,
shape-correct 20-band interface artifacts with exact NNKP-neighbor correlation and
EIG-to-QEXSD agreement within `5.37e-13 eV`. Its authorization is consumed.
A fresh precise-profile localization preflight bound those artifacts with no checkpoint
or failed-output consumption, one process, a 14,400-second timeout, a 128 MiB
retained-byte ceiling, and zero retries. One separately authorized occurrence completed
natively: disentanglement converged at iteration 1517 and Wannierisation at iteration
378. The provider initially rejected the output because it compared matrix coordinates
with the lossy eight-decimal NNKP representation. ProjectKoios corrected the reference
space to the canonical WIN block. No-calculator reverification measured gauge and
`u_dis` residuals of `3.300004713935323e-11`, passing the unchanged `1.0e-10` gate.
The occurrence is provider-eligible; the original rejection remains false-negative
audit evidence. Separately authorized S30 full untruncated characterization then
verified source reconstruction, pair Hermiticity, valleys, curvature masses, and the
complete locality curve without applying spatial truncation. The separately authorized
no-calculator S40 comparison then applied the frozen targets to the revealed 408-point
parent evidence. All six valley-position comparisons passed, but the indirect-gap error
was `12.7605%` against `5%`, all six longitudinal masses failed, and 11 of 12 transverse
masses failed the `8%` evaluation criterion. These discrepancies are revealed
parent-oracle labels, not operational reduction diagnostics. They limit physical-fidelity
claims but do not block controlled spatial truncation or Slater--Koster reduction from
the structurally eligible S30 operator. The reductions, diagnostic rules, fits, and
predicted hidden errors must be frozen before the 402-point confirmation parent values
are observed. The S90-through-S110
[controlled-reduction protocol](research-protocol/controlled-reduction-protocol.tex)
formalized this hidden-oracle separation. Separately authorized S90 design then froze
all 18 complete physical-radius shells and the operational tail, operator, spectral,
valley, curvature, and mass diagnostics without selecting a radius or consuming
402-point parent values. Separately authorized S100 then evaluated all 18 masks against
the full source without accepting a radius. Every mask preserves pair closure and pair
Hermiticity; the full-support control is exact; and the onsite-only valley/mass
observables are explicitly undefined. The first three dispersive masks fail to preserve
all declared Delta identities, while later direct and observable changes are retained as
descriptive controlled-reduction evidence. Separately authorized S105 then retained the
383-representative full-support shell: `H_T = H_W`, so the selected spatial-truncation
error is identically zero. No post-observation threshold was created to accept a
nontrivial shell, and the parent numerical-convergence tolerances were not repurposed as
reduction criteria. Separately authorized S110 then stopped at the mandatory
common-state-space gate: the TB-anchored ten-orbital `sp3s*` projection has resolved
rank 9 at Gamma and one additional C6 point under the native-format singular-value
bound. No fit ran, no parameter vector was produced, and S50 remains blocked. The
default disposition is to retain no Slater--Koster reduction from this source. The
current
[post-S110 protocol](research-protocol/controlled-reduction-protocol-post-s110.tex)
orders separately authorized continuation by increasing implementation difficulty:
reusable foundations, spectral-only feasibility, global-unitary rank-10 fitting,
rank-9 projection, and a new Wannier source. The 30-band factor-three adaptation
remains a conditional source-fidelity diagnostic, not an automatic successor or a
prerequisite for controlled reduction.

A changed lattice changes reciprocal vectors. Equal integer mesh tuples therefore do
not prove equal sampling resolution; the confirmation must apply the declared
reciprocal-space rule or explicitly reassess the retained tuple.

Throughout this stage, keep total-energy, stress, fixed-point band/gap, branch identity,
and later curvature requirements separate. Finite adjacent-setting stability must not
be reported as an infinite-basis bound. Outputs must include an independent
compact-result verifier and either an accepted \((S_*,Q_*)\) disposition or a bounded
failure/inconclusive record.

## Stage 3 — characterize the retained band manifold

Begin only from the accepted exact pair \((S_*,Q_*)\). The final parent SCF is a new,
separately authorized route occurrence. A confirmation occurrence cannot double as the
parent in this architecture; changing that boundary would require separate review.

Locate and identity-track the conduction valley rather than assuming the nominal
`Delta_0.85` probe is the minimum. Define disjoint construction and withheld momentum
sets. Retain eigenpair residuals, projector or cluster identities, isolating gaps where
available, and explicit degeneracy handling.

Effective-mass analysis requires a separately reviewed stencil or fit window,
conditioning assessment, and convergence rule; fixed-point band agreement is
insufficient.

## Stage 4 — construct and qualify the Wannier bridge

Subject to separate Wannier90 authorization, freeze projections, windows, meshes,
centers, spreads, convergence status, symmetry conventions, reciprocal sewing, and
energy reference. Compare direct-parent and Wannier bands, projectors, and represented
operators on construction and withheld meshes.

The tutorial-scale silicon Wannier preview is a software/integration precursor only and
cannot fill this gate. The first provider-eligible `4 x 4 x 4`, rank-10 lower-energy
frozen-window candidate completed a prospectively frozen direct-parent comparison but
was not adequate for the declared SSSP-pilot intended use. Optimizer changes cannot
repair that scientific disposition. The protocol-first `C6` recommendation changes only
the Gamma-origin construction mesh from `4 x 4 x 4` to `6 x 6 x 6`; all other scientific
and optimizer coordinates remain fixed. Any later band, rank, window, projection,
conditional `C8`, or bounded-diagnostic `C12` revision is a separate decision, and every
calculator occurrence requires its own exact preflight and authorization.

## Stage 5 — freeze the local-model decision problem

Before fitting, declare:

- the finite `sp3s*` hierarchy and every support extension;
- the retained rank and orbital semantics;
- alignment family and group constraints;
- spectral and operator losses with exact normalizations;
- training and withheld sets;
- cost ordering;
- search budgets and global/exhaustive status; and
- thresholds justified from measured numerical floors.

Separate channel optima do not constitute a common witness.

The calculation-local Vogl 1983 LCAO `sp3s*` control now provides the accepted complete
Table 1 transcription and an independently implemented spinless ten-band Bloch
Hamiltonian. It can test representation conventions and later reduction machinery, but
it neither freezes the candidate hierarchy nor supplies evidence of adequacy against the
future accepted first-principles parent.

## Stage 6 — perform joint admissibility analysis

For every candidate, evaluate the spectral set and aligned-operator set under the same
model, support, alignment, and energy reference. Produce either:

- a common witness;
- a reviewed separation certificate for the frozen finite inventory; or
- an explicit inconclusive outcome.

A failed local optimizer is not evidence that the feasible set is empty.

## Stage 7 — withheld validation and attribution

Evaluate disjoint band, gap, valley, mass, projector, operator, and locality channels.
Attribute stable residuals by onsite/hopping block, orbital semantics, symmetry channel,
and support shell where justified. Repeat prospectively declared parent, Wannier,
stencil, map-resolution, and threshold sensitivities.

## Stage 8 — retain and verify

Create a no-overwrite package containing exact inputs, compact outputs, schemas,
provenance, checksums, source identities, candidate inventory, thresholds, independent
verification, plots derived only from verified inputs, and a calculation-facing
technical report.

Only after these gates may Paper D promote authenticated values into a completed
material result. Formal certificates may check exact finite claims but do not certify
Quantum ESPRESSO, Wannier90, binary64 execution, or physical validation.
