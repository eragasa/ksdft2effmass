"""Independent numerical verification of calculated Appendix G composite bands.

The verifier consumes a complete execution-local calculation ResultObject and directly
reconstructs its finite plane-wave matrices, eigenspaces, polar transport, deterministic
gauge attacks, projected operators, Wilson phase multisets, complete Fourier pair,
truncation errors, and least-squares route with NumPy. It deliberately imports no
production model construction, frame transport, projection, hopping transform,
truncation, interpolation, fitting, gap, or band-error algorithm.

Passing is bounded numerical verification of the represented finite calculation. It is
not basis convergence, material validation, polarization or topology evidence,
uncertainty quantification, or human acceptance.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from ksdft2effmass.operators import ScalarQuantity, Unitless

from .composite_calculation import Periodic1DCompositeBandCalculationResult

type ComplexMatrix = npt.NDArray[np.complex128]
type ComplexArray3 = npt.NDArray[np.complex128]
type IntegerVector = npt.NDArray[np.int64]
type RealMatrix = npt.NDArray[np.float64]
type RealVector = npt.NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeBandCalculationVerificationRequest:
    """Provide one calculated result and an inclusive unitless tolerance."""

    calculation: Periodic1DCompositeBandCalculationResult
    absolute_tolerance: ScalarQuantity

    def __post_init__(self) -> None:
        """Require the exact calculation type and a nonnegative unitless tolerance."""

        if type(self.calculation) is not Periodic1DCompositeBandCalculationResult:
            raise TypeError(
                "calculation must be Periodic1DCompositeBandCalculationResult"
            )
        if type(self.absolute_tolerance) is not ScalarQuantity:
            raise TypeError("absolute_tolerance must be ScalarQuantity")
        if not isinstance(self.absolute_tolerance.unit, Unitless):
            raise ValueError("absolute_tolerance must use Unitless")
        if self.absolute_tolerance.magnitude < 0.0:
            raise ValueError("absolute_tolerance must be nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeBandGroupCalculationVerificationResult:
    """Retain independent maximum defects for one calculated composite group."""

    group_id: str
    source_projector_maximum_frobenius_defect: ScalarQuantity
    smooth_frame_maximum_frobenius_defect: ScalarQuantity
    spectral_diagnostic_maximum_absolute_defect: ScalarQuantity
    gauge_diagnostic_maximum_absolute_defect: ScalarQuantity
    smooth_operator_maximum_frobenius_defect: ScalarQuantity
    smooth_hopping_maximum_absolute_defect: ScalarQuantity
    rough_hopping_maximum_absolute_defect: ScalarQuantity
    transform_diagnostic_maximum_absolute_defect: ScalarQuantity
    range_diagnostic_maximum_absolute_defect: ScalarQuantity
    direct_route_maximum_absolute_defect: ScalarQuantity
    absolute_tolerance: ScalarQuantity
    passes: bool

    def __post_init__(self) -> None:
        """Validate nonnegative unitless defects and their derived disposition."""

        if type(self.group_id) is not str or not self.group_id:
            raise ValueError("group_id must be a nonempty built-in str")
        quantities = (
            self.source_projector_maximum_frobenius_defect,
            self.smooth_frame_maximum_frobenius_defect,
            self.spectral_diagnostic_maximum_absolute_defect,
            self.gauge_diagnostic_maximum_absolute_defect,
            self.smooth_operator_maximum_frobenius_defect,
            self.smooth_hopping_maximum_absolute_defect,
            self.rough_hopping_maximum_absolute_defect,
            self.transform_diagnostic_maximum_absolute_defect,
            self.range_diagnostic_maximum_absolute_defect,
            self.direct_route_maximum_absolute_defect,
            self.absolute_tolerance,
        )
        if any(type(quantity) is not ScalarQuantity for quantity in quantities):
            raise TypeError("verification defects must be ScalarQuantity")
        if any(not isinstance(quantity.unit, Unitless) for quantity in quantities):
            raise ValueError("verification defects must use Unitless")
        if any(quantity.magnitude < 0.0 for quantity in quantities):
            raise ValueError("verification defects must be nonnegative")
        if type(self.passes) is not bool:
            raise TypeError("passes must be a built-in bool")
        measured = quantities[:-1]
        expected = all(
            quantity.magnitude <= self.absolute_tolerance.magnitude
            for quantity in measured
        )
        if self.passes is not expected:
            raise ValueError("passes must be derived from every represented defect")


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeBandCalculationVerificationResult:
    """Retain independent parent and group verification for one calculation."""

    request: Periodic1DCompositeBandCalculationVerificationRequest
    parent_operator_maximum_absolute_defect: ScalarQuantity
    training_eigenvalue_maximum_absolute_defect: ScalarQuantity
    withheld_eigenvalue_maximum_absolute_defect: ScalarQuantity
    groups: tuple[Periodic1DCompositeBandGroupCalculationVerificationResult, ...]
    passes: bool

    def __post_init__(self) -> None:
        """Validate parent defects, complete group coverage, and disposition."""

        if (
            type(self.request)
            is not Periodic1DCompositeBandCalculationVerificationRequest
        ):
            raise TypeError(
                "request must be Periodic1DCompositeBandCalculationVerificationRequest"
            )
        parent_defects = (
            self.parent_operator_maximum_absolute_defect,
            self.training_eigenvalue_maximum_absolute_defect,
            self.withheld_eigenvalue_maximum_absolute_defect,
        )
        if any(type(quantity) is not ScalarQuantity for quantity in parent_defects):
            raise TypeError("parent defects must be ScalarQuantity")
        if any(not isinstance(quantity.unit, Unitless) for quantity in parent_defects):
            raise ValueError("parent defects must use Unitless")
        if any(quantity.magnitude < 0.0 for quantity in parent_defects):
            raise ValueError("parent defects must be nonnegative")
        if type(self.groups) is not tuple or not self.groups:
            raise TypeError("groups must be a nonempty built-in tuple")
        if any(
            type(group) is not Periodic1DCompositeBandGroupCalculationVerificationResult
            for group in self.groups
        ):
            raise TypeError("groups must contain group verification results")
        if type(self.passes) is not bool:
            raise TypeError("passes must be a built-in bool")
        tolerance = self.request.absolute_tolerance.magnitude
        expected = all(
            defect.magnitude <= tolerance for defect in parent_defects
        ) and all(group.passes for group in self.groups)
        if self.passes is not expected:
            raise ValueError("passes must be derived from parent and group defects")


class Periodic1DCompositeBandCalculationVerifier:
    """Independently reconstruct one execution-local composite calculation."""

    __slots__ = ()

    def execute(
        self,
        request: Periodic1DCompositeBandCalculationVerificationRequest,
    ) -> Periodic1DCompositeBandCalculationVerificationResult:
        """Reconstruct all represented finite channels with direct NumPy routes."""

        if type(request) is not Periodic1DCompositeBandCalculationVerificationRequest:
            raise TypeError(
                "request must be Periodic1DCompositeBandCalculationVerificationRequest"
            )
        calculation = request.calculation
        definition = calculation.request.definition
        tolerance = request.absolute_tolerance.magnitude
        unit = Unitless()
        required_bands = (
            max(group.upper_index for group in definition.retained_band_groups) + 2
        )

        def parent_samples(
            coordinates: RealVector,
        ) -> tuple[ComplexArray3, RealMatrix, ComplexArray3]:
            cutoff = definition.plane_wave_cutoff
            harmonics = np.arange(-cutoff, cutoff + 1, dtype=np.float64)
            coupling = definition.potential_strength_over_recoil.magnitude / 2.0
            matrices: list[ComplexMatrix] = []
            values: list[RealVector] = []
            vectors: list[ComplexMatrix] = []
            for coordinate in coordinates:
                matrix = np.diag((harmonics + coordinate) ** 2).astype(np.complex128)
                for index in range(harmonics.size - 1):
                    matrix[index, index + 1] = coupling
                    matrix[index + 1, index] = coupling
                eigenvalues, eigenvectors = np.linalg.eigh(matrix)
                matrices.append(matrix)
                values.append(
                    np.asarray(eigenvalues[:required_bands], dtype=np.float64)
                )
                vectors.append(
                    np.asarray(eigenvectors[:, :required_bands], dtype=np.complex128)
                )
            return (
                np.asarray(matrices, dtype=np.complex128),
                np.asarray(values, dtype=np.float64),
                np.asarray(vectors, dtype=np.complex128),
            )

        def smooth_transport(
            frames: ComplexArray3,
            sewing: ComplexMatrix,
        ) -> tuple[ComplexArray3, RealVector, RealVector]:
            transported = np.empty_like(frames)
            transported[0] = frames[0]
            minima: list[float] = []
            for index in range(1, frames.shape[0]):
                overlap = transported[index - 1].conj().T @ frames[index]
                left, singular_values, right = np.linalg.svd(overlap)
                transported[index] = frames[index] @ (left @ right).conj().T
                minima.extend(float(value) for value in singular_values)
            seam = transported[-1].conj().T @ sewing @ transported[0]
            left, singular_values, right = np.linalg.svd(seam)
            minima.extend(float(value) for value in singular_values)
            unitary_seam = left @ right
            eigenvalues, eigenvectors = np.linalg.eig(unitary_seam)
            phases = np.angle(eigenvalues).astype(np.float64)
            order = np.argsort(phases)
            phases = phases[order]
            eigenvectors = eigenvectors[:, order]
            count = transported.shape[0]
            for index in range(count):
                fraction = index / count
                root = (
                    eigenvectors
                    @ np.diag(np.exp(1j * phases * fraction))
                    @ np.linalg.inv(eigenvectors)
                )
                transported[index] = transported[index] @ root
            return transported, np.asarray(minima, dtype=np.float64), phases

        def controlled_gauge(frames: ComplexArray3) -> ComplexArray3:
            attacked = np.empty_like(frames)
            count = frames.shape[0]
            amplitude = definition.controlled_gauge_amplitude.magnitude
            for index in range(count):
                coordinate = index / count
                angle = amplitude * np.sin(2.0 * np.pi * coordinate)
                rotation = np.asarray(
                    [
                        [np.cos(angle), -np.sin(angle)],
                        [np.sin(angle), np.cos(angle)],
                    ],
                    dtype=np.complex128,
                )
                phases = np.diag(
                    np.exp(
                        1j
                        * np.asarray(
                            [
                                0.31 * np.cos(2.0 * np.pi * coordinate),
                                -0.27 * np.sin(4.0 * np.pi * coordinate),
                            ]
                        )
                    )
                )
                attacked[index] = frames[index] @ rotation @ phases
            return attacked

        def rough_gauge(frames: ComplexArray3) -> ComplexArray3:
            attacked = np.empty_like(frames)
            amplitude = definition.rough_gauge_amplitude.magnitude
            for index in range(frames.shape[0]):
                sign = 1.0 if index % 2 == 0 else -1.0
                angle = amplitude * sign
                rotation = np.asarray(
                    [
                        [np.cos(angle), -np.sin(angle)],
                        [np.sin(angle), np.cos(angle)],
                    ],
                    dtype=np.complex128,
                )
                phases = np.diag(np.exp(1j * np.asarray([0.43 * sign, -0.37 * sign])))
                attacked[index] = frames[index] @ rotation @ phases
            return attacked

        def project(parent: ComplexArray3, frames: ComplexArray3) -> ComplexArray3:
            return np.asarray(
                [
                    frame.conj().T @ matrix @ frame
                    for matrix, frame in zip(parent, frames, strict=True)
                ],
                dtype=np.complex128,
            )

        def transform(
            samples: ComplexArray3,
            coordinates: RealVector,
            representatives: IntegerVector,
        ) -> ComplexArray3:
            return np.asarray(
                [
                    np.mean(
                        samples
                        * np.exp(-2j * np.pi * coordinates * representative)[
                            :, None, None
                        ],
                        axis=0,
                    )
                    for representative in representatives
                ],
                dtype=np.complex128,
            )

        def interpolate(
            hopping: ComplexArray3,
            representatives: IntegerVector,
            coordinates: RealVector,
        ) -> ComplexArray3:
            return np.asarray(
                [
                    np.sum(
                        hopping
                        * np.exp(2j * np.pi * coordinate * representatives)[
                            :, None, None
                        ],
                        axis=0,
                    )
                    for coordinate in coordinates
                ],
                dtype=np.complex128,
            )

        def eigenvalue_error(target: RealMatrix, operators: ComplexArray3) -> float:
            represented = np.asarray(
                [np.linalg.eigvalsh(matrix) for matrix in operators],
                dtype=np.float64,
            )
            return float(np.max(np.abs(represented - target)))

        def phase_set_defect(reference: RealVector, candidate: RealVector) -> float:
            first = np.sort((reference + np.pi) % (2.0 * np.pi) - np.pi)
            second = np.sort((candidate + np.pi) % (2.0 * np.pi) - np.pi)
            direct = np.max(np.abs((first - second + np.pi) % (2.0 * np.pi) - np.pi))
            swapped = np.max(
                np.abs((first - second[::-1] + np.pi) % (2.0 * np.pi) - np.pi)
            )
            return float(min(direct, swapped))

        training_coordinates = calculation.parent.mesh.coordinates.magnitude
        withheld_coordinates = (
            calculation.parent.withheld_spectrum.coordinates.magnitude
        )
        parent, values, vectors = parent_samples(training_coordinates)
        _, withheld_values, _ = parent_samples(withheld_coordinates)
        represented_parent = np.asarray(
            [
                matrix.magnitude
                for matrix in calculation.parent.parent_operators.matrices
            ]
        )
        parent_operator_defect = float(np.max(np.abs(parent - represented_parent)))
        training_eigenvalue_defect = float(
            np.max(
                np.abs(
                    values - calculation.parent.training_spectrum.eigenvalues.magnitude
                )
            )
        )
        withheld_eigenvalue_defect = float(
            np.max(
                np.abs(
                    withheld_values
                    - calculation.parent.withheld_spectrum.eigenvalues.magnitude
                )
            )
        )
        dimension = parent.shape[1]
        sewing = np.asarray(
            np.roll(np.eye(dimension, dtype=np.complex128), -1, axis=0),
            dtype=np.complex128,
        )
        representatives = np.arange(
            -definition.reciprocal_mesh_size // 2,
            definition.reciprocal_mesh_size // 2,
            dtype=np.int64,
        )
        group_results: list[
            Periodic1DCompositeBandGroupCalculationVerificationResult
        ] = []
        for calculated_group in calculation.groups:
            group = calculated_group.group
            outcome = calculated_group.outcome
            gauge = outcome.gauge_comparison
            representation = outcome.hopping_representation
            selected = slice(group.lower_index, group.upper_index + 1)
            independent_source = vectors[:, :, selected]
            independent_projectors = independent_source @ np.swapaxes(
                independent_source.conj(), 1, 2
            )
            source = np.asarray(
                [frame.magnitude for frame in calculated_group.source_frames.frames]
            )
            represented_source_projectors = np.asarray(
                [
                    projector.magnitude
                    for projector in calculated_group.source_projectors.projectors
                ]
            )
            source_projector_defect = float(
                np.max(
                    np.linalg.norm(
                        independent_projectors - represented_source_projectors,
                        axis=(1, 2),
                    )
                )
            )
            smooth, singular_values, smooth_phases = smooth_transport(source, sewing)
            represented_smooth = np.asarray(
                [
                    frame.magnitude
                    for frame in calculated_group.smooth_transport.transported.frames
                ]
            )
            smooth_frame_defect = float(
                np.max(np.linalg.norm(smooth - represented_smooth, axis=(1, 2)))
            )

            internal_gaps = (
                withheld_values[:, group.lower_index + 1]
                - withheld_values[:, group.lower_index]
            )
            external_candidates: list[float] = []
            if group.lower_index > 0:
                external_candidates.append(
                    float(
                        np.min(
                            withheld_values[:, group.lower_index]
                            - withheld_values[:, group.lower_index - 1]
                        )
                    )
                )
            if group.upper_index + 1 < withheld_values.shape[1]:
                external_candidates.append(
                    float(
                        np.min(
                            withheld_values[:, group.upper_index + 1]
                            - withheld_values[:, group.upper_index]
                        )
                    )
                )
            internal_gap = float(np.min(internal_gaps))
            external_gap = min(external_candidates)
            spectral_defect = max(
                abs(internal_gap - outcome.isolation.internal_minimum_gap),
                abs(external_gap - outcome.isolation.external_minimum_gap),
            )

            controlled_source = controlled_gauge(source)
            controlled, _, controlled_phases = smooth_transport(
                controlled_source, sewing
            )
            source_projectors = source @ np.swapaxes(source.conj(), 1, 2)
            controlled_projectors = controlled_source @ np.swapaxes(
                controlled_source.conj(), 1, 2
            )
            projector_defect = float(
                np.max(
                    np.linalg.norm(
                        source_projectors - controlled_projectors, axis=(1, 2)
                    )
                )
            )
            aligned = np.empty_like(controlled)
            for index in range(controlled.shape[0]):
                overlap = controlled[index].conj().T @ smooth[index]
                left, _, right = np.linalg.svd(overlap)
                aligned[index] = controlled[index] @ (left @ right)
            frame_alignment_defect = float(
                np.max(np.linalg.norm(smooth - aligned, axis=(1, 2)))
            )
            smooth_operators = project(parent, smooth)
            controlled_operators = project(parent, controlled)
            aligned_operators = project(parent, aligned)
            operator_alignment_defect = float(
                np.max(
                    np.linalg.norm(smooth_operators - aligned_operators, axis=(1, 2))
                )
            )
            target_training = values[:, selected]
            controlled_eigenvalue_error = eigenvalue_error(
                target_training, controlled_operators
            )
            smooth_wilson_defect = phase_set_defect(
                smooth_phases,
                np.asarray(outcome.wilson.spectrum.eigenphases, dtype=np.float64),
            )
            controlled_wilson_defect = abs(
                phase_set_defect(smooth_phases, controlled_phases)
                - outcome.wilson.controlled_gauge_phase_set_defect
            )
            gauge_defect = max(
                abs(
                    float(np.min(singular_values))
                    - gauge.neighbor_overlap_minimum_singular_value
                ),
                abs(
                    projector_defect
                    - gauge.controlled_gauge_projector_maximum_frobenius_defect
                ),
                abs(
                    frame_alignment_defect
                    - gauge.pointwise_alignment_frame_maximum_frobenius_defect
                ),
                abs(
                    operator_alignment_defect
                    - gauge.pointwise_alignment_operator_maximum_frobenius_defect
                ),
                abs(
                    controlled_eigenvalue_error
                    - gauge.controlled_gauge_eigenvalue_maximum_defect
                ),
                smooth_wilson_defect,
                controlled_wilson_defect,
            )
            represented_smooth_operators = np.asarray(
                [
                    matrix.magnitude
                    for matrix in representation.smooth_reciprocal_hamiltonians.matrices
                ]
            )
            smooth_operator_defect = float(
                np.max(
                    np.linalg.norm(
                        smooth_operators - represented_smooth_operators,
                        axis=(1, 2),
                    )
                )
            )

            rough = rough_gauge(smooth)
            rough_operators = project(parent, rough)
            smooth_hopping = transform(
                smooth_operators, training_coordinates, representatives
            )
            rough_hopping = transform(
                rough_operators, training_coordinates, representatives
            )
            represented_smooth_hopping = np.asarray(
                [
                    block.magnitude
                    for block in representation.smooth_hopping_model.hopping_blocks
                ]
            )
            represented_rough_hopping = np.asarray(
                [
                    block.magnitude
                    for block in representation.rough_hopping_model.hopping_blocks
                ]
            )
            smooth_hopping_defect = float(
                np.max(np.abs(smooth_hopping - represented_smooth_hopping))
            )
            rough_hopping_defect = float(
                np.max(np.abs(rough_hopping - represented_rough_hopping))
            )
            smooth_reconstructed = interpolate(
                smooth_hopping, representatives, training_coordinates
            )
            rough_reconstructed = interpolate(
                rough_hopping, representatives, training_coordinates
            )
            smooth_reconstruction_error = float(
                np.max(
                    np.linalg.norm(smooth_reconstructed - smooth_operators, axis=(1, 2))
                )
            )
            rough_reconstruction_error = float(
                np.max(
                    np.linalg.norm(rough_reconstructed - rough_operators, axis=(1, 2))
                )
            )
            hermiticity_residuals: list[float] = []
            representative_to_index = {
                int(representative): index
                for index, representative in enumerate(representatives)
            }
            modulus = representatives.size
            for index, representative in enumerate(representatives):
                opposite = int(
                    (-representative + modulus // 2) % modulus - modulus // 2
                )
                opposite_index = representative_to_index[opposite]
                hermiticity_residuals.append(
                    float(
                        np.linalg.norm(
                            smooth_hopping[index]
                            - smooth_hopping[opposite_index].conj().T
                        )
                    )
                )
            hermiticity_residual = max(hermiticity_residuals)
            rough_vs_smooth = float(
                np.sqrt(np.sum(np.abs(smooth_hopping - rough_hopping) ** 2))
            )
            reported_hermiticity = (
                representation.smooth_hopping_hermiticity_maximum_frobenius_residual
            )
            transform_defect = max(
                abs(
                    smooth_reconstruction_error
                    - representation.smooth_full_reconstruction_maximum_frobenius_error
                ),
                abs(
                    rough_reconstruction_error
                    - representation.rough_full_reconstruction_maximum_frobenius_error
                ),
                abs(hermiticity_residual - reported_hermiticity),
                abs(
                    rough_vs_smooth - gauge.rough_vs_smooth_unaligned_hopping_l2_defect
                ),
            )

            target_withheld = withheld_values[:, selected]
            range_defects: list[float] = []
            for represented_range in outcome.range_study:
                mask = np.abs(representatives) <= represented_range.hopping_range_cells
                truncated_smooth = np.where(mask[:, None, None], smooth_hopping, 0.0)
                truncated_rough = np.where(mask[:, None, None], rough_hopping, 0.0)
                smooth_omitted = float(
                    np.sqrt(np.sum(np.abs(smooth_hopping[~mask]) ** 2))
                )
                rough_omitted = float(
                    np.sqrt(np.sum(np.abs(rough_hopping[~mask]) ** 2))
                )
                smooth_training_error = eigenvalue_error(
                    target_training,
                    interpolate(
                        truncated_smooth, representatives, training_coordinates
                    ),
                )
                rough_training_error = eigenvalue_error(
                    target_training,
                    interpolate(truncated_rough, representatives, training_coordinates),
                )
                smooth_withheld_error = eigenvalue_error(
                    target_withheld,
                    interpolate(
                        truncated_smooth, representatives, withheld_coordinates
                    ),
                )
                rough_withheld_error = eigenvalue_error(
                    target_withheld,
                    interpolate(truncated_rough, representatives, withheld_coordinates),
                )
                range_defects.extend(
                    (
                        abs(
                            smooth_omitted
                            - represented_range.smooth_omitted_block_l2_norm
                        ),
                        abs(
                            rough_omitted
                            - represented_range.rough_omitted_block_l2_norm
                        ),
                        abs(
                            smooth_training_error
                            - represented_range.smooth_training_eigenvalue_maximum_error
                        ),
                        abs(
                            rough_training_error
                            - represented_range.rough_training_eigenvalue_maximum_error
                        ),
                        abs(
                            smooth_withheld_error
                            - represented_range.smooth_withheld_eigenvalue_maximum_error
                        ),
                        abs(
                            rough_withheld_error
                            - represented_range.rough_withheld_eigenvalue_maximum_error
                        ),
                    )
                )

            direct_range = definition.direct_route_range_cells
            direct_representatives = np.arange(
                -direct_range, direct_range + 1, dtype=np.int64
            )
            design = np.exp(
                2j
                * np.pi
                * training_coordinates[:, None]
                * direct_representatives[None, :]
            )
            direct_coefficients = np.empty(
                (direct_representatives.size, group.band_count, group.band_count),
                dtype=np.complex128,
            )
            for row in range(group.band_count):
                for column in range(group.band_count):
                    direct_coefficients[:, row, column] = np.linalg.lstsq(
                        design,
                        smooth_operators[:, row, column],
                        rcond=None,
                    )[0]
            mediated = smooth_hopping[np.abs(representatives) <= direct_range]
            coefficient_defect = float(
                np.sqrt(np.sum(np.abs(direct_coefficients - mediated) ** 2))
            )
            direct_samples = interpolate(
                direct_coefficients, direct_representatives, training_coordinates
            )
            mediated_samples = interpolate(
                mediated, direct_representatives, training_coordinates
            )
            sample_defect = float(
                np.max(np.linalg.norm(direct_samples - mediated_samples, axis=(1, 2)))
            )
            route_defect = max(
                abs(
                    coefficient_defect
                    - outcome.direct_route.coefficient_frobenius_defect
                ),
                abs(
                    sample_defect
                    - outcome.direct_route.training_operator_maximum_frobenius_defect
                ),
            )
            magnitudes = (
                source_projector_defect,
                smooth_frame_defect,
                spectral_defect,
                gauge_defect,
                smooth_operator_defect,
                smooth_hopping_defect,
                rough_hopping_defect,
                transform_defect,
                max(range_defects),
                route_defect,
            )
            group_results.append(
                Periodic1DCompositeBandGroupCalculationVerificationResult(
                    group.identifier,
                    ScalarQuantity(magnitudes[0], unit),
                    ScalarQuantity(magnitudes[1], unit),
                    ScalarQuantity(magnitudes[2], unit),
                    ScalarQuantity(magnitudes[3], unit),
                    ScalarQuantity(magnitudes[4], unit),
                    ScalarQuantity(magnitudes[5], unit),
                    ScalarQuantity(magnitudes[6], unit),
                    ScalarQuantity(magnitudes[7], unit),
                    ScalarQuantity(magnitudes[8], unit),
                    ScalarQuantity(magnitudes[9], unit),
                    request.absolute_tolerance,
                    all(value <= tolerance for value in magnitudes),
                )
            )

        parent_magnitudes = (
            parent_operator_defect,
            training_eigenvalue_defect,
            withheld_eigenvalue_defect,
        )
        groups = tuple(group_results)
        return Periodic1DCompositeBandCalculationVerificationResult(
            request,
            ScalarQuantity(parent_magnitudes[0], unit),
            ScalarQuantity(parent_magnitudes[1], unit),
            ScalarQuantity(parent_magnitudes[2], unit),
            groups,
            all(value <= tolerance for value in parent_magnitudes)
            and all(group.passes for group in groups),
        )
