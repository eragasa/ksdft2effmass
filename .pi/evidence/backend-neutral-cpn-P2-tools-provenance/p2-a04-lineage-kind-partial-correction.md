# P2-A04 LineageKind partial correction

Status: **file-specific deterministic validation passed**

Starting revision: `9c7bdbe70a6d2cb794ecd96883f4146ec8f603a5`.

The completed human file-level audit found that `LineageKind` lacked a dedicated
class-owned module and that `SV-PROV-019` was misowned by
`test__LineageRelation.py`. The vocabulary owner moved to
`test__LineageKind.py` and was not duplicated. `SV-PROV-133` and its
`LineageRelation` constructor test remained byte-for-byte unchanged. Production
`records.py` remained unchanged.

## Evidence inventory

The new module owns exactly six test functions:

- `test_field__wire_vocabulary__has_exact_order_names_values_and_count`;
- `test_method__call__constructs_each_kind_from_wire_value`;
- `test_method__getitem__returns_each_kind_from_declared_name`;
- `test_method__call__rejects_unknown_wire_value`;
- `test_method__call__rejects_wrong_semantic_type`; and
- `test_method__getitem__rejects_unknown_member_name`.

The new module collects ten cases. Historical `SV-PROV-019` remains on the
expanded vocabulary owner. New IDs `SV-PROV-373` through `SV-PROV-377` own
successful wire-value construction, successful declared-name lookup, unknown
wire-value rejection, wrong semantic value-type rejection, and unknown
member-name rejection.

The one historical node maps one-to-one from
`test__LineageRelation.py::test_field__lineage_enum_values__match_version_one_vocabulary`
to
`test__LineageKind.py::test_field__wire_vocabulary__has_exact_order_names_values_and_count`.
The five new owners have no historical predecessors.

## Structural validator

Exact command:

```bash
python harness/pi/validation/validate_python_test_evidence.py \
  python/tests/software_verification/ksdft2effmass/provenance/test__LineageKind.py \
  python/tests/software_verification/ksdft2effmass/provenance/test__LineageRelation.py \
  --ownership .pi/evidence/backend-neutral-cpn-P2-tools-provenance/p2-a04-lineage-kind-test-evidence-ownership.json \
  --migration-map .pi/evidence/backend-neutral-cpn-P2-tools-provenance/p2-a04-lineage-kind-test-evidence-node-migration.json
```

Structured result: PASS with two class-owned modules, 13 evidence owners, zero
helpers, 13 test functions, four parameterized functions, 30 static parameter
cases, and zero findings. Structural PASS does not replace the human audit or
establish semantic, numerical, or scientific correctness.

## Deterministic results

- exact two-module collection and execution: 39 collected and 39 passed;
- dedicated enum module: ten collected and ten passed, with no missing enum-class
  statements or branches;
- Ruff format and lint over both modules: PASS;
- mypy over `records.py` and both modules: PASS;
- focused public API regression: three passed;
- focused serializer enum-type regression: one passed;
- unique evidence-ID and retained `SV-PROV-133` owner checks: PASS;
- production, inactive backlog, harness, route, and unrelated-work nonmutation:
  PASS;
- `git diff --check`: PASS.

The complete P2-A04 aggregate result is retained in `p2-a04-completion.json` and
`p2-a04-parent-verification.md`.
