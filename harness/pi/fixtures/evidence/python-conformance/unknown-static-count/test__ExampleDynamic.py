r"""Software verification of ``ExampleDynamic``.

Facet and represented meaning
Software verification of dynamic controlled inputs.
Intrinsic and cross-object scope
ExampleDynamic is the sole SUT.
VVUQ and scientific exclusions
No numerical verification, validation, UQ, or physical claim is made.
"""
import pytest
from example import ExampleDynamic
SUT = ExampleDynamic
CASES = [pytest.param(1, id="positive_one")]

@pytest.mark.parametrize("value", CASES)
def test_constructor__value__preserves_input(value):
    """
    Evidence ID
    SV-EXAMPLE-098
    Requirement
    Construction preserves value.
    Method
    Construct over externally assembled cases.
    Oracle
    Exact input value.
    Acceptance
    Exact equality.
    Interpretation
    Failure indicates drift.
    Limitations
    Static collection is intentionally unknown.
    """
    assert SUT(value).value == value
