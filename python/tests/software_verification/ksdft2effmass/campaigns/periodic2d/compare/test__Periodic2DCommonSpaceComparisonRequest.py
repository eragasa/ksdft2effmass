"""Software verification for ``Periodic2DCommonSpaceComparisonRequest``."""

import pytest

from ksdft2effmass.campaigns.periodic2d import (
    Periodic2DCommonSpaceComparisonRequest,
)
from ksdft2effmass.campaigns.periodic2d.model.toy_models import (
    Periodic2DCosinePotentialToyModel,
    Periodic2DFiniteDifferenceHamiltonianConstructor,
    Periodic2DFiniteDifferenceHamiltonianRequest,
    Periodic2DFiniteDifferenceHamiltonianResult,
    Periodic2DPlaneWaveHamiltonianConstructor,
    Periodic2DPlaneWaveHamiltonianRequest,
    Periodic2DPlaneWaveHamiltonianResult,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic2DCommonSpaceComparisonRequest:
    """Own represented-space compatibility and alias-precondition evidence."""

    @staticmethod
    def represented_results(
        *,
        cutoff: int = 1,
        points: int = 5,
        finite_momentum_y: float = -0.2,
    ) -> tuple[
        Periodic2DPlaneWaveHamiltonianResult,
        Periodic2DFiniteDifferenceHamiltonianResult,
    ]:
        """Return compatible or intentionally varied represented test results."""
        model = Periodic2DCosinePotentialToyModel(0.4, 0.7, 0.2)
        plane = Periodic2DPlaneWaveHamiltonianConstructor().execute(
            Periodic2DPlaneWaveHamiltonianRequest(model, 0.1, -0.2, cutoff)
        )
        finite = Periodic2DFiniteDifferenceHamiltonianConstructor().execute(
            Periodic2DFiniteDifferenceHamiltonianRequest(
                model, 0.1, finite_momentum_y, points
            )
        )
        return plane, finite

    def test_construction__compatible_results__retains_common_dimension(self) -> None:
        """Matching model, momentum, and resolvable basis define a comparison."""
        plane, finite = self.represented_results()

        request = Periodic2DCommonSpaceComparisonRequest(
            plane,
            finite,
            "cosine-common-space",
        )

        assert request.common_dimension == 9
        assert request.comparison_identifier == "cosine-common-space"

    def test_construction__different_model__raises_value_error(self) -> None:
        """Operators with different Fourier potentials cannot be subtracted."""
        plane, _ = self.represented_results()
        different_model = Periodic2DCosinePotentialToyModel(0.4, 0.7, 0.3)
        finite = Periodic2DFiniteDifferenceHamiltonianConstructor().execute(
            Periodic2DFiniteDifferenceHamiltonianRequest(different_model, 0.1, -0.2, 5)
        )

        with pytest.raises(ValueError, match="same toy model"):
            Periodic2DCommonSpaceComparisonRequest(
                plane,
                finite,
                "mismatched-models",
            )

    def test_construction__different_momentum__raises_value_error(self) -> None:
        """Operators from different Bloch fibers cannot be subtracted."""
        plane, finite = self.represented_results(finite_momentum_y=-0.1)

        with pytest.raises(ValueError, match="same Bloch momentum"):
            Periodic2DCommonSpaceComparisonRequest(
                plane,
                finite,
                "mismatched-fibers",
            )

    def test_construction__aliased_basis__raises_value_error(self) -> None:
        """A grid smaller than the retained reciprocal side cannot define the map."""
        plane, finite = self.represented_results(cutoff=3, points=5)

        with pytest.raises(ValueError, match="resolve every plane-wave"):
            Periodic2DCommonSpaceComparisonRequest(
                plane,
                finite,
                "aliased-common-space",
            )
