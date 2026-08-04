# Independent P1 test-ownership correction review

## Verdict: FAIL (traceability/provenance evidence gaps)

The current executable ownership surface itself passes: all 14 pytest modules are exact `test__ClassName.py` files, each declares one exported class as `SUT` and sole primary SUT, and manual assertion-by-assertion review found only class-owned construction, behavior, operational results, or structured errors. Collaborators are synthetic setup only. Package/schema/fixture/topology/SNAKES assertions are absent from these modules and execute through the non-pytest gate script.

P1 remains open and blocked at unresolved `P1-HC01`; this review does not resolve it, accept P1, or authorize a successor.

## Findings

1. **MEDIUM — the five newly assigned evidence IDs lack explicit predecessor/split traceability.** The correction record says only that splitting formerly multi-owner cases added `SV-CPN-035` through `SV-CPN-039` (`.pi/evidence/backend-neutral-cpn-P1-contract/implementation-progress.md:19-24`). The manifest lists those IDs and current requirements (`test-ownership-manifest.json:11,65,107,118,156`) but has no predecessor module, former test, former ID, or `split_from` field. Historical review evidence establishes selected old assertions—for example old `SV-CPN-010` included empty-string-sequence rejection (`review-tests-correction-1.md:30`) and old `SV-CPN-019` was described as including ResultObject consistency—but does not inventory every former assertion in a machine-readable mapping. Consequently preservation of IDs `001`–`034` is confirmed, and the new behaviors are executable, but the stricter requirement that every former multi-owner assertion be preserved **or explicitly split with correct stable/new traceability cannot be independently attested**.

2. **MEDIUM — the “production/source/schema/fixture semantics unchanged by correction” claim has no immutable pre-correction baseline.** `implementation-progress.md:8-10` and the task at `.pi/tasks/backend-neutral-cpn-P1-contract.md:125-126` make the unchanged claim, while `implementation-progress.md:34-35` explicitly characterizes `checksums.sha256` as the **current** nonhistorical inventory. The checksum file begins at `checksums.sha256:1-12` and validates the current tree only. Production source, schemas, fixtures, and the correction artifacts are untracked in Git, so `git diff` cannot compare pre- and post-correction P1 contents. Current semantics agree with retained pre-checkpoint narrative (49 exports, same schema/fixture scope, and the same unresolved REAL/integer blockers), and no semantic change was detected manually; however, byte- or semantic-identity across the correction cannot be independently proven from durable evidence.

3. **LOW — “case” count terminology is ambiguous across authoritative prose.** The task calls the surface “31 focused cases” (`.pi/tasks/backend-neutral-cpn-P1-contract.md:114-117`) and the Sphinx page says “31 class-owned cases” (`docs/verification/cpn-contract.rst:12-14`), while pytest collects 34 parameterized cases. `implementation-progress.md:19-20,62-65` resolves the underlying inventory as 31 test functions/31 class-owned IDs and 34 collected parameter cases. No executable count is wrong, but the two shorter documents should say “test functions/evidence items” if collection-count ambiguity is to be eliminated.

## Confirmed inventory and ownership

