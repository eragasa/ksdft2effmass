r"""Software verification of ``CorrelationStatus``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

-----------------------------
This module verifies the closed request/outcome correlation-status vocabulary.

Intrinsic and cross-object scope

--------------------------------
``CorrelationStatus`` is the sole SUT; its names, values, and order are fixed by the
public P2 contract.

VVUQ and scientific exclusions

------------------------------
Passing establishes only the software vocabulary. It excludes external execution,
provenance truth, numerical verification, scientific validation, UQ, and portability.
"""

import pytest

from ksdft2effmass.provenance import CorrelationStatus

SUT = CorrelationStatus
pytestmark = pytest.mark.software_verification


def test_field__correlation_status_vocabulary__is_exact() -> None:
    """Evidence ID: SV-PROV-053

    Requirement: Correlation outcomes are exactly CORRELATED and MISMATCH with stable
    wire values.

    Method: Enumerate the public string enum without invoking a correlator.

    Oracle: The accepted P2 vocabulary independently fixes names, values, and order.

    Acceptance: Name and value tuples equal the literal expected tuples exactly.

    Interpretation: Failure indicates public or serialized status-vocabulary drift.

    Limitations: Enumeration does not establish correlation of any real external
    outcome.
    """
    assert tuple(item.name for item in SUT) == ("CORRELATED", "MISMATCH")
    assert tuple(item.value for item in SUT) == ("correlated", "mismatch")
