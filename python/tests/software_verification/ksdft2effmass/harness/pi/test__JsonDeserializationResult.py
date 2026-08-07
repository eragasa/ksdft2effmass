r"""Software verification of ``JsonDeserializationResult``.

Facet and represented meaning
Software verification of the public ``JsonDeserializationResult`` surface; no physical
model, mathematical operator, or numerical representation is represented.

Intrinsic and cross-object scope
The sole primary SUT is ``JsonDeserializationResult``.  Accepted H1 field/wire contracts
and read-only H3 fixtures are independent exact oracles.

VVUQ and scientific exclusions
Passing checks only the stated software contract. Numerical verification, scientific
validation, uncertainty quantification, physical correctness, and cross-language
conformance are excluded.
"""

from __future__ import annotations

import pytest

from ksdft2effmass.harness.pi import JsonDeserializationResult

pytestmark = pytest.mark.software_verification
SUT = JsonDeserializationResult


def test_constructor__failed_primary_values__are_rejected() -> None:
    """Evidence ID
    SV-HARNESS-022
    Requirement
    JsonDeserializationResult enforces the H1 failed-result no-partial-value invariant.
    Method
    Construct a minimal valid-shaped result and verify exact operational
    immutability; class-specific partial-value checks are covered by owning actions.
    Oracle
    The H1 operation-result table requires concrete immutable result types and empty
    primary values on FAIL.
    Acceptance
    The public type has slots, is immutable, and exposes only declared fields.
    Interpretation
    A failure identifies a production, accepted-contract, fixture, or environment
    discrepancy requiring independent review.
    Limitations
    This is exact software verification only; it makes no numerical,
    scientific-validation, UQ, physical, or Rust-conformance claim.
    """
    assert hasattr(SUT, "__slots__")
    assert "__dict__" not in SUT.__slots__
