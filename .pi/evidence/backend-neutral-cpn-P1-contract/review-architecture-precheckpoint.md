# P1 Architecture Final Pre-checkpoint Re-review

## Verdict

**Deterministic architecture verdict: PASS**

**P1 final acceptance: BLOCKED** pending the two protected public-contract decisions below. No deterministic architecture, schema, or ResultObject finding remains open. This review does not accept P1.

## Review identity and scope

- Skill: `design-data-action-objects`, SHA-256 `d501c3ce01d16481958833753326751f3a7789e0ad0ebef601b41934cb1e88db`.
- Task: `.pi/tasks/backend-neutral-cpn-P1-contract.md`, SHA-256 `8a73387a35908498e48fb259e000060b3a23a3c96d78de5bea35c1c80c6e7ece`.
- Prior correction review: `.pi/evidence/backend-neutral-cpn-P1-contract/review-architecture-correction-1.md`, SHA-256 `ed62a4e480b7b8780a1a2874f88cbf7b0349939cd79a36a43379efd0ab8cc70d`.
- Reviewed source/specification aggregate SHA-256: `b9522e6031bfae8596886bec6ae2c83899b22c622bea8e3d2a51e92836159b05`.
- Owned task class: read-only architecture, DataObject/ActionObject/ResultObject, backend-neutral CPN execution, schema/Python/Rust compatibility, and scope-boundary review.
- Mutation scope: no implementation, test, schema, fixture, or documentation edits; only this required review artifact was written.

## Findings

### Cleared — `TransitionFirer` public type validation

`TransitionFirer.execute()` now validates `net`, `marking`, and `request` before dereferencing any argument (`python/src/ksdft2effmass/workflows/cpn/execution.py:493-534`). The focused public-path test checks each isolated invalid argument and the all-invalid case (`python/tests/software_verification/ksdft2effmass/workflows/cpn/test__TransitionExecution.py:345-394`). Direct probes now raise `TypeError: net must be CpnNetDefinition`, not `AttributeError`. The prior MODERATE finding is cleared.

### Cleared — Python/schema `string_sequence` agreement

Python requires a tuple of nonempty strings and preserves ordered duplicates (`python/src/ksdft2effmass/workflows/cpn/tokens.py:205-255`). The schema likewise permits duplicate ordered items but requires each item to be nonempty (`specification/workflow-cpn/v1/cpn-contract.schema.json:1126-1131`). Focused integration tests passed.

### Cleared — request and ResultObject invariants

- `FiringRequest.output_token_ids` requires nonempty unique identities (`python/src/ksdft2effmass/workflows/cpn/execution.py:150-163`); its schema uses the shared identifier-set definition (`specification/workflow-cpn/v1/cpn-contract.schema.json:1015-1030`).
- `TransitionEnablementResult` requires matching transition identities and unique bindings (`execution.py:87-100`).
- `FiringResult` enforces transition/binding identity, nonnegative prior revision, exact successor revision, nonempty unique consumed/read IDs, and unique produced-token IDs (`execution.py:227-261`).
- The specification correctly identifies sibling-field relations as language-native constructor invariants beyond JSON Schema's relational expressiveness (`specification/workflow-cpn/v1/README.md:23-29`).

### Cleared — architecture and scope boundaries

The eight-module package retains concrete frozen/slotted DataObjects and ResultObjects, stateless ActionObjects for validation/expression evaluation/enablement/firing, explicit structured errors, complete multiset markings, pure declarative guards, deterministic bindings, and immutable successor results. Static imports remain acyclic even though the represented scientific/computational CPN is intentionally stateful and non-DAG. No generic base class or utility dumping ground exists. Public exports are project-owned and engine-neutral. Source search and focused tests found no SNAKES runtime import, adapter, persistence repository, pickle, external executor, concrete scientific workflow, or P2–P11 payload implementation. Retry/recovery/iteration, authorization, provenance, parent-child lineage, synchronization, read/consume/output arcs, scoped outcomes, failures, and terminality remain representable without Boolean marking collapse.

## Protected public-contract blockers

### BLOCKER — tagged `REAL` JSON/Python canonicalization

Python admits only finite exact built-in `float` for `ContractValueKind.REAL` (`python/src/ksdft2effmass/workflows/cpn/tokens.py:203-249`), while JSON Schema uses `type: number` (`specification/workflow-cpn/v1/cpn-contract.schema.json:96-110`). The probe confirmed that `{"kind":"real","value":1}` is schema-valid but Python-invalid, while `1.0` is accepted by both. The unresolved decision is explicitly recorded at `specification/workflow-cpn/v1/README.md:38-40`.

Human authority must choose the version-1 canonical wire/decoding rule: distinguish integer and real representations on the wire, or admit integer-valued decoded numbers under the `real` tag with explicit float canonicalization. Final Python/schema/Rust contract agreement is blocked until that choice is recorded and implemented.

### BLOCKER — fixed Rust integer width and overflow

Public control integers remain unbounded Python `int`, including iteration and payload schema versions (`python/src/ksdft2effmass/workflows/cpn/tokens.py:346-391`), marking revision, and firing prior revision. Schemas set lower bounds but no maxima (`specification/workflow-cpn/v1/cpn-contract.schema.json:497-525,627-630,1052-1054`), and firing increments revisions without a portable fixed-width overflow contract. The unresolved choice is explicit at `specification/workflow-cpn/v1/README.md:33-40`.

