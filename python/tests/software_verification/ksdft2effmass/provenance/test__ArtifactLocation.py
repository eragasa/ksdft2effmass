"""Evidence class and represented meaning
Software verification of immutable deployment-location alternatives.
Owned contract, oracle, and scope
ArtifactLocation is the SUT; the approved reference/location separation and tagged
alternatives are the oracle.
VVUQ and scientific exclusions
Evidence excludes resolver I/O, numerical verification, scientific validation, UQ,
physical correctness, and cross-language conformance.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.provenance import ArtifactLocation, ArtifactLocationKind

SUT = ArtifactLocation
pytestmark = pytest.mark.software_verification


def test_constructor__tagged_location_forms__maps_exclusive_fields() -> None:
    """Evidence ID
    SV-PROV-009
    Requirement
    Locations use either explicit root-relative coordinates or one opaque external
    descriptor.
    Method
    Construct both public enum-tagged alternatives and inspect every field.
    Oracle
    The accepted P2 disjoint tagged representation fixes exact null and non-null fields.
    Acceptance
    Both alternatives equal the expected five-field tuples exactly.
    Interpretation
    Failure indicates mapping or representation-separation drift.
    Limitations
    Roots and descriptors are not resolved.
    """
    root = SUT("a", ArtifactLocationKind.ROOT_RELATIVE, "root-1", "out/a", None)
    external = SUT("a", ArtifactLocationKind.EXTERNAL_DESCRIPTOR, None, None, "store-1")
    assert (root.root_id, root.path, root.external_descriptor_id) == (
        "root-1",
        "out/a",
        None,
    )
    assert (external.root_id, external.path, external.external_descriptor_id) == (
        None,
        None,
        "store-1",
    )


def test_constructor__kind_and_exclusivity__rejects_strings_and_mixed_forms() -> None:
    """Evidence ID
    SV-PROV-010
    Requirement
    The discriminator is an exact enum and fields from the two forms cannot be mixed or
    omitted.
    Method
    Pass a string discriminator, incomplete root form, and mixed external form.
    Oracle
    Public semantic typing and the approved tagged-union invariant determine the
    exceptions.
    Acceptance
    String kind raises TypeError; incomplete or mixed forms raise TypeError or
    ValueError at their documented boundary.
    Interpretation
    Failure indicates coercion or weakened location separation.
    Limitations
    Only representative invalid members of each semantic partition are used.
    """
    with pytest.raises(TypeError):
        SUT("a", "root_relative", "root", "a")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT("a", ArtifactLocationKind.ROOT_RELATIVE, None, "a")
    with pytest.raises(ValueError):
        SUT("a", ArtifactLocationKind.EXTERNAL_DESCRIPTOR, "root", None, "external")


def test_field__enum_values_and_immutability__are_exact() -> None:
    """Evidence ID
    SV-PROV-011
    Requirement
    Location enum wire values are exact and location records are frozen.
    Method
    Assert the complete enum value tuple and attempt ordinary mutation.
    Oracle
    The version-1 closed vocabulary contains root_relative then external_descriptor.
    Acceptance
    Enum values match exactly and reassignment raises FrozenInstanceError.
    Interpretation
    Failure indicates enum drift or mutability.
    Limitations
    No schema or cross-language runtime is exercised here.
    """
    assert tuple(member.value for member in ArtifactLocationKind) == (
        "root_relative",
        "external_descriptor",
    )
    value = SUT(
        "a", ArtifactLocationKind.EXTERNAL_DESCRIPTOR, external_descriptor_id="x"
    )
    with pytest.raises(FrozenInstanceError):
        value.artifact_id = "b"  # type: ignore[misc]
