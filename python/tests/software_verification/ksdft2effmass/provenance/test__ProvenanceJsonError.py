r"""Software verification of ``ProvenanceJsonError``.

Facet and represented meaning
The evidence verifies direct construction of the public strict-JSON exception and
its software exception taxonomy and stored message payload.

Intrinsic and cross-object scope
``ProvenanceJsonError`` is the sole SUT. Python exception construction semantics
and the accepted public ``ValueError`` inheritance contract provide the oracle.

VVUQ and scientific exclusions
Direct construction does not verify decoder translation, JSON syntax, schema
agreement, numerical verification, scientific validation, uncertainty
quantification, portability, cross-language conformance, or provenance truth.
"""

import pytest

from ksdft2effmass.provenance import ProvenanceJsonError

SUT = ProvenanceJsonError
pytestmark = pytest.mark.software_verification


def test_constructor__error_taxonomy__stores_message_and_inherits_value_error() -> None:
    """Evidence ID
    SV-PROV-056
    Requirement
    Direct public construction stores the supplied message and creates exactly a
    ProvenanceJsonError within the ValueError taxonomy.
    Method
    Construct ProvenanceJsonError with the fixed text ``detail`` and inspect its
    exact runtime type, base-class membership, args tuple, and string form.
    Oracle
    The public class declaration requires ValueError inheritance, while Python's
    exception constructor defines the exact args and string payload semantics.
    Acceptance
    The exact type is ProvenanceJsonError, the instance is a ValueError, args is
    ``("detail",)``, and ``str(error)`` is exactly ``"detail"``.
    Interpretation
    Failure identifies drift in the public exception class, inheritance, or
    directly stored message payload.
    Limitations
    This direct-construction check verifies only public exception taxonomy and
    payload; it does not exercise decoding or any JSON or schema boundary.
    """
    error = SUT("detail")
    assert type(error) is ProvenanceJsonError
    assert isinstance(error, ValueError)
    assert error.args == ("detail",)
    assert str(error) == "detail"
