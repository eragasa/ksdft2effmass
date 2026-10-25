"""Software verification of immutable PIAB1D visualization artifacts."""

from __future__ import annotations

import hashlib
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
import pytest
from projectkoios.physkit.units import (
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.analysis import (
    RelativeErrorConvergenceResult,
    TailProbabilitySelection,
)
from ksdft2effmass.analysis.operators import KineticPotentialDecompositionAnalyzer
from ksdft2effmass.model_systems import (
    BaseModelAnalysisVisualization,
    BaseModelAnalysisVisualizer,
)
from ksdft2effmass.model_systems.piab1d import (
    Piab1dGridSweepAnalyzer,
    Piab1dGridSweepDefinition,
    Piab1dVerification,
    Piab1dVisualization,
    Piab1dVisualizationData,
    Piab1dVisualizationPlotEnum,
    Piab1dVisualizer,
)
from ksdft2effmass.verification import VerificationObservation

pytestmark = pytest.mark.software_verification
SUT = Piab1dVisualization


class TestPiab1dVisualization:
    """Own the immutable PNG and plot-enum boundary."""

    def test_init__png_and_plot__retains_stable_filename(self) -> None:
        figure, axis = plt.subplots()
        axis.plot([0.0, 1.0], [0.0, 1.0])
        buffer = BytesIO()
        figure.savefig(buffer, format="png")
        plt.close(figure)
        png = buffer.getvalue()

        visualization = SUT(
            plot=Piab1dVisualizationPlotEnum.spectrum_and_states,
            png=png,
        )

        assert isinstance(visualization, BaseModelAnalysisVisualization)
        assert issubclass(Piab1dVisualizer, BaseModelAnalysisVisualizer)
        assert visualization.png is png
        assert visualization.filename == "spectrum-and-states.png"
        assert visualization.media_type == "image/png"

    def test_init__non_png_bytes__rejects_value(self) -> None:
        with pytest.raises(ValueError, match="decodable PNG image"):
            SUT(
                plot=Piab1dVisualizationPlotEnum.residual_matrices,
                png=b"not-png",
            )

    def test_visualizer__different_verified_digest__rejects_typed_immutable_data(
        self,
    ) -> None:
        grid_sweep = Piab1dGridSweepAnalyzer().execute(
            Piab1dGridSweepDefinition(
                length=1.0,
                mass=1.0,
                interior_points=(3, 4),
                retained_dimension=3,
                fixed_modes=(3,),
            )
        )
        data = Piab1dVisualizationData(
            length=ScalarQuantity(1.0, Unitless()),
            retained_dimension=3,
            computed_energies=VectorQuantity(np.asarray([1.0, 2.0, 3.0]), Unitless()),
            continuum_energies=VectorQuantity(np.asarray([1.0, 2.0, 3.0]), Unitless()),
            eigenvectors=MatrixQuantity(np.eye(3), Unitless()),
            quadrature_eigenvectors=MatrixQuantity(np.eye(3), Unitless()),
            consistent=MatrixQuantity(np.zeros((3, 3)), Unitless()),
            unmatched=MatrixQuantity(np.eye(3), Unitless()),
            boundary=MatrixQuantity(np.eye(3), Unitless()),
            continuum_coordinates=VectorQuantity(np.asarray([0.0, 1.0]), Unitless()),
            continuum_wavefunctions=MatrixQuantity(np.zeros((2, 3)), Unitless()),
            selection=TailProbabilitySelection(
                probabilities=VectorQuantity(np.asarray([0.8, 0.19, 0.01]), Unitless()),
                omitted_probabilities=VectorQuantity(
                    np.asarray([0.2, 0.01, 0.0]), Unitless()
                ),
                tolerance=0.01,
                selected_count=2,
            ),
            convergence_interior_points=(8, 9, 10),
            convergence_modes=(1,),
            eigenpair_sweep=grid_sweep.eigenpairs,
            residual_norm_sweep=grid_sweep.residual_norms,
            finite_algebraic_diagnostics=grid_sweep.finite_algebraic_diagnostics,
            kinetic_potential_decomposition=KineticPotentialDecompositionAnalyzer().execute(
                MatrixQuantity(np.diag([1.0, 2.0, 3.0]), Unitless()),
                MatrixQuantity(
                    np.asarray(
                        [
                            [0.5, 1.0, 0.4],
                            [1.0, -0.25, -0.75],
                            [0.4, -0.75, 0.75],
                        ]
                    ),
                    Unitless(),
                ),
            ),
            convergence=RelativeErrorConvergenceResult(
                spacings=VectorQuantity(
                    np.asarray([1.0 / 9.0, 0.1, 1.0 / 11.0]), Unitless()
                ),
                relative_errors=MatrixQuantity(
                    np.asarray([[(1.0 / 9.0) ** 2], [0.1**2], [(1.0 / 11.0) ** 2]]),
                    Unitless(),
                ),
                order_columns=(0,),
                observed_orders=MatrixQuantity(np.asarray([[2.0], [2.0]]), Unitless()),
            ),
        )
        verification = Piab1dVerification(
            subject_sha256="b" * 64,
            visualization_data_sha256="c" * 64,
            components=tuple(
                component_type(
                    {
                        f"test_observation_{index}": VerificationObservation(
                            value=ScalarQuantity(0.0, Unitless()),
                            tolerance=ScalarQuantity(0.0, Unitless()),
                        )
                    }
                )
                for index, component_type in enumerate(
                    Piab1dVerification.component_types.values()
                )
            ),
        )

        with pytest.raises(ValueError, match="digests differ"):
            Piab1dVisualizer(data=data, verification=verification)
        with pytest.raises(ValueError, match="read-only"):
            data.computed_energies.magnitude[0] = 0.0
        restored = Piab1dVisualizationData.from_json(data.to_json())
        assert (
            hashlib.sha256(restored.to_json()).hexdigest()
            == hashlib.sha256(data.to_json()).hexdigest()
        )

    def test_plot_enum__complete_migration_target__uses_lower_snake_case(self) -> None:
        assert {plot.name for plot in Piab1dVisualizationPlotEnum} == {
            "spectrum_and_states",
            "residual_matrices",
            "continuum_wavefunction_ladder",
            "discrete_wavefunction_ladder",
            "retained_dimension_selection",
            "convergence_series",
            "convergence_mode_sweep",
            "higher_eigenpair_sweep",
            "higher_mode_convergence",
            "operator_residual_norms",
            "eigensolver_residual_norms",
            "finite_algebraic_diagnostics",
            "kinetic_potential_decomposition",
        }
