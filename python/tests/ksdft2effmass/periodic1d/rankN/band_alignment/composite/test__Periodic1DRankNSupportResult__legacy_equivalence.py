"""Legacy-equivalence checks for the relocated rank-N support-result type."""

import pytest

from ksdft2effmass.periodic1d.rankN.band_alignment.composite import (
    Periodic1DRankNAlignmentCalculationResult,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.results.support import (  # noqa: E501
    Periodic1DRankNSupportResult as LegacyEquivalenceSupportResult,
)
from ksdft2effmass.periodic1d.rankN.support_truncation import (
    Periodic1DRankNSupportResult,
)

pytestmark = [
    pytest.mark.expensive,
    pytest.mark.integration,
    pytest.mark.legacy_equivalence,
    pytest.mark.software_verification,
]


class TestPeriodic1DRankNSupportResult:
    """Limit legacy equivalence to class identity and unchanged JSON bytes."""

    def test__legacy_equivalence__preserves_class_and_json_bytes(
        self,
        higher_rank_calculation_result: Periodic1DRankNAlignmentCalculationResult,
    ) -> None:
        assert LegacyEquivalenceSupportResult is Periodic1DRankNSupportResult
        for mesh in higher_rank_calculation_result.meshes:
            for alignment in mesh.gauge_alignment_results:
                for support in alignment.supports:
                    original_bytes = support.to_json()
                    canonical_decoded = Periodic1DRankNSupportResult.from_json(
                        original_bytes
                    )
                    legacy_equivalence_decoded = (
                        LegacyEquivalenceSupportResult.from_json(original_bytes)
                    )
                    assert canonical_decoded.to_json() == original_bytes
                    assert legacy_equivalence_decoded.to_json() == original_bytes
