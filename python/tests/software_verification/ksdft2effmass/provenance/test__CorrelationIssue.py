r"""Software verification of ``CorrelationIssue``.

Facet and represented meaning

-----------------------------
This module verifies the closed request/outcome identity-defect vocabulary.

Intrinsic and cross-object scope

--------------------------------
``CorrelationIssue`` is the sole SUT; public enum names, values, and deterministic order
are fixed by the P2 correlation contract.

VVUQ and scientific exclusions

------------------------------
Passing establishes only software vocabulary. It excludes external execution,
provenance truth, numerical verification, scientific validation, UQ, portability, and
cross-language conformance.
"""

import pytest

from ksdft2effmass.provenance import CorrelationIssue

SUT = CorrelationIssue
pytestmark = pytest.mark.software_verification


def test_field__correlation_issue_vocabulary__is_exact() -> None:
    """Evidence ID: SV-PROV-073

    Requirement: Issues are exactly request, correlation, then attempt identifier
    mismatch.

    Method: Enumerate the public string enum without invoking a correlator.

    Oracle: The accepted P2 taxonomy independently fixes names, values, and order.

    Acceptance: Names and values equal the literal expected tuples exactly.

    Interpretation: Failure indicates public or serialized issue-taxonomy drift.

    Limitations: Reachability is owned by ExecutionOutcomeCorrelator; no execution claim
    is made.
    """
    assert tuple(item.name for item in SUT) == (
        "REQUEST_ID_MISMATCH",
        "CORRELATION_ID_MISMATCH",
        "ATTEMPT_ID_MISMATCH",
    )
    assert tuple(item.value for item in SUT) == (
        "request_id_mismatch",
        "correlation_id_mismatch",
        "attempt_id_mismatch",
    )
