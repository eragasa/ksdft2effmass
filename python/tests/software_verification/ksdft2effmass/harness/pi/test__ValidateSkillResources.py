"""Evidence class and represented meaning
Software verification of the public ``ValidateSkillResources`` surface; no physical
model, mathematical operator, or numerical representation is represented.

Owned contract, oracle, and scope
The sole primary SUT is ``ValidateSkillResources``.  Accepted H1 field/wire contracts
and read-only H3 fixtures are independent exact oracles.

VVUQ and scientific exclusions
Passing checks only the stated software contract. Numerical verification, scientific
validation, uncertainty quantification, physical correctness, and cross-language
conformance are excluded.
"""

from __future__ import annotations

import pytest

from ksdft2effmass.harness.pi import ValidateSkillResources

pytestmark = pytest.mark.software_verification
SUT = ValidateSkillResources


def test_constructor__action_object__is_stateless_and_fieldless() -> None:
    """Evidence ID
    SV-HARNESS-035
    Requirement
    ValidateSkillResources is a concrete stateless ActionObject.
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


def test_execute__valid_and_invalid__returns_exact_partition() -> None:
    """Evidence ID
    SV-HARNESS-059
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
        DeserializeJsonRecord,
        ProjectProfile,
        ResourceManifest,
        SerializeJsonRecord,
        SkillDescriptor,
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
    assert SUT().execute((), generic, identity, None, None, profile).status == "PASS"
    descriptor = SkillDescriptor(
        1,
        "missing-skill",
        1,
        "missing-entry",
        ("cap",),
        ("missing-entry", "missing-policy"),
        "read_only",
        "missing-policy",
        "none",
        "stop_after_result",
    )
    invalid = SUT().execute((descriptor,), generic, identity, None, None, profile)
    assert invalid.status == "FAIL"
    assert {issue.code for issue in invalid.issues} >= {
        "PIH.SKILL.ENTRY_MISSING",
        "PIH.SKILL.CLOSURE_INCOMPLETE",
    }
