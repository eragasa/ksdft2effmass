r"""Software verification of ``ExampleRecord``.

Facet and represented meaning

Software verification of exact public record construction and represented value.

Intrinsic and cross-object scope

``ExampleRecord`` is the sole SUT; exact public value semantics supply the oracle.

VVUQ and scientific exclusions

Passing establishes only the stated software contract, not numerical verification,
scientific validation, UQ, physical correctness, or cross-language agreement.
"""

import pytest
from example import ExampleRecord

SUT = ExampleRecord


@pytest.mark.parametrize("value", [pytest.param(1, id="SV-EXAMPLE-001-positive_one")])
def test_constructor__public_fields__preserves_exact_value(value):
    """Evidence ID: SV-EXAMPLE-001

    Requirement: Construction preserves the public value.

    Method: Construct through the public API over the declared partition.

    Oracle: Exact Python value semantics supply the expected value.

    Acceptance: Stored and input values are exactly equal.

    Interpretation: Failure may identify implementation, fixture, environment,
    oracle, or contract defects.

    Limitations: No numerical verification, scientific validation, UQ, physical, or
    cross-language claim.
    """
    assert SUT(value).value == value
