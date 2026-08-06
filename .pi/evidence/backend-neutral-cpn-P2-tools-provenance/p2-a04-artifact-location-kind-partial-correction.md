# P2-A04 ArtifactLocationKind partial correction

Status: **deterministic validation passed; P2-A04 remains open**

Starting revision: `f9831a7c97431a7419fc708fed5eaa56f54a130e`.

The completed human file-level audit found that `ArtifactLocationKind` lacked a
dedicated class-owned module and that historical evidence `SV-PROV-011` was
misowned by `test__ArtifactLocation.py`. The evidence owner moved to
`test__ArtifactLocationKind.py`; it was not duplicated. Production `records.py`
remained unchanged.

## Evidence inventory

The new module owns exactly six test functions:

- `test_field__wire_vocabulary__has_exact_order_names_values_and_count`;
- `test_method__call__constructs_each_kind_from_wire_value`;
- `test_method__getitem__returns_each_kind_from_declared_name`;
- `test_method__call__rejects_unknown_wire_value`;
- `test_method__call__rejects_wrong_semantic_type`; and
- `test_method__getitem__rejects_unknown_member_name`.

These functions collect eight cases. `SV-PROV-011` remains on the moved exact
vocabulary owner. New IDs `SV-PROV-363` through `SV-PROV-367` own successful
wire-value construction, successful declared-name lookup, unknown wire-value
rejection, wrong semantic value-type rejection, and unknown declared-name
rejection respectively.

The one historical node maps one-to-one from
`test__ArtifactLocation.py::test_field__location_kind_vocabulary__is_exact` to
`test__ArtifactLocationKind.py::test_field__wire_vocabulary__has_exact_order_names_values_and_count`.
The five new owners have no historical predecessors.

## Structural validator

Exact command:

```bash
python harness/pi/validation/validate_python_test_evidence.py \
  python/tests/software_verification/ksdft2effmass/provenance/test__ArtifactLocationKind.py \
  python/tests/software_verification/ksdft2effmass/provenance/test__ArtifactLocation.py \
  --ownership .pi/evidence/backend-neutral-cpn-P2-tools-provenance/p2-a04-artifact-location-kind-test-evidence-ownership.json \
  --migration-map .pi/evidence/backend-neutral-cpn-P2-tools-provenance/p2-a04-artifact-location-kind-test-evidence-node-migration.json
```

Exact structured result:

```json
{"claim_boundary":["oracle independence","mathematical correctness","property/surface correctness","test cohesion","tolerance adequacy","scientific validity","uncertainty quantification","human acceptance"],"counts":{"artifact_owned_modules":0,"class_owned_modules":2,"evidence_class_modules":{"numerical_verification":0,"scientific_validation":0,"software_verification":2,"uncertainty_quantification":0},"findings_by_code":{},"helper_functions":0,"modules":2,"parameterized_functions":7,"static_collected_parameter_cases":38,"test_functions":19,"unique_evidence_owners":19},"findings":[],"paths":["python/tests/software_verification/ksdft2effmass/provenance/test__ArtifactLocationKind.py","python/tests/software_verification/ksdft2effmass/provenance/test__ArtifactLocation.py"],"schema_version":1,"status":"PASS"}
```

Structural PASS does not establish semantic, numerical, or scientific
correctness.

## Deterministic results

- exact two-module collection and execution: 50 collected and 50 passed;
- enum-owned tests: eight passed; the enum class has no executable statement or
  branch body beyond declaration-time members, and coverage reports no missing
  enum-class statements or branches;
- Ruff format and lint over both modules: PASS;
- mypy over `records.py` and both modules: PASS;
- focused public API regression: three passed;
- focused serializer enum-type regression: one passed;
- unique evidence-ID check: PASS for `SV-PROV-011` and `SV-PROV-363`--`367`;
- production-source Git nonmutation, untouched ManifestState/LineageKind tests,
  `git diff --check`, and unrelated-work preservation: PASS.

P2-A04 remains `pending_read_only_audit`. The next human-audit target is
`test__ManifestState.py`; neither ManifestState nor LineageKind work began. P2
remains open and unaccepted.
