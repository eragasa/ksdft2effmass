# Stage C execution-free implementation review

## Review boundary

This review covers `stage-c-design.json`, `stage-c-protocol.md`,
`stage-c-preflight.md`, `run_stage_c.py`, `verify_stage_c.py`,
`stage-c-toy-result.schema.json`, and the maintained Stage C software-verification
module. It reviews authored-toy software behavior only. It does not review or
authorize accepted-parent execution, Stage D or E, material transfer, DFT,
Wannier90, scientific validation, uncertainty quantification, publication, or
release.

## Finding disposition

| Finding | Disposition | Resolution |
|---|---|---|
| Directional defects could be incorrectly tested as $D_4$-invariant rather than as an oriented covariant inventory. | `FIXED` | The design and implementation transform both the origin and bond displacement and compare all eight Gamma-point orientations. |
| Route agreement could erase the distinction between gauge equivalence and an independent estimate. | `FIXED` | Route A and Route B are constructed independently, and the explicit bridge remains a separate equivalence diagnostic with no voting. |
| Evaluating both route orders in one process would not expose process-global schedule state. | `FIXED` | A-then-B and B-then-A run through separate one-worker spawn executors; the parent rejects reused or parent process identities while serializing only deterministic fresh-process status. |
| A favorable larger model could be selected after a smaller class already passes. | `FIXED` | All five classes are retained in frozen order, and selection stops logically at the first passing class without deleting later diagnostic fits. |
| Complex twist-gauge matrices could silently permit complex fit coefficients. | `FIXED` | Fits use real coefficients over stacked real and imaginary entries, preserving the declared real defect amplitudes. |
| Locality could be inferred only from a total norm. | `FIXED` | Every fit retains maximum-entry, Frobenius, and periodic-Chebyshev shell residuals with an exact radius-two exterior criterion. |
| The verifier could reproduce runner behavior by importing the runner. | `FIXED` | `verify_stage_c.py` imports no runner code and independently reconstructs matrix bytes, bridge values, analytic fit residuals, schedules, and adverse controls. |
| A toy design mutation could be mistaken for accepted-parent execution authority. | `FIXED` | The deserializer rejects any design whose execution-authority flag is not exactly false; maintained tests exercise the rejection. |
| The frozen toy hierarchy includes one diagonal radius-two basis direction rather than every possible radius-two nonlocal term. | `ACCEPTED_LIMITATION` | The scope is explicitly an authored software discriminator for the two frozen plants, not a complete physical nonlocal basis or material model. |

## Technical review outcome

`NO_BLOCKING_FINDINGS`

The execution-free package retains 16 route records, 8 bridge records, 16
oriented-symmetry records, and 80 model-fit records. Independent reconstruction
of the authored toy reports a maximum difference of approximately
$1.39\times10^{-17}E_G$. The wrong-isotropic, wrong-directional,
omitted-reverse, and omitted-bridge controls remain discriminating. These are
software-verification observations from synthetic toy data, not accepted-parent
Stage C results.

## Operator input

No additional input is required to retain this execution-free implementation.
HC10 human-accepts this exact execution-free package and authorizes managed
closeout only. A future accepted-parent Stage C design or execution requires a
separate human decision. Neither `NO_BLOCKING_FINDINGS` nor HC10 provides
execution authority or human acceptance of any future calculated result.
