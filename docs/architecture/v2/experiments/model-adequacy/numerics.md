# Model-adequacy numerical method

## Quadratic construction

When a channel residual is affine in real candidate coordinates, the sampled normalized
squared loss is assembled as a quadratic and independently checked against direct
residual evaluation.

- Form the declared design rows in deterministic order.
- Apply raw positive objective multipliers exactly once.
- Preserve the declared energy scale and nondimensionalization.
- Complete the square only after validating symmetry and rank.
- Retain the center, quadratic matrix, minimum squared loss, and construction diagnostics.
- Compare quadratic evaluation with direct residual sums at bounded test points.

## Feasibility calculation

Each candidate class is evaluated on its active affine slice of the common maximal
parameter space.

- Reconstruct inactive zero constraints.
- Minimize each channel over the declared domain.
- Classify a channel as empty only from a verified minimum above threshold.
- Search for a common candidate without changing thresholds or sample roles.
- Re-evaluate every retained candidate directly before assigning evidence meaning.

## Distance bounds

Nonempty channel sets receive constructive upper bounds and conservative lower bounds
through separate calculations.

- Compute an upper bound from one verified feasible pair.
- Select and retain any proposed separating covector.
- Reconstruct channel support bounds in that direction.
- Normalize the directional gap by the dual of the declared metric.
- Apply outward rounding or exact enclosure before comparison with resolution.
- Keep the result unresolved when no lower bound exceeds resolution.

## Domain containment

Unconstrained ellipsoid formulas are used only when their relationship to the actual
domain is proved for the retained case.

- Reconstruct the full quadratic sublevel ellipsoid.
- Evaluate every coordinate support extremum.
- Verify containment in the box or declared feasible domain.
- Use full-ellipsoid support only after containment succeeds.
- Report a failed containment premise rather than silently substituting a different problem.

## Independent reconstruction

The verifier follows formulas rather than producer control flow.

- Rebuild features, weights, targets, and quadratics from retained inputs.
- Rebuild nonemptiness and candidate membership.
- Rebuild metric norms and support bounds.
- Rebuild the strict comparison with resolution.
- Check evidence and disposition correlation after numerical reconstruction.

## References and provenance

The common steps are project-derived compositions of elementary least-squares and convex
support identities; each child records the exact owner or literature source for any
specialized algorithm.

- [Shared admissible-set evidence semantics](../../ksdft2effmass/analysis/model_adequacy/admissible-set-evidence-semantics.md).
- The periodic-1D maintained experiment records the reviewed Optimization owner revision for complex affine residual quadratics.
- The periodic-2D and periodic-3D children must record exact numerical-owner revisions before implementation.
- No external source is claimed here for a generic arbitrary-lattice solver or certificate framework.
