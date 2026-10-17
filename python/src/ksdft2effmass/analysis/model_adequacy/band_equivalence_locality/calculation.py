"""Bounded development calculations for dimensional locality replications.

These calculations exercise the complete parent--subspace--gauge--Fourier--truncation
chain on deliberately small synthetic meshes.  They are development diagnostics, not
retained evidence, continuous convergence results, or material validation.

Serialization intentionally does not live in this module. Definitions and immutable
results are domain objects, while JSON keys, schema identities, canonical byte encoding,
and file output are wire concerns owned by :mod:`.serialization`. Keeping that boundary
prevents storage-format changes from becoming calculation changes. The independent
verifier imports canonical serialization locally only to bind the exact input and result
bytes by SHA-256; it does not choose or mutate scientific values.
"""

from __future__ import annotations

import hashlib
import math

import numpy as np
from numpy.typing import NDArray
from scipy.special import j0, jv  # type: ignore[import-untyped]

from .alignment import (
    FrameTransportDiagnostic,
    frame_transport_diagnostics,
    restricted_alignment,
)
from .constrained_bessel import (
    ConstrainedBesselGeometry,
    ConstrainedBesselZeroModeDiagnostic,
    ConstrainedBesselZeroModeRequest,
)
from .definitions import (
    BandEquivalenceLocalityCase,
    BandEquivalenceLocalityFamily,
    BandEquivalenceLocalityRequest,
    GaugeNormalization,
    ParentKind,
)
from .fourier import (
    error_channels,
    evaluate_blocks,
    fourier_blocks,
    fourier_hermiticity_defects,
    iter_shell_fields,
    maximum_matrix_defect,
)
from .geometry import (
    basis_distance_range,
    metric_covariance_defect,
    minimum_mesh_separation,
)
from .geometry import (
    metric_indices as physical_metric_indices,
)
from .records import (
    AmplitudeMidpointDiagnostic,
    BandEquivalenceLocalityResult,
    BandEquivalenceLocalityVerificationResult,
    CaseDiagnostic,
    FirstPassingDecision,
    FlatAmplitudeResolutionDiagnostic,
    PointDiagnostic,
    ShellDiagnostic,
)

ComplexArray = NDArray[np.complex128]
FloatArray = NDArray[np.float64]
IntArray = NDArray[np.int64]

_ONSITE = np.array(
    [
        [-1.20, 0.06, 0.0, 0.0],
        [0.06, -0.35, 0.0, 0.0],
        [0.0, 0.0, 1.00, 0.04],
        [0.0, 0.0, 0.04, 1.75],
    ],
    dtype=np.complex128,
)
_DIRECTED = np.array(
    [
        [0.15, 0.0, 0.12, 0.0],
        [0.0, -0.10, 0.0, 0.10],
        [0.0, 0.0, 0.05, 0.0],
        [0.0, 0.0, 0.0, -0.04],
    ],
    dtype=np.complex128,
)
_HERMITIAN_BOND = _DIRECTED + _DIRECTED.conjugate().T
_SEED = np.eye(4, 2, dtype=np.complex128)


def _coordinates(size: int, dimension: int, mesh_offset: float) -> FloatArray:
    """Return a tensor grid in reduced reciprocal coordinates.

    ``mesh_offset=0.5`` is the conventional Monkhorst--Pack origin for an even
    construction size. Other offsets define withheld uniform meshes and are not
    silently identified with the construction mesh.
    """
    axis = -0.5 + (np.arange(size, dtype=np.float64) + mesh_offset) / float(size)
    return np.stack(np.meshgrid(*(axis,) * dimension, indexing="ij"), axis=-1)


def _rotation_field(angles: FloatArray) -> ComplexArray:
    rotations = np.empty((*angles.shape, 2, 2), dtype=np.complex128)
    cosine = np.cos(angles)
    sine = np.sin(angles)
    rotations[..., 0, 0] = cosine
    rotations[..., 0, 1] = -sine
    rotations[..., 1, 0] = sine
    rotations[..., 1, 1] = cosine
    return rotations


def _parent_field(
    case: BandEquivalenceLocalityCase, coordinates: FloatArray, parent_scale: float
) -> ComplexArray:
    shape = coordinates.shape[:-1]
    result = np.broadcast_to(_ONSITE, (*shape, 4, 4)).copy()
    if case.parent_kind is ParentKind.DIRECTED_AXIS:
        phase_average = np.mean(np.exp(2.0j * np.pi * coordinates), axis=-1)
        scaled = parent_scale * phase_average
        result += scaled[..., None, None] * _DIRECTED
        result += scaled.conjugate()[..., None, None] * _DIRECTED.conjugate().T
        return result
    if case.parent_kind is ParentKind.HERMITIAN_BRAVAIS:
        bonds = np.asarray(case.positive_bonds, dtype=np.float64)
        arguments = np.einsum("...d,bd->...b", coordinates, bonds)
        structure = np.mean(np.cos(2.0 * np.pi * arguments), axis=-1)
        result += parent_scale * structure[..., None, None] * _HERMITIAN_BOND
        return result

    exponentials = np.exp(-2.0j * np.pi * coordinates)
    gamma = (1.0 + np.sum(exponentials, axis=-1)) / float(case.dimension + 1)
    sublattice = np.empty((*shape, 2, 2), dtype=np.complex128)
    sublattice[..., 0, 0] = 0.0
    sublattice[..., 0, 1] = gamma
    sublattice[..., 1, 0] = gamma.conjugate()
    sublattice[..., 1, 1] = 0.0
    result = np.zeros((*shape, 4, 4), dtype=np.complex128)
    identity = np.eye(2, dtype=np.complex128)
    result[..., :2, :2] = -1.20 * identity + parent_scale * 0.30 * sublattice
    result[..., 2:, 2:] = 1.20 * identity + parent_scale * 0.10 * sublattice
    result[..., :2, 2:] = 0.08 * identity
    result[..., 2:, :2] = 0.08 * identity
    return result


def _continuous_gap_lower_bound(
    case: BandEquivalenceLocalityCase, parent_scale: float
) -> float:
    if case.parent_kind is ParentKind.BIPARTITE_INSPIRED:
        return 2.40 - parent_scale * 0.40 - 0.16
    onsite_gap = float(np.linalg.eigvalsh(_ONSITE)[2] - np.linalg.eigvalsh(_ONSITE)[1])
    if case.parent_kind is ParentKind.DIRECTED_AXIS:
        return onsite_gap - 4.0 * parent_scale * float(np.linalg.norm(_DIRECTED, 2))
    return onsite_gap - 2.0 * parent_scale * float(np.linalg.norm(_HERMITIAN_BOND, 2))


