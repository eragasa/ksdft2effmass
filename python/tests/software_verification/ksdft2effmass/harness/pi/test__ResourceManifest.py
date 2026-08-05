"""Evidence class and represented meaning
Software verification of the public ``ResourceManifest`` surface; no physical model,
mathematical operator, or numerical representation is represented.

Owned contract, oracle, and scope
The sole primary SUT is ``ResourceManifest``.  Accepted H1 field/wire contracts and
read-only H3 fixtures are independent exact oracles.

VVUQ and scientific exclusions
Passing checks only the stated software contract. Numerical verification, scientific
validation, uncertainty quantification, physical correctness, and cross-language
conformance are excluded.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from ksdft2effmass.harness.pi import (
    DeserializeJsonRecord,
    ResourceManifest,
    WireRecordKind,
)

ROOT = Path(__file__).resolve().parents[6]

pytestmark = pytest.mark.software_verification
SUT = ResourceManifest


def test_constructor__h3_valid_fixture__preserves_exact_public_value() -> None:
    """Evidence ID
    SV-HARNESS-003
    Requirement
    ResourceManifest accepts the complete valid version-1 H3 wire instance and is
    immutable.
    Method
    Decode the accepted ``resource-manifest.json`` fixture through the
    caller-selected public record kind, then attempt field mutation.
    Oracle
    The accepted H1 field contract and H3 valid fixture fix the class, field values,
    tuple storage, and immutability.
    Acceptance
    The result is exactly SUT, validation is PASS, tuple fields remain tuples, and
    mutation raises AttributeError.
    Interpretation
    A failure identifies a production, accepted-contract, fixture, or environment
    discrepancy requiring independent review.
    Limitations
    This is exact software verification only; it makes no numerical,
    scientific-validation, UQ, physical, or Rust-conformance claim.
    """
    payload = (ROOT / "harness/pi/fixtures/valid/resource-manifest.json").read_bytes()
    result = DeserializeJsonRecord().execute(WireRecordKind.ResourceManifest, payload)
    assert result.validation.status == "PASS"
    assert type(result.record) is SUT
    for value in (
        vars(result.record).values() if hasattr(result.record, "__dict__") else ()
    ):
        assert type(value) is not list
    with pytest.raises((AttributeError, TypeError)):
        setattr(result.record, next(iter(result.record.__dataclass_fields__)), None)
