"""Evidence class and represented meaning
Software verification of the public ``ResolveResource`` surface; no physical model,
mathematical operator, or numerical representation is represented.

Owned contract, oracle, and scope
The sole primary SUT is ``ResolveResource``.  Accepted H1 field/wire contracts and
read-only H3 fixtures are independent exact oracles.

VVUQ and scientific exclusions
Passing checks only the stated software contract. Numerical verification, scientific
validation, uncertainty quantification, physical correctness, and cross-language
conformance are excluded.
"""

from __future__ import annotations

import pytest

from ksdft2effmass.harness.pi import ResolveResource

pytestmark = pytest.mark.software_verification
SUT = ResolveResource


def test_constructor__action_object__is_stateless_and_fieldless() -> None:
    """Evidence ID
    SV-HARNESS-028
    Requirement
    ResolveResource is a concrete stateless ActionObject.
    Method
    Construct two instances and inspect their public storage boundary.
    Oracle
    The accepted H1 action contract requires no retained root, profile, cache,
    client, or mutable state.
    Acceptance
    Construction succeeds and instances expose no instance dictionary or slots
    containing fields.
    Interpretation
    A failure identifies a production, accepted-contract, fixture, or environment
    discrepancy requiring independent review.
    Limitations
    This is exact software verification only; it makes no numerical,
    scientific-validation, UQ, physical, or Rust-conformance claim.
    """
    action = SUT()
    assert not hasattr(action, "__dict__")
    assert SUT.__slots__ == ()


def test_method__execute_valid_and_invalid__returns_exact_partition(tmp_path) -> None:
    """Evidence ID
    SV-HARNESS-052
    Requirement
    The public action executes one valid and one major invalid partition.
    Method
    Invoke execute directly with accepted records and a controlled invalid input.
    Oracle
    Accepted H1 action semantics and H3 fixtures fix the exact result partition.
    Acceptance
    Valid output is exact; invalid output has the expected code and no partial value.
    Interpretation
    Failure identifies action-contract drift requiring independent review.
    Limitations
    This is deterministic software verification, not scientific validation or UQ.
    """

    import json
    import shutil
    from pathlib import Path

    from ksdft2effmass.harness.pi import (
        DeserializeJsonRecord,
        ProjectProfile,
        ResourceManifest,
        SerializeJsonRecord,
        WireRecordKind,
    )

    root = Path(__file__).resolve().parents[6]
    case = json.loads(
        (
            root
            / "harness/pi/fixtures/resource-resolution/cases/resolve-generic-leaf.json"
        ).read_text()
    )

    def decode(kind, value):
        result = DeserializeJsonRecord().execute(
            kind, (json.dumps(value) + "\n").encode()
        )
        assert result.record is not None
        return result.record

    generic = decode(WireRecordKind.ResourceManifest, case["generic_manifest"])
    profile = decode(WireRecordKind.ProjectProfile, case["profile"])
    assert isinstance(generic, ResourceManifest) and isinstance(profile, ProjectProfile)
    identity = SerializeJsonRecord().execute(generic).content_identity
    assert identity is not None
    work = tmp_path / "roots"
    shutil.copytree(root / "harness/pi/fixtures/resource-resolution/roots", work)
    valid = SUT().execute(
        case["resource_id"],
        work / "generic",
        generic,
        identity,
        None,
        None,
        None,
        profile,
    )
    assert valid.validation.status == "PASS" and valid.reference is not None
    invalid = SUT().execute(
        "absent.resource",
        work / "generic",
        generic,
        identity,
        None,
        None,
        None,
        profile,
    )
    assert invalid.reference is None and invalid.resolved_path is None
    assert [issue.code for issue in invalid.validation.issues] == [
        "PIH.RESOURCE.NOT_FOUND"
    ]


@pytest.mark.parametrize(
    ("case_id", "expected_code"),
    [
        ("duplicate-resource-id", "PIH.RESOURCE.DUPLICATE_ID"),
        ("duplicate-resource-path", "PIH.RESOURCE.DUPLICATE_PATH"),
        ("self-dependency", "PIH.RESOURCE.DEPENDENCY_CYCLE"),
    ],
)
def test_method__execute_invalid_manifest__short_circuits_without_selection(
    tmp_path, case_id: str, expected_code: str
) -> None:
    """Evidence ID
    SV-HARNESS-063
    Requirement
    ResolveResource validates a manifest first and returns no selected/interpreted
    resource result when that manifest is relationally invalid.
    Method
    Deserialize each corrected H3 candidate, supply a deliberately absent explicit
    root, and request a represented resource ID through the public action.
    Oracle
    Corrected H1 action precedence fixes manifest failure before filesystem access;
    H3 fixes the exact relational issue code for each candidate.
    Acceptance
    The exact singleton manifest code is propagated and both ``reference`` and
    ``resolved_path`` are None; no root needs to exist.
    Interpretation
    Failure identifies manifest-gate bypass, partial-result leakage, precedence drift,
    or H3 fixture disagreement.
    Limitations
    Only the corrected duplicate/self-edge partitions are covered; no physical,
    scientific-validation, UQ, or Rust-conformance claim is made.
    """
    import json
    from pathlib import Path

    from ksdft2effmass.harness.pi import (
        DeserializeJsonRecord,
        ProjectProfile,
        ResourceManifest,
        SerializeJsonRecord,
        WireRecordKind,
    )

    root = Path(__file__).resolve().parents[6]
    case = json.loads(
        (
            root / f"harness/pi/fixtures/resource-resolution/cases/{case_id}.json"
        ).read_text()
    )
    manifest_result = DeserializeJsonRecord().execute(
        WireRecordKind.ResourceManifest,
        (json.dumps(case["generic_manifest"]) + "\n").encode(),
    )
    profile_result = DeserializeJsonRecord().execute(
        WireRecordKind.ProjectProfile,
        (json.dumps(case["profile"]) + "\n").encode(),
    )
    assert isinstance(manifest_result.record, ResourceManifest)
    assert isinstance(profile_result.record, ProjectProfile)
    identity = SerializeJsonRecord().execute(manifest_result.record).content_identity
    assert identity is not None

    result = SUT().execute(
        manifest_result.record.resources[0].resource_id,
        tmp_path / "intentionally-absent-root",
        manifest_result.record,
        identity,
        None,
        None,
        None,
        profile_result.record,
    )
    assert [issue.code for issue in result.validation.issues] == [expected_code]
    assert result.reference is None
    assert result.resolved_path is None
