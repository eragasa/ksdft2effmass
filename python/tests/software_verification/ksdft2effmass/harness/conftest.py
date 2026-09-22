"""Pytest-owned shared fixtures for development-harness software verification."""

import hashlib
from pathlib import PurePosixPath

import pytest

from ksdft2effmass.harness import (
    DevelopmentTaskSelection,
    HarnessCapabilityCatalog,
    HarnessEvidenceCatalog,
    HarnessResourceCatalog,
    HarnessSourceFamily,
    HarnessSourceIdentity,
    HarnessState,
    HarnessTask,
    HarnessTaskRegistry,
)
from ksdft2effmass.harness.pi import (
    ArtifactIdentity,
    PiHarnessAgentDefinition,
    ResourceManifest,
    ResourceReference,
    SkillDescriptor,
)
from ksdft2effmass.harness.pi.conformance.python import PythonModuleSource


@pytest.fixture
def normalized_harness_state() -> HarnessState:
    """Return one synthetic complete and cross-record-consistent Harness state."""
    task = HarnessTask(
        schema_version=3,
        task_id="validation-task",
        title="Validation test Task",
        status="active",
        status_detail="Synthetic software-verification state.",
        parent_task_id=None,
        task_prerequisite_ids=(),
        external_prerequisite_ids=(),
        superseded_by_task_ids=(),
        explicit_activation_required=True,
        objective="Exercise normalized Harness validation.",
        authority_reference_paths=("docs/architecture/v2/index.md",),
        authorized_scope=("Synthetic software-verification input only.",),
        completion_criteria=("The represented software contract is satisfied.",),
        exclusions=("No authority or scientific claim is represented.",),
        intake_path=None,
    )
    skill = SkillDescriptor(
        1,
        "validation-skill",
        1,
        "validation-entry",
        ("validation-capability",),
        ("validation-entry",),
        "read_only",
        "validation-policy",
        "none",
        "stop_after_result",
    )
    agent = PiHarnessAgentDefinition(
        1,
        "validation-agent",
        "validation",
        "validation.validation-agent",
        "agents/validation-agent.md",
        ArtifactIdentity(1, "sha256", "1" * 64),
        "read_only",
        ("validation-skill",),
        True,
    )
    resource = ResourceReference(
        1,
        "validation-entry",
        "skill",
        1,
        "skills/validation/SKILL.md",
        ArtifactIdentity(1, "sha256", "2" * 64),
        (),
    )
    manifest = ResourceManifest(
        1,
        "validation-resources",
        1,
        "generic",
        None,
        (resource,),
    )
    source = PythonModuleSource(
        "python/tests/software_verification/test_validation_sample.py",
        b"assert True\n",
    )
    assert source.payload is not None
    source_identity = HarnessSourceIdentity(
        family=HarnessSourceFamily.EVIDENCE,
        relative_path=PurePosixPath(source.path),
        format_version=1,
        sha256=hashlib.sha256(source.payload).hexdigest(),
        byte_count=len(source.payload),
    )
    normalization_version = "validation-test-v1"
    capabilities = HarnessCapabilityCatalog.create(
        model_version=1,
        normalization_version=normalization_version,
        capabilities=(skill,),
        agent_definitions=(agent,),
    )
    resources = HarnessResourceCatalog.create(
        model_version=1,
        normalization_version=normalization_version,
        resources=(manifest,),
    )
    evidence = HarnessEvidenceCatalog.create(
        model_version=1,
        normalization_version=normalization_version,
        evidence=(source,),
        source_identities=(source_identity,),
    )
    return HarnessState.create(
        source_snapshot_identity="3" * 64,
        normalization_version=normalization_version,
        tasks=HarnessTaskRegistry(1, (task,)),
        selection=DevelopmentTaskSelection(
            schema_version=1,
            active_task_id=task.task_id,
            explicit_activation_receipt_ids=(),
            automatic_successor_activation=False,
        ),
        decisions=(),
        capabilities=capabilities,
        resources=resources,
        evidence=evidence,
        provenance=(),
    )
