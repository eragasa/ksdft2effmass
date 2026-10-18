# Multiband-alignment numerical owner boundary

## Decision and status

This architecture-first review inventories the implemented
`Periodic1DMultibandAlignmentCalculator` before any further numerical extraction. It
changes no source, API, result schema, verifier, retained evidence, or dependency.

The immediate decisions are:

- no further reusable mechanism should be extracted from the maintained constrained-
  admissible-sets experiment;
- M2's experiment composition, feature and channel meaning, finite attack, sample
  roles, normalization, labels, thresholds, locality interpretation, result
  correlation, serialization, and intentionally direct verification remain KSD-owned;
- direct finite-periodic linear algebra remains a candidate for separately reviewed
  `projectkoios.numerics` slices;
- the invariant-only Hermitian spectral-subspace slice is implemented and qualified at
  `projectkoios-optimization@23e1c88772f1bc9a1505cd25df5418cd945a76fa` under
  `projectkoios.numerics.linalg`; the current live dependency chain is resolved through
  PhysKit `7120b735c7e3e450aa8924780a71deb59d812632` and Optimization
  `2c6dd7f717722f6b0495feb8cfe1287a104268a6`;
- that invariant slice returns no frames; the maintained successor requires
  backend-qualified eigenvector-diagonal frames for historical parity, with the backend
  and version retained and no claim of cross-backend canonical coordinates;
- any operation that **selects** an alignment or unitary transformation is a candidate
  for `projectkoios.optimization.alignment`;
- square pointwise and aggregate Procrustes operations must reject numerically
  rank-deficient cross-covariances rather than complete unconstrained null-space action;
  and
- the current local NumPy frame and SVD selection mechanisms are explicitly
  `TECH_DEBT` until reviewed owner operations can replace them directly.

This page now records the bound invariant Hermitian slice, the selected successor
contracts, and deferred extraction candidates. The temporary mechanisms and exit
criteria are tracked in the [technical-debt record](../../../../../../tasks/tech_debt/composite-band-alignment-and-locality/index.md).
Existing cohesive KSD `solid_state` capabilities remain supported until a
matching owner slice is reviewed, version-bound, and can replace their mechanism. KSD
consumes owner contracts directly where their unit-free boundaries already fit; it does
not add pass-through facades.

## Current calculation decomposition

The calculator currently composes the following stages in order:

1. interpolate the finite block-hopping parent on the training mesh;
2. compute retained eigenvalues and raw retained eigenframes;
3. polar-transport the frame path and distribute closure holonomy;
4. construct and apply the experiment's rank-two momentum-dependent attack;
5. select pointwise Procrustes transformations;
6. select one aggregate global unitary transformation;
7. represent the parent operator in reference, attacked, pointwise-aligned, and
   globally constrained frames;
8. Fourier-transform the first three represented channels and reconstruct them;
9. calculate finite-mesh gap, frame, projector, operator, and Hermiticity diagnostics;
10. truncate declared hopping ranges and evaluate training and withheld spectra; and
11. correlate every result with the exact M2 controls and sample roles.

Only stages that are demonstrably owner-neutral numerical mechanisms are extraction
candidates. Their placement in one current Action does not make the full calculation a
reusable optimizer or workflow.

## Candidate ownership inventory

