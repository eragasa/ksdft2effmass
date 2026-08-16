r"""Software verification of the local public API and common records.

Evidence profile: claim_bearing

Bounded artifact scope: project-local public imports and adapter facade.

Facet and represented meaning

The module owns the exact maintained local import surface and adapter identities.

Intrinsic and cross-object scope

Record-specific invariants remain with their class-owned modules; this artifact checks
only package and facade agreement plus common immutable adaptation records.

VVUQ and scientific exclusions

Passing establishes software representation behavior only, not numerical verification,
scientific validation, UQ, physical correctness, or human acceptance.
"""

from inspect import signature
from pathlib import Path

import pytest

import ksdft2effmass.harness.pi.local as local
import ksdft2effmass.harness.pi.local.adapters as adapter_facade
import ksdft2effmass.harness.pi.local.dbcontrol as dbcontrol
from ksdft2effmass.harness.pi.local import (
    AdaptationResult,
    LocalIssue,
    LocalValidationResult,
    RepositoryRoots,
)

pytestmark = pytest.mark.software_verification

ADAPTER_EXECUTE_PARAMETERS = {
    "AgentRecordAdapter": ("self", "agent_documents"),
    "ChainRecordAdapter": ("self", "chain_bytes", "task_records", "activation_bytes"),
    "CheckpointRecordAdapter": ("self", "checkpoint_documents"),
    "ChecksumCatalogAdapter": ("self", "catalog_bytes"),
    "EvidenceModuleSelector": ("self", "module_payloads", "profile"),
    "OwnershipManifestAdapter": ("self", "manifest_bytes"),
    "SkillInventoryAdapter": ("self", "inventory_bytes", "descriptor_bytes"),
    "TaskRecordAdapter": ("self", "task_documents", "chain_bytes", "activation_bytes"),
}

EXPECTED = (
    "AgentRecordAdapter",
    "ChainRecordAdapter",
    "CheckpointRecordAdapter",
    "ChecksumCatalogAdapter",
    "OwnershipManifestAdapter",
    "SkillInventoryAdapter",
    "TaskRecordAdapter",
    "AdaptationResult",
    "LocalHarnessContextLoader",
    "LocalHarnessContext",
    "LocalIssue",
    "LocalValidationResult",
    "RepositoryRoots",
    "EvidenceModuleSelector",
    "HarnessValidationRequest",
    "HarnessValidationCheck",
    "HarnessValidationResult",
    "HarnessValidator",
    "ArchivedTaskSource",
    "HarnessTask",
    "HarnessTaskSerializer",
    "HarnessTaskDeserializer",
    "HarnessTaskGraphValidator",
)

RETIRED_CONTROL_NAMES = (
    "HarnessControlMigrationRequest",
    "HarnessControlMigrationResult",
    "HarnessControlMigrator",
    "HarnessControlVerificationFinding",
    "HarnessControlVerificationResult",
    "HarnessControlVerifier",
)


def test_public_api__exports__contains_exact_maintained_names() -> None:
    """Evidence ID: SV-HL-001

    Requirement: The project-local package exposes exactly the maintained names, and
    the adapter facade preserves the eight operational adapter identities.

    Method: Compare exports, runtime identities, and execute parameter names with fixed
    independent inventories.

    Oracle: The post-retirement local boundary and accepted adapter signatures are
    literal expectations.

    Acceptance: Package and facade exports, identities, and signatures agree exactly.

    Interpretation: Failure identifies stale compatibility or packaging drift.

    Limitations: Import agreement does not establish behavior or scientific claims.
    """
    assert tuple(local.__all__) == EXPECTED
    assert all(not hasattr(local, name) for name in RETIRED_CONTROL_NAMES)
    assert dbcontrol.__all__ == []
    assert all(not hasattr(dbcontrol, name) for name in RETIRED_CONTROL_NAMES)
    assert tuple(adapter_facade.__all__) == tuple(ADAPTER_EXECUTE_PARAMETERS)
    assert all(
        getattr(adapter_facade, name) is getattr(local, name)
        for name in ADAPTER_EXECUTE_PARAMETERS
    )
    assert {
        name: tuple(signature(getattr(local, name).execute).parameters)
        for name in ADAPTER_EXECUTE_PARAMETERS
    } == ADAPTER_EXECUTE_PARAMETERS


def test_public_api__action_names__follow_target_actionizer_grammar() -> None:
    """Evidence ID: SV-HL-044

    Requirement: Every project-local public ActionObject uses target-first Actionizer
    grammar.

    Method: Select exported classes exposing ``execute`` and inspect exact names.

    Oracle: Accepted suffixes describe every remaining operational Action owner.

    Acceptance: Every selected class ends with an accepted Actionizer suffix.

    Interpretation: Failure identifies project-local public naming drift.

    Limitations: Naming does not establish behavior or scientific validity.
    """
    suffixes = (
        "Adapter",
        "Deserializer",
        "Loader",
        "Selector",
        "Serializer",
        "Validator",
        "Migrator",
        "Verifier",
    )
    actions = (
        name
        for name in local.__all__
        if isinstance(value := getattr(local, name), type)
        and callable(getattr(value, "execute", None))
    )
    assert all(name.endswith(suffixes) for name in actions)


def test_constructor__common_local_records__enforce_immutable_values(
    tmp_path: Path,
) -> None:
    """Evidence ID: SV-HL-002

    Requirement: Common local records reject invalid roots, status disagreement, and
    mutable adaptation values while preserving exact immutable state.

    Method: Construct representative literal valid and invalid values.

    Oracle: Public constructor contracts and exact dataclass equality define outcomes.

    Acceptance: Valid state compares exactly and each invalid partition raises the
    documented exception category.

    Interpretation: Failure identifies a common record contract defect.

    Limitations: Class-specific records and filesystem lifetime are covered elsewhere.
    """
    repository = tmp_path.resolve()
    (repository / "generic").mkdir()
    (repository / "local").mkdir()
    roots = RepositoryRoots(repository, repository / "generic", repository / "local")
    assert roots.repository_root == repository
    issue = LocalIssue("PIHL.TEST", "a", "detail")
    failed = LocalValidationResult("FAIL", (issue,))
    assert AdaptationResult(None, failed) == AdaptationResult(None, failed)
    with pytest.raises(ValueError):
        LocalIssue("BAD", None, "x")
    with pytest.raises(ValueError):
        LocalValidationResult("PASS", (issue,))
    with pytest.raises(TypeError):
        AdaptationResult({"mutable": []}, LocalValidationResult("PASS", ()))
    with pytest.raises(ValueError, match="parent traversal"):
        RepositoryRoots(
            repository,
            repository / "generic" / ".." / "generic",
            repository / "local",
        )
