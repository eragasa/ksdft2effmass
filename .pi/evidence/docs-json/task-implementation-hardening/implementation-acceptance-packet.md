# HarnessTask Stage-2A implementation-acceptance packet

Decision requested: Accept, request bounded correction, or defer the corrected Stage-2A implementation. This packet does not activate Stage 2B or accept any file migration.

The human is being asked to accept the exact 16-field/21-interface implementation: the original 19 interfaces plus the explicitly recorded runtime-only review document and renderer. The boundary also includes complete source/target binding, generic-decision revalidation, the earlier committed-tree syntax correction, focused regression evidence, and the manually supplied representative example. Test counts, mapped differences, and review agreement do not themselves establish acceptance.

## Outcome

The accepted schema-version-2 `HarnessTask` wire contract remains unchanged. The corrected project-local surface has 21 public interfaces: the original 19 plus `HarnessTaskMigrationReviewDocument` and `HarnessTaskMigrationReviewPacketRenderer`. Canonical JSON, strict decoding, structural graph validation, explicit documentation rendering, byte-structural comparison, exact migration-review preparation, deterministic complete human-readable packet rendering, generic-decision revalidation, disposition recording, v1/v2/Markdown compatibility, resources, documentation, and maintained software-verification evidence are present.

The earlier bounded correction changed the evidence-identifier syntax and initial packet binding. This architectural correction adds the two review-rendering interfaces, complete source and target binding, generic-decision revalidation, exact presentation evidence, synchronized API/control documentation, and a renewed pending checkpoint. The exact current changed-path list is retained in `human-review-boundary-validation.md`; the earlier list remains historical in `bounded-correction-validation.md`.

## Production files

Python production changes:

- `python/src/ksdft2effmass/harness/pi/local/task_model.py` — corrected 21-interface implementation and hardened algorithms;
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
| Runtime DataObjects and ResultObjects | `HarnessTaskDocumentSource`, `HarnessTaskSourceMapping`, `HarnessTaskDocumentationContent`, `HarnessTaskProjectionProfile`, `HarnessTaskDocumentation`, `HarnessTaskDocumentationComparisonResult`, `HarnessTaskMigrationReviewPacketRequest`, `HarnessTaskMigrationReviewPacket`, `HarnessTaskMigrationReviewDocument`, `HarnessTaskMigrationFileDisposition` |
| Closed enums | `HarnessTaskSourceDisposition`, `HarnessTaskMigrationDisposition` |
| Stateless ActionObjects | `HarnessTaskSerializer`, `HarnessTaskDeserializer`, `HarnessTaskGraphValidator`, `HarnessTaskDocumentationRenderer`, `HarnessTaskDocumentationComparator`, `HarnessTaskMigrationReviewPacketPreparer`, `HarnessTaskMigrationReviewPacketRenderer`, `HarnessTaskMigrationFileDispositionRecorder` |

Only `HarnessTask` is serialized. No generic `WireRecordKind`, persistence, database, selection-state, or chain-cutover API was added.

## Differences from the accepted Stage-1 contract

One narrow correction is explicit: two runtime-only public interfaces were added, increasing the project-local HarnessTask inventory from 19 to 21. `HarnessTaskMigrationReviewDocument` owns exact human-readable Markdown bytes, a derived path, and SHA-256 identity. `HarnessTaskMigrationReviewPacketRenderer` revalidates a structured packet and deterministically renders its complete before/after review view. The 16-field wire record, original 19 signatures, serialized behavior, and ownership boundaries remain unchanged.

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

## Representative human-review document

The retained synthetic exact-byte oracle is `python/tests/software_verification/ksdft2effmass/harness/pi/local/fixtures/harness-task-migration-review.md`. It directly includes the complete original Markdown, complete canonical JSON, complete candidate documentation, mapping table, comparison and diff, opaque-block result, rollback identity, limitations, and four choices. Its opening demonstrates the human-facing target and provenance boundary:

```text
# HarnessTask migration review: `example.task`

## Review target
- Review ID: `harness-task-migration.example.task`
- Evidence class: `software_verification`
- Source revision: `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`

## Source provenance and rollback identity
- Path: `records/example-source.md`
- Git object: `bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb`
- Byte count: `24`
- SHA-256: `3715d0dba7b70a3f0748951baf83a4ee6b796487d63897fc4ecd37433d17f4d8`
```

The document identity is `9a9caa947a592f2a9636ff5eee9a3829ffab5794d1b818c228cc58ea774b1e10`. It is a runtime review view, not operational authority or a migration disposition.

## Verification and review

The original Stage-2A independent review remains retained: it failed with two high, one medium, and one low finding; all four were accepted and corrected in the one original authorized correction pass. No additional reviewer session or replay loop was launched for either bounded correction, consistent with the instruction not to use another session.

The current human-review-boundary checks and clean committed-tree source-path proof are retained in `human-review-boundary-validation.md`; the earlier correction remains historical in `bounded-correction-validation.md`. The focused Stage-2A set now includes independent negative partitions for every required packet-binding element and direct inconsistent-packet disposition. Maintained evidence conformance now records 243 modules and 2,969 collected nodes. Counts establish only the declared software checks.

The prior `2,922 passed` claim did not expose the unparenthesized exception lists because the tests ran under Python 3.14, whose grammar accepts that PEP 758 form. Durable evidence did not retain a clean-checkout import-path proof, so the old wording was not a reproducible committed-tree claim. Investigation found no alternate installed package or unimported-module boundary: the editable environment resolves `ksdft2effmass` to `python/src`, and maintained tests import `ksdft2effmass.harness.pi.evidence.identifiers` directly. The syntax predated revision `a577ebb`, so a different nearby revision does not explain the result. The corrected tuple form is now retained and the resulting commit is validated from an isolated checkout with its imported package path printed.

## Known limitations

- Byte-structural `MAPPED_DIFFERENCES` does not establish semantic correctness or human acceptance.
- No selected Task has been converted, rendered, dispositioned, or migrated.
- The chain remains operational authority; selection state and cutover remain unauthorized.
- The virtual environment lacks `pip`, so two unrelated offline wheel tests could not execute. No dependency or environment change was authorized.
- The package requires Python 3.14; the former unparenthesized exception-list form was accepted by that interpreter even though it obscured reproducible syntax review. The explicit tuple form is retained with a formatter-suppression comment because Ruff targeting Python 3.14 otherwise rewrites it to the PEP 758 form.
- The generic observation detail is deterministic canonical JSON text validated against exact immutable observations; it is runtime-only and does not change the 16-field HarnessTask wire contract.
- Human-review rendering requires source and candidate documentation bytes to be valid UTF-8 and fails closed otherwise; the internal structured packet remains byte-oriented.
- The rendered document is reproducible presentation only. It does not replace the structured packet or recorded disposition as authority.
- Passing tests establish software verification only, not scientific validation.

## Unchanged authority and Stage-2B boundary

All six authoritative Markdown Tasks remain byte-identical at their accepted SHA-256 identities and total 20,074 bytes. No proposed `docs/harness/ksdft2effmass.harness.002.002.*` migration destination was created.

If the corrected Stage 2A is explicitly human-accepted at `.pi/checkpoints/harness.simplification.docs-json.task-implementation-hardening.human-review-boundary-acceptance.json`, it may be completed. Stage 2B must still remain inactive until a separate activation checkpoint is created and explicitly approved. Only then may exactly one real file packet be prepared. Automatic successor activation remains false.
