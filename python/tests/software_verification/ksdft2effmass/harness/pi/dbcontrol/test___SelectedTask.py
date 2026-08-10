r"""Software verification of ``_SelectedTask``.

Facet and represented meaning

The module owns the intrinsic represented behavior of ``_SelectedTask``.

Intrinsic and cross-object scope

Only the object's bounded contract is exercised; collaborators are literal inputs.

VVUQ and scientific exclusions

This is software verification only; scientific validation and UQ are excluded.
"""

import pytest

from ksdft2effmass.harness.pi.dbcontrol.documents import _SelectedTask

SUT = _SelectedTask

pytestmark = pytest.mark.software_verification


def test_constructor__defaults__represent_absent_declarations() -> None:
    """Evidence ID: software-verification.harness.dbcontrol.selected-task.constructor.absent-defaults

    Requirement: A selected Task begins with no declared record paths or status.

    Method: Construct the internal record without arguments.

    Oracle: The documented bounded inspection model distinguishes absence with ``None`` and empty tuples.

    Acceptance: Scalar fields are ``None`` and all path collections are exact empty tuples.

    Interpretation: Failure indicates invented durable declarations.

    Limitations: Parsing and filesystem inspection are excluded.
    """  # noqa: E501
    value = _SelectedTask()
    assert (value.status, value.task_record_path, value.ownership_path) == (
        None,
        None,
        None,
    )
    assert (value.artifact_paths, value.run_paths, value.handoff_paths) == ((), (), ())
