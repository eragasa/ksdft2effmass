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


def test_constructor__field_mapping_and_immutability__preserves_portable_metadata() -> (
    None
):
    """Evidence ID
    SV-PROV-004
    Requirement
    The specification stores exactly logical path, format, semantic role, and retention
    policy and is frozen.
    Method
    Construct through the public import, inspect fields, and attempt reassignment.
    Oracle
    The accepted P2 field vocabulary and frozen DataObject rule are exact.
    Acceptance
    The field tuple equals the inputs and reassignment raises FrozenInstanceError.
    Interpretation
    Failure indicates field drift or operational mutability.
    Limitations
    Values are synthetic metadata; no storage or retention action occurs.
    """
    value = SUT("outputs/result.json", "json", "result", "retain")
    assert (
        value.logical_path,
        value.format,
        value.semantic_role,
        value.retention_policy,
    ) == (
        "outputs/result.json",
        "json",
        "result",
        "retain",
    )
    with pytest.raises(FrozenInstanceError):
        value.format = "text"  # type: ignore[misc]


def test_constructor__root_relative_path__rejects_nonportable_forms() -> None:
    """Evidence ID
    SV-PROV-005
    Requirement
    Logical paths are nonempty NFC root-relative POSIX lexical paths without controls or
    Windows devices.
    Method
    Attempt absolute, parent, backslash, drive, device, non-NFC, and C1-control paths.
    Oracle
    The accepted H1/H2 lexical path partition incorporated by P2 is independently fixed.
    Acceptance
    Every prohibited path raises ValueError; a nested POSIX path is accepted.
    Interpretation
    Failure indicates a path-contract implementation or evidence defect.
    Limitations
    No filesystem, symlink, case-folding filesystem, or URI behavior is exercised.
    """
    assert SUT("a/b", "json", "result", "retain").logical_path == "a/b"
    for path in (
        "",
        "/a",
        "../a",
        "a/./b",
        "a//b",
        "a/",
        "a\\b",
        "C:/a",
        "CON.txt",
        "dir/lpt1.log",
        "e\u0301/a",
        "a\u0085b",
        "a\u2028b",
        "\ud800",
    ):
        with pytest.raises(ValueError):
            SUT(path, "json", "result", "retain")


def test_field__logical_path_semantic_type__rejects_non_string_values() -> None:
    """Evidence ID
    SV-PROV-083
    Requirement
    logical_path requires a built-in string without iterable or path-object coercion.
    Method
    Pass bytes through the public constructor while all metadata fields remain valid.
    Oracle
    The documented semantic type boundary classifies bytes as TypeError.
    Acceptance
    Construction raises TypeError.
    Interpretation
    Failure indicates implicit path coercion at a durable boundary.
    Limitations
    Filesystem path resolution and existence are excluded.
    """
    with pytest.raises(TypeError):
        SUT(b"a/b", "json", "result", "retain")  # type: ignore[arg-type]


@pytest.mark.parametrize("field", ["format", "semantic_role", "retention_policy"])
def test_field__metadata_identifier__enforces_type_and_portability(field: str) -> None:
    """Evidence ID
    SV-PROV-084
    Requirement
    Every metadata identifier is a built-in, nonempty, NFC bounded identifier.
    Method
    Replace each field with bytes, empty, spaced, decomposed, surrogate, and overlength
    values while holding the other public fields fixed.
    Oracle
    The common public identifier grammar independently defines invalid partitions.
    Acceptance
    Bytes raise TypeError and every invalid string raises ValueError for every field.
    Interpretation
    Failure identifies incomplete owner-local validation for the named field.
    Limitations
    Identifier registries and semantic-role truth are not assessed.
    """
    defaults: dict[str, object] = {
        "logical_path": "out/a",
        "format": "json",
        "semantic_role": "result",
        "retention_policy": "retain",
    }
    for invalid in (b"json", "", "bad id", "e\u0301", "\ud800", "a" * 129):
        values = defaults | {field: invalid}
        expected = TypeError if type(invalid) is bytes else ValueError
        with pytest.raises(expected):
            SUT(**values)  # type: ignore[arg-type]


def test_property__exact_value_semantics__compares_all_represented_fields() -> None:
    """Evidence ID
    SV-PROV-085
    Requirement
    ArtifactSpecification equality is exact over all four immutable fields.
    Method
    Compare identical constructions and one construction with a different role.
    Oracle
    Frozen dataclass value semantics over declared fields provide the acceptance oracle.
    Acceptance
    Identical values compare equal and the changed role compares unequal.
    Interpretation
    Failure indicates equality omits or transforms represented metadata.
    Limitations
    Semantic equivalence between distinct format or role identifiers is excluded.
    """
    value = SUT("out/a", "json", "result", "retain")
    assert value == SUT("out/a", "json", "result", "retain")
    assert value != SUT("out/a", "json", "diagnostic", "retain")
