"""Evidence class and represented meaning
Software verification of the exact structured external-failure code artifact.
Owned contract, oracle, and scope
ExternalFailureCode is the SUT; the accepted version-1 failure taxonomy is the oracle.
VVUQ and scientific exclusions
Evidence excludes adapters, execution, numerical verification, scientific validation,
UQ, physical correctness, and cross-language conformance.
"""

import pytest

from ksdft2effmass.provenance import ExternalFailureCode

SUT = ExternalFailureCode
pytestmark = pytest.mark.software_verification


def test_artifact__enum_values__matches_exact_external_failure_taxonomy() -> None:
    """Evidence ID
    SV-PROV-074
    Requirement
    Public external failure codes equal the complete accepted six-value vocabulary.
    Method
    Enumerate the public enum and compare its values with an independent fixed tuple.
    Oracle
    The accepted version-1 structured failure contract fixes values and declaration
    order.
    Acceptance
    Values equal unavailable, not_authorized, rejected, interrupted, malformed_result,
    internal_error exactly.
    Interpretation
    Failure indicates public/schema failure-taxonomy drift.
    Limitations
    Adapter classification quality and real external failures are not validated.
    """
    assert tuple(item.value for item in SUT) == (
        "unavailable",
        "not_authorized",
        "rejected",
        "interrupted",
        "malformed_result",
        "internal_error",
    )
