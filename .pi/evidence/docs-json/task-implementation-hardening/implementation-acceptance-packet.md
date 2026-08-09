# HarnessTask Stage-2A implementation-acceptance packet

Decision requested: Accept, request bounded correction, or defer the corrected Stage-2A implementation. This packet does not activate Stage 2B or accept any file migration.

The human is being asked to accept the exact 16-field/19-interface implementation together with the bounded committed-tree syntax correction, deterministic review-packet evidence binding, disposition-time revalidation, focused regression evidence, and the explicitly relabeled manually supplied representative example. Test counts, mapped differences, and review agreement do not themselves establish acceptance.

## Outcome

The accepted schema-version-2 `HarnessTask` contract is implemented as 19 project-local public interfaces. Canonical JSON, strict decoding, structural graph validation, explicit rendering, byte-structural comparison, migration-review packet preparation, exact disposition recording, v1/v2/Markdown compatibility, resources, documentation, and maintained software-verification evidence are present.

The bounded correction also changes `python/src/ksdft2effmass/harness/pi/evidence/identifiers.py`, the packet-preparer and disposition-recorder evidence modules and their synthetic constructor, maintained conformance inventory, this packet and correction evidence, representative artifacts, Stage-2A API/control documentation, the Stage-2A Task and chain state, the resolved prior checkpoint, and the renewed pending checkpoint. The exact changed-path list is retained in `bounded-correction-validation.md`.

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

Status: Illustrative example and synthetic test data only. The `HarnessTask` is manually supplied. No Markdown parser or Markdown-to-`HarnessTask` extraction is implemented or demonstrated.

The example keeps these transformations distinct:

1. a manually supplied `HarnessTask` is serialized to canonical JSON;
2. that `HarnessTask`, exact documentation content, and an explicit projection profile produce rendered Markdown; and
3. source Markdown, rendered Markdown, and accepted mappings produce an exact byte-structural comparison.

Retained identities:

- source Markdown: `40ada86450912593bb5554de6b6536011eadce13eaa103ecfe4754846d088fd9`;
- canonical HarnessTask JSON: `4f660787561789952d49df747e0fcdbe0fe1a9faf7e0aa9b51e566e5cfdc3bfc`;
- rendered Markdown: `a404ce5c5c0d75df3dedc600193461137f00fce7c867e246567fa96f5eaf872a`; and
- template bytes: `c064215ba47c0275df3567933511ec5d2aab50d2974c85d9fcde6b2d3f58077c`.

The exact comparison status is `MAPPED_DIFFERENCES`; the only opcode is:

```text
insert:source[0:0]->rendered[0:183]
```

There are no unmapped spans, and the source paragraph—including code, mathematics, and literal braces—is preserved exactly. The full source, canonical JSON, rendering, manifest, and unified diff are under `representative-example/`. This is not a packet for any of the six selected Tasks and makes no claim about extraction provenance for candidate Task fields.

## Verification and review

The original Stage-2A independent review remains retained: it failed with two high, one medium, and one low finding; all four were accepted and corrected in the one original authorized correction pass. No additional reviewer session or replay loop was launched for this bounded correction, consistent with the current instruction not to use another session.

Current-boundary checks and the clean committed-tree source-path proof are retained in `bounded-correction-validation.md`. The focused Stage-2A set now includes independent negative partitions for every required packet-binding element and direct inconsistent-packet disposition. Maintained evidence conformance now records 241 modules and 2,937 collected nodes. Counts establish only the declared software checks.

The prior `2,922 passed` claim did not expose the unparenthesized exception lists because the tests ran under Python 3.14, whose grammar accepts that PEP 758 form. Durable evidence did not retain a clean-checkout import-path proof, so the old wording was not a reproducible committed-tree claim. Investigation found no alternate installed package or unimported-module boundary: the editable environment resolves `ksdft2effmass` to `python/src`, and maintained tests import `ksdft2effmass.harness.pi.evidence.identifiers` directly. The syntax predated revision `a577ebb`, so a different nearby revision does not explain the result. The corrected tuple form is now retained and the resulting commit is validated from an isolated checkout with its imported package path printed.

## Known limitations

- Byte-structural `MAPPED_DIFFERENCES` does not establish semantic correctness or human acceptance.
- No selected Task has been converted, rendered, dispositioned, or migrated.
- The chain remains operational authority; selection state and cutover remain unauthorized.
- The virtual environment lacks `pip`, so two unrelated offline wheel tests could not execute. No dependency or environment change was authorized.
- The package requires Python 3.14; the former unparenthesized exception-list form was accepted by that interpreter even though it obscured reproducible syntax review. The explicit tuple form is retained with a formatter-suppression comment because Ruff targeting Python 3.14 otherwise rewrites it to the PEP 758 form.
- The generic observation detail is deterministic canonical JSON text validated against exact immutable observations; it is runtime-only and does not change the 16-field HarnessTask wire contract.
- Passing tests establish software verification only, not scientific validation.

## Unchanged authority and Stage-2B boundary

All six authoritative Markdown Tasks remain byte-identical at their accepted SHA-256 identities and total 20,074 bytes. No proposed `docs/harness/ksdft2effmass.harness.002.002.*` migration destination was created.

If the corrected Stage 2A is explicitly human-accepted at `.pi/checkpoints/harness.simplification.docs-json.task-implementation-hardening.corrected-implementation-acceptance.json`, it may be completed. Stage 2B must still remain inactive until a separate activation checkpoint is created and explicitly approved. Only then may exactly one real file packet be prepared. Automatic successor activation remains false.