| Current behavior | Prospective owner | KSD responsibility that remains | Disposition |
|---|---|---|---|
| Centered reciprocal mesh identity, units, representative convention | PhysKit lattice primitives plus KSD adapters | M2 mesh size, period, sample role, and centered finite convention | Keep local; do not duplicate lattice ownership |
| Finite hopping interpolation and complete reciprocal/cell Fourier pair | `projectkoios.numerics.finite_periodic` | Units, reciprocal geometry, block meaning, representative identities, and reconstruction tolerance | Numerics candidate after represented-space contract review |
| Dense Hermitian invariant spectrum/projector | `projectkoios.numerics.linalg.hermitian_spectral_subspace` at owner revision `23e1c88772f1bc9a1505cd25df5418cd945a76fa` | Lowest-group selection, retained rank, energy units, scientific gap meaning, and sample roles | Implemented, qualified, and dependency-bound; consume directly when KSD needs invariant output |
| Dense Hermitian eigenframes | Future `projectkoios.numerics.linalg` frame-selection capability | Backend-qualified eigenvector-diagonal frames for historical parity, backend/version provenance, and no canonical-frame claim | `TECH_DEBT`: selected locally through NumPy until a reviewed owner contract is available; the invariant slice is not a substitute |
| Frame isometry, overlaps, projectors, supplied-unitary application, and $F^\dagger H F$ | `projectkoios.numerics.finite_periodic` | Frame/path identity, sewing meaning, basis/gauge interpretation, and unit-bearing operator records | Numerics candidate |
| Pointwise unitary Procrustes selection | `projectkoios.optimization.alignment` | Which paths are compared, coordinate and sewing compatibility, channel identity, and scientific interpretation | `TECH_DEBT`: contract rejects numerical rank deficiency; local SVD selection remains until owner extraction |
| One-global-unitary aggregate selection | `projectkoios.optimization.alignment` | The one-transform feasible-family meaning and equal training-point aggregation selected by M2 | `TECH_DEBT`: same rejection policy; local aggregate SVD selection remains until owner extraction |
| Neighborwise polar transport and closure transformation selection | `projectkoios.optimization.alignment`, consuming Numerics frame records | Reciprocal-path ordering, sewing convention, overlap threshold meaning, and closure interpretation | Defer until Procrustes and degenerate-closure policies are qualified |
| Rank-two sine-series attack and path rotation inventory | KSD experiment composition | Entire attack family, coefficients, angles, and role as a controlled gauge perturbation | Keep in KSD |
| Symmetric range selection and omitted-block locality interpretation | Numerics kernel may apply a supplied mask; KSD owns the study | Range inventory, shell meaning, training/withheld comparisons, and locality claims | Keep policy in KSD; kernel extraction optional |
| Gap, Hermiticity, frame/projector/operator defects, and band errors | Numerics may own primitive evaluations | Units, thresholds, channel separation, aggregation, and evidentiary meaning | Extract only narrow primitives, never the M2 disposition policy |
| Definition, aggregate results, serialization, and independent verifier | KSD | Exact controls, identities, correlations, wire compatibility, provenance, and evidence boundary | Keep in KSD |

`projectkoios.numerics` must consume owner-neutral finite arrays and explicit ordering; it
must not redefine PhysKit direct/reciprocal lattices or acquire KSD units, model roles,
mesh roles, thresholds, or scientific labels. Optimization may depend on Numerics;
Numerics must not depend on Optimization or KSD.

## Bound invariant Hermitian slice and remaining eigenframe nonuniqueness gate

A Hermitian eigensolver does not in general define reproducible eigenvector coordinates.
Each nondegenerate eigenvector is free up to a complex phase, and every degenerate
eigenspace admits an arbitrary internal unitary rotation. Near-degenerate grouping adds a
numerical decision governed by a scale and cluster tolerance. Sorting eigenvalues and
calling one backend's dense eigensolver therefore does not define cross-backend frame
identity.

A reviewed frame-producing Numerics contract must choose and version one of three
materially distinct behaviors:

1. **Backend-qualified eigenframes.** Return the eigenvectors selected by an identified
   backend and version, together with residual and orthonormality diagnostics, while
   making no cross-backend phase or degenerate-basis reproducibility claim. This is the
   smallest frame-producing contract, but retained frame coordinates remain coupled to
   the backend.
