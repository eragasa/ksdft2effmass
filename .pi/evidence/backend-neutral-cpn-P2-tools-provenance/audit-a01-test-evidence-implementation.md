# P2 A01 test-evidence implementation

## Skill and invocation identity

- Request: `P2-PROVENANCE-AUDIT-1-A01`
- Task: `P2`
- Parent workflow: `backend-neutral-kohn-sham-qe`
- Attempt: `a01-test-correction-1`
- Profile: `AUTHORIZED_TEST_EVIDENCE_WRITE`
- Skill content: `.pi/skills/develop-python-test-evidence/SKILL.md` and the complete `references/test-evidence-conventions.md`
- Authority input: `.pi/evidence/backend-neutral-cpn-P2-tools-provenance/task-ownership.json`
- Evidence class: software verification
- Ownership: four `class_owned` modules recorded exactly in `audit-a01-test-evidence-ownership.json`
- Production input: `python/src/ksdft2effmass/provenance/external_tools.py`, inspected read-only
- Stop policy: stop on invalid ownership, unauthorized mutation, incomplete historical mapping, a production defect, or a failed required final gate

## Semantic judgment

The malformed portable-identifier owner in each record module now covers every
identifier field independently across empty, embedded-space, non-NFC, surrogate,
and 129-character partitions. Each case has a field-and-partition semantic ID.
`requested_version` separately covers valid lengths 1 and 64 and seven rejected
partitions: empty, prohibited leading character, embedded space, embedded colon,
non-NFC text, a Unicode surrogate, and length 65. These cases directly apply the
accepted opaque grammar `[0-9A-Za-z][0-9A-Za-z._+-]{0,63}` without interpreting
version precedence.

Each record equality owner compares equal state and independently changes every
represented field to another valid value. Enum evidence retains exact vocabulary,
order, `StrEnum`, and alias checks while separating concrete class-call value
lookup from concrete class-subscription name lookup. Historical `SV-PROV-176`
owns value construction; new `SV-PROV-238` owns the distinct name-lookup
requirement. Historical invalid value and name owners retain `SV-PROV-177` and
`SV-PROV-178`. New `SV-PROV-237` owns valid requested-version endpoints. No
other new identifier was assigned.

All four modules retain their exact headings and software-verification
classification. Their seven-field test documentation now states owner-specific
requirements, methods, independent lexical or language-semantic oracles, exact
acceptance, failure meaning, and exclusions. Blanket E501 suppression was
removed; no helper was introduced. Semantic inspection found no production
defect.

## Direct generic-validator invocation

The literal direct invocation was:

```text
python harness/pi/validation/validate_python_test_evidence.py python/tests/software_verification/ksdft2effmass/provenance/test__CapabilityKind.py python/tests/software_verification/ksdft2effmass/provenance/test__ExternalToolIdentity.py python/tests/software_verification/ksdft2effmass/provenance/test__ExternalToolSpecification.py python/tests/software_verification/ksdft2effmass/provenance/test__DeclaredCapability.py --ownership .pi/evidence/backend-neutral-cpn-P2-tools-provenance/audit-a01-test-evidence-ownership.json --migration-map .pi/evidence/backend-neutral-cpn-P2-tools-provenance/audit-a01-test-evidence-node-migration.json
```

Its exact final JSON output was:

```json
{"claim_boundary":["oracle independence","mathematical correctness","property/surface correctness","test cohesion","tolerance adequacy","scientific validity","uncertainty quantification","human acceptance"],"counts":{"artifact_owned_modules":0,"class_owned_modules":4,"evidence_class_modules":{"numerical_verification":0,"scientific_validation":0,"software_verification":4,"uncertainty_quantification":0},"findings_by_code":{},"helper_functions":0,"modules":4,"parameterized_functions":14,"static_collected_parameter_cases":85,"test_functions":26,"unique_evidence_owners":26},"findings":[],"paths":["python/tests/software_verification/ksdft2effmass/provenance/test__CapabilityKind.py","python/tests/software_verification/ksdft2effmass/provenance/test__ExternalToolIdentity.py","python/tests/software_verification/ksdft2effmass/provenance/test__ExternalToolSpecification.py","python/tests/software_verification/ksdft2effmass/provenance/test__DeclaredCapability.py"],"schema_version":1,"status":"PASS"}
```

Skill/profile selection and the semantic judgments above are separate from this
deterministic structural result. The validator cannot establish oracle
independence, semantic field completeness, scientific validation, UQ, or human
acceptance. An initial pre-final invocation rejected double-underscore parameter
IDs as nonsemantic; those IDs were changed to single-underscore field-and-partition
IDs, the migration record was regenerated, and all final gates were then run.

## Identity and count reconciliation

- Supplied modules: 4
- Test functions and evidence owners: 26 each
- Parameterized functions: 14
- Static parameter cases: 85
- Unparameterized collected cases: 12
- Authoritative pytest collection: 97
- Helpers: 0
- Ownership: 4 class-owned, 0 artifact-owned
- Evidence classes: 4 software-verification modules
- Historical collection: 43 nodes
- Closed one-to-one migration: 43 old nodes to 43 current nodes
- Current nodes without historical predecessors: 54
- Historical evidence identifiers preserved: 24
- Never-used new identifiers: `SV-PROV-237` and `SV-PROV-238`

The exact old inventory, migration targets, current per-module inventory, counts,
and new-owner rationales are in `audit-a01-test-evidence-inventory.json`. The
closed mapping is in `audit-a01-test-evidence-node-migration.json`.

## Final validation

- Task-ownership preflight: PASS.
- Direct structural validator on exactly four paths: PASS with zero findings.
- Complete four-module collection: PASS, 97 nodes.
- Four class-owned modules: PASS, 97 cases.
- Ruff format check and lint without E501 suppression: PASS.
- Focused mypy over `src` plus the four tests: PASS, 47 source files.
- Staging-area check: PASS, empty.

## Scope and residual boundary

Only the four assigned class-owned tests and four assigned A01 evidence records
were modified by this writer. Concurrent queue, task, validator, documentation,
and unrelated worktree changes were not modified. Production source remained
read-only. Passing synthetic software verification does not establish external
tool availability, installation correctness, execution behavior, provenance
truth, numerical verification, scientific validation, UQ, portability,
cross-language conformance, release readiness, reviewer acceptance, or human
acceptance.
