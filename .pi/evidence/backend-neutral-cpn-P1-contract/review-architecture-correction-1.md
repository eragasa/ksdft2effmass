# P1 Architecture/Rust Correction Re-review

**Verdict: FAIL**

The initial deterministic Python/schema and ResultObject consistency findings are corrected. The protected `real` wire canonicalization and Rust integer width/overflow choices remain unresolved exactly as documented. However, they are **not the only remaining issues**: `TransitionFirer.execute()` still violates its documented public wrong-type exception contract by dereferencing `net` and `marking` before validating those arguments. This is a deterministic correction, so the review cannot return `BLOCKED` solely on the protected choices.

## Review identity and scope

- Skill: `design-data-action-objects`, SHA-256 `d501c3ce01d16481958833753326751f3a7789e0ad0ebef601b41934cb1e88db`.
- Request: read-only P1 correction architecture/Rust re-review; mutation scope `none` except this required review artifact.
- Task identity: `.pi/tasks/backend-neutral-cpn-P1-contract.md`, SHA-256 `8a73387a35908498e48fb259e000060b3a23a3c96d78de5bea35c1c80c6e7ece`.
- Parent-workflow/attempt identity: runtime artifact attempt `e6505e86`; no separate parent-workflow identity was supplied.
- Prior review: `.pi/evidence/backend-neutral-cpn-P1-contract/review-architecture-initial.md`, SHA-256 `e5fcf717430b1495a517b6cc9831557cbc69894d4e01225ad4a84a4e5c2c0b84`.
- Reviewed source/specification aggregate SHA-256: `011515e1069c67a3ccdcfe227045102efed5323e00c7287f9f6acc20e99e8bec`.
- Owned task class: independent architecture, DataObject/ActionObject/ResultObject, neutral execution, schema/Python/Rust, and scope-boundary review.

## Findings

### MODERATE — `TransitionFirer` bypasses its public argument-type contract

`TransitionFirer.execute()` documents `TypeError` for a public argument of the wrong semantic type at `python/src/ksdft2effmass/workflows/cpn/execution.py:493-519`. It validates only `request` at lines 526-527, then dereferences `net.model_id`/`net.arcs` at lines 528-545 and `marking.places` at lines 551-553 before `TransitionEnabler` performs type-aware validation later. The direct public probe

```text
TransitionFirer().execute(object(), object(), FiringRequest("t", TransitionBinding("t", ()), ()))
```

raised `AttributeError: 'object' object has no attribute 'arcs'`, not the documented `TypeError`. This is inconsistent with the public ActionObject exception taxonomy and leaves a gap in the requirement that invalid firings produce documented structured/type errors (`.pi/tasks/backend-neutral-cpn-P1-contract.md:73-76`). The focused tests do not cover wrong-type `net`/`marking` arguments for this ActionObject.

**Recommendation:** deterministically validate all three public arguments before any dereference or operational work, and add public-path software-verification coverage. Preserve the independently reachable mismatched request/binding path and its structured `invalid_binding` error.

## Initial findings rechecked

### Corrected — `string_sequence` Python/schema agreement

- Python now requires nonempty strings while preserving ordered duplicates: `python/src/ksdft2effmass/workflows/cpn/tokens.py:203-210,244-259`.
- Schema now uses a nonunique ordered array with nonempty items: `specification/workflow-cpn/v1/cpn-contract.schema.json:1126-1131`.
- Integration evidence covers duplicates accepted and empty entries rejected: `python/tests/software_verification/ksdft2effmass/integration/test__CpnJsonSchemas.py:121-130`.
- Probe result: `['x', 'x']` accepted by both; `['']` rejected by both.

### Corrected — firing request/output and result invariants

- `FiringRequest.output_token_ids` rejects empty and duplicate IDs: `python/src/ksdft2effmass/workflows/cpn/execution.py:150-163`; schema uses unique nonempty `$defs/ids` at `specification/workflow-cpn/v1/cpn-contract.schema.json:1021-1030`.
- `TransitionEnablementResult` enforces matching transition identity and unique bindings: `execution.py:87-100`.
- `FiringResult` enforces nonempty transition identity, matching binding identity, nonnegative prior revision, successor revision, unique/nonempty consumed/read IDs, and unique produced IDs: `execution.py:227-268`.
- Public tests cover these corrected states without invariant bypass: `python/tests/software_verification/ksdft2effmass/workflows/cpn/test__TransitionExecution.py:254-318`.
- The language-neutral README correctly identifies sibling-field relations as language-native constructor invariants where JSON Schema cannot express them: `specification/workflow-cpn/v1/README.md:23-29`.

### Still protected — `real` wire canonicalization

