r"""Software verification of harness pi public api.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

Software verification of the generic PI harness package import surface; no physical,
mathematical, or numerical object is represented.

Intrinsic and cross-object scope

The primary owner is the package public API artifact. The accepted maintained-tool
contracts provide the exact public-surface list used as the independent oracle.

VVUQ and scientific exclusions

Passing establishes import completeness and closure only, not numerical verification,
scientific validation, UQ, physical correctness, or release readiness.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

import pytest

import ksdft2effmass.harness.pi as api

pytestmark = pytest.mark.software_verification

ROOT = Path(__file__).resolve().parents[6]


def test_public_api__exports__match_exact_h1_surface() -> None:
    """Evidence ID: SV-HARNESS-039

    Requirement: The package exports every and only the accepted maintained harness
    public names.

    Method: Compare ``__all__`` and attribute availability with a literal transcription
    of
    the accepted surface.

    Oracle: The accepted validator and task-state tool contracts expand the H1 surface
    with
    the exact records, results, and actions named below.

    Acceptance: ``__all__`` equals the exact literal sequence and every listed
    attribute resolves from the public package.

    Interpretation: Failure indicates source/public-contract drift or an incomplete
    package import.

    Limitations: Import presence does not prove action semantics, documentation quality,
    scientific validity, UQ, or release status.
    """
    expected = (
        "ArtifactIdentity",
        "ResourceReference",
        "ResourceManifest",
        "ResourceManifestRefreshRequest",
        "ProjectProfile",
        "SkillDescriptor",
        "OwnershipScope",
        "AgentDescriptorView",
        "PiHarnessConfiguration",
        "PiHarnessAgentDefinition",
        "conformance",
        "HumanReviewTarget",
        "HumanReviewObservation",
        "HumanReviewFinding",
        "HumanReviewPacket",
        "HumanReviewDecision",
        "OwnershipManifestView",
        "CheckpointRecord",
        "CheckpointDecisionResolutionRequest",
        "ChecksumEntry",
        "ChecksumManifest",
        "TaskStateInspectionRequest",
        "ValidationIssue",
        "ValidationResult",
        "ProjectProfileLoadResult",
        "ResourceResolutionResult",
        "TaskStateInspectionResult",
        "ResourceManifestRefreshResult",
        "CheckpointDecisionResolutionResult",
        "JsonSerializationResult",
        "JsonDeserializationResult",
        "WireRecordKind",
        "HarnessWireRecord",
        "HarnessInternalError",
        "JsonRecordSerializer",
        "JsonRecordDeserializer",
        "PiHarnessConfigurationDeserializer",
        "PiHarnessAgentDefinitionResolver",
        "ProjectProfileLoader",
        "ResourceManifestRefresher",
        "ResourceResolver",
        "ResourceManifestValidator",
        "CheckpointDecisionResolver",
        "CheckpointSetValidator",
        "HumanReviewPreparer",
        "HumanReviewDecisionRecorder",
        "TaskStateInspector",
        "ChecksumManifestValidator",
        "SkillResourceValidator",
        "Identifier",
        "ResourcePath",
        "OwnershipScopePath",
        "DiagnosticPath",
        "Version",
    )
    assert api.__all__ == expected
    assert all(hasattr(api, name) for name in expected)


def test_public_api__retired_chains__retain_history_without_live_capability() -> None:
    """Evidence ID: SV-HARNESS-183

    Requirement: Canonical Tasks and selection replace the former public chain model
    while archived chain bytes remain retained as non-operational history.

    Method: Inspect module discovery, the exact root namespace, executable Pi-chain
    discovery, and the retained archive directory.

    Oracle: The conditionally accepted chain-replacement cutover retires live chain
    capability while preserving historical files outside Pi discovery.

    Acceptance: No chain module or former public name is importable, no executable Pi
    chain directory exists, and the archived chain directory remains nonempty.

    Interpretation: Failure identifies surviving public chain capability, executable
    discovery, or loss of retained historical files.

    Limitations: Path and import checks establish neither semantic interpretation of
    archived bytes nor scientific, protected-execution, or release claims.

    Provenance: Human-authorized minimal Architecture v2 cutover frontier.
    """
    assert importlib.util.find_spec("ksdft2effmass.harness.pi.chains") is None
    assert not {
        "TaskReference",
        "ChainView",
        "ChainEvaluationResult",
        "ChainStateEvaluator",
        "OwnershipManifestValidator",
    } & set(vars(api))
    assert not (ROOT / ".pi/chains").exists()
    assert tuple((ROOT / "harness/archive/task-control-v1/chains").glob("*.json"))


def test_public_api__action_instances__retain_no_mutable_state() -> None:
    """Evidence ID: SV-HARNESS-040

    Requirement: Every accepted ActionObject is concrete, fieldless, and stateless.

    Method: Construct each exact public action and inspect its instance storage surface.

    Oracle: The accepted maintained harness surface requires the listed concrete
    actions with no roots, profiles, caches, clients, or mutable state.

    Acceptance: Every instance lacks ``__dict__`` and its class declares empty slots.

    Interpretation: Failure exposes an unauthorized retained-state or public-surface
    change.

    Limitations: This structural check does not establish each action's relational
    behavior or
    any scientific claim.
    """
    names = (
        "JsonRecordSerializer",
        "JsonRecordDeserializer",
        "PiHarnessConfigurationDeserializer",
        "PiHarnessAgentDefinitionResolver",
        "ProjectProfileLoader",
        "ResourceManifestRefresher",
        "ResourceResolver",
        "ResourceManifestValidator",
        "CheckpointDecisionResolver",
        "CheckpointSetValidator",
        "HumanReviewPreparer",
        "HumanReviewDecisionRecorder",
        "TaskStateInspector",
        "ChecksumManifestValidator",
        "SkillResourceValidator",
    )

    def assert_public_action_is_fieldless_and_stateless(name: Any) -> Any:
        """Evidence ID: Owns no identifier; supports the enclosing stable evidence ID
        SV-HARNESS-040.

        Requirement: Each action in the exact literal inventory satisfies the same
        fieldless and
        stateless public-action requirement.

        Method: Construct the named action and mechanically apply the enclosing test's
        two
        storage assertions.

        Oracle: The accepted inventory requires identical empty-slot instance structure
        for
        every listed action.

        Acceptance: The instance has no ``__dict__`` and its class declares empty slots.

        Interpretation: Failure identifies one listed action that violates the shared
        structural
        contract; this helper makes no independent evidence claim.

        Limitations: The iteration mechanically applies one identical requirement,
        oracle, and
        acceptance rule across the exact literal inventory; it hides no distinct
        partition or action semantics.
        """
        instance = getattr(api, name)()
        assert not hasattr(instance, "__dict__")
        assert type(instance).__slots__ == ()

    _ = [assert_public_action_is_fieldless_and_stateless(name) for name in names]


def test_public_api__action_names__follow_target_actionizer_grammar() -> None:
    """Evidence ID: SV-HARNESS-170

    Requirement: Public ActionObjects use target-first names ending in precise agent
    nouns.

    Method: Inspect the exact generic root and Python-conformance ActionObject
    inventories.

    Oracle: The accepted grammar is ``<DataObject-or-operation-target><Actionizer>``.

    Acceptance: Every public ActionObject name ends in an accepted suffix, including
    ``PythonConformanceValidator`` at its conformance owner.

    Interpretation: Failure indicates naming drift or an undocumented migration
    exception.

    Limitations: Name conformance does not establish ActionObject behavior or scientific
    validity.
    """
    suffixes = (
        "Auditor",
        "Deserializer",
        "Evaluator",
        "Inspector",
        "Loader",
        "Preparer",
        "Recorder",
        "Refresher",
        "Resolver",
        "Serializer",
        "Validator",
    )
    action_names = {
        name
        for package in (api, api.conformance.python)
        for name in package.__all__
        if isinstance(value := getattr(package, name), type)
        and callable(getattr(value, "execute", None))
    }
    assert all(name.endswith(suffixes) for name in action_names)
    assert "PythonConformanceValidator" in action_names
    assert "IdentifierAuditor" not in action_names
