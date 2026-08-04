# Final independent P1 test-ownership correction re-review

## Verdict: PASS (one LOW documentation-count residual)

The two material failures from the initial review are corrected. Manifest v2 provides complete executable old-to-new traceability for all ten former modules and every old ID `SV-CPN-001`--`SV-CPN-034`, including the exact five splits. The mutation audit and synchronized task/progress/Sphinx prose truthfully limit the unchanged-content statement because no durable per-file pre-correction baseline exists. Current one-class ownership, package/specification gates, focused tests, full tests, static checks, Sphinx, checkpoint state, and current SHA-256 inventory pass.

The sole new residual is LOW: implementation progress still calls the checksum inventory “59-file,” while the current passing inventory has 61 entries. This does not invalidate any digest or ownership result, but that historical command-count sentence is stale.

P1 remains open and blocked at unresolved `P1-HC01`; this review neither resolves the checkpoint nor accepts/closes P1 or authorizes a successor.

## Findings

1. **LOW — stale checksum-entry count in implementation evidence.** `.pi/evidence/backend-neutral-cpn-P1-contract/implementation-progress.md:81-82` reports a “59-file SHA-256 validation,” but `.pi/evidence/backend-neutral-cpn-P1-contract/checksums.sha256:1-61` currently contains 61 entries. `sha256sum -c` passed all 61. The inventory content is internally valid; only the recorded count is stale.

No MEDIUM or HIGH test-ownership finding remains.

## Initial-finding disposition

- **Old-to-new traceability: resolved.** The manifest states the former ten-module/34-ID surface and mapping rule at `test-ownership-manifest.json:632-635`. The validator hard-codes the authoritative former module by each old ID and split predecessors at `validate_test_ownership.py:18-68`, requires ten former modules, one retained partition for every old item, exact current targets, all old IDs `001`--`034`, all current IDs `001`--`039`, and exact split mapping at `validate_test_ownership.py:98-156`.
- **Exact split IDs: resolved and executable.** The mappings are `010 -> 035` (`test-ownership-manifest.json:762-778`), `012 -> 036` (`:801-816`), `018 -> 037` (`:890-906`), and `019 -> 038,039` (`:910-933`). The validator's exact predecessor map is `{35:10, 36:12, 37:18, 38:19, 39:19}` (`validate_test_ownership.py:68`). Each old ID retains its original ID in addition to any partition split.
- **Test-count wording: resolved.** Current authoritative prose consistently distinguishes 14 modules, 31 test functions/class-owned evidence items, and 34 collected parameter cases (`implementation-progress.md:24-30`, `.pi/tasks/backend-neutral-cpn-P1-contract.md:113-125`, `docs/verification/cpn-contract.rst:12-20`). `SV-CPN-004` is the only parameter expansion, over four scopes. This wording no longer calls 31 functions merely “cases.”
- **Unavailable baseline: resolved as a truthful limitation.** The audit expressly says byte identity is not independently attested and unlike aggregates are not comparable proof (`test-ownership-mutation-audit.json:3-11,61-73`). Progress (`implementation-progress.md:8-15`), task (`.pi/tasks/backend-neutral-cpn-P1-contract.md:127-133`), and Sphinx (`docs/verification/cpn-contract.rst:84-93`) repeat the bounded “no detected change” statement and the unavailable-baseline limitation. This review therefore does **not** attest pre/post byte identity.

## Current ownership inventory

Manual assertion-by-assertion review reconfirmed the following sole-primary-SUT modules:

- `test__ContractValue.py`: `SV-CPN-035`
- `test__CpnDefinitionValidator.py`: `SV-CPN-011`
- `test__CpnExpressionEvaluator.py`: `SV-CPN-008`--`010`
- `test__CpnMarking.py`: `SV-CPN-012`
- `test__CpnMarkingValidator.py`: `SV-CPN-013`, `014`, `036`
- `test__CpnToken.py`: `SV-CPN-001`--`003`
- `test__FiringRequest.py`: `SV-CPN-037`
- `test__FiringResult.py`: `SV-CPN-039`
- `test__GuardExpression.py`: `SV-CPN-007`
- `test__TokenOutcome.py`: `SV-CPN-004`, `005`
- `test__TransitionEnablementResult.py`: `SV-CPN-038`
- `test__TransitionEnabler.py`: `SV-CPN-015`, `016`, `024`--`026`
- `test__TransitionFirer.py`: `SV-CPN-017`--`022`, `034`
- `test__ValueExpression.py`: `SV-CPN-006`

