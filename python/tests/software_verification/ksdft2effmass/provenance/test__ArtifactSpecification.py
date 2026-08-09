r"""Software verification of ``ArtifactSpecification``.

Facet and represented meaning

-----------------------------
This module verifies portable artifact specification metadata, including the lexical
logical path and identifier-valued representation fields.

Intrinsic and cross-object scope

--------------------------------
``ArtifactSpecification`` is the sole SUT; path, metadata, immutability, and exact-value
invariants are owner-local, while artifact existence is excluded.

VVUQ and scientific exclusions

------------------------------
Evidence excludes filesystem resolution, numerical verification, scientific validation,
UQ, physical correctness, retention actions, and cross-language conformance.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.provenance import ArtifactSpecification

SUT = ArtifactSpecification
pytestmark = pytest.mark.software_verification


def test_constructor__field_mapping__preserves_portable_metadata() -> None:
    """Evidence ID: SV-PROV-004

    Requirement: The specification stores exactly logical path, format, semantic role,
    and
    retention policy.

    Method: Construct through the public import and inspect every represented field.

    Oracle: The accepted P2 four-field vocabulary fixes the expected tuple
    independently.

    Acceptance: The complete field tuple equals the supplied inputs exactly.

    Interpretation: Failure indicates constructor mapping, field-order, contract, or
    test-data drift.

    Limitations: Values are synthetic; storage, retention action, validation, UQ, and
    cross-language claims are excluded.
    """
    value = SUT("outputs/result.json", "json", "result", "retain")
    assert (
        value.logical_path,
        value.format,
        value.semantic_role,
        value.retention_policy,
    ) == ("outputs/result.json", "json", "result", "retain")


def test_field__frozen_assignment__rejects_reassignment() -> None:
    """Evidence ID: SV-PROV-106

    Requirement: ArtifactSpecification is operationally immutable through ordinary
    assignment.

    Method: Construct valid synthetic metadata and assign another valid format
    identifier.

    Oracle: The public frozen DataObject contract requires FrozenInstanceError.

    Acceptance: Assignment raises FrozenInstanceError.

    Interpretation: Failure indicates operational mutability or frozen-record
    architecture drift.

    Limitations: Hostile reflection, storage actions, validation, UQ, and cross-language
    claims
    are excluded.
    """
    value = SUT("outputs/result.json", "json", "result", "retain")
    with pytest.raises(FrozenInstanceError):
        value.format = "text"  # type: ignore[misc]


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
        pytest.param("CON.txt", id="windows_device_root"),
        pytest.param("dir/lpt1.log", id="windows_device_nested"),
        pytest.param("e\u0301/a", id="non_nfc_path"),
        pytest.param("a\u0085b", id="c1_control"),
        pytest.param("a\u2028b", id="unicode_line_control"),
        pytest.param("\ud800", id="unicode_surrogate"),
    ],
)
def test_constructor__root_relative_path__rejects_nonportable_forms(path: str) -> None:
    """Evidence ID: SV-PROV-005

    Requirement: Logical paths are nonempty NFC root-relative POSIX lexical paths
    without controls or
    Windows devices.

    Method: Attempt absolute, parent, backslash, drive, device, non-NFC, and C1-control
    paths.

    Oracle: The accepted H1/H2 lexical path partition incorporated by P2 is
    independently fixed.

    Acceptance: Every prohibited path raises ValueError; a nested POSIX path is
    accepted.

    Interpretation: Failure indicates a path-contract implementation or evidence defect.

    Limitations: No filesystem, symlink, case-folding filesystem, or URI behavior is
    exercised.
    """
    with pytest.raises(ValueError):
        SUT(path, "json", "result", "retain")


def test_constructor__root_relative_path__accepts_nested_posix_path() -> None:
    """Evidence ID: SV-PROV-138

    Requirement: A nested root-relative POSIX lexical logical path is accepted exactly.

    Method: Construct with the fixed valid path a/b and inspect the stored field.

    Oracle: The public lexical-path grammar independently classifies a/b as valid.

    Acceptance: Construction succeeds and logical_path equals a/b exactly.

    Interpretation: Failure rejects a valid portable logical path or changes field
    mapping.

    Limitations: No filesystem resolution, scientific validation, UQ, or cross-language
    conformance is established.
    """
    assert SUT("a/b", "json", "result", "retain").logical_path == "a/b"


def test_field__logical_path_semantic_type__rejects_non_string_values() -> None:
    """Evidence ID: SV-PROV-083

    Requirement: logical_path requires a built-in string without iterable or path-object
    coercion.

    Method: Pass bytes through the public constructor while all metadata fields remain
    valid.

    Oracle: The documented semantic type boundary classifies bytes as TypeError.

    Acceptance: Construction raises TypeError.

    Interpretation: Failure indicates implicit path coercion at a durable boundary.

    Limitations: Filesystem path resolution and existence are excluded.
    """
    with pytest.raises(TypeError):
        SUT(b"a/b", "json", "result", "retain")  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field",
    [
        pytest.param("format", id="format_identifier"),
        pytest.param("semantic_role", id="semantic_role_identifier"),
        pytest.param("retention_policy", id="retention_policy_identifier"),
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
def test_field__metadata_identifier_values__reject_nonportable_text(
    field: str, invalid: str
) -> None:
    """Evidence ID: SV-PROV-084

    Requirement: Each metadata identifier is nonempty NFC text matching the bounded
    grammar.

    Method: Replace the named public field with the named malformed string.

    Oracle: The published identifier grammar and NFC definition classify every literal.

    Acceptance: Construction raises ValueError.

    Interpretation: Failure admits malformed durable specification metadata.

    Limitations: Synthetic metadata only; scientific validation, UQ, physical
    correctness, and
    cross-language conformance are excluded.
    """
    values: dict[str, object] = {
        "logical_path": "out/a",
        "format": "json",
        "semantic_role": "result",
        "retention_policy": "retain",
    }
    with pytest.raises(ValueError):
        SUT(**(values | {field: invalid}))  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field",
    [
        pytest.param("format", id="format_identifier"),
        pytest.param("semantic_role", id="semantic_role_identifier"),
        pytest.param("retention_policy", id="retention_policy_identifier"),
    ],
)
def test_field__metadata_identifier_semantic_types__reject_bytes(field: str) -> None:
    """Evidence ID: SV-PROV-115

    Requirement: Each metadata identifier requires a built-in string without bytes
    coercion.

    Method: Replace the named public field with bytes.

    Oracle: The exact public semantic-type boundary classifies bytes.

    Acceptance: Construction raises TypeError.

    Interpretation: Failure indicates unintended metadata coercion or missing type
    validation.

    Limitations: Synthetic metadata only; scientific validation, UQ, physical
    correctness, and
    cross-language conformance are excluded.
    """
    values: dict[str, object] = {
        "logical_path": "out/a",
        "format": "json",
        "semantic_role": "result",
        "retention_policy": "retain",
    }
    with pytest.raises(TypeError):
        SUT(**(values | {field: b"json"}))  # type: ignore[arg-type]


def test_method__eq__compares_all_represented_fields() -> None:
    """Evidence ID: SV-PROV-085

    Requirement: ArtifactSpecification equality distinguishes an otherwise equal value
    when its
    semantic role differs.

    Method: Compare identical constructions and one construction with a different role.

    Oracle: Frozen dataclass value semantics over declared fields provide the acceptance
    oracle.

    Acceptance: Identical values compare equal and the changed role compares unequal.

    Interpretation: Failure indicates equality omits or transforms represented metadata.

    Limitations: Semantic equivalence between distinct format or role identifiers is
    excluded.
    """
    value = SUT("out/a", "json", "result", "retain")
    assert value == SUT("out/a", "json", "result", "retain")
    assert value != SUT("out/a", "json", "diagnostic", "retain")
