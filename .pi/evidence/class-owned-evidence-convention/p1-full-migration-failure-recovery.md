# P1 full-migration aborted-attempt recovery

## Failure

The first `EVIDENCE-DOC-1-HC02` full-P1 test-writer attempt generated a bulk text-offset rewrite for 37 evidence modules and `conftest.py`. Its compile probe found:

- helper docstrings inserted at incorrect indentation in `conftest.py`, `test__FiringResult.py`, and `test__TokenTemplate.py`;
- `ARTIFACT_OWNER` inserted before `from __future__ import annotations` in four integration modules.

The shell command continued to a successful `git diff --stat`, masking the compile failures as the tool call's final status. The child then ended without a final result. No deterministic test or ownership pass was produced by that attempt.

## Recovery

The partial bulk rewrite was removed only from the exact manifest-owned P1 test paths. The previously validated `CpnToken` and `FiringRequest` migrations were restored, and current manifest targets were reconstructed from `p1-pre-full-migration-baseline.json`. No production, schema, fixture, dependency, numerical-tolerance, checkpoint-decision, or unrelated user path was reverted.

Post-recovery checks:

- Python compilation of all 37 P1 evidence modules and `conftest.py`: pass;
- P1 ownership validator: 32 class modules, five artifact modules, 49 exports, 88 IDs: pass;
- focused `CpnToken` plus `FiringRequest`: 12 passed;
- unified bounded validator: two migrated modules, 12 tests/IDs/node mappings, 96 inventoried modules: pass;
- `git diff --check`: pass.

## Successful bounded retry and follow-up

The test writer subsequently completed all 32 class-owned modules in the CPN
workflow test directory plus the declared helpers, preserving the 78 evidence
identities. The implementation/control-plane follow-up replaced pilot-only
structural enforcement with mandatory complete-directory checks and consolidated
the 78 function-node renames in
`cpn-complete-directory-node-id-map.json`. The preserved baseline and the two
pilot maps remain available for traceability.

This recovery records successful deterministic structure and traceability only.
It does not claim semantic review, scientific validation, uncertainty
quantification, or human final acceptance.

## Retry constraint

Do not repeat the monolithic text-offset transformation. Any correction remains
bounded to a consolidated authorized cycle, must preserve the pre-migration
baseline, and must compile and structurally validate before review.
