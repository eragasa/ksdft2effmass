# Constrained admissible-sets experiment migration

## Maintained identity and location

The publication-independent family is

```text
ksdft2effmass.campaign.model-adequacy.periodic1d.constrained-admissible-sets
```

Its maintained successor is being assembled under
`experiments/model-adequacy/periodic1d/constrained-admissible-sets/`. Historical `M3`,
conference, paper, and appendix labels remain aliases only. Existing source and retained
calculation evidence are not rewritten by these development slices. The experiment's
compatibility, certified-separation, unresolved, evidence-correlation, and independent-
verification meanings follow the shared
[admissible-set evidence semantics](analysis/model_adequacy/admissible-set-evidence-semantics.md).
Its finite-angle family, rectangle, thresholds, containment premise, and certificate
construction remain experiment-owned.

## Implemented migration slices

The first slice established the Optimization-owned bounded quadratic geometry. The
second slice now composes an exact rank-two KSD multiband baseline and derives labeled,
normalized spectral and represented-operator training quadratics inside the experiment.
The owner-integration slice delegates unit-free complex affine-residual construction while
retaining KSD's direct verification formulas.
The experiment owns:

- energy-shift and splitting-scale coordinate meaning;
- the finite ordered alignment-angle family;
- compatible and separated threshold cases;
- the prospective common witness;
- full-ellipsoid support containment in the experiment rectangle;
- the splitting-axis lower-bound certificate;
- separation resolution and bounded dispositions; and
- independent reconstruction of decisive geometry.

The exact dependency
`projectkoios-optimization@f6bdecc418e46240087d1dfb1c22dac396cdc455` owns the
following Optimization capabilities. The advance from the earlier development pin is a
qualified typing refactor; the consumed public contracts are unchanged:

- dense complex-observation affine-residual construction over real coordinates;
- positive-definite completed-square validation and evaluation;
- exact two-dimensional closed-rectangle minimization;
- full-ellipsoid support points; and
- inclusive ordered finite-family filtering and first-exact-minimum selection.

The experiment does not add a generic solver or a reusable box-clipped-sublevel-set
distance algorithm. Support results acquire certificate meaning only after KSD checks
the declared rectangle premise.

## Parent and verification boundary

The experiment composes `Periodic1DMultibandAlignmentCalculator` as an upstream KSD
capability; it does not import the historical constrained-admissible-set producer. The
parent Hamiltonian, rank-two retained-space controls, energy scale, complex feature
construction, loss normalization, and angle-resolved quadratic labels remain KSD-owned.
The Optimization owner receives deterministic C-order flattened complex feature rows,
negated offsets as targets, raw positive objective weights, and unit-free bounds. The
uniform affine-residual weight is
`1 / (N * rank * loss_energy_scale**2)`; it is not pre-square-rooted. KSD maps
`owner_absolute_tolerance` to the owner's absolute tolerance with zero relative
component and wraps the returned completed-square state with KSD labels.

`ConstrainedAdmissibleSetsExperimentVerifier` does not call the producer Action or
Optimization solvers. It invokes M2's independent verifier for the composed baseline,
then separately reconstructs complex-feature quadratics, completed-square values, the
clipped center and four conditional edge candidates, full-ellipsoid support by a separate
linear solve, ordered finite choices, point roles, bounds, and dispositions. It retains
separate dimensionless and parent-energy defect channels so unit changes cannot alter an
untyped aggregate.

Tests use compact unitless and physical-energy rank-two parents. Their deterministic
agreement establishes
software behavior only. It does not establish scientific validation, uncertainty
calibration, parent-model adequacy, or new retained evidence.

## Remaining migration before `.v1`

1. Restore separate training and evaluation roles plus candidate-locality diagnostics
   without importing the historical M3 producer.
2. Add strict experiment-local input/result schemas and an independent evidence
   verifier.
3. Review and freeze controls, dependency and adapter identities, interpretation, and
   evidence policy before assigning an immutable experiment-version ID.
4. Execute and retain a run only after explicit authorization.

The composed multiband baseline's experiment-versus-reusable boundary has now been
reviewed in the separate
[M2 numerical owner-boundary inventory](periodic/periodic1d/multiband_alignment/owner-boundary.md).
That review recommends no further M3 extraction and gates any later alignment move on a
rank-deficient Procrustes decision. It is a separate capability migration and does not
require this experiment to import a provisional owner API.

Until the remaining steps close, this directory is an owner-integrated development
slice, not a replacement retained experiment and not publication evidence.
