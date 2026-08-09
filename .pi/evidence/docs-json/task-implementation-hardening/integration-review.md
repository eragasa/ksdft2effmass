# Stage-2A consolidated independent review

**Result:** Material findings remain. Stage 2A is **not ready for implementation acceptance**. This review does not activate Stage 2B or accept any migration.

## Findings

1. **High — Required behavioral evidence is materially incomplete.**
   All 19 class-owned modules primarily verify only class identity, fields, enum vocabulary, or fieldlessness. Examples:
   - `python/tests/software_verification/ksdft2effmass/harness/pi/local/test__HarnessTask.py:28-46`
   - `python/tests/software_verification/ksdft2effmass/harness/pi/local/test__HarnessTaskDeserializer.py:26-44`
   - `python/tests/software_verification/ksdft2effmass/harness/pi/local/test__HarnessTaskGraphValidator.py:26-44`
   - `python/tests/software_verification/ksdft2effmass/harness/pi/local/test__HarnessTaskMigrationReviewPacketPreparer.py:26-44`

   The artifact-owned test covers selected integrations, but does not exhaust the accepted obligations for intrinsic type/value boundaries, nested immutability, BOM/invalid-UTF-8/key-closure partitions, source byte-count/Git-object/span identities, comparison-result invariants, or packet one-field disagreement checks. For example, searches across the maintained Stage-2A tests found no behavioral cases for `byte_count`, `git_object`, `span_identity`, BOM, or invalid UTF-8.

   **Correction:** Add focused behavioral evidence to the owning class modules for their intrinsic/public contracts. Retain cross-object agreement in the artifact-owned module. Update ownership and conformance inventories deterministically.

2. **High — Mixed-format and `TaskStateInspector` compatibility claims lack Stage-2A evidence.**
   The only new v2 adapter case supplies one v2 JSON Task:
   - `python/tests/software_verification/ksdft2effmass/harness/pi/local/test__harness_task_contract_v2.py:489-529`

   It does not exercise one chain containing v1 JSON, v2 JSON, and Markdown together. Existing inspector command evidence constructs only a Markdown Task:
   - `python/tests/software_verification/ksdft2effmass/harness/pi/local/test__inspect_task_state_command_api_agreement.py:55-96`

   Consequently, the compatibility claim in `docs/api/harness-task.rst:68-71` is not directly verified for inspector behavior across all three formats.

   **Correction:** Add artifact-owned cases using explicit controlled inputs for:
   - mixed v1 JSON + v2 JSON + Markdown adaptation in one chain; and
   - direct `TaskStateInspector` results for equivalent Markdown, v1 JSON, and v2 JSON records, including identity/status disagreement failures.

3. **Medium — Maintained mypy gate fails.**
   `python/tests/software_verification/ksdft2effmass/harness/pi/local/test__harness_task_contract_v2.py:28` imports untyped `jsonschema` without the established suppression. Focused mypy reports `import-untyped`.

   **Correction:** Use the repository-established `# type: ignore[import-untyped]` annotation, then rerun maintained mypy.

4. **Low — Accepted public field annotation is transcribed inconsistently.**
   The accepted contract specifies `HarnessTaskDocumentationComparisonResult.status: Identifier`, while implementation declares:
   - `python/src/ksdft2effmass/harness/pi/local/task_model.py:819` — `status: str`

   The aliases have identical runtime representation, so behavior is unaffected, but the public typing surface is not an exact transcription.

   **Correction:** Annotate the field as `Identifier` and add an annotation/field-contract assertion.

## Confirmed conforming points

- The public surface exports the accepted 19 project-local interfaces; generic code remains independent of local code.
- `HarnessTask` retains the accepted 16-field order and schema version 2.
- Serializer/deserializer implementation follows the accepted canonical JSON and strict decoding boundaries.
- Graph codes and lexical `(code, path, detail)` ordering agree with maintained hardening documentation.
- Template parsing uses explicit authoritative bytes and preserves inserted opaque bytes without reparsing.
- Comparator claims remain byte-structural and explicitly disclaim semantic or human acceptance.
- Packet preparation and disposition routing retain generic human-review ownership and prohibit persistence/activation.
- Resource manifests, fixture index, hashes, overlay direction, and dependency closure pass the maintained resource validator.
- Representative example identities match its retained source, canonical Task JSON, and rendered Markdown bytes; it is labeled synthetic/non-migration.
- The six authoritative Markdown Tasks remain unchanged: all SHA-256 values and the total `20,074` bytes match the accepted source inventory.
- Sphinx builds successfully with warnings treated as errors.
- No staged files were present, and this review changed no repository files.

## Residual risks

- Passing tests and validators establish software verification only.
- Full repository pytest was not rerun; validation was focused on affected harness surfaces.
- Behavioral gaps above prevent reliance on the current maintained evidence as complete Stage-2A acceptance evidence.
- The working tree remains uncommitted and may change after this review.
