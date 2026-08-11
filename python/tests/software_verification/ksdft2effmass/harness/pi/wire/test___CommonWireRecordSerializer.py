r"""Software verification of private common wire-record serializer implementation.

Evidence profile: routine

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

Routine software verification of common wire-record field mapping delegated by the
public harness wire boundary. No physical model, mathematical operator, or numerical
representation is represented.

Intrinsic and cross-object scope

The primary owner is the private common wire-record serializer implementation.
``_CommonWireRecordSerializer`` is used only as a direct implementation access point;
its name, defining module, constructor, and identity are not public contracts. Fixed
accepted fixtures and exact Python or JSON semantics are the behavioral oracles.

VVUQ and scientific exclusions

Passing checks only private implementation behavior supporting the public contract. It
does not make the private class public or establish numerical verification, scientific
validation, uncertainty quantification, physical correctness, or human acceptance.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ksdft2effmass.harness.pi.wire.records import _CommonWireRecordSerializer

pytestmark = pytest.mark.software_verification
SUT = _CommonWireRecordSerializer


def test_artifact__common_mapping__round_trips_validation_fixture() -> None:
    """Evidence ID: software-verification.harness.wire.common-record-codec.mapping

    Requirement: The codec owns nested common validation-result field mappings.

    Method: Decode and re-encode the fixed valid validation-result fixture.

    Oracle: The accepted valid validation-result wire fixture.

    Acceptance: The re-encoded object equals the parsed fixture exactly.

    Interpretation: Failure identifies common-record mapping drift.

    Limitations: One valid fixture does not exhaust all common record kinds.
    """
    path = (
        Path(__file__).resolve().parents[7]
        / "harness/pi/fixtures/valid/validation-result.json"
    )
    obj = json.loads(path.read_text())
    codec = SUT()
    assert codec.encode(codec.decode("ValidationResult", obj)) == obj
