# Stage C execution-free implementation preflight

## Authorization

- [x] HC09 records the verbatim response `recommendation authorized`.
- [x] The normalized decision is
  `AUTHORIZE_EXECUTION_FREE_STAGE_C_DESIGN_AND_IMPLEMENTATION`.
- [x] No accepted-parent Stage C execution is authorized.
- [x] Stage B reruns and Stages D--E remain unauthorized.

## Inputs and represented meaning

- [x] `stage-c-design.json` fixes the $8\times8$ scalar toy space, ordering,
  units, energy reference, twists, routes, bridge, plants, model order, and
  tolerances.
- [x] All coefficients are authored synthetic test data.
- [x] The runner accepts only the design and a new toy-output path.
- [x] Neither runner nor verifier reads the accepted periodic parent.
- [x] Directional covariance is distinguished from $D_4$ invariance.
- [x] Gauge, schedule, model-reduction, and locality diagnostics remain
  separate.

## Implementation

- [x] Immutable records own bond, operation, and control data.
- [x] Matrix construction, fitting, serialization, and verification have named
  ActionObject owners.
- [x] Route A and Route B are independently constructed from compact bond terms.
- [x] The explicit bridge is not used as a third estimate or vote.
- [x] Both route orders run in fresh spawned processes and are compared exactly.
- [x] The first passing model class is selected in frozen order.
- [x] Wrong-class, omitted-reverse, and omitted-bridge adverse controls are
  retained.
- [x] The independent verifier does not import the runner.
- [x] The result schema is closed Draft 2020-12.

## Evidence boundary

- [x] HC10 human-accepts this exact execution-free package and authorizes
  managed closeout only.
- [x] Maintained tests use pytest scratch paths and retain no toy result.
- [x] Toy behavior is labeled software verification.
- [x] No numerical result from an accepted parent is claimed.
- [x] No material validation, scientific validation, uncertainty
  quantification, publication, or release is claimed.
- [x] Any future accepted-parent Stage C calculation requires a separate exact
  design review and human checkpoint.
