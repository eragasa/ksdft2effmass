# P2-A03 ExternalExecutionFailure partial correction

Status: **file-specific deterministic validation passed**

Starting revision: `92edd0b0ca0290e6f8139173eea97cc10c969d7a`.

The completed human file-level audit authorized correction of only
`test__ExternalExecutionFailure.py` plus its file-specific ownership and
migration records. Production `external_execution.py` remained unchanged.

## Evidence inventory

The module contains 39 evidence-owner functions, 21 parameterized functions,
112 static parameter cases, 130 collected cases, and one visible helper:
`make_external_execution_failure`. The helper calls the public constructor with
valid baseline state and explicit overrides and owns no evidence ID, assertion,
normalization, hidden oracle, or I/O.

Historical IDs `SV-PROV-043`, `SV-PROV-044`, and `SV-PROV-230` through
`SV-PROV-236` are preserved. All 17 historical collected nodes map one-to-one to
17 unique current successors. The remaining 113 collected cases are new.

New IDs `SV-PROV-333` through `SV-PROV-362` independently own the newly split
identifier, exact stage/code, wrong-type and cross-enum, diagnostic-path lexical
and tuple-relation, identical/unrelated equality, and stage/code
distinguishability requirements. Historical IDs remain on their closest
semantic successors.

## Structural validator

Exact command:

```bash
python harness/pi/validation/validate_python_test_evidence.py \
  python/tests/software_verification/ksdft2effmass/provenance/test__ExternalExecutionFailure.py \
  --ownership .pi/evidence/backend-neutral-cpn-P2-tools-provenance/p2-a03-external-execution-failure-test-evidence-ownership.json \
  --migration-map .pi/evidence/backend-neutral-cpn-P2-tools-provenance/p2-a03-external-execution-failure-test-evidence-node-migration.json
```

Structured result: PASS with one class-owned module, 39 evidence owners, one
helper, 39 test functions, 21 parameterized functions, 112 static parameter
cases, and zero findings. Structural PASS does not establish semantic,
numerical, or scientific correctness.

## Deterministic results

- exact collection and execution: 130 collected and 130 passed;
- `ExternalExecutionFailure` diagnostic coverage: 54/54 statements and 50/50
  branches;
- Ruff format and lint: PASS;
- mypy over production and the corrected module: PASS;
- focused failure schema/fixture/serialization regression: six passed;
- focused public API regression: three passed;
- production-source Git nonmutation and `git diff --check`: PASS.

The subsequent aggregate P2-A03 consistency result is recorded separately in
`p2-a03-completion.json` and `p2-a03-parent-verification.md`.
