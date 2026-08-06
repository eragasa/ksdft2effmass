# P2-A03 ExternalExecutionResult partial correction

Status: **deterministic validation passed; P2-A03 remains open**

Starting revision: `0d1189b73227ddccfb93fbf479dd02bf427901cc`.

The completed human file-level audit authorized correction of
`test__ExternalExecutionResult.py` and relocation of the internal
`ExternalExecutionOutcome` assertion to one artifact-owned module. Production
`external_execution.py` was inspected read-only and remained unchanged.
`ExternalExecutionFailure` and its test module were not modified.

## Ownership and evidence inventory

The accepted artifact-owned filename convention is descriptive lowercase snake
case, so the requested explicit filename
`test__external_execution_outcome_type_alias.py` is convention-compliant.
Ownership is exactly one class-owned module with sole SUT
`ExternalExecutionResult` and one artifact-owned module with primary artifact
`ksdft2effmass.provenance.external_execution.ExternalExecutionOutcome`.

The two modules contain 29 evidence-owner functions, 12 parameterized
functions, 80 static parameter cases, 97 collected cases, and one visible helper:
`make_external_execution_result`. The helper calls the public constructor with
valid baseline state and explicit overrides; it owns no ID, assertions,
normalization, hidden oracle, or I/O. The class-owned module contains 28 evidence
owners; the artifact-owned module contains one.

Historical IDs `SV-PROV-040`, `SV-PROV-041`, and `SV-PROV-222` through
`SV-PROV-229` are preserved. The 15 historical collected nodes map one-to-one to
14 class-owned successor nodes and the moved artifact-owned alias node. The
remaining 82 collected cases are newly added.

New IDs `SV-PROV-314` through `SV-PROV-332` were required for independently
owned requirements:

- `314`: accepted identifier ordinary/minimum/maximum partitions;
- `315`--`320`: independently split identifier empty, grammar, leading,
  surrogate, NFC, and length rejection;
- `321`--`322`: accepted exact status state and unrelated integer rejection;
- `323`--`330`: independently split output member type, nonempty, grammar,
  leading, Unicode, length, ordering, and uniqueness evidence;
- `331`: identical complete-state equality; and
- `332`: unrelated-object equality.

Historical IDs remain on their closest semantic successors: `SV-PROV-224` owns
identifier wrong-type cases; `SV-PROV-223` owns the status string lookalike;
`SV-PROV-222` owns tuple container type; `SV-PROV-228` owns valid one-field
equality variation; and `SV-PROV-226` owns the moved alias artifact.

## Structural validator

Exact command:

```bash
python harness/pi/validation/validate_python_test_evidence.py \
  python/tests/software_verification/ksdft2effmass/provenance/test__ExternalExecutionResult.py \
  python/tests/software_verification/ksdft2effmass/provenance/test__external_execution_outcome_type_alias.py \
  --ownership .pi/evidence/backend-neutral-cpn-P2-tools-provenance/p2-a03-external-execution-result-test-evidence-ownership.json \
  --migration-map .pi/evidence/backend-neutral-cpn-P2-tools-provenance/p2-a03-external-execution-result-test-evidence-node-migration.json
```

Exact structured result:

```json
{"claim_boundary":["oracle independence","mathematical correctness","property/surface correctness","test cohesion","tolerance adequacy","scientific validity","uncertainty quantification","human acceptance"],"counts":{"artifact_owned_modules":1,"class_owned_modules":1,"evidence_class_modules":{"numerical_verification":0,"scientific_validation":0,"software_verification":2,"uncertainty_quantification":0},"findings_by_code":{},"helper_functions":1,"modules":2,"parameterized_functions":12,"static_collected_parameter_cases":80,"test_functions":29,"unique_evidence_owners":29},"findings":[],"paths":["python/tests/software_verification/ksdft2effmass/provenance/test__ExternalExecutionResult.py","python/tests/software_verification/ksdft2effmass/provenance/test__external_execution_outcome_type_alias.py"],"schema_version":1,"status":"PASS"}
```

Structural PASS does not establish semantic correctness, scientific validity,
provenance truth, or human acceptance.

## Deterministic results

- exact collection and execution: 97 collected and 97 passed;
- result-class diagnostic coverage: 100% statement coverage (44/44) and 100%
  branch coverage (42/42) for `ExternalExecutionResult` at source lines 265--361;
  aggregate containing-module coverage was 38%, with unrelated request/failure
  records intentionally absent;
- Ruff format and lint: PASS for exactly the two authorized modules;
- focused mypy over production and the two authorized modules: PASS;
- focused result schema/fixture/runtime/canonical round-trip regression: six
  passed, with unrelated cases deselected;
- focused package public API and internal-alias nonexport regression: four
  passed;
- migration: 15 unique historical nodes to 15 unique current successors;
- production-source Git nonmutation, `git diff --check`, and unrelated-work
  preservation: PASS.

The earlier three enum and request corrections remain durable. P2-A03 remains
`pending_read_only_audit`; `ExternalExecutionFailure` is the next human-audit
target and remains untouched. No general independent review, successor,
protected execution, publication, or release work began.