def _retained_frame(
    parent: ComplexArray,
) -> tuple[ComplexArray, FloatArray, FloatArray]:
    eigenvalues, eigenvectors = np.linalg.eigh(parent)
    low = eigenvectors[..., :, :2]
    projector = low @ np.swapaxes(low.conjugate(), -1, -2)
    projected_seed = projector @ _SEED
    seed_gram = np.swapaxes(projected_seed.conjugate(), -1, -2) @ projected_seed
    gram_values, gram_vectors = np.linalg.eigh(seed_gram)
    inverse_root = (
        gram_vectors * (1.0 / np.sqrt(gram_values))[..., None, :]
    ) @ np.swapaxes(gram_vectors.conjugate(), -1, -2)
    frame = projected_seed @ inverse_root
    return frame, eigenvalues, gram_values


def _retained_field(frame: ComplexArray, parent: ComplexArray) -> ComplexArray:
    return np.swapaxes(frame.conjugate(), -1, -2) @ parent @ frame


def _gauge_angles(
    case: BandEquivalenceLocalityCase, coordinates: FloatArray, amplitude: float
) -> FloatArray:
    bonds = np.asarray(case.positive_bonds, dtype=np.float64)
    arguments = np.einsum("...d,bd->...b", coordinates, bonds)
    sine_sum = np.sum(np.sin(2.0 * np.pi * arguments), axis=-1)
    if case.gauge_normalization is GaugeNormalization.AXIS_MAXIMUM:
        return amplitude * sine_sum / float(case.dimension)
    return amplitude * math.sqrt(2.0 / float(len(case.positive_bonds))) * sine_sum


def _analytic_flat_correlation(
    case: BandEquivalenceLocalityCase, amplitude: float
) -> tuple[float, float]:
    bond_count = len(case.positive_bonds)
    if case.gauge_normalization is GaugeNormalization.AXIS_MAXIMUM:
        argument = 2.0 * amplitude / float(case.dimension)
    else:
        argument = 2.0 * amplitude * math.sqrt(2.0 / float(bond_count))
    bonds = np.asarray(case.positive_bonds, dtype=np.float64)
    if bond_count == case.dimension and np.linalg.matrix_rank(bonds) == case.dimension:
        return float(j0(argument)) ** bond_count, 0.0
    if case.dimension == 2 and bond_count == 3:
        diagnostic = ConstrainedBesselZeroModeDiagnostic().execute(
            ConstrainedBesselZeroModeRequest(
                ConstrainedBesselGeometry.TRIANGULAR,
                argument,
                20,
            )
        )
        return diagnostic.value, diagnostic.remainder_bound
    if case.dimension == 3 and bond_count == 6:
        diagnostic = ConstrainedBesselZeroModeDiagnostic().execute(
            ConstrainedBesselZeroModeRequest(
                ConstrainedBesselGeometry.FCC,
                argument,
                9,
            )
        )
        return diagnostic.value, diagnostic.remainder_bound
    raise ValueError("no analytic flat correlation owns this bond inventory")


def _analytic_flat_correlation_values(
    case: BandEquivalenceLocalityCase, amplitudes: FloatArray
) -> FloatArray:
    """Evaluate one flat correlation law vectorially for resolution diagnostics."""
    bond_count = len(case.positive_bonds)
    scale = (
        2.0 / float(case.dimension)
        if case.gauge_normalization is GaugeNormalization.AXIS_MAXIMUM
        else 2.0 * math.sqrt(2.0 / float(bond_count))
    )
    arguments = scale * amplitudes
    bonds = np.asarray(case.positive_bonds, dtype=np.float64)
    if bond_count == case.dimension and np.linalg.matrix_rank(bonds) == case.dimension:
        return np.asarray(j0(arguments) ** bond_count, dtype=np.float64)
    if case.dimension == 2 and bond_count == 3:
        indices = np.arange(-20, 21, dtype=np.int64)
        positive = jv(indices[None, :], arguments[:, None])
        negative = jv(-indices[None, :], arguments[:, None])
        return np.asarray(
            np.sum(negative * positive * positive, axis=1), dtype=np.float64
        )
    if case.dimension == 3 and bond_count == 6:
        free = np.arange(-9, 10, dtype=np.int64)
        one, two, three = np.meshgrid(free, free, free, indexing="ij")
        orders = np.arange(-18, 19, dtype=np.int64)
        offset = 18
        flattened_indices = tuple(
            value.ravel() + offset
            for value in (
                one + two,
                -one + three,
                -two - three,
                one,
                two,
                three,
            )
        )
        values = np.empty(arguments.size, dtype=np.float64)
        batch_size = 64
        for start in range(0, arguments.size, batch_size):
            stop = min(start + batch_size, arguments.size)
            bessel = jv(orders[None, :], arguments[start:stop, None])
            product = np.ones((stop - start, one.size), dtype=np.float64)
            for indices in flattened_indices:
                product *= bessel[:, indices]
            values[start:stop] = np.sum(product, axis=1)
        return values
    raise ValueError("no analytic flat correlation owns this bond inventory")


def _flat_amplitude_resolution(
    definition: BandEquivalenceLocalityRequest, case: BandEquivalenceLocalityCase
) -> tuple[FlatAmplitudeResolutionDiagnostic, ...]:
    maximum_amplitude = definition.amplitudes[-1]
    finest_intervals = definition.amplitude_resolution_intervals[-1]
    fine_positions = np.arange(2 * finest_intervals + 1, dtype=np.float64)
    fine_amplitudes = maximum_amplitude * fine_positions / float(2 * finest_intervals)
    correlations = np.clip(
        _analytic_flat_correlation_values(case, fine_amplitudes), -1.0, 1.0
    )
    operator = np.sqrt(np.maximum(0.0, 1.0 - correlations**2))
    joint = np.sqrt(np.maximum(0.0, 2.0 * (1.0 - correlations)))
    results: list[FlatAmplitudeResolutionDiagnostic] = []
    for intervals in definition.amplitude_resolution_intervals:
        stride = finest_intervals // intervals
        node_indices = np.arange(0, 2 * finest_intervals + 1, 2 * stride)
        midpoint_indices = node_indices[:-1] + stride
        operator_interpolated = 0.5 * (
            operator[node_indices[:-1]] + operator[node_indices[1:]]
        )
        joint_interpolated = 0.5 * (joint[node_indices[:-1]] + joint[node_indices[1:]])
        results.append(
            FlatAmplitudeResolutionDiagnostic(
                amplitude_intervals=intervals,
                amplitude_nodes=intervals + 1,
                maximum_operator_threshold_midpoint_interpolation_defect=float(
                    np.max(np.abs(operator_interpolated - operator[midpoint_indices]))
                ),
                maximum_joint_threshold_midpoint_interpolation_defect=float(
                    np.max(np.abs(joint_interpolated - joint[midpoint_indices]))
                ),
                passes_unit_scale_draft_tolerance=None,
                tolerance_inapplicable_reason=(
                    "Paper 2 did not prospectively freeze a family-owned amplitude "
                    "resolution tolerance; Paper 1's tolerance is not transferred"
                ),
            )
        )
    return tuple(results)


