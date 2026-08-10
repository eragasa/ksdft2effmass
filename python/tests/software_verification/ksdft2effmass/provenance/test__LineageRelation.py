r"""Software verification of ``LineageRelation``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

-----------------------------
This module verifies one immutable directed parent-to-child lineage edge, its kind, and
its supporting provenance identity.

Intrinsic and cross-object scope

--------------------------------
``LineageRelation`` is the sole SUT; identifier, enum, distinct-endpoint, immutability,
and exact-value rules are intrinsic. Provenance existence and graph analysis are
excluded.

VVUQ and scientific exclusions

------------------------------
Evidence excludes lineage truth, graph analysis, numerical verification, scientific
validation, UQ, physical correctness, and cross-language conformance.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.provenance import LineageKind, LineageRelation

SUT = LineageRelation
pytestmark = pytest.mark.software_verification


def test_constructor__directed_lineage_fields__maps_parent_to_child() -> None:
    """Evidence ID: SV-PROV-017

    Requirement: A lineage relation preserves distinct directed parent and child
    identities and
    supporting provenance.

    Method: Construct one representation edge and inspect every field.

    Oracle: The accepted directed field mapping is exact and independent of production
    behavior.

    Acceptance: All five fields equal the supplied values in parent-to-child
    orientation.

    Interpretation: Failure indicates direction or field mapping drift.

    Limitations: The semantic truth of the edge is not validated.
    """
    value = SUT("lineage-1", "parent", "child", LineageKind.REPRESENTATION, "prov-1")
    assert (
        value.lineage_id,
        value.parent_id,
        value.child_id,
        value.kind,
        value.provenance_id,
    ) == ("lineage-1", "parent", "child", LineageKind.REPRESENTATION, "prov-1")


def test_constructor__distinct_endpoints__rejects_self_edge() -> None:
    """Evidence ID: SV-PROV-018

    Requirement: A lineage parent and child must differ.

    Method: Construct a derived relation with identical endpoint literals.

    Oracle: Exact equality of the public endpoint inputs supplies the oracle.

    Acceptance: Construction raises ValueError.

    Interpretation: Failure permits a directed lineage self-edge.

    Limitations: Synthetic metadata only; scientific validation, UQ, physical
    correctness, and
    cross-language conformance are excluded.
    """
    with pytest.raises(ValueError):
        SUT("l", "same", "same", LineageKind.DERIVED, "p")


def test_constructor__kind_semantic_type__rejects_string_lookalike() -> None:
    """Evidence ID: SV-PROV-133

    Requirement: kind requires a LineageKind member rather than its wire string.

    Method: Construct with the string derived as kind.

    Oracle: The public enum semantic-type contract classifies the string.

    Acceptance: Construction raises TypeError.

    Interpretation: Failure indicates unintended lineage-kind coercion.

    Limitations: Synthetic metadata only; scientific validation, UQ, physical
    correctness, and
    cross-language conformance are excluded.
    """
    with pytest.raises(TypeError):
        SUT("l", "a", "b", "derived", "p")  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field",
    [
        pytest.param("lineage_id", id="lineage_identifier"),
        pytest.param("parent_id", id="parent_identifier"),
        pytest.param("child_id", id="child_identifier"),
        pytest.param("provenance_id", id="provenance_identifier"),
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
def test_field__lineage_identifier_values__reject_nonportable_text(
    field: str, invalid: str
) -> None:
    """Evidence ID: SV-PROV-101

    Requirement: Every lineage identifier is nonempty NFC text matching the bounded
    grammar.

    Method: Replace the named identifier with the named malformed string.

    Oracle: The identifier grammar and NFC definition classify each literal.

    Acceptance: Construction raises ValueError.

    Interpretation: Failure admits malformed lineage identity metadata.

    Limitations: Synthetic metadata only; scientific validation, UQ, physical
    correctness, and
    cross-language conformance are excluded.
    """
    values: dict[str, object] = {
        "lineage_id": "lineage-1",
        "parent_id": "parent",
        "child_id": "child",
        "kind": LineageKind.DERIVED,
        "provenance_id": "prov-1",
    }
    with pytest.raises(ValueError):
        SUT(**(values | {field: invalid}))  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field",
    [
        pytest.param("lineage_id", id="lineage_identifier"),
        pytest.param("parent_id", id="parent_identifier"),
        pytest.param("child_id", id="child_identifier"),
        pytest.param("provenance_id", id="provenance_identifier"),
    ],
)
def test_field__lineage_identifier_semantic_types__reject_bytes(field: str) -> None:
    """Evidence ID: SV-PROV-134

    Requirement: Every lineage identifier requires a built-in string.

    Method: Replace the named identifier with bytes.

    Oracle: The exact semantic-type contract classifies bytes.

    Acceptance: Construction raises TypeError.

    Interpretation: Failure indicates unintended lineage identifier coercion.

    Limitations: Synthetic metadata only; scientific validation, UQ, physical
    correctness, and
    cross-language conformance are excluded.
    """
    values: dict[str, object] = {
        "lineage_id": "lineage-1",
        "parent_id": "parent",
        "child_id": "child",
        "kind": LineageKind.DERIVED,
        "provenance_id": "prov-1",
    }
    with pytest.raises(TypeError):
        SUT(**(values | {field: b"id"}))  # type: ignore[arg-type]


def test_method__eq__includes_direction_and_kind() -> None:
    """Evidence ID: SV-PROV-102

    Requirement: Lineage relation equality is exact including direction and kind.

    Method: Compare equal constructions and reverse endpoints in another value.

    Oracle: The declared frozen dataclass fields define exact directional equality.

    Acceptance: Equal edges compare equal and reversed edges compare unequal.

    Interpretation: Failure indicates lost direction, kind, or incomplete equality
    semantics.

    Limitations: Graph equivalence and truth of the asserted relationship are excluded.
    """
    value = SUT("l", "parent", "child", LineageKind.DERIVED, "p")
    assert value == SUT("l", "parent", "child", LineageKind.DERIVED, "p")
    assert value != SUT("l", "child", "parent", LineageKind.DERIVED, "p")


def test_field__frozen_assignment__rejects_reassignment() -> None:
    """Evidence ID: SV-PROV-113

    Requirement: LineageRelation is operationally immutable through ordinary field
    assignment.

    Method: Construct a valid edge and assign another valid LineageKind member.

    Oracle: The public frozen DataObject contract requires FrozenInstanceError.

    Acceptance: Reassignment raises FrozenInstanceError.

    Interpretation: Failure indicates mutable lineage state or frozen-record
    architecture drift.

    Limitations: Hostile reflection, lineage truth, validation, UQ, and cross-language
    claims are
    excluded.
    """
    value = SUT("l", "parent", "child", LineageKind.DERIVED, "p")
    with pytest.raises(FrozenInstanceError):
        value.kind = LineageKind.RETRY  # type: ignore[misc]