- Python accepts only finite exact built-in `float`: `python/src/ksdft2effmass/workflows/cpn/tokens.py:203-210,232-253`.
- JSON Schema `type: number` admits integer-valued JSON numbers: `specification/workflow-cpn/v1/cpn-contract.schema.json:96-110`.
- Probe remains: `{"kind":"real","value":1}` is schema-valid and Python-invalid.
- The unresolved status is explicit in `specification/workflow-cpn/v1/README.md:38-40`, `docs/api/workflows-cpn.md:14-18`, and `docs/verification/cpn-contract.rst:36-38`.

### Still protected — Rust integer width and overflow

- Public control integers remain Python `int`, including token iteration/schema fields (`python/src/ksdft2effmass/workflows/cpn/tokens.py:346-354,388-392`), marking revision (`python/src/ksdft2effmass/workflows/cpn/markings.py:82-84,104-107`), and firing prior revision (`python/src/ksdft2effmass/workflows/cpn/execution.py:177-181,204-207`).
- Schemas provide lower bounds but no maxima, e.g. `specification/workflow-cpn/v1/cpn-contract.schema.json:497-525,627-630,1052-1054`.
- Successor firing increments revision without a portable overflow case at `python/src/ksdft2effmass/workflows/cpn/execution.py:660-663`.
- Rust mapping remains structural but intentionally does not choose widths/overflow: `specification/workflow-cpn/v1/README.md:33-40`; `docs/api/workflows-cpn.md:13-18`.

## Architecture conformance observed

- DataObjects and ResultObjects are frozen, slotted, tuple-backed, and own intrinsic invariants. Cross-object graph/marking policy belongs to `CpnDefinitionValidator` and `CpnMarkingValidator`; expression evaluation, enablement, and firing belong to stateless ActionObjects. No generic base class or utility dumping ground was introduced.
- Static Python imports are acyclic and layered (`tokens/markings/expressions/model/validation/execution`) while the represented computational model remains a stateful CPN, not an import DAG. `SV-CPN-032` enforces the static dependency allowlist.
- `CpnNetDefinition` represents places, transitions, arcs, colors, guards, inscriptions, and initial marking; markings retain complete place sets and token multiplicity. Pure declarative guards contain no callable/eval/I/O surface. Enablement/firing represent synchronization, read/consume/output behavior, retry/recovery/iteration, authorization, provenance, lineage, and scoped outcomes.
- External operations remain outside guard evaluation. No source module imports SNAKES or implements an engine adapter, persistence repository, external executor, concrete scientific workflow/payload, or P2–P11 object. `SV-CPN-033` checks adapter/persistence absence and SNAKES isolation.
- Public exports remain engine-neutral at `python/src/ksdft2effmass/workflows/cpn/__init__.py:1-104`.

## Decision required: `real` wire canonicalization

### Exact conflict

JSON Schema admits integer-valued JSON numbers for a `real`, while the Python reference admits only exact built-in `float`. A cross-language lexical/canonical decoding rule is not established.

### Files inspected

- `python/src/ksdft2effmass/workflows/cpn/tokens.py:203-259`: Python tagged-value invariant.
- `specification/workflow-cpn/v1/cpn-contract.schema.json:96-110`: JSON `number` wire rule.
- `specification/workflow-cpn/v1/README.md:38-40`: explicitly unresolved protected choice.

### Conflicting instructions

- `AGENTS.md`: runtime acceptance, schemas, tests, and Rust mappings must agree.
- Current Python and schema contracts intentionally remain different pending authority.

### Options

1. **Fix a wire canonicalization that distinguishes integer and real representations**
   - Consequence: schema/decoder/fixtures must encode how a JSON number is assigned a tag across languages.
2. **Allow integer-valued decoded numbers under the `real` tag**
   - Consequence: Python runtime acceptance broadens and canonicalization to built-in `float` must be explicit.

### Recommendation

Human authority must select and record the version-1 wire rule before cross-language conformance or P1 acceptance.

### Work status

- Safe to continue: deterministic review and Python-only software verification.
- Blocked: final wire contract and attested Python/schema/Rust agreement.

## Decision required: Rust integer widths and overflow

### Exact conflict

Python and JSON currently expose unbounded nonnegative integers, but no Rust width, maximum, conversion-overflow rule, or successor-revision overflow error is fixed.

### Files inspected

- `python/src/ksdft2effmass/workflows/cpn/tokens.py:346-354,388-392`.
- `python/src/ksdft2effmass/workflows/cpn/markings.py:82-84,104-107`.
- `python/src/ksdft2effmass/workflows/cpn/execution.py:204-207,660-663`.
- `specification/workflow-cpn/v1/README.md:33-40`.

### Conflicting instructions

No conflicting instruction found. The required Rust-compatible mapping is incomplete.

### Options

1. **Adopt fixed-width unsigned control integers**
   - Consequence: schemas/Python need maxima and firing needs a structured overflow case.
