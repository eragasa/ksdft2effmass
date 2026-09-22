r"""Software verification of explicit Task-state document parsing.

Evidence profile: routine

Bounded artifact scope: private explicit-input Task-state parser behavior.

Facet and represented meaning

The module verifies that selection state remains separate from Task state.

Intrinsic and cross-object scope

Only bounded parsing of literal bytes is exercised.

VVUQ and scientific exclusions

This is software verification only; authority, scientific validation, and UQ are
excluded.
"""

import pytest

from ksdft2effmass.harness.pi.dbcontrol.documents import _TaskStateDocumentParser

pytestmark = pytest.mark.software_verification


def test_method__parse_selection__represents_no_current_selection() -> None:
    """Evidence ID: software-verification.harness.dbcontrol.selection.parse.inactive

    Requirement: An inactive canonical selection represents no selected Task.

    Method: Parse literal closed version-1 selection JSON.

    Oracle: JSON null maps exactly to Python None.

    Acceptance: selected_task_id is exactly None.

    Interpretation: Failure indicates fabricated selection state.

    Limitations: Repository I/O and Task eligibility are excluded.
    """
    payload = (
        b'{"schema_version":1,"active_task_id":null,'
        b'"explicit_activation_receipt_ids":[],'
        b'"automatic_successor_activation":false}'
    )
    assert _TaskStateDocumentParser().parse_selection(payload).selected_task_id is None
