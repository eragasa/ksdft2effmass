"""Evidence class and represented meaning
Software verification of the public ``WireRecordKind`` surface; no physical model,
mathematical operator, or numerical representation is represented.

Owned contract, oracle, and scope
The sole primary SUT is ``WireRecordKind``.  Accepted H1 field/wire contracts and
read-only H3 fixtures are independent exact oracles.

VVUQ and scientific exclusions
Passing checks only the stated software contract. Numerical verification, scientific
validation, uncertainty quantification, physical correctness, and cross-language
conformance are excluded.
"""

from __future__ import annotations

import pytest

from ksdft2effmass.harness.pi import WireRecordKind

pytestmark = pytest.mark.software_verification
SUT = WireRecordKind


def test_constructor__closed_values__equal_public_json_record_names() -> None:
    """Evidence ID
    SV-HARNESS-023
    Requirement
    The enum is closed over the sixteen public JSON record class names.
    Method
    Enumerate public enum values.
    Oracle
    The H1 closed-union table lists the exact sixteen names.
    Acceptance
    The enumerated values equal the literal accepted sequence.
    Interpretation
    A failure identifies a production, accepted-contract, fixture, or environment
    discrepancy requiring independent review.
    Limitations
    This is exact software verification only; it makes no numerical,
    scientific-validation, UQ, physical, or Rust-conformance claim.
    """
    assert tuple(x.value for x in SUT) == (
        "ArtifactIdentity",
        "ResourceReference",
        "ResourceManifest",
        "ProjectProfile",
        "SkillDescriptor",
        "OwnershipScope",
        "AgentDescriptorView",
        "OwnershipManifestView",
        "CheckpointRecord",
        "TaskReference",
        "ChainView",
        "ChecksumEntry",
        "ChecksumManifest",
        "EvidenceIdentifierOccurrence",
        "ValidationIssue",
        "ValidationResult",
    )
