# Stage-2A independent-review correction

Review input: [integration-review.md](integration-review.md)

Correction-cycle policy: This is the single authorized consolidated correction pass. The original failed review remains unchanged. No repeated independent-review loop was performed.

Claim boundary: Passing corrections and tests establish software verification only. They do not accept the implementation, activate Stage 2B, authorize a migration, or establish scientific validity.

## Finding dispositions

### 1. Required behavioral evidence was incomplete — corrected

Disposition: Material finding accepted.

Correction:

- retained one class-owned module for every accepted public class;
- added owning behavioral evidence for intrinsic type/value boundaries, canonical serializer type closure, BOM/invalid-UTF-8/key closure, graph input closure, source byte count/Git object/SHA-256 identity, mapping ranges/types/span checks, documentation mapping alignment and opaque bytes, template and rendered identities, renderer explicit-input behavior, comparator overlap/span failures, comparison-result ranges/status, request field closure, packet-preparer recomputation, packet type closure, and disposition type closure;
- expanded cross-surface artifact evidence while preserving class ownership;
- retained exact test ownership in `test-ownership.json`; and
- updated the maintained conformance inventory and the `SV-HT` evidence namespace.

Verification:

- 62 focused Stage-2A tests passed before compatibility tests were added;
- 74 focused Stage-2A plus predecessor adapter/inspector tests passed after correction;
- explicit Python conformance validation passed with zero findings; and
- repository-wide maintained-evidence conformance passed with 241 modules and 2,924 collected nodes.

### 2. Mixed-format and TaskStateInspector compatibility evidence was absent — corrected

Disposition: Material finding accepted.

Correction:

- added one explicit `TaskRecordAdapter` chain containing Markdown, version-1 JSON, and version-2 JSON records;
- verified all three references and failure on duplicated version-2 JSON/chain status authority;
- added parameterized direct `TaskStateInspector` evidence for selected Markdown, version-1 JSON, and version-2 JSON paths;
- verified established status precedence for every format; and
- verified version-2 identity disagreement reports `PIH.TASK_STATE.REFERENCE_INVALID`.

Verification: The corrected focused set passed, including semantic parameter identities for all three selected formats.

### 3. Focused mypy failed on jsonschema — corrected

Disposition: Material finding accepted.

Correction: Added the repository-established `# type: ignore[import-untyped]` annotation to the maintained `jsonschema` import.

Verification: Focused mypy passed for production Task model, adapter compatibility, synthetic helpers, and the cross-surface artifact module with zero issues.

### 4. Comparison-result status annotation used `str` instead of `Identifier` — corrected

Disposition: Material finding accepted.

Correction: Changed `HarnessTaskDocumentationComparisonResult.status` to the accepted `Identifier` alias and added an exact future-annotation assertion to public API evidence.

Verification: Ruff, mypy, focused pytest, public API evidence, and Sphinx autodoc all passed.

## Additional compatibility corrections found by deterministic broad testing

The first broad repository test run found four Stage-2A compatibility expectations that still described the pre-Stage-2A 30-name/resource boundary. These were deterministic predecessor-evidence updates, not a second review:

- changed the local import-side-effect inventory from 30 to 49 public names and included the explicit `task_model` submodule;
- extended the exact local public inventory with the accepted 19 interfaces;
- extended Actionizer suffix evidence with `Deserializer`, `Recorder`, `Renderer`, and `Serializer`;
- extended bounded manifest-coverage evidence to the accepted `fixtures/task-record-v2` family and exact oracle index; and
- retained the one renamed public-inventory node in `test-node-migration.json`.

The same broad run also reported two unrelated wheel-fixture setup errors because the canonical virtual environment has no `pip` module. No dependency or environment mutation was authorized or performed. After correcting the four in-scope expectations, the broad suite passed with 2,922 tests and the two wheel tests explicitly deselected. The wheel limitation is pre-existing packaging-environment coverage, not a HarnessTask failure.

## Final deterministic correction verification

- Focused HarnessTask, adapter, and inspector tests: 74 passed.
- Broad Python suite excluding the two unavailable-pip wheel cases: 2,922 passed, 2 deselected.
- Focused Ruff: passed.
- Focused mypy: passed with zero issues.
- Explicit Stage-2A evidence-conformance validation: passed with zero findings.
- Repository maintained-evidence conformance: passed with 241 modules, 2,924 collected nodes, and zero findings.
- Local harness resource validation: passed with zero issues.
- Sphinx warnings-as-errors build: passed.
- Git whitespace validation: passed.
- Six authoritative Markdown Task SHA-256 identities: unchanged.

No real migration packet was prepared, no authoritative Markdown Task changed, and Stage 2B remains inactive.