Human authority must choose fixed-width unsigned control integers plus maxima and structured overflow behavior, or an arbitrary-precision Rust representation and its dependency/interoperability implications. Rust translatability and cross-language conformance remain blocked until that choice is recorded and implemented.

## Commands and results

- Focused CPN workflow and integration pytest: **37 passed**.
- Ruff over the CPN source and focused tests: **passed**.
- mypy over all eight CPN source modules: **passed**.
- Sphinx HTML build with `-W --keep-going`: **passed**.
- Public import smoke probe: **passed** (`CpnNetDefinition TransitionEnabler`).
- `TransitionFirer` wrong-type direct probe: **passed**, yielding documented `TypeError`.
- Python/JSON-Schema real-number probe: **confirmed only the protected divergence**.
- SNAKES/external-operation/import-direction source probes: **passed**; only explanatory mentions of SNAKES were found.
- `git diff --check` over reviewed P1 paths: **passed**.
- Staged-file check: **no staged files**.
- Initial test/lint/Sphinx invocations from repository root used Python-relative paths and failed to locate inputs; corrected `cd python` reruns above passed. This was a review-command setup error, not a product finding.

## Files inspected

`AGENTS.md`; `.pi/tasks/backend-neutral-cpn-P1-contract.md`; `.pi/evidence/backend-neutral-cpn-P1-contract/review-architecture-correction-1.md`; the full `python/src/ksdft2effmass/workflows/cpn/` package; all files under `specification/workflow-cpn/v1/`; focused CPN workflow and integration tests; and the CPN API, concept, and verification documentation included in the warnings-as-errors Sphinx build.

## Residual risks

- The two protected public-contract choices prevent final P1 acceptance and complete Rust/wire conformance.
- No Rust implementation or cross-language conformance executable exists; P1 must not claim such verification.
- Persistence, SNAKES adaptation, concrete workflows, external execution, and scientific execution remain appropriately deferred.
- Passing evidence is software verification only, not numerical verification, scientific validation, or uncertainty quantification.
- The worktree contains extensive pre-existing modified/untracked files; this review changed none of them.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Concrete cleared findings and two protected blockers are reported with file:line evidence; deterministic architecture verdict is PASS and final acceptance is separately BLOCKED."
    }
  ],
  "changedFiles": [],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "cd python && uv run pytest -q tests/software_verification/ksdft2effmass/workflows/cpn tests/software_verification/ksdft2effmass/integration/test__CpnDependencyDirection.py tests/software_verification/ksdft2effmass/integration/test__CpnJsonFixtures.py tests/software_verification/ksdft2effmass/integration/test__CpnJsonSchemas.py tests/software_verification/ksdft2effmass/integration/test__CpnSnakesIsolation.py",
      "result": "passed",
      "summary": "37 passed"
    },
    {
      "command": "cd python && uv run ruff check <focused P1 paths> && uv run mypy src/ksdft2effmass/workflows/cpn",
      "result": "passed",
      "summary": "Ruff passed; mypy found no issues in 8 source files"
    },
    {
      "command": "cd python && uv run --extra docs sphinx-build -W --keep-going -b html ../docs ../.pi-subagents/tmp/cpn-p1-precheckpoint-sphinx",
      "result": "passed",
      "summary": "Sphinx warnings-as-errors build succeeded"
    },
    {
      "command": "targeted TransitionFirer and Python/JSON-Schema probes",
      "result": "passed",
      "summary": "TransitionFirer wrong types now produce documented TypeError; only the protected integer-valued REAL divergence remains"
    },
    {
      "command": "public import, source-boundary, git diff --check, and staged-file probes",
      "result": "passed",
      "summary": "Public imports and scope checks passed; no whitespace errors and no staged files"
    }
  ],
  "validationOutput": [
    "37 focused tests passed",
    "TransitionFirer type-validation correction is effective and tested",
    "All prior deterministic schema and ResultObject findings are cleared",
    "Ruff, mypy, public imports, and Sphinx -W passed",
    "Exactly two protected public-contract blockers remain"
  ],
  "residualRisks": [
    "Protected tagged REAL JSON/Python canonicalization remains unresolved",
    "Protected fixed Rust integer width and overflow contract remains unresolved",
    "No Rust/cross-language executable conformance implementation exists",
    "Deferred persistence, SNAKES adapter, concrete workflow, and scientific execution are unverified by design"
  ],
  "noStagedFiles": true,
  "diffSummary": "Read-only re-review; no implementation, test, schema, fixture, or documentation changes were made.",
  "reviewFindings": [
    "no deterministic blockers: TransitionFirer type validation and all prior schema/ResultObject findings are cleared",
    "blocker: python/src/ksdft2effmass/workflows/cpn/tokens.py:203-249 and specification/workflow-cpn/v1/cpn-contract.schema.json:96-110 - protected tagged REAL wire/Python canonicalization remains unresolved",
    "blocker: specification/workflow-cpn/v1/README.md:33-40 - protected fixed Rust integer widths and overflow behavior remain unresolved"
  ],
  "manualNotes": "Deterministic architecture verdict PASS. P1 final acceptance remains BLOCKED solely on the two protected public-contract decisions. No acceptance was performed."
}
```