- **14 modules / 31 test functions / 34 collected pytest cases / 31 class-owned IDs.** The parameter expansion is `SV-CPN-004` over four scopes.
- **8 non-class deterministic gates:** `SV-CPN-023` and `SV-CPN-027`–`033`; these cover export inventory, schema metaschema/local resolution, valid/invalid fixtures, relational fixture execution, static dependency direction, and SNAKES/deferred-module isolation (`contract_gates.py`; summarized at `docs/verification/cpn-contract.rst:43-59`). Static import acyclicity is not represented as a scientific-workflow DAG.
- **39 total unique contiguous IDs:** `SV-CPN-001`–`SV-CPN-039`.
- **49 sorted public exports:** manifest and runtime `__all__` agree.
- **14 dedicated-module exports:** `ContractValue`, `CpnDefinitionValidator`, `CpnExpressionEvaluator`, `CpnMarking`, `CpnMarkingValidator`, `CpnToken`, `FiringRequest`, `FiringResult`, `GuardExpression`, `TokenOutcome`, `TransitionEnablementResult`, `TransitionEnabler`, `TransitionFirer`, `ValueExpression`.
- **35 exports explicitly lacking dedicated modules:** `ArcDefinition`, `ArcDirection`, `ColorDefinition`, `ContractValueKind`, `CpnBindingError`, `CpnContractError`, `CpnDefinitionError`, `CpnErrorCode`, `CpnErrorDetail`, `CpnFiringError`, `CpnGuardEvaluationError`, `CpnIssueCode`, `CpnMarkingError`, `CpnNetDefinition`, `CpnValidationIssue`, `CpnValidationResult`, `GuardEvaluationResult`, `GuardOperator`, `InputArcMode`, `InputInscription`, `OutcomeScope`, `OutcomeStatus`, `OutcomeTerminality`, `OutputInscription`, `PlaceDefinition`, `PlaceMarking`, `TokenBinding`, `TokenField`, `TokenFieldAssignment`, `TokenPattern`, `TokenTemplate`, `TransitionBinding`, `TransitionDefinition`, `TransitionNotEnabledError`, `ValueExpressionKind`.
- All six former combined workflow filenames and all four former `integration/test__Cpn*.py` files are absent. Only ignored stale `__pycache__` bytecode for old names remains; it is not collected source evidence.
- Manual review found no disguised package, schema, fixture inventory, import-topology, SNAKES-isolation, persistence, or scientific-workflow assertions in any class module. `validate_test_ownership.py:73-133` correctly checks inventory, naming, SUT declaration, marker, structural owner exercise, ID uniqueness/range, and export status; semantic assertion ownership still appropriately requires manual review.
- VVUQ classification is software verification only. Test/module documentation is non-tautological and states acceptance, failure meaning, limitations, and scientific-validation/UQ exclusions. No controlled fault injection, numerical verification, scientific validation, or UQ is claimed.

## Validation evidence

- Ownership validator and all eight non-class gates: **PASS**, `modules=14 public_exports=49 evidence_ids=39 package_gates=8`.
- Focused pytest: **PASS**, 34 collected cases.
- Full pytest: **PASS**, 955 tests (73 pre-existing unknown-marker warnings when invoked from repository root).
- Ruff check/format: **PASS**, 25 focused files.
- mypy: **PASS**, 25 focused files.
- Sphinx `-W`: **PASS**, 33 sources with MyST 5.1.0, temporary output only.
- SHA-256 validation: **PASS**, all 59 current entries.
- Checkpoint dry-run: **PASS**, 6 valid records and exactly 1 unresolved (`P1-HC01`).
- Strict evidence audit: P1/maintained evidence is clean (`audit_errors=0`); process exits 1 solely for the documented 22 non-P1 unowned operator tests.
- `git diff --check`, staged-file check, and obsolete-source scans: **PASS**; no staged files and no obsolete combined/integration Python sources.

## Residual risks

