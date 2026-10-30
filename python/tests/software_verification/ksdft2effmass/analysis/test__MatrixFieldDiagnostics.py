"""Software verification for rank-generic matrix-field diagnostics."""

from __future__ import annotations

import math

import numpy as np
import pytest
from projectkoios.numerics.finite_periodic.meshes import CenteredUniformMesh
from projectkoios.numerics.finite_periodic.numpy.matrix_series import (
    NumpyFiniteFourierMatrixSeries,
)
from projectkoios.physkit.solidstate.tb import FinitePeriodicMatrixFourierSeries
from projectkoios.physkit.units import Unitless

from ksdft2effmass.analysis.matrix_field.diagnostics import (
    FourierMatrixBlockNormInventoryAnalyzer1D,
    MatrixErrorDecompositionAnalyzer,
    MatrixFieldComparisonAnalyzer,
    MatrixFieldErrorAnalyzer,
    MatrixFieldHermiticityAnalyzer,
    MatrixFieldIsometryAnalyzer,
    MatrixProjectorFieldAnalyzer,
    ScalarRefinementAnalyzer,
    SymmetricRangeTailAnalyzer1D,
    SymmetricRangeTailMonotonicityAnalyzer1D,
)

pytestmark = pytest.mark.software_verification


class TestMatrixFieldDiagnostics:
    """Establish typed rank-generic errors, bounds, decomposition, and tails."""

    @staticmethod
    def diagonal_field(values: tuple[tuple[float, ...], ...]) -> np.ndarray:
        """Return exact complex128 diagonal matrices for concise test inputs."""
        return np.asarray(
            [np.diag(np.asarray(row, dtype=np.complex128)) for row in values],
            dtype=np.complex128,
        )

    @staticmethod
    def series() -> FinitePeriodicMatrixFourierSeries:
        """Return one unit-aware inversion-complete rank-three matrix series."""
        modes = np.arange(-2, 3, dtype=np.int64).reshape((-1, 1))
        desired_norms = np.asarray((1.0, 2.0, 3.0, 2.0, 1.0))
        identity = np.eye(3, dtype=np.complex128)
        coefficients = np.asarray(
            [value * identity / math.sqrt(3.0) for value in desired_norms],
            dtype=np.complex128,
        )
        return FinitePeriodicMatrixFourierSeries.from_arrays(
            source_mesh=CenteredUniformMesh(1, 5, (0.0,)),
            integer_modes=modes,
            matrix_coefficients=coefficients,
            energy_unit=Unitless(),
            energy_reference="synthetic-zero",
            basis_identifier="rank-three-test-basis",
        )

    def test_error_summary__retains_raw_and_rank_normalized_channels(self) -> None:
        """Raw pointwise norms and rank-normalized forms remain distinguishable."""
        reference = self.diagonal_field(((0.0, 0.0, 0.0), (0.0, 0.0, 0.0)))
        approximation = self.diagonal_field(((2.0, 0.0, 0.0), (0.0, 0.0, 0.0)))

        result = MatrixFieldErrorAnalyzer(
            approximation=approximation,
            reference=reference,
            energy_reference=2.0,
        ).result()

        assert result.rank == 3
        assert result.matrix_frobenius_maximum == 2.0
        assert result.matrix_frobenius_rms == pytest.approx(math.sqrt(2.0))
        assert result.normalized_matrix_frobenius_maximum == pytest.approx(
            1.0 / math.sqrt(3.0)
        )
        assert result.ordered_spectrum_maximum == 2.0
        assert result.ordered_spectrum_l2_rms == pytest.approx(math.sqrt(2.0))
        assert result.normalized_ordered_spectrum_maximum == 1.0
        assert result.normalized_ordered_spectrum_l2_rms == pytest.approx(
            1.0 / math.sqrt(6.0)
        )

    def test_comparison__checks_weyl_and_norm_bounds_with_qualified_ratios(
        self,
    ) -> None:
        """Perturbation ratios are present only above the declared denominator floor."""
        reference = self.diagonal_field(((0.0, 0.0, 0.0), (0.0, 0.0, 0.0)))
        approximation = reference.copy()
        approximation[0, 0, 1] = 1.0
        approximation[0, 1, 0] = 1.0

        result = MatrixFieldComparisonAnalyzer(
            approximation=approximation,
            reference=reference,
            energy_reference=1.0,
            saturation_denominator_floor=1.0e-30,
        ).execute()
        bounds = result.perturbation_bounds

        assert bounds.maximum_ordered_spectrum_minus_spectral_norm == pytest.approx(
            0.0,
            abs=2.0e-15,
        )
        assert bounds.maximum_ordered_spectrum_minus_frobenius_norm == 0.0
        assert bounds.maximum_spectral_norm_minus_frobenius_norm == 0.0
        assert bounds.band_over_spectral_eligible_count == 1
        assert bounds.band_over_frobenius_eligible_count == 1
        assert bounds.maximum_band_over_spectral_ratio == pytest.approx(1.0)
        assert bounds.maximum_band_over_frobenius_ratio == pytest.approx(
            1.0 / math.sqrt(2.0)
        )

        zero = (
            MatrixFieldComparisonAnalyzer(
                approximation=reference,
                reference=reference,
                energy_reference=1.0,
                saturation_denominator_floor=1.0e-30,
            )
            .execute()
            .perturbation_bounds
        )
        assert zero.band_over_spectral_eligible_count == 0
        assert zero.maximum_band_over_spectral_ratio is None
        assert zero.band_over_frobenius_eligible_count == 0
        assert zero.maximum_band_over_frobenius_ratio is None

    def test_structure__separates_hermiticity_isometry_and_projector_defects(
        self,
    ) -> None:
        """Structural identities retain separate raw and normalized diagnostics."""
        frame = np.zeros((2, 6, 3), dtype=np.complex128)
        frame[:, :3, :] = np.eye(3, dtype=np.complex128)
        isometry = MatrixFieldIsometryAnalyzer().execute(frame)
        assert isometry.ambient_dimension == 6
        assert isometry.rank == 3
        assert isometry.maximum_frobenius_defect == 0.0

        projectors = frame @ np.swapaxes(frame.conjugate(), -1, -2)
        projector = MatrixProjectorFieldAnalyzer().execute(projectors)
        assert projector.dimension == 6
        assert projector.maximum_hermiticity_frobenius_defect == 0.0
        assert projector.maximum_idempotency_frobenius_defect == 0.0

        matrices = self.diagonal_field(((1.0, 2.0, 3.0),))
        hermiticity = MatrixFieldHermiticityAnalyzer().execute(
            matrices,
            energy_reference=2.0,
        )
        assert hermiticity.maximum_frobenius_defect == 0.0
        attacked = matrices.copy()
        attacked[0, 0, 1] = 1.0j
        nonhermitian = MatrixFieldHermiticityAnalyzer().execute(
            attacked,
            energy_reference=2.0,
        )
        assert nonhermitian.maximum_frobenius_defect == pytest.approx(math.sqrt(2.0))
        assert nonhermitian.normalized_maximum_frobenius_defect == pytest.approx(
            math.sqrt(2.0) / (2.0 * math.sqrt(3.0))
        )

    def test_decomposition__measures_exact_matrix_identity_defect(self) -> None:
        """The total channel is checked as a matrix identity, not a norm sum."""
        interpolation = self.diagonal_field(((1.0, 0.0, 0.0),))
        truncation = self.diagonal_field(((-0.25, 0.0, 0.0),))
        total = interpolation + truncation

        exact = MatrixErrorDecompositionAnalyzer(
            interpolation_error=interpolation,
            truncation_error=truncation,
            total_error=total,
            energy_reference=2.0,
        ).execute()
        assert exact.maximum_frobenius_defect == 0.0
        assert exact.normalized_maximum_frobenius_defect == 0.0

        perturbed = total.copy()
        perturbed[0, 1, 1] += 1.0e-3
        observed = MatrixErrorDecompositionAnalyzer(
            interpolation_error=interpolation,
            truncation_error=truncation,
            total_error=perturbed,
            energy_reference=2.0,
        ).execute()
        assert observed.maximum_frobenius_defect == pytest.approx(1.0e-3)
        assert observed.normalized_maximum_frobenius_defect == pytest.approx(
            1.0e-3 / (2.0 * math.sqrt(3.0))
        )

    def test_symmetric_tail__retains_explicit_support_and_w_n_l(self) -> None:
        """One owner matrix series yields explicit raw and normalized tail measures."""
        analyzer = SymmetricRangeTailAnalyzer1D()
        series = self.series()
        support_zero = analyzer.execute(series, 0, energy_reference=2.0)
        support_one = analyzer.execute(series, 1, energy_reference=2.0)
        support_two = analyzer.execute(series, 2, energy_reference=2.0)

        assert support_zero.retained_translations == (0,)
        assert support_zero.omitted_translations == (-2, -1, 1, 2)
        assert support_zero.omitted_squared_frobenius_weight == pytest.approx(10.0)
        assert support_zero.omitted_frobenius_l2_norm == pytest.approx(math.sqrt(10.0))
        assert support_zero.omitted_block_l1_norm == pytest.approx(6.0)
        assert support_zero.normalized_omitted_squared_frobenius_weight == (
            pytest.approx(10.0 / 12.0)
        )
        assert support_one.omitted_squared_frobenius_weight == pytest.approx(2.0)
        assert support_two.omitted_squared_frobenius_weight == 0.0

        monotonicity = SymmetricRangeTailMonotonicityAnalyzer1D().execute(
            (support_zero, support_one, support_two),
            tolerance=2.0e-11,
        )
        assert len(monotonicity) == 2
        assert all(item.passes for item in monotonicity)
        assert all(
            item.normalized_squared_weight_increase == 0.0 for item in monotonicity
        )

    def test_block_inventory_and_refinement__retain_exact_derived_values(self) -> None:
        """Bounded block norms and absolute-relative refinement remain explicit."""
        inventory = FourierMatrixBlockNormInventoryAnalyzer1D().execute(
            self.series(),
            maximum_range=1,
            energy_reference=2.0,
        )
        assert tuple(block.translation for block in inventory.blocks) == (-1, 0, 1)
        assert tuple(block.raw_frobenius_norm for block in inventory.blocks) == (
            pytest.approx(2.0),
            pytest.approx(3.0),
            pytest.approx(2.0),
        )
        assert inventory.blocks[1].normalized_frobenius_norm == pytest.approx(
            3.0 / (2.0 * math.sqrt(3.0))
        )

        stable = ScalarRefinementAnalyzer().execute(
            coarse_mesh_size=1025,
            fine_mesh_size=2049,
            coarse_value=1.0e-5,
            fine_value=1.0e-5 + 5.0e-11,
            denominator_floor=1.0e-30,
            absolute_tolerance=1.0e-10,
            relative_tolerance=1.0e-6,
        )
        assert stable.absolute_change == pytest.approx(5.0e-11)
        assert stable.relative_change == pytest.approx(5.0e-6, rel=1.0e-5)
        assert stable.applied_tolerance == pytest.approx(1.1e-10)
        assert stable.signed_margin > 0.0
        assert stable.passes

        unresolved = ScalarRefinementAnalyzer().execute(
            coarse_mesh_size=1025,
            fine_mesh_size=2049,
            coarse_value=1.0e-5,
            fine_value=1.1e-5,
            denominator_floor=1.0e-30,
            absolute_tolerance=1.0e-10,
            relative_tolerance=1.0e-6,
        )
        assert unresolved.signed_margin < 0.0
        assert not unresolved.passes

    def test_public_numeric_boundaries__reject_ambiguous_values(self) -> None:
        """Ambiguous scalars, arrays, and duplicate mode inventories fail."""
        field = self.diagonal_field(((0.0, 0.0, 0.0),))
        with pytest.raises(TypeError, match="energy_reference"):
            MatrixFieldErrorAnalyzer(
                approximation=field,
                reference=field,
                energy_reference=True,  # type: ignore[arg-type]
            )
        with pytest.raises(TypeError, match="energy_reference"):
            MatrixFieldErrorAnalyzer(
                approximation=field,
                reference=field,
                energy_reference="1.0",  # type: ignore[arg-type]
            )
        with pytest.raises(TypeError, match="complex128"):
            MatrixFieldErrorAnalyzer(
                approximation=field.real,  # type: ignore[arg-type]
                reference=field.real,  # type: ignore[arg-type]
                energy_reference=1.0,
            )
        nonfinite = field.copy()
        nonfinite[0, 0, 0] = np.nan
        with pytest.raises(ValueError, match="finite"):
            MatrixFieldErrorAnalyzer(
                approximation=nonfinite,
                reference=field,
                energy_reference=1.0,
            )

        modes = np.asarray(((0,), (0,)), dtype=np.int64)
        coefficients = np.zeros((2, 2, 2), dtype=np.complex128)
        unit_free_series = NumpyFiniteFourierMatrixSeries.from_arrays(
            1,
            modes,
            coefficients,
        )
        with pytest.raises(TypeError, match="FinitePeriodicMatrixFourierSeries"):
            SymmetricRangeTailAnalyzer1D().execute(
                unit_free_series,  # type: ignore[arg-type]
                0,
                energy_reference=1.0,
            )
