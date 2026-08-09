r"""Software verification of ``ExampleOne``.

Facet and represented meaning
Software verification of exact public construction.
Intrinsic and cross-object scope
ExampleOne is the sole SUT and exact value semantics are the oracle.
VVUQ and scientific exclusions
No numerical verification, validation, UQ, or physical claim is made.
"""
from example import ExampleOne
SUT = ExampleOne

def test_constructor__value__preserves_input():
    """
    Evidence ID
    SV-EXAMPLE-099
    Requirement
    Construction preserves value.
    Method
    Construct publicly.
    Oracle
    Exact input value.
    Acceptance
    Exact equality.
    Interpretation
    Failure indicates drift.
    Limitations
    Other behavior is excluded.
    """
    assert SUT(1).value == 1
