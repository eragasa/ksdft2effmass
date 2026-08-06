# P2 test-evidence migration implementation

## Invocation identity

- Request/task: P2-HC02 Option-B / `P2`
- Parent workflow: `backend-neutral-kohn-sham-qe`
- Migration attempt: `P2-TEST-EVIDENCE-MIGRATION-1`
- Consolidated correction: `P2-TEST-EVIDENCE-MIGRATION-1-CORRECTION-1`
- Profile: `AUTHORIZED_TEST_EVIDENCE_WRITE`
- Skill: `harness/pi/skills/develop-python-test-evidence/SKILL.md`
- Review input: `.pi-subagents/artifacts/4419c4f1_ksdft2effmass.ksdft2effmass-integration-reviewer_0_output.md`
- Evidence class: software verification only
- Ownership: seven `class_owned` modules and one `artifact_owned` module, exactly as recorded in `test-evidence-ownership.json`

## Corrected migration result

The sole consolidated post-review correction separates semantic `TypeError` boundaries from malformed-value/grammar `ValueError` boundaries and separates lifecycle presence, timestamp grammar/order, valid terminal construction, direct self-parenting, and enum semantic typing where their requirements differ. Repeated independent assertions were removed from parameter nodes and placed under their own evidence owners. `SV-PROV-097` now documents only timestamp semantic-type rejection; equality remains solely `SV-PROV-112`.

Artifact fixture evidence now retains `SV-PROV-067` for schema validation and uses `SV-PROV-135` for strict runtime deserialization and `SV-PROV-136` for canonical serialization/round-trip text. The active NFC predicate is the visible, seven-field, ID-free `is_nfc_text` helper supporting `SV-PROV-067`.

The review request to split the four `ArtifactReference` properties is inapplicable under the explicit higher-authority correction instruction. `test_property__nested_field_delegation__returns_exact_views` remains one authorized cohesive delegation-map requirement with one method shape, nested-state oracle, tuple acceptance rule, and failure interpretation.

All 50 historical evidence IDs and pre-correction `SV-PROV-104` through `SV-PROV-113` are retained. New independent owners use `SV-PROV-114` through `SV-PROV-142`; individual rationales are recorded in `test-evidence-inventory.json`. Valid-path acceptance, impossible start/finish calendar checks, and fixture-family membership/inventory checks are also separated so parameter nodes do not repeat independent assertions.

## Identity and count reconciliation

- Historical input: 50 test functions, 2 helpers, 50 evidence owners, 90 collected nodes.
- Reviewed pre-correction state: 60 test functions, 2 helpers, 60 evidence owners, 278 collected nodes.
- Corrected state: 89 test functions, 3 helpers, 89 evidence owners, 373 collected nodes.
- Ownership: 7 class-owned modules and 1 artifact-owned module; all 8 are software verification.
- Historical-to-corrected migration: closed one-to-one 90-to-90 map; 13 unchanged node IDs and 77 unique replacements.
- Reviewed-current-to-corrected transition: closed one-to-one 278-to-278 retained/replacement map; 113 unchanged and 165 replacements. The 95 genuinely new corrected nodes have no current predecessor.
- Complete historical, reviewed-current, and corrected node identities and both transition partitions are recorded in `test-evidence-inventory.json`. The validator-facing closed historical map remains `test-evidence-node-migration.json`.
- Structural static parameter accounting reports 323 cases because stacked pytest decorators collect Cartesian products; complete pytest collection is the authoritative 373-node inventory.

## Validation

- P2 ownership preflight: PASS.
- Accepted structural validator on exactly eight paths with ownership and historical migration input: PASS; 8 modules, 89 tests, 3 helpers, 89 evidence owners, zero findings.
- Complete collection inspection: PASS; 373 nodes.
- Seven class-owned modules: PASS, 238 cases.
- Artifact-owned fixture/runtime module: PASS, 135 cases.
- Focused P2 provenance suite with branch coverage: PASS, 415 cases; `records.py` 97% coverage (352 statements, 8 missed; 264 branches, 8 partial).
- Ruff format and lint on the eight paths: PASS.
- mypy over source, provenance tests, and artifact module: PASS, 67 source files.
- P2 completion and checkpoint validators: PASS; zero issues and zero unresolved checkpoints.
- H3 resource, skill-capability, and maintained local-route validators: PASS (58 gates/0 defects, 0 capability errors, selected local route PASS).
- Production `records.py` and public provenance schema SHA-256 values match `HEAD`; dependencies and locks have no diff; staging is empty; `git diff --check` passes.

## Scope and residual boundary

Exactly the same twelve authorized paths were modified. Production source, public behavior, schema, fixtures, dependencies, locks, control records, and unrelated work remain unchanged. No production defect was observed. Passing synthetic nonnumerical evidence does not establish numerical verification, scientific validation, UQ, physical correctness, external execution, cross-language conformance, release readiness, or human acceptance.

This correction pass is consumed. Independent confirmation of the corrected result and renewed P2-HC03 human acceptance remain separate gates; no further writer/reviewer loop is authorized here.