2. **Deterministic coordinate-dependent frames.** Freeze an eigenvalue-cluster rule;
   fix each nondegenerate vector's phase through a declared coordinate-pivot rule; and
   build each degenerate-block basis from its invariant projector by projecting standard
   coordinate vectors in fixed index order, applying a specified reorthogonalization
   procedure, accepting pivots under a declared tolerance, and fixing their phases. This
   can provide repeatable coordinates for declared inputs, but the result is coordinate
   dependent rather than basis invariant and must fail closed when completion cannot
   satisfy its contract.
3. **Invariant-only output.** Return ordered eigenvalues and selected-subspace spectral
   projectors, leaving any frame selection to a separate capability with its own policy.
   This avoids presenting arbitrary eigenvectors as canonical but cannot directly supply
   every downstream frame-based operation.

The implemented first owner boundary is the third contract: owner revision
`23e1c88772f1bc9a1505cd25df5418cd945a76fa` exposes the complete ascending spectrum and
one caller-selected isolated-range projector without public eigenvectors. It retains the
original input-Hermiticity evidence, the explicit symmetrized representative evidence,
boundary gaps and applied numerical policy, complete-eigensystem residuals, and
projector diagnostics. Numerics must not export supposedly canonical Hermitian
eigenvectors until the eigenvalue-cluster tolerance, phase pivot, degenerate-block
completion, failure behavior, and independent verification are frozen. Qualification of
any future frame output must include direct eigen-residual, orthonormality,
phase-perturbation, degenerate-block rotation, near-cluster-cutoff,
coordinate-permutation, and repeatability cases. Comparing one eigensolver call with
itself is not an independent oracle.

KSD continues to own selection of the lowest group, external-gap meaning, retained rank,
sample roles, units, and scientific interpretation. The maintained successor requires
backend-qualified eigenvector-diagonal frames to preserve historical parity. The
backend and version must be retained, and neither KSD nor a future owner may describe
those coordinates as canonical across backends or within degenerate eigenspaces.
Projector-derived frames would be a different scientific protocol and are not selected
for this migration.

## Square complex Procrustes contract required before extraction

For a candidate frame $C$ and reference frame $R$ with equal retained rank $p$, M2
selects a unitary $U\in\mathbb C^{p\times p}$ minimizing

$$
\lVert CU-R\rVert_F^2.
$$

With cross-covariance $M=C^\dagger R=L\Sigma V^\dagger$, the current implementation
uses $U=LV^\dagger$. The aggregate channel replaces $M$ by the ordered sum of the
per-point cross-covariances before applying the same construction.

A reusable owner contract must state all of the following explicitly:

- source/target orientation and therefore the direction of the returned transform;
- real-valued objective definition and Frobenius normalization, if any;
- square-unitary versus rectangular partial-isometry operation;
- ordered batch and aggregate semantics;
- singular values, numerical rank, and rank cutoff;
- residual evaluation from the original inputs;
- unitary and stationarity checks;
- condition reporting, with no finite condition claim for numerical rank deficiency;
- backend identity and failure translation; and
- the behavior when the optimizer is not unique.

The owner should use `rank_tolerance=None` for its backend-defined default cutoff and
report the applied cutoff. KSD must not invent a second rank rule inside its adapter.

## Rank-deficient nonuniqueness and deterministic completion gate

When $\operatorname{rank}M=r<p$, the Procrustes objective has multiple optimal unitary
transformations. Returning the raw product of complete backend SVD factors silently
selects backend-dependent null-space bases. That is not a portable deterministic
contract.

The maintained successor selects the first behavior: reject numerically rank-deficient
inputs and return no transformation. This is a fail-closed domain restriction, not a
claim that the nonunique optimization problem has no solutions. A future deterministic
completion would define a broader, materially different contract and is not required by
this experiment.

If a later concrete consumer requires completion, a qualifying coordinate-dependent
policy would need to:

1. determine numerical rank from the declared cutoff;
2. retain the unique support partial polar factor $L_rV_r^\dagger$;
3. form left and right null-space projectors;
4. derive each null basis by projecting standard coordinate vectors in fixed index
   order, applying a specified reorthogonalization algorithm, and accepting pivots under
   a declared completion tolerance;
