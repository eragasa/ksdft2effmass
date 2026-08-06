# P2-A02 test-evidence implementation

## Skill and invocation identity

- Request: `P2-PROVENANCE-AUDIT-1:P2-A02`
- Task: `P2`
- Parent workflow: `backend-neutral-kohn-sham-qe`
- Attempt: `p2-a02-test-correction-1`
- Profile: `AUTHORIZED_TEST_EVIDENCE_WRITE`
- Skill content: `.pi/skills/develop-python-test-evidence/SKILL.md` and the complete `references/test-evidence-conventions.md`
- Evidence class: software verification
- Ownership: three `class_owned` modules in `p2-a02-test-evidence-ownership.json`
- Production input: `python/src/ksdft2effmass/provenance/tool_observations.py`, inspected read-only
- Production SHA-256 before and after: `eb41f05d156181483afe6a3218d00907500288fd1bb63dafa032b0297e14a0f1`
- Stop policy: stop on invalid ownership, unauthorized mutation, incomplete historical mapping, a production defect, or a failed required gate

## Bounded correction

The three class-owned modules now independently exercise every accepted and
rejected partition named by the human audit. Identifier cases cover every
validated field and ordinary, minimum, maximum, type, empty, malformed,
leading-character, surrogate, NFC, and overlength partitions. Version, digest,
evidence-member, ordering, uniqueness, provenance, frozen-state, equality, enum
construction, and enum name lookup are separate coherent owners where their
requirements or exception partitions differ.

The exact field order, stored values, built-in types, enum type, tuple type, and
absence of coercion are checked directly. Equality includes identical complete
state and independent changes to every represented field. Every public field is
included in frozen reassignment evidence. Installation durability and
verification lifecycle exclusions remain explicit without asserting execution,
provenance truth, numerical verification, scientific validation, or UQ.

All historical evidence identifiers were retained. Forty-three new identifiers,
`SV-PROV-239` through `SV-PROV-281`, own newly independent requirements; their
owners and rationales are recorded in `p2-a02-test-evidence-inventory.json`.
The 32 historical collected nodes map one-to-one to their closest current
successors in `p2-a02-test-evidence-node-migration.json`. The current collection
contains 191 cases, of which 159 have no historical predecessor.

The exact headings and seven documentation fields are present. Blanket E501
suppression, doubled punctuation, vague protocol surfaces, generated parameter
IDs, literal-loop parameterization, and generic unsupported prose were removed.
Two module-visible, assertion-free, ID-free helpers provide direct valid baseline
construction without hiding oracles.

## Direct structural-validator invocation

```bash
python harness/pi/validation/validate_python_test_evidence.py \
  python/tests/software_verification/ksdft2effmass/provenance/test__VerificationStatus.py \
  python/tests/software_verification/ksdft2effmass/provenance/test__InstallationObservation.py \
  python/tests/software_verification/ksdft2effmass/provenance/test__VerificationObservation.py \
  --ownership .pi/evidence/backend-neutral-cpn-P2-tools-provenance/p2-a02-test-evidence-ownership.json \
  --migration-map .pi/evidence/backend-neutral-cpn-P2-tools-provenance/p2-a02-test-evidence-node-migration.json
```

Exact structured output:

```json
{"claim_boundary":["oracle independence","mathematical correctness","property/surface correctness","test cohesion","tolerance adequacy","scientific validity","uncertainty quantification","human acceptance"],"counts":{"artifact_owned_modules":0,"class_owned_modules":3,"evidence_class_modules":{"numerical_verification":0,"scientific_validation":0,"software_verification":3,"uncertainty_quantification":0},"findings_by_code":{},"helper_functions":2,"modules":3,"parameterized_functions":30,"static_collected_parameter_cases":157,"test_functions":64,"unique_evidence_owners":64},"findings":[],"paths":["python/tests/software_verification/ksdft2effmass/provenance/test__VerificationStatus.py","python/tests/software_verification/ksdft2effmass/provenance/test__InstallationObservation.py","python/tests/software_verification/ksdft2effmass/provenance/test__VerificationObservation.py"],"schema_version":1,"status":"PASS"}
```

This PASS establishes structural convention conformance only. It does not
establish semantic completeness, oracle independence, scientific meaning,
numerical verification, scientific validation, UQ, provenance truth, or human
acceptance.

## Counts

- Class-owned modules: 3
- Test functions and unique evidence owners: 64
- Parameterized functions: 30
- Static parameter cases: 157
- Authoritative pytest collection: 191
- Helpers: 2
- Historical collected nodes mapped: 32 of 32
- Current nodes without historical predecessors: 159
- Historical evidence identifiers preserved: 21
- New evidence identifiers: 43

## Writer-scope validation

The test writer reported PASS for Ruff formatting and lint, focused collection
and 191-case execution, focused mypy over production plus the three modules,
`git diff --check`, an empty staging area, and the final supplied-path structural
validator. Parent integration, complete provenance, documentation, control-plane,
coverage, and nonmutation gates are recorded separately.

## Scope boundary

Production source, schemas, fixtures, serialization, dependencies, and locks
were not modified. These synthetic software-verification tests do not establish
external-tool availability, execution correctness, provenance truth, numerical
verification, scientific validation, UQ, portability, cross-language agreement,
release readiness, reviewer acceptance, or P2 human acceptance.
