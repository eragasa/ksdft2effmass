# HarnessTask Stage-2A implementation-acceptance packet

Decision requested: Accept, request bounded correction, or defer the Stage-2A implementation. This packet does not activate Stage 2B or accept any file migration.

## Outcome

The accepted schema-version-2 `HarnessTask` contract is implemented as 19 project-local public interfaces. Canonical JSON, strict decoding, structural graph validation, explicit rendering, byte-structural comparison, migration-review packet preparation, exact disposition recording, v1/v2/Markdown compatibility, resources, documentation, and maintained software-verification evidence are present.

## Production files

Python production changes:

- `python/src/ksdft2effmass/harness/pi/local/task_model.py` — 19 interfaces and hardened algorithms;
- `python/src/ksdft2effmass/harness/pi/local/__init__.py` — accepted public exports; and
- `python/src/ksdft2effmass/harness/pi/local/adapters.py` — version-2 dispatch while retaining version-1 and Markdown behavior.

Project-local resource changes:

- `harness/local/schemas/task-record-v2.schema.json`;
- `harness/local/projections/harness-task-documentation-v2.json`;
- `harness/local/fixtures/task-record-v2/` — 2 valid and 26 invalid fixtures plus index;
- `harness/local/fixtures/oracle-index.json`;
- `harness/local/resource-manifest.json`; and
- `harness/local/profiles/ksdft2effmass-v2.json`.

Maintained public documentation:

- `docs/api/harness-task.rst`;
- `docs/api/index.rst`; and
- `docs/harness/ksdft2effmass.harness.002.001.012.md`.

## Final public API

| Kind | Interfaces |
|---|---|
| Serialized DataObject | `HarnessTask` |
| Runtime DataObjects and ResultObjects | `HarnessTaskDocumentSource`, `HarnessTaskSourceMapping`, `HarnessTaskDocumentationContent`, `HarnessTaskProjectionProfile`, `HarnessTaskDocumentation`, `HarnessTaskDocumentationComparisonResult`, `HarnessTaskMigrationReviewPacketRequest`, `HarnessTaskMigrationReviewPacket`, `HarnessTaskMigrationFileDisposition` |
| Closed enums | `HarnessTaskSourceDisposition`, `HarnessTaskMigrationDisposition` |
| Stateless ActionObjects | `HarnessTaskSerializer`, `HarnessTaskDeserializer`, `HarnessTaskGraphValidator`, `HarnessTaskDocumentationRenderer`, `HarnessTaskDocumentationComparator`, `HarnessTaskMigrationReviewPacketPreparer`, `HarnessTaskMigrationFileDispositionRecorder` |

Only `HarnessTask` is serialized. No generic `WireRecordKind`, persistence, database, selection-state, or chain-cutover API was added.

## Differences from the accepted Stage-1 contract

None. The implementation preserves all accepted fields, field order, signatures, ownership boundaries, runtime-only boundaries, and wire behavior.

Stage-2A resolved only the explicitly deferred hardening details:

- exact lexical `PIHL.TASK.*` code ordering;
- strict project-local Identifier grammar;
- ResourcePath schema/runtime fixture partition;
- base64 storage of the sole authoritative template bytes;
- exact template token grammar and final-LF behavior;
- byte-opcode, coverage, insertion, and documentation-block comparison rules; and
- complete packet and disposition compatibility checks.

These decisions are documented in `hardening-decisions.md`.

## Representative non-migration example

Status: Illustrative example and synthetic test data only.

Retained identities:

- source Markdown: `40ada86450912593bb5554de6b6536011eadce13eaa103ecfe4754846d088fd9`;
- canonical HarnessTask JSON: `ea9e3d602c9946341df3697f2419fa8fb87eeaced339db1dd4ab3abfe8f49e1d`;
- rendered Markdown: `22ee50b56de9b6c01d7a7ce9679bc889d9446ac1b3d3643adfc9a317c8d783cd`; and
- template bytes: `c064215ba47c0275df3567933511ec5d2aab50d2974c85d9fcde6b2d3f58077c`.

The exact comparison status is `MAPPED_DIFFERENCES`; the only opcode is:

```text
insert:source[0:0]->rendered[0:158]
```

There are no unmapped spans, and the source paragraph—including code, mathematics, and literal braces—is preserved exactly. The full source, canonical JSON, rendering, manifest, and unified diff are under `representative-example/`. This is not a packet for any of the six selected Tasks.

## Verification and review

- Focused final set: 74 passed.
- Broad suite: 2,922 passed, 2 deselected unavailable-pip wheel cases.
- Ruff, focused mypy, resource validation, evidence conformance, Sphinx warnings-as-errors, and whitespace checks: passed.
- Repository evidence gate: 241 modules, 2,924 collected nodes, zero findings.
- Independent review: original result failed with two high, one medium, and one low finding.
- Correction: all four findings were accepted and corrected in the single authorized pass; deterministic final verification passed.

The original review is retained in `integration-review.md`; dispositions and checks are retained in `review-correction.md` and `validation.md`.

## Known limitations

- Byte-structural `MAPPED_DIFFERENCES` does not establish semantic correctness or human acceptance.
- No selected Task has been converted, rendered, dispositioned, or migrated.
- The chain remains operational authority; selection state and cutover remain unauthorized.
- The virtual environment lacks `pip`, so two unrelated offline wheel tests could not execute. No dependency or environment change was authorized.
- Passing tests establish software verification only, not scientific validation.

## Unchanged authority and Stage-2B boundary

All six authoritative Markdown Tasks remain byte-identical at their accepted SHA-256 identities and total 20,074 bytes. No proposed `docs/harness/ksdft2effmass.harness.002.002.*` migration destination was created.

If Stage 2A is explicitly human-accepted, it may be completed. Stage 2B must still remain inactive until a separate activation checkpoint is created and explicitly approved. Only then may exactly one real file packet be prepared. Automatic successor activation remains false.