def _amplitude_midpoint_diagnostic(
    definition: BandEquivalenceLocalityRequest, points: tuple[PointDiagnostic, ...]
) -> AmplitudeMidpointDiagnostic:
    amplitudes = definition.amplitudes
    if len(amplitudes) != 3 or not math.isclose(
        amplitudes[1],
        0.5 * (amplitudes[0] + amplitudes[2]),
        rel_tol=0.0,
        abs_tol=1.0e-15,
    ):
        return AmplitudeMidpointDiagnostic(
            amplitude_nodes=len(amplitudes),
            applicable=False,
            inapplicable_reason=(
                "the declared amplitudes do not form one "
                "endpoint-midpoint-endpoint triple"
            ),
            endpoint_minimum_threshold_over_sqrt_splitting=None,
            maximum_correlation_midpoint_defect=None,
            maximum_operator_threshold_midpoint_defect=None,
            maximum_joint_threshold_midpoint_defect=None,
            maximum_nonzero_hopping_weight_midpoint_defect=None,
            maximum_hopping_block_power_midpoint_defect=None,
        )

    endpoint_thresholds: list[float] = []
    correlations: list[float] = []
    operator_thresholds: list[float] = []
    joint_thresholds: list[float] = []
    hopping_weights: list[float] = []
    hopping_block_powers: list[float] = []
    for parent_scale in definition.parent_scales:
        triple = tuple(point for point in points if point.parent_scale == parent_scale)
        if len(triple) != 3:
            raise RuntimeError("amplitude point inventory does not match definition")
        left, midpoint, right = triple
        if right.minimum_operator_threshold_over_sqrt_splitting is not None:
            endpoint_thresholds.append(
                right.minimum_operator_threshold_over_sqrt_splitting
            )
        if (
            left.finite_mesh_maximum_correlation is not None
            and midpoint.finite_mesh_maximum_correlation is not None
            and right.finite_mesh_maximum_correlation is not None
        ):
            correlations.append(
                abs(
                    midpoint.finite_mesh_maximum_correlation
                    - 0.5
                    * (
                        left.finite_mesh_maximum_correlation
                        + right.finite_mesh_maximum_correlation
                    )
                )
            )
        operator_thresholds.append(
            abs(
                midpoint.minimum_operator_threshold
                - 0.5
                * (left.minimum_operator_threshold + right.minimum_operator_threshold)
            )
        )
        joint_thresholds.append(
            abs(
                midpoint.exact_spectrum_joint_operator_threshold
                - 0.5
                * (
                    left.exact_spectrum_joint_operator_threshold
                    + right.exact_spectrum_joint_operator_threshold
                )
            )
        )
        hopping_weights.append(
            abs(
                midpoint.comparison_nononsite_power
                - 0.5
                * (left.comparison_nononsite_power + right.comparison_nononsite_power)
            )
        )
        for left_shell, midpoint_shell, right_shell in zip(
            left.shell_diagnostics,
            midpoint.shell_diagnostics,
            right.shell_diagnostics,
            strict=True,
        ):
            if not (
                left_shell.shell_index
                == midpoint_shell.shell_index
                == right_shell.shell_index
            ):
                raise RuntimeError("amplitude shell inventories differ")
            hopping_block_powers.append(
                abs(
                    midpoint_shell.comparison_shell_power
                    - 0.5
                    * (
                        left_shell.comparison_shell_power
                        + right_shell.comparison_shell_power
                    )
                )
            )
    return AmplitudeMidpointDiagnostic(
        amplitude_nodes=len(amplitudes),
        applicable=True,
        inapplicable_reason=None,
        endpoint_minimum_threshold_over_sqrt_splitting=(
            min(endpoint_thresholds) if endpoint_thresholds else None
        ),
        maximum_correlation_midpoint_defect=(
            max(correlations) if correlations else None
        ),
        maximum_operator_threshold_midpoint_defect=max(operator_thresholds),
        maximum_joint_threshold_midpoint_defect=max(joint_thresholds),
        maximum_nonzero_hopping_weight_midpoint_defect=max(hopping_weights),
        maximum_hopping_block_power_midpoint_defect=max(hopping_block_powers),
    )


