r"""Software verification of local public api and models.

Facet and represented meaning

Software verification of the 51-name local public import surface and immutable
routing/data records.

Intrinsic and cross-object scope

The artifact owner is ``ksdft2effmass.harness.pi.local``; exact exports, constructors,
sorting, and rollback are checked against the accepted H4 task and public source
contract.

VVUQ and scientific exclusions

Passing establishes software representation behavior only, not numerical verification,
scientific validation, UQ, physical correctness, or cross-language conformance.
"""

from pathlib import Path
from typing import Any

import pytest

import ksdft2effmass.harness.pi.local as local
from ksdft2effmass.harness.pi import ValidationIssue, ValidationResult
from ksdft2effmass.harness.pi.local import (
    AdaptationResult,
    EvidenceOwnershipRelation,
    LegacyInvocation,
    LocalIssue,
    LocalValidationResult,
    RepositoryRoots,
    RepositoryValidationResult,
    RouteConfiguration,
    RouteSelection,
    ShadowObservation,
    ShadowPairResult,
    ValidationRoute,
)

pytestmark = pytest.mark.software_verification

EXPECTED = (
    "AgentRecordAdapter",
    "ChainRecordAdapter",
    "CheckpointRecordAdapter",
    "ChecksumCatalogAdapter",
    "EvidenceOwnershipManifestAdapter",
    "OwnershipManifestAdapter",
    "SkillInventoryAdapter",
    "TaskRecordAdapter",
    "AdaptationResult",
    "AdaptedRepositoryRecords",
    "ShadowPairComparator",
    "EvidenceOwnershipRelation",
    "LegacyInvocation",
    "LocalHarnessContextLoader",
    "LocalHarnessContext",
    "LocalIssue",
    "LocalValidationResult",
    "ShadowSuiteReplayer",
    "RepositoryRoots",
    "RepositoryValidationResult",
    "LegacyRouteConfigurationPreparer",
    "RouteConfiguration",
    "RouteSelection",
    "EvidenceModuleSelector",
    "ValidationRouteSelector",
    "ShadowObservation",
    "ShadowPairResult",
    "ShadowReplayResult",
    "LocalRepositoryValidator",
    "ValidationRoute",
    "HarnessTask",
    "HarnessTaskSerializer",
    "HarnessTaskDeserializer",
    "HarnessTaskGraphValidator",
    "HarnessTaskDocumentSource",
    "HarnessTaskSourceDisposition",
    "HarnessTaskSourceMapping",
    "HarnessTaskDocumentationContent",
    "HarnessTaskProjectionProfile",
    "HarnessTaskDocumentation",
    "HarnessTaskDocumentationRenderer",
    "HarnessTaskDocumentationComparator",
    "HarnessTaskDocumentationComparisonResult",
    "HarnessTaskMigrationReviewPacketRequest",
    "HarnessTaskMigrationReviewPacketPreparer",
    "HarnessTaskMigrationReviewPacket",
    "HarnessTaskMigrationReviewDocument",
    "HarnessTaskMigrationReviewPacketRenderer",
    "HarnessTaskMigrationDisposition",
    "HarnessTaskMigrationFileDisposition",
    "HarnessTaskMigrationFileDispositionRecorder",
)


def test_public_api__exports__contains_exact_51_names() -> None:
    """Evidence ID: SV-HL-001

    Requirement: The project-local package exposes exactly the corrected 51 public
    names.

    Method: Compare the package ``__all__`` and runtime attributes to a fixed
    independent
    inventory.

    Oracle: The accepted H4 inventory and corrected HarnessTask inventory supply the
    exact local boundary.

    Acceptance: The ordered tuple is exact, has length 51, and every name resolves.

    Interpretation: Failure identifies packaging drift or an incorrect inventory.

    Limitations: This does not establish behavior of each export, numerical results,
    science, UQ, or
    portability.
    """
    assert tuple(local.__all__) == EXPECTED
    assert len(EXPECTED) == 51
    assert all(getattr(local, name) is not None for name in EXPECTED)


