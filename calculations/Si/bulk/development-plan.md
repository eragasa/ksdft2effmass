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

- the selected 680-byte `Si.PrimitiveUnitCell` seed \(S_0\), SHA-256
  `6e048c7001f329459e85f321e7bd406f4dd871d6fabf8d12fa349a1623f87ccc`, explicitly
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
cannot fill this gate.

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
