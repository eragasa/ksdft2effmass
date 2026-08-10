r"""Software verification of generic dbcontrol chain-state implementation artifact.

Evidence profile: routine

Bounded artifact scope: generic dbcontrol private chain-state implementation behavior.

Facet and represented meaning

The module owns the intrinsic represented behavior of ``_ChainState``.

Intrinsic and cross-object scope

Only the object's bounded contract is exercised; collaborators are literal inputs.

VVUQ and scientific exclusions

This is software verification only; scientific validation and UQ are excluded.
"""  # noqa: E501

import pytest

from ksdft2effmass.harness.pi.dbcontrol.documents import _ChainState

SUT = _ChainState

pytestmark = pytest.mark.software_verification


def test_constructor__defaults__represent_no_selection() -> None:
    """Evidence ID: software-verification.harness.dbcontrol.chain-state.constructor.no-selection

    Requirement: Unparsed chain state represents neither activation nor selection.

    Method: Construct the internal state without arguments.

    Oracle: Explicit absence is represented by Python ``None``.

    Acceptance: Both fields are exactly ``None``.

    Interpretation: Failure indicates fabricated chain selection.

    Limitations: Chain JSON parsing is excluded.
    """  # noqa: E501
    assert _ChainState() == _ChainState(active_task=None, selected_task=None)
