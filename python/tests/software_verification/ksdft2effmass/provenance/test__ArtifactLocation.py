r"""Software verification of ``ArtifactLocation``.

Facet and represented meaning
-----------------------------
This module verifies immutable root-relative and external-descriptor deployment-location
alternatives and their disjoint represented fields.

Intrinsic and cross-object scope
--------------------------------
``ArtifactLocation`` is the sole SUT; tagged-form, identifier, lexical-path,
immutability, and equality invariants are intrinsic. Root and descriptor resolution are
excluded.

VVUQ and scientific exclusions
------------------------------
Evidence excludes resolver I/O, storage observation, numerical verification, scientific
validation, UQ, physical correctness, and cross-language conformance.
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
        SUT("a", ArtifactLocationKind.ROOT_RELATIVE, "root", "a", "external")
    with pytest.raises(ValueError):
        SUT("a", ArtifactLocationKind.EXTERNAL_DESCRIPTOR, "root", None, "external")
    with pytest.raises(ValueError):
        SUT("a", ArtifactLocationKind.EXTERNAL_DESCRIPTOR, None, "a", "external")


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


@pytest.mark.parametrize("field", ["artifact_id", "root_id"])
def test_field__root_location_identifiers__enforce_portable_contract(
    field: str,
) -> None:
    """Evidence ID
    SV-PROV-088
    Requirement
    Root-relative artifact and root identifiers are built-in, nonempty NFC identifiers.
    Method
    Replace each identifier with representative wrong-type and invalid text values.
    Oracle
    The public identifier grammar defines the complete accepted scalar form.
    Acceptance
    Bytes raise TypeError and all invalid strings raise ValueError for both fields.
    Interpretation
    Failure indicates a branch-specific identifier validation gap.
    Limitations
    Identifier existence or authorization is not checked.
    """
    defaults: dict[str, object] = {
        "artifact_id": "artifact-1",
        "kind": ArtifactLocationKind.ROOT_RELATIVE,
        "root_id": "root-1",
        "path": "out/a",
    }
    for invalid in (b"id", "", "bad id", "e\u0301", "\ud800", "a" * 129):
        values = defaults | {field: invalid}
        expected = TypeError if type(invalid) is bytes else ValueError
        with pytest.raises(expected):
            SUT(**values)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "path",
    [
        "",
        "/a",
        "../a",
        "a/./b",
        "a//b",
        "a/",
        "a\\b",
        "C:/a",
        "NUL.dat",
        "dir/com1.txt",
        "e\u0301/a",
        "a\u0085b",
        "a\u2029b",
        "\ud800",
    ],
)
def test_field__root_relative_path__rejects_nonportable_lexical_forms(
    path: str,
) -> None:
    """Evidence ID
    SV-PROV-089
    Requirement
    Root-relative locations use nonempty NFC POSIX lexical paths without controls,
    traversal, drive syntax, backslashes, or Windows device components.
    Method
    Construct the root-relative branch with one representative of each prohibited form.
    Oracle
    The accepted lexical path grammar independently classifies each literal.
    Acceptance
    Every prohibited path raises ValueError.
    Interpretation
    Failure permits a nonportable deployment location.
    Limitations
    No filesystem, symlink, or root resolution occurs.
    """
    with pytest.raises(ValueError):
        SUT("artifact-1", ArtifactLocationKind.ROOT_RELATIVE, "root-1", path)


def test_field__root_relative_path_semantic_type__rejects_non_string_values() -> None:
    """Evidence ID
    SV-PROV-090
    Requirement
    A root-relative path requires a built-in string without coercion.
    Method
    Supply bytes as path with an otherwise complete root-relative branch.
    Oracle
    The public semantic type boundary requires TypeError.
    Acceptance
    Construction raises TypeError.
    Interpretation
    Failure indicates implicit path coercion.
    Limitations
    Other non-string types are represented by bytes.
    """
    with pytest.raises(TypeError):
        SUT("artifact-1", ArtifactLocationKind.ROOT_RELATIVE, "root-1", b"out/a")  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("descriptor", "exception"),
    [
        (None, TypeError),
        (b"store", TypeError),
        ("", ValueError),
        ("bad id", ValueError),
        ("e\u0301", ValueError),
        ("\ud800", ValueError),
        ("a" * 129, ValueError),
    ],
)
def test_field__external_descriptor_identifier__rejects_missing_or_nonportable_values(
    descriptor: object, exception: type[Exception]
) -> None:
    """Evidence ID
    SV-PROV-091
    Requirement
    The external branch requires exactly one built-in nonempty NFC descriptor
    identifier.
    Method
    Supply missing, wrong-type, and invalid-text descriptors with other branch fields
    absent.
    Oracle
    The tagged representation and identifier grammar classify each case.
    Acceptance
    Each construction raises the documented exception class.
    Interpretation
    Failure weakens external-location identity or branch completeness.
    Limitations
    Descriptor authorization and resolution remain external concerns.
    """
    with pytest.raises(exception):
        SUT(
            "artifact-1",
            ArtifactLocationKind.EXTERNAL_DESCRIPTOR,
            external_descriptor_id=descriptor,  # type: ignore[arg-type]
        )


def test_property__exact_value_semantics__includes_tag_and_branch_payload() -> None:
    """Evidence ID
    SV-PROV-092
    Requirement
    ArtifactLocation equality is exact over the discriminator and all branch fields.
    Method
    Compare two equal root-relative values and a distinct external value.
    Oracle
    Frozen dataclass fields define exact represented equality.
    Acceptance
    Equal branch values compare equal and different branches compare unequal.
    Interpretation
    Failure indicates incomplete tagged-value semantics.
    Limitations
    Different locations resolving to the same bytes are not semantically aligned.
    """
    value = SUT("a", ArtifactLocationKind.ROOT_RELATIVE, "root", "out/a")
    assert value == SUT("a", ArtifactLocationKind.ROOT_RELATIVE, "root", "out/a")
    assert value != SUT(
        "a", ArtifactLocationKind.EXTERNAL_DESCRIPTOR, external_descriptor_id="store"
    )
