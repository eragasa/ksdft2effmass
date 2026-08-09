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


def test_constructor__nested_fields__maps_exact_reference() -> None:
    """Evidence ID: SV-PROV-006

    Requirement: A reference stores exact identity/specification records and producer
    identity.

    Method: Construct independent nested records and inspect the stored public fields.

    Oracle: The P2 reference field map fixes all expected values without executing
    serializer
    code.

    Acceptance: Nested records retain object identity and producer_manifest_id equals
    its input.

    Interpretation: Failure indicates mapping, ownership, or property drift.

    Limitations: The synthetic digest is not proof of actual content.
    """
    identity = ArtifactIdentity("artifact-1", "b" * 64, 8)
    specification = ArtifactSpecification("out/a.json", "json", "result", "retain")
    value = SUT(identity, specification, "manifest-1")
    assert value.identity is identity
    assert value.specification is specification
    assert value.producer_manifest_id == "manifest-1"


def test_property__nested_field_delegation__returns_exact_views() -> None:
    """Evidence ID: SV-PROV-107

    Requirement: The four actual public properties delegate exactly to the nested
    represented fields.

    Method: Construct fixed nested public records and read artifact_id, logical_path,
    sha256, and byte_size.

    Oracle: The independently supplied nested field values fix every expected property
    result.

    Acceptance: The four-property tuple equals the four source-field values exactly.

    Interpretation: Failure indicates property delegation or public-property contract
    drift.

    Limitations: Synthetic values do not prove content, storage, scientific validity,
    UQ, or
    cross-language conformance.
    """
    value = SUT(
        ArtifactIdentity("artifact-1", "b" * 64, 8),
        ArtifactSpecification("out/a.json", "json", "result", "retain"),
        "manifest-1",
    )
    assert (value.artifact_id, value.logical_path, value.sha256, value.byte_size) == (
        "artifact-1",
        "out/a.json",
        "b" * 64,
        8,
    )


def test_field__reference_location_separation__excludes_location_fields() -> None:
    """Evidence ID: SV-PROV-007

    Requirement: Portable references contain no deployment root, location path, or
    external
    descriptor.

    Method: Inspect the public dataclass field inventory.

    Oracle: The human-approved ArtifactReference/ArtifactLocation separation fixes the
    exact
    field set.

    Acceptance: Fields are exactly identity, specification, and producer_manifest_id.

    Interpretation: Failure indicates a protected reference/location separation
    regression.

    Limitations: Reflection checks the declared public dataclass surface, not hostile
    runtime
    injection.
    """
    SUT(
        ArtifactIdentity("artifact-1", "b" * 64, 8),
        ArtifactSpecification("out/a", "json", "result", "retain"),
        "manifest-1",
    )
    assert tuple(field.name for field in fields(SUT)) == (
        "identity",
        "specification",
        "producer_manifest_id",
    )


def test_field__frozen_assignment__rejects_reassignment() -> None:
    """Evidence ID: SV-PROV-108

    Requirement: ArtifactReference is operationally immutable through ordinary field
    assignment.

    Method: Construct a valid reference and assign another valid producer manifest
    identifier.

    Oracle: The public frozen DataObject contract requires FrozenInstanceError.

    Acceptance: Reassignment raises FrozenInstanceError.

    Interpretation: Failure indicates mutable durable reference state or architecture
    drift.

    Limitations: Hostile reflection, content observation, validation, UQ, and
    cross-language
    claims are excluded.
    """
    value = SUT(
        ArtifactIdentity("artifact-1", "b" * 64, 8),
        ArtifactSpecification("out/a", "json", "result", "retain"),
        "manifest-1",
    )
    with pytest.raises(FrozenInstanceError):
        value.producer_manifest_id = "other"  # type: ignore[misc]


def test_constructor__nested_types__rejects_lookalikes() -> None:
    """Evidence ID: SV-PROV-008

    Requirement: Reference collaborators must be the exact accepted public record
    families rather
    than mappings or strings.

    Method: Pass dictionary and string lookalikes through the public constructor.

    Oracle: The public semantic type contract requires TypeError for both wrong
    collaborators.

    Acceptance: Each lookalike raises TypeError.

    Interpretation: Failure indicates unintended coercion or a stale contract.

    Limitations: User-defined subclasses are not partitioned separately.
    """
    identity = ArtifactIdentity("artifact-1", "b" * 64, 8)
    specification = ArtifactSpecification("out/a", "json", "result", "retain")
    with pytest.raises(TypeError):
        SUT({}, specification, "manifest-1")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT(identity, "out/a", "manifest-1")  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "producer_manifest_id",
    [
        pytest.param("", id="empty_identifier"),
        pytest.param("bad id", id="embedded_space"),
        pytest.param("e\u0301", id="non_nfc_identifier"),
        pytest.param("\ud800", id="unicode_surrogate"),
        pytest.param("a" * 129, id="overlength_identifier"),
    ],
)
def test_field__producer_manifest_identifier_values__reject_nonportable_text(
    producer_manifest_id: str,
) -> None:
    """Evidence ID: SV-PROV-086

    Requirement: producer_manifest_id is nonempty NFC text matching the bounded
    identifier grammar.

    Method: Construct with the named malformed producer identifier.

    Oracle: The public identifier grammar and NFC definition classify every literal.

    Acceptance: Construction raises ValueError.

    Interpretation: Failure admits a malformed producer relationship identifier.

    Limitations: Synthetic metadata only; scientific validation, UQ, physical
    correctness, and
    cross-language conformance are excluded.
    """
    identity = ArtifactIdentity("artifact-1", "b" * 64, 8)
    specification = ArtifactSpecification("out/a", "json", "result", "retain")
    with pytest.raises(ValueError):
        SUT(identity, specification, producer_manifest_id)


def test_field__producer_manifest_identifier_semantic_type__rejects_bytes() -> None:
    """Evidence ID: SV-PROV-116

    Requirement: producer_manifest_id requires a built-in string without bytes coercion.

    Method: Construct with bytes as the producer identifier.

    Oracle: The exact public semantic-type boundary classifies bytes.

    Acceptance: Construction raises TypeError.

    Interpretation: Failure indicates unintended producer-identifier coercion.

    Limitations: Synthetic metadata only; scientific validation, UQ, physical
    correctness, and
    cross-language conformance are excluded.
    """
    identity = ArtifactIdentity("artifact-1", "b" * 64, 8)
    specification = ArtifactSpecification("out/a", "json", "result", "retain")
    with pytest.raises(TypeError):
        SUT(identity, specification, b"manifest")  # type: ignore[arg-type]


def test_method__eq__includes_nested_and_producer_fields() -> None:
    """Evidence ID: SV-PROV-087

    Requirement: Reference equality is exact over identity, specification, and producer
    manifest.

    Method: Compare separately constructed equal values and a value with another
    producer.

    Oracle: Public frozen dataclass fields define exact equality without storage lookup.

    Acceptance: Equal represented fields compare equal and the producer change compares
    unequal.

    Interpretation: Failure indicates incomplete or identity-based reference equality.

    Limitations: Byte existence and semantic equivalence of producers are excluded.
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
