r"""Software verification of private resource wire serializer implementation.

Evidence profile: routine

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

Routine software verification of resource and profile field mapping delegated by the
public harness wire boundary. No physical model, mathematical operator, or numerical
representation is represented.

Intrinsic and cross-object scope

The primary owner is the private resource wire serializer implementation.
``_ResourceWireSerializer`` is used only as a direct implementation access point; its
name, defining module, constructor, and identity are not public contracts. Fixed
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

from ksdft2effmass.harness.pi.wire.human_review import _ReviewOwnershipWireSerializer
from ksdft2effmass.harness.pi.wire.records import _CommonWireRecordSerializer
from ksdft2effmass.harness.pi.wire.resources import _ResourceWireSerializer

pytestmark = pytest.mark.software_verification
SUT = _ResourceWireSerializer


def test_artifact__resource_mapping__round_trips_project_profile_fixture() -> None:
    """Evidence ID: software-verification.harness.wire.resource-wire-codec.mapping

    Requirement: The codec owns project-profile mappings with explicit codec
    dependencies.

    Method: Decode and re-encode the fixed valid project-profile fixture.

    Oracle: The accepted valid project-profile wire fixture.

    Acceptance: The re-encoded object equals the parsed fixture exactly.

    Interpretation: Failure identifies resource/profile mapping or dependency drift.

    Limitations: One valid fixture does not exhaust invalid field partitions.
    """
    path = (
        Path(__file__).resolve().parents[7]
        / "harness/pi/fixtures/valid/project-profile.json"
    )
    obj = json.loads(path.read_text())
    codec = SUT(_CommonWireRecordSerializer(), _ReviewOwnershipWireSerializer())
    assert codec.encode(codec.decode("ProjectProfile", obj)) == obj
