r"""Independent numerical verification of retained Appendix G stress results.

The verifier reconstructs every retained stress channel directly from the correlated
version-one controls using NumPy and SciPy primitives. Plane-wave and periodic
second-difference matrices act in the dimensionless convention :math:`a=2\pi`,
:math:`G=1`, and :math:`E_G=1`. Complete scalar hopping coefficients use the direct
finite sum

.. math::

   t_R=N_k^{-1}\sum_j e^{-i k_j R}E(k_j),

and fitting routes solve their stated complex least-squares problems without normal
equations. Scalar parallel transport includes the reciprocal sewing shift of the
finite plane-wave basis and rejects overlaps no larger than ``1e-14``.

The implementation does not import the historical runner or production plane-wave,
finite-difference, frame-transport, hopping-transform, or fitting algorithms. The
result is numerical verification of the represented dimensionless cosine-model stress
campaign, not material validation or uncertainty quantification.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
from scipy.linalg import eigh  # type: ignore[import-untyped]

from ksdft2effmass.operators import ScalarQuantity, Unitless

from .stress import Periodic1DStressCampaignDefinition, Periodic1DStressPotentialShape
from .stress_results import Periodic1DStressCampaignResult
from .workflows import Periodic1DStressCampaignWorkflowResult

type ComplexMatrix = npt.NDArray[np.complex128]
type ComplexVector = npt.NDArray[np.complex128]
type RealMatrix = npt.NDArray[np.float64]
type RealVector = npt.NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class Periodic1DStressVerificationRequest:
    """Provide a correlated stress campaign and stable-scalar tolerance.

    Parameters
    ----------
    correlated_campaign
        Read-only input/result correlation with exact retained byte identities.
    absolute_tolerance
        Inclusive ``Unitless`` tolerance applied numerically to stable reconstructed
        diagnostics. Energy residuals already use normalized :math:`E_G=1` values.
        Isolated single-band overlaps use the larger of this value and twice the
        square root of binary64 epsilon because eigenvector directions are
        conditioning-sensitive near the accepted isolation boundary.
    """

    correlated_campaign: Periodic1DStressCampaignWorkflowResult
    absolute_tolerance: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate exact correlation ownership and nonnegative unitless tolerance."""
        if type(self.correlated_campaign) is not Periodic1DStressCampaignWorkflowResult:
            raise TypeError(
                "correlated_campaign must be Periodic1DStressCampaignWorkflowResult"
            )
        if type(self.absolute_tolerance) is not ScalarQuantity:
            raise TypeError("absolute_tolerance must be ScalarQuantity")
        if not isinstance(self.absolute_tolerance.unit, Unitless):
            raise ValueError("absolute_tolerance must use Unitless")
        if self.absolute_tolerance.magnitude < 0.0:
            raise ValueError("absolute_tolerance must be nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DStressVerificationResult:
    """Retain independent defects for every stress-result channel.

    Parameters
    ----------
    potential_amplitude_maximum_absolute_defect
        Maximum defect across amplitude gaps, statuses, sign covariance, and both
        discretization studies.
    potential_shape_maximum_absolute_defect
        Maximum defect across shape spectra, adjacent gaps, finite-difference errors,
        time reversal, translation, and constant shifts.
    mesh_band_isolation_maximum_absolute_defect
        Maximum defect across every mesh, band, amplitude, isolation,
        complete-reconstruction, and withheld-range record.
    isolated_overlap_maximum_absolute_defect
        Maximum single-band sewn-overlap defect among records whose isolation
        disposition is true.
    gauge_covariance_maximum_absolute_defect
        Maximum defect across deterministic phase-gauge projector, transported-frame,
        and closure-holonomy diagnostics.
    route_assumption_maximum_absolute_defect
        Maximum defect across complete, weighted, and incomplete fitting routes in
        coefficient and comparison spaces.
    unavailable_nonisolated_overlap_count
        Number of single-band overlap records excluded because their retained
        isolation disposition is false.  Such eigenvectors are not uniquely defined.
    isolated_overlap_absolute_tolerance
        Inclusive binary64 eigenvector tolerance applied to isolated sewn overlaps.
    absolute_tolerance
        Inclusive unitless tolerance applied separately to the five stable channel
        maxima other than the separately conditioned overlap channel.
    passes
        Aggregate bounded numerical-verification disposition.
    """

    potential_amplitude_maximum_absolute_defect: ScalarQuantity
    potential_shape_maximum_absolute_defect: ScalarQuantity
    mesh_band_isolation_maximum_absolute_defect: ScalarQuantity
    isolated_overlap_maximum_absolute_defect: ScalarQuantity
    gauge_covariance_maximum_absolute_defect: ScalarQuantity
    route_assumption_maximum_absolute_defect: ScalarQuantity
    unavailable_nonisolated_overlap_count: int
    isolated_overlap_absolute_tolerance: ScalarQuantity
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
        values = (
            *defects,
            self.isolated_overlap_maximum_absolute_defect,
            self.isolated_overlap_absolute_tolerance,
            self.absolute_tolerance,
        )
        if any(type(value) is not ScalarQuantity for value in values):
            raise TypeError("stress verification values must be ScalarQuantity")
        if any(not isinstance(value.unit, Unitless) for value in values):
            raise ValueError("stress verification values must use Unitless")
        if any(value.magnitude < 0.0 for value in values):
            raise ValueError("stress verification values must be nonnegative")
        if (
            type(self.unavailable_nonisolated_overlap_count) is not int
            or self.unavailable_nonisolated_overlap_count < 0
        ):
            raise ValueError(
                "unavailable_nonisolated_overlap_count must be a nonnegative integer"
            )
        if type(self.passes) is not bool:
            raise TypeError("passes must be a built-in bool")
        expected = all(
            defect.magnitude <= self.absolute_tolerance.magnitude for defect in defects
        ) and (
            self.isolated_overlap_maximum_absolute_defect.magnitude
            <= self.isolated_overlap_absolute_tolerance.magnitude
        )
        if self.passes is not expected:
            raise ValueError("passes must match all channel defects and tolerance")


class Periodic1DStressResultVerifier:
    """Independently reconstruct all retained periodic-1D stress diagnostics."""

    __slots__ = ()

    sample_momenta = (-0.5, -0.25, 0.0, 0.25, 0.5)

    def execute(
        self, request: Periodic1DStressVerificationRequest
    ) -> Periodic1DStressVerificationResult:
        """Reconstruct every typed stress channel and compare retained scalars.

        Parameters
        ----------
        request
            Correlated stress controls, outcomes, and explicit tolerance.

        Returns
        -------
        Periodic1DStressVerificationResult
            Five separate maximum defects and their aggregate disposition.
        """
        if type(request) is not Periodic1DStressVerificationRequest:
            raise TypeError("request must be Periodic1DStressVerificationRequest")
        correlated = request.correlated_campaign
        definition = correlated.definition
        result = correlated.campaign_result
        (
            mesh_defect,
            isolated_overlap_defect,
            unavailable_overlap_count,
        ) = self.mesh_band_isolation_defect(definition, result)
        defects = (
            self.potential_amplitude_defect(definition, result),
            self.potential_shape_defect(definition, result),
            mesh_defect,
            self.gauge_covariance_defect(definition, result),
            self.route_assumption_defect(definition, result),
        )
        quantities = tuple(ScalarQuantity(value, Unitless()) for value in defects)
        tolerance = request.absolute_tolerance.magnitude
        overlap_tolerance = max(
            tolerance, 2.0 * float(np.sqrt(np.finfo(np.float64).eps))
        )
        return Periodic1DStressVerificationResult(
            quantities[0],
            quantities[1],
            quantities[2],
            ScalarQuantity(isolated_overlap_defect, Unitless()),
            quantities[3],
            quantities[4],
            unavailable_overlap_count,
            ScalarQuantity(overlap_tolerance, Unitless()),
            request.absolute_tolerance,
            all(value <= tolerance for value in defects)
            and isolated_overlap_defect <= overlap_tolerance,
        )

    def potential_amplitude_defect(
        self,
        definition: Periodic1DStressCampaignDefinition,
        result: Periodic1DStressCampaignResult,
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
        for retained in result.potential_amplitude_stress:
            strength = retained.potential_strength
            reference = np.asarray(
                [
                    self.cosine_eigensystem(k, strength, reference_cutoff)[0][
                        :band_count
                    ]
                    for k in self.sample_momenta
                ],
                dtype=np.float64,
            )
            boundary = self.cosine_eigensystem(0.5, strength, reference_cutoff)[0]
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
                    self.cosine_eigensystem(
                        k, strength, definition.plane_wave_cutoffs[-1]
                    )[0][:band_count]
                    for k in self.sample_momenta
                ]
            )
            negative = np.asarray(
                [
                    self.cosine_eigensystem(
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
                        self.cosine_eigensystem(k, strength, observation.resolution)[0][
                            :band_count
                        ]
                        for k in self.sample_momenta
                    ]
                )
                observed = float(np.max(np.abs(values - reference)))
                defects.append(abs(observed - observation.maximum_low_band_error))
            for observation in retained.finite_difference_grid_study:
                values = np.asarray(
                    [
                        self.finite_difference_energies(
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
        return max(defects)

    def potential_shape_defect(
        self,
        definition: Periodic1DStressCampaignDefinition,
        result: Periodic1DStressCampaignResult,
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
            item.identifier: item for item in result.potential_shape_stress.cases
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
                    self.shape_eigensystem(
                        float(k), shape, definition.plane_wave_reference_cutoff
                    )[0][: definition.compared_band_count]
                    for k in mesh
                ],
                dtype=np.float64,
            )
            finite_difference = np.asarray(
                [
                    self.finite_difference_energies(
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
            gaps = self.minimum_band_gaps(reference)
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
        shape_stress = result.potential_shape_stress
        defects.extend(
            (
                abs(translation - shape_stress.translation_isospectral_maximum_error),
                abs(
                    constant_shift
                    - shape_stress.constant_shift_covariance_maximum_error
                ),
            )
        )
        return max(defects)

    def mesh_band_isolation_defect(
        self,
        definition: Periodic1DStressCampaignDefinition,
        result: Periodic1DStressCampaignResult,
    ) -> tuple[float, float, int]:
        """Return stable mesh and overlap defects plus unavailable-overlap count.

        Parameters
        ----------
        definition
            Exact amplitude, mesh, band, hopping-range, and withheld-mesh controls.
        result
            Typed retained mesh, isolation, overlap, and reconstruction outcomes.

        Returns
        -------
        tuple
            Maximum absolute numeric defect across dimensionless energy and
            reconstruction diagnostics, maximum applicable isolated-band overlap
            defect, and count of unavailable nonisolated single-band overlap channels.

        Raises
        ------
        ValueError
            If a retained isolation applicability flag disagrees with the recomputed
            adjacent-gap rule.
        """
        defects: list[float] = []
        isolated_overlap_defects: list[float] = []
        unavailable_overlap_count = 0
        lookup = {
            (item.potential_strength, item.mesh_size, item.band_index): item
            for item in result.mesh_band_and_isolation_stress
        }
        period = definition.period.magnitude
        withheld_coordinates = np.linspace(-0.5, 0.5, definition.withheld_mesh_size)
        required_bands = max(definition.stress_band_indices) + 2
        cutoff = definition.plane_wave_cutoffs[-1]
        for strength in definition.potential_strengths.magnitude:
            numeric_strength = float(strength)
            withheld = np.asarray(
                [
                    self.cosine_eigensystem(float(k), numeric_strength, cutoff)[0][
                        :required_bands
                    ]
                    for k in withheld_coordinates
                ]
            )
            for mesh_size in definition.reciprocal_mesh_sizes:
                coordinates, bands, states = self.cosine_band_mesh(
                    numeric_strength, cutoff, mesh_size, required_bands
                )
                gaps = self.minimum_band_gaps(bands)
                representatives = np.arange(
                    -mesh_size // 2, mesh_size // 2, dtype=np.int64
                )
                mask = np.abs(representatives) <= definition.hopping_range_cells
                for band_index in definition.stress_band_indices:
                    retained = lookup[(numeric_strength, mesh_size, band_index)]
                    energies = bands[:, band_index]
                    band_states = states[:, band_index, :]
                    minimum_overlap = self.minimum_sewn_overlap(band_states)
                    hoppings = self.direct_hoppings(
                        energies, coordinates, representatives, period
                    )
                    reconstruction = self.reconstruct(
                        hoppings, coordinates, representatives, period
                    )
                    withheld_model = self.reconstruct(
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
                    if applicable:
                        isolated_overlap_defects.append(
                            abs(
                                minimum_overlap - retained.minimum_sewn_neighbor_overlap
                            )
                        )
                    else:
                        unavailable_overlap_count += 1
        return (
            max(defects),
            max(isolated_overlap_defects),
            unavailable_overlap_count,
        )

    def gauge_covariance_defect(
        self,
        definition: Periodic1DStressCampaignDefinition,
        result: Periodic1DStressCampaignResult,
    ) -> float:
        """Return the maximum reconstructed deterministic gauge-channel defect.

        Parameters
        ----------
        definition
            Exact gauge-stress amplitude, cutoff, and reciprocal mesh.
        result
            Typed retained projector, transported-frame, and holonomy defects.

        Returns
        -------
        float
            Maximum absolute retained-versus-recomputed gauge diagnostic defect.
        """
        retained = result.gauge_covariance_stress
        _, _, all_states = self.cosine_band_mesh(
            definition.route_stress_potential_strength.magnitude,
            definition.plane_wave_cutoffs[-1],
            definition.route_stress_mesh_size,
            1,
        )
        states = all_states[:, 0, :]
        indices = np.arange(definition.route_stress_mesh_size, dtype=np.float64)
        phases = np.exp(1j * (0.7 * np.sin(indices) + 0.3 * np.cos(3.0 * indices)))
        transformed = states * phases[:, None]
        transported_a, holonomy_a = self.parallel_transport(states)
        transported_b, holonomy_b = self.parallel_transport(transformed)
        branch_shift = 2.0 * np.pi * round((holonomy_a - holonomy_b) / (2.0 * np.pi))
        transported_b *= np.exp(
            1j * branch_shift * indices[:, None] / definition.route_stress_mesh_size
        )
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
        return max(
            abs(
                projector_defect
                - retained.random_phase_projector_maximum_frobenius_defect
            ),
            abs(
                frame_defect - retained.parallel_transport_frame_maximum_aligned_defect
            ),
            abs(holonomy_defect - retained.closure_holonomy_difference_modulo_2pi),
        )

    def route_assumption_defect(
        self,
        definition: Periodic1DStressCampaignDefinition,
        result: Periodic1DStressCampaignResult,
    ) -> float:
        """Return the maximum reconstructed fitting-route channel defect.

        Parameters
        ----------
        definition
            Exact route-stress amplitude, mesh, hopping range, and period.
        result
            Typed complete, incomplete-training, and weighted-route outcomes.

        Returns
        -------
        float
            Maximum absolute defect across coefficient and 257-point comparison-space
            diagnostics.
        """
        retained = result.route_assumption_stress
        period = definition.period.magnitude
        mesh_size = definition.route_stress_mesh_size
        coordinates, bands, _ = self.cosine_band_mesh(
            definition.route_stress_potential_strength.magnitude,
            definition.plane_wave_cutoffs[-1],
            mesh_size,
            1,
        )
        energies = bands[:, 0]
        representatives = np.arange(-mesh_size // 2, mesh_size // 2, dtype=np.int64)
        hoppings = self.direct_hoppings(energies, coordinates, representatives, period)
        mask = np.abs(representatives) <= definition.route_stress_hopping_range_cells
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
        return max(
            abs(value - expected)
            for value, expected in zip(observed, retained_values, strict=True)
        )

    def cosine_eigensystem(
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
        values, vectors = np.linalg.eigh(matrix)
        return (
            np.asarray(values, dtype=np.float64),
            np.asarray(vectors, dtype=np.complex128),
        )

    def shape_eigensystem(
        self, momentum: float, shape: Periodic1DStressPotentialShape, cutoff: int
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
        values, vectors = np.linalg.eigh(matrix)
        return (
            np.asarray(values, dtype=np.float64),
            np.asarray(vectors, dtype=np.complex128),
        )

    def finite_difference_energies(
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
        return np.asarray(
            eigh(
                matrix,
                subset_by_index=(0, bands - 1),
                eigvals_only=True,
                check_finite=False,
            ),
            dtype=np.float64,
        )

    def cosine_band_mesh(
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
            values, vectors = self.cosine_eigensystem(float(momentum), strength, cutoff)
            energies[index] = values[:band_count]
            states[index] = vectors[:, :band_count].T
        return coordinates, energies, states

    def minimum_band_gaps(self, energies: RealMatrix) -> RealVector:
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
        return gaps

    def minimum_sewn_overlap(self, states: ComplexMatrix) -> float:
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
        return float(min(values))

    def parallel_transport(
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
        return states, holonomy

    def direct_hoppings(
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
        return np.asarray(phase @ energies / coordinates.size, dtype=np.complex128)

    def reconstruct(
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
        return np.asarray(design @ hoppings, dtype=np.complex128)
