r"""Software verification of ``ArtifactLocationKind``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

-----------------------------
This class-owned software evidence verifies the exact closed version-1
representation vocabulary: ``ROOT_RELATIVE`` maps to ``root_relative`` and
``EXTERNAL_DESCRIPTOR`` maps to ``external_descriptor``. ``ROOT_RELATIVE``
selects the representation using ``root_id`` and lexical ``path``;
``EXTERNAL_DESCRIPTOR`` selects the representation using an opaque approved
descriptor identity.

Intrinsic and cross-object scope

--------------------------------
The sole primary SUT is ``ArtifactLocationKind``. Exact fixed names, wire values,
declaration order, and Python ``StrEnum`` lookup behavior provide the oracles.
The enum selects a representation form only. It does not validate an
``ArtifactLocation`` or path, resolve a root or external descriptor, prove
artifact existence, retrieve artifact content, or establish byte identity.

VVUQ and scientific exclusions

------------------------------
Passing establishes only the stated enum vocabulary and lookup behavior; failure
identifies production vocabulary, test oracle, or accepted-contract drift. This
evidence does not establish scientific validity, UQ, physical correctness,
portability beyond the declared vocabulary, or cross-language agreement.
"""

from enum import StrEnum

import pytest

from ksdft2effmass.provenance import ArtifactLocationKind

SUT = ArtifactLocationKind
pytestmark = pytest.mark.software_verification


def test_field__wire_vocabulary__has_exact_order_names_values_and_count() -> None:
    """Evidence ID: SV-PROV-011

    Requirement: The version-1 location-kind vocabulary has two exact alias-free
    members.

    Method: Inspect inheritance, iteration order, declared names, wire values, count,
    and
    the complete member mapping.

    Oracle: The accepted vocabulary is ROOT_RELATIVE/root_relative followed by
    EXTERNAL_DESCRIPTOR/external_descriptor.

    Acceptance: The enum subclasses StrEnum; order, names, values, and count match
    exactly;
    ``__members__`` has exactly those names and identities with no aliases.

    Interpretation: Passing establishes the closed representation vocabulary; failure
    indicates
    member, ordering, value, inheritance, count, or alias drift.

    Limitations: This does not construct or validate an ArtifactLocation or resolve
    either
    representation form.
    """
    expected_members = (
        ArtifactLocationKind.ROOT_RELATIVE,
        ArtifactLocationKind.EXTERNAL_DESCRIPTOR,
    )
    assert issubclass(ArtifactLocationKind, StrEnum)
    assert tuple(ArtifactLocationKind) == expected_members
    assert tuple(member.name for member in ArtifactLocationKind) == (
        "ROOT_RELATIVE",
        "EXTERNAL_DESCRIPTOR",
    )
    assert tuple(member.value for member in ArtifactLocationKind) == (
        "root_relative",
        "external_descriptor",
    )
    assert len(ArtifactLocationKind) == 2
    assert tuple(ArtifactLocationKind.__members__) == (
        "ROOT_RELATIVE",
        "EXTERNAL_DESCRIPTOR",
    )
    assert tuple(ArtifactLocationKind.__members__.values()) == expected_members


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(
            "root_relative",
            ArtifactLocationKind.ROOT_RELATIVE,
            id="root_relative_kind",
        ),
        pytest.param(
            "external_descriptor",
            ArtifactLocationKind.EXTERNAL_DESCRIPTOR,
            id="external_descriptor_kind",
        ),
    ],
)
def test_method__call__constructs_each_kind_from_wire_value(
    value: str, expected: ArtifactLocationKind
) -> None:
    """Evidence ID: SV-PROV-363

    Requirement: Enum value construction resolves each declared wire value to its exact
    member.

    Method: Call the enum with each explicit wire value and an independently named
    expected
    member.

    Oracle: The fixed version-1 value/member pairs define the expected identities
    without
    consulting ``__members__``.

    Acceptance: ``ArtifactLocationKind(value)`` is the independently specified member.

    Interpretation: Passing establishes successful value construction for both
    representation
    forms; failure indicates lookup or vocabulary drift.

    Limitations: Construction selects a kind only and does not validate a location
    payload.
    """
    assert ArtifactLocationKind(value) is expected


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        pytest.param(
            "ROOT_RELATIVE",
            ArtifactLocationKind.ROOT_RELATIVE,
            id="root_relative_kind",
        ),
        pytest.param(
            "EXTERNAL_DESCRIPTOR",
            ArtifactLocationKind.EXTERNAL_DESCRIPTOR,
            id="external_descriptor_kind",
        ),
    ],
)
def test_method__getitem__returns_each_kind_from_declared_name(
    name: str, expected: ArtifactLocationKind
) -> None:
    """Evidence ID: SV-PROV-364

    Requirement: Declared-name lookup resolves each exact member name to its exact
    member.

    Method: Index the enum class with each explicit name and independently named
    expected
    member.

    Oracle: The fixed version-1 name/member pairs define expected identities without
    using
    ``__members__`` as the successful oracle.

    Acceptance: ``ArtifactLocationKind[name]`` is the independently specified member.

    Interpretation: Passing establishes successful declared-name lookup for both
    members; failure
    indicates name lookup or declaration drift.

    Limitations: Name lookup does not validate location payloads or serialized wire
    values.
    """
    assert ArtifactLocationKind[name] is expected


def test_method__call__rejects_unknown_wire_value() -> None:
    """Evidence ID: SV-PROV-365

    Requirement: Value construction rejects wire text outside the closed version-1
    vocabulary.

    Method: Call ``ArtifactLocationKind`` with the explicit string ``unknown``.

    Oracle: The accepted vocabulary contains only root_relative and external_descriptor.

    Acceptance: Construction raises exactly ValueError.

    Interpretation: Passing establishes unknown-value rejection; failure indicates
    unintended
    vocabulary expansion or coercion.

    Limitations: This does not assess unknown names or wrong semantic Python types.
    """
    with pytest.raises(ValueError):
        ArtifactLocationKind("unknown")


def test_method__call__rejects_wrong_semantic_type() -> None:
    """Evidence ID: SV-PROV-366

    Requirement: Value construction rejects an integer rather than coercing it to wire
    text.

    Method: Call ``ArtifactLocationKind`` with integer 1.

    Oracle: Standard enum value construction raises ValueError when no member has that
    exact value.

    Acceptance: Construction raises exactly ValueError.

    Interpretation: Passing establishes wrong-type value rejection without string
    coercion;
    failure indicates broadened construction behavior.

    Limitations: Integer 1 represents this wrong semantic type partition only.
    """
    with pytest.raises(ValueError):
        ArtifactLocationKind(1)  # type: ignore[arg-type]


def test_method__getitem__rejects_unknown_member_name() -> None:
    """Evidence ID: SV-PROV-367

    Requirement: Declared-name lookup rejects names outside the closed member inventory.

    Method: Index ``ArtifactLocationKind`` with the explicit name ``UNKNOWN``.

    Oracle: The accepted declared names are ROOT_RELATIVE and EXTERNAL_DESCRIPTOR only.

    Acceptance: Lookup raises exactly KeyError.

    Interpretation: Passing establishes unknown-name rejection; failure indicates an
    unexpected
    alias or member declaration.

    Limitations: This does not assess unknown wire values or location construction.
    """
    with pytest.raises(KeyError):
        ArtifactLocationKind["UNKNOWN"]
