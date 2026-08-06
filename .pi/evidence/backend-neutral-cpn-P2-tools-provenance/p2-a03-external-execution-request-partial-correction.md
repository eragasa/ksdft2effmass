# P2-A03 ExternalExecutionRequest partial correction

Status: **deterministic validation passed; P2-A03 remains open**

Starting revision: `6cb9bb4774bcd8c003efff0ca87095b67e3e92b1`.

The completed human file-level audit authorized correction of only
`test__ExternalExecutionRequest.py`. Production
`external_execution.py` was inspected read-only and is required to remain
unchanged by the final Git boundary check.

## Evidence inventory

The module contains 35 evidence-owner functions, 23 parameterized functions,
134 static parameter cases, 146 collected cases, and one visible helper:
`make_external_execution_request`. The helper calls the public constructor with
valid baseline state and explicit overrides; it owns no ID, assertions,
normalization, hidden oracle, or I/O.

Historical IDs `SV-PROV-037`, `SV-PROV-038`, `SV-PROV-039`, `SV-PROV-078`, and
`SV-PROV-217` through `SV-PROV-221` are preserved. The 16 historical collected
nodes map one-to-one to closest current successors. The remaining 130 collected
cases are new.

New IDs `SV-PROV-288` through `SV-PROV-313` were necessary for independently
owned requirements:

- `288`--`294`: required-identifier accepted bounds and split value partitions;
- `295`--`301`: retry-parent type and lexical partitions;
- `302`--`310`: tuple member, lexical, ordering, and uniqueness invariants;
- `311`: symmetric absent/present retry-parent equality;
- `312`: valid-state equality effects for both tuple fields; and
- `313`: unrelated-object equality behavior.

The evidence covers all eight required identifiers across ordinary/minimum/
maximum/type/empty/grammar/leading/surrogate/NFC/overlength partitions; all
optional retry-parent states plus direct self-reference; both tuple fields
across accepted, container, member, lexical, ordering, and uniqueness states;
all eleven frozen fields; every field in equality; exact stored values/types;
and the durable authorization/runtime boundary.

## Structural validator

Exact command:

```bash
python harness/pi/validation/validate_python_test_evidence.py \
  python/tests/software_verification/ksdft2effmass/provenance/test__ExternalExecutionRequest.py \
  --ownership .pi/evidence/backend-neutral-cpn-P2-tools-provenance/p2-a03-external-execution-request-test-evidence-ownership.json \
  --migration-map .pi/evidence/backend-neutral-cpn-P2-tools-provenance/p2-a03-external-execution-request-test-evidence-node-migration.json
```

Exact structured result:

```json
{"claim_boundary":["oracle independence","mathematical correctness","property/surface correctness","test cohesion","tolerance adequacy","scientific validity","uncertainty quantification","human acceptance"],"counts":{"artifact_owned_modules":0,"class_owned_modules":1,"evidence_class_modules":{"numerical_verification":0,"scientific_validation":0,"software_verification":1,"uncertainty_quantification":0},"findings_by_code":{},"helper_functions":1,"modules":1,"parameterized_functions":23,"static_collected_parameter_cases":134,"test_functions":35,"unique_evidence_owners":35},"findings":[],"paths":["python/tests/software_verification/ksdft2effmass/provenance/test__ExternalExecutionRequest.py"],"schema_version":1,"status":"PASS"}
```

Structural PASS does not establish semantic correctness, scientific validity,
provenance truth, or human acceptance.

## Deterministic results

- exact collection and execution: 146 collected and 146 passed;
- request-class diagnostic coverage: no missing statements or branches in the
  `ExternalExecutionRequest` class lines 126--261; aggregate containing-module
  coverage was 50%, with unrelated result/failure records intentionally absent;
- Ruff format and lint: PASS;
- focused mypy over production and corrected test: PASS;
- request fixture/schema/deserialization/canonical round-trip regression: four
  passed;
- public package API regression: three passed;
- migration: 16 unique old nodes to 16 unique current successors;
- `git diff --check` and unrelated-file preservation: PASS.

The three enum corrections remain durable and unchanged. The result and failure
record modules remain untouched and incomplete. The next human-audit target is
`test__ExternalExecutionResult.py`. P2-A03 remains `pending_read_only_audit`;
P2-HC06 remains pending and is not superseded.
