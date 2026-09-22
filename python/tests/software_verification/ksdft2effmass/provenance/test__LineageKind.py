r"""Software verification of ``LineageKind``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

-----------------------------
This class-owned software evidence verifies the exact closed version-1 lineage
vocabulary: ``DERIVED`` maps to ``derived``, ``REPRESENTATION`` maps to
``representation``, and ``RETRY`` maps to ``retry``. ``DERIVED`` classifies a
child derived from a parent; ``REPRESENTATION`` classifies a child that is a
distinct representation of parent content; and ``RETRY`` classifies a new
attempt descended from a failed parent attempt.

Intrinsic and cross-object scope

--------------------------------
The sole primary SUT is ``LineageKind``. Exact fixed names, wire values,
declaration order, and Python ``StrEnum`` lookup behavior provide the oracles.
The enum classifies one lineage-edge kind only. It does not validate parent or
child identities, reject self-edges, prove derivation or representation
equivalence, prove that a retry parent failed, authorize retry, or enforce
graph-wide acyclicity.

VVUQ and scientific exclusions

------------------------------
Passing establishes only the stated enum vocabulary and lookup behavior; failure
identifies production vocabulary, test oracle, or accepted-contract drift. The
enum does not establish numerical verification, scientific validation, UQ,
provenance truth, physical correctness, portability beyond the declared
vocabulary, or cross-language agreement.
"""

from enum import StrEnum

import pytest

from ksdft2effmass.provenance import LineageKind

SUT = LineageKind
pytestmark = pytest.mark.software_verification


def test_field__wire_vocabulary__has_exact_order_names_values_and_count() -> None:
    """Evidence ID: SV-PROV-019

    Requirement: The version-1 lineage vocabulary has three exact alias-free members.

    Method: Inspect inheritance, paired declaration order, names, values, count, and the
    complete member mapping.

    Oracle: The accepted pairs are DERIVED/derived, REPRESENTATION/representation, and
    RETRY/retry in that order.

    Acceptance: The enum subclasses StrEnum; paired order, names, values, and count
    match
    exactly; ``__members__`` contains exactly those identities without aliases.

    Interpretation: Passing establishes the closed lineage vocabulary; failure indicates
    member,
    order, value, inheritance, count, or alias drift.

    Limitations: This does not validate an edge, endpoint relation, lineage claim, or
    graph.
    """
    expected_members = (
        LineageKind.DERIVED,
        LineageKind.REPRESENTATION,
        LineageKind.RETRY,
    )
    assert issubclass(LineageKind, StrEnum)
    assert tuple(LineageKind) == expected_members
    assert tuple((member.name, member.value) for member in LineageKind) == (
        ("DERIVED", "derived"),
        ("REPRESENTATION", "representation"),
        ("RETRY", "retry"),
    )
    assert len(LineageKind) == 3
    assert tuple(LineageKind.__members__) == ("DERIVED", "REPRESENTATION", "RETRY")
    assert tuple(LineageKind.__members__.values()) == expected_members


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param("derived", LineageKind.DERIVED, id="derived_kind"),
        pytest.param(
            "representation",
            LineageKind.REPRESENTATION,
            id="representation_kind",
        ),
        pytest.param("retry", LineageKind.RETRY, id="retry_kind"),
    ],
)
def test_method__call__constructs_each_kind_from_wire_value(
    value: str, expected: LineageKind
) -> None:
    """Evidence ID: SV-PROV-373

    Requirement: Enum value construction resolves each lineage wire value to its exact
    member.

    Method: Call the enum with each explicit wire value and an independently supplied
    expected member.

    Oracle: The fixed version-1 value/member pairs define expected identities without
    consulting ``__members__``.

    Acceptance: ``LineageKind(value)`` is the independently specified member.

    Interpretation: Passing establishes successful value construction for all lineage
    kinds;
    failure indicates lookup or vocabulary drift.

    Limitations: Construction selects a kind only and does not validate or prove a
    lineage edge.
    """
    assert LineageKind(value) is expected


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        pytest.param("DERIVED", LineageKind.DERIVED, id="derived_kind"),
        pytest.param(
            "REPRESENTATION",
            LineageKind.REPRESENTATION,
            id="representation_kind",
        ),
        pytest.param("RETRY", LineageKind.RETRY, id="retry_kind"),
    ],
)
def test_method__getitem__returns_each_kind_from_declared_name(
    name: str, expected: LineageKind
) -> None:
    """Evidence ID: SV-PROV-374

    Requirement: Declared-name lookup resolves each exact lineage name to its exact
    member.

    Method: Index the enum class with each explicit name and independently supplied
    expected
    member.

    Oracle: The fixed version-1 name/member pairs define expected identities without
    using
    ``__members__`` as the successful oracle.

    Acceptance: ``LineageKind[name]`` is the independently specified member.

    Interpretation: Passing establishes declared-name lookup for every lineage kind;
    failure
    indicates name lookup or declaration drift.

    Limitations: Name lookup does not validate endpoint identities or serialized wire
    values.
    """
    assert LineageKind[name] is expected


def test_method__call__rejects_unknown_wire_value() -> None:
    """Evidence ID: SV-PROV-375

    Requirement: Value construction rejects wire text outside the closed lineage
    vocabulary.

    Method: Call ``LineageKind`` with the explicit string ``unknown``.

    Oracle: The accepted wire values are derived, representation, and retry only.

    Acceptance: Construction raises exactly ValueError.

    Interpretation: Passing establishes unknown-value rejection; failure indicates
    unintended
    vocabulary expansion or coercion.

    Limitations: This does not assess unknown names or wrong semantic Python types.
    """
    with pytest.raises(ValueError):
        LineageKind("unknown")


def test_method__call__rejects_wrong_semantic_type() -> None:
    """Evidence ID: SV-PROV-376

    Requirement: Value construction rejects an integer rather than coercing it to wire
    text.

    Method: Call ``LineageKind`` with integer 1.

    Oracle: Standard enum value construction raises ValueError when no member has that
    exact
    value.

    Acceptance: Construction raises exactly ValueError.

    Interpretation: Passing establishes wrong-type value rejection without string
    coercion; failure
    indicates broadened construction behavior.

    Limitations: Integer 1 represents this wrong semantic type partition only.
    """
    with pytest.raises(ValueError):
        LineageKind(1)  # type: ignore[arg-type]


def test_method__getitem__rejects_unknown_member_name() -> None:
    """Evidence ID: SV-PROV-377

    Requirement: Declared-name lookup rejects names outside the closed lineage
    inventory.

    Method: Index ``LineageKind`` with the explicit name ``UNKNOWN``.

    Oracle: The accepted declared names are DERIVED, REPRESENTATION, and RETRY only.

    Acceptance: Lookup raises exactly KeyError.

    Interpretation: Passing establishes unknown-name rejection; failure indicates an
    unexpected
    alias or member declaration.

    Limitations: This does not assess unknown wire values or lineage-relation
    construction.
    """
    with pytest.raises(KeyError):
        LineageKind["UNKNOWN"]
