# TEST-EVIDENCE-SKILL-1 post-review correction evidence

## Independent-review correction

The single authorized correction pass resolves all three High findings:

1. Current root `AGENTS.md` now assigns maintained test-evidence grammar to `.pi/skills/develop-python-test-evidence/references/test-evidence-conventions.md`; a current-consumer search finds no deleted documentation-skill reference outside the intentional retirement check.
2. `validate_python_test_evidence.py` now parses ownership and migration inputs totally and fail-closed. Null/malformed JSON, non-object entries, missing/non-string paths, unexpected keys, duplicate paths, invalid modes/classes/SUTs/artifacts, and malformed maps always emit structured JSON findings without traceback.
3. Controlled fixtures now cover valid class/artifact owners; maintained/superseded headings; semantic/evidence-qualified and ordinal/raw/missing parameter IDs; semantic/invalid helpers and no-ID declarations; duplicate IDs across modules; known/unknown static collection counts; malformed ownership; and valid, duplicate, incomplete, and unexpected-key migration inputs. Migration completeness compares explicit expected old/new inventories with exact one-to-one mapping sets.

The canonical/live skill and complete reference remain byte-identical. Generic examples remain project-neutral. The current local route uses the manifest-owned current replay and passes without reading immutable H4 catalogs. The legacy rollback identity remains retained, but immutable historical H4 replay cannot be restored to current retired-path compatibility without either restoring the competing old grammar or rewriting historical catalogs; both are prohibited.

## Exact controlled evidence

- Valid class: PASS; class-owned=1, tests=1, helpers=0, static cases=1, unique owners=1.
- Valid artifact: PASS; artifact-owned=1, tests=1, helpers=1, static cases=2, unique owners=1.
- Invalid grammar: expected FAIL with exact multiset including three `TE.PARAMETER_ID`, two superseded headings, helper/name/no-ID documentation, loop, opening, filename, and semantic-name findings.
- Duplicate modules: expected one `TE.DUPLICATE_ID`; 2 tests and 1 unique evidence owner.
- Dynamic parameter source: expected `TE.PARAMETER_ID` and `static_collected_parameter_cases=null`.
- Thirteen ownership cases assert exact structured code multisets for invalid JSON, null input, missing/null/numeric paths, entry shape, duplicate path, mode, evidence class, SUT, artifact, and unexpected keys.
- Migration cases: valid PASS; invalid JSON and unexpected keys produce `TE.MIGRATION_INPUT`; duplicate produces `TE.MIGRATION_ONE_TO_ONE` plus `TE.MIGRATION_INCOMPLETE`; incomplete produces `TE.MIGRATION_INCOMPLETE`.
- Task completion validator invokes all 23 controlled cases and compares exact exit/status, finding-code multisets, required count fields, and case-specific count values.

## Validation results

- Ownership preflight: PASS.
- Controlled completion suite: PASS, zero issues.
- Read-only forward diagnostic: expected FAIL with 88 findings over 8 class-owned modules, 50 tests, 4 helpers, 12 parameterized functions, 52 static parameter cases, and 50 unique evidence owners; class counts remain 7 software and 1 numerical verification.
- Selected local route: PASS with `selected_route=local`, `rollback_route=legacy`, current H3 and seven-skill checks both PASS.
- H3 resources: PASS, 58 gates, zero defects.
- Skill capabilities: PASS, 7 skills and zero errors.
- Root-environment Ruff over the affected validators/replay: PASS (`All checks passed!`) after making both shebang scripts executable, replacing both `re.I` aliases with `re.IGNORECASE`, and flattening artifact ownership validation without behavior change. Ruff formatting was then applied to exactly the four affected Python files; `ruff format --check` reports `4 files already formatted`. The local replay manifest SHA-256 was refreshed after formatting.
- Canonical/live comparison, JSON parsing, Python compilation, link check, Sphinx warnings-as-errors, diff check, protected nonmutation, and no-staged-files checks: PASS.

## Boundaries and residuals

No raw P2 source/tests/schema/fixtures, checkpoint/task/chain record, immutable H4 evidence/catalog, dependency, lock, or unrelated user file was changed. Forward debt remains diagnostic. Structural validation cannot establish semantic surface/cohesion, oracle independence, mathematics, tolerance adequacy, scientific validation, UQ, or human acceptance. No second review is requested; final acceptance remains human-owned.
