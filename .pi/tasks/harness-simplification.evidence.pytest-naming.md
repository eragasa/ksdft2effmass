# Evaluate pytest-evidence naming

Status: proposed_inactive; must complete before `harness-simplification.evidence-and-sqlite`

Task identity: `harness-simplification.evidence.pytest-naming`

This future harness-simplification task evaluates and, only after an explicit public-contract and compatibility decision, may migrate the current `test_evidence` naming to terminology that states its actual pytest-specific boundary.

The preferred candidate for evaluation is the module name `pytest_evidence.py`, because the current contract validates evidence-bearing pytest modules, including `test_*` functions, pytest markers, parameter IDs, evidence-owner docstrings, and class-owned or artifact-owned pytest modules. `evidence_tester` is not preferred because it could imply that the component tests evidence rather than validates the structure of evidence-bearing pytest tests.

The task must review the complete affected public family before implementation, including `PythonTestEvidenceSource`, `PythonTestEvidenceRequest`, `PythonTestEvidenceFinding`, `PythonTestEvidenceValidationResult`, and `ValidatePythonTestEvidence`. It must decide whether public names also migrate to a coherent pytest-specific DataObject/ResultObject/ActionObject family, define hard-rename or compatibility behavior, preserve existing evidence IDs through an explicit maintained migration map, and synchronize source, tests, skills, resources, documentation, manifests, and command wrappers.

This record does not authorize the rename, a compatibility alias, SQLite, schemas, persistence, execution, or successor activation. The task remains inactive until separately authorized. `harness-simplification.evidence-and-sqlite` must remain inactive and depend on completion of this naming task.
