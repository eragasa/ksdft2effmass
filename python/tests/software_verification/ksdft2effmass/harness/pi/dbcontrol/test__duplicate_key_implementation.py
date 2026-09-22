r"""Software verification of generic dbcontrol duplicate-key implementation artifact.

Evidence profile: routine

Bounded artifact scope: generic dbcontrol private duplicate-key implementation behavior.

Facet and represented meaning

The module owns the intrinsic represented behavior of ``_DuplicateKey``.

Intrinsic and cross-object scope

Only the object's bounded contract is exercised; collaborators are literal inputs.

VVUQ and scientific exclusions

This is software verification only; scientific validation and UQ are excluded.
"""  # noqa: E501

import pytest

from ksdft2effmass.harness.pi.dbcontrol.documents import _DuplicateKey

SUT = _DuplicateKey

pytestmark = pytest.mark.software_verification


def test_constructor__message__preserves_duplicate_key() -> None:
    """Evidence ID: software-verification.harness.dbcontrol.duplicate-key.constructor.preserves-key

    Requirement: The duplicate-key failure preserves the conflicting key for diagnostics.

    Method: Construct the private bounded parser exception with a literal key.

    Oracle: Python ``ValueError`` preserves its positional argument exactly.

    Acceptance: ``args`` equals exactly ``("task_id",)``.

    Interpretation: Failure indicates loss of parser conflict context.

    Limitations: JSON parsing is not exercised.
    """  # noqa: E501
    assert _DuplicateKey("task_id").args == ("task_id",)
