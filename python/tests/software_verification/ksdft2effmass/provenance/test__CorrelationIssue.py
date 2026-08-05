"""Evidence class and represented meaning
Software verification of the exact correlation-issue enum artifact.
Owned contract, oracle, and scope
CorrelationIssue is the SUT; the accepted version-1 issue vocabulary is the oracle.
VVUQ and scientific exclusions
Evidence excludes execution, numerical verification, scientific validation, UQ, physical
correctness, and cross-language conformance.
"""

import pytest

from ksdft2effmass.provenance import CorrelationIssue

SUT = CorrelationIssue
pytestmark = pytest.mark.software_verification


def test_artifact__enum_values__matches_exact_correlation_issue_vocabulary() -> None:
    """Evidence ID
    SV-PROV-073
    Requirement
    Public correlation issues are exactly request, correlation, then attempt-ID
    mismatch.
    Method
    Enumerate the public enum and inspect names and values without invoking an action.
    Oracle
    The accepted version-1 correlation taxonomy fixes both exact ordered tuples.
    Acceptance
    Names and values equal the independently listed tuples exactly.
    Interpretation
    Failure indicates public or wire taxonomy drift.
    Limitations
    Reachability is covered by ExecutionOutcomeCorrelator; no execution or scientific
    claim is made.
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
