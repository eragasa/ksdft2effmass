"""Experiment composition for periodic one-dimensional single-band reduction."""

from __future__ import annotations

import numpy as np
from ksdft2effmass.analysis.periodic_bands import (
    BandGapAnalyzer1D,
    BandSpectrumSamples1D,
    ContiguousBandSelection,
)
from ksdft2effmass.analysis.single_band_reduction import (
    SingleBandHoppingReductionRequest1D,
    SingleBandHoppingReductionWorkflow1D,
)
from ksdft2effmass.model_systems import (
    PeriodicFiniteDifferenceFiberHamiltonian1DConstructor,
    PeriodicUniformGrid1D,
    PlaneWaveFiberHamiltonian1DConstructor,
)
from ksdft2effmass.solidstate import (
    CenteredUniformReciprocalMesh1D,
    PlaneWaveBasis1D,
)
from projectkoios.physkit.units import (
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from scipy.sparse.linalg import eigsh  # type: ignore[import-untyped]

from .definition import SingleBandFourierReductionExperimentDefinition
from .results import (
    FiniteDifferenceRefinementObservation,
    PlaneWaveRefinementObservation,
    SingleBandFourierReductionExperimentResult,
)


class SingleBandFourierReductionExperiment:
    """Compose one model-specific experiment from reusable scientific Actions.

    This Action owns the selected finite Fourier parent, represented-reference sweeps,
    retained-band selection, disjoint sample roles, and experiment controls. The
    complete transform and finite-range route calculations are delegated to
    :class:`SingleBandHoppingReductionWorkflow1D`.

    It performs deterministic in-process numerical work only. It does not read or
    write evidence, execute an external calculator, choose an adequate hopping range,
    or promote a positive sampled gap to a continuum isolation claim.
    """

    __slots__ = ()

    def execute(
        self, definition: SingleBandFourierReductionExperimentDefinition
    ) -> SingleBandFourierReductionExperimentResult:
        """Calculate parent refinement, sampled gaps, and single-band reduction."""
        if type(definition) is not SingleBandFourierReductionExperimentDefinition:
            raise TypeError(
                "definition must be SingleBandFourierReductionExperimentDefinition"
            )
        parent_coordinates = self._physical_coordinates(
            definition,
            np.asarray(
                definition.parent_sample_reduced_momenta,
                dtype=np.float64,
            ),
        )
        parent_reference = self._plane_wave_spectrum(
            definition,
            definition.plane_wave_reference_cutoff,
            parent_coordinates,
            definition.compared_band_count,
        )
        plane_wave_refinement = tuple(
            PlaneWaveRefinementObservation(
                cutoff,
                self._maximum_spectrum_error(
                    self._plane_wave_spectrum(
                        definition,
                        cutoff,
                        parent_coordinates,
                        definition.compared_band_count,
                    ),
                    parent_reference,
                ),
            )
            for cutoff in definition.plane_wave_cutoffs
        )
        finite_difference_refinement = tuple(
            FiniteDifferenceRefinementObservation(
                point_count,
                self._maximum_spectrum_error(
                    self._finite_difference_spectrum(
                        definition,
                        point_count,
                        parent_coordinates,
                        definition.compared_band_count,
                    ),
                    parent_reference,
                ),
            )
            for point_count in definition.finite_difference_points
        )

        training_mesh = CenteredUniformReciprocalMesh1D(
            definition.parent_model.reciprocal_vector,
            definition.reciprocal_training_mesh_size,
        )
        retained_band_count = definition.selected_band_index + 2
        training_spectrum = self._plane_wave_spectrum(
            definition,
            definition.production_plane_wave_cutoff,
            training_mesh.coordinates,
            retained_band_count,
        )
        evaluation_spectrum = self._plane_wave_spectrum(
            definition,
            definition.production_plane_wave_cutoff,
            definition.evaluation_coordinates,
            retained_band_count,
        )
        selection = ContiguousBandSelection(
            definition.selected_band_index,
            definition.selected_band_index,
        )
        gap_analyzer = BandGapAnalyzer1D()
        training_gap = gap_analyzer.execute(training_spectrum, selection)
        evaluation_gap = gap_analyzer.execute(evaluation_spectrum, selection)
        training_target = self._selected_band(training_spectrum, selection.lower_index)
        evaluation_target = self._selected_band(
            evaluation_spectrum, selection.lower_index
        )
        reduction_request = SingleBandHoppingReductionRequest1D(
            training_target=training_target,
            evaluation_target=evaluation_target,
            transform_mesh=training_mesh,
            hopping_ranges=definition.hopping_ranges,
            fitting_weights=VectorQuantity(
                np.asarray(definition.fitting_weights, dtype=np.float64),
                Unitless(),
            ),
            tolerances=definition.tolerances,
        )
        reduction = SingleBandHoppingReductionWorkflow1D().execute(reduction_request)
        return SingleBandFourierReductionExperimentResult(
            definition,
            parent_reference,
            plane_wave_refinement,
            finite_difference_refinement,
            training_gap,
            evaluation_gap,
            reduction,
        )

    @staticmethod
    def _selected_band(
        spectrum: BandSpectrumSamples1D, index: int
    ) -> BandSpectrumSamples1D:
        """Select one already identified band without changing sample roles."""
        if type(spectrum) is not BandSpectrumSamples1D:
            raise TypeError("spectrum must be BandSpectrumSamples1D")
        if type(index) is not int:
            raise TypeError("index must be a built-in int")
        if index < 0 or index >= spectrum.band_count:
            raise ValueError("index must select one represented band")
        return BandSpectrumSamples1D(
            spectrum.coordinates,
            spectrum.reciprocal_period,
            MatrixQuantity(
                spectrum.eigenvalues.magnitude[:, index : index + 1],
                spectrum.eigenvalues.unit,
            ),
        )

    @staticmethod
    def _plane_wave_spectrum(
        definition: SingleBandFourierReductionExperimentDefinition,
        cutoff: int,
        coordinates: VectorQuantity,
        band_count: int,
    ) -> BandSpectrumSamples1D:
        """Diagonalize the finite plane-wave parent at supplied coordinates."""
        model = definition.parent_model
        reduced = coordinates.magnitude / model.reciprocal_vector.magnitude
        basis = PlaneWaveBasis1D(model.reciprocal_vector, cutoff)
        constructor = PlaneWaveFiberHamiltonian1DConstructor()
        values = np.asarray(
            [
                np.linalg.eigvalsh(
                    constructor.execute(
                        float(momentum),
                        basis,
                        model.potential,
                        model.recoil_energy,
                        model.duality_absolute_tolerance,
                    ).represented_matrix.magnitude
                )[:band_count]
                for momentum in reduced
            ],
            dtype=np.float64,
        )
        return BandSpectrumSamples1D(
            coordinates,
            model.reciprocal_vector,
            MatrixQuantity(values, model.recoil_energy.unit),
        )

    @staticmethod
    def _finite_difference_spectrum(
        definition: SingleBandFourierReductionExperimentDefinition,
        point_count: int,
        coordinates: VectorQuantity,
        band_count: int,
    ) -> BandSpectrumSamples1D:
        """Diagonalize the centered periodic finite-difference parent."""
        model = definition.parent_model
        grid = PeriodicUniformGrid1D(
            ScalarQuantity(0.0, model.potential.period.unit),
            model.potential.period,
            point_count,
        )
        constructor = PeriodicFiniteDifferenceFiberHamiltonian1DConstructor()
        reduced = coordinates.magnitude / model.reciprocal_vector.magnitude
        values: list[np.ndarray] = []
        for momentum in reduced:
            matrix = constructor.execute(
                float(momentum),
                grid,
                model.potential,
                model.recoil_energy,
                model.duality_absolute_tolerance,
            ).represented_matrix.to_csr()
            eigenvalues = eigsh(
                matrix,
                k=band_count,
                which="SA",
                return_eigenvectors=False,
                v0=np.full(
                    point_count,
                    1.0 / np.sqrt(float(point_count)),
                    dtype=np.float64,
                ),
            )
            values.append(np.sort(np.asarray(eigenvalues, dtype=np.float64)))
        return BandSpectrumSamples1D(
            coordinates,
            model.reciprocal_vector,
            MatrixQuantity(np.asarray(values), model.recoil_energy.unit),
        )

    @staticmethod
    def _physical_coordinates(
        definition: SingleBandFourierReductionExperimentDefinition,
        reduced: np.ndarray,
    ) -> VectorQuantity:
        """Convert reduced momenta to the parent reciprocal-coordinate unit."""
        if type(reduced) is not np.ndarray or reduced.dtype != np.float64:
            raise TypeError("reduced must be a float64 numpy.ndarray")
        reciprocal = definition.parent_model.reciprocal_vector
        return VectorQuantity(reciprocal.magnitude * reduced, reciprocal.unit)

    @staticmethod
    def _maximum_spectrum_error(
        candidate: BandSpectrumSamples1D,
        reference: BandSpectrumSamples1D,
    ) -> ScalarQuantity:
        """Return one maximum absolute represented-spectrum discrepancy."""
        if candidate.eigenvalues.unit != reference.eigenvalues.unit:
            raise ValueError("candidate and reference energy units must agree")
        if candidate.eigenvalues.magnitude.shape != (
            reference.eigenvalues.magnitude.shape
        ):
            raise ValueError("candidate and reference spectrum shapes must agree")
        return ScalarQuantity(
            float(
                np.max(
                    np.abs(
                        candidate.eigenvalues.magnitude
                        - reference.eigenvalues.magnitude
                    )
                )
            ),
            reference.eigenvalues.unit,
        )


__all__ = ["SingleBandFourierReductionExperiment"]
