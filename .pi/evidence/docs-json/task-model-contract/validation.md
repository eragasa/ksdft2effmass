# HarnessTask model-contract deterministic validation

Validation status: passed and human-accepted for completed Stage 1, with one accepted separate legacy-projection limitation reported below

Source revision: `dd50c74513f6c51e2a1c823a60b3111738082b3c`

Source identity and mapping coverage: PASS — six Git blobs, 20,074 bytes, 118 ordered contiguous nonoverlapping mappings, all span SHA-256 values recomputed, zero gaps, zero overlaps, zero proposed removals

Documentation routing after correction: PASS — every mapping with a `docs/` target uses `DOCUMENTATION_OWNED_CONTENT`

Documentation progression correction: PASS — the six unique proposed targets are exactly `docs/harness/ksdft2effmass.harness.002.002.000.md` through `.002.002.005.md`; the former `.002.001.012.md` through `.002.001.017.md` targets are absent from the current inventory, mappings, contract, and maintained review page

Contract accounting: PASS — 16 exact `HarnessTask` fields, 19 proposed interfaces, 20 Mermaid diagrams, one focused diagram per interface

Final clarification: PASS — graph results use existing `LocalValidationResult`; the projection profile has one authoritative `template_bytes` representation and only intrinsic constructor invariants; comparator claims are byte-structural rather than semantic; `ResourcePath` reuses the accepted contract; Stage-2 hardening owns exact codes, precedence, parsing, comparison algorithms, and exhaustive cases

Review correction assertions: PASS — all seven retained review findings have explicit corrected dispositions and deterministic checks

Task schemas: PASS — completed Stage 1, inactive Stage 2A, and blocked Stage 2B validate against the current project-local Task schema

Task/chain relations: PASS — Stage 1 is completed, the chain has no active Task, Stage 2A awaits separate human activation review, Stage 2B is blocked on human-accepted Stage 2A, and automatic successor activation is false

Checkpoint validation: PASS — 43 checkpoint records valid and exactly one unresolved Stage-2A activation checkpoint

Relative links: PASS

Whitespace: PASS — `git diff --check`

Dependency and lockfile boundary: PASS — unchanged

Implementation boundary: PASS — no Python source, schema, fixture, projection profile, production test, migrated Task JSON, proposed destination document, dependency, or lockfile was created or modified

## Accepted separate legacy-projection limitation

Command: existing `validate_task_schema_projection.py` invocation for the completed version-1 schema-projection pilot

Result: FAIL with `TASK_RENDER_EXPECTED_DRIFT` and `TASK_RENDER_LIVE_DRIFT`

Cause: activation of Stage 1 changed the authoritative chain-owned active-Task fact from null to `harness.simplification.docs-json.task-model-contract`, while the completed pilot's non-authoritative generated page and expected-byte fixture retain the pre-activation null value.

Disposition status: accepted by the human as a separate legacy limitation that does not block Stage 1. Stage 1 explicitly excludes generated-document and fixture modification, so this contract-only correction does not rewrite either file. The drift does not affect source identities, mapping coverage, the proposed version-2 contract, or exact TaskStateInspector results, and the stale generated page is not authority.
