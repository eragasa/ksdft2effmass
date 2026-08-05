# P2 post-R2 bounded-correction parent verification

Status: **PASS_PENDING_RENEWED_HUMAN_ACCEPTANCE**

This current-boundary verification covers the human-authorized Option-B correction only. It is software-verification evidence, not numerical verification, scientific validation, uncertainty quantification, cross-language conformance, external execution, publication, or release evidence.

## Implemented boundary

- Removed `_require_text`, `_require_identifier`, `_require_sha256`, `_require_root_relative_path`, and `_require_identifier_tuple` from `records.py`.
- Retained only immutable constants and compiled regular expressions as shared module implementation objects.
- Moved intrinsic validation visibly into the seven owning records.
- Added direct `RunManifest` self-dependency rejection.
- Preserved reference/location separation, public exports, serialization compatibility, and TypeError/ValueError behavior.
- Preserved nonempty `output_artifact_ids` for `DECLARED` as preallocated expected identities, supported by the accepted architecture statement that manifests use opaque preallocated identities; documentation states that this does not assert observed bytes or terminal completion.
- Added `SV-PROV-080` through `SV-PROV-103` without renumbering existing evidence.
- Added a schema-valid but runtime-invalid direct-self-dependency fixture and strict-deserializer evidence.

## Deterministic validation

- Seven class-owned modules: **85 passed**.
- Schema/fixture/runtime agreement modules: **8 passed**.
- Focused P2 provenance tests excluding wheel: **140 passed**.
- Wheel build/content/isolated import in the declared root project environment: **1 passed**.
- Combined seven classes plus fixture integration after final test correction: **90 passed**.
- P2 Ruff formatting and lint: PASS.
- P2 mypy: PASS for 35 source files.
- Sphinx warnings-as-errors: PASS for 45 sources; output was written outside the repository and removed.
- P2 completion validator, task-ownership validator, checkpoint validator, maintained local harness route, skill-capability validator, and H3 resource validator: PASS.
- JSON parse, dependency/lockfile nonmutation, protected provenance-module nonmutation, `git diff --check`, and unrelated-work preservation checks: PASS.

## Branch-coverage diagnostic

`records.py` branch coverage was **97%**: 352 statements, eight missed statements, 264 branches, and eight partial branches. The remaining unexecuted branches are the SHA-256 surrogate and non-NFC rejection paths and the empty, surrogate, and non-NFC rejection paths for `started_at` and `finished_at`. These are defensive partitions of the same accepted scalar-Unicode contract; identifier/path surrogate and NFC behavior, SHA-256 syntax/type behavior, and malformed/impossible/chronological timestamp behavior are directly exercised. Branch coverage is diagnostic and no fixed percentage gate applies.

## Review and replay boundary

The single targeted review confirmed the substantive implementation, test, schema/runtime, declared-output, compatibility, and scope requirements. Its heading finding was overridden by the current human instruction; its missing-`Raises` finding was corrected in the one permitted small pass and deterministically revalidated. No repeated general review cycle was started.

R1 and R2 remain immutable historical evidence. No R3/E3 exists. P2 remains open pending renewed human acceptance at `P2-HC02`.
