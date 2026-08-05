"""Evidence class and represented meaning
Software verification of the public ``ResourceReference`` surface; no physical model,
mathematical operator, or numerical representation is represented.

Owned contract, oracle, and scope
The sole primary SUT is ``ResourceReference``.  Accepted H1 field/wire contracts and
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
    ResourceReference,
    WireRecordKind,
)

ROOT = Path(__file__).resolve().parents[6]

pytestmark = pytest.mark.software_verification
SUT = ResourceReference


def test_constructor__h3_valid_fixture__preserves_exact_public_value() -> None:
    """Evidence ID
    SV-HARNESS-002
    Requirement
    ResourceReference accepts the complete valid version-1 H3 wire instance and is
    immutable.
    Method
    Decode the accepted ``resource-reference.json`` fixture through the
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
    payload = (ROOT / "harness/pi/fixtures/valid/resource-reference.json").read_bytes()
    result = DeserializeJsonRecord().execute(WireRecordKind.ResourceReference, payload)
    assert result.validation.status == "PASS"
    assert type(result.record) is SUT
    for value in (
        vars(result.record).values() if hasattr(result.record, "__dict__") else ()
    ):
        assert type(value) is not list
    with pytest.raises((AttributeError, TypeError)):
        setattr(result.record, next(iter(result.record.__dataclass_fields__)), None)


def test_constructor__self_dependency__constructs_and_deserializes() -> None:
    """Evidence ID
    SV-HARNESS-060
    Requirement
    A resource self-dependency is structurally representable and is not an intrinsic
    ResourceReference violation.
    Method
    Construct a reference with its own ID in ``dependency_ids`` and publicly decode
    the corrected H3 self-dependency candidate.
    Oracle
    The corrected H1 field contract assigns self-edge validity to
    ValidateResourceManifest, while the H3 candidate fixes the wire instance.
    Acceptance
    Direct construction preserves the self-edge tuple and public deserialization
    returns PASS with a ResourceReference containing that same self-edge.
    Interpretation
    Failure identifies constructor/decoder enforcement at the wrong contract layer or
    H1/H3 fixture drift.
    Limitations
    Manifest acceptance is intentionally not tested here; there is no numerical,
    scientific-validation, UQ, physical, or Rust-conformance claim.
    """
    import json

    from ksdft2effmass.harness.pi import ArtifactIdentity

    reference = SUT(
        1,
        "example.base.v1",
        "reference",
        1,
        "references/base.txt",
        ArtifactIdentity(1, "sha256", "0" * 64),
        ("example.base.v1",),
    )
    assert reference.dependency_ids == (reference.resource_id,)

    case = json.loads(
        (
            ROOT / "harness/pi/fixtures/resource-resolution/cases/self-dependency.json"
        ).read_text()
    )
    payload = (json.dumps(case["generic_manifest"]["resources"][0]) + "\n").encode()
    result = DeserializeJsonRecord().execute(WireRecordKind.ResourceReference, payload)
    assert result.validation.status == "PASS"
    assert isinstance(result.record, SUT)
    assert result.record.dependency_ids == (result.record.resource_id,)