2. **Require arbitrary-precision Rust integers**
   - Consequence: adds dependency, ownership, and interoperability implications.

### Recommendation

Human authority should select widths and overflow taxonomy before P1 acceptance.

### Work status

- Safe to continue: bounded Python synthetic verification.
- Blocked: Rust-translatability and cross-language conformance claims.

## Commands and exact results

- Focused CPN pytest: **36 passed**.
- Ruff over eight source modules and focused tests: **passed**.
- mypy over eight source modules: **passed**.
- Public import smoke test: **passed** (`CpnNetDefinition TransitionEnabler`).
- Sphinx HTML build with `-W --keep-going`: **passed**.
- Python/schema correction probe: duplicate/nonempty `string_sequence` agreement confirmed; protected integer-valued-real divergence confirmed.
- Result/request probe: mismatched/duplicate enablement bindings and duplicate output IDs rejected.
- `TransitionFirer` wrong-type probe: **failed contract** with `AttributeError` instead of documented `TypeError`.
- `git diff --check` over reviewed P1 paths: **passed**.
- Staged-file check: **no staged files**.

## Files inspected

`AGENTS.md`; the active P1 task; the initial architecture review; the complete eight-module `python/src/ksdft2effmass/workflows/cpn/` package; all version-1 schemas/fixtures and both specification READMEs; focused CPN tests and integration owners (with correction-specific modules read directly and the complete set executed); `docs/api/workflows-cpn.md`; `docs/concepts/cpn-contract.md`; `docs/verification/cpn-contract.rst`; Sphinx configuration/navigation implicated by the successful build.

## Mutation summary

No implementation, schema, fixture, test, or documentation file was edited. Only this required review artifact was written. The working tree contained extensive pre-existing changes/untracked P1 files.

## Residual risks

- The deterministic `TransitionFirer` argument-validation defect must be corrected and covered before a re-review can determine whether only the two protected decisions remain.
- No Rust implementation or cross-language fixture test exists.
- Persistence, SNAKES adaptation, concrete workflows, external execution, and scientific execution remain appropriately deferred.
- Passing checks establish software verification only, not numerical verification, scientific validation, or UQ.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Concrete MODERATE finding at python/src/ksdft2effmass/workflows/cpn/execution.py:493-553 plus corrected and protected findings with exact file:line evidence."
    }
  ],
  "changedFiles": [],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "cd python && uv run pytest -q <focused CPN and integration paths>",
      "result": "passed",
      "summary": "36 passed"
    },
    {
      "command": "cd python && uv run ruff check <focused P1 paths> && uv run mypy src/ksdft2effmass/workflows/cpn",
      "result": "passed",
      "summary": "Ruff passed; mypy found no issues in 8 source files"
    },
    {
      "command": "cd python && uv run --extra docs sphinx-build -W --keep-going -b html ../docs ../.pi-subagents/tmp/e6505e86-sphinx",
      "result": "passed",
      "summary": "Sphinx build succeeded with warnings treated as errors"
    },
    {
      "command": "targeted Python/JSON-Schema and public constructor/ActionObject probes",
      "result": "failed",
      "summary": "Corrections passed, protected real divergence remained, and TransitionFirer wrong-type input raised AttributeError instead of TypeError"
    },
    {
      "command": "git diff --check over reviewed P1 paths and staged-file check",
      "result": "passed",
      "summary": "No whitespace errors and no staged files"
    }
  ],
  "validationOutput": [
    "36 focused tests passed",
    "Ruff and mypy passed",
    "Sphinx -W passed",
    "Public import smoke test passed",
    "TransitionFirer wrong-type probe exposed an undocumented AttributeError"
  ],
  "residualRisks": [
    "Protected real wire canonicalization remains unresolved",
    "Protected Rust integer width/overflow contract remains unresolved",
    "TransitionFirer public argument validation remains deterministically defective",
    "No Rust/cross-language conformance implementation exists"
  ],
  "noStagedFiles": true,
  "diffSummary": "Read-only re-review; no production/test/schema/doc changes made.",
  "reviewFindings": [
    "moderate: python/src/ksdft2effmass/workflows/cpn/execution.py:493-553 - TransitionFirer dereferences net and marking before public type validation, producing AttributeError rather than documented TypeError",
    "blocker: specification/workflow-cpn/v1/cpn-contract.schema.json:96-110 and python/src/ksdft2effmass/workflows/cpn/tokens.py:203-259 - protected real wire canonicalization remains unresolved",
    "blocker: specification/workflow-cpn/v1/README.md:33-40 - protected Rust integer widths and overflow behavior remain unresolved"
  ],
  "manualNotes": "Verdict FAIL. Initial deterministic findings are corrected, but the two protected choices are not yet the only remaining issues. No acceptance was performed."
}
```
