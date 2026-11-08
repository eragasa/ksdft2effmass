"""Software verification for ``Periodic2DCommonSpaceComparisonResult``."""

import numpy as np
import pytest
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    ScalarQuantity,
    Unitless,
)

from ksdft2effmass.periodic.models import PeriodicModelRole
from ksdft2effmass.periodic.periodic2d.models import (
    Periodic2DCosinePotentialModel,
    Periodic2DFiniteDifferenceHamiltonian,
    Periodic2DFiniteDifferenceHamiltonianRequest,
    Periodic2DPlaneWaveHamiltonian,
    Periodic2DPlaneWaveHamiltonianRequest,
)
from ksdft2effmass.periodic2d.compare.common_space import (
    Periodic2DCommonSpaceComparisonRequest,
    Periodic2DCommonSpaceComparisonResult,
    Periodic2DCommonSpaceOperatorComparator,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic2DCommonSpaceComparisonResult:
    """Own result correlation, unit, shape, and exact-difference evidence."""

    @staticmethod
    def request() -> Periodic2DCommonSpaceComparisonRequest:
        """Return a compatible cutoff-one, five-point comparison request."""
        model = Periodic2DCosinePotentialModel(
            0.4, 0.7, 0.2, role=PeriodicModelRole.CONTROL_MODEL
        )
        plane = Periodic2DPlaneWaveHamiltonian(
            Periodic2DPlaneWaveHamiltonianRequest(model, 0.1, -0.2, 1)
        ).result()
        finite = Periodic2DFiniteDifferenceHamiltonian(
            Periodic2DFiniteDifferenceHamiltonianRequest(model, 0.1, -0.2, 5)
        ).result()
        return Periodic2DCommonSpaceComparisonRequest(
            plane, finite, "cosine-common-space"
        )

    def test__Periodic2DCommonSpaceComparisonResult__execute__valid_result__retains_immutable_correlated_outputs(  # noqa: E501
        self,
    ) -> None:
        """The comparator returns immutable matrices tied to the exact request."""
        request = self.request()

        result = Periodic2DCommonSpaceOperatorComparator().execute(request)

        assert result.request is request
        assert result.plane_wave_to_grid.magnitude.shape == (25, 9)
        assert result.transported_finite_difference.magnitude.shape == (9, 9)
        assert result.operator_difference.magnitude.shape == (9, 9)
        assert not result.operator_difference.magnitude.flags.writeable
        assert result.operator_frobenius_error.magnitude >= 0.0
        assert result.operator_maximum_absolute_error.magnitude >= 0.0

    def test__Periodic2DCommonSpaceComparisonResult__construction__forged_difference__raises_value_error(  # noqa: E501
        self,
    ) -> None:
        """The retained difference must equal transported minus plane-wave matrices."""
        source = Periodic2DCommonSpaceOperatorComparator().execute(self.request())

        with pytest.raises(ValueError, match="must equal"):
            Periodic2DCommonSpaceComparisonResult(
                request=source.request,
                plane_wave_to_grid=source.plane_wave_to_grid,
                transported_finite_difference=source.transported_finite_difference,
                operator_difference=ComplexMatrixQuantity(
                    np.zeros((9, 9), dtype=np.complex128), Unitless()
                ),
                isometry_frobenius_defect=source.isometry_frobenius_defect,
                operator_frobenius_error=source.operator_frobenius_error,
                operator_maximum_absolute_error=(
                    source.operator_maximum_absolute_error
                ),
            )

    def test__Periodic2DCommonSpaceComparisonResult__construction__forged_metric__raises_value_error(  # noqa: E501
        self,
    ) -> None:
        """Diagnostic magnitudes must be derived from the retained matrices."""
        source = Periodic2DCommonSpaceOperatorComparator().execute(self.request())

        with pytest.raises(ValueError, match="must match operator_difference"):
            Periodic2DCommonSpaceComparisonResult(
                request=source.request,
                plane_wave_to_grid=source.plane_wave_to_grid,
                transported_finite_difference=source.transported_finite_difference,
                operator_difference=source.operator_difference,
                isometry_frobenius_defect=source.isometry_frobenius_defect,
                operator_frobenius_error=ScalarQuantity(0.0, Unitless()),
                operator_maximum_absolute_error=(
                    source.operator_maximum_absolute_error
                ),
            )
