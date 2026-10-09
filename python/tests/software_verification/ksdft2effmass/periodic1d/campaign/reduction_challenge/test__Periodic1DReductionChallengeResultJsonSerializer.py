r"""Software verification of ``Periodic1DReductionChallengeResultJsonSerializer``.

Evidence profile: claim_bearing

Bounded artifact scope: typed adaptation of the retained Appendix G stress result.

Facet and represented meaning

Amplitude, mesh/band/isolation, shape, gauge, and fitting-route channels are retained.

Intrinsic and cross-object scope

The typed channels remain correlated with the complete immutable source document.

VVUQ and scientific exclusions

This read-only compatibility test does not rerun or scientifically validate the study.
"""

import json
from pathlib import Path

import pytest

from ksdft2effmass.periodic1d.campaign.reduction_challenge import (
    Periodic1DReductionChallengeResultJsonSerializer,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DReductionChallengeResultJsonSerializer


class TestPeriodic1DReductionChallengeResultJsonSerializer:
    """Own typed compatibility evidence for the retained challenge result."""

    @staticmethod
    def _payload() -> bytes:
        """Return the exact retained result bytes."""
        repository_root = Path(__file__).resolve().parents[7]
        return repository_root.joinpath(
            "calculations/research-monograph/periodic-1d/stress-result.json"
        ).read_bytes()

    @staticmethod
    def _encoded(document: dict[str, object]) -> bytes:
        """Return one deterministic mutated JSON fixture."""
        return (
            json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n"
        ).encode()

    def test_method__deserialize_serialize__extracts_all_challenge_channels(
        self,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-010

        Requirement: Every demonstrated challenge channel has a typed immutable
        representation correlated to the complete retained result document.

        Method: Deserialize retained bytes, assert independent channel sizes and named
        shape identities, then deserialize the canonical reconstruction.

        Oracle: The retained Appendix G ``stress-result.json`` artifact.

        Acceptance: Seven amplitude cases, 210 mesh/band cases, six shape cases, gauge
        mesh 64, and route range 3 are retained with equal reconstructed source roots.

        Interpretation: A pass establishes typed historical-result compatibility.

        Limitations: Calculation correctness, validation, and UQ are not established.

        Provenance: Retained Appendix G stress-result bytes.
        """
        serializer = SUT()

        result = serializer.deserialize(self._payload())
        reconstructed = serializer.deserialize(serializer.serialize(result))

        assert len(result.potential_amplitude) == 7
        assert len(result.mesh_band_isolation) == 210
        assert tuple(case.identifier for case in result.potential_shapes.cases) == (
            "baseline_cosine",
            "translated_cosine",
            "constant_shifted_cosine",
            "second_harmonic_cosine",
            "inversion_broken",
            "three_harmonic",
        )
        assert result.gauge_covariance.mesh_size == 64
        assert result.route_assumptions.hopping_range_cells == 3
        assert reconstructed.source_document.root == result.source_document.root

    def test_method__deserialize__rejects_changed_evidence_status(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-060-026.

        Requirement: The historical schema-one evidence-status literal is immutable.

        Method: Replace only that literal in an otherwise complete result document.

        Oracle: The reviewed version-one wire contract.

        Acceptance: Deserialization raises ``ValueError``.

        Interpretation: A pass prevents broadening the result's evidence class.

        Limitations: The literal does not itself establish scientific validity.
        """
        document = json.loads(self._payload())
        document["evidence_status"] = "validated material result"

        with pytest.raises(ValueError, match="evidence_status"):
            SUT().deserialize(self._encoded(document))

    def test_method__deserialize__rejects_changed_root_field_set(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-060-027.

        Requirement: The result root uses one exact closed version-one field set.

        Method: Independently add an unknown field and remove a required field.

        Oracle: The retained schema-one result shape.

        Acceptance: Both altered documents raise ``ValueError``.

        Interpretation: A pass excludes silent root-schema extensions and omissions.

        Limitations: Closed fields do not authenticate producer provenance.
        """
        added = json.loads(self._payload())
        added["unreviewed_extension"] = True
        missing = json.loads(self._payload())
        del missing["schema_version"]

        with pytest.raises(ValueError, match="fields must match"):
            SUT().deserialize(self._encoded(added))
        with pytest.raises(ValueError, match="required routing field"):
            SUT().deserialize(self._encoded(missing))

    def test_method__deserialize__rejects_changed_nested_field_set(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-060-028.

        Requirement: Every nested observation and provenance object is closed.

        Method: Add an unknown potential-shape field and remove a route field.

        Oracle: The retained schema-one nested object shapes.

        Acceptance: Both altered documents raise ``ValueError``.

        Interpretation: A pass excludes unreviewed nested schema drift.

        Limitations: Field closure does not prove decoded numerical correctness.
        """
        added = json.loads(self._payload())
        added["potential_shape_stress"]["cases"][0]["unknown"] = 0
        missing = json.loads(self._payload())
        del missing["route_assumption_stress"]["mesh_size"]

        for document in (added, missing):
            with pytest.raises(ValueError, match="fields must match"):
                SUT().deserialize(self._encoded(document))

    def test_contract__retired_forwarding_methods_are_absent(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-060-003.

        Requirement: The canonical result codec exposes only nominal ``serialize`` and
        ``deserialize`` operations.

        Method: Inspect one serializer instance for former forwarding names.

        Oracle: Row-060 no-compatibility-alias policy.

        Acceptance: Neither ``encode`` nor ``decode`` exists.

        Interpretation: A pass establishes one reviewed codec surface.

        Limitations: Method absence does not establish decoded correctness.
        """
        serializer = SUT()

        assert not hasattr(serializer, "encode")
        assert not hasattr(serializer, "decode")
