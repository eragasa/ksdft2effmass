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

import ksdft2effmass.integration.quantum_espresso as qe_integration
from ksdft2effmass.integration.quantum_espresso import QePwInputFile

pytestmark = pytest.mark.software_verification

SUT = QePwInputFile

type InvalidGroups = (
    list[str]
    | tuple[tuple[str, list[str]], ...]
    | tuple[tuple[int, tuple[str, ...]], ...]
    | tuple[tuple[str, tuple[int, ...]], ...]
)


class TestQePwInputFile:
    """Own this module's maintained software-verification evidence."""

    def test_public_api__package__exports_canonical_input(self) -> None:
        """Evidence ID: SV-QE-PW-008

        Requirement: The canonical integration root exports the input representation.

        Acceptance: The package root exposes the exact class and its defining module
        uses the canonical underscored package spelling.
        """
        assert qe_integration.QePwInputFile is SUT
        assert SUT.__module__ == "ksdft2effmass.integration.quantum_espresso.pw_input"

    def test_constructor__groups__preserves_ordered_loose_content(self) -> None:
        """Evidence ID: SV-QE-PW-001

        Requirement: The input file retains upstream group tags, order, and body lines
        without interpreting unknown names or values.

        Acceptance: Stored groups equal the exact supplied immutable tuple.
        """
        groups = (("&control", ("calculation = 'scf'",)), ("CUSTOM_CARD x", ("a b",)))
        assert SUT(groups).groups == groups

    def test_constructor__immutability__rejects_field_assignment(self) -> None:
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
        self,
        groups: InvalidGroups,
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
        self,
        groups: tuple[tuple[str, tuple[str, ...]], ...],
    ) -> None:
        """Evidence ID: SV-QE-PW-004

        Requirement: Group boundaries are represented structurally rather than hidden in
        tag or body-line terminators.

        Acceptance: Every named malformed lexical partition raises ``ValueError``.
        """
        with pytest.raises(ValueError):
            SUT(groups)
