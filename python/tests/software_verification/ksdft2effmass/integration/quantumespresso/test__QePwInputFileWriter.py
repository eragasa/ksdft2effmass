r"""Software verification of ``QePwInputFileWriter``.

Evidence profile: routine

Bounded artifact scope: deterministic loose ``pw.x`` input text writing.

Facet and represented meaning

The ActionObject writes upstream-grouped namelists and cards into QE input syntax.

Intrinsic and cross-object scope

The tests cover grouping delimiters, indentation, ordering, unknown-group retention,
and the public semantic type boundary. QE defaults and execution are separate.

VVUQ and scientific exclusions

These exact text checks establish software behavior only, not input acceptance by a
QE executable, numerical verification, scientific validation, or uncertainty
quantification.
"""

import pytest

from ksdft2effmass.integration.quantumespresso import (
    QePwInputFile,
    QePwInputFileWriter,
)

pytestmark = pytest.mark.software_verification

SUT = QePwInputFileWriter


def test_method__execute__writes_namelists_cards_and_unknown_groups() -> None:
    """Evidence ID: SV-QE-PW-005

    Requirement: The writer maps ordered upstream grouping tags to namelist and card
    syntax without filtering unknown content.

    Acceptance: Output equals the independently specified text exactly.
    """
    input_file = QePwInputFile(
        (
            ("&control", ("calculation = 'scf'",)),
            ("ATOMIC_POSITIONS alat", ("Si 0.0 0.0 0.0",)),
            ("UNKNOWN_CARD option", ("opaque row",)),
        )
    )
    assert SUT().execute(input_file) == (
        "&control\n"
        "    calculation = 'scf'\n"
        "/\n"
        "ATOMIC_POSITIONS alat\n"
        " Si 0.0 0.0 0.0\n"
        "UNKNOWN_CARD option\n"
        " opaque row\n"
    )


def test_method__execute__writes_empty_input_as_empty_text() -> None:
    """Evidence ID: SV-QE-PW-006

    Requirement: An input file with no upstream groups has an empty text
    representation.

    Acceptance: The returned built-in string is exactly empty.
    """
    assert SUT().execute(QePwInputFile(())) == ""


def test_method__execute__rejects_wrong_semantic_type() -> None:
    """Evidence ID: SV-QE-PW-007

    Requirement: The writer does not coerce arbitrary objects into QE input files.

    Acceptance: A built-in tuple raises ``TypeError``.
    """
    with pytest.raises(TypeError):
        SUT().execute(())  # type: ignore[arg-type]
