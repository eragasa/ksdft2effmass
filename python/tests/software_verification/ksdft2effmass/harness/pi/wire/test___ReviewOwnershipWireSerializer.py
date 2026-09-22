r"""Software verification of private review-ownership wire serializer implementation.

Evidence profile: routine

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

Routine software verification of review-ownership field mapping delegated by the public
harness wire boundary. No physical model, mathematical operator, or numerical
representation is represented.

Intrinsic and cross-object scope

The primary owner is the private review-ownership wire serializer implementation.
``_ReviewOwnershipWireSerializer`` is used only as a direct implementation access point;
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

from ksdft2effmass.harness.pi.wire.human_review import _ReviewOwnershipWireSerializer

pytestmark = pytest.mark.software_verification
SUT = _ReviewOwnershipWireSerializer


def test_artifact__review_ownership_mapping__round_trips_ownership_fixture() -> None:
    """Evidence ID: software-verification.harness.wire.review-ownership-codec.mapping

    Requirement: The codec owns nested ownership-manifest field mappings.

    Method: Decode and re-encode the fixed valid ownership-manifest fixture.

    Oracle: The accepted valid ownership-manifest wire fixture.

    Acceptance: The re-encoded object equals the parsed fixture exactly.

    Interpretation: Failure identifies review-ownership mapping drift.

    Limitations: One valid fixture does not exhaust invalid field partitions.
    """
    path = (
        Path(__file__).resolve().parents[7]
        / "harness/pi/fixtures/valid/ownership-manifest-view.json"
    )
    obj = json.loads(path.read_text())
    codec = SUT()
    assert codec.encode(codec.decode("OwnershipManifestView", obj)) == obj
