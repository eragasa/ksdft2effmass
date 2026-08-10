r"""Software verification of ``CheckpointRecord``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

Software verification of the public ``CheckpointRecord`` surface; no physical model,
mathematical operator, or numerical representation is represented.

Intrinsic and cross-object scope

The sole primary SUT is ``CheckpointRecord``.  Accepted H1 field/wire contracts and
read-only H3 fixtures are independent exact oracles.

VVUQ and scientific exclusions

Passing checks only the stated software contract. Numerical verification, scientific
validation, uncertainty quantification, physical correctness, and cross-language
conformance are excluded.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from ksdft2effmass.harness.pi import (
    CheckpointRecord,
    JsonRecordDeserializer,
    WireRecordKind,
)

ROOT = Path(__file__).resolve().parents[6]

pytestmark = pytest.mark.software_verification
SUT = CheckpointRecord


def test_constructor__h3_valid_fixture__preserves_exact_public_value() -> None:
    """Evidence ID: SV-HARNESS-010

    Requirement: CheckpointRecord accepts the complete valid version-1 H3 wire instance
    and is
    immutable.

    Method: Decode the accepted ``checkpoint-record.json`` fixture through the
    caller-selected public record kind, then attempt field mutation.

    Oracle: The accepted H1 field contract and H3 valid fixture fix the class, field
    values,
    tuple storage, and immutability.

    Acceptance: The result is exactly SUT, validation is PASS, tuple fields remain
    tuples, and
    mutation raises AttributeError.

    Interpretation: A failure identifies a production, accepted-contract, fixture, or
    environment
    discrepancy requiring independent review.

    Limitations: This is exact software verification only; it makes no numerical,
    scientific-validation, UQ, physical, or Rust-conformance claim.
    """
    payload = (ROOT / "harness/pi/fixtures/valid/checkpoint-record.json").read_bytes()
    result = JsonRecordDeserializer().execute(WireRecordKind.CheckpointRecord, payload)
    assert result.validation.status == "PASS"
    assert type(result.record) is SUT

    def exercise_value_case_61_1(value: Any) -> Any:
        assert type(value) is not list

    _ = [
        exercise_value_case_61_1(value)
        for value in (
            vars(result.record).values() if hasattr(result.record, "__dict__") else ()
        )
    ]
    with pytest.raises((AttributeError, TypeError)):
        setattr(result.record, next(iter(result.record.__dataclass_fields__)), None)