5. fix each vector's phase by making its first accepted pivot real and positive;
6. pair left and right null vectors in canonical order; and
7. return
   $U=L_rV_r^\dagger+N_LN_R^\dagger$
   with retained completion-policy and defect diagnostics.

The coordinate dependence of this completion must be documented; it is deterministic,
not basis invariant. Failure to construct the declared number of null vectors must fail
closed. Tests must cover zero, rank-one, repeated-singular-value, near-cutoff, phase,
permutation, and backend-repeatability cases. They must verify objective optimality and
unitarity independently rather than using one SVD call as its own oracle.

The human-owned decision is closed for this successor: rank-deficient pointwise and
aggregate cross-covariances are rejected. The current local mechanisms are retained only
as `TECH_DEBT` while Optimization completes its already-authorized higher-priority box-
quadratic work.

## Transport and closure follow after Procrustes

`PolarBandFrameTransporter1D` repeatedly selects Procrustes transformations and then
selects a distributed root of the sewn closure unitary. It is not merely a matrix
multiplication utility. Its extraction must follow, not precede, the square Procrustes
contract.

Sorting closure eigenphases does not by itself define eigenvectors within degenerate or
near-degenerate phase subspaces. A future transport contract must additionally freeze:

- sewing orientation and endpoint convention;
- closure polar-factor rank acceptance;
- phase branch and ordering;
- degenerate-phase subspace handling;
- deterministic basis completion;
- the distribution fractions along the finite path; and
- retained local-overlap, closure, and holonomy diagnostics.

Phase synchronization or closure-root selection therefore belongs with Alignment, while
frame/path storage, overlaps, projectors, and application of supplied transformations
belong with Numerics.

## KSD binding and verification requirements

KSD calls a reviewed owner operation directly when its unit-free contract fits. It must
not introduce a pass-through solver facade or result wrapper merely to rename the owner
API. The experiment composition must:

- construct owner-neutral matrices from identified KSD frames;
- bind exact source/target orientation and point order;
- pass raw objective controls without hidden rescaling;
- use returned transforms directly in the existing scientific composition;
- preserve path, mesh, sewing, rank, and channel identities in experiment-owned results;
- independently reconstruct aligned frames and KSD diagnostics; and
- bind the reviewed owner commit and operation contract in the experiment version.

The M2 verifier must not call the producer or owner alignment solver. Direct
reconstruction of objectives, unitary identities, frame/projector defects, Fourier
blocks, and result correlations remains KSD-owned. Shared BLAS/LAPACK or array libraries
must be disclosed as a limitation; passing numerical parity is not scientific
validation.

## Separate extraction sequence

1. **Completed:** freeze this inventory and the no-further-M3-extraction decision.
2. **Completed:** implement, qualify, and bind the invariant-only Hermitian
   spectrum/projector capability before eigenframes.
3. **Completed decision:** require backend-qualified eigenvector-diagonal frames for
   historical parity, retain backend/version provenance, and make no canonical-frame
   claim.
4. **Completed decision:** reject numerically rank-deficient pointwise and aggregate
   Procrustes cross-covariances; do not complete null-space action.
5. **`TECH_DEBT`:** after Optimization's current box-quadratic work closes, implement
   and qualify square pointwise and aggregate complex Procrustes in Optimization.
6. Replace KSD transformation-selection mechanisms with direct owner calls and verify
   exact parity independently; do not leave forwarding facades.
7. Review transport/closure extraction only after the Procrustes contract is stable.
8. Broaden rectangular partial-isometry or higher-dimensional path capabilities only
   when a concrete consumer requires them.

The current authorization covers the exact dependency binding. It does not authorize a
production calculation, retained run, KSD commit or push, release, or modification of
historical M2/M3 evidence.
