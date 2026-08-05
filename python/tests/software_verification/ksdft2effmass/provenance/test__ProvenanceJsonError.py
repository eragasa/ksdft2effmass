"""Evidence class and represented meaning
Software verification of the public strict-JSON error boundary.
Owned contract, oracle, and scope
ProvenanceJsonError is the SUT; public exception taxonomy and inherited ValueError
semantics are the oracle.
VVUQ and scientific exclusions
Evidence excludes schema completeness, numerical verification, scientific validation,
UQ, and cross-language conformance.
"""

import pytest

from ksdft2effmass.provenance import ProvenanceJsonError, ProvenanceJsonSerializer

SUT = ProvenanceJsonError
pytestmark = pytest.mark.software_verification


def test_constructor__error_taxonomy__is_public_value_error_with_message() -> None:
    """Evidence ID
    SV-PROV-056
    Requirement
    Strict JSON contract failures expose a public ProvenanceJsonError that is a
    ValueError with stable message payload.
    Method
    Construct the public error directly and inspect inheritance and args.
    Oracle
    Python exception semantics and the accepted public error declaration are exact.
    Acceptance
    The instance is both ProvenanceJsonError and ValueError and args equals ('detail',).
    Interpretation
    Failure indicates public error taxonomy drift.
    Limitations
    Direct construction does not exercise a decoder failure.
    """
    error = SUT("detail")
    assert isinstance(error, ValueError)
    assert error.args == ("detail",)


def test_method__deserialize_contract_failure__raises_public_error() -> None:
    """Evidence ID
    SV-PROV-057
    Requirement
    Malformed JSON is translated to the public ProvenanceJsonError boundary.
    Method
    Call the public serializer with a syntactically incomplete object.
    Oracle
    RFC 8259 syntax makes the literal invalid independently of production parsing.
    Acceptance
    deserialize raises ProvenanceJsonError rather than leaking JSONDecodeError.
    Interpretation
    Failure indicates error translation or public boundary drift.
    Limitations
    Detailed strict-input partitions are owned by serializer and fixture integration
    evidence.
    """
    with pytest.raises(SUT):
        ProvenanceJsonSerializer().deserialize("{")
