r"""Software verification of ``LineageRelation``.

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
    """Evidence ID
    SV-PROV-017
    Requirement
    A lineage relation preserves distinct directed parent and child identities and
    supporting provenance.
    Method
    Construct one representation edge and inspect every field.
    Oracle
    The accepted directed field mapping is exact and independent of production behavior.
    Acceptance
    All five fields equal the supplied values in parent-to-child orientation.
    Interpretation
    Failure indicates direction or field mapping drift.
    Limitations
    The semantic truth of the edge is not validated.
    """
    value = SUT("lineage-1", "parent", "child", LineageKind.REPRESENTATION, "prov-1")
    assert (
        value.lineage_id,
        value.parent_id,
        value.child_id,
        value.kind,
        value.provenance_id,
    ) == ("lineage-1", "parent", "child", LineageKind.REPRESENTATION, "prov-1")


def test_constructor__kind_and_distinct_endpoints__enforces_exact_contract() -> None:
    """Evidence ID
    SV-PROV-018
    Requirement
    Endpoints differ and kind is an exact LineageKind rather than a string.
    Method
    Construct a self-edge and a string-kind edge.
    Oracle
    Public intrinsic invariants determine ValueError and TypeError respectively.
    Acceptance
    Self-edge raises ValueError and string enum lookalike raises TypeError.
    Interpretation
    Failure indicates weakened lineage typing or direction invariants.
    Limitations
    Multi-edge cycles are not assessed.
    """
    with pytest.raises(ValueError):
        SUT("l", "same", "same", LineageKind.DERIVED, "p")
    with pytest.raises(TypeError):
        SUT("l", "a", "b", "derived", "p")  # type: ignore[arg-type]


def test_field__lineage_enum_values__match_version_one_vocabulary() -> None:
    """Evidence ID
    SV-PROV-019
    Requirement
    The complete lineage vocabulary is derived, representation, retry in declared order.
    Method
    Enumerate public LineageKind members and read their values.
    Oracle
    The accepted version-1 enum artifact fixes the exact tuple.
    Acceptance
    Values equal the three expected lowercase strings exactly.
    Interpretation
    Failure indicates a public or wire vocabulary change.
    Limitations
    Cross-language enum conformance is not claimed.
    """
    assert tuple(item.value for item in LineageKind) == (
        "derived",
        "representation",
        "retry",
    )


@pytest.mark.parametrize(
    "field", ["lineage_id", "parent_id", "child_id", "provenance_id"]
)
def test_field__lineage_identifiers__enforce_portable_contract(field: str) -> None:
    """Evidence ID
    SV-PROV-101
    Requirement
    Every lineage identifier is a built-in nonempty NFC bounded identifier.
    Method
    Replace each field independently with wrong-type and invalid-text representatives.
    Oracle
    The public identifier grammar and semantic type boundary classify each case.
    Acceptance
    Bytes raise TypeError and all invalid strings raise ValueError for every field.
    Interpretation
    Failure identifies incomplete owner-local validation of the named identity.
    Limitations
    Existence and global uniqueness of identifiers are excluded.
    """
    defaults: dict[str, object] = {
        "lineage_id": "lineage-1",
        "parent_id": "parent",
        "child_id": "child",
        "kind": LineageKind.DERIVED,
        "provenance_id": "prov-1",
    }
    for invalid in (b"id", "", "bad id", "e\u0301", "\ud800", "a" * 129):
        expected = TypeError if type(invalid) is bytes else ValueError
        with pytest.raises(expected):
            SUT(**(defaults | {field: invalid}))  # type: ignore[arg-type]


def test_property__immutable_exact_value_semantics__includes_direction_and_kind() -> (
    None
):
    """Evidence ID
    SV-PROV-102
    Requirement
    Lineage relations are frozen exact values including direction and kind.
    Method
    Compare equal constructions, reverse endpoints in another value, and reassign kind.
    Oracle
    The declared frozen dataclass fields define exact directional equality.
    Acceptance
    Equal edges compare equal, reversed edges differ, and reassignment is rejected.
    Interpretation
    Failure indicates lost direction, kind, or operational immutability.
    Limitations
    Graph equivalence and truth of the asserted relationship are excluded.
    """
    value = SUT("l", "parent", "child", LineageKind.DERIVED, "p")
    assert value == SUT("l", "parent", "child", LineageKind.DERIVED, "p")
    assert value != SUT("l", "child", "parent", LineageKind.DERIVED, "p")
    with pytest.raises(FrozenInstanceError):
        value.kind = LineageKind.RETRY  # type: ignore[misc]
