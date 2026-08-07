r"""Software verification of ``ValidateResourceManifest``.

Facet and represented meaning
Software verification of the public ``ValidateResourceManifest`` surface; no physical
model, mathematical operator, or numerical representation is represented.

Intrinsic and cross-object scope
The sole primary SUT is ``ValidateResourceManifest``.  Accepted H1 field/wire contracts
and read-only H3 fixtures are independent exact oracles.

VVUQ and scientific exclusions
Passing checks only the stated software contract. Numerical verification, scientific
validation, uncertainty quantification, physical correctness, and cross-language
conformance are excluded.
"""

from __future__ import annotations

from typing import Any

import pytest

from ksdft2effmass.harness.pi import ValidateResourceManifest

pytestmark = pytest.mark.software_verification
SUT = ValidateResourceManifest


def test_constructor__action_object__is_stateless_and_fieldless() -> None:
    """Evidence ID
    SV-HARNESS-029
    Requirement
    ValidateResourceManifest is a concrete stateless ActionObject.
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


def test_method__execute_valid_and_invalid__returns_exact_partition() -> None:
    """Evidence ID
    SV-HARNESS-053
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
    from pathlib import Path

    from ksdft2effmass.harness.pi import (
        ArtifactIdentity,
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

    def decode(kind: WireRecordKind, value: Any) -> object:
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
    assert SUT().execute(generic, identity, None, None, profile).status == "PASS"
    wrong = ArtifactIdentity(1, "sha256", "0" * 64)
    invalid = SUT().execute(generic, wrong, None, None, profile)
    assert [issue.code for issue in invalid.issues] == [
        "PIH.RESOURCE.MANIFEST_MISMATCH"
    ]


@pytest.mark.parametrize(
    ("case_id", "expected_code"),
    [
        ("duplicate-resource-id", "PIH.RESOURCE.DUPLICATE_ID"),
        ("duplicate-resource-path", "PIH.RESOURCE.DUPLICATE_PATH"),
        ("self-dependency", "PIH.RESOURCE.DEPENDENCY_CYCLE"),
    ],
    ids=["duplicate_resource_id", "duplicate_resource_path", "self_dependency"],
)
def test_method__execute_relational_precedence__returns_exact_existing_code(
    case_id: str, expected_code: str
) -> None:
    """Evidence ID
    SV-HARNESS-062
    Requirement
    Manifest validation owns duplicate IDs, duplicate paths, and self-edge cycles and
    reports their existing capability-specific code under accepted precedence.
    Method
    Publicly deserialize each corrected H3 relational candidate and its profile,
    compute the candidate's public serialized identity, and validate it.
    Oracle
    Corrected H1 action precedence and the H3 oracle index independently fix the three
    exact singleton issue-code sequences.
    Acceptance
    Candidate deserialization passes; validation fails; the issue-code list is exactly
    the parameter's singleton code, without a wire or lower-precedence substitute.
    Interpretation
    Failure identifies decoder/validator ownership drift, precedence drift, or an H3
    oracle defect requiring independent review.
    Limitations
    The three corrected relational partitions are covered; other invalid-manifest
    relations, scientific validation, UQ, and Rust conformance are excluded.
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
    assert manifest_result.validation.status == "PASS"
    assert profile_result.validation.status == "PASS"
    assert isinstance(manifest_result.record, ResourceManifest)
    assert isinstance(profile_result.record, ProjectProfile)
    identity = SerializeJsonRecord().execute(manifest_result.record).content_identity
    assert identity is not None

    result = SUT().execute(
        manifest_result.record, identity, None, None, profile_result.record
    )
    assert result.status == "FAIL"
    assert [issue.code for issue in result.issues] == [expected_code]


@pytest.mark.parametrize(
    ("resource_kind", "format_version", "expected_code"),
    [
        ("skill", 1, "PIH.RESOURCE.KIND_UNSUPPORTED"),
        ("reference", 2, "PIH.RESOURCE.VERSION_INCOMPATIBLE"),
    ],
    ids=["unsupported_resource_kind", "incompatible_format_version"],
)
def test_method__execute_profile_compatibility__distinguishes_kind_from_version(
    resource_kind: str, format_version: int, expected_code: str
) -> None:
    """Evidence ID
    SV-HARNESS-065
    Requirement
    Manifest validation distinguishes a closed-enum kind absent from the profile
    from an unsupported version of a kind that the profile does support.
    Method
    Mutate only kind or format_version in the valid H3 generic-leaf candidate,
    deserialize it publicly, compute its public identity, and validate it.
    Oracle
    The accepted H1 issue/action contract assigns KIND_UNSUPPORTED to an absent
    profiled kind and VERSION_INCOMPATIBLE to an absent supported-kind pair.
    Acceptance
    Deserialization passes and validation returns the exact singleton code.
    Interpretation
    Failure identifies compatibility-classification or precedence drift.
    Limitations
    This is deterministic software verification, not scientific validation, UQ,
    or cross-language conformance.
    """
    import copy
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
            root
            / "harness/pi/fixtures/resource-resolution/cases/resolve-generic-leaf.json"
        ).read_text()
    )
    candidate = copy.deepcopy(case["generic_manifest"])
    candidate["resources"][0]["resource_kind"] = resource_kind
    candidate["resources"][0]["format_version"] = format_version
    manifest_result = DeserializeJsonRecord().execute(
        WireRecordKind.ResourceManifest,
        (json.dumps(candidate) + "\n").encode(),
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
        manifest_result.record, identity, None, None, profile_result.record
    )
    assert result.status == "FAIL"
    assert [issue.code for issue in result.issues] == [expected_code]
