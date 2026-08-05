"""Evidence class and represented meaning
Software verification of a portable sealed-artifact reference.
Owned contract, oracle, and scope
ArtifactReference is the SUT; public nested ownership and location separation are the
oracle.
VVUQ and scientific exclusions
Evidence excludes storage discovery, numerical verification, scientific validation, UQ,
physical correctness, and cross-language conformance.
"""

from dataclasses import FrozenInstanceError, fields

import pytest

from ksdft2effmass.provenance import (
    ArtifactIdentity,
    ArtifactReference,
    ArtifactSpecification,
)

SUT = ArtifactReference
pytestmark = pytest.mark.software_verification


def test_constructor__nested_fields_and_properties__maps_exact_reference() -> None:
    """Evidence ID
    SV-PROV-006
    Requirement
    A reference owns exact identity/specification records and exposes matching flat
    read-only properties.
    Method
    Construct independent nested records and inspect stored and derived public fields.
    Oracle
    The P2 reference field map fixes all expected values without executing serializer
    code.
    Acceptance
    Nested identities are retained and all four convenience properties equal their
    source fields.
    Interpretation
    Failure indicates mapping, ownership, or property drift.
    Limitations
    The synthetic digest is not proof of actual content.
    """
    identity = ArtifactIdentity("artifact-1", "b" * 64, 8)
    specification = ArtifactSpecification("out/a.json", "json", "result", "retain")
    value = SUT(identity, specification, "manifest-1")
    assert value.identity is identity
    assert value.specification is specification
    assert (value.artifact_id, value.logical_path, value.sha256, value.byte_size) == (
        "artifact-1",
        "out/a.json",
        "b" * 64,
        8,
    )


def test_field__reference_location_separation__excludes_location_and_is_frozen() -> (
    None
):
    """Evidence ID
    SV-PROV-007
    Requirement
    Portable references contain no deployment root, location path, or external
    descriptor.
    Method
    Inspect public dataclass fields and attempt producer identity reassignment.
    Oracle
    The human-approved ArtifactReference/ArtifactLocation separation fixes the exact
    field set.
    Acceptance
    Fields are identity, specification, producer_manifest_id only and mutation is
    rejected.
    Interpretation
    Failure indicates a protected boundary regression.
    Limitations
    Reflection checks the declared public dataclass surface, not hostile runtime
    injection.
    """
    value = SUT(
        ArtifactIdentity("artifact-1", "b" * 64, 8),
        ArtifactSpecification("out/a", "json", "result", "retain"),
        "manifest-1",
    )
    assert tuple(field.name for field in fields(SUT)) == (
        "identity",
        "specification",
        "producer_manifest_id",
    )
    with pytest.raises(FrozenInstanceError):
        value.producer_manifest_id = "other"  # type: ignore[misc]


def test_constructor__nested_types__rejects_lookalikes() -> None:
    """Evidence ID
    SV-PROV-008
    Requirement
    Reference collaborators must be the exact accepted public record families rather
    than mappings or strings.
    Method
    Pass dictionary and string lookalikes through the public constructor.
    Oracle
    The public semantic type contract requires TypeError for both wrong collaborators.
    Acceptance
    Each lookalike raises TypeError.
    Interpretation
    Failure indicates unintended coercion or a stale contract.
    Limitations
    User-defined subclasses are not partitioned separately.
    """
    identity = ArtifactIdentity("artifact-1", "b" * 64, 8)
    specification = ArtifactSpecification("out/a", "json", "result", "retain")
    with pytest.raises(TypeError):
        SUT({}, specification, "manifest-1")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT(identity, "out/a", "manifest-1")  # type: ignore[arg-type]
