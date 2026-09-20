r"""Software verification of ``Periodic1DIsolatedBandResultJsonSerializer``.

Evidence profile: claim_bearing

Bounded artifact scope: typed adaptation of the retained Appendix G isolated result.

Facet and represented meaning

Parent convergence, common-subspace errors, scalar reciprocal operators, complete
hoppings, range diagnostics, observables, and localization identity are included.

Intrinsic and cross-object scope

The typed result remains correlated with the complete immutable source document.

VVUQ and scientific exclusions

This read-only compatibility test does not rerun or scientifically validate the study.
"""

from pathlib import Path

import numpy as np
import pytest

from ksdft2effmass.campaigns.research_monograph import (
    Periodic1DIsolatedBandResultJsonSerializer,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DIsolatedBandResultJsonSerializer


class TestPeriodic1DIsolatedBandResultJsonSerializer:
    """Own typed compatibility evidence for the retained isolated result."""

    def test_method__decode_encode__extracts_correlated_domain_results(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-008

        Requirement: Every demonstrated isolated-band result channel needed by public
        analysis contracts has a typed immutable representation correlated to the full
        retained document.

        Method: Decode retained bytes, assert independent inventory and identity
        literals, reconstruct canonical bytes, and decode the typed result again.

        Oracle: The retained Appendix G ``result.json`` artifact and its named studies.

        Acceptance: Study sizes, scalar model dimensions, representatives, density
        identity, and reconstructed reciprocal values agree exactly or by array value.

        Interpretation: A pass establishes typed retained-result compatibility.

        Limitations: The test does not establish calculation correctness, scientific
        validation, material relevance, or uncertainty quantification.

        Provenance: Retained Appendix G isolated-band result bytes.
        """
        repository_root = Path(__file__).resolve().parents[7]
        payload = repository_root.joinpath(
            "calculations/research-monograph/periodic-1d/result.json"
        ).read_bytes()
        serializer = SUT()

        result = serializer.deserialize(payload)
        reconstructed = serializer.deserialize(serializer.serialize(result))

        assert len(result.parent_verification.plane_wave_cutoff_study) == 5
        assert len(result.parent_verification.finite_difference_grid_study) == 4
        assert len(result.parent_verification.common_low_mode_operator_study) == 4
        assert len(result.parent_verification.weak_potential_gap_study) == 4
        assert result.reduction.reciprocal_samples.matrix_dimension == 1
        assert result.reduction.hopping_model.matrix_dimension == 1
        assert len(result.reduction.hopping_model.representatives) == 64
        assert len(result.reduction.hopping_range_study) == 7
        assert (
            result.reduction.localization.profile_density_content_sha256
            == "815c158b3196c5141e44489afa1f84ea8249ad0db6e2687f549df64ec047dc3b"
        )
        np.testing.assert_array_equal(
            reconstructed.reduction.reciprocal_samples.coordinates.magnitude,
            result.reduction.reciprocal_samples.coordinates.magnitude,
        )
        assert reconstructed.source_document.root == result.source_document.root
