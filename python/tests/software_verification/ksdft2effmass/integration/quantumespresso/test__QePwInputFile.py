r"""Software verification of ``QePwInputFile``.

Evidence profile: routine

Bounded artifact scope: the loose ordered ``pw.x`` input-file DataObject.

Facet and represented meaning

The class represents upstream-selected grouping tags and uninterpreted body lines.

Intrinsic and cross-object scope

The tests cover immutable ordered storage and intrinsic lexical boundary rejection.
Scientific defaults, cross-field QE meaning, writing, and execution are separate.

VVUQ and scientific exclusions

These synthetic checks establish software behavior only, not numerical verification,
scientific validation, uncertainty quantification, or calculator correctness.
"""

from dataclasses import FrozenInstanceError

import pytest

import ksdft2effmass.integration.quantumespresso as qe_integration
from ksdft2effmass.integration.quantumespresso import QePwInputFile

pytestmark = pytest.mark.software_verification

SUT = QePwInputFile


def test_public_api__package__exports_only_primary_input_boundary() -> None:
    """Evidence ID: SV-QE-PW-008

    Requirement: The root integration package presents input representation and
    writing as its selected public surface rather than promoting output parsing.

    Acceptance: Ordered exports contain exactly the two selected input classes.
    """
    assert tuple(qe_integration.__all__) == ("QePwInputFile", "QePwInputFileWriter")
    assert SUT.__module__ == "ksdft2effmass.integration.quantumespresso.pw_input"


def test_constructor__groups__preserves_ordered_loose_content() -> None:
    """Evidence ID: SV-QE-PW-001

    Requirement: The input file retains upstream group tags, order, and body lines
    without interpreting unknown names or values.

    Acceptance: Stored groups equal the exact supplied immutable tuple.
    """
    groups = (("&control", ("calculation = 'scf'",)), ("CUSTOM_CARD x", ("a b",)))
    assert SUT(groups).groups == groups


def test_constructor__immutability__rejects_field_assignment() -> None:
    """Evidence ID: SV-QE-PW-002

    Requirement: The loose input-file representation is immutable.

    Acceptance: Ordinary field assignment raises ``FrozenInstanceError``.
    """
    value = SUT(())
    with pytest.raises(FrozenInstanceError):
        value.groups = ()  # type: ignore[misc]


@pytest.mark.parametrize(
    "groups",
    [
        pytest.param([], id="outer_list"),
        pytest.param((("&control", []),), id="line_list"),
        pytest.param(((1, ()),), id="integer_tag"),
        pytest.param((("&control", (1,)),), id="integer_line"),
    ],
)
def test_constructor__semantic_types__rejects_non_builtin_structure(
    groups: object,
) -> None:
    """Evidence ID: SV-QE-PW-003

    Requirement: Public grouping boundaries reject implicit collection and scalar
    coercion.

    Acceptance: Every named wrong-type partition raises ``TypeError``.
    """
    with pytest.raises(TypeError):
        SUT(groups)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "groups",
    [
        pytest.param((("", ()),), id="empty_tag"),
        pytest.param(((" &control", ()),), id="padded_tag"),
        pytest.param((("&control\n", ()),), id="tag_line_terminator"),
        pytest.param((("&control", ("x = 1\n",)),), id="body_line_terminator"),
    ],
)
def test_constructor__lexical_invariants__rejects_ambiguous_boundaries(
    groups: tuple[tuple[str, tuple[str, ...]], ...],
) -> None:
    """Evidence ID: SV-QE-PW-004

    Requirement: Group boundaries are represented structurally rather than hidden in
    tag or body-line terminators.

    Acceptance: Every named malformed lexical partition raises ``ValueError``.
    """
    with pytest.raises(ValueError):
        SUT(groups)
