r"""Software verification of generic dbcontrol task-state-document-parser implementation artifact.

Evidence profile: routine

Bounded artifact scope: generic dbcontrol private task-state-document-parser implementation behavior.

Facet and represented meaning

The module owns the intrinsic represented behavior of ``_TaskStateDocumentParser``.

Intrinsic and cross-object scope

Only the object's bounded contract is exercised; collaborators are literal inputs.

VVUQ and scientific exclusions

This is software verification only; scientific validation and UQ are excluded.
"""  # noqa: E501

import pytest

from ksdft2effmass.harness.pi.dbcontrol.documents import (
    _DuplicateKey,
    _TaskStateDocumentParser,
)

SUT = _TaskStateDocumentParser

pytestmark = pytest.mark.software_verification


def test_method__json_object_duplicate_key__raises_exact_error() -> None:
    """Evidence ID: software-verification.harness.dbcontrol.task-state-document-parser.method.duplicate-key

    Requirement: Durable JSON parsing rejects duplicate object keys.

    Method: Parse immutable literal JSON bytes containing two ``task_id`` keys.

    Oracle: JSON object keys must be unique for unambiguous control state.

    Acceptance: Parsing raises ``_DuplicateKey`` with exact key argument.

    Interpretation: Failure indicates ambiguous durable state acceptance.

    Limitations: Full chain reconciliation is excluded.
    """  # noqa: E501
    with pytest.raises(_DuplicateKey) as caught:
        _TaskStateDocumentParser()._json_object(b'{"task_id":"a","task_id":"b"}')
    assert caught.value.args == ("task_id",)
