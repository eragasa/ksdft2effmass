"""Independent verification of decoded PIAB1D analysis results."""

from __future__ import annotations

from collections.abc import Mapping
from typing import ClassVar

from projectkoios.physkit.units import ScalarQuantity, Unitless

from ksdft2effmass.analysis import (
    DiagnosticVerification,
    EigensystemVerification,
    KineticPotentialDecompositionVerification,
    RelativeErrorConvergenceVerification,
    TailProbabilitySelectionVerification,
)
from ksdft2effmass.hamiltonian import (
    HamiltonianVerification,
    SpectralReductionVerification,
)
from ksdft2effmass.model_systems.analysis import BaseModelAnalysisVerifier
from ksdft2effmass.model_systems.verification import (
    QuadratureVerification,
    VisualizationProjectionVerification,
)
from ksdft2effmass.serialization import SerializableValue
from ksdft2effmass.verification import (
    CompositeVerification,
)

from ...result import Piab1dCalculationResult
from ...visualization import Piab1dVisualizationData
from .reference import Piab1dIndependentReferenceAnalyzer
from .values import Piab1dVerification


class Piab1dVerifier(
    BaseModelAnalysisVerifier[Piab1dVerification, Piab1dVisualizationData]
):
    """Independently verify one decoded successor PIAB1D result mapping."""

    __slots__ = ("_result", "_subject_sha256")

    verification_inventory: ClassVar[
        tuple[tuple[type[CompositeVerification], frozenset[str]], ...]
    ] = (
        (
            HamiltonianVerification,
            frozenset(
                {
                    "parent_hamiltonian_maximum_absolute_error",
                    "cyclic_reference_maximum_absolute_error",
                    "boundary_realization_maximum_absolute_error",
                }
            ),
        ),
        (
            EigensystemVerification,
            frozenset(
                {
                    "discrete_spectrum_maximum_absolute_error",
                    "reported_discrete_spectrum_maximum_absolute_error",
                    "continuum_spectrum_maximum_absolute_error",
                    "eigenpair_residual_maximum_norm",
                    "eigenvector_orthonormality_maximum_absolute_error",
                    "eigenpair_sweep_spacing_maximum_absolute_error",
                    "eigenpair_sweep_fractional_index_maximum_absolute_error",
                    "eigenpair_sweep_dispersion_maximum_absolute_error",
                    "eigenpair_sweep_nodal_overlap_defect_maximum",
                    "eigenpair_sweep_scaled_residual_maximum",
                }
            ),
        ),
        (
            SpectralReductionVerification,
            frozenset(
                {
                    "projector_maximum_absolute_error",
                    "reduced_hamiltonian_maximum_absolute_error",
                    "embedded_hamiltonian_maximum_absolute_error",
                    "retained_block_maximum_absolute_error",
                    "retained_to_discarded_block_maximum_absolute_error",
                    "discarded_to_retained_block_maximum_absolute_error",
                    "discarded_block_maximum_absolute_error",
                    "consistent_analysis_maximum_absolute_error",
                    "unmatched_analysis_maximum_absolute_error",
                    "discarded_analysis_maximum_absolute_error",
                }
            ),
        ),
        (
            QuadratureVerification,
            frozenset(
                {
                    "quadrature_spacing_absolute_error",
                    "quadrature_weight_maximum_absolute_error",
                    "quadrature_eigenvector_maximum_absolute_error",
                    "weighted_gram_maximum_absolute_error",
                    "weighted_orthonormality_maximum_absolute_error",
                    "weighted_projector_maximum_absolute_error",
                    "weighted_projector_equivalence_maximum_absolute_error",
                }
            ),
        ),
        (
            RelativeErrorConvergenceVerification,
            frozenset(
                {
                    "convergence_spacing_maximum_absolute_error",
                    "convergence_relative_error_maximum_absolute_error",
                    "convergence_order_maximum_absolute_error",
                }
            ),
        ),
        (
            TailProbabilitySelectionVerification,
            frozenset(
                {
                    "selection_probability_maximum_absolute_error",
                    "selection_omitted_probability_maximum_absolute_error",
                    "selection_identity_error",
                }
            ),
        ),
        (
            DiagnosticVerification,
            frozenset(
                {
                    "serialized_discrete_spectrum_maximum_absolute_error_maximum_absolute_error",
                    "serialized_scaled_eigenpair_residuals_maximum_absolute_error",
                    "serialized_spectral_reconstruction_error_maximum_absolute_error",
                    "serialized_projector_idempotency_error_maximum_absolute_error",
                    "serialized_weighted_gram_error_maximum_absolute_error",
                    "serialized_weighted_projector_error_maximum_absolute_error",
                    "residual_norm_hamiltonian_maximum_absolute_error",
                    "residual_norm_boundary_maximum_absolute_error",
                    "residual_norm_unmatched_maximum_absolute_error",
                    "residual_norm_consistent_maximum",
                    "residual_norm_eigensolver_relative_maximum",
                    "residual_norm_boundary_ratio_maximum_absolute_error",
                    "residual_norm_unmatched_ratio_maximum_absolute_error",
                    "residual_norm_eigensolver_ratio_maximum_absolute_error",
                    "finite_algebraic_discrete_spectrum_maximum",
                    "finite_algebraic_spectral_reconstruction_maximum",
                    "finite_algebraic_projector_idempotency_maximum",
                    "finite_algebraic_retained_coordinate_maximum",
                    "finite_algebraic_retained_embedding_maximum",
                    "finite_algebraic_spectral_leakage_maximum",
                }
            ),
        ),
        (
            KineticPotentialDecompositionVerification,
            frozenset(
                {
                    "decomposition_physical_kinetic_maximum_absolute_error",
                    "decomposition_physical_potential_maximum_absolute_error",
                    "decomposition_alternative_kinetic_maximum_absolute_error",
                    "decomposition_physical_reconstruction_error",
                    "decomposition_alternative_reconstruction_error",
                    "decomposition_model_fit_maximum_absolute_error",
                    "decomposition_model_residual_maximum_absolute_error",
                    "decomposition_model_norm_maximum_absolute_error",
                }
            ),
        ),
        (
            VisualizationProjectionVerification,
            frozenset(
                {
                    "visualization_length_absolute_error",
                    "visualization_retained_dimension_error",
                    "visualization_computed_energy_maximum_absolute_error",
                    "visualization_continuum_energy_maximum_absolute_error",
                    "visualization_eigenvector_maximum_absolute_error",
                    "visualization_quadrature_eigenvector_maximum_absolute_error",
                    "visualization_consistent_maximum_absolute_error",
                    "visualization_unmatched_maximum_absolute_error",
                    "visualization_boundary_maximum_absolute_error",
                    "visualization_probability_maximum_absolute_error",
                    "visualization_omitted_probability_maximum_absolute_error",
                    "visualization_selection_tolerance_absolute_error",
                    "visualization_selected_dimension_error",
                    "continuum_visualization_coordinate_maximum_absolute_error",
                    "continuum_visualization_wavefunction_maximum_absolute_error",
                }
            ),
        ),
    )

    def __init__(
        self,
        *,
        result: Mapping[str, SerializableValue],
        subject_sha256: str,
    ) -> None:
        """Bind a typed decoded result to its exact subject digest.

        Parameters
        ----------
        result
            Typed mapping decoded from the calculation-result JSON bytes.
        subject_sha256
            Lowercase SHA-256 digest of the exact result bytes under verification.

        Raises
        ------
        TypeError
            ``result`` is not a string-keyed mapping or a decoded field has the wrong
            domain type.
        ValueError
            The digest is malformed or the typed result violates a local or correlated
            invariant.

        Notes
        -----
        Construction imports no calculation script and executes no production
        analyzer. The digest binds later verification values to exact subject bytes.
        """
        if not isinstance(result, Mapping):
            raise TypeError("result must be a mapping")
        if (
            type(subject_sha256) is not str
            or len(subject_sha256) != 64
            or any(character not in "0123456789abcdef" for character in subject_sha256)
        ):
            raise ValueError("subject_sha256 must be a lowercase SHA-256 digest")
        copied: dict[str, SerializableValue] = {}
        for name, value in result.items():
            if type(name) is not str:
                raise TypeError("result keys must be built-in strings")
            copied[name] = value
        self._result = Piab1dCalculationResult.from_dict(copied)
        self._subject_sha256 = subject_sha256

    def _visualization_data(self) -> Piab1dVisualizationData:
        """Derive the visualization projection from authoritative result sections."""
        result = self._result
        return Piab1dVisualizationData.from_dict(
            {
                "length": ScalarQuantity(result.configuration.length, Unitless()),
                "retained_dimension": result.configuration.retained_dimension,
                "computed_energies": result.eigensystem.vector("computed_discrete"),
                "continuum_energies": result.eigensystem.vector(
                    "continuum_closed_form"
                ),
                "eigenvectors": result.eigensystem.matrix("euclidean"),
                "quadrature_eigenvectors": result.eigensystem.matrix(
                    "quadrature_normalized"
                ),
                "consistent": result.reduction.matrix("consistent"),
                "unmatched": result.reduction.matrix("unmatched"),
                "boundary": result.hamiltonian.matrix("boundary_realization"),
                "continuum_coordinates": result.analytical_sampling.vector(
                    "coordinates"
                ),
                "continuum_wavefunctions": result.analytical_sampling.matrix(
                    "wavefunctions"
                ),
                "selection": result.selection.selection.to_dict(),
                "convergence_interior_points": result.convergence.interior_points,
                "convergence_modes": result.convergence.modes,
                "convergence": result.convergence.analysis.to_dict(),
                "eigenpair_sweep": result.eigenpair_sweep.to_dict(),
                "residual_norm_sweep": result.residual_norm_sweep.to_dict(),
                "finite_algebraic_diagnostics": (
                    result.finite_algebraic_diagnostics.to_dict()
                ),
                "kinetic_potential_decomposition": (
                    result.kinetic_potential_decomposition.to_dict()
                ),
            }
        )

    def _verification_types(self) -> tuple[type[CompositeVerification], ...]:
        """Return the reusable component classes composed by PIAB1D."""
        return tuple(
            component_type for component_type, _ in self.verification_inventory
        )

    def _verification_components(self) -> tuple[CompositeVerification, ...]:
        """Compose reusable checks from the independent PIAB1D reference."""
        reference = Piab1dIndependentReferenceAnalyzer().execute(
            self._result,
            self._visualization_data(),
        )
        return tuple(
            component_type.evaluate(
                {name: reference.comparisons[name] for name in sorted(component_names)}
            )
            for component_type, component_names in self.verification_inventory
        )

    def _verification(
        self,
        *,
        visualization_data_sha256: str,
        components: tuple[CompositeVerification, ...],
    ) -> Piab1dVerification:
        """Compose the PIAB1D aggregate from reusable verification values."""
        return Piab1dVerification(
            subject_sha256=self._subject_sha256,
            visualization_data_sha256=visualization_data_sha256,
            components=components,
        )
