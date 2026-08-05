"""Evidence class and represented meaning
Software verification of directed immutable lineage edges.
Owned contract, oracle, and scope
LineageRelation is the SUT; direction, enum vocabulary, and intrinsic edge rules are the
oracle.
VVUQ and scientific exclusions
Evidence excludes lineage truth, graph analysis, numerical verification, scientific
validation, UQ, and cross-language conformance.
"""

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
