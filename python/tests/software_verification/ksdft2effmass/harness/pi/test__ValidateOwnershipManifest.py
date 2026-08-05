"""Evidence class and represented meaning
Software verification of the public ``ValidateOwnershipManifest`` surface; no physical
model, mathematical operator, or numerical representation is represented.

Owned contract, oracle, and scope
The sole primary SUT is ``ValidateOwnershipManifest``.  Accepted H1 field/wire contracts
and read-only H3 fixtures are independent exact oracles.

VVUQ and scientific exclusions
Passing checks only the stated software contract. Numerical verification, scientific
validation, uncertainty quantification, physical correctness, and cross-language
conformance are excluded.
"""

from __future__ import annotations

import pytest

from ksdft2effmass.harness.pi import ValidateOwnershipManifest

pytestmark = pytest.mark.software_verification
SUT = ValidateOwnershipManifest


def test_constructor__action_object__is_stateless_and_fieldless() -> None:
    """Evidence ID
    SV-HARNESS-030
    Requirement
    ValidateOwnershipManifest is a concrete stateless ActionObject.
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
    SV-HARNESS-054
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

    from pathlib import Path

    from ksdft2effmass.harness.pi import (
        AgentDescriptorView,
        ChainView,
        DeserializeJsonRecord,
        OwnershipManifestView,
        OwnershipScope,
        ProjectProfile,
        WireRecordKind,
    )

    root = Path(__file__).resolve().parents[6]

    def load(kind, name):
        result = DeserializeJsonRecord().execute(
            kind, (root / f"harness/pi/fixtures/valid/{name}.json").read_bytes()
        )
        assert result.record is not None
        return result.record

    chain = load(WireRecordKind.ChainView, "chain-view")
    profile = load(WireRecordKind.ProjectProfile, "project-profile")
    assert isinstance(chain, ChainView) and isinstance(profile, ProjectProfile)
    manifest = OwnershipManifestView(
        1,
        "T1",
        "tasks/T1.json",
        (
            (
                "resource-writer",
                "agent.writer",
                (OwnershipScope(1, "validation/complete.py", "file"),),
            ),
        ),
        (("independent-reviewer", "agent.reviewer"),),
        "validation/complete.py",
        ("python", "validation/complete.py"),
        None,
    )
    agents = (
        AgentDescriptorView(1, "agent.reviewer", "read_only"),
        AgentDescriptorView(1, "agent.writer", "writer"),
    )
    assert SUT().execute(manifest, chain, agents, profile).status == "PASS"
    invalid = SUT().execute(manifest, chain, agents[:1], profile)
    assert [issue.code for issue in invalid.issues] == ["PIH.OWNERSHIP.AGENT_MISMATCH"]
