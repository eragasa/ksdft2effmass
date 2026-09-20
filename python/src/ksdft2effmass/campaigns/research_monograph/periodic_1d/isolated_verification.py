"""Independent numerical verification of retained Appendix G isolated-band results.

This verifier reconstructs the parent plane-wave, finite-difference, Mathieu,
symmetry, weak-gap, complete hopping, finite-range, withheld-mesh, Parseval, direct-fit,
and parent-observable channels directly from the correlated input controls.  It uses
NumPy and SciPy reference functions without importing production periodic model,
operator-construction, hopping-transform, fitting, or diagnostic algorithms.

The retained transported frames and localization density samples are unavailable, so
their overlap, holonomy, center, spread, and density identity cannot be independently
reconstructed.  Those exclusions are explicit and never contribute to ``passes``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

import numpy as np
import numpy.typing as npt
from scipy.special import mathieu_a, mathieu_b  # type: ignore[import-untyped]

from ksdft2effmass.operators import ScalarQuantity, Unitless

from .isolated import Periodic1DIsolatedBandCampaignDefinition
from .isolated_results import (
    Periodic1DHoppingRangeDiagnostic,
    Periodic1DIsolatedBandCampaignResult,
)
from .workflows import Periodic1DIsolatedBandCampaignWorkflowResult

type ComplexMatrix = npt.NDArray[np.complex128]
type ComplexVector = npt.NDArray[np.complex128]
type RealMatrix = npt.NDArray[np.float64]
type RealVector = npt.NDArray[np.float64]
type IntegerVector = npt.NDArray[np.int64]


class Periodic1DIsolatedUnavailableVerificationChannel(StrEnum):
    """Identify isolated-band channels lacking their required source arrays."""

    GAUGE_TRANSPORT_AND_OVERLAPS = "gauge_transport_and_overlaps"
    WANNIER_LOCALIZATION_PROFILE = "wannier_localization_profile"


@dataclass(frozen=True, slots=True)
class Periodic1DIsolatedVerificationRequest:
    """Provide a correlated isolated campaign and unitless absolute tolerance.

    Parameters
    ----------
    correlated_campaign
        Read-only Workflow result with exact input/result and provenance correlation.
    absolute_tolerance
        Inclusive absolute tolerance in normalized recoil-energy units :math:`E_G`.
    curvature_absolute_tolerance
        Separate tolerance for the finite-difference zone-center curvature diagnostic,
        whose subtraction is scaled by a squared ``1e-3`` momentum step.
    """

    correlated_campaign: Periodic1DIsolatedBandCampaignWorkflowResult
    absolute_tolerance: ScalarQuantity
    curvature_absolute_tolerance: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate exact request ownership and a nonnegative unitless tolerance."""
        if (
            type(self.correlated_campaign)
            is not Periodic1DIsolatedBandCampaignWorkflowResult
        ):
            raise TypeError(
                "correlated_campaign must be the isolated campaign Workflow result"
            )
        for name, value in (
            ("absolute_tolerance", self.absolute_tolerance),
            ("curvature_absolute_tolerance", self.curvature_absolute_tolerance),
        ):
            if type(value) is not ScalarQuantity:
                raise TypeError(f"{name} must be ScalarQuantity")
            if not isinstance(value.unit, Unitless):
                raise ValueError(f"{name} must use Unitless")
            if value.magnitude < 0.0:
                raise ValueError(f"{name} must be nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DIsolatedVerificationResult:
    """Retain independent isolated-band reconstruction diagnostics.

    Parameters
    ----------
    parent_maximum_reported_absolute_defect
        Maximum difference between independently recomputed and retained parent
        verification diagnostics.
    lowest_band_maximum_absolute_defect
        Maximum difference between independently assembled plane-wave lowest-band
        energies and the retained reciprocal path.
    hopping_transform_maximum_absolute_defect
        Maximum entry defect between the direct finite Fourier sum and retained
        complete hopping coefficients.
    inverse_reconstruction_maximum_absolute_error
        Maximum absolute complex reconstruction error on the complete training mesh.
    reduction_maximum_reported_absolute_defect
        Maximum discrepancy in retained reconstruction and imaginary-part summaries.
    range_study_maximum_reported_absolute_defect
        Maximum discrepancy across all reconstructable finite-range study fields.
    parent_observable_maximum_reported_absolute_defect
        Maximum discrepancy in bandwidth and zone-boundary gap.
    zone_center_curvature_reported_absolute_defect
        Discrepancy in the cancellation-sensitive finite-difference center curvature.
    unavailable_channels
        Exact channels whose source frame or density arrays were not retained.
    absolute_tolerance
        Inclusive unitless :math:`E_G` tolerance for ordinary diagnostics.
    curvature_absolute_tolerance
        Separate inclusive tolerance for zone-center curvature.
    passes
        Aggregate bounded numerical-verification disposition.
    """

    parent_maximum_reported_absolute_defect: ScalarQuantity
    lowest_band_maximum_absolute_defect: ScalarQuantity
    hopping_transform_maximum_absolute_defect: ScalarQuantity
    inverse_reconstruction_maximum_absolute_error: ScalarQuantity
    reduction_maximum_reported_absolute_defect: ScalarQuantity
    range_study_maximum_reported_absolute_defect: ScalarQuantity
    parent_observable_maximum_reported_absolute_defect: ScalarQuantity
    zone_center_curvature_reported_absolute_defect: ScalarQuantity
    unavailable_channels: tuple[Periodic1DIsolatedUnavailableVerificationChannel, ...]
    absolute_tolerance: ScalarQuantity
    curvature_absolute_tolerance: ScalarQuantity
    passes: bool

    def __post_init__(self) -> None:
        """Validate unitless diagnostics, unavailable inventory, and disposition."""
        diagnostics = (
            self.parent_maximum_reported_absolute_defect,
            self.lowest_band_maximum_absolute_defect,
            self.hopping_transform_maximum_absolute_defect,
            self.inverse_reconstruction_maximum_absolute_error,
            self.reduction_maximum_reported_absolute_defect,
            self.range_study_maximum_reported_absolute_defect,
            self.parent_observable_maximum_reported_absolute_defect,
            self.zone_center_curvature_reported_absolute_defect,
            self.absolute_tolerance,
            self.curvature_absolute_tolerance,
        )
        if any(type(value) is not ScalarQuantity for value in diagnostics):
            raise TypeError("verification diagnostics must be ScalarQuantity values")
        if any(not isinstance(value.unit, Unitless) for value in diagnostics):
            raise ValueError("verification diagnostics must use Unitless")
        if any(value.magnitude < 0.0 for value in diagnostics):
            raise ValueError("verification diagnostics must be nonnegative")
        if (
            not isinstance(self.unavailable_channels, tuple)
            or not self.unavailable_channels
            or any(
                type(channel) is not Periodic1DIsolatedUnavailableVerificationChannel
                for channel in self.unavailable_channels
            )
        ):
            raise TypeError("unavailable_channels must be a nonempty typed tuple")
        if len(set(self.unavailable_channels)) != len(self.unavailable_channels):
            raise ValueError("unavailable_channels must be unique")
        if type(self.passes) is not bool:
            raise TypeError("passes must be a built-in bool")
        ordinary = diagnostics[:-3]
        expected = all(
            value.magnitude <= self.absolute_tolerance.magnitude for value in ordinary
        ) and (
            self.zone_center_curvature_reported_absolute_defect.magnitude
            <= self.curvature_absolute_tolerance.magnitude
        )
        if self.passes is not expected:
            raise ValueError("passes must match diagnostics and tolerances")


class Periodic1DIsolatedResultVerifier:
    """Independently reconstruct retained isolated-band numerical channels."""

    __slots__ = ()

    unavailable_channels = (
        Periodic1DIsolatedUnavailableVerificationChannel.GAUGE_TRANSPORT_AND_OVERLAPS,
        Periodic1DIsolatedUnavailableVerificationChannel.WANNIER_LOCALIZATION_PROFILE,
    )

    def execute(
        self, request: Periodic1DIsolatedVerificationRequest
    ) -> Periodic1DIsolatedVerificationResult:
        """Reconstruct every channel supported by retained values and controls.

        Parameters
        ----------
        request
            Correlated campaign records and explicit numerical tolerance.

        Returns
        -------
        Periodic1DIsolatedVerificationResult
            Independent diagnostics, exclusions, and aggregate disposition.
        """
        if type(request) is not Periodic1DIsolatedVerificationRequest:
            raise TypeError("request must be Periodic1DIsolatedVerificationRequest")
        correlated = request.correlated_campaign
        definition = correlated.definition
        result = correlated.campaign_result
        parent_defect = self.parent_report_defect(definition, result)
        reduction = result.reduction
        coordinates = np.asarray(
            reduction.reciprocal_samples.coordinates.magnitude, dtype=np.float64
        )
        retained_energies = np.asarray(
            [
                matrix.magnitude[0, 0].real
                for matrix in reduction.reciprocal_samples.matrices
            ],
            dtype=np.float64,
        )
        cutoff = definition.plane_wave_cutoffs[-1]
        expected_energies = np.asarray(
            [
                self.plane_wave_energies(
                    float(momentum), definition.potential_strength.magnitude, cutoff
                )[0]
                for momentum in coordinates
            ],
            dtype=np.float64,
        )
        energy_defect = float(np.max(np.abs(retained_energies - expected_energies)))
        representatives = np.asarray(
            reduction.hopping_model.representatives, dtype=np.int64
        )
        hoppings = np.asarray(
            [block.magnitude[0, 0] for block in reduction.hopping_model.hopping_blocks],
            dtype=np.complex128,
        )
        direct_hoppings = self.direct_hoppings(
            expected_energies,
            coordinates,
            representatives,
            definition.lattice_period.magnitude,
        )
        transform_defect = float(np.max(np.abs(direct_hoppings - hoppings)))
        reconstructed = self.reconstruct(
            hoppings,
            coordinates,
            representatives,
            definition.lattice_period.magnitude,
        )
        inverse_error = float(np.max(np.abs(reconstructed - expected_energies)))
        reduction_defect = max(
            abs(
                float(np.max(np.abs(reconstructed.real - retained_energies)))
                - reduction.full_mesh_reconstruction_maximum_absolute_error
            ),
            abs(
                float(np.max(np.abs(reconstructed.imag)))
                - reduction.full_mesh_reconstruction_maximum_imaginary
            ),
            abs(
                float(np.max(np.abs(hoppings.imag)))
                - reduction.hopping_maximum_imaginary
            ),
        )
        range_defect = self.range_report_defect(
            definition,
            result,
            expected_energies,
            coordinates,
            representatives,
            hoppings,
        )
        observable_defect, curvature_defect = self.parent_observable_report_defects(
            definition, result
        )
        values = (
            parent_defect,
            energy_defect,
            transform_defect,
            inverse_error,
            reduction_defect,
            range_defect,
            observable_defect,
        )
        tolerance = request.absolute_tolerance.magnitude
        quantities = tuple(ScalarQuantity(value, Unitless()) for value in values)
        return Periodic1DIsolatedVerificationResult(
            parent_maximum_reported_absolute_defect=quantities[0],
            lowest_band_maximum_absolute_defect=quantities[1],
            hopping_transform_maximum_absolute_defect=quantities[2],
            inverse_reconstruction_maximum_absolute_error=quantities[3],
            reduction_maximum_reported_absolute_defect=quantities[4],
            range_study_maximum_reported_absolute_defect=quantities[5],
            parent_observable_maximum_reported_absolute_defect=quantities[6],
            zone_center_curvature_reported_absolute_defect=ScalarQuantity(
                curvature_defect, Unitless()
            ),
            unavailable_channels=self.unavailable_channels,
            absolute_tolerance=request.absolute_tolerance,
            curvature_absolute_tolerance=request.curvature_absolute_tolerance,
            passes=(
                all(value <= tolerance for value in values)
                and curvature_defect <= request.curvature_absolute_tolerance.magnitude
            ),
        )

    def plane_wave_energies(
        self, momentum: float, potential_strength: float, cutoff: int
    ) -> RealVector:
        """Return dense cosine-potential plane-wave eigenvalues in :math:`E_G`.

        Parameters
        ----------
        momentum, potential_strength
            Reduced reciprocal coordinate and normalized cosine amplitude.
        cutoff
            Positive symmetric plane-wave index cutoff.

        Returns
        -------
        numpy.ndarray
            Increasing binary64 eigenvalue vector.
        """
        indices = np.arange(-cutoff, cutoff + 1, dtype=np.float64)
        matrix = np.diag(np.square(momentum + indices))
        coupling = 0.5 * potential_strength
        matrix += np.diag(np.full(2 * cutoff, coupling), 1)
        matrix += np.diag(np.full(2 * cutoff, coupling), -1)
        return np.asarray(np.linalg.eigvalsh(matrix), dtype=np.float64)

    def finite_difference_energies(
        self,
        momentum: float,
        potential_strength: float,
        points: int,
        band_count: int,
        lattice_period: float,
    ) -> RealVector:
        """Return the lowest periodic second-difference fiber eigenvalues.

        Parameters
        ----------
        momentum, potential_strength
            Reduced reciprocal coordinate and normalized cosine amplitude.
        points
            Periodic real-space grid-point count.
        band_count
            Number of increasing eigenvalues to return.
        lattice_period
            Direct-lattice period in the dimensionless convention.

        Returns
        -------
        numpy.ndarray
            Lowest ``band_count`` binary64 eigenvalues.
        """
        spacing = lattice_period / points
        kinetic = 1.0 / spacing**2
        coordinates = spacing * np.arange(points, dtype=np.float64)
        matrix = np.diag(
            2.0 * kinetic + potential_strength * np.cos(coordinates)
        ).astype(np.complex128)
        off_diagonal = np.full(points - 1, -kinetic)
        matrix += np.diag(off_diagonal, 1) + np.diag(off_diagonal, -1)
        matrix[0, -1] = -kinetic * np.exp(-1j * momentum * lattice_period)
        matrix[-1, 0] = matrix[0, -1].conjugate()
        return np.asarray(np.linalg.eigvalsh(matrix)[:band_count], dtype=np.float64)

    def low_mode_operator_error(
        self,
        momentum: float,
        potential_strength: float,
        points: int,
        low_mode_cutoff: int,
        lattice_period: float,
    ) -> float:
        """Return the finite-difference versus plane-wave low-mode Frobenius error.

        Parameters
        ----------
        momentum, potential_strength
            Reduced reciprocal coordinate and normalized cosine amplitude.
        points
            Periodic finite-difference grid-point count.
        low_mode_cutoff
            Symmetric Fourier subspace cutoff used for both represented operators.
        lattice_period
            Direct-lattice period in the dimensionless convention.

        Returns
        -------
        float
            Absolute Frobenius defect in normalized :math:`E_G` units.
        """
        spacing = lattice_period / points
        kinetic = 1.0 / spacing**2
        coordinates = spacing * np.arange(points, dtype=np.float64)
        matrix = np.diag(
            2.0 * kinetic + potential_strength * np.cos(coordinates)
        ).astype(np.complex128)
        off_diagonal = np.full(points - 1, -kinetic)
        matrix += np.diag(off_diagonal, 1) + np.diag(off_diagonal, -1)
        matrix[0, -1] = -kinetic * np.exp(-1j * momentum * lattice_period)
        matrix[-1, 0] = matrix[0, -1].conjugate()
        indices = np.arange(-low_mode_cutoff, low_mode_cutoff + 1)
        transform = np.exp(
            1j * np.outer(coordinates, momentum + indices.astype(np.float64))
        ) / np.sqrt(points)
        transported = transform.conj().T @ matrix @ transform
        plane_wave = np.diag(np.square(momentum + indices)).astype(np.complex128)
        coupling = 0.5 * potential_strength
        plane_wave += np.diag(np.full(2 * low_mode_cutoff, coupling), 1)
        plane_wave += np.diag(np.full(2 * low_mode_cutoff, coupling), -1)
        return float(np.linalg.norm(transported - plane_wave))

    def parent_report_defect(
        self,
        definition: Periodic1DIsolatedBandCampaignDefinition,
        result: Periodic1DIsolatedBandCampaignResult,
    ) -> float:
        """Return the maximum independently recomputed parent diagnostic defect.

        Parameters
        ----------
        definition
            Exact parent discretization and reference controls.
        result
            Typed retained parent observations.

        Returns
        -------
        float
            Maximum retained-versus-recomputed absolute defect.
        """
        parent = result.parent_verification
        momenta = definition.parent_sample_momenta.magnitude
        potential = definition.potential_strength.magnitude
        band_count = definition.compared_band_count
        reference = np.asarray(
            [
                self.plane_wave_energies(
                    float(momentum), potential, definition.plane_wave_reference_cutoff
                )[:band_count]
                for momentum in momenta
            ],
            dtype=np.float64,
        )
        defects: list[float] = []
        for pw_record in parent.plane_wave_cutoff_study:
            values = np.asarray(
                [
                    self.plane_wave_energies(
                        float(momentum), potential, pw_record.cutoff
                    )[:band_count]
                    for momentum in momenta
                ],
                dtype=np.float64,
            )
            observed = float(np.max(np.abs(values - reference)))
            defects.append(abs(observed - pw_record.maximum_first_bands_absolute_error))
        for fd_record in parent.finite_difference_grid_study:
            values = np.asarray(
                [
                    self.finite_difference_energies(
                        float(momentum),
                        potential,
                        fd_record.interior_cell_points,
                        band_count,
                        definition.lattice_period.magnitude,
                    )
                    for momentum in momenta
                ],
                dtype=np.float64,
            )
            observed = float(np.max(np.abs(values - reference)))
            defects.extend(
                (
                    abs(observed - fd_record.maximum_first_bands_absolute_error),
                    abs(
                        1.0 / fd_record.interior_cell_points
                        - fd_record.grid_spacing_over_period
                    ),
                )
            )
        for low_record in parent.common_low_mode_operator_study:
            observed = max(
                self.low_mode_operator_error(
                    float(momentum),
                    potential,
                    low_record.interior_cell_points,
                    low_record.low_mode_cutoff,
                    definition.lattice_period.magnitude,
                )
                for momentum in momenta
            )
            defects.append(
                abs(observed - low_record.maximum_low_mode_operator_frobenius_error)
            )
        defects.extend(self.symmetry_and_reference_defects(definition, result))
        return max(defects)

    def symmetry_and_reference_defects(
        self,
        definition: Periodic1DIsolatedBandCampaignDefinition,
        result: Periodic1DIsolatedBandCampaignResult,
    ) -> tuple[float, ...]:
        """Recompute symmetry, Mathieu, and weak-potential reference diagnostics.

        Parameters
        ----------
        definition
            Exact potential, basis, and comparison controls.
        result
            Typed retained parent observations.

        Returns
        -------
        tuple
            Absolute retained-versus-recomputed defects for every reference channel.
        """
        parent = result.parent_verification
        potential = definition.potential_strength.magnitude
        cutoff = definition.plane_wave_cutoffs[-1]
        band_count = definition.compared_band_count
        symmetry_mesh = np.linspace(-0.5, 0.5, 41)
        positive = np.asarray(
            [
                self.plane_wave_energies(float(momentum), potential, cutoff)[
                    :band_count
                ]
                for momentum in symmetry_mesh
            ]
        )
        reflected = np.asarray(
            [
                self.plane_wave_energies(float(-momentum), potential, cutoff)[
                    :band_count
                ]
                for momentum in symmetry_mesh
            ]
        )
        negative = np.asarray(
            [
                self.plane_wave_energies(float(momentum), -potential, cutoff)[
                    :band_count
                ]
                for momentum in symmetry_mesh
            ]
        )
        defects = [
            abs(
                float(np.max(np.abs(positive - reflected)))
                - parent.inversion_maximum_absolute_energy
            ),
            abs(
                float(np.max(np.abs(positive - negative)))
                - parent.potential_sign_translation_maximum_absolute_energy
            ),
        ]
        q = 2.0 * potential
        center = float(mathieu_a(0, q) / 4.0)
        boundary = np.sort(
            np.asarray([mathieu_a(1, q), mathieu_b(1, q)], dtype=np.float64) / 4.0
        )
        reference_cutoff = definition.plane_wave_reference_cutoff
        center_pw = self.plane_wave_energies(0.0, potential, reference_cutoff)[0]
        boundary_pw = self.plane_wave_energies(0.5, potential, reference_cutoff)[:2]
        defects.extend(
            (
                abs(center - parent.mathieu_zone_center_lowest),
                float(
                    np.max(
                        np.abs(
                            boundary
                            - np.asarray(parent.mathieu_zone_boundary_lowest_two)
                        )
                    )
                ),
                abs(
                    abs(center_pw - center)
                    - parent.mathieu_plane_wave_zone_center_absolute_error
                ),
                abs(
                    float(np.max(np.abs(boundary_pw - boundary)))
                    - parent.mathieu_plane_wave_zone_boundary_maximum_absolute_error
                ),
            )
        )
        if parent.mathieu_q_convention != "q=2*V0/E_G and E/E_G=A/4":
            raise ValueError("unsupported retained Mathieu convention")
        for record in parent.weak_potential_gap_study:
            values = self.plane_wave_energies(
                0.5, record.potential_strength, reference_cutoff
            )
            gap = float(values[1] - values[0])
            relative = abs(gap - record.potential_strength) / record.potential_strength
            defects.extend(
                (
                    abs(gap - record.zone_boundary_gap),
                    abs(record.leading_perturbative_gap - record.potential_strength),
                    abs(relative - record.relative_deviation_from_leading_gap),
                )
            )
        return tuple(defects)

    def direct_hoppings(
        self,
        energies: RealVector,
        coordinates: RealVector,
        representatives: IntegerVector,
        lattice_period: float,
    ) -> ComplexVector:
        """Return direct finite Fourier coefficients for one scalar band.

        Parameters
        ----------
        energies, coordinates
            Ordered scalar band values and reduced reciprocal coordinates.
        representatives
            Ordered integer cell representatives.
        lattice_period
            Direct-lattice period used in the phase convention.

        Returns
        -------
        numpy.ndarray
            Ordered complete complex hopping coefficients.
        """
        transform = (
            np.exp(-1j * np.outer(representatives * lattice_period, coordinates))
            / coordinates.size
        )
        return np.asarray(transform @ energies, dtype=np.complex128)

    def reconstruct(
        self,
        hoppings: ComplexVector,
        coordinates: RealVector,
        representatives: IntegerVector,
        lattice_period: float,
    ) -> ComplexVector:
        """Return the scalar band reconstructed by the direct inverse finite sum.

        Parameters
        ----------
        hoppings
            Ordered complex hopping coefficients.
        coordinates
            Reduced reciprocal coordinates for reconstruction.
        representatives
            Integer cell representative corresponding to each coefficient.
        lattice_period
            Direct-lattice period used in the phase convention.

        Returns
        -------
        numpy.ndarray
            Complex reconstructed scalar-band values.
        """
        design = np.exp(1j * np.outer(coordinates, representatives * lattice_period))
        return np.asarray(design @ hoppings, dtype=np.complex128)

    def range_report_defect(
        self,
        definition: Periodic1DIsolatedBandCampaignDefinition,
        result: Periodic1DIsolatedBandCampaignResult,
        energies: RealVector,
        coordinates: RealVector,
        representatives: IntegerVector,
        hoppings: ComplexVector,
    ) -> float:
        """Return the maximum reconstructed finite-range study field defect.

        Parameters
        ----------
        definition, result
            Exact campaign controls and typed retained outcomes.
        energies, coordinates
            Independently reconstructed training band and reciprocal mesh.
        representatives, hoppings
            Complete centered cell representatives and coefficients.

        Returns
        -------
        float
            Maximum defect across every retained finite-range field.
        """
        withheld_coordinates = np.linspace(-0.5, 0.5, definition.withheld_mesh_size)
        cutoff = definition.plane_wave_cutoffs[-1]
        potential = definition.potential_strength.magnitude
        withheld_parent = np.asarray(
            [
                self.plane_wave_energies(float(momentum), potential, cutoff)[0]
                for momentum in withheld_coordinates
            ],
            dtype=np.float64,
        )
        defects: list[float] = []
        for record in result.reduction.hopping_range_study:
            defects.extend(
                self.one_range_defects(
                    record,
                    energies,
                    coordinates,
                    withheld_coordinates,
                    withheld_parent,
                    representatives,
                    hoppings,
                    definition.lattice_period.magnitude,
                )
            )
        return max(defects)

    def one_range_defects(
        self,
        record: Periodic1DHoppingRangeDiagnostic,
        energies: RealVector,
        coordinates: RealVector,
        withheld_coordinates: RealVector,
        withheld_parent: RealVector,
        representatives: IntegerVector,
        hoppings: ComplexVector,
        lattice_period: float,
    ) -> tuple[float, ...]:
        """Recompute every retained scalar metric for one hopping range.

        Parameters
        ----------
        record
            Typed retained finite-range diagnostics.
        energies, coordinates
            Training target and reciprocal coordinates.
        withheld_coordinates, withheld_parent
            Independent withheld mesh and parent target.
        representatives, hoppings
            Complete centered cell representatives and coefficients.
        lattice_period
            Direct-lattice period used by the phase convention.

        Returns
        -------
        tuple
            Absolute retained-versus-recomputed defects for all record fields.
        """
        mask = np.abs(representatives) <= record.hopping_range_cells
        kept_representatives = representatives[mask]
        kept_hoppings = hoppings[mask]
        training = self.reconstruct(
            kept_hoppings, coordinates, kept_representatives, lattice_period
        )
        withheld = self.reconstruct(
            kept_hoppings,
            withheld_coordinates,
            kept_representatives,
            lattice_period,
        )
        training_residual = energies - training.real
        withheld_residual = withheld_parent - withheld.real
        omitted = float(np.linalg.norm(hoppings[~mask]))
        training_rms = float(np.sqrt(np.mean(np.square(training_residual))))
        withheld_rms = float(np.sqrt(np.mean(np.square(withheld_residual))))
        training_max = float(np.max(np.abs(training_residual)))
        withheld_max = float(np.max(np.abs(withheld_residual)))
        parseval = abs(
            float(np.sum(np.square(training_residual))) - coordinates.size * omitted**2
        )
        design = np.exp(
            1j * np.outer(coordinates, kept_representatives * lattice_period)
        )
        direct = np.linalg.lstsq(design, energies, rcond=None)[0]
        direct_training = design @ direct
        coefficient_defect = float(np.linalg.norm(direct - kept_hoppings))
        training_route_defect = float(np.linalg.norm(direct_training - training))
        bandwidth_error = abs(
            float(np.ptp(withheld.real)) - float(np.ptp(withheld_parent))
        )
        curvature = float(
            -np.sum(
                np.square(kept_representatives * lattice_period) * kept_hoppings
            ).real
        )
        return (
            abs(int(np.count_nonzero(mask)) - record.retained_coefficient_count),
            abs(omitted - record.omitted_hopping_l2_norm),
            abs(training_max - record.training_maximum_absolute_error),
            abs(training_rms - record.training_root_mean_square_error),
            abs(withheld_max - record.withheld_maximum_absolute_error),
            abs(withheld_rms - record.withheld_root_mean_square_error),
            abs(bandwidth_error - record.bandwidth_error),
            abs(curvature - record.zone_center_curvature),
            abs(coefficient_defect - record.direct_mediated_coefficient_l2_defect),
            abs(training_route_defect - record.direct_mediated_training_l2_defect),
            abs(parseval - record.parseval_absolute_residual),
        )

    def parent_observable_report_defects(
        self,
        definition: Periodic1DIsolatedBandCampaignDefinition,
        result: Periodic1DIsolatedBandCampaignResult,
    ) -> tuple[float, float]:
        """Recompute ordinary parent observables and center curvature separately.

        Parameters
        ----------
        definition
            Exact potential, basis, and withheld-mesh controls.
        result
            Typed retained parent observables.

        Returns
        -------
        tuple
            Maximum bandwidth/gap defect followed by the separately scaled curvature
            defect.
        """
        cutoff = definition.plane_wave_cutoffs[-1]
        potential = definition.potential_strength.magnitude
        withheld_coordinates = np.linspace(-0.5, 0.5, definition.withheld_mesh_size)
        withheld = np.asarray(
            [
                self.plane_wave_energies(float(momentum), potential, cutoff)[0]
                for momentum in withheld_coordinates
            ]
        )
        boundary = self.plane_wave_energies(0.5, potential, cutoff)
        step = 1.0e-3
        center = np.asarray(
            [
                self.plane_wave_energies(momentum, potential, cutoff)[0]
                for momentum in (-step, 0.0, step)
            ]
        )
        curvature = float((center[0] - 2.0 * center[1] + center[2]) / step**2)
        retained = result.reduction.parent_observables
        return (
            max(
                abs(float(np.ptp(withheld)) - retained.bandwidth),
                abs(float(boundary[1] - boundary[0]) - retained.zone_boundary_gap),
            ),
            abs(curvature - retained.zone_center_curvature),
        )
