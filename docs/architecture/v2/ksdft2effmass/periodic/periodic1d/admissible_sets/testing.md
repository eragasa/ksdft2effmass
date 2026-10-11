# M3 testing and evidence

## Direct test owners

- `python/tests/software_verification/ksdft2effmass/periodic1d/test__Periodic1DConstrainedAdmissibleSetCalculator.py`
- `python/tests/software_verification/ksdft2effmass/periodic1d/test__Periodic1DConstrainedAdmissibleSetThresholdSensitivity.py`

## Confirmatory claim-to-test map

| Claim | Test suffix | Oracle or mutation |
|---|---|---|
| M3 composes exact rank-two M2 | `test_construction__composes_rank_two_m2_definition` | Exact object/type assertions |
| Non-rank-two composition fails | `test_construction__composed_baseline_rejects_non_rank_two` | Rank mutation |
| Compatible and separated results are retained | `test_execution__retains_compatible_and_certified_separated_cases` | Witness and lower-bound assertions |
| Independent reconstruction passes | `test_verification__independent_reconstruction_passes` | Rebuilt bounded rectangle and finite angle protocol |
| Withheld diagnostic tampering is detected | `test_verification__detects_tampered_withheld_diagnostic` | Mutated evaluation loss |
| Evaluation-role tampering is detected | `test_verification__detects_tampered_evaluation_role` | Wrong role mutation, defect `1.0` |
| Quadratic/result miscorrelation is rejected | `test_result__rejects_tampered_training_quadratic_correlation` | Shifted quadratic |
| Locality inventory miscorrelation is rejected | `test_result__rejects_tampered_locality_inventory` | Altered range summary |
| Schema bytes are deterministic | `test_serialization__is_deterministic_and_distinct` | Exact schema/byte comparison |
| Boolean thresholds/parameters/matrix entries fail | three `rejects_boolean` tests | Boolean impostors |
| Editable configuration reproduces retained input | `test_configuration__materializes_the_retained_input` | Byte-identical generation |
| Standalone verifier avoids producer imports | `test_retained_verifier__does_not_import_producer_modules` | Import inspection |
| Wire and tolerance tampering fails closed | `test_retained_verifier__rejects_contract_tampering` | Parameterized document mutations |

All suffixes above belong to `TestPeriodic1DConstrainedAdmissibleSetCalculator`.

## Post-hoc sensitivity map

| Claim | Full pytest node | Oracle or mutation |
|---|---|---|
| Consumed `result.json` is the exact manifest-bound source | `TestPeriodic1DConstrainedAdmissibleSetThresholdSensitivity::test_retained_verifier__rejects_source_manifest_miscorrelation` | Altered manifest entry |
| Decisive quadratic premises are independently enforced | `...::test_retained_verifier__rejects_invalid_quadratic_premise` | Shifted center, asymmetric/cross-term, and nonpositive-curvature mutations |

## Evidence interpretation

The confirmatory package was frozen before evaluation. Later corrections are recorded as
amendments and sealed manifest boundaries. Documentation amendment 10 binds current M3
and composed M2 source bytes in a separate sidecar, preserving the retained package
manifest digest consumed by the sensitivity package. It changes no controls, numerical
result, certificate, or disposition. The sensitivity package is explicitly post hoc and
cannot retrospectively strengthen the prospective status of M3.

## Common dependencies and residual risk

Library and standalone verifiers share NumPy/SciPy, binary64 arithmetic, eigensolvers,
and conventions. SHA-256 binds bytes but not chronology or semantic correctness.
Passing tests establishes bounded software/numerical behavior only.
