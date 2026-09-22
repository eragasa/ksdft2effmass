r"""Software verification of ``Periodic1DStressResultJsonSerializer``.

Evidence profile: claim_bearing

Bounded artifact scope: typed adaptation of the retained Appendix G stress result.

Facet and represented meaning

Amplitude, mesh/band/isolation, shape, gauge, and fitting-route channels are retained.

Intrinsic and cross-object scope

The typed channels remain correlated with the complete immutable source document.

VVUQ and scientific exclusions

This read-only compatibility test does not rerun or scientifically validate the study.
"""

from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph import (
    Periodic1DStressResultJsonSerializer,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DStressResultJsonSerializer


class TestPeriodic1DStressResultJsonSerializer:
    """Own typed compatibility evidence for the retained stress result."""

    def test_method__deserialize_serialize__extracts_all_stress_channels(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-010

        Requirement: Every demonstrated stress-result channel has a typed immutable
        representation correlated to the complete retained result document.

        Method: Deserialize retained bytes, assert independent channel sizes and named
        shape identities, then deserialize the canonical reconstruction.

        Oracle: The retained Appendix G ``stress-result.json`` artifact.

        Acceptance: Seven amplitude cases, 210 mesh/band cases, six shape cases, gauge
        mesh 64, and route range 3 are retained with equal reconstructed source roots.

        Interpretation: A pass establishes typed stress-result wire compatibility.

        Limitations: Calculation correctness, validation, and UQ are not established.

        Provenance: Retained Appendix G stress-result bytes.
        """
        repository_root = Path(__file__).resolve().parents[7]
        payload = repository_root.joinpath(
            "calculations/research-monograph/periodic-1d/stress-result.json"
        ).read_bytes()
        serializer = SUT()

        result = serializer.deserialize(payload)
        reconstructed = serializer.deserialize(serializer.serialize(result))

        assert len(result.potential_amplitude_stress) == 7
        assert len(result.mesh_band_and_isolation_stress) == 210
        assert tuple(
            case.identifier for case in result.potential_shape_stress.cases
        ) == (
            "baseline_cosine",
            "translated_cosine",
            "constant_shifted_cosine",
            "second_harmonic_cosine",
            "inversion_broken",
            "three_harmonic",
        )
        assert result.gauge_covariance_stress.mesh_size == 64
        assert result.route_assumption_stress.hopping_range_cells == 3
        assert reconstructed.source_document.root == result.source_document.root
