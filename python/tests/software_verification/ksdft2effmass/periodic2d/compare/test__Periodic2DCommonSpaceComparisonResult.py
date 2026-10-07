"""Software verification for ``Periodic2DCommonSpaceComparisonResult``.

Synthetic cosine-model represented operators establish immutable shape, unit, exact
transport, signed-difference, and diagnostic-correlation contracts. The fixtures are
software inputs rather than retained calculations or literature values. Exact array
comparisons are required for algebra retained by one Result; no scientific tolerance
or acceptance threshold is introduced.

Passing this module does not establish continuum convergence, parent-model adequacy,
scientific validation, uncertainty quantification, or human acceptance.
"""

import numpy as np
import pytest

from ksdft2effmass.operators import ComplexMatrixQuantity, ScalarQuantity, Unitless
from ksdft2effmass.periodic2d.compare.common_space import (
    Periodic2DCommonSpaceComparisonRequest,
    Periodic2DCommonSpaceComparisonResult,
    Periodic2DCommonSpaceOperatorComparator,
)
from ksdft2effmass.periodic2d.model.toy_models import (
    Periodic2DCosinePotentialToyModel,
    Periodic2DFiniteDifferenceHamiltonianConstructor,
    Periodic2DFiniteDifferenceHamiltonianRequest,
    Periodic2DPlaneWaveHamiltonianConstructor,
    Periodic2DPlaneWaveHamiltonianRequest,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic2DCommonSpaceComparisonResult:
    """Own intrinsic common-space structure and algebraic-correlation evidence."""

    @staticmethod
    def request() -> Periodic2DCommonSpaceComparisonRequest:
        """Return a compatible cutoff-one, five-point synthetic comparison request."""
        model = Periodic2DCosinePotentialToyModel(0.4, 0.7, 0.2)
        plane = Periodic2DPlaneWaveHamiltonianConstructor().execute(
            Periodic2DPlaneWaveHamiltonianRequest(model, 0.1, -0.2, 1)
        )
        finite = Periodic2DFiniteDifferenceHamiltonianConstructor().execute(
            Periodic2DFiniteDifferenceHamiltonianRequest(model, 0.1, -0.2, 5)
        )
        return Periodic2DCommonSpaceComparisonRequest(
            plane, finite, "cosine-common-space"
        )

    @staticmethod
    def result() -> Periodic2DCommonSpaceComparisonResult:
        """Return one valid Action-produced Result used as immutable mutation source."""
        return Periodic2DCommonSpaceOperatorComparator().execute(
            TestPeriodic2DCommonSpaceComparisonResult.request()
        )

    def test_construction__valid_result__retains_immutable_correlated_outputs(
        self,
    ) -> None:
        """The Result keeps directional dimensions and immutable unitless quantities."""
        source = self.result()

        assert source.plane_wave_to_grid.magnitude.shape == (25, 9)
        assert source.transported_finite_difference.magnitude.shape == (9, 9)
        assert source.operator_difference.magnitude.shape == (9, 9)
        assert not source.plane_wave_to_grid.magnitude.flags.writeable
        assert not source.transported_finite_difference.magnitude.flags.writeable
        assert not source.operator_difference.magnitude.flags.writeable
        assert source.isometry_frobenius_defect.magnitude >= 0.0
        assert source.operator_frobenius_error.magnitude >= 0.0
        assert source.operator_maximum_absolute_error.magnitude >= 0.0

    def test_construction__forged_transport__raises_value_error(self) -> None:
        """A self-consistent forged difference cannot hide an incorrect transport."""
        source = self.result()
        forged_transport = source.transported_finite_difference.magnitude.copy()
        forged_transport[0, 0] += 1.0
        forged_difference = forged_transport - source.request.plane_wave.matrix

        # Recompute downstream fields from the forged transport so rejection isolates
        # T^dagger H_fd T correlation rather than the later subtraction or norms.
        with pytest.raises(ValueError, match="must equal plane_wave_to_grid"):
            Periodic2DCommonSpaceComparisonResult(
                request=source.request,
                plane_wave_to_grid=source.plane_wave_to_grid,
                transported_finite_difference=ComplexMatrixQuantity(
                    forged_transport, Unitless()
                ),
                operator_difference=ComplexMatrixQuantity(
                    forged_difference, Unitless()
                ),
                isometry_frobenius_defect=source.isometry_frobenius_defect,
                operator_frobenius_error=ScalarQuantity(
                    float(np.linalg.norm(forged_difference)), Unitless()
                ),
                operator_maximum_absolute_error=ScalarQuantity(
                    float(np.max(np.abs(forged_difference))), Unitless()
                ),
            )

    def test_construction__forged_difference__raises_value_error(self) -> None:
        """The signed difference must equal transported finite difference minus PW."""
        source = self.result()

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

    def test_construction__forged_isometry_defect__raises_value_error(self) -> None:
        """The isometry defect must be the Frobenius norm of retained T^dagger T-I."""
        source = self.result()

        with pytest.raises(ValueError, match="must match plane_wave_to_grid"):
            Periodic2DCommonSpaceComparisonResult(
                request=source.request,
                plane_wave_to_grid=source.plane_wave_to_grid,
                transported_finite_difference=source.transported_finite_difference,
                operator_difference=source.operator_difference,
                isometry_frobenius_defect=ScalarQuantity(
                    source.isometry_frobenius_defect.magnitude + 1.0,
                    Unitless(),
                ),
                operator_frobenius_error=source.operator_frobenius_error,
                operator_maximum_absolute_error=(
                    source.operator_maximum_absolute_error
                ),
            )

    def test_construction__forged_operator_norms__raise_value_error(self) -> None:
        """Both retained difference norms must remain correlated to the same matrix."""
        source = self.result()

        with pytest.raises(ValueError, match="operator_frobenius_error"):
            Periodic2DCommonSpaceComparisonResult(
                request=source.request,
                plane_wave_to_grid=source.plane_wave_to_grid,
                transported_finite_difference=source.transported_finite_difference,
                operator_difference=source.operator_difference,
                isometry_frobenius_defect=source.isometry_frobenius_defect,
                operator_frobenius_error=ScalarQuantity(
                    source.operator_frobenius_error.magnitude + 1.0,
                    Unitless(),
                ),
                operator_maximum_absolute_error=(
                    source.operator_maximum_absolute_error
                ),
            )
        with pytest.raises(ValueError, match="operator_maximum_absolute_error"):
            Periodic2DCommonSpaceComparisonResult(
                request=source.request,
                plane_wave_to_grid=source.plane_wave_to_grid,
                transported_finite_difference=source.transported_finite_difference,
                operator_difference=source.operator_difference,
                isometry_frobenius_defect=source.isometry_frobenius_defect,
                operator_frobenius_error=source.operator_frobenius_error,
                operator_maximum_absolute_error=ScalarQuantity(
                    source.operator_maximum_absolute_error.magnitude + 1.0,
                    Unitless(),
                ),
            )
