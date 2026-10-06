# Conditioning-diagnostic expansion

## Status

**Safe to defer.** Existing least-squares fit results already retain the conditioning
information required by their current in-process contract. This record concerns wider
persistence and consistency, not a current scientific-validation claim or a reason to
expand every verifier.

## Current behavior

[`BlockHoppingLeastSquaresFitResult1D`](../../../python/src/ksdft2effmass/analysis/hopping_fits.py)
retains:

- weighted-design rank;
- weighted-design two-norm condition number when the design is full rank; and
- an explicit identifiability disposition.

The condition number is computed from the extreme singular values of the weighted
design matrix. Rank-deficient fits retain `design_condition_number = None` and
`is_identified = False`. The fit result also retains training residuals. These values
remain numerical diagnostics; they are not model-adequacy, scientific-validation, or
uncertainty-quantification results.

The periodic-1D replay sidecar currently retains fitted coefficients but does not
persist the fit rank, condition number, or resolved comparison allowance for every
range. The scientific adoption reconstructs a typed least-squares fit result in
process, so the current software result still exposes those diagnostics without
requiring the retained-result verifier to reimplement conditioning analysis.

## Deferred expansion

When a persisted or cross-calculation conditioning contract becomes necessary:

1. Retain, for each fitted range, the coefficient count, design rank, weighted-design
   two-norm condition number, and identifiability disposition.
2. Identify the exact conditioned object, weighting, scaling, norm, scalar dtype, and
   whether the value is calculated exactly from retained singular values or estimated.
3. If `absolute_tolerance=None` selects an automatic numerical comparison allowance,
   retain the resolved allowance, reference scale, operation dimension, and named
   calculation rule used for that route.
4. Keep coordinate, reconstruction-energy, and coefficient-route allowances distinct,
   even when one public override is permitted by a campaign request.
5. Represent rank deficiency or unavailable conditioning explicitly. Do not enlarge a
   tolerance until an unidentified fit passes.
6. Add focused software tests for the calculation and serialization rules. Do not add
   independent conditioning reconstruction to every retained-result verifier unless
   conditioning becomes part of that verifier's claim-bearing acceptance contract.

## Scope boundary

Do not add a universal condition-number field to every calculation. Different
operations require different stability evidence:

- least-squares routes use design rank, singular values, condition number, and
  residuals;
- linear solves use residual or backward error and, where relevant, a condition
  estimate;
- eigenvector and retained-subspace calculations use spectral separation, eigenpair
  residuals, or projector defects rather than an indiscriminate matrix condition
  number;
- complete normalized Fourier transforms use their known transform structure and
  reconstruction residuals; and
- direct evaluation, truncation, hashing, and serialization do not acquire a condition
  number merely for uniformity.

Conditioning remains separate from parent-model error, numerical discretization error,
model-reduction error, scientific validation, and uncertainty quantification, as
required by the [periodic architecture](../../architecture/v2/ksdft2effmass/periodic/index.md).
No registry, factory, discovery mechanism, generic verifier hierarchy, or universal
conditioning container is proposed.

## Revisit conditions

Revisit this debt when any of the following occurs:

- a persisted result uses conditioning to calculate an acceptance tolerance;
- fitted replay artifacts must be compared across numerical-library environments;
- a new fit, inverse, alignment, or sensitivity-amplifying route lacks an
  operation-appropriate diagnostic; or
- conditioning becomes part of a claim-bearing verifier contract.

## Exclusions

This deferral does not absorb or postpone the periodic crosswalk program.
`PERIODIC-XWALK-023` completed the untruncated-parent versus finite plane-wave
representation separation and the replay-adoption tolerance correction. The broader
crosswalk remains active until every row has a terminal implemented disposition and
passes its applicable preservation and verification gates.
