r"""Software verification of ``HarnessInternalError``.

Facet and represented meaning
Software verification of the public ``HarnessInternalError`` surface; no physical model,
mathematical operator, or numerical representation is represented.

Intrinsic and cross-object scope
The sole primary SUT is ``HarnessInternalError``.  Accepted H1 field/wire contracts and
read-only H3 fixtures are independent exact oracles.

VVUQ and scientific exclusions
Passing checks only the stated software contract. Numerical verification, scientific
validation, uncertainty quantification, physical correctness, and cross-language
conformance are excluded.
"""

from __future__ import annotations

from typing import Any, cast

import pytest

from ksdft2effmass.harness.pi import HarnessInternalError

pytestmark = pytest.mark.software_verification
SUT = HarnessInternalError


def test_constructor__attributes__are_exact_and_immutable() -> None:
    """Evidence ID
    SV-HARNESS-024
    Requirement
    The internal-failure channel stores immutable operation and detail strings.
    Method
    Construct the error and attempt mutation.
    Oracle
    The accepted H1 support-error contract fixes both attributes and RuntimeError
    ancestry.
    Acceptance
    Exact strings are stored and later assignment raises AttributeError.
    Interpretation
    A failure identifies a production, accepted-contract, fixture, or environment
    discrepancy requiring independent review.
    Limitations
    This is exact software verification only; it makes no numerical,
    scientific-validation, UQ, physical, or Rust-conformance claim.
    """
    error = SUT("ResolveResource", "read race")
    observed = cast(Any, error)
    assert (observed.operation, observed.detail) == (
        "ResolveResource",
        "read race",
    )
    assert isinstance(error, RuntimeError)
    with pytest.raises(AttributeError):
        error.detail = "changed"
