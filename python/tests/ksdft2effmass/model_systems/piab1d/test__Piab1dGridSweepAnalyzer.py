"""Software verification of typed PIAB1D represented-grid sweeps."""

from __future__ import annotations

from dataclasses import replace

import numpy as np
import pytest
from projectkoios.physkit.units import (
    MatrixQuantity,
    PhysicalUnit,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.model_systems.piab1d.analysis.grid_sweep import (
    Piab1dEigenpairSweepResult,
    Piab1dGridSweepAnalysis,
    Piab1dGridSweepAnalyzer,
    Piab1dGridSweepDefinition,
)
from ksdft2effmass.model_systems.piab1d.analysis.verification import (
    Piab1dEigenpairSweepReferenceAnalyzer,
)

pytestmark = pytest.mark.software_verification


class TestPiab1dGridSweepAnalyzer:
    """Establish full-spectrum sweep construction and representation boundaries."""

    def test_execute__two_grids__retains_each_eigenpair_once(self) -> None:
        definition = Piab1dGridSweepDefinition(
            length=1.0,
            mass=1.0,
            interior_points=(8, 9),
            retained_dimension=3,
            fixed_modes=(8,),
        )

        analyzer = Piab1dGridSweepAnalyzer(definition)
        analysis = analyzer.execute()
        result = analysis.eigenpairs

        assert analyzer.request is definition
        assert result.grid_offsets == (0, 8, 17)
        assert result.mode_numbers == (*range(1, 9), *range(1, 10))
        np.testing.assert_allclose(result.spacings.magnitude, (1.0 / 9.0, 0.1))
        assert result.relative_energy_errors.magnitude.shape == (17,)
        assert np.max(result.nodal_overlap_defects.magnitude) < 1.0e-14
        assert np.max(result.scaled_eigenpair_residuals.magnitude) < 1.0e-14
        convergence = result.fixed_mode_convergence(8)
        assert convergence.relative_errors.magnitude.shape == (2, 1)
        assert convergence.observed_orders.magnitude.shape == (1, 1)
        reference = Piab1dEigenpairSweepReferenceAnalyzer().execute(result)
        assert all(
            comparison.result().passed for comparison in reference.comparisons.values()
        )
        assert analysis.residual_norms.hamiltonian.magnitude.shape == (2, 3)
        assert np.all(analysis.residual_norms.consistent.magnitude == 0.0)
        assert np.all(analysis.residual_norms.boundary_relative.magnitude > 0.0)
        assert (
            analysis.finite_algebraic_diagnostics.discrete_spectrum.magnitude.shape
            == (2,)
        )
        reconstructed_analysis = Piab1dGridSweepAnalysis.from_json(analysis.to_json())
        assert reconstructed_analysis.eigenpairs.grid_offsets == (0, 8, 17)
        reconstructed = Piab1dEigenpairSweepResult.from_json(result.to_json())
        np.testing.assert_array_equal(
            reconstructed.relative_energy_errors.magnitude,
            result.relative_energy_errors.magnitude,
        )

    def test_init__nonincreasing_modes__rejects_definition(self) -> None:
        with pytest.raises(ValueError, match="strictly increasing"):
            Piab1dGridSweepDefinition(
                length=1.0,
                mass=1.0,
                interior_points=(8, 9),
                retained_dimension=3,
                fixed_modes=(2, 1),
            )

    def test_init__spacing_unit__rejects_dimensioned_grid_spacing(self) -> None:
        definition = Piab1dGridSweepDefinition(
            length=1.0,
            mass=1.0,
            interior_points=(8, 9),
            retained_dimension=3,
            fixed_modes=(1,),
        )
        result = Piab1dGridSweepAnalyzer(definition).execute().eigenpairs

        with pytest.raises(ValueError, match="nondimensional unit"):
            replace(
                result,
                spacings=VectorQuantity(
                    result.spacings.magnitude,
                    PhysicalUnit("meter"),
                ),
            )

    def test_init__spacing_values__rejects_different_grid_definition(self) -> None:
        definition = Piab1dGridSweepDefinition(
            length=1.0,
            mass=1.0,
            interior_points=(8, 9),
            retained_dimension=3,
            fixed_modes=(1,),
        )
        result = Piab1dGridSweepAnalyzer(definition).execute().eigenpairs

        with pytest.raises(ValueError, match="declared represented grids"):
            replace(
                result,
                spacings=VectorQuantity(np.asarray([0.2, 0.1]), Unitless()),
            )

    def test_init__residual_shape__rejects_incomplete_norm_inventory(self) -> None:
        definition = Piab1dGridSweepDefinition(
            length=1.0,
            mass=1.0,
            interior_points=(8, 9),
            retained_dimension=3,
            fixed_modes=(1,),
        )
        result = Piab1dGridSweepAnalyzer(definition).execute().residual_norms

        with pytest.raises(ValueError, match="cover every grid and norm"):
            replace(
                result,
                consistent=MatrixQuantity(np.zeros((2, 2)), Unitless()),
            )

    def test_init__diagnostic_unit__rejects_dimensioned_observation(self) -> None:
        definition = Piab1dGridSweepDefinition(
            length=1.0,
            mass=1.0,
            interior_points=(8, 9),
            retained_dimension=3,
            fixed_modes=(1,),
        )
        result = (
            Piab1dGridSweepAnalyzer(definition).execute().finite_algebraic_diagnostics
        )

        with pytest.raises(ValueError, match="nondimensional unit"):
            replace(
                result,
                spectral_leakage=VectorQuantity(
                    result.spectral_leakage.magnitude,
                    PhysicalUnit("joule"),
                ),
            )

    def test_init__cross_section_grid__rejects_different_definition(self) -> None:
        definition = Piab1dGridSweepDefinition(
            length=1.0,
            mass=1.0,
            interior_points=(8, 9),
            retained_dimension=3,
            fixed_modes=(1,),
        )
        analysis = Piab1dGridSweepAnalyzer(definition).execute()
        other_definition = Piab1dGridSweepDefinition(
            length=2.0,
            mass=1.0,
            interior_points=(8, 9),
            retained_dimension=3,
            fixed_modes=(1,),
        )
        mismatched_residuals = replace(
            analysis.residual_norms,
            definition=other_definition,
        )

        with pytest.raises(ValueError, match="share one definition"):
            Piab1dGridSweepAnalysis(
                eigenpairs=analysis.eigenpairs,
                residual_norms=mismatched_residuals,
                finite_algebraic_diagnostics=analysis.finite_algebraic_diagnostics,
            )

    def test_init__nonincreasing_grids__rejects_definition(self) -> None:
        with pytest.raises(ValueError, match="strictly increasing"):
            Piab1dGridSweepDefinition(
                length=1.0,
                mass=1.0,
                interior_points=(8, 8),
                retained_dimension=3,
                fixed_modes=(1,),
            )
