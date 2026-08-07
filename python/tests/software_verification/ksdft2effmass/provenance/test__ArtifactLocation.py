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


def test_constructor__kind_semantic_type__rejects_string_lookalike() -> None:
    """Evidence ID
    SV-PROV-010
    Requirement
    kind requires an ArtifactLocationKind member rather than its wire string.
    Method
    Construct a root location with the string root_relative.
    Oracle
    The public enum semantic-type contract classifies the string.
    Acceptance
    Construction raises TypeError.
    Interpretation
    Failure indicates unintended discriminator coercion.
    Limitations
    Synthetic metadata only; scientific validation, UQ, physical correctness, and
    cross-language conformance are excluded.
    """
    with pytest.raises(TypeError):
        SUT("a", "root_relative", "root", "a")  # type: ignore[arg-type]


def test_constructor__root_branch_completeness__requires_root_identifier() -> None:
    """Evidence ID
    SV-PROV-117
    Requirement
    The root-relative alternative requires a built-in root_id.
    Method
    Construct the root branch with root_id absent and a valid path.
    Oracle
    The tagged representation requires the root coordinate.
    Acceptance
    Construction raises TypeError.
    Interpretation
    Failure permits an incomplete root-relative location.
    Limitations
    Synthetic metadata only; scientific validation, UQ, physical correctness, and
    cross-language conformance are excluded.
    """
    with pytest.raises(TypeError):
        SUT("a", ArtifactLocationKind.ROOT_RELATIVE, None, "a")


@pytest.mark.parametrize(
    ("kind", "root_id", "path", "descriptor"),
    [
        pytest.param(
            ArtifactLocationKind.ROOT_RELATIVE,
            "root",
            "a",
            "external",
            id="descriptor_on_root_branch",
        ),
        pytest.param(
            ArtifactLocationKind.EXTERNAL_DESCRIPTOR,
            "root",
            None,
            "external",
            id="root_identifier_on_external_branch",
        ),
        pytest.param(
            ArtifactLocationKind.EXTERNAL_DESCRIPTOR,
            None,
            "a",
            "external",
            id="path_on_external_branch",
        ),
    ],
)
def test_constructor__branch_exclusivity__rejects_mixed_fields(
    kind: ArtifactLocationKind, root_id: str | None, path: str | None, descriptor: str
) -> None:
    """Evidence ID
    SV-PROV-118
    Requirement
    Location alternatives reject fields belonging to the other tagged branch.
    Method
    Construct the named mixed-field alternative.
    Oracle
    The approved disjoint tagged representation fixes absent fields.
    Acceptance
    Construction raises ValueError.
    Interpretation
    Failure weakens ArtifactLocation branch separation.
    Limitations
    Synthetic metadata only; scientific validation, UQ, physical correctness, and
    cross-language conformance are excluded.
    """
    with pytest.raises(ValueError):
        SUT("a", kind, root_id, path, descriptor)


def test_field__frozen_assignment__rejects_reassignment() -> None:
    """Evidence ID
    SV-PROV-109
    Requirement
    ArtifactLocation is operationally immutable through ordinary field assignment.
    Method
    Construct the external-descriptor alternative and assign another valid artifact ID.
    Oracle
    The public frozen DataObject contract requires FrozenInstanceError.
    Acceptance
    Reassignment raises FrozenInstanceError.
    Interpretation
    Failure indicates mutable location metadata or frozen-record architecture drift.
    Limitations
    Hostile reflection, descriptor resolution, validation, UQ, and cross-language
    claims are excluded.
    """
    value = SUT(
        "a", ArtifactLocationKind.EXTERNAL_DESCRIPTOR, external_descriptor_id="x"
    )
    with pytest.raises(FrozenInstanceError):
        value.artifact_id = "b"  # type: ignore[misc]


