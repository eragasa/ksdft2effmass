r"""Software verification of ``ArtifactReference``.

Facet and represented meaning
-----------------------------
This module verifies a portable reference to sealed artifact identity, specification,
and producer-manifest metadata without deployment-location state.

Intrinsic and cross-object scope
--------------------------------
``ArtifactReference`` is the sole SUT; nested public types, producer identity, derived
properties, immutability, and equality are intrinsic. Referenced-object existence is
excluded.

VVUQ and scientific exclusions
------------------------------
Evidence excludes storage discovery, content observation, numerical verification,
scientific validation, UQ, physical correctness, and cross-language conformance.
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


@pytest.mark.parametrize(
    ("producer_manifest_id", "exception"),
    [
        (b"manifest", TypeError),
        ("", ValueError),
        ("bad id", ValueError),
        ("e\u0301", ValueError),
        ("\ud800", ValueError),
        ("a" * 129, ValueError),
    ],
)
def test_field__producer_manifest_identifier__rejects_nonportable_values(
    producer_manifest_id: object, exception: type[Exception]
) -> None:
    """Evidence ID
    SV-PROV-086
    Requirement
    producer_manifest_id is a built-in, nonempty, NFC bounded identifier.
    Method
    Supply wrong-type, empty, spaced, decomposed, surrogate, and overlength values.
    Oracle
    The public identifier and semantic type contracts classify each representative.
    Acceptance
    Each construction raises its documented TypeError or ValueError class.
    Interpretation
    Failure permits a nonportable producer relationship identifier.
    Limitations
    Existence of the producer manifest is a cross-object concern and is not checked.
    """
    identity = ArtifactIdentity("artifact-1", "b" * 64, 8)
    specification = ArtifactSpecification("out/a", "json", "result", "retain")
    with pytest.raises(exception):
        SUT(identity, specification, producer_manifest_id)  # type: ignore[arg-type]


def test_property__exact_value_semantics__includes_nested_and_producer_fields() -> None:
    """Evidence ID
    SV-PROV-087
    Requirement
    Reference equality is exact over identity, specification, and producer manifest.
    Method
    Compare separately constructed equal values and a value with another producer.
    Oracle
    Public frozen dataclass fields define exact equality without storage lookup.
    Acceptance
    Equal represented fields compare equal and the producer change compares unequal.
    Interpretation
    Failure indicates incomplete or identity-based reference equality.
    Limitations
    Byte existence and semantic equivalence of producers are excluded.
    """
    identity = ArtifactIdentity("artifact-1", "b" * 64, 8)
    specification = ArtifactSpecification("out/a", "json", "result", "retain")
    value = SUT(identity, specification, "manifest-1")
    assert value == SUT(
        ArtifactIdentity("artifact-1", "b" * 64, 8),
        ArtifactSpecification("out/a", "json", "result", "retain"),
        "manifest-1",
    )
    assert value != SUT(identity, specification, "manifest-2")
