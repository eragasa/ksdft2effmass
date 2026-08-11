r"""Software verification of private Task wire serializer implementation.

Evidence profile: routine

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

Routine software verification of Task and chain field mapping delegated by the public
harness wire boundary. No physical model, mathematical operator, or numerical
representation is represented.

Intrinsic and cross-object scope

The primary owner is the private Task wire serializer implementation.
``_TaskWireSerializer`` is used only as a direct implementation access point; its name,
defining module, constructor, and identity are not public contracts. Fixed accepted
fixtures and exact Python or JSON semantics are the behavioral oracles.

VVUQ and scientific exclusions

Passing checks only private implementation behavior supporting the public contract. It
does not make the private class public or establish numerical verification, scientific
validation, uncertainty quantification, physical correctness, or human acceptance.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ksdft2effmass.harness.pi.wire.tasks import _TaskWireSerializer

pytestmark = pytest.mark.software_verification
SUT = _TaskWireSerializer


def test_artifact__task_mapping__round_trips_chain_fixture() -> None:
    """Evidence ID: software-verification.harness.wire.task-wire-codec.mapping

    Requirement: The codec owns nested Task-reference and chain field mappings.

    Method: Decode and re-encode the fixed valid chain fixture.

    Oracle: The accepted valid chain wire fixture.

    Acceptance: The re-encoded object equals the parsed fixture exactly.

    Interpretation: Failure identifies Task or chain mapping drift.

    Limitations: One valid fixture does not exhaust invalid field partitions.
    """
    path = (
        Path(__file__).resolve().parents[7]
        / "harness/pi/fixtures/valid/chain-view.json"
    )
    obj = json.loads(path.read_text())
    codec = SUT()
    assert codec.encode(codec.decode("ChainView", obj)) == obj