- The unresolved REAL canonicalization and fixed integer-width/overflow choices remain human-owned blockers; current passing gates do not resolve them.
- The absent explicit old-to-new split map and absent immutable pre-correction content baseline prevent an attested preservation/unchanged conclusion.
- Passing evidence establishes neither Rust conformance, SNAKES adaptation, persistence, two-phase external execution, concrete/common-parent scientific workflow gates, numerical verification, scientific validation, nor UQ.
- The shared worktree is broadly dirty and P1 files are untracked; parent verification must bound the intended combined-tree change.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Three severity-ranked findings cite exact task, manifest, progress, history, checksum, and Sphinx file/line evidence; inventory confirmation and residual risks are explicit."
    }
  ],
  "changedFiles": [],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "cd python && uv run python ../.pi/evidence/backend-neutral-cpn-P1-contract/validate_test_ownership.py",
      "result": "passed",
      "summary": "14 modules, 49 exports, 39 IDs, and 8 package/specification gates passed."
    },
    {
      "command": "cd python && uv run pytest -q tests/software_verification/ksdft2effmass/workflows/cpn",
      "result": "passed",
      "summary": "34 parameterized cases passed from 31 test functions."
    },
    {
      "command": "uv run pytest -q",
      "result": "passed",
      "summary": "955 tests passed; 73 unknown-marker warnings were emitted from root invocation."
    },
    {
      "command": "cd python && uv run python ../.pi/skills/audit_evidence_identifiers.py --strict",
      "result": "failed",
      "summary": "audit_errors=0; exit 1 solely for 22 documented non-P1 unowned-test warnings."
    },
    {
      "command": "sha256sum -c .pi/evidence/backend-neutral-cpn-P1-contract/checksums.sha256",
      "result": "passed",
      "summary": "All 59 current checksum entries validated."
    },
    {
      "command": "cd python && uv run ruff check/format --check <focused P1 files> && uv run mypy <focused P1 files>",
      "result": "passed",
      "summary": "Ruff and mypy passed for 25 focused files."
    },
    {
      "command": "cd docs && ../python/.venv/bin/sphinx-build -W -b html . /tmp/ksdft2effmass-p1-ownership-review",
      "result": "passed",
      "summary": "33 sources built with MyST 5.1.0 and no warnings."
    },
    {
      "command": "python .pi/checkpoints/validate_checkpoints.py --dry-run; git diff --check; staged/obsolete-source scans",
      "result": "passed",
      "summary": "6 checkpoint records valid, exactly 1 unresolved, no staged files, and obsolete combined/integration sources absent."
    }
  ],
  "validationOutput": [
    "Current ownership surface passes all executable gates: 14 modules, 31 functions, 34 collected cases, 49 exports, 35 explicitly missing dedicated modules, 39 contiguous IDs.",
    "FAIL is limited to attested historical split traceability and unchanged-content provenance, plus low count wording ambiguity.",
    "P1-HC01 remains unresolved; P1 and all successors remain blocked/unaccepted."
  ],
  "residualRisks": [
    "No explicit former-case/ID to SV-CPN-035..039 split map exists.",
    "No immutable pre-correction checksum or tracked Git baseline proves production/schema/fixture identity across the correction.",
    "REAL canonicalization and fixed integer width/overflow remain unresolved human-owned decisions.",
    "No Rust, SNAKES-adapter, persistence, external-execution, numerical-verification, scientific-validation, or UQ evidence is established."
  ],
  "noStagedFiles": true,
  "diffSummary": "Read-only project review; no production, test, schema, fixture, task, checkpoint, or documentation source was edited. The required external review artifact was written.",
  "reviewFindings": [
    "medium: .pi/evidence/backend-neutral-cpn-P1-contract/implementation-progress.md:19-24 and test-ownership-manifest.json:11,65,107,118,156 - new IDs 035-039 have no explicit predecessor/split mapping",
    "medium: .pi/evidence/backend-neutral-cpn-P1-contract/implementation-progress.md:8-10,34-35 and checksums.sha256:1-12 - unchanged production/schema/fixture claim has only a current, nonhistorical checksum inventory and no pre-correction baseline",
    "low: .pi/tasks/backend-neutral-cpn-P1-contract.md:114-117 and docs/verification/cpn-contract.rst:12-14 - '31 cases' is ambiguous against 34 collected parameter cases, though implementation-progress.md correctly distinguishes 31 functions from 34 collected cases"
  ],
  "manualNotes": "Verdict is FAIL for attested historical traceability/provenance only; the current one-class ownership implementation and deterministic gates pass. No checkpoint resolution, P1 acceptance, or successor launch occurred."
}
```
