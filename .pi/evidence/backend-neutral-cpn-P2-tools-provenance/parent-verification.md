# P2 parent verification

Status: **PASS_WITH_RECORDED_BASELINE_AND_REPLAY_LIMITATIONS**

The root PI agent verified the corrected P2 boundary after one consolidated review/correction cycle. P2 is software-verification work only. No external tool, QE, Wannier90, scheduler, scientific calculation, numerical-verification protocol, scientific-validation protocol, or UQ protocol was executed.

## Current boundary

- Public package: `python/src/ksdft2effmass/provenance/` (32 sorted exports).
- Shared wire contract: `specification/provenance/v1/provenance-v1.schema.json` with 17 valid and 26 invalid strict fixtures.
- Evidence: 24 class-owned modules and five named artifact-owned integration modules.
- Documentation: public API, concepts, lifecycle, user-guide, and software-verification pages.
- Dependency direction: provenance imports no CPN, SNAKES, harness, backend, scheduler, subprocess, or mutable-client package.

## Validation

- Focused P2 software verification: PASS (77 tests in the observed run; counts are observation only, not acceptance semantics).
- P2 source/test Ruff and formatting: PASS.
- P2 source/test mypy: PASS.
- P2 completion validator: PASS, count-independent semantic conditions.
- Draft 2020-12 schema compilation, valid fixtures, invalid fixtures, canonical round trips, Python/schema enums, and strict JSON: PASS through focused artifact evidence.
- Sphinx warnings-as-errors: PASS.
- Wheel build, content inspection, clean no-dependency installation, and isolated import: PASS.
- Repository Ruff: PASS.
- Repository full pytest: 1196 passed and 12 failed. The exact 12 failures are the pre-existing H4 local-harness failures reproduced at starting revision `fb43f32307d326396ac095dd58011c16861d0d82` (starting observation: 1119 passed and the same 12 failed). No P2 test failed.
- Repository full mypy: the same nine pre-existing H2/H4 harness-test annotation errors recorded at the accepted H4 boundary; affected P2 mypy passes.
- Maintained local harness consumer: PASS after restoring the H4 checksum-protected historical `docs/verification/cpn-contract.rst` bytes.
- Checkpoint, task-ownership, package-lock parse, dependency/lockfile diff, `git diff --check`, and unrelated-work preservation checks: PASS.

## Review and bounded correction

The one consolidated reviewer returned FAIL and identified credential-bearing raw text channels, runtime/schema mismatches, cross-module private validators, stale maintained status text, and enum/source-documentation issues. One consolidated implementation/test/documentation correction removed raw channels, added attempt/retry correlation, added calendar validation, derived relational statuses, made validators owner-local, adopted documented `StrEnum`, synchronized schema/fixtures/tests/docs, and updated unprotected maintained status pages.

The targeted closure review found one remaining single-backslash diagnostic-path defect and an R2 scope-label/inventory limitation. Root integration deterministically corrected and tested the backslash defect without starting another writer/reviewer cycle. The checksum-protected H4 CPN verification page was restored rather than rewriting historical H4 identity. The R2 inventory limitation remains recorded below.

## Replay boundary

- P2-R1/E1: one ordinary replay before review.
- P2-R2/E2: the single permitted replacement replay after material correction; PASS against its immutable input catalog.
- No third replay was performed. The final root single-backslash correction and some ancillary corrected status/catalog documentation are therefore validated by the final deterministic checks but are not bound into R2. R1 and R2 remain historical and were not rewritten.

This replay limitation and the pre-existing repository-wide H4 pytest/mypy failures are disclosed to the human acceptance checkpoint. They do not alter the focused P2 software-verification result, but the human PI may defer acceptance if exact final-boundary replay identity is required.
