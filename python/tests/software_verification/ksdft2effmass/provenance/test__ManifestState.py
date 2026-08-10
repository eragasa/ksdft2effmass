r"""Software verification of ``ManifestState``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

-----------------------------
This class-owned software evidence verifies the exact closed version-1 manifest
lifecycle vocabulary: ``DECLARED`` maps to ``declared``, ``COMPLETE`` maps to
``complete``, and ``FAILED`` maps to ``failed``. ``DECLARED`` records a declared
attempt, ``COMPLETE`` records external-boundary completion, and ``FAILED``
records unsuccessful termination.

Intrinsic and cross-object scope

--------------------------------
The sole primary SUT is ``ManifestState``. Exact fixed names, wire values,
declaration order, and Python ``StrEnum`` lookup behavior provide the oracles.
The enum selects a manifest lifecycle state only. It does not validate manifest
timestamps or finish-state relations, execute a tool, or parse a result.

VVUQ and scientific exclusions

------------------------------
Passing establishes only the stated enum vocabulary and lookup behavior; failure
identifies production vocabulary, test oracle, or accepted-contract drift. The
enum does not establish solver convergence, numerical acceptance, scientific
validation, UQ, human acceptance, physical correctness, portability beyond the
declared vocabulary, or cross-language agreement.
"""

from enum import StrEnum

import pytest

from ksdft2effmass.provenance import ManifestState

SUT = ManifestState
pytestmark = pytest.mark.software_verification


def test_field__wire_vocabulary__has_exact_order_names_values_and_count() -> None:
    """Evidence ID: SV-PROV-075

    Requirement: The version-1 manifest lifecycle vocabulary has three exact alias-free
    members.

    Method: Inspect inheritance, paired declaration order, names, values, count, and the
    complete member mapping.

    Oracle: The accepted pairs are DECLARED/declared, COMPLETE/complete, and
    FAILED/failed
    in that order.

    Acceptance: The enum subclasses StrEnum; paired order, names, values, and count
    match
    exactly; ``__members__`` contains exactly those identities without aliases.

    Interpretation: Passing establishes the closed lifecycle vocabulary; failure
    indicates member,
    order, value, inheritance, count, or alias drift.

    Limitations: This does not validate a manifest, timestamp relation, execution, or
    result.
    """
    expected_members = (
        ManifestState.DECLARED,
        ManifestState.COMPLETE,
        ManifestState.FAILED,
    )
    assert issubclass(ManifestState, StrEnum)
    assert tuple(ManifestState) == expected_members
    assert tuple((member.name, member.value) for member in ManifestState) == (
        ("DECLARED", "declared"),
        ("COMPLETE", "complete"),
        ("FAILED", "failed"),
    )
    assert len(ManifestState) == 3
    assert tuple(ManifestState.__members__) == ("DECLARED", "COMPLETE", "FAILED")
    assert tuple(ManifestState.__members__.values()) == expected_members


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param("declared", ManifestState.DECLARED, id="declared_state"),
        pytest.param("complete", ManifestState.COMPLETE, id="complete_state"),
        pytest.param("failed", ManifestState.FAILED, id="failed_state"),
    ],
)
def test_method__call__constructs_each_state_from_wire_value(
    value: str, expected: ManifestState
) -> None:
    """Evidence ID: SV-PROV-368

    Requirement: Enum value construction resolves each lifecycle wire value to its exact
    member.

    Method: Call the enum with each explicit wire value and an independently supplied
    expected member.

    Oracle: The fixed version-1 value/member pairs define expected identities without
    consulting ``__members__``.

    Acceptance: ``ManifestState(value)`` is the independently specified member.

    Interpretation: Passing establishes successful value construction for all lifecycle
    states;
    failure indicates lookup or vocabulary drift.

    Limitations: Construction selects a state only and does not validate manifest
    relations.
    """
    assert ManifestState(value) is expected


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        pytest.param("DECLARED", ManifestState.DECLARED, id="declared_state"),
        pytest.param("COMPLETE", ManifestState.COMPLETE, id="complete_state"),
        pytest.param("FAILED", ManifestState.FAILED, id="failed_state"),
    ],
)
def test_method__getitem__returns_each_state_from_declared_name(
    name: str, expected: ManifestState
) -> None:
    """Evidence ID: SV-PROV-369

    Requirement: Declared-name lookup resolves each exact lifecycle name to its exact
    member.

    Method: Index the enum class with each explicit name and independently supplied
    expected
    member.

    Oracle: The fixed version-1 name/member pairs define expected identities without
    using
    ``__members__`` as the successful oracle.

    Acceptance: ``ManifestState[name]`` is the independently specified member.

    Interpretation: Passing establishes declared-name lookup for every lifecycle state;
    failure
    indicates name lookup or declaration drift.

    Limitations: Name lookup does not validate manifest data or serialized wire values.
    """
    assert ManifestState[name] is expected


def test_method__call__rejects_unknown_wire_value() -> None:
    """Evidence ID: SV-PROV-370

    Requirement: Value construction rejects wire text outside the closed lifecycle
    vocabulary.

    Method: Call ``ManifestState`` with the explicit string ``unknown``.

    Oracle: The accepted wire values are declared, complete, and failed only.

    Acceptance: Construction raises exactly ValueError.

    Interpretation: Passing establishes unknown-value rejection; failure indicates
    unintended
    vocabulary expansion or coercion.

    Limitations: This does not assess unknown names or wrong semantic Python types.
    """
    with pytest.raises(ValueError):
        ManifestState("unknown")


def test_method__call__rejects_wrong_semantic_type() -> None:
    """Evidence ID: SV-PROV-371

    Requirement: Value construction rejects an integer rather than coercing it to wire
    text.

    Method: Call ``ManifestState`` with integer 1.

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
        ManifestState(1)  # type: ignore[arg-type]


def test_method__getitem__rejects_unknown_member_name() -> None:
    """Evidence ID: SV-PROV-372

    Requirement: Declared-name lookup rejects names outside the closed lifecycle
    inventory.

    Method: Index ``ManifestState`` with the explicit name ``UNKNOWN``.

    Oracle: The accepted declared names are DECLARED, COMPLETE, and FAILED only.

    Acceptance: Lookup raises exactly KeyError.

    Interpretation: Passing establishes unknown-name rejection; failure indicates an
    unexpected
    alias or member declaration.

    Limitations: This does not assess unknown wire values or manifest construction.
    """
    with pytest.raises(KeyError):
        ManifestState["UNKNOWN"]