def test_public_api__action_names__follow_target_actionizer_grammar() -> None:
    """Evidence ID: SV-HL-044

    Requirement: Every project-local public ActionObject uses target-first Actionizer
    grammar.

    Method: Select exported classes exposing ``execute`` and inspect their exact names.

    Oracle: The accepted suffixes describe adapter, comparator, deserializer, loader,
    preparer, recorder, renderer, replayer, selector, serializer, and validator owners.

    Acceptance: Every selected public class ends with one accepted Actionizer suffix.

    Interpretation: Failure indicates project-local public naming drift.

    Limitations: Naming does not establish behavior, scientific validity, or UQ.
    """
    suffixes = (
        "Adapter",
        "Comparator",
        "Deserializer",
        "Loader",
        "Preparer",
        "Recorder",
        "Renderer",
        "Replayer",
        "Selector",
        "Serializer",
        "Validator",
    )
    actions = (
        name
        for name in local.__all__
        if isinstance(value := getattr(local, name), type)
        and callable(getattr(value, "execute", None))
    )
    assert all(name.endswith(suffixes) for name in actions)


def test_constructor__local_records__enforces_invariants_and_value_semantics(
    tmp_path: Path,
) -> None:
    """Evidence ID: SV-HL-002

    Requirement: Local records reject invalid types/order/status and retain immutable
    exact values.

    Method: Construct representative valid and invalid RepositoryRoots, LocalIssue,
    LocalValidationResult, AdaptationResult, LegacyInvocation, ShadowObservation,
    RouteConfiguration, RouteSelection, and RepositoryValidationResult values.

    Oracle: Dataclass and enum invariants documented by the public constructors define
    exact
    outcomes.

    Acceptance: Valid values compare exactly; invalid roots, namespaces, order, failed
    values, and
    rollback targets raise TypeError or ValueError.

    Interpretation: Failure indicates a constructor-contract defect or stale test
    transcription.

    Limitations: Filesystem lifetime, subprocess execution, numerical verification,
    science, UQ, and
    cross-language behavior are excluded.
    """
    repo = tmp_path.resolve()
    (repo / "g").mkdir()
    (repo / "l").mkdir()
    roots = RepositoryRoots(repo, repo / "g", repo / "l")
    relation = EvidenceOwnershipRelation(
        "tests/evidence.py",
        ("SV-HL-002",),
        "artifact_owned",
        "left <-> right",
        "agreement",
        "left",
        "right",
        "none",
    )
    assert relation.direction == "none"
    issue = LocalIssue("PIHL.TEST", "a", "detail")
    failed = LocalValidationResult("FAIL", (issue,))
    assert AdaptationResult(None, failed).value is None
    invocation = LegacyInvocation("p", ("python",), ("input",), None)
    observation = ShadowObservation("legacy", "PASS", (), (), (), 0, None)
    selection = RouteSelection(True, False, ValidationRoute.LEGACY)
    assert (roots.repository_root, invocation.pair_id, observation.exit_status) == (
        repo,
        "p",
        0,
    )
    assert selection.authoritative_route is ValidationRoute.LEGACY
    passing = ValidationResult(1, "PASS", ())
    warning_issue = ValidationIssue(
        1, "PIH.EVIDENCE.PROTECTED_GAP", "WARNING", None, None, (), "gap"
    )
    warning = ValidationResult(1, "WARN", (warning_issue,))
    assert (
        RepositoryValidationResult("WARN", (("a", passing), ("b", warning))).status
        == "WARN"
    )
    with pytest.raises(ValueError):
        RepositoryValidationResult("PASS", (("a", warning),))
    with pytest.raises(ValueError):
        LocalIssue("BAD", None, "x")
    with pytest.raises(ValueError):
        LocalValidationResult("PASS", (issue,))
    with pytest.raises(TypeError):
        AdaptationResult(object(), failed)
    mutable_cases: tuple[object, ...] = ({"nested": []}, [()], ([],))

    def exercise_mutable_case_148_1(mutable: Any) -> Any:
        with pytest.raises(TypeError):
            AdaptationResult(mutable, LocalValidationResult("PASS", ()))

    _ = [exercise_mutable_case_148_1(mutable) for mutable in (mutable_cases)]
    with pytest.raises(ValueError, match="parent traversal"):
        RepositoryRoots(repo, repo / "g" / ".." / "g", repo / "l")
    with pytest.raises(ValueError):
        RouteConfiguration(ValidationRoute.LOCAL, ValidationRoute.LOCAL)
    with pytest.raises(ValueError):
        RouteSelection(False, False, ValidationRoute.LEGACY)
    with pytest.raises(TypeError):
        ShadowObservation("x", "PASS", (), (), (), True, None)
    with pytest.raises(ValueError):
        ShadowPairResult(
            "bad", observation, observation, "intentional", (), "x", ("authority",)
        )
