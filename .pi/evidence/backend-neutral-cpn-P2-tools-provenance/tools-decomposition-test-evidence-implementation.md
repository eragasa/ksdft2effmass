# P2 tools-decomposition test-evidence implementation

## Invocation identity and authority

- Request: `P2-TOOLS-DECOMPOSITION-1`
- Task: `P2`
- Parent workflow: `backend-neutral-kohn-sham-qe`
- Attempt: `p2-tools-decomposition-test-1`
- Selected skill: `.pi/skills/develop-python-test-evidence/SKILL.md`, with its complete `references/test-evidence-conventions.md`
- Selected profile: `AUTHORIZED_TEST_EVIDENCE_WRITE`
- Validated ownership: `.pi/evidence/backend-neutral-cpn-P2-tools-provenance/task-ownership.json`
- Evidence class: software verification
- Ownership: 13 `class_owned` modules; zero `artifact_owned` modules
- Stop policy: stop on authority or contract conflict, incomplete historical mapping, unauthorized mutation, or a failed required gate.

The skill/profile selection is an invocation fact independent of validation results. Validator success does not establish that the skill ran, semantic correctness, scientific validity, UQ, or human acceptance.

## Implemented evidence

The four missing enum owners and nine migrated record/enum owners now use package-level public class imports, one public class SUT per module, the software-verification marker, exact maintained headings, semantic ID-free test names, explicit semantic parameter IDs, and all seven documentation fields. There are no evidence helpers and no hidden case loops.

Every enum checks exact name/value/order vocabulary, `StrEnum` inheritance, alias-free `__members__`, value/name lookup identity, and invalid lookup behavior without production reachability. Every record checks its applicable exact fields and types, optional states, type/value boundaries, canonical tuples, relational invariants, frozen assignment, complete equality, lifecycle distinctions, and exclusion of runtime/credential/handle state. `ExternalExecutionOutcome` is an internal defining-module typing-alias collaborator used only to expose the explicitly approved result/failure decomposition under the sole `ExternalExecutionResult` SUT and owner. It is not an accepted package export, separate public owner, or fourteenth owner; all class SUTs remain package imports.

Historical evidence IDs `SV-PROV-024` through `SV-PROV-045`, `SV-PROV-074`, and `SV-PROV-078` are retained without renumbering. The 24 baseline nodes from `/tmp/p2-tools-old-collection.txt` map one-to-one to 24 current nodes. New cohesive evidence owners use never-used IDs `SV-PROV-176` through `SV-PROV-236`; abandoned IDs `SV-PROV-143` and `SV-PROV-163` remain unused.

## Counts and classifications

- supplied modules: 13
- test functions: 85
- static parameter cases: 87
- collected pytest cases: 145
- unique evidence owners: 85
- helpers: 0
- class-owned modules: 13
- artifact-owned modules: 0
- software-verification modules: 13
- numerical-verification, scientific-validation, and UQ modules: 0
- mapped historical nodes: 24
- genuinely new collected nodes: 121

Collection count, test-function count, static parameter-case count, and evidence-owner count are distinct quantities.

## Commands and exact results

Ownership preflight:

```text
python .pi/task-ownership/validate_task_ownership.py --task P2
task ownership preflight passed: .pi/evidence/backend-neutral-cpn-P2-tools-provenance/task-ownership.json
```

Direct supplied-path structural validator (the exact invocation used):

```text
python harness/pi/validation/validate_python_test_evidence.py python/tests/software_verification/ksdft2effmass/provenance/test__CapabilityKind.py python/tests/software_verification/ksdft2effmass/provenance/test__VerificationStatus.py python/tests/software_verification/ksdft2effmass/provenance/test__ExternalExecutionStatus.py python/tests/software_verification/ksdft2effmass/provenance/test__ExternalFailureStage.py python/tests/software_verification/ksdft2effmass/provenance/test__ExternalFailureCode.py python/tests/software_verification/ksdft2effmass/provenance/test__ExternalToolIdentity.py python/tests/software_verification/ksdft2effmass/provenance/test__ExternalToolSpecification.py python/tests/software_verification/ksdft2effmass/provenance/test__DeclaredCapability.py python/tests/software_verification/ksdft2effmass/provenance/test__InstallationObservation.py python/tests/software_verification/ksdft2effmass/provenance/test__VerificationObservation.py python/tests/software_verification/ksdft2effmass/provenance/test__ExternalExecutionRequest.py python/tests/software_verification/ksdft2effmass/provenance/test__ExternalExecutionResult.py python/tests/software_verification/ksdft2effmass/provenance/test__ExternalExecutionFailure.py --ownership .pi/evidence/backend-neutral-cpn-P2-tools-provenance/tools-decomposition-test-evidence-ownership.json --migration-map .pi/evidence/backend-neutral-cpn-P2-tools-provenance/tools-decomposition-test-evidence-node-migration.json
{"claim_boundary":["oracle independence","mathematical correctness","property/surface correctness","test cohesion","tolerance adequacy","scientific validity","uncertainty quantification","human acceptance"],"counts":{"artifact_owned_modules":0,"class_owned_modules":13,"evidence_class_modules":{"numerical_verification":0,"scientific_validation":0,"software_verification":13,"uncertainty_quantification":0},"findings_by_code":{},"helper_functions":0,"modules":13,"parameterized_functions":27,"static_collected_parameter_cases":87,"test_functions":85,"unique_evidence_owners":85},"findings":[],"schema_version":1,"status":"PASS"}
```

