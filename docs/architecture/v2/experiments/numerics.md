# Experiment numerical documentation

## Local controls

Every concrete experiment owns the numerical choices that affect its outcome.

- Discretization and coordinate ordering.
- Feature construction and flattening order.
- Units and nondimensionalization.
- Weights and normalization.
- Parameter domain and active coordinates.
- Thresholds, metric, and resolution.
- Rank, conditioning, tolerance, and overflow policy.
- Certificate premises and conservative arithmetic.

## Numeric input policy

Numeric contracts remain explicit and reject silent coercion.

- Booleans are not accepted as numeric scalars.
- Numeric strings are rejected unless a schema explicitly permits them.
- Nonfinite values are rejected.
- Positive objective weights retain their declared meaning across adapters.
- Complex residual rows use a deterministic declared order.
- Owner diagnostics are interpreted only in the coordinate system they describe.

## Evidence policy

Constructive evidence and lower-bound evidence have different meanings.

- A feasible point may establish membership.
- A feasible pair may establish an upper distance bound.
- A common point may establish compatibility.
- A local optimum cannot establish positive global separation.
- A separation claim requires a conservative lower bound above declared resolution.
- Independent verification reconstructs decisive formulas without calling the producer.

## Extraction boundary

Shared equations do not automatically justify shared software.

- This root defines no generic solver facade.
- This root defines no common result or certificate hierarchy.
- Experiments consume reviewed numerical-owner contracts directly when those unit-free boundaries already fit; pass-through facades are not required.
- One concrete experiment need and a clear semantic owner are sufficient to extract the smallest complete reusable contract; a duplicate implementation or second consumer is not required.
- Later consumers may justify broadening that contract, but they are not a prerequisite for correct initial ownership.
