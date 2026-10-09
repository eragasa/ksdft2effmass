r"""Independent numerical verification of the Appendix G reduction challenge.

The verifier reconstructs every retained channel directly from correlated version-one
controls using NumPy and SciPy primitives. Plane-wave and periodic second-difference
matrices act in the dimensionless convention :math:`a=2\pi`, :math:`G=1`, and
:math:`E_G=1`. Complete scalar hopping coefficients use

.. math::

   t_R=N_k^{-1}\sum_j e^{-i k_j R}E(k_j),

and fitting routes solve their stated complex least-squares problems without normal
equations. Scalar parallel transport includes reciprocal sewing of the finite
plane-wave basis and rejects overlaps no larger than ``1e-14``.

The implementation does not import the historical runner or production plane-wave,
finite-difference, frame-transport, hopping-transform, or fitting algorithms. Dense
plane-wave work scales cubically in ``2*cutoff+1``; finite-difference eigensolves scale
cubically in the requested point count; stored dense matrices scale quadratically.
The verifier imposes no arbitrary size cap, so allocation may raise ``MemoryError``.
Its result is bounded numerical verification of represented dimensionless channels,
not convergence, parent-model adequacy, material validation, UQ, or acceptance.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import SupportsFloat

import numpy as np
import numpy.typing as npt
from scipy.linalg import eigh  # type: ignore[import-untyped]

from ksdft2effmass.operators import ScalarQuantity, Unitless

from .correlation_workflow import (
    Periodic1DReductionChallengeCampaignWorkflowResult,
)
from .definition import (
    Periodic1DReductionChallengeCampaignDefinition,
    Periodic1DReductionChallengePotentialShape,
)
from .results import Periodic1DReductionChallengeCampaignResult

type ComplexMatrix = npt.NDArray[np.complex128]
type ComplexVector = npt.NDArray[np.complex128]
type RealMatrix = npt.NDArray[np.float64]
type RealVector = npt.NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class Periodic1DReductionChallengeVerificationRequest:
    """Provide correlated records and one inclusive absolute tolerance.

    Parameters
    ----------
    correlated_campaign
        Read-only input/result correlation with exact retained byte identities.
    absolute_tolerance
        Inclusive ``Unitless`` tolerance applied separately to each reconstructed
        channel maximum. Energy residuals use normalized :math:`E_G=1`; overlap,
        aligned-frame, and phase diagnostics are dimensionless.

    Raises
    ------
    TypeError
        If either value has the wrong exact semantic type.
    ValueError
        If the tolerance is not unitless or is negative.
    OverflowError
        If the tolerance is not finite binary64.
    """

    correlated_campaign: Periodic1DReductionChallengeCampaignWorkflowResult
    absolute_tolerance: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate exact correlation ownership and nonnegative unitless tolerance."""
        if (
            type(self.correlated_campaign)
            is not Periodic1DReductionChallengeCampaignWorkflowResult
        ):
            raise TypeError(
                "correlated_campaign must be "
                "Periodic1DReductionChallengeCampaignWorkflowResult"
            )
        if type(self.absolute_tolerance) is not ScalarQuantity:
            raise TypeError("absolute_tolerance must be ScalarQuantity")
        if not isinstance(self.absolute_tolerance.unit, Unitless):
            raise ValueError("absolute_tolerance must use Unitless")
        if not np.isfinite(self.absolute_tolerance.magnitude):
            raise OverflowError("absolute_tolerance must be finite binary64")
        if self.absolute_tolerance.magnitude < 0.0:
            raise ValueError("absolute_tolerance must be nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DReductionChallengeVerificationResult:
    """Retain independent defects for every challenge-result channel.

    Parameters
    ----------
    potential_amplitude_maximum_absolute_defect
        Maximum defect across amplitude gaps, statuses, sign covariance, and both
        discretization studies.
    potential_shape_maximum_absolute_defect
        Maximum defect across shape spectra, adjacent gaps, finite-difference errors,
        time reversal, translation, and constant shifts.
    mesh_band_isolation_maximum_absolute_defect
        Maximum defect across every mesh, band, amplitude, isolation, overlap,
        complete-reconstruction, and withheld-range record.
    gauge_covariance_maximum_absolute_defect
        Maximum defect across deterministic phase-gauge projector, transported-frame,
        and closure-holonomy diagnostics.
    route_assumption_maximum_absolute_defect
        Maximum defect across complete, weighted, and incomplete fitting routes in
        coefficient and comparison spaces.
    absolute_tolerance
        Inclusive unitless tolerance applied separately to all five channel maxima.
    passes
        Aggregate bounded numerical-verification disposition.
    """

    potential_amplitude_maximum_absolute_defect: ScalarQuantity
    potential_shape_maximum_absolute_defect: ScalarQuantity
    mesh_band_isolation_maximum_absolute_defect: ScalarQuantity
    gauge_covariance_maximum_absolute_defect: ScalarQuantity
    route_assumption_maximum_absolute_defect: ScalarQuantity
    absolute_tolerance: ScalarQuantity
    passes: bool

    def __post_init__(self) -> None:
        """Validate unitless nonnegative defects and the exact disposition."""
        defects = (
            self.potential_amplitude_maximum_absolute_defect,
            self.potential_shape_maximum_absolute_defect,
            self.mesh_band_isolation_maximum_absolute_defect,
            self.gauge_covariance_maximum_absolute_defect,
            self.route_assumption_maximum_absolute_defect,
        )
        values = (*defects, self.absolute_tolerance)
        if any(type(value) is not ScalarQuantity for value in values):
            raise TypeError("challenge verification values must be ScalarQuantity")
        if any(not isinstance(value.unit, Unitless) for value in values):
            raise ValueError("challenge verification values must use Unitless")
        if any(not np.isfinite(value.magnitude) for value in values):
            raise OverflowError("challenge verification values must be finite binary64")
        if any(value.magnitude < 0.0 for value in values):
            raise ValueError("challenge verification values must be nonnegative")
        if type(self.passes) is not bool:
            raise TypeError("passes must be a built-in bool")
        expected = all(
            defect.magnitude <= self.absolute_tolerance.magnitude for defect in defects
        )
        if self.passes is not expected:
            raise ValueError("passes must match all channel defects and tolerance")


class Periodic1DReductionChallengeResultVerifier:
    """Independently reconstruct all retained reduction-challenge diagnostics.

    The Action consumes one authenticated correlation and retains no mutable request or
    result state. Expected qualitative trends are never converted into additional pass
    criteria; only retained-versus-reconstructed channel defects are compared with the
    caller's explicit tolerance.
    """

    __slots__ = ()

    sample_momenta = (-0.5, -0.25, 0.0, 0.25, 0.5)

    def execute(
        self, request: Periodic1DReductionChallengeVerificationRequest
    ) -> Periodic1DReductionChallengeVerificationResult:
        """Reconstruct every typed channel and compare retained scalars.

        Parameters
        ----------
        request
            Correlated controls, outcomes, and explicit tolerance.

        Returns
        -------
        Periodic1DReductionChallengeVerificationResult
            Five separate maximum defects and their aggregate disposition.

        Raises
        ------
        TypeError
            If ``request`` or a nested value has the wrong exact representation.
        ValueError
            If retained dispositions, controls, dimensions, or required cases disagree.
        OverflowError
            If a reconstructed scalar or array is not finite binary64/complex128.
        MemoryError
            If dense matrix, path, Fourier, or least-squares allocation fails.
        numpy.linalg.LinAlgError
            If a dense eigensolver or least-squares operation does not converge.
        """
        if type(request) is not Periodic1DReductionChallengeVerificationRequest:
            raise TypeError(
                "request must be Periodic1DReductionChallengeVerificationRequest"
            )
        correlated = request.correlated_campaign
        definition = correlated.definition
        result = correlated.campaign_result
        defects = tuple(
            self._finite_scalar(value, name)
            for value, name in zip(
                (
                    self._potential_amplitude_defect(definition, result),
                    self._potential_shape_defect(definition, result),
                    self._mesh_band_isolation_defect(definition, result),
                    self._gauge_covariance_defect(definition, result),
                    self._route_assumption_defect(definition, result),
                ),
                (
                    "potential-amplitude maximum defect",
                    "potential-shape maximum defect",
                    "mesh/band/isolation maximum defect",
                    "gauge-covariance maximum defect",
                    "route-assumption maximum defect",
                ),
                strict=True,
            )
        )
        quantities = tuple(ScalarQuantity(value, Unitless()) for value in defects)
        tolerance = request.absolute_tolerance.magnitude
        return Periodic1DReductionChallengeVerificationResult(
            quantities[0],
            quantities[1],
            quantities[2],
            quantities[3],
            quantities[4],
            request.absolute_tolerance,
            all(value <= tolerance for value in defects),
        )

    def _potential_amplitude_defect(
        self,
        definition: Periodic1DReductionChallengeCampaignDefinition,
        result: Periodic1DReductionChallengeCampaignResult,
    ) -> float:
        """Return the maximum reconstructed potential-amplitude channel defect.

        Parameters
        ----------
        definition
            Exact amplitude, cutoff, grid, band-count, and isolation controls.
        result
            Typed retained amplitude outcomes.

        Returns
        -------
        float
            Maximum absolute retained-versus-recomputed defect in unitless
            :math:`E_G` units.

        Raises
        ------
        ValueError
            If a retained isolation status disagrees with the recomputed gap rule.
        """
        defects: list[float] = []
        band_count = definition.compared_band_count
        reference_cutoff = definition.plane_wave_reference_cutoff
        for retained in result.potential_amplitude:
            strength = retained.potential_strength
            reference = np.asarray(
                [
                    self._cosine_eigensystem(k, strength, reference_cutoff)[0][
                        :band_count
                    ]
                    for k in self.sample_momenta
                ],
                dtype=np.float64,
            )
            boundary = self._cosine_eigensystem(0.5, strength, reference_cutoff)[0]
            gap = float(boundary[1] - boundary[0])
            expected_status = (
                "pass"
                if gap > definition.isolation_gap_threshold.magnitude
                else "failed_gap_closure"
            )
            if retained.isolated_band_status != expected_status:
                raise ValueError("retained amplitude isolation status is incorrect")
            defects.append(abs(gap - retained.zone_boundary_gap))
            positive = np.asarray(
                [
                    self._cosine_eigensystem(
                        k, strength, definition.plane_wave_cutoffs[-1]
                    )[0][:band_count]
                    for k in self.sample_momenta
                ]
            )
            negative = np.asarray(
                [
                    self._cosine_eigensystem(
                        k, -strength, definition.plane_wave_cutoffs[-1]
                    )[0][:band_count]
                    for k in self.sample_momenta
                ]
            )
            sign_defect = float(np.max(np.abs(positive - negative)))
            defects.append(
                abs(sign_defect - retained.potential_sign_invariance_maximum_error)
            )
            for observation in retained.plane_wave_cutoff_study:
                values = np.asarray(
                    [
                        self._cosine_eigensystem(k, strength, observation.resolution)[
                            0
                        ][:band_count]
                        for k in self.sample_momenta
                    ]
                )
                observed = float(np.max(np.abs(values - reference)))
                defects.append(abs(observed - observation.maximum_low_band_error))
            for observation in retained.finite_difference_grid_study:
                values = np.asarray(
                    [
                        self._finite_difference_energies(
                            k,
                            0.0,
                            (strength,),
                            (0.0,),
                            observation.resolution,
                            band_count,
                            definition.period.magnitude,
                        )
                        for k in self.sample_momenta
                    ]
                )
                observed = float(np.max(np.abs(values - reference)))
                defects.append(abs(observed - observation.maximum_low_band_error))
        return self._maximum_finite_defect(defects, "potential-amplitude defects")

    def _potential_shape_defect(
        self,
        definition: Periodic1DReductionChallengeCampaignDefinition,
        result: Periodic1DReductionChallengeCampaignResult,
    ) -> float:
        """Return the maximum reconstructed potential-shape channel defect.

        Parameters
        ----------
        definition
            Exact named finite-Fourier potentials and discretization controls.
        result
            Typed retained shape, translation, and constant-shift outcomes.

        Returns
        -------
        float
            Maximum absolute retained-versus-recomputed defect in unitless
            :math:`E_G` units.

        Raises
        ------
        ValueError
            If the baseline, translated, or constant-shifted covariance controls are
            absent from the correlated campaign.
        """
        defects: list[float] = []
        mesh = np.linspace(-0.5, 0.5, 33)
        spectra: dict[str, RealVector] = {}
        retained_by_id = {
            item.identifier: item for item in result.potential_shapes.cases
        }
        shape_by_id = {item.identifier: item for item in definition.potential_shapes}
        required_shapes = {
            "baseline_cosine",
            "translated_cosine",
            "constant_shifted_cosine",
        }
        if not (
            required_shapes.issubset(retained_by_id)
            and required_shapes.issubset(shape_by_id)
        ):
            raise ValueError("required potential-shape covariance controls are absent")
        for shape in definition.potential_shapes:
            retained = retained_by_id[shape.identifier]
            reference = np.asarray(
                [
                    self._shape_eigensystem(
                        float(k), shape, definition.plane_wave_reference_cutoff
                    )[0][: definition.compared_band_count]
                    for k in mesh
                ],
                dtype=np.float64,
            )
            finite_difference = np.asarray(
                [
                    self._finite_difference_energies(
                        float(k),
                        shape.potential.constant_coefficient.magnitude,
                        tuple(
                            float(value)
                            for value in shape.potential.cosine_coefficients.magnitude
                        ),
                        tuple(
                            float(value)
                            for value in shape.potential.sine_coefficients.magnitude
                        ),
                        definition.finite_difference_points[-1],
                        definition.compared_band_count,
                        definition.period.magnitude,
                    )
                    for k in mesh
                ],
                dtype=np.float64,
            )
            gaps = self._minimum_band_gaps(reference)
            defects.extend(
                (
                    abs(
                        float(np.max(np.abs(finite_difference - reference)))
                        - retained.finest_grid_maximum_band_error
                    ),
                    abs(
                        float(np.max(np.abs(reference - reference[::-1])))
                        - retained.time_reversal_energy_residual
                    ),
                    float(
                        np.max(
                            np.abs(
                                gaps
                                - np.asarray(
                                    retained.minimum_adjacent_gaps, dtype=np.float64
                                )
                            )
                        )
                    ),
                )
            )
            spectra[shape.identifier] = np.asarray(
                reference.reshape(-1), dtype=np.float64
            )
        translation = float(
            np.max(np.abs(spectra["translated_cosine"] - spectra["baseline_cosine"]))
        )
        constant_offset = (
            shape_by_id[
                "constant_shifted_cosine"
            ].potential.constant_coefficient.magnitude
            - shape_by_id["baseline_cosine"].potential.constant_coefficient.magnitude
        )
        constant_shift = float(
            np.max(
                np.abs(
                    spectra["constant_shifted_cosine"]
                    - constant_offset
                    - spectra["baseline_cosine"]
                )
            )
        )
        shape_result = result.potential_shapes
        defects.extend(
            (
                abs(translation - shape_result.translation_isospectral_maximum_error),
                abs(
                    constant_shift
                    - shape_result.constant_shift_covariance_maximum_error
                ),
            )
        )
        return self._maximum_finite_defect(defects, "potential-shape defects")

    def _mesh_band_isolation_defect(
        self,
        definition: Periodic1DReductionChallengeCampaignDefinition,
        result: Periodic1DReductionChallengeCampaignResult,
    ) -> float:
        """Return the maximum reconstructed mesh/band/isolation channel defect.

        Parameters
        ----------
        definition
            Exact amplitude, mesh, band, hopping-range, and withheld-mesh controls.
        result
            Typed retained mesh, isolation, overlap, and reconstruction outcomes.

        Returns
        -------
        float
            Maximum absolute numeric defect across dimensionless energy, overlap, and
            reconstruction diagnostics.

        Raises
        ------
        ValueError
            If a retained isolation applicability flag disagrees with the recomputed
            adjacent-gap rule.
        """
        defects: list[float] = []
        lookup = {
            (item.potential_strength, item.mesh_size, item.band_index): item
            for item in result.mesh_band_isolation
        }
        period = definition.period.magnitude
        withheld_coordinates = np.linspace(-0.5, 0.5, definition.withheld_mesh_size)
        required_bands = max(definition.challenged_band_indices) + 2
        cutoff = definition.plane_wave_cutoffs[-1]
        for strength in definition.potential_strengths.magnitude:
            numeric_strength = float(strength)
            withheld = np.asarray(
                [
                    self._cosine_eigensystem(float(k), numeric_strength, cutoff)[0][
                        :required_bands
                    ]
                    for k in withheld_coordinates
                ]
            )
            for mesh_size in definition.reciprocal_mesh_sizes:
                coordinates, bands, states = self._cosine_band_mesh(
                    numeric_strength, cutoff, mesh_size, required_bands
                )
                gaps = self._minimum_band_gaps(bands)
                representatives = np.arange(
                    -mesh_size // 2, mesh_size // 2, dtype=np.int64
                )
                mask = np.abs(representatives) <= definition.hopping_range_cells
                for band_index in definition.challenged_band_indices:
                    retained = lookup[(numeric_strength, mesh_size, band_index)]
                    energies = bands[:, band_index]
                    band_states = states[:, band_index, :]
                    minimum_overlap = self._minimum_sewn_overlap(band_states)
                    hoppings = self._direct_hoppings(
                        energies, coordinates, representatives, period
                    )
                    reconstruction = self._reconstruct(
                        hoppings, coordinates, representatives, period
                    )
                    withheld_model = self._reconstruct(
                        hoppings[mask],
                        withheld_coordinates,
                        representatives[mask],
                        period,
                    )
                    gap = float(gaps[band_index])
                    applicable = gap > definition.isolation_gap_threshold.magnitude
                    if retained.isolation_applicable is not applicable:
                        raise ValueError(
                            "retained mesh isolation disposition is incorrect"
                        )
                    defects.extend(
                        (
                            abs(gap - retained.minimum_adjacent_gap),
                            abs(
                                minimum_overlap - retained.minimum_sewn_neighbor_overlap
                            ),
                            abs(
                                float(np.max(np.abs(reconstruction.real - energies)))
                                - retained.full_reconstruction_maximum_error
                            ),
                            abs(
                                float(
                                    np.max(
                                        np.abs(
                                            withheld[:, band_index]
                                            - withheld_model.real
                                        )
                                    )
                                )
                                - retained.fixed_range_withheld_maximum_error
                            ),
                        )
                    )
        return self._maximum_finite_defect(defects, "mesh/band/isolation defects")

    def _gauge_covariance_defect(
        self,
        definition: Periodic1DReductionChallengeCampaignDefinition,
        result: Periodic1DReductionChallengeCampaignResult,
    ) -> float:
        """Return the maximum reconstructed deterministic gauge-channel defect.

        Parameters
        ----------
        definition
            Exact gauge-challenge amplitude, cutoff, and reciprocal mesh.
        result
            Typed retained projector, transported-frame, and holonomy defects.

        Returns
        -------
        float
            Maximum absolute retained-versus-recomputed gauge diagnostic defect.
        """
        retained = result.gauge_covariance
        _, _, all_states = self._cosine_band_mesh(
            definition.route_challenge_potential_strength.magnitude,
            definition.plane_wave_cutoffs[-1],
            definition.route_challenge_mesh_size,
            1,
        )
        states = all_states[:, 0, :]
        indices = np.arange(definition.route_challenge_mesh_size, dtype=np.float64)
        phases = np.exp(1j * (0.7 * np.sin(indices) + 0.3 * np.cos(3.0 * indices)))
        transformed = states * phases[:, None]
        transported_a, holonomy_a = self._parallel_transport(states)
        transported_b, holonomy_b = self._parallel_transport(transformed)
        overlap = np.vdot(transported_a[0], transported_b[0])
        transported_b *= np.exp(-1j * np.angle(overlap))
        frame_defect = float(
            np.max(np.linalg.norm(transported_a - transported_b, axis=1))
        )
        projector_defect = float(
            max(
                np.linalg.norm(
                    np.outer(state, state.conj()) - np.outer(changed, changed.conj())
                )
                for state, changed in zip(states, transformed, strict=True)
            )
        )
        holonomy_defect = float(abs(np.angle(np.exp(1j * (holonomy_a - holonomy_b)))))
        return self._maximum_finite_defect(
            [
                abs(
                    projector_defect
                    - retained.random_phase_projector_maximum_frobenius_defect
                ),
                abs(
                    frame_defect
                    - retained.parallel_transport_frame_maximum_aligned_defect
                ),
                abs(holonomy_defect - retained.closure_holonomy_difference_modulo_2pi),
            ],
            "gauge-covariance defects",
        )

    def _route_assumption_defect(
        self,
        definition: Periodic1DReductionChallengeCampaignDefinition,
        result: Periodic1DReductionChallengeCampaignResult,
    ) -> float:
        """Return the maximum reconstructed fitting-route channel defect.

        Parameters
        ----------
        definition
            Exact route-challenge amplitude, mesh, hopping range, and period.
        result
            Typed complete, incomplete-training, and weighted-route outcomes.

        Returns
        -------
        float
            Maximum absolute defect across coefficient and 257-point comparison-space
            diagnostics.
        """
        retained = result.route_assumptions
        period = definition.period.magnitude
        mesh_size = definition.route_challenge_mesh_size
        coordinates, bands, _ = self._cosine_band_mesh(
            definition.route_challenge_potential_strength.magnitude,
            definition.plane_wave_cutoffs[-1],
            mesh_size,
            1,
        )
        energies = bands[:, 0]
        representatives = np.arange(-mesh_size // 2, mesh_size // 2, dtype=np.int64)
        hoppings = self._direct_hoppings(energies, coordinates, representatives, period)
        mask = np.abs(representatives) <= definition.route_challenge_hopping_range_cells
        kept_representatives = representatives[mask]
        mediated = hoppings[mask]
        design = np.exp(1j * np.outer(coordinates, kept_representatives * period))
        uniform = np.linalg.lstsq(design, energies, rcond=None)[0]
        weights = 1.0 + 4.0 * np.exp(-np.square(coordinates / 0.15))
        weighted = np.linalg.lstsq(
            np.sqrt(weights)[:, None] * design,
            np.sqrt(weights) * energies,
            rcond=None,
        )[0]
        training = np.abs(coordinates) <= 0.3
        incomplete = np.linalg.lstsq(design[training], energies[training], rcond=None)[
            0
        ]
        comparison_coordinates = np.linspace(-0.5, 0.5, 257)
        comparison_design = np.exp(
            1j * np.outer(comparison_coordinates, kept_representatives * period)
        )
        observed = (
            float(np.linalg.norm(uniform - mediated)),
            float(np.linalg.norm(incomplete - mediated)),
            float(np.linalg.norm(comparison_design @ (incomplete - mediated))),
            float(np.linalg.norm(weighted - mediated)),
            float(np.linalg.norm(comparison_design @ (weighted - mediated))),
        )
        retained_values = (
            retained.uniform_complete_coefficient_defect,
            retained.incomplete_training_coefficient_defect,
            retained.incomplete_training_comparison_l2_defect,
            retained.nonuniform_weight_coefficient_defect,
            retained.nonuniform_weight_comparison_l2_defect,
        )
        return self._maximum_finite_defect(
            [
                abs(value - expected)
                for value, expected in zip(observed, retained_values, strict=True)
            ],
            "route-assumption defects",
        )

    def _maximum_finite_defect(self, values: list[float], name: str) -> float:
        """Return a maximum only after every candidate is finite binary64."""
        if not values:
            raise ValueError(f"{name} must be nonempty")
        finite_values = tuple(
            self._finite_scalar(value, f"{name}[{index}]")
            for index, value in enumerate(values)
        )
        return max(finite_values)

    @staticmethod
    def _finite_scalar(value: SupportsFloat, name: str) -> float:
        """Return one finite binary64 scalar or fail closed on range loss."""
        try:
            result = float(value)
        except (OverflowError, ValueError) as error:
            raise OverflowError(f"{name} must be representable as binary64") from error
        if not np.isfinite(result):
            raise OverflowError(f"{name} must be finite binary64")
        return result

    @staticmethod
    def _finite_real_array(value: RealVector | RealMatrix, name: str) -> None:
        """Require every element of a binary64 vector or matrix to be finite."""
        if not np.all(np.isfinite(value)):
            raise OverflowError(f"{name} must contain finite binary64 values")

    @staticmethod
    def _finite_complex_array(value: ComplexVector | ComplexMatrix, name: str) -> None:
        """Require every real and imaginary component to be finite binary64."""
        if not np.all(np.isfinite(value.real)) or not np.all(np.isfinite(value.imag)):
            raise OverflowError(f"{name} must contain finite complex128 values")

    def _cosine_eigensystem(
        self, momentum: float, strength: float, cutoff: int
    ) -> tuple[RealVector, ComplexMatrix]:
        """Return one independently assembled cosine plane-wave eigensystem.

        Parameters
        ----------
        momentum, strength
            Reduced reciprocal coordinate and cosine amplitude in unitless
            :math:`E_G` conventions.
        cutoff
            Symmetric reciprocal-index cutoff; the matrix dimension is ``2*cutoff+1``.

        Returns
        -------
        tuple
            Increasing binary64 eigenvalues and column-oriented complex eigenvectors.
        """
        indices = np.arange(-cutoff, cutoff + 1, dtype=np.float64)
        matrix = np.diag(np.square(momentum + indices)).astype(np.complex128)
        coupling = 0.5 * strength
        matrix += np.diag(np.full(2 * cutoff, coupling), 1)
        matrix += np.diag(np.full(2 * cutoff, coupling), -1)
        self._finite_complex_array(matrix, "cosine plane-wave matrix")
        raw_values, raw_vectors = np.linalg.eigh(matrix)
        values = np.asarray(raw_values, dtype=np.float64)
        vectors = np.asarray(raw_vectors, dtype=np.complex128)
        self._finite_real_array(values, "cosine eigenvalues")
        self._finite_complex_array(vectors, "cosine eigenvectors")
        return values, vectors

    def _shape_eigensystem(
        self,
        momentum: float,
        shape: Periodic1DReductionChallengePotentialShape,
        cutoff: int,
    ) -> tuple[RealVector, ComplexMatrix]:
        """Return one independently assembled finite-Fourier eigensystem.

        Parameters
        ----------
        momentum
            Reduced reciprocal coordinate.
        shape
            Named real finite-Fourier potential with unitless coefficients.
        cutoff
            Symmetric reciprocal-index cutoff.

        Returns
        -------
        tuple
            Increasing binary64 eigenvalues and column-oriented complex eigenvectors.
        """
        indices = np.arange(-cutoff, cutoff + 1, dtype=np.float64)
        dimension = 2 * cutoff + 1
        matrix = np.diag(
            np.square(momentum + indices)
            + shape.potential.constant_coefficient.magnitude
        ).astype(np.complex128)
        for harmonic, (cosine, sine) in enumerate(
            zip(
                shape.potential.cosine_coefficients.magnitude,
                shape.potential.sine_coefficients.magnitude,
                strict=True,
            ),
            start=1,
        ):
            diagonal_size = dimension - harmonic
            matrix += np.diag(
                np.full(diagonal_size, 0.5 * (cosine + 1j * sine)), harmonic
            )
            matrix += np.diag(
                np.full(diagonal_size, 0.5 * (cosine - 1j * sine)), -harmonic
            )
        self._finite_complex_array(matrix, "finite-Fourier plane-wave matrix")
        raw_values, raw_vectors = np.linalg.eigh(matrix)
        values = np.asarray(raw_values, dtype=np.float64)
        vectors = np.asarray(raw_vectors, dtype=np.complex128)
        self._finite_real_array(values, "finite-Fourier eigenvalues")
        self._finite_complex_array(vectors, "finite-Fourier eigenvectors")
        return values, vectors

    def _finite_difference_energies(
        self,
        momentum: float,
        constant: float,
        cosine_coefficients: tuple[float, ...],
        sine_coefficients: tuple[float, ...],
        points: int,
        bands: int,
        period: float,
    ) -> RealVector:
        """Return independently assembled lowest finite-difference eigenvalues.

        Parameters
        ----------
        momentum, constant
            Reduced reciprocal coordinate and constant potential coefficient.
        cosine_coefficients, sine_coefficients
            Equal-length real harmonic coefficient inventories in :math:`E_G` units.
        points
            Number of half-open periodic grid points.
        bands
            Number of increasing low eigenvalues to return.
        period
            Direct-cell period in the unitless representation.

        Returns
        -------
        numpy.ndarray
            Lowest ``bands`` binary64 eigenvalues of the Hermitian periodic
            second-difference matrix.
        """
        spacing = period / float(points)
        kinetic = 1.0 / spacing**2
        coordinates = spacing * np.arange(points, dtype=np.float64)
        potential = np.full(points, constant, dtype=np.float64)
        for harmonic, (cosine, sine) in enumerate(
            zip(cosine_coefficients, sine_coefficients, strict=True), start=1
        ):
            potential += cosine * np.cos(harmonic * coordinates)
            potential += sine * np.sin(harmonic * coordinates)
        matrix = np.diag(2.0 * kinetic + potential).astype(np.complex128)
        off_diagonal = np.full(points - 1, -kinetic)
        matrix += np.diag(off_diagonal, 1) + np.diag(off_diagonal, -1)
        matrix[0, -1] = -kinetic * np.exp(-1j * momentum * period)
        matrix[-1, 0] = matrix[0, -1].conjugate()
        # SciPy's ``check_finite=False`` avoids a duplicate dense scan; this independent
        # verifier performs its own explicit finite check immediately beforehand.
        self._finite_complex_array(matrix, "finite-difference Hamiltonian")
        values = np.asarray(
            eigh(
                matrix,
                subset_by_index=(0, bands - 1),
                eigvals_only=True,
                check_finite=False,
            ),
            dtype=np.float64,
        )
        self._finite_real_array(values, "finite-difference eigenvalues")
        return values

    def _cosine_band_mesh(
        self, strength: float, cutoff: int, mesh_size: int, band_count: int
    ) -> tuple[RealVector, RealMatrix, npt.NDArray[np.complex128]]:
        """Return centered reciprocal coordinates, energies, and row states.

        Parameters
        ----------
        strength
            Cosine amplitude in normalized :math:`E_G` units.
        cutoff
            Symmetric reciprocal-index cutoff.
        mesh_size
            Number of points in the centered half-open reciprocal mesh.
        band_count
            Number of increasing bands and eigenstates to retain.

        Returns
        -------
        tuple
            Reciprocal coordinates with shape ``(mesh_size,)``, energies with shape
            ``(mesh_size, band_count)``, and row-state coefficients with shape
            ``(mesh_size, band_count, 2*cutoff+1)``.
        """
        coordinates = -0.5 + np.arange(mesh_size, dtype=np.float64) / mesh_size
        energies = np.empty((mesh_size, band_count), dtype=np.float64)
        states = np.empty((mesh_size, band_count, 2 * cutoff + 1), dtype=np.complex128)
        for index, momentum in enumerate(coordinates):
            values, vectors = self._cosine_eigensystem(
                float(momentum), strength, cutoff
            )
            energies[index] = values[:band_count]
            states[index] = vectors[:, :band_count].T
        self._finite_real_array(coordinates, "reciprocal coordinates")
        self._finite_real_array(energies, "band-mesh energies")
        self._finite_complex_array(states, "band-mesh states")
        return coordinates, energies, states

    def _minimum_band_gaps(self, energies: RealMatrix) -> RealVector:
        """Return each sampled band's minimum gap to an included neighbor.

        Parameters
        ----------
        energies
            Binary64 array with reciprocal samples by increasing band index.

        Returns
        -------
        numpy.ndarray
            One minimum nonnegative adjacent-band gap per included band.
        """
        band_count = energies.shape[1]
        gaps = np.empty(band_count, dtype=np.float64)
        for band_index in range(band_count):
            candidates: list[float] = []
            if band_index > 0:
                candidates.append(
                    float(np.min(energies[:, band_index] - energies[:, band_index - 1]))
                )
            if band_index + 1 < band_count:
                candidates.append(
                    float(np.min(energies[:, band_index + 1] - energies[:, band_index]))
                )
            gaps[band_index] = min(candidates)
        self._finite_real_array(gaps, "minimum adjacent gaps")
        return gaps

    def _minimum_sewn_overlap(self, states: ComplexMatrix) -> float:
        """Return the minimum neighbor overlap including reciprocal sewing.

        Parameters
        ----------
        states
            Ordered normalized row states on a half-open reciprocal mesh.

        Returns
        -------
        float
            Minimum absolute overlap across ordinary neighbors and the sewn closure,
            where the first state is shifted by one reciprocal basis index.
        """
        values = [
            abs(np.vdot(states[index], states[index + 1]))
            for index in range(states.shape[0] - 1)
        ]
        sewn_first = np.zeros_like(states[0])
        sewn_first[:-1] = states[0][1:]
        values.append(abs(np.vdot(states[-1], sewn_first)))
        return self._finite_scalar(min(values), "minimum sewn overlap")

    def _parallel_transport(
        self, input_states: ComplexMatrix
    ) -> tuple[ComplexMatrix, float]:
        """Return deterministic scalar parallel transport and closure holonomy.

        Parameters
        ----------
        input_states
            Ordered normalized complex row states on the half-open reciprocal mesh.

        Returns
        -------
        tuple
            Periodic-gauge transported row states and principal closure phase in
            radians.

        Raises
        ------
        ValueError
            If an ordinary or sewn closure overlap has magnitude at most ``1e-14``.
        """
        states = input_states.copy()
        for index in range(states.shape[0] - 1):
            overlap = np.vdot(states[index], states[index + 1])
            if abs(overlap) <= 1.0e-14:
                raise ValueError("parallel transport encountered a vanishing overlap")
            states[index + 1] *= np.exp(-1j * np.angle(overlap))
        sewn_first = np.zeros_like(states[0])
        sewn_first[:-1] = states[0][1:]
        closure = np.vdot(states[-1], sewn_first)
        if abs(closure) <= 1.0e-14:
            raise ValueError("parallel transport closure overlap vanished")
        holonomy = float(np.angle(closure))
        phases = np.exp(
            1j
            * holonomy
            * np.arange(states.shape[0], dtype=np.float64)
            / states.shape[0]
        )
        states *= phases[:, None]
        self._finite_complex_array(states, "parallel-transport states")
        return states, self._finite_scalar(holonomy, "closure holonomy")

    def _direct_hoppings(
        self,
        energies: RealVector,
        coordinates: RealVector,
        representatives: npt.NDArray[np.int64],
        period: float,
    ) -> ComplexVector:
        """Return direct complete scalar finite-Fourier coefficients.

        Parameters
        ----------
        energies, coordinates
            Ordered scalar-band energies and reduced reciprocal coordinates.
        representatives
            Ordered centered integer cell representatives.
        period
            Direct-cell period used in the Fourier phase.

        Returns
        -------
        numpy.ndarray
            Complex hopping coefficients in representative order.
        """
        phase = np.exp(-1j * np.outer(representatives * period, coordinates))
        result = np.asarray(phase @ energies / coordinates.size, dtype=np.complex128)
        self._finite_complex_array(result, "complete hopping coefficients")
        return result

    def _reconstruct(
        self,
        hoppings: ComplexVector,
        coordinates: RealVector,
        representatives: npt.NDArray[np.int64],
        period: float,
    ) -> ComplexVector:
        """Return direct inverse finite-Fourier reconstruction.

        Parameters
        ----------
        hoppings
            Ordered complex scalar hopping coefficients.
        coordinates
            Reduced reciprocal coordinates for reconstruction.
        representatives
            Cell representatives paired with ``hoppings``.
        period
            Direct-cell period used in the inverse phase.

        Returns
        -------
        numpy.ndarray
            Complex reconstructed values in coordinate order.
        """
        design = np.exp(1j * np.outer(coordinates, representatives * period))
        result = np.asarray(design @ hoppings, dtype=np.complex128)
        self._finite_complex_array(result, "Fourier reconstruction")
        return result
