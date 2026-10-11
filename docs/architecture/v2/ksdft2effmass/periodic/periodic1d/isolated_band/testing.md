# M1 testing and evidence

## Direct test owner

`python/tests/software_verification/ksdft2effmass/periodic1d/test__Periodic1DIsolatedBandCalculator.py`

## Claim-to-test map

| Claim | Pytest node | Oracle or mutation |
|---|---|---|
| Parent, training, and evaluation roles remain separate | `TestPeriodic1DIsolatedBandCalculator::test_execute__keeps_parent_training_and_withheld_channels_separate` | Exact coordinate and object-identity assertions |
| Retained reconstruction avoids producer imports | `...::test_retained_verifier__does_not_import_the_producer_package` | Static import inspection and subprocess execution |
| Library verification reconstructs all channels | `...::test_verifier__independently_reconstructs_calculation_channels` | Recomputed spectra, Fourier blocks, and diagnostics |
| Schema identity and bytes are deterministic | `...::test_serializer__uses_distinct_deterministic_schema_v1` | Exact schema and byte comparison |
| Fresh calculations are binary64 deterministic | `...::test_execute__is_binary64_deterministic_across_fresh_calculations` | Exact serialized-byte equality |
| Tampered retained scalar is rejected | `...::test_verifier__rejects_a_tampered_convergence_observation` | Mutated convergence observation |
| Parseval tolerance has squared-energy dimensions | `...::test_definition__requires_squared_energy_parseval_tolerance` | Wrong-unit construction failure |
| Boolean numeric controls are rejected | `...::test_definition__rejects_boolean_numeric_control` | `bool` passed at integer boundary |

The `...` prefix above denotes
`TestPeriodic1DIsolatedBandCalculator` in the direct test module.

## Evidence classes

Software tests establish strict construction, correlation, determinism, and tamper
response. Independent reconstruction provides bounded numerical verification for the
frozen finite protocol. Neither establishes material validation, uncertainty
quantification, or acceptance.

## Retained evidence

The retained M1 package includes canonical input, freeze record, result, verifier
output, figure data, report, software record, source manifest, and artifact manifest.
Documentation amendment 1 records that the historical source manifest does not
correlate with identified commit `ee89d347`; two listed digests differ and one listed
path is absent. The cause is not established. A separate current-source sidecar is
sealed without rewriting the retained manifests and is not represented as execution
source. SHA-256 detects byte changes relative to recorded digests; it does not prove
chronology or semantic validity by itself.

## Known common dependencies

Producer and verifier share Python, NumPy/SciPy, eigensolvers, floating-point behavior,
unit conventions, and parts of the lower-level implementation. The standalone route is
independent of producer Actions, not an independent physical oracle.