Each file is exactly `test__ClassName.py`, declares that exported class as `SUT`, carries the software-verification marker, and documents it as sole primary SUT. The validator enforces these properties and exact manifest/test agreement (`validate_test_ownership.py:159-209`). Manual review found assertions only about the named constructor/invariants, ActionObject behavior/results, or structured error translation. Collaborators build synthetic setup. No class module disguises export inventory, schema/fixture orchestration, source topology, SNAKES isolation, persistence, scientific acceptance, or UQ assertions.

**Counts:** 14 modules; 31 test functions/class-owned IDs; 34 collected parameter cases; 8 non-class gate IDs; 39 unique contiguous total IDs; 49 sorted public exports; 14 dedicated modules; 35 exports without a dedicated module. The validator confirms the contiguous ID and export inventories at `validate_test_ownership.py:170-172,211-218`.

**35 exports explicitly lacking a dedicated module:** `ArcDefinition`, `ArcDirection`, `ColorDefinition`, `ContractValueKind`, `CpnBindingError`, `CpnContractError`, `CpnDefinitionError`, `CpnErrorCode`, `CpnErrorDetail`, `CpnFiringError`, `CpnGuardEvaluationError`, `CpnIssueCode`, `CpnMarkingError`, `CpnNetDefinition`, `CpnValidationIssue`, `CpnValidationResult`, `GuardEvaluationResult`, `GuardOperator`, `InputArcMode`, `InputInscription`, `OutcomeScope`, `OutcomeStatus`, `OutcomeTerminality`, `OutputInscription`, `PlaceDefinition`, `PlaceMarking`, `TokenBinding`, `TokenField`, `TokenFieldAssignment`, `TokenPattern`, `TokenTemplate`, `TransitionBinding`, `TransitionDefinition`, `TransitionNotEnabledError`, and `ValueExpressionKind`.

All six former combined workflow source modules and all four former integration source modules are absent. Only stale ignored bytecode remains. The eight package/specification gates retain `SV-CPN-023` and `SV-CPN-027`--`033` outside pytest, as documented at `docs/verification/cpn-contract.rst:46-67`. Static dependency direction is correctly treated as package import acyclicity, not as a claim that the stateful CPN scientific workflow is a DAG.

## Validation evidence

- Ownership validator plus eight non-class gates: **PASS** — `modules=14 public_exports=49 evidence_ids=39 package_gates=8`.
- Focused pytest: **PASS** — 34 collected parameter cases.
- Full Python pytest: **PASS** — 955 tests.
- Ruff check and format: **PASS** — 26 focused files.
- mypy: **PASS** — 26 focused files.
- Sphinx `-W`: **PASS** — 33 sources, MyST 5.1.0, temporary output only.
- SHA-256: **PASS** — all 61 current entries.
- Checkpoint dry run: **PASS** — 6 valid records, exactly 1 unresolved.
- Strict evidence audit: `audit_errors=0`; expected process exit 1 solely for 22 documented non-P1 operator-test ownership warnings.
- `git diff --check`, no-staged-file check, and obsolete-source scan: **PASS**.

## Residual risks and boundaries