Focused collection and execution:

```text
PYTHONPATH=python/src python -m pytest --collect-only -q <the same 13 explicit module paths>
145 tests collected in 0.04s

PYTHONPATH=python/src python -m pytest -q <the same 13 explicit module paths>
145 passed in 0.09s
```

Formatting and lint for the 13 modules and completion validator:

```text
python -m ruff format <the 13 explicit module paths> .pi/evidence/backend-neutral-cpn-P2-tools-provenance/validate_p2_completion.py
14 files left unchanged

python -m ruff check <the 13 explicit module paths> .pi/evidence/backend-neutral-cpn-P2-tools-provenance/validate_p2_completion.py
All checks passed!
```

P2 completion validation:

```text
python .pi/evidence/backend-neutral-cpn-P2-tools-provenance/validate_p2_completion.py
{"issues":[],"observed":{"class_owned_modules":30,"complete_migrated_nodes":373,"fixtures":44,"mapped_historical_nodes":90,"public_exports":32,"schemas":1,"test_evidence_modules":8,"tools_decomposition_complete_nodes":145,"tools_decomposition_historical_nodes":24,"tools_decomposition_modules":13},"schema_version":1,"status":"PASS","task_id":"P2"}
```

## Pre-review deterministic integration continuation

The focused mypy gate initially reported 59 errors because intentionally invalid runtime inputs and frozen-field assignments were expressed as statically valid calls. The same evidence owners now use visible `cast(Any, ...)`, `dict[str, Any]`, and dynamic-name `setattr` mechanics. These changes preserve runtime values, exception assertions, node IDs, evidence IDs, and represented semantics; no whole-file mypy suppression or weakened configuration was added.

Every inventory entry for `SV-PROV-176` through `SV-PROV-236` now has an owner-specific rationale naming its exact SUT, semantic test owner, and requirement. The collection remains exactly identical to the 145-node maintained inventory.

Exact focused mypy gate:

```text
cd python && uv run mypy src/ksdft2effmass/provenance tests/software_verification/ksdft2effmass/provenance tests/software_verification/ksdft2effmass/integration/test__provenance_python_import_dependency_direction.py tests/software_verification/ksdft2effmass/integration/test__provenance_package_wheel_contract.py
warning: `VIRTUAL_ENV=/Users/eugene/repos/ksdft2effmass/.venv` does not match the project environment path `.venv` and will be ignored; use `--active` to target the active environment instead
Success: no issues found in 40 source files
```

Continuation validation results:

```text
python harness/pi/validation/validate_python_test_evidence.py <the 13 explicit module paths> --ownership .pi/evidence/backend-neutral-cpn-P2-tools-provenance/tools-decomposition-test-evidence-ownership.json --migration-map .pi/evidence/backend-neutral-cpn-P2-tools-provenance/tools-decomposition-test-evidence-node-migration.json
status=PASS; findings=[]; test_functions=85; static_collected_parameter_cases=87; unique_evidence_owners=85

PYTHONPATH=python/src python -m pytest --collect-only -q <the 13 explicit module paths>
145 collected nodes exactly match inventory

PYTHONPATH=python/src python -m pytest -q <the 13 explicit module paths>
145 passed in 0.11s

python -m ruff check <the 13 explicit module paths> .pi/evidence/backend-neutral-cpn-P2-tools-provenance/validate_p2_completion.py
All checks passed!
```

## Sole consolidated post-review correction disposition

The sole reviewer finding was accepted and corrected in the one authorized consolidated pass. `SV-PROV-226`, its node ID, and its exact `get_args(ExternalExecutionOutcome) == (ExternalExecutionResult, ExternalExecutionFailure)` assertion are retained under the sole `ExternalExecutionResult` SUT. Module and test documentation now classify `ExternalExecutionOutcome` only as an internal defining-module typing-alias collaborator implementing the explicitly approved result/failure decomposition, explicitly not as a package export or separate public owner. The owner-specific inventory rationale is synchronized. Counts, assertions, package exports, source, documentation, schemas, fixtures, and integration tests are unchanged. No second review is scheduled.

Post-review correction gates passed: the exact supplied-path structural validator reported `status=PASS`, `findings=[]`, 85 test functions, 87 static parameter cases, and 85 unique evidence owners; the exact 13 modules reported `145 passed in 0.09s`; Ruff reported `All checks passed!`; and the focused mypy command reported `Success: no issues found in 40 source files` (with only the recorded virtual-environment warning).

## Separate semantic review and residual judgments

Manual semantic review found no blocker in public-surface naming, test cohesion, exact deterministic oracles, enum lookup semantics, dataclass value semantics, lifecycle separation, or schema/runtime layering. The fixed expected vocabularies, field inventories, Python exception semantics, and canonical tuple/path relations are independent of production algorithms. No approximate tolerance or warning behavior applies.

The structural validator does not establish oracle independence, semantic completeness, property/surface correctness, mathematics, scientific validity, UQ, portability, cross-language agreement, or human acceptance. These tests use synthetic metadata and do not execute external tools, validate solver convergence, validate physical models, or exercise serialization/schema interoperability.
