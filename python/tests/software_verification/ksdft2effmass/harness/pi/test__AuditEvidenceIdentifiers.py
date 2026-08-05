"""Evidence class and represented meaning
Software verification of the public ``AuditEvidenceIdentifiers`` surface; no physical
model, mathematical operator, or numerical representation is represented.

Owned contract, oracle, and scope
The sole primary SUT is ``AuditEvidenceIdentifiers``.  Accepted H1 field/wire contracts
and read-only H3 fixtures are independent exact oracles.

VVUQ and scientific exclusions
Passing checks only the stated software contract. Numerical verification, scientific
validation, uncertainty quantification, physical correctness, and cross-language
conformance are excluded.
"""

from __future__ import annotations

import pytest

from ksdft2effmass.harness.pi import AuditEvidenceIdentifiers

pytestmark = pytest.mark.software_verification
SUT = AuditEvidenceIdentifiers


def test_constructor__action_object__is_stateless_and_fieldless() -> None:
    """Evidence ID
    SV-HARNESS-033
    Requirement
    AuditEvidenceIdentifiers is a concrete stateless ActionObject.
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
    SV-HARNESS-057
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
        DeserializeJsonRecord,
        ProjectProfile,
        WireRecordKind,
    )

    root = Path(__file__).resolve().parents[6]
    decoded = DeserializeJsonRecord().execute(
        WireRecordKind.ProjectProfile,
        (root / "harness/pi/fixtures/valid/project-profile.json").read_bytes(),
    )
    assert isinstance(decoded.record, ProjectProfile)
    source = (
        b"import pytest\n"
        b"pytestmark = pytest.mark.verification_alpha\n"
        b'def test_x():\n    """VX-A-001"""\n'
    )
    valid = SUT().execute(
        (("tests/classification-alpha/test_x.py", source),), decoded.record
    )
    assert (
        valid.validation.status == "PASS"
        and valid.occurrences[0].evidence_id == "VX-A-001"
    )
    invalid = SUT().execute(
        (("tests/classification-alpha/test_x.py", b"not python !"),), decoded.record
    )
    assert invalid.occurrences == ()
    assert [issue.code for issue in invalid.validation.issues] == [
        "PIH.EVIDENCE.SOURCE_INVALID"
    ]