@pytest.mark.parametrize(
    "field",
    [
        pytest.param("artifact_id", id="artifact_identifier"),
        pytest.param("root_id", id="root_identifier"),
    ],
)
@pytest.mark.parametrize(
    "invalid",
    [
        pytest.param("", id="empty_identifier"),
        pytest.param("bad id", id="embedded_space"),
        pytest.param("e\u0301", id="non_nfc_identifier"),
        pytest.param("\ud800", id="unicode_surrogate"),
        pytest.param("a" * 129, id="overlength_identifier"),
    ],
)
def test_field__root_location_identifier_values__reject_nonportable_text(
    field: str, invalid: str
) -> None:
    """Evidence ID
    SV-PROV-088
    Requirement
    Root-branch artifact and root identifiers are nonempty NFC bounded identifiers.
    Method
    Replace the named identifier with the named malformed string.
    Oracle
    The public identifier grammar and NFC definition classify each literal.
    Acceptance
    Construction raises ValueError.
    Interpretation
    Failure admits malformed root-location identity metadata.
    Limitations
    Synthetic metadata only; scientific validation, UQ, physical correctness, and
    cross-language conformance are excluded.
    """
    values: dict[str, object] = {
        "artifact_id": "artifact-1",
        "kind": ArtifactLocationKind.ROOT_RELATIVE,
        "root_id": "root-1",
        "path": "out/a",
    }
    with pytest.raises(ValueError):
        SUT(**(values | {field: invalid}))  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field",
    [
        pytest.param("artifact_id", id="artifact_identifier"),
        pytest.param("root_id", id="root_identifier"),
    ],
)
def test_field__root_location_identifier_semantic_types__reject_bytes(
    field: str,
) -> None:
    """Evidence ID
    SV-PROV-119
    Requirement
    Root-branch artifact and root identifiers require built-in strings.
    Method
    Replace the named identifier with bytes.
    Oracle
    The exact semantic-type boundary classifies bytes.
    Acceptance
    Construction raises TypeError.
    Interpretation
    Failure indicates unintended root-location identifier coercion.
    Limitations
    Synthetic metadata only; scientific validation, UQ, physical correctness, and
    cross-language conformance are excluded.
    """
    values: dict[str, object] = {
        "artifact_id": "artifact-1",
        "kind": ArtifactLocationKind.ROOT_RELATIVE,
        "root_id": "root-1",
        "path": "out/a",
    }
    with pytest.raises(TypeError):
        SUT(**(values | {field: b"id"}))  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "path",
    [
        pytest.param("", id="empty_path"),
        pytest.param("/a", id="absolute_posix_path"),
        pytest.param("../a", id="parent_traversal"),
        pytest.param("a/./b", id="dot_component"),
        pytest.param("a//b", id="repeated_separator"),
        pytest.param("a/", id="trailing_separator"),
        pytest.param("a\\b", id="backslash_separator"),
        pytest.param("C:/a", id="windows_drive_path"),
        pytest.param("NUL.dat", id="windows_device_root"),
        pytest.param("dir/com1.txt", id="windows_device_nested"),
        pytest.param("e\u0301/a", id="non_nfc_path"),
        pytest.param("a\u0085b", id="c1_control"),
        pytest.param("a\u2029b", id="unicode_line_control"),
        pytest.param("\ud800", id="unicode_surrogate"),
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
    "descriptor",
    [
        pytest.param("", id="empty_identifier"),
        pytest.param("bad id", id="embedded_space"),
        pytest.param("e\u0301", id="non_nfc_identifier"),
        pytest.param("\ud800", id="unicode_surrogate"),
        pytest.param("a" * 129, id="overlength_identifier"),
    ],
)
def test_field__external_descriptor_identifier_values__reject_nonportable_text(
    descriptor: str,
) -> None:
    """Evidence ID
    SV-PROV-091
    Requirement
    An external descriptor is nonempty NFC text matching the bounded identifier grammar.
    Method
    Construct the external branch with the named malformed string.
    Oracle
    The public identifier grammar and NFC definition classify each literal.
    Acceptance
    Construction raises ValueError.
    Interpretation
    Failure admits malformed external-location metadata.
    Limitations
    Synthetic metadata only; scientific validation, UQ, physical correctness, and
    cross-language conformance are excluded.
    """
    with pytest.raises(ValueError):
        SUT(
            "artifact-1",
            ArtifactLocationKind.EXTERNAL_DESCRIPTOR,
            external_descriptor_id=descriptor,
        )


def test_field__external_descriptor_presence__rejects_missing_value() -> None:
    """Evidence ID
    SV-PROV-120
    Requirement
    The external branch requires external_descriptor_id to be present.
    Method
    Construct the external branch with the descriptor absent.
    Oracle
    The tagged representation requires its sole branch payload.
    Acceptance
    Construction raises TypeError.
    Interpretation
    Failure permits an incomplete external location.
    Limitations
    Synthetic metadata only; scientific validation, UQ, physical correctness, and
    cross-language conformance are excluded.
    """
    with pytest.raises(TypeError):
        SUT(
            "artifact-1",
            ArtifactLocationKind.EXTERNAL_DESCRIPTOR,
            external_descriptor_id=None,
        )


def test_field__external_descriptor_semantic_type__rejects_bytes() -> None:
    """Evidence ID
    SV-PROV-121
    Requirement
    external_descriptor_id requires a built-in string.
    Method
    Construct the external branch with a bytes descriptor.
    Oracle
    The exact semantic-type boundary classifies bytes.
    Acceptance
    Construction raises TypeError.
    Interpretation
    Failure indicates unintended descriptor coercion.
    Limitations
    Synthetic metadata only; scientific validation, UQ, physical correctness, and
    cross-language conformance are excluded.
    """
    with pytest.raises(TypeError):
        SUT(
            "artifact-1",
            ArtifactLocationKind.EXTERNAL_DESCRIPTOR,
            external_descriptor_id=b"store",  # type: ignore[arg-type]
        )


def test_method__eq__includes_tag_and_branch_payload() -> None:
    """Evidence ID
    SV-PROV-092
    Requirement
    ArtifactLocation equality distinguishes otherwise equal values using different
    branch discriminators and payloads.
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