- **LOW documentation residual:** the 59-file wording at `implementation-progress.md:81-82` is stale against the passing 61-entry current inventory.
- Pre-correction per-file hashes are unavailable. Evidence supports “no detected protected mutation,” not independently attested byte identity.
- `P1-HC01` remains blocked with no human response (`.pi/checkpoints/P1-HC01-cpn-numeric-wire-contract.json:2-6,28-32,67-72`). Tagged-`REAL` canonicalization and integer width/overflow remain human-owned.
- Passing software verification establishes no Rust conformance, authoritative persistence, SNAKES adaptation, external execution, concrete/common-parent scientific workflow acceptance, numerical verification, scientific validation, or UQ.
- The shared worktree remains broadly dirty and P1 files are untracked. No staged files were present; this review made no repository-source change.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "One exact LOW finding cites implementation-progress.md:81-82 and checksums.sha256:1-61; resolved initial findings, current ownership inventory, commands, and residual risks are explicitly documented."
    }
  ],
  "changedFiles": [],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "cd python && uv run python ../.pi/evidence/backend-neutral-cpn-P1-contract/validate_test_ownership.py",
      "result": "passed",
      "summary": "14 modules, 49 exports, 39 contiguous IDs, exact migration map, and 8 package/specification gates passed."
    },
    {
      "command": "sha256sum -c .pi/evidence/backend-neutral-cpn-P1-contract/checksums.sha256",
      "result": "passed",
      "summary": "All 61 current inventory entries passed."
    },
    {
      "command": "cd python && uv run pytest -q tests/software_verification/ksdft2effmass/workflows/cpn",
      "result": "passed",
      "summary": "34 parameter cases from 31 functions passed."
    },
    {
      "command": "cd python && uv run pytest -q",
      "result": "passed",
      "summary": "955 tests passed."
    },
    {
      "command": "cd python && uv run ruff check <26 focused files> && uv run ruff format --check <26 focused files> && uv run mypy <26 focused files>",
      "result": "passed",
      "summary": "Lint, formatting, and static typing passed for all 26 focused files."
    },
    {
      "command": "cd docs && ../python/.venv/bin/sphinx-build -W -b html . /tmp/ksdft2effmass-p1-final-review",
      "result": "passed",
      "summary": "33 sources built without warnings using MyST 5.1.0."
    },
    {
      "command": "python .pi/checkpoints/validate_checkpoints.py --dry-run; git diff --check; staged and obsolete-source scans",
      "result": "passed",
      "summary": "6 checkpoint records valid, exactly 1 unresolved, no staged files, and no obsolete test sources."
    },
    {
      "command": "cd python && uv run python ../.pi/skills/audit_evidence_identifiers.py --strict",
      "result": "failed",
      "summary": "audit_errors=0; exit 1 solely for 22 documented non-P1 unowned operator-test warnings."
    }
  ],
  "validationOutput": [
    "PASS: material initial traceability/provenance/count findings are corrected.",
    "Inventory: 14 modules, 31 functions/class IDs, 34 collected cases, 8 non-class gates, 39 total IDs, 49 exports, 14 dedicated and 35 missing dedicated modules.",
    "Checksum inventory passes all 61 entries; implementation-progress.md retains one stale 59-file count.",
    "P1-HC01 remains unresolved and no acceptance or successor action occurred."
  ],
  "residualRisks": [
    "LOW: implementation-progress.md:81-82 says 59-file SHA-256 validation while the current passing inventory has 61 entries.",
    "No durable pre-correction per-file baseline exists; byte identity is not independently attested.",
    "P1-HC01 numeric wire semantics remain unresolved and human-owned.",
    "No Rust, persistence, SNAKES-adapter, external-execution, scientific-validation, or UQ evidence is established."
  ],
  "noStagedFiles": true,
  "diffSummary": "Read-only review; no repository production, test, specification, fixture, task, checkpoint, or documentation source was edited. Only the required external review artifact was written.",
  "reviewFindings": [
    "low: .pi/evidence/backend-neutral-cpn-P1-contract/implementation-progress.md:81-82 - reports a 59-file SHA-256 validation, but checksums.sha256:1-61 contains 61 currently passing entries",
    "no medium or high test-ownership findings"
  ],
  "manualNotes": "Verdict PASS applies only to the bounded deterministic test-ownership correction. P1 remains open and blocked at P1-HC01; this review does not accept P1 or authorize successors."
}
```
