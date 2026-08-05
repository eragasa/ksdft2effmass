# ruff: noqa: E501
"""Evidence class and represented meaning
Software verification of the 30-name local public import surface and immutable routing/data records.
Owned contract, oracle, and scope
The artifact owner is ``ksdft2effmass.harness.pi.local``; exact exports, constructors, sorting, and rollback are checked against the accepted H4 task and public source contract.
VVUQ and scientific exclusions
Passing establishes software representation behavior only, not numerical verification, scientific validation, UQ, physical correctness, or cross-language conformance.
"""

from pathlib import Path

import pytest

import ksdft2effmass.harness.pi.local as local
from ksdft2effmass.harness.pi.local import (
    AdaptationResult,
    EvidenceOwnershipRelation,
    LegacyInvocation,
    LocalIssue,
    LocalValidationResult,
    RepositoryRoots,
    RollBackValidationRoute,
    RouteConfiguration,
    RouteSelection,
    ShadowObservation,
    ShadowPairResult,
    ValidationRoute,
)

pytestmark = pytest.mark.software_verification

EXPECTED = (
    "AdaptAgentRecords",
    "AdaptChainRecord",
    "AdaptCheckpointRecords",
    "AdaptChecksumCatalog",
    "AdaptEvidenceOwnershipManifest",
    "AdaptOwnershipManifest",
    "AdaptSkillInventory",
    "AdaptTaskRecords",
    "AdaptationResult",
    "AdaptedRepositoryRecords",
    "CompareShadowPair",
    "EvidenceOwnershipRelation",
    "LegacyInvocation",
    "LoadLocalHarnessContext",
    "LocalHarnessContext",
    "LocalIssue",
    "LocalValidationResult",
    "ReplayShadowSuite",
    "RepositoryRoots",
    "RepositoryValidationResult",
    "RollBackValidationRoute",
    "RouteConfiguration",
    "RouteSelection",
    "SelectEvidenceModules",
    "SelectValidationRoute",
    "ShadowObservation",
    "ShadowPairResult",
    "ShadowReplayResult",
    "ValidateLocalRepository",
    "ValidationRoute",
)


def test_public_api__exports__contains_exact_30_names() -> None:
    "Evidence ID\nSV-HL-001\nRequirement\n        The project-local package exposes exactly the accepted 30 public names.\nMethod\n        Compare the package ``__all__`` and runtime attributes to a fixed independent inventory.\nOracle\n        The H4 public inventory is transcribed from the activated local boundary.\nAcceptance\n        The ordered tuple is exact, has length 30, and every name resolves.\nInterpretation\n        Failure identifies packaging drift or an incorrect inventory.\nLimitations\n        This does not establish behavior of each export, numerical results, science, UQ, or portability."
    assert tuple(local.__all__) == EXPECTED
    assert len(EXPECTED) == 30
    assert all(getattr(local, name) is not None for name in EXPECTED)


def test_constructor__local_records__enforces_invariants_and_value_semantics(
    tmp_path: Path,
) -> None:
    "Evidence ID\nSV-HL-002\nRequirement\n        Local records reject invalid types/order/status and retain immutable exact values.\nMethod\n        Construct representative valid and invalid RepositoryRoots, LocalIssue, LocalValidationResult, AdaptationResult, LegacyInvocation, ShadowObservation, RouteConfiguration, and RouteSelection values.\nOracle\n        Dataclass and enum invariants documented by the public constructors define exact outcomes.\nAcceptance\n        Valid values compare exactly; invalid roots, namespaces, order, failed values, and rollback targets raise TypeError or ValueError.\nInterpretation\n        Failure indicates a constructor-contract defect or stale test transcription.\nLimitations\n        Filesystem lifetime, subprocess execution, numerical verification, science, UQ, and cross-language behavior are excluded."
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
    assert (
        RollBackValidationRoute()
        .execute(RouteConfiguration(ValidationRoute.LOCAL))
        .route
        is ValidationRoute.LEGACY
    )
    with pytest.raises(ValueError):
        LocalIssue("BAD", None, "x")
    with pytest.raises(ValueError):
        LocalValidationResult("PASS", (issue,))
    with pytest.raises(TypeError):
        AdaptationResult(object(), failed)
    for mutable in ({"nested": []}, [()], ([],)):
        with pytest.raises(TypeError):
            AdaptationResult(mutable, LocalValidationResult("PASS", ()))
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
