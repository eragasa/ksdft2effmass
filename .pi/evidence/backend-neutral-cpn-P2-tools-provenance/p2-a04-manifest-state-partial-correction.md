# P2-A04 ManifestState partial correction

Status: **deterministic validation passed; P2-A04 remains open**

Starting revision: `26d9e007beab4681fbba6523fd392aea66c59103`.

The completed human file-level audit found that `test__ManifestState.py`
incorrectly described the enum as artifact-owned, used an `artifact` surface,
and covered only names and values. The module now has explicit class ownership
with sole SUT `ManifestState` and complete version-1 enum evidence. Production
`records.py` remained unchanged.

## Evidence inventory

The module owns exactly six test functions:

- `test_field__wire_vocabulary__has_exact_order_names_values_and_count`;
- `test_method__call__constructs_each_state_from_wire_value`;
- `test_method__getitem__returns_each_state_from_declared_name`;
- `test_method__call__rejects_unknown_wire_value`;
- `test_method__call__rejects_wrong_semantic_type`; and
- `test_method__getitem__rejects_unknown_member_name`.

These functions collect ten cases. Historical `SV-PROV-075` remains on the
expanded vocabulary owner. New IDs `SV-PROV-368` through `SV-PROV-372` own
successful wire-value construction, successful declared-name lookup, unknown
wire-value rejection, wrong semantic value-type rejection, and unknown
member-name rejection respectively.

The one historical node maps one-to-one from
`test_artifact__enum_values__matches_exact_manifest_lifecycle_vocabulary` to
`test_field__wire_vocabulary__has_exact_order_names_values_and_count`. The five
new owners have no historical predecessors.

## Structural validator

Exact command:

```bash
python harness/pi/validation/validate_python_test_evidence.py \
  python/tests/software_verification/ksdft2effmass/provenance/test__ManifestState.py \
  --ownership .pi/evidence/backend-neutral-cpn-P2-tools-provenance/p2-a04-manifest-state-test-evidence-ownership.json \
  --migration-map .pi/evidence/backend-neutral-cpn-P2-tools-provenance/p2-a04-manifest-state-test-evidence-node-migration.json
```

Exact structured result:

```json
{"claim_boundary":["oracle independence","mathematical correctness","property/surface correctness","test cohesion","tolerance adequacy","scientific validity","uncertainty quantification","human acceptance"],"counts":{"artifact_owned_modules":0,"class_owned_modules":1,"evidence_class_modules":{"numerical_verification":0,"scientific_validation":0,"software_verification":1,"uncertainty_quantification":0},"findings_by_code":{},"helper_functions":0,"modules":1,"parameterized_functions":2,"static_collected_parameter_cases":6,"test_functions":6,"unique_evidence_owners":6},"findings":[],"paths":["python/tests/software_verification/ksdft2effmass/provenance/test__ManifestState.py"],"schema_version":1,"status":"PASS"}
```

Structural PASS does not replace the completed human audit and does not establish
semantic, numerical, or scientific correctness.

## Deterministic results

- exact collection and execution: ten collected and ten passed;
- enum-owned diagnostic: no missing enum-class statements or branches; enum
  members execute at declaration time and the class has no executable method
  body;
- Ruff format and lint: PASS;
- mypy over `records.py` and the module: PASS;
- focused public API regression: three passed;
- focused serializer enum-type regression: one passed;
- unique evidence-ID check: PASS for `SV-PROV-075` and `SV-PROV-368`--`372`;
- production-source Git nonmutation, protected prior-test nonmutation,
  `git diff --check`, and unrelated-work preservation: PASS.

P2-A04 remains `pending_read_only_audit`. The next human-audit target is the
`LineageKind` evidence surface, which was not created or modified. P2 remains
open and unaccepted.
