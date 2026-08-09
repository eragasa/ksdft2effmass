# Co-design JSON control schemas and generated documentation

Status: blocked_awaiting_human_decision; activated on 2026-08-09 after completed documentation correction

Task identity: `harness.simplification.docs-json.schema-projection`

Parent task: `harness.simplification.docs-json`

## Objective

For one human-selected operational record family, replace manually synchronized control prose with authoritative JSON and a deterministic fully generated control-reference page. Derive the smallest useful schema from resolved examples rather than prescribing one universal control schema.

The hierarchical Markdown Task records are bootstrap inputs only. Until a JSON Task contract exists, Markdown decomposition cannot activate children, compute parent completion, supply executable scope, or be interpreted by chain evaluation.

## Authority direction

```text
accepted JSON control record
→ deterministic full-page renderer
→ generated control-reference page
```

Human-authored intake and subject-matter documentation remain separate and may link to the generated page. Generated blocks inside editable pages are not used.

## Bounded pilot

1. Select one corrected operational record family and its exact inputs.
2. Resolve only material field-meaning ambiguities with the human.
3. Define one schema, one valid fixture, important invalid fixtures, and one projection profile.
4. Render one complete expected page in the pilot-selected Markdown or reStructuredText location.
5. Add schema validation and byte-for-byte drift validation and correct the bounded family.

Normal Git history records discarded iterations. Because the software is pre-release with no compatibility consumers, do not create schema-iteration histories, deprecation layers, or old/new field maps unless an existing maintained-evidence identity requires one.

## Object and ownership boundary

JSON control records and projection profiles are immutable DataObjects; validation and rendering outcomes are immutable ResultObjects. Actions follow the accepted grammar, such as `ControlRecordValidator` and `DocumentationProjectionRenderer`.

Generic harness ownership is limited to explicit-input schema-validation and deterministic rendering mechanics. Project-local ownership retains Task and control schemas, authority vocabulary, projection profiles, selected document locations, and fixtures. Generic code must not depend on `.pi/` or ksdft2effmass identities and statuses.

## Completion

Completion requires the accepted schema and fixtures, deterministic full-page rendering from explicit inputs, stable ordering and links, a passing drift check, separate human-authored intake, and no documentation-based activation. Human acceptance is needed only for unresolved material field semantics or another human-owned contract boundary.

This Task does not convert all documentation to JSON, introduce SQLite, change scientific meaning, or activate work from generated pages.

## Current decision boundary

The Task control family is the bounded pilot. Three materially distinct authoritative JSON allocations remain: complete Task records embedded in owning chains, one central Task catalog referenced by chains, or one authoritative JSON file per Task referenced by chains. The decision analysis is `.pi/evidence/docs-json/task-json-authority-architecture.md`; the pending checkpoint is `.pi/checkpoints/harness.simplification.docs-json.schema-projection.task-json-authority.json`. Schema fields, fixtures, rendering, generated-page work, and Python implementation remain blocked until the human selects an allocation.
