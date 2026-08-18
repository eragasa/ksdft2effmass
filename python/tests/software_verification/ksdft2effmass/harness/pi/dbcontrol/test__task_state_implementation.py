r"""Software verification of private explicit Task-state representation.

Evidence profile: routine

Bounded artifact scope: private Task-state result representation.

Facet and represented meaning

The module owns the intrinsic represented behavior of ``_TaskState``.

Intrinsic and cross-object scope

Only the object's bounded immutable status field is exercised.

VVUQ and scientific exclusions

This is software verification only; authority, scientific validation, and UQ are
excluded.
"""

import pytest

from ksdft2effmass.harness.pi.dbcontrol.documents import _TaskState

pytestmark = pytest.mark.software_verification


def test_constructor__status__preserves_exact_canonical_value() -> None:
    """Evidence ID: software-verification.harness.dbcontrol.task-state.constructor.status

    Requirement: Parsed Task state represents the exact canonical lifecycle status.

    Method: Construct the private result from one literal status.

    Oracle: The constructor input fixes the represented value.

    Acceptance: The status field equals the literal exactly.

    Interpretation: Failure indicates invented or transformed Task state.

    Limitations: Parsing, lifecycle meaning, and authority are excluded.
    """  # noqa: E501
    assert _TaskState("completed").status == "completed"