class BandEquivalenceLocalityCalculator:
    """Execute every methodological channel for one bounded family definition."""

    __slots__ = ()

    def execute(
        self,
        definition: BandEquivalenceLocalityRequest,
        analysis_request_sha256: str,
    ) -> BandEquivalenceLocalityResult:
        if type(definition) is not BandEquivalenceLocalityRequest:
            raise TypeError("definition must be BandEquivalenceLocalityRequest")
        if type(analysis_request_sha256) is not str:
            raise TypeError("analysis_request_sha256 must be a built-in str")
        if len(analysis_request_sha256) != 64 or any(
            character not in "0123456789abcdef" for character in analysis_request_sha256
        ):
            raise ValueError(
                "analysis_request_sha256 must be a lowercase SHA-256 digest"
            )
        construction = _coordinates(
            definition.construction_size, definition.dimension, 0.5
        )
        evaluation = _coordinates(
            definition.evaluation_size,
            definition.dimension,
            0.5 + definition.evaluation_shift,
        )
        separation = minimum_mesh_separation(construction, evaluation)
        case_results = tuple(
            self._case(definition, case, construction, evaluation, separation)
            for case in definition.cases
        )
        return BandEquivalenceLocalityResult(
            family=definition.family,
            status="development-smoke-not-retained-evidence",
            analysis_request_sha256=analysis_request_sha256,
            construction_size=definition.construction_size,
            evaluation_size=definition.evaluation_size,
            cases=case_results,
        )

    def _case(
        self,
        definition: BandEquivalenceLocalityRequest,
        case: BandEquivalenceLocalityCase,
        construction: FloatArray,
        evaluation: FloatArray,
        separation: float,
    ) -> CaseDiagnostic:
        points: list[PointDiagnostic] = []
        for parent_scale in definition.parent_scales:
            parent = _parent_field(case, construction, parent_scale)
            frame, eigenvalues, seed_gram_values = _retained_frame(parent)
            transport = frame_transport_diagnostics(
                frame,
                case.dimension,
                definition.transport_rank_absolute,
                definition.transport_rank_relative,
            )
            projector = frame @ np.swapaxes(frame.conjugate(), -1, -2)
            retained = _retained_field(frame, parent)
            eigensystem = np.linalg.eigh(parent)
            reconstructed_parent = (
                eigensystem.eigenvectors * eigensystem.eigenvalues[..., None, :]
            ) @ np.swapaxes(eigensystem.eigenvectors.conjugate(), -1, -2)
            identity = np.eye(2, dtype=np.complex128)
            parent_reconstruction = projector @ parent @ projector
            lifted = frame @ retained @ np.swapaxes(frame.conjugate(), -1, -2)
            parent_displacements, parent_blocks = fourier_blocks(
                parent, case.dimension, 0.5
            )
            parent_fourier_reconstruction = maximum_matrix_defect(
                evaluate_blocks(
                    parent_displacements,
                    parent_blocks,
                    construction,
                    definition.construction_size,
                ),
                parent,
            )
            periodic_frame_closure = 0.0
            for axis in range(case.dimension):
                shifted = construction.copy()
                shifted[..., axis] += 1.0
                shifted_frame, _, _ = _retained_frame(
                    _parent_field(case, shifted, parent_scale)
                )
                periodic_frame_closure = max(
                    periodic_frame_closure,
                    maximum_matrix_defect(shifted_frame, frame),
                )
            minimum_sampled_external_gap = float(
                np.min(eigenvalues[..., 2] - eigenvalues[..., 1])
            )
            continuous_external_gap_lower_bound = _continuous_gap_lower_bound(
                case, parent_scale
            )
            minimum_seed_overlap = float(np.min(seed_gram_values))
            maximum_parent_hermiticity_defect = maximum_matrix_defect(
                parent, np.swapaxes(parent.conjugate(), -1, -2)
            )
            maximum_eigensystem_reconstruction_defect = maximum_matrix_defect(
                parent, reconstructed_parent
            )
            maximum_frame_orthonormality_defect = maximum_matrix_defect(
                np.swapaxes(frame.conjugate(), -1, -2) @ frame,
                np.broadcast_to(identity, (*construction.shape[:-1], 2, 2)),
            )
            maximum_projector_reconstruction_defect = maximum_matrix_defect(
                projector,
                eigensystem.eigenvectors[..., :, :2]
                @ np.swapaxes(eigensystem.eigenvectors[..., :, :2].conjugate(), -1, -2),
            )
            maximum_parent_retained_reconstruction_defect = maximum_matrix_defect(
                parent_reconstruction, lifted
            )
            direct_parent_eval = _parent_field(case, evaluation, parent_scale)
            direct_frame_eval, _, _ = _retained_frame(direct_parent_eval)
            direct_reference_eval = _retained_field(
                direct_frame_eval, direct_parent_eval
            )
            for amplitude in definition.amplitudes:
                points.append(
                    self._point(
                        definition,
                        case,
                        construction,
                        evaluation,
                        parent_scale,
                        amplitude,
                        retained,
                        direct_reference_eval,
                        transport,
                        minimum_sampled_external_gap=minimum_sampled_external_gap,
                        continuous_external_gap_lower_bound=(
                            continuous_external_gap_lower_bound
                        ),
                        minimum_seed_overlap=minimum_seed_overlap,
                        maximum_parent_hermiticity_defect=(
                            maximum_parent_hermiticity_defect
                        ),
                        maximum_eigensystem_reconstruction_defect=(
                            maximum_eigensystem_reconstruction_defect
                        ),
                        maximum_frame_orthonormality_defect=(
                            maximum_frame_orthonormality_defect
                        ),
                        maximum_projector_reconstruction_defect=(
                            maximum_projector_reconstruction_defect
                        ),
                        maximum_parent_retained_reconstruction_defect=(
                            maximum_parent_retained_reconstruction_defect
                        ),
                        maximum_parent_fourier_reconstruction_defect=(
                            parent_fourier_reconstruction
                        ),
                        maximum_periodic_frame_closure_defect=periodic_frame_closure,
                    )
                )
        point_tuple = tuple(points)
        return CaseDiagnostic(
            name=case.name,
            metric_covariance_defect=metric_covariance_defect(case),
            construction_evaluation_minimum_separation=separation,
            amplitude_midpoint=_amplitude_midpoint_diagnostic(definition, point_tuple),
            flat_amplitude_resolution=_flat_amplitude_resolution(definition, case),
            points=point_tuple,
        )

    def _point(
        self,
        definition: BandEquivalenceLocalityRequest,
        case: BandEquivalenceLocalityCase,
        construction: FloatArray,
        evaluation: FloatArray,
        parent_scale: float,
        amplitude: float,
        reference: ComplexArray,
        direct_reference_eval: ComplexArray,
        transport: FrameTransportDiagnostic,
        *,
        minimum_sampled_external_gap: float,
        continuous_external_gap_lower_bound: float,
        minimum_seed_overlap: float,
        maximum_parent_hermiticity_defect: float,
        maximum_eigensystem_reconstruction_defect: float,
        maximum_frame_orthonormality_defect: float,
        maximum_projector_reconstruction_defect: float,
        maximum_parent_retained_reconstruction_defect: float,
        maximum_parent_fourier_reconstruction_defect: float,
        maximum_periodic_frame_closure_defect: float,
    ) -> PointDiagnostic:
        rotation = _rotation_field(_gauge_angles(case, construction, amplitude))
        comparison = np.swapaxes(rotation.conjugate(), -1, -2) @ reference @ rotation
        rotation_eval = _rotation_field(_gauge_angles(case, evaluation, amplitude))
        direct_comparison_eval = (
            np.swapaxes(rotation_eval.conjugate(), -1, -2)
            @ direct_reference_eval
            @ rotation_eval
        )
        direct_band_defect = float(
            np.max(
                np.abs(np.linalg.eigvalsh(reference) - np.linalg.eigvalsh(comparison))
            )
        )
        covariant_defect = maximum_matrix_defect(
            comparison,
            np.swapaxes(rotation.conjugate(), -1, -2) @ reference @ rotation,
        )
        (
            angle,
            angle_degenerate,
            splitting_scale,
            correlation,
            minimum_threshold,
            exact_spectrum_threshold,
        ) = restricted_alignment(reference, comparison)
        displacements, reference_blocks = fourier_blocks(reference, case.dimension, 0.5)
        comparison_displacements, comparison_blocks = fourier_blocks(
            comparison, case.dimension, 0.5
        )
        if not np.array_equal(displacements, comparison_displacements):
            raise RuntimeError("reference and comparison Fourier inventories differ")
        analytic_correlation: float | None = None
        analytic_remainder: float | None = None
        correlation_defect: float | None = None
        if parent_scale == 0.0 and correlation is not None:
            analytic_correlation, analytic_remainder = _analytic_flat_correlation(
                case, amplitude
            )
            correlation_defect = abs(correlation - analytic_correlation)
        block_power_reference = (
            np.sum(np.abs(reference_blocks) ** 2, axis=(-2, -1)) / 2.0
        )
        block_power_comparison = (
            np.sum(np.abs(comparison_blocks) ** 2, axis=(-2, -1)) / 2.0
        )
        onsite = np.all(displacements == 0, axis=1)
        reference_total_power = float(np.sum(block_power_reference))
        comparison_total_power = float(np.sum(block_power_comparison))
        reference_onsite_power = float(np.sum(block_power_reference[onsite]))
        comparison_onsite_power = float(np.sum(block_power_comparison[onsite]))
        reference_nononsite_power = reference_total_power - reference_onsite_power
        comparison_nononsite_power = comparison_total_power - comparison_onsite_power
        excess_nonzero_power = comparison_nononsite_power - reference_nononsite_power
        root_splitting = math.sqrt(splitting_scale)
        if root_splitting > 1.0e-15:
            normalized_operator_threshold = minimum_threshold / root_splitting
            normalized_joint_threshold = exact_spectrum_threshold / root_splitting
            normalized_squared_residual = normalized_operator_threshold**2
            normalized_excess_power = excess_nonzero_power / splitting_scale
            flat_identity_departure = (
                normalized_excess_power - normalized_squared_residual
            )
        else:
            normalized_operator_threshold = None
            normalized_joint_threshold = None
            normalized_squared_residual = None
            normalized_excess_power = None
            flat_identity_departure = None
        flat_identity_defect = (
            abs(minimum_threshold**2 - comparison_nononsite_power)
            if parent_scale == 0.0 and correlation is not None
            else None
        )
        reconstructed_reference = evaluate_blocks(
            displacements,
            reference_blocks,
            construction,
            definition.construction_size,
        )
        reconstructed_comparison = evaluate_blocks(
            displacements,
            comparison_blocks,
            construction,
            definition.construction_size,
        )
        reference_parseval = abs(
            float(np.mean(np.sum(np.abs(reference) ** 2, axis=(-2, -1))))
            - float(np.sum(np.abs(reference_blocks) ** 2))
        )
        comparison_parseval = abs(
            float(np.mean(np.sum(np.abs(comparison) ** 2, axis=(-2, -1))))
            - float(np.sum(np.abs(comparison_blocks) ** 2))
        )
        reference_twisted, reference_hermiticity = fourier_hermiticity_defects(
            definition.construction_size, displacements, reference_blocks
        )
        comparison_twisted, comparison_hermiticity = fourier_hermiticity_defects(
            definition.construction_size, displacements, comparison_blocks
        )
        nyquist = np.any(displacements == -definition.construction_size // 2, axis=1)
        reference_nyquist_power = float(
            np.sum(np.abs(reference_blocks[nyquist]) ** 2) / 2.0
        )
        comparison_nyquist_power = float(
            np.sum(np.abs(comparison_blocks[nyquist]) ** 2) / 2.0
        )
        ordinary = ~nyquist
        ordinary_displacements = displacements[ordinary]
        ordinary_reference = reference_blocks[ordinary]
        ordinary_comparison = comparison_blocks[ordinary]
        full_reference_eval = evaluate_blocks(
            ordinary_displacements,
            ordinary_reference,
            evaluation,
            definition.construction_size,
        )
        full_comparison_eval = evaluate_blocks(
            ordinary_displacements,
            ordinary_comparison,
            evaluation,
            definition.construction_size,
        )
        full_reference_source = evaluate_blocks(
            ordinary_displacements,
            ordinary_reference,
            construction,
            definition.construction_size,
        )
        full_comparison_source = evaluate_blocks(
            ordinary_displacements,
            ordinary_comparison,
            construction,
            definition.construction_size,
        )
        reference_interpolation = error_channels(
            full_reference_eval, direct_reference_eval
        )
        comparison_interpolation = error_channels(
            full_comparison_eval, direct_comparison_eval
        )
        metric_indices = physical_metric_indices(case, ordinary_displacements)
        shells = tuple(
            int(value)
            for value in sorted(set(metric_indices.tolist()))
            if value <= definition.shell_cap
        )
        reference_evaluations = iter_shell_fields(
            ordinary_displacements,
            ordinary_reference,
            evaluation,
            definition.construction_size,
            metric_indices,
            shells,
        )
        comparison_evaluations = iter_shell_fields(
            ordinary_displacements,
            ordinary_comparison,
            evaluation,
            definition.construction_size,
            metric_indices,
            shells,
        )
        reference_sources = iter_shell_fields(
            ordinary_displacements,
            ordinary_reference,
            construction,
            definition.construction_size,
            metric_indices,
            shells,
        )
        comparison_sources = iter_shell_fields(
            ordinary_displacements,
            ordinary_comparison,
            construction,
            definition.construction_size,
            metric_indices,
            shells,
        )
        shell_results: list[ShellDiagnostic] = []
        for (
            shell,
            reference_eval,
            comparison_eval,
            reference_source,
            comparison_source,
        ) in zip(
            shells,
            reference_evaluations,
            comparison_evaluations,
            reference_sources,
            comparison_sources,
            strict=True,
        ):
            retained_mask = metric_indices <= shell
            shell_mask = metric_indices == shell
            reference_shell_power = float(
                np.sum(np.abs(ordinary_reference[shell_mask]) ** 2) / 2.0
            )
            comparison_shell_power = float(
                np.sum(np.abs(ordinary_comparison[shell_mask]) ** 2) / 2.0
            )
            reference_omitted = float(
                np.sum(np.abs(ordinary_reference[~retained_mask]) ** 2) / 2.0
            )
            comparison_omitted = float(
                np.sum(np.abs(ordinary_comparison[~retained_mask]) ** 2) / 2.0
            )
            reference_source_truncation = error_channels(
                reference_source, full_reference_source
            )
            comparison_source_truncation = error_channels(
                comparison_source, full_comparison_source
            )
            shell_results.append(
                ShellDiagnostic(
                    shell_index=shell,
                    retained_blocks=int(np.count_nonzero(retained_mask)),
                    reference_truncation=error_channels(
                        reference_eval, full_reference_eval
                    ),
                    comparison_truncation=error_channels(
                        comparison_eval, full_comparison_eval
                    ),
                    reference_total=error_channels(
                        reference_eval, direct_reference_eval
                    ),
                    comparison_total=error_channels(
                        comparison_eval, direct_comparison_eval
                    ),
                    reference_shell_power=reference_shell_power,
                    comparison_shell_power=comparison_shell_power,
                    reference_omitted_power=reference_omitted,
                    comparison_omitted_power=comparison_omitted,
                    reference_total_omitted_power=(
                        reference_omitted + reference_nyquist_power
                    ),
                    comparison_total_omitted_power=(
                        comparison_omitted + comparison_nyquist_power
                    ),
                    reference_truncation_parseval_defect=abs(
                        reference_source_truncation.rms_hamiltonian**2
                        - reference_omitted
                    ),
                    comparison_truncation_parseval_defect=abs(
                        comparison_source_truncation.rms_hamiltonian**2
                        - comparison_omitted
                    ),
                )
            )
        decisions = tuple(
            _first_passing(tuple(shell_results), tolerance)
            for tolerance in definition.band_tolerances
        )
        largest_mask = metric_indices <= shells[-1]
        basis_minimum, basis_maximum = basis_distance_range(
            case, ordinary_displacements[largest_mask]
        )
        return PointDiagnostic(
            parent_scale=parent_scale,
            amplitude=amplitude,
            minimum_sampled_external_gap=minimum_sampled_external_gap,
            continuous_external_gap_lower_bound=continuous_external_gap_lower_bound,
            minimum_seed_overlap=minimum_seed_overlap,
            maximum_parent_hermiticity_defect=maximum_parent_hermiticity_defect,
            maximum_eigensystem_reconstruction_defect=(
                maximum_eigensystem_reconstruction_defect
            ),
            maximum_frame_orthonormality_defect=(maximum_frame_orthonormality_defect),
            maximum_projector_reconstruction_defect=(
                maximum_projector_reconstruction_defect
            ),
            maximum_parent_retained_reconstruction_defect=(
                maximum_parent_retained_reconstruction_defect
            ),
            maximum_parent_fourier_reconstruction_defect=(
                maximum_parent_fourier_reconstruction_defect
            ),
            maximum_periodic_frame_closure_defect=(
                maximum_periodic_frame_closure_defect
            ),
            minimum_sampled_transport_singular_value=(transport.minimum_singular_value),
            maximum_transport_procrustes_residual=(
                transport.maximum_procrustes_residual
            ),
            maximum_transport_squared_residual_roundoff_cutoff=(
                transport.maximum_squared_residual_roundoff_cutoff
            ),
            maximum_transport_unitarity_defect=transport.maximum_unitarity_defect,
            maximum_transport_rank_cutoff=transport.maximum_rank_cutoff,
            transport_rank_deficient_link_count=(transport.rank_deficient_link_count),
            transport_closure_and_plaquette_applicable=(
                transport.closure_and_plaquette_applicable
            ),
            transport_closure_and_plaquette_inapplicable_reason=(
                transport.closure_and_plaquette_inapplicable_reason
            ),
            maximum_absolute_closure_holonomy_phases=(
                transport.maximum_absolute_closure_phases
            ),
            maximum_closure_holonomy_unitarity_defect=(
                transport.maximum_closure_unitarity_defect
            ),
            maximum_plaquette_holonomy_phase=transport.maximum_plaquette_phase,
            maximum_direct_band_defect=direct_band_defect,
            maximum_covariant_defect=covariant_defect,
            alignment_applicable=correlation is not None,
            alignment_inapplicable_reason=(
                None
                if correlation is not None
                else "zero splitting scale: normalized correlation is undefined"
            ),
            restricted_global_rotation_angle=angle,
            restricted_global_rotation_degenerate=angle_degenerate,
            splitting_scale=splitting_scale,
            finite_mesh_maximum_correlation=correlation,
            analytic_flat_correlation=analytic_correlation,
            analytic_correlation_remainder_bound=analytic_remainder,
            correlation_quadrature_defect=correlation_defect,
            minimum_operator_threshold=minimum_threshold,
            exact_spectrum_joint_operator_threshold=exact_spectrum_threshold,
            minimum_operator_threshold_over_sqrt_splitting=(
                normalized_operator_threshold
            ),
            exact_spectrum_joint_threshold_over_sqrt_splitting=(
                normalized_joint_threshold
            ),
            normalized_squared_operator_residual=normalized_squared_residual,
            restricted_global_rotation_residual=minimum_threshold,
            reference_fourier_reconstruction_defect=maximum_matrix_defect(
                reconstructed_reference, reference
            ),
            comparison_fourier_reconstruction_defect=maximum_matrix_defect(
                reconstructed_comparison, comparison
            ),
            reference_parseval_defect=reference_parseval,
            comparison_parseval_defect=comparison_parseval,
            reference_twisted_nyquist_defect=reference_twisted,
            comparison_twisted_nyquist_defect=comparison_twisted,
            reference_ordinary_hermiticity_defect=reference_hermiticity,
            comparison_ordinary_hermiticity_defect=comparison_hermiticity,
            reference_interpolation=reference_interpolation,
            comparison_interpolation=comparison_interpolation,
            reference_total_power=reference_total_power,
            comparison_total_power=comparison_total_power,
            reference_onsite_power=reference_onsite_power,
            comparison_onsite_power=comparison_onsite_power,
            reference_nononsite_power=reference_nononsite_power,
            comparison_nononsite_power=comparison_nononsite_power,
            excess_nonzero_hopping_weight=excess_nonzero_power,
            normalized_excess_nonzero_hopping_weight=normalized_excess_power,
            flat_identity_departure=flat_identity_departure,
            reference_nyquist_power=reference_nyquist_power,
            comparison_nyquist_power=comparison_nyquist_power,
            flat_residual_tail_identity_defect=flat_identity_defect,
            basis_distance_minimum=basis_minimum,
            basis_distance_maximum=basis_maximum,
            shell_diagnostics=tuple(shell_results),
            first_passing=decisions,
        )


def _first_passing(
    shells: tuple[ShellDiagnostic, ...], tolerance: float
) -> FirstPassingDecision:
    def select(
        channel: str, quantity: str
    ) -> tuple[int | None, float | None, float | None]:
        previous: float | None = None
        for shell in shells:
            errors = (
                shell.reference_total
                if channel == "reference"
                else shell.comparison_total
            )
            value = (
                errors.maximum_band
                if quantity == "band"
                else errors.maximum_hamiltonian
            )
            if value <= tolerance:
                return shell.shell_index, value, previous
            previous = value
        return None, None, None

    reference_band = select("reference", "band")
    comparison_band = select("comparison", "band")
    reference_hamiltonian = select("reference", "hamiltonian")
    comparison_hamiltonian = select("comparison", "hamiltonian")
    return FirstPassingDecision(
        tolerance=tolerance,
        reference_band_shell=reference_band[0],
        comparison_band_shell=comparison_band[0],
        reference_hamiltonian_shell=reference_hamiltonian[0],
        comparison_hamiltonian_shell=comparison_hamiltonian[0],
        reference_band_passing_error=reference_band[1],
        reference_band_preceding_error=reference_band[2],
        comparison_band_passing_error=comparison_band[1],
        comparison_band_preceding_error=comparison_band[2],
        reference_hamiltonian_passing_error=reference_hamiltonian[1],
        reference_hamiltonian_preceding_error=reference_hamiltonian[2],
        comparison_hamiltonian_passing_error=comparison_hamiltonian[1],
        comparison_hamiltonian_preceding_error=comparison_hamiltonian[2],
    )


def _transport_record_defects(
    point: PointDiagnostic, expected: FrameTransportDiagnostic
) -> tuple[float, ...]:
    """Compare one stored transport record without zero-filling topology."""
    defects = [
        abs(
            point.minimum_sampled_transport_singular_value
            - expected.minimum_singular_value
        ),
        abs(
            point.maximum_transport_procrustes_residual
            - expected.maximum_procrustes_residual
        ),
        abs(
            point.maximum_transport_squared_residual_roundoff_cutoff
            - expected.maximum_squared_residual_roundoff_cutoff
        ),
        abs(
            point.maximum_transport_unitarity_defect - expected.maximum_unitarity_defect
        ),
        abs(point.maximum_transport_rank_cutoff - expected.maximum_rank_cutoff),
        float(
            abs(
                point.transport_rank_deficient_link_count
                - expected.rank_deficient_link_count
            )
        ),
        0.0
        if point.transport_closure_and_plaquette_applicable
        == expected.closure_and_plaquette_applicable
        else 1.0,
        0.0
        if point.transport_closure_and_plaquette_inapplicable_reason
        == expected.closure_and_plaquette_inapplicable_reason
        else 1.0,
    ]
    if expected.closure_and_plaquette_applicable:
        phases = point.maximum_absolute_closure_holonomy_phases
        expected_phases = expected.maximum_absolute_closure_phases
        closure = point.maximum_closure_holonomy_unitarity_defect
        expected_closure = expected.maximum_closure_unitarity_defect
        plaquette = point.maximum_plaquette_holonomy_phase
        expected_plaquette = expected.maximum_plaquette_phase
        if (
            phases is None
            or expected_phases is None
            or closure is None
            or expected_closure is None
            or plaquette is None
            or expected_plaquette is None
        ):
            raise ValueError("applicable transport is missing topology diagnostics")
        defects.extend(
            (
                abs(phases[0] - expected_phases[0]),
                abs(phases[1] - expected_phases[1]),
                abs(closure - expected_closure),
                abs(plaquette - expected_plaquette),
            )
        )
    return tuple(defects)


class BandEquivalenceLocalityVerifier:
    """Independently reconstruct selected point and stored-identity diagnostics."""

    __slots__ = ()

    def execute(
        self,
        definition: BandEquivalenceLocalityRequest,
        result: BandEquivalenceLocalityResult,
    ) -> BandEquivalenceLocalityVerificationResult:
        if type(definition) is not BandEquivalenceLocalityRequest:
            raise TypeError("definition must be BandEquivalenceLocalityRequest")
        if type(result) is not BandEquivalenceLocalityResult:
            raise TypeError("result must be BandEquivalenceLocalityResult")

        # Local import keeps wire mechanics out of numerical module initialization.
        from .serialization import (
            band_equivalence_locality_request_document,
            band_equivalence_locality_result_document,
            canonical_json_bytes,
        )

        input_encoded = canonical_json_bytes(
            band_equivalence_locality_request_document(definition)
        )
        input_sha256 = hashlib.sha256(input_encoded).hexdigest()
        if result.analysis_request_sha256 != input_sha256:
            raise ValueError("result does not belong to the analysis request")
        if result.family is not definition.family:
            raise ValueError("result family does not match definition")
        if (
            result.construction_size != definition.construction_size
            or result.evaluation_size != definition.evaluation_size
        ):
            raise ValueError("result mesh sizes do not match definition")
        stored_defects: list[float] = []
        for case in result.cases:
            stored_defects.append(case.metric_covariance_defect)
            for point in case.points:
                stored_defects.extend(
                    (
                        max(0.0, -point.continuous_external_gap_lower_bound),
                        point.maximum_parent_hermiticity_defect,
                        point.maximum_eigensystem_reconstruction_defect,
                        point.maximum_frame_orthonormality_defect,
                        point.maximum_projector_reconstruction_defect,
                        point.maximum_parent_retained_reconstruction_defect,
                        point.maximum_parent_fourier_reconstruction_defect,
                        point.maximum_periodic_frame_closure_defect,
                        point.maximum_transport_unitarity_defect,
                        point.maximum_direct_band_defect,
                        point.maximum_covariant_defect,
                        point.flat_residual_tail_identity_defect or 0.0,
                        (
                            0.0
                            if point.normalized_squared_operator_residual is None
                            else abs(
                                point.normalized_squared_operator_residual
                                - point.minimum_operator_threshold**2
                                / point.splitting_scale
                            )
                        ),
                        (
                            0.0
                            if point.flat_identity_departure is None
                            else abs(
                                point.flat_identity_departure
                                - (
                                    point.normalized_excess_nonzero_hopping_weight
                                    or 0.0
                                )
                                + (point.normalized_squared_operator_residual or 0.0)
                            )
                        ),
                        abs(
                            point.restricted_global_rotation_residual
                            - point.minimum_operator_threshold
                        ),
                        point.reference_fourier_reconstruction_defect,
                        point.comparison_fourier_reconstruction_defect,
                        point.reference_parseval_defect,
                        point.comparison_parseval_defect,
                        point.reference_twisted_nyquist_defect,
                        point.comparison_twisted_nyquist_defect,
                        point.reference_ordinary_hermiticity_defect,
                        point.comparison_ordinary_hermiticity_defect,
                    )
                )
                if point.transport_closure_and_plaquette_applicable:
                    closure_defect = point.maximum_closure_holonomy_unitarity_defect
                    if closure_defect is None:
                        raise ValueError(
                            "applicable transport is missing closure unitarity"
                        )
                    stored_defects.append(closure_defect)
                for shell in point.shell_diagnostics:
                    stored_defects.append(
                        max(
                            0.0,
                            shell.reference_total.maximum_band
                            - math.sqrt(2.0)
                            * shell.reference_total.maximum_hamiltonian,
                            shell.comparison_total.maximum_band
                            - math.sqrt(2.0)
                            * shell.comparison_total.maximum_hamiltonian,
                            shell.reference_truncation.maximum_band
                            - math.sqrt(2.0)
                            * shell.reference_truncation.maximum_hamiltonian,
                            shell.comparison_truncation.maximum_band
                            - math.sqrt(2.0)
                            * shell.comparison_truncation.maximum_hamiltonian,
                            shell.reference_truncation_parseval_defect,
                            shell.comparison_truncation_parseval_defect,
                            abs(
                                shell.reference_total_omitted_power
                                - shell.reference_omitted_power
                                - point.reference_nyquist_power
                            ),
                            abs(
                                shell.comparison_total_omitted_power
                                - shell.comparison_omitted_power
                                - point.comparison_nyquist_power
                            ),
                        )
                    )
                shell_positions = {
                    shell.shell_index: index
                    for index, shell in enumerate(point.shell_diagnostics)
                }
                for decision in point.first_passing:
                    channels = (
                        (
                            "reference_band",
                            decision.reference_band_shell,
                            decision.reference_band_passing_error,
                            decision.reference_band_preceding_error,
                        ),
                        (
                            "comparison_band",
                            decision.comparison_band_shell,
                            decision.comparison_band_passing_error,
                            decision.comparison_band_preceding_error,
                        ),
                        (
                            "reference_hamiltonian",
                            decision.reference_hamiltonian_shell,
                            decision.reference_hamiltonian_passing_error,
                            decision.reference_hamiltonian_preceding_error,
                        ),
                        (
                            "comparison_hamiltonian",
                            decision.comparison_hamiltonian_shell,
                            decision.comparison_hamiltonian_passing_error,
                            decision.comparison_hamiltonian_preceding_error,
                        ),
                    )
                    for name, shell_index, passing, preceding in channels:
                        if shell_index is None:
                            stored_defects.append(
                                0.0 if passing is None and preceding is None else 1.0
                            )
                            continue
                        position = shell_positions[shell_index]
                        shell = point.shell_diagnostics[position]
                        errors = (
                            shell.reference_total
                            if name.startswith("reference")
                            else shell.comparison_total
                        )
                        expected_passing = (
                            errors.maximum_band
                            if name.endswith("band")
                            else errors.maximum_hamiltonian
                        )
                        assert passing is not None
                        stored_defects.extend(
                            (
                                abs(passing - expected_passing),
                                max(0.0, passing - decision.tolerance),
                            )
                        )
                        if position == 0:
                            stored_defects.append(0.0 if preceding is None else 1.0)
                        else:
                            previous = point.shell_diagnostics[position - 1]
                            previous_errors = (
                                previous.reference_total
                                if name.startswith("reference")
                                else previous.comparison_total
                            )
                            expected_preceding = (
                                previous_errors.maximum_band
                                if name.endswith("band")
                                else previous_errors.maximum_hamiltonian
                            )
                            assert preceding is not None
                            stored_defects.extend(
                                (
                                    abs(preceding - expected_preceding),
                                    max(0.0, decision.tolerance - preceding),
                                )
                            )
        independent_parent = 0.0
        independent_band = 0.0
        probes = tuple(
            0.137 * (index + 1) - 0.25 for index in range(definition.dimension)
        )
        coordinate = np.asarray(probes, dtype=np.float64).reshape(
            *((1,) * definition.dimension), definition.dimension
        )
        for case_definition, case_result in zip(
            definition.cases, result.cases, strict=True
        ):
            if case_definition.name != case_result.name:
                raise ValueError("case order or identity does not match definition")
            expected_point_identities = tuple(
                (parent_scale, amplitude)
                for parent_scale in definition.parent_scales
                for amplitude in definition.amplitudes
            )
            stored_point_identities = tuple(
                (point.parent_scale, point.amplitude) for point in case_result.points
            )
            if stored_point_identities != expected_point_identities:
                raise ValueError("point identities do not match the analysis request")
            construction = _coordinates(
                result.construction_size,
                definition.dimension,
                0.5,
            )
            for parent_scale in definition.parent_scales:
                parent_grid = _parent_field(case_definition, construction, parent_scale)
                frame_grid, _, _ = _retained_frame(parent_grid)
                expected_transport = frame_transport_diagnostics(
                    frame_grid,
                    case_definition.dimension,
                    definition.transport_rank_absolute,
                    definition.transport_rank_relative,
                )
                matching_points = tuple(
                    point
                    for point in case_result.points
                    if point.parent_scale == parent_scale
                )
                if len(matching_points) != len(definition.amplitudes):
                    raise ValueError(
                        "transport point inventory does not match definition"
                    )
                for point in matching_points:
                    stored_defects.extend(
                        _transport_record_defects(point, expected_transport)
                    )
                parent = _independent_parent(case_definition, probes, parent_scale)
                vectorized = _parent_field(
                    case_definition, coordinate, parent_scale
                ).reshape(4, 4)
                independent_parent = max(
                    independent_parent,
                    float(np.linalg.norm(parent - vectorized)),
                )
                frame, _, _ = _retained_frame(vectorized.reshape(1, 4, 4))
                retained = _retained_field(frame, vectorized.reshape(1, 4, 4))[0]
                for amplitude in definition.amplitudes:
                    theta = _independent_angle(case_definition, probes, amplitude)
                    cosine = math.cos(theta)
                    sine = math.sin(theta)
                    rotation = np.array(
                        [[cosine, -sine], [sine, cosine]], dtype=np.complex128
                    )
                    comparison = rotation.T @ retained @ rotation
                    independent_band = max(
                        independent_band,
                        float(
                            np.max(
                                np.abs(
                                    np.linalg.eigvalsh(retained)
                                    - np.linalg.eigvalsh(comparison)
                                )
                            )
                        ),
                    )
        maximum_stored = max(stored_defects, default=0.0)

        result_encoded = canonical_json_bytes(
            band_equivalence_locality_result_document(result)
        )
        passes = (
            maximum_stored <= 5.0e-11
            and independent_parent <= 5.0e-14
            and independent_band <= 5.0e-14
        )
        return BandEquivalenceLocalityVerificationResult(
            family=result.family,
            passes=passes,
            maximum_stored_identity_defect=maximum_stored,
            maximum_independent_parent_defect=independent_parent,
            maximum_independent_band_defect=independent_band,
            input_sha256=input_sha256,
            result_sha256=hashlib.sha256(result_encoded).hexdigest(),
        )


def _independent_parent(
    case: BandEquivalenceLocalityCase,
    coordinate: tuple[float, ...],
    parent_scale: float,
) -> ComplexArray:
    if case.parent_kind is ParentKind.DIRECTED_AXIS:
        phase = sum(
            complex(math.cos(math.tau * value), math.sin(math.tau * value))
            for value in coordinate
        ) / float(case.dimension)
        return _ONSITE + parent_scale * (
            phase * _DIRECTED + phase.conjugate() * _DIRECTED.conjugate().T
        )
    if case.parent_kind is ParentKind.HERMITIAN_BRAVAIS:
        structure = math.fsum(
            math.cos(
                math.tau
                * math.fsum(
                    value * component
                    for value, component in zip(coordinate, bond, strict=True)
                )
            )
            for bond in case.positive_bonds
        ) / float(len(case.positive_bonds))
        return _ONSITE + parent_scale * structure * _HERMITIAN_BOND
    gamma = (
        1.0
        + sum(
            complex(math.cos(-math.tau * value), math.sin(-math.tau * value))
            for value in coordinate
        )
    ) / float(case.dimension + 1)
    sublattice = np.array([[0.0, gamma], [gamma.conjugate(), 0.0]], dtype=np.complex128)
    result = np.zeros((4, 4), dtype=np.complex128)
    result[:2, :2] = -1.20 * np.eye(2) + parent_scale * 0.30 * sublattice
    result[2:, 2:] = 1.20 * np.eye(2) + parent_scale * 0.10 * sublattice
    result[:2, 2:] = 0.08 * np.eye(2)
    result[2:, :2] = 0.08 * np.eye(2)
    return result


def _independent_angle(
    case: BandEquivalenceLocalityCase, coordinate: tuple[float, ...], amplitude: float
) -> float:
    total = math.fsum(
        math.sin(
            math.tau
            * math.fsum(
                value * component
                for value, component in zip(coordinate, bond, strict=True)
            )
        )
        for bond in case.positive_bonds
    )
    if case.gauge_normalization is GaugeNormalization.AXIS_MAXIMUM:
        return amplitude * total / float(case.dimension)
    return amplitude * math.sqrt(2.0 / len(case.positive_bonds)) * total


__all__ = [
    "BandEquivalenceLocalityCalculator",
    "BandEquivalenceLocalityCase",
    "BandEquivalenceLocalityRequest",
    "BandEquivalenceLocalityFamily",
    "BandEquivalenceLocalityResult",
    "BandEquivalenceLocalityVerificationResult",
    "BandEquivalenceLocalityVerifier",
    "GaugeNormalization",
    "ParentKind",
]
