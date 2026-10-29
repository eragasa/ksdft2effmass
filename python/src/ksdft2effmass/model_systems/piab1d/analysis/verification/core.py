"""Independent represented-PIAB1D reference reconstruction."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

import numpy as np
from projectkoios.physkit.linalg.matrix.norm import MatrixNormEnum
from projectkoios.physkit.units import ScalarQuantity, Unitless

from ksdft2effmass.verification import MaximumAbsoluteErrorComparison

from ...diagnostics import diagnostic_method_names
from ...result import Piab1dCalculationResult
from ...visualizations.data import Piab1dVisualizationData


@dataclass(frozen=True, slots=True)
class Piab1dCoreReference:
    """Retain immutable comparisons derived by independent reconstruction."""

    comparisons: Mapping[str, MaximumAbsoluteErrorComparison]

    def __post_init__(self) -> None:
        if not self.comparisons:
            raise ValueError("independent reference comparisons must be nonempty")
        object.__setattr__(
            self,
            "comparisons",
            MappingProxyType(dict(self.comparisons)),
        )


@dataclass(frozen=True, slots=True, eq=False)
class Piab1dCoreReferenceRequest:
    """Bind admitted PIAB1D result data for independent core reconstruction."""

    result: Piab1dCalculationResult
    visualization_data: Piab1dVisualizationData

    def __post_init__(self) -> None:
        """Admit the complete typed core-reference request."""
        if type(self.result) is not Piab1dCalculationResult:
            raise TypeError("result must be Piab1dCalculationResult")
        if type(self.visualization_data) is not Piab1dVisualizationData:
            raise TypeError("visualization_data must be Piab1dVisualizationData")


class Piab1dCoreReferenceAnalyzer:
    """Derive core references from one constructor-bound admitted subject."""

    __slots__ = ("_request",)

    def __init__(self, request: Piab1dCoreReferenceRequest) -> None:
        if type(request) is not Piab1dCoreReferenceRequest:
            raise TypeError("request must be Piab1dCoreReferenceRequest")
        self._request = request

    @property
    def request(self) -> Piab1dCoreReferenceRequest:
        """Return the complete immutable core-reference request."""
        return self._request

    def execute(self) -> Piab1dCoreReference:
        """Reconstruct and compare the core finite problem independently.

        Returns
        -------
        Piab1dCoreReference
            Immutable operation-qualified comparisons for core calculations and the
            visualization projection.

        Raises
        ------
        ValueError
            Configuration or reconstructed finite identities are inadmissible.

        Notes
        -----
        The method constructs the finite-difference matrix and analytical formulas
        directly. It does not invoke ``Piab1dAnalyzer``.
        """
        result = self.request.result
        visualization_data = self.request.visualization_data
        configuration = result.configuration
        hamiltonian_section = result.hamiltonian
        eigensystem_section = result.eigensystem
        reduction_section = result.reduction
        quadrature_section = result.quadrature
        diagnostics = result.diagnostics

        length = configuration.length
        mass = configuration.mass
        points = configuration.interior_points
        retained = configuration.retained_dimension

        selection_beta = result.selection.beta
        selection = result.selection.selection
        selection_tolerance = selection.tolerance
        reported_probabilities = selection.probabilities.magnitude
        reported_omitted_probabilities = selection.omitted_probabilities.magnitude
        reported_selected_dimension = selection.selected_count
        if selection_beta <= 0.0:
            raise ValueError("selection beta must be positive")

        hamiltonian = hamiltonian_section.matrix("parent_hamiltonian").magnitude
        reduced_hamiltonian = hamiltonian_section.matrix(
            "reduced_hamiltonian"
        ).magnitude
        embedded_hamiltonian = hamiltonian_section.matrix(
            "embedded_reduced_hamiltonian"
        ).magnitude
        cyclic_reference = hamiltonian_section.matrix("cyclic_reference").magnitude
        boundary_realization = hamiltonian_section.matrix(
            "boundary_realization"
        ).magnitude
        reduction_map = reduction_section.matrix("reduction").magnitude
        embedding_map = reduction_section.matrix("embedding").magnitude
        projector = reduction_section.matrix("projector").magnitude
        eigenvectors = eigensystem_section.matrix("euclidean").magnitude
        quadrature_eigenvectors = eigensystem_section.matrix(
            "quadrature_normalized"
        ).magnitude
        quadrature_spacing = quadrature_section.scalar("spacing").magnitude
        quadrature_weights = quadrature_section.vector("interior_weights").magnitude
        reported_weighted_gram = quadrature_section.matrix("weighted_gram").magnitude
        reported_weighted_projector = quadrature_section.matrix(
            "weighted_projector"
        ).magnitude
        computed_energies = eigensystem_section.vector("computed_discrete").magnitude
        reported_discrete_energies = eigensystem_section.vector(
            "discrete_closed_form"
        ).magnitude
        reported_continuum_energies = eigensystem_section.vector(
            "continuum_closed_form"
        ).magnitude
        visualization_length = visualization_data.length.magnitude
        visualization_retained = visualization_data.retained_dimension
        visualization_computed_energies = visualization_data.computed_energies.magnitude
        visualization_continuum_energies = (
            visualization_data.continuum_energies.magnitude
        )
        visualization_eigenvectors = visualization_data.eigenvectors.magnitude
        visualization_quadrature_eigenvectors = (
            visualization_data.quadrature_eigenvectors.magnitude
        )
        visualization_consistent = visualization_data.consistent.magnitude
        visualization_unmatched = visualization_data.unmatched.magnitude
        visualization_boundary = visualization_data.boundary.magnitude
        visualization_selection = visualization_data.selection
        visualization_probabilities = visualization_selection.probabilities.magnitude
        visualization_omitted_probabilities = (
            visualization_selection.omitted_probabilities.magnitude
        )
        visualization_selection_tolerance = visualization_selection.tolerance
        visualization_selected_dimension = visualization_selection.selected_count
        continuum_coordinates = visualization_data.continuum_coordinates.magnitude
        continuum_wavefunctions = visualization_data.continuum_wavefunctions.magnitude
        convergence_points = visualization_data.convergence_interior_points
        convergence_modes = visualization_data.convergence_modes
        convergence = visualization_data.convergence
        convergence_order_modes = tuple(
            convergence_modes[column] for column in convergence.order_columns
        )
        convergence_spacings = convergence.spacings.magnitude
        convergence_errors = convergence.relative_errors.magnitude
        convergence_orders = convergence.observed_orders.magnitude

        if hamiltonian.shape != (points, points):
            raise ValueError("parent Hamiltonian shape does not match its space")
        if reduced_hamiltonian.shape != (retained, retained):
            raise ValueError("reduced Hamiltonian shape does not match its space")
        if embedding_map.shape != (points, retained) or reduction_map.shape != (
            retained,
            points,
        ):
            raise ValueError("coordinate-map shapes do not match their spaces")
        if eigenvectors.shape != (points, points):
            raise ValueError("eigenvectors do not match the parent space")

        # Rebuild the matrix from the declared convention instead of calling the
        # production solver; this preserves the verification route's independence.
        spacing = length / (points + 1)
        kinetic_prefactor = 1.0 / (2.0 * mass * spacing**2)
        expected_hamiltonian = np.diag(np.full(points, 2.0 * kinetic_prefactor))
        if points > 1:
            expected_hamiltonian += np.diag(
                np.full(points - 1, -kinetic_prefactor), k=1
            )
            expected_hamiltonian += np.diag(
                np.full(points - 1, -kinetic_prefactor), k=-1
            )
        mode_numbers = np.arange(1, points + 1, dtype=np.float64)
        expected_discrete_energies = (
            2.0
            * kinetic_prefactor
            * (1.0 - np.cos(mode_numbers * np.pi / (points + 1)))
        )
        expected_continuum_energies = (
            mode_numbers**2 * np.pi**2 / (2.0 * mass * length**2)
        )
        expected_continuum_coordinates = np.linspace(0.0, 1.0, 800)
        expected_continuum_wavefunctions = np.column_stack(
            tuple(
                np.sqrt(2.0) * np.sin(mode * np.pi * expected_continuum_coordinates)
                for mode in range(1, retained + 1)
            )
        )
        if continuum_coordinates.shape != expected_continuum_coordinates.shape:
            raise ValueError("continuum visualization coordinates have wrong shape")
        if continuum_wavefunctions.shape != expected_continuum_wavefunctions.shape:
            raise ValueError("continuum visualization wavefunctions have wrong shape")
        expected_convergence_points = tuple(range(8, 257))
        expected_convergence_modes = tuple(range(1, 7))
        expected_convergence_order_modes = tuple(range(1, 4))
        if convergence_points != expected_convergence_points:
            raise ValueError("convergence interior points differ from the contract")
        if convergence_modes != expected_convergence_modes:
            raise ValueError("convergence modes differ from the contract")
        if convergence_order_modes != expected_convergence_order_modes:
            raise ValueError("convergence order modes differ from the contract")
        expected_convergence_spacings = 1.0 / (
            np.asarray(expected_convergence_points, dtype=np.float64) + 1.0
        )
        convergence_arguments = (
            np.asarray(expected_convergence_modes, dtype=np.float64)[None, :]
            * np.pi
            / (
                2.0
                * (
                    np.asarray(expected_convergence_points, dtype=np.float64)[:, None]
                    + 1.0
                )
            )
        )
        expected_convergence_errors = (
            1.0 - (np.sin(convergence_arguments) / convergence_arguments) ** 2
        )
        expected_convergence_orders = np.log(
            expected_convergence_errors[:-1, :3] / expected_convergence_errors[1:, :3]
        ) / np.log(
            expected_convergence_spacings[:-1, None]
            / expected_convergence_spacings[1:, None]
        )
        if convergence_spacings.shape != expected_convergence_spacings.shape:
            raise ValueError("convergence spacings have the wrong shape")
        if convergence_errors.shape != expected_convergence_errors.shape:
            raise ValueError("convergence errors have the wrong shape")
        if convergence_orders.shape != expected_convergence_orders.shape:
            raise ValueError("convergence orders have the wrong shape")
        expected_boltzmann_factors = np.exp(
            -selection_beta * expected_discrete_energies
        )
        expected_probability_normalization = float(
            math.fsum(expected_boltzmann_factors)
        )
        expected_probabilities = (
            expected_boltzmann_factors / expected_probability_normalization
        )
        expected_omitted_probabilities = np.asarray(
            [
                math.fsum(expected_probabilities[dimension:])
                for dimension in range(1, points + 1)
            ],
            dtype=np.float64,
        )
        passing_dimensions = np.flatnonzero(
            expected_omitted_probabilities <= selection_tolerance
        )
        if passing_dimensions.size == 0:
            raise ValueError("no retained dimension satisfies the selection tolerance")
        expected_selected_dimension = int(passing_dimensions[0]) + 1
        expected_projector = embedding_map @ reduction_map
        expected_reduced = reduction_map @ hamiltonian @ embedding_map
        expected_embedded = embedding_map @ expected_reduced @ reduction_map
        complement = np.eye(points) - projector
        expected_retained = projector @ hamiltonian @ projector
        expected_retained_to_discarded = projector @ hamiltonian @ complement
        expected_discarded_to_retained = complement @ hamiltonian @ projector
        expected_discarded = complement @ hamiltonian @ complement
        expected_quadrature_weights = np.full(points, spacing, dtype=np.float64)
        expected_quadrature_eigenvectors = eigenvectors / np.sqrt(spacing)
        retained_quadrature_eigenvectors = expected_quadrature_eigenvectors[
            :, :retained
        ]
        expected_weighted_gram = retained_quadrature_eigenvectors.T @ (
            expected_quadrature_weights[:, None] * retained_quadrature_eigenvectors
        )
        expected_weighted_projector = (
            retained_quadrature_eigenvectors
            @ (
                expected_quadrature_weights[:, None] * retained_quadrature_eigenvectors
            ).T
        )
        eigenpair_residuals = np.linalg.norm(
            hamiltonian @ eigenvectors - eigenvectors @ np.diag(computed_energies),
            axis=0,
        )
        spectral_scale = float(np.max(np.abs(computed_energies)))
        if spectral_scale == 0.0:
            raise ValueError("the computed spectrum must have a nonzero scale")
        expected_scaled_eigenpair_residuals = eigenpair_residuals / spectral_scale
        expected_diagnostics: dict[str, float | np.ndarray] = {
            "discrete_spectrum_maximum_absolute_error": float(
                np.max(np.abs(computed_energies - expected_discrete_energies))
            ),
            "scaled_eigenpair_residuals": expected_scaled_eigenpair_residuals,
            "spectral_reconstruction_error": float(
                np.linalg.norm(
                    hamiltonian
                    - eigenvectors @ np.diag(computed_energies) @ eigenvectors.T,
                    ord="fro",
                )
            ),
            "projector_idempotency_error": float(
                np.linalg.norm(projector @ projector - projector, ord="fro")
            ),
            "weighted_gram_error": float(
                np.linalg.norm(expected_weighted_gram - np.eye(retained), ord="fro")
            ),
            "weighted_projector_error": float(
                np.linalg.norm(expected_weighted_projector - projector, ord="fro")
            ),
        }
        if {
            diagnostic_method_names[method] for method in diagnostics.observations
        } != set(expected_diagnostics):
            raise ValueError("diagnostics do not match the declared inventory")
        expected_cyclic = hamiltonian.copy()
        if points > 1:
            expected_cyclic[0, -1] = hamiltonian[0, 1]
            expected_cyclic[-1, 0] = hamiltonian[1, 0]

        checks = {
            "parent_hamiltonian_maximum_absolute_error": float(
                np.max(np.abs(hamiltonian - expected_hamiltonian))
            ),
            "discrete_spectrum_maximum_absolute_error": float(
                np.max(np.abs(computed_energies - expected_discrete_energies))
            ),
            "reported_discrete_spectrum_maximum_absolute_error": float(
                np.max(np.abs(reported_discrete_energies - expected_discrete_energies))
            ),
            "continuum_spectrum_maximum_absolute_error": float(
                np.max(
                    np.abs(reported_continuum_energies - expected_continuum_energies)
                )
            ),
            "eigenpair_residual_maximum_norm": float(np.max(eigenpair_residuals)),
            "eigenvector_orthonormality_maximum_absolute_error": float(
                np.max(np.abs(eigenvectors.T @ eigenvectors - np.eye(points)))
            ),
            "projector_maximum_absolute_error": float(
                np.max(np.abs(projector - expected_projector))
            ),
            "quadrature_spacing_absolute_error": abs(quadrature_spacing - spacing),
            "quadrature_weight_maximum_absolute_error": float(
                np.max(np.abs(quadrature_weights - expected_quadrature_weights))
            ),
            "quadrature_eigenvector_maximum_absolute_error": float(
                np.max(
                    np.abs(quadrature_eigenvectors - expected_quadrature_eigenvectors)
                )
            ),
            "weighted_gram_maximum_absolute_error": float(
                np.max(np.abs(reported_weighted_gram - expected_weighted_gram))
            ),
            "weighted_orthonormality_maximum_absolute_error": float(
                np.max(np.abs(expected_weighted_gram - np.eye(retained)))
            ),
            "weighted_projector_maximum_absolute_error": float(
                np.max(
                    np.abs(reported_weighted_projector - expected_weighted_projector)
                )
            ),
            "weighted_projector_equivalence_maximum_absolute_error": float(
                np.max(np.abs(expected_weighted_projector - projector))
            ),
            "reduced_hamiltonian_maximum_absolute_error": float(
                np.max(np.abs(reduced_hamiltonian - expected_reduced))
            ),
            "embedded_hamiltonian_maximum_absolute_error": float(
                np.max(np.abs(embedded_hamiltonian - expected_embedded))
            ),
            "retained_block_maximum_absolute_error": float(
                np.max(
                    np.abs(
                        reduction_section.matrix("retained").magnitude
                        - expected_retained
                    )
                )
            ),
            "retained_to_discarded_block_maximum_absolute_error": float(
                np.max(
                    np.abs(
                        reduction_section.matrix("retained_to_discarded").magnitude
                        - expected_retained_to_discarded
                    )
                )
            ),
            "discarded_to_retained_block_maximum_absolute_error": float(
                np.max(
                    np.abs(
                        reduction_section.matrix("discarded_to_retained").magnitude
                        - expected_discarded_to_retained
                    )
                )
            ),
            "discarded_block_maximum_absolute_error": float(
                np.max(
                    np.abs(
                        reduction_section.matrix("discarded").magnitude
                        - expected_discarded
                    )
                )
            ),
            "consistent_analysis_maximum_absolute_error": float(
                np.max(np.abs(reduction_section.matrix("consistent").magnitude))
            ),
            "unmatched_analysis_maximum_absolute_error": float(
                np.max(
                    np.abs(
                        reduction_section.matrix("unmatched").magnitude
                        - (embedded_hamiltonian - hamiltonian)
                    )
                )
            ),
            "discarded_analysis_maximum_absolute_error": float(
                np.max(
                    np.abs(
                        reduction_section.matrix("discarded_sector").magnitude
                        + expected_discarded
                    )
                )
            ),
            "cyclic_reference_maximum_absolute_error": float(
                np.max(np.abs(cyclic_reference - expected_cyclic))
            ),
            "boundary_realization_maximum_absolute_error": float(
                np.max(np.abs(boundary_realization - (hamiltonian - expected_cyclic)))
            ),
            "selection_probability_maximum_absolute_error": float(
                np.max(np.abs(reported_probabilities - expected_probabilities))
            ),
            "selection_omitted_probability_maximum_absolute_error": float(
                np.max(
                    np.abs(
                        np.asarray(
                            reported_omitted_probabilities,
                            dtype=np.float64,
                        )
                        - expected_omitted_probabilities
                    )
                )
            ),
            "selection_identity_error": float(
                reported_selected_dimension != expected_selected_dimension
            ),
            "visualization_length_absolute_error": abs(visualization_length - length),
            "visualization_retained_dimension_error": float(
                visualization_retained != retained
            ),
            "visualization_computed_energy_maximum_absolute_error": float(
                np.max(np.abs(visualization_computed_energies - computed_energies))
            ),
            "visualization_continuum_energy_maximum_absolute_error": float(
                np.max(
                    np.abs(
                        visualization_continuum_energies - reported_continuum_energies
                    )
                )
            ),
            "visualization_eigenvector_maximum_absolute_error": float(
                np.max(np.abs(visualization_eigenvectors - eigenvectors))
            ),
            "visualization_quadrature_eigenvector_maximum_absolute_error": float(
                np.max(
                    np.abs(
                        visualization_quadrature_eigenvectors - quadrature_eigenvectors
                    )
                )
            ),
            "visualization_consistent_maximum_absolute_error": float(
                np.max(
                    np.abs(
                        visualization_consistent
                        - reduction_section.matrix("consistent").magnitude
                    )
                )
            ),
            "visualization_unmatched_maximum_absolute_error": float(
                np.max(
                    np.abs(
                        visualization_unmatched
                        - reduction_section.matrix("unmatched").magnitude
                    )
                )
            ),
            "visualization_boundary_maximum_absolute_error": float(
                np.max(np.abs(visualization_boundary - boundary_realization))
            ),
            "visualization_probability_maximum_absolute_error": float(
                np.max(np.abs(visualization_probabilities - expected_probabilities))
            ),
            "visualization_omitted_probability_maximum_absolute_error": float(
                np.max(
                    np.abs(
                        visualization_omitted_probabilities
                        - expected_omitted_probabilities
                    )
                )
            ),
            "visualization_selection_tolerance_absolute_error": abs(
                visualization_selection_tolerance - selection_tolerance
            ),
            "visualization_selected_dimension_error": float(
                visualization_selected_dimension != reported_selected_dimension
            ),
            "continuum_visualization_coordinate_maximum_absolute_error": float(
                np.max(np.abs(continuum_coordinates - expected_continuum_coordinates))
            ),
            "continuum_visualization_wavefunction_maximum_absolute_error": float(
                np.max(
                    np.abs(continuum_wavefunctions - expected_continuum_wavefunctions)
                )
            ),
            "convergence_spacing_maximum_absolute_error": float(
                np.max(np.abs(convergence_spacings - expected_convergence_spacings))
            ),
            "convergence_relative_error_maximum_absolute_error": float(
                np.max(np.abs(convergence_errors - expected_convergence_errors))
            ),
            "convergence_order_maximum_absolute_error": float(
                np.max(np.abs(convergence_orders - expected_convergence_orders))
            ),
        }

        energy_tolerance = 1.0e-12
        length_tolerance = 1.0e-12
        unitless_tolerance = 1.0e-12
        for method, diagnostic in diagnostics.observations.items():
            name = diagnostic_method_names[method]
            expected = expected_diagnostics[name]
            expected_atol = (
                energy_tolerance
                if name
                in {
                    "discrete_spectrum_maximum_absolute_error",
                    "spectral_reconstruction_error",
                }
                else unitless_tolerance
            )
            if diagnostic.atol.magnitude != expected_atol or diagnostic.rtol != 0.0:
                raise ValueError(f"diagnostic tolerance differs: {name}")
            if diagnostic.options is not None and (
                diagnostic.options.matrix_norm is not MatrixNormEnum.frobenius
            ):
                raise ValueError(f"matrix-norm option differs: {name}")
            observed = np.asarray(diagnostic.value.magnitude, dtype=np.float64)
            expected_values = np.asarray(expected, dtype=np.float64)
            if observed.shape != expected_values.shape:
                raise ValueError(f"diagnostic shape differs: {name}")
            checks[f"serialized_{name}_maximum_absolute_error"] = float(
                np.max(np.abs(observed - expected_values))
            )

        energy_check_names = {
            "parent_hamiltonian_maximum_absolute_error",
            "discrete_spectrum_maximum_absolute_error",
            "reported_discrete_spectrum_maximum_absolute_error",
            "continuum_spectrum_maximum_absolute_error",
            "eigenpair_residual_maximum_norm",
            "reduced_hamiltonian_maximum_absolute_error",
            "embedded_hamiltonian_maximum_absolute_error",
            "retained_block_maximum_absolute_error",
            "retained_to_discarded_block_maximum_absolute_error",
            "discarded_to_retained_block_maximum_absolute_error",
            "discarded_block_maximum_absolute_error",
            "consistent_analysis_maximum_absolute_error",
            "unmatched_analysis_maximum_absolute_error",
            "discarded_analysis_maximum_absolute_error",
            "cyclic_reference_maximum_absolute_error",
            "boundary_realization_maximum_absolute_error",
            "visualization_computed_energy_maximum_absolute_error",
            "visualization_continuum_energy_maximum_absolute_error",
            "visualization_consistent_maximum_absolute_error",
            "visualization_unmatched_maximum_absolute_error",
            "visualization_boundary_maximum_absolute_error",
            "serialized_discrete_spectrum_maximum_absolute_error_maximum_absolute_error",
            "serialized_spectral_reconstruction_error_maximum_absolute_error",
        }
        length_check_names = {
            "quadrature_spacing_absolute_error",
            "quadrature_weight_maximum_absolute_error",
            "visualization_length_absolute_error",
        }
        check_tolerances = {
            name: (
                energy_tolerance
                if name in energy_check_names
                else length_tolerance
                if name in length_check_names
                else unitless_tolerance
            )
            for name in checks
        }
        minimum_order_error = float(
            np.min(expected_convergence_errors[:, : len(convergence_order_modes)])
        )
        minimum_log_spacing_ratio = float(
            np.min(
                np.log(
                    expected_convergence_spacings[:-1]
                    / expected_convergence_spacings[1:]
                )
            )
        )
        check_tolerances["convergence_order_maximum_absolute_error"] = float(
            8.0
            * np.finfo(np.float64).eps
            / minimum_order_error
            / minimum_log_spacing_ratio
        )
        comparisons = {
            name: MaximumAbsoluteErrorComparison(
                observed=ScalarQuantity(value, Unitless()),
                reference=ScalarQuantity(0.0, Unitless()),
                tolerance=ScalarQuantity(check_tolerances[name], Unitless()),
            )
            for name, value in checks.items()
        }
        return Piab1dCoreReference(comparisons=comparisons)
