# M2 testing and evidence

## Direct test owner

`python/tests/software_verification/ksdft2effmass/periodic1d/test__Periodic1DMultibandAlignmentCalculator.py`

## Claim-to-test map

| Claim | Pytest node suffix | Oracle or mutation |
|---|---|---|
| Pointwise and global alignment are distinct channels | `test_execution__m2__separates_pointwise_and_global_alignment` | Frame/projector/operator/locality comparisons |
| Independent reconstruction passes | `test_verification__m2__independent_reconstruction_passes` | Rebuilt finite protocol |
| Schema and bytes are deterministic | `test_serialization__m2__is_deterministic_and_distinct` | Exact schema and bytes |
| Fresh execution is binary64 deterministic | `test_execution__m2__is_binary64_deterministic` | Byte identity |
| Alignment tampering is detected | `test_verification__m2__detects_tampered_alignment_diagnostic` | Mutated diagnostic |
| Hermiticity tampering is detected | `test_verification__m2__detects_tampered_hermiticity` | Mutated block defect |
| Standalone verifier avoids producers | `test_retained_verifier__m2__does_not_import_producer_modules` | Import inspection |
| Frozen control tampering is rejected | `test_retained_verifier__m2__rejects_contract_tampering` | Parameterized wire mutations |
| Generic definitions may contain identity attacks | `test_definition__m2__permits_identity_attack_for_generic_use` | Boundary construction |
| Results bind frame-transport thresholds | `test_construction__m2_result__binds_transport_threshold` | Cross-wired construction failure |
| Boolean mesh extents are rejected | `test_definition__m2__rejects_boolean_mesh_extent` | `bool` mutation |
| Definitions are immutable | `test_mutation__m2_definition__raises_frozen_instance_error` | Dataclass mutation attempt |

All nodes belong to `TestPeriodic1DMultibandAlignmentCalculator`.

## Evidence interpretation

The tests and retained verifier establish bounded software and numerical consistency.
The external gap, overlap, projector, operator, and locality diagnostics are finite
synthetic observations. They do not validate a material, a general gauge optimizer, or
a continuum limit.

## Documentation amendment

The retained source manifest correlates with all 24 listed paths at identified commit
`2e010d9f`. Documentation amendment 2 seals current source bytes after docstring
hardening in a separate sidecar without rewriting or substituting for that historical
execution-source record.

## Common dependencies and residual risk

Producer and verifier share NumPy/SciPy linear algebra, binary64 arithmetic, frame and
unit conventions, and portions of the lower-level domain stack. Adversarial mutations
show fail-closed behavior for named contracts; they cannot enumerate every possible
semantic error.
