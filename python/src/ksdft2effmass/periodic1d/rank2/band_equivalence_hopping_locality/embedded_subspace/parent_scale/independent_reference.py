"""Independent direct-formula reference for the embedded-subspace rank-two control.

The reference reconstructs the installed parent, spectral subspace, closed-loop polar
transport, represented operators, restricted alignment, and cyclic Fourier powers
without calling the production parent, transport, analysis, or Fourier owners.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array
from projectkoios.optimization.alignment.closed_loop_polar_transport import (
    ClosedLoopPolarFrameTransportStatus,
)
from projectkoios.optimization.selection.harmonic import (
    PeriodicHarmonic,
    PeriodicHarmonicMaximum,
    PeriodicHarmonicMaximumStatus,
)

from .request import Periodic1DRank2Request
from .results import (
    Periodic1DRank2Analysis,
    Periodic1DRank2BandTransportNumericallyUnresolved,
    Periodic1DRank2BandTransportThresholdFailure,
    Periodic1DRank2ExternalGapFailure,
    Periodic1DRank2HoppingPower,
    Periodic1DRank2PointAnalysis,
    Periodic1DRank2QualifiedParent,
)


@dataclass(frozen=True, slots=True)
class _IndependentTransportFailure:
    minimum_singular_value: float


@dataclass(frozen=True, slots=True)
class _IndependentTransport:
    frames: Complex128Array
    minimum_singular_value: float
    maximum_rank_cutoff: float
    maximum_unitarity_defect: float
    maximum_primitive_link_frobenius_residual: float
    closure_phases: tuple[float, float]
    closure_alignment_residual: float
    closure_alignment_unitarity_defect: float


class Periodic1DRank2IndependentReferenceAnalyzer:
    """Reconstruct all retained observations through independent finite formulas."""

    __slots__ = ("_request",)

    def __init__(self, request: Periodic1DRank2Request) -> None:
        if type(request) is not Periodic1DRank2Request:
            raise TypeError("request must be Periodic1DRank2Request")
        self._request = request

    def execute(self) -> Periodic1DRank2Analysis:
        """Return an independently reconstructed analysis for the installed model."""
        request = self._request
        size = request.reciprocal_mesh_size
        coordinates = np.asarray(
            tuple(-0.5 + float(index) / float(size) for index in range(size)),
            dtype=np.float64,
        )
        parent = _parent_matrices(coordinates, request.parent_hopping_scale)
        eigenvalues, eigenvectors = np.linalg.eigh(parent)
        minimum_gap = float(np.min(eigenvalues[:, 2] - eigenvalues[:, 1]))
        if minimum_gap < request.minimum_external_gap:
            return Periodic1DRank2Analysis(
                request=request,
                qualification=Periodic1DRank2ExternalGapFailure(minimum_gap),
                points=(),
            )

        transport = _closed_loop_transport(
            eigenvectors[:, :, :2],
            request,
        )
        if type(transport) is _IndependentTransportFailure:
            return Periodic1DRank2Analysis(
                request=request,
                qualification=(
                    Periodic1DRank2BandTransportNumericallyUnresolved(
                        minimum_external_gap=minimum_gap,
                        band_transport_status=(
                            ClosedLoopPolarFrameTransportStatus.RANK_DEFICIENT
                        ),
                        minimum_transport_singular_value=(
                            transport.minimum_singular_value
                        ),
                    )
                ),
                points=(),
            )
        if type(transport) is not _IndependentTransport:
            raise TypeError("independent transport returned an unknown variant")
        if transport.minimum_singular_value <= request.minimum_transport_singular_value:
            return Periodic1DRank2Analysis(
                request=request,
                qualification=(
                    Periodic1DRank2BandTransportThresholdFailure(
                        minimum_external_gap=minimum_gap,
                        minimum_transport_singular_value=(
                            transport.minimum_singular_value
                        ),
                    )
                ),
                points=(),
            )

        frames = transport.frames
        identity = np.eye(2, dtype=np.complex128)
        frame_defect = float(
            max(np.linalg.norm(frame.conj().T @ frame - identity) for frame in frames)
        )
        retained = np.asarray(
            _adjoint(frames) @ parent @ frames,
            dtype=np.complex128,
        )
        hermiticity_defect = float(np.max(np.abs(retained - _adjoint(retained))))
        means = np.asarray(
            np.trace(retained, axis1=1, axis2=2).real / 2.0,
            dtype=np.float64,
        )
        traceless = np.asarray(
            retained - means[:, None, None] * identity,
            dtype=np.complex128,
        )
        splitting_scale = float(
            np.mean(np.sum(np.abs(traceless) ** 2, axis=(1, 2))) / 2.0
        )
        reference_blocks = _direct_fourier_blocks(coordinates, retained)
        reference_powers = _normalized_powers(reference_blocks)
        reference_nonzero = math.fsum(
            power
            for displacement, power in zip(
                _representatives(coordinates.size),
                reference_powers,
                strict=True,
            )
            if displacement != 0
        )
        reference_parseval = _parseval_defect(retained, reference_powers)
        qualification = Periodic1DRank2QualifiedParent(
            minimum_external_gap=minimum_gap,
            minimum_transport_singular_value=transport.minimum_singular_value,
            maximum_transport_rank_cutoff=transport.maximum_rank_cutoff,
            maximum_transport_unitarity_defect=(transport.maximum_unitarity_defect),
            maximum_primitive_link_frobenius_residual=(
                transport.maximum_primitive_link_frobenius_residual
            ),
            closure_holonomy_phases=transport.closure_phases,
            closure_alignment_residual=transport.closure_alignment_residual,
            closure_alignment_unitarity_defect=(
                transport.closure_alignment_unitarity_defect
            ),
            maximum_frame_orthonormality_defect=frame_defect,
            maximum_reference_hermiticity_defect=hermiticity_defect,
        )
        points = tuple(
            _point(
                request=request,
                coordinates=coordinates,
                retained=retained,
                traceless=traceless,
                means=means,
                splitting_scale=splitting_scale,
                reference_powers=reference_powers,
                reference_nonzero=reference_nonzero,
                reference_parseval=reference_parseval,
                amplitude=amplitude,
            )
            for amplitude in request.amplitudes
        )
        return Periodic1DRank2Analysis(
            request=request,
            qualification=qualification,
            points=points,
        )


def _parent_matrices(coordinates: Float64Array, scale: float) -> Complex128Array:
    lower_onsite = np.asarray([[-1.20, 0.06], [0.06, -0.35]], dtype=np.complex128)
    upper_onsite = np.asarray([[1.00, 0.04], [0.04, 1.75]], dtype=np.complex128)
    lower_hopping = np.diag(np.asarray([0.15, -0.10])).astype(np.complex128)
    upper_hopping = np.diag(np.asarray([0.05, -0.04])).astype(np.complex128)
    coupling = np.diag(np.asarray([0.12, 0.10])).astype(np.complex128)
    matrices = np.empty((coordinates.size, 4, 4), dtype=np.complex128)
    for index, coordinate in enumerate(coordinates):
        phase = scale * np.exp(2.0j * np.pi * coordinate)
        matrices[index] = np.block(
            [
                [
                    lower_onsite
                    + phase * lower_hopping
                    + phase.conjugate() * lower_hopping.conj().T,
                    phase * coupling,
                ],
                [
                    phase.conjugate() * coupling.conj().T,
                    upper_onsite
                    + phase * upper_hopping
                    + phase.conjugate() * upper_hopping.conj().T,
                ],
            ]
        )
    return matrices


def _closed_loop_transport(
    raw_frames: Complex128Array,
    request: Periodic1DRank2Request,
) -> _IndependentTransport | _IndependentTransportFailure:
    point_count = raw_frames.shape[0]
    identity = np.eye(2, dtype=np.complex128)
    preliminary: list[Complex128Array] = [
        np.asarray(raw_frames[0], dtype=np.complex128)
    ]
    primitive_actions: list[Complex128Array] = [identity]
    singular_values: list[float] = []
    rank_cutoffs: list[float] = []
    unitarity_defects: list[float] = []
    for index in range(point_count - 1):
        action, link_singular_values, cutoff = _polar_right_action(
            raw_frames[index + 1], preliminary[index], request
        )
        singular_values.extend(float(value) for value in link_singular_values)
        rank_cutoffs.append(cutoff)
        if action is None:
            return _IndependentTransportFailure(
                minimum_singular_value=float(min(singular_values, default=0.0))
            )
        unitarity_defects.append(_unitarity_defect(action))
        primitive_actions.append(action)
        preliminary.append(
            np.asarray(raw_frames[index + 1] @ action, dtype=np.complex128)
        )

    closure_action, closure_singular_values, closure_cutoff = _polar_right_action(
        preliminary[-1], preliminary[0], request
    )
    singular_values.extend(float(value) for value in closure_singular_values)
    rank_cutoffs.append(closure_cutoff)
    if closure_action is None:
        return _IndependentTransportFailure(
            minimum_singular_value=float(min(singular_values, default=0.0))
        )
    unitarity_defects.append(_unitarity_defect(closure_action))
    endpoint_mismatch = np.asarray(closure_action.conj().T, dtype=np.complex128)
    eigenvalues, eigenvectors = np.linalg.eig(endpoint_mismatch)
    phases = np.angle(eigenvalues).astype(np.float64)
    phases[phases == -math.pi] = math.pi
    order = np.argsort(phases, kind="stable")
    phases = phases[order]
    vectors = np.asarray(eigenvectors[:, order], dtype=np.complex128)
    vectors /= np.linalg.norm(vectors, axis=0)[None, :]
    inverse_vectors = np.linalg.inv(vectors)
    frames = np.empty_like(raw_frames)
    for index, action in enumerate(primitive_actions):
        fraction = -float(index) / float(point_count)
        correction = _matrix_phase(vectors, inverse_vectors, phases, fraction)
        frames[index] = raw_frames[index] @ action @ correction
    primitive_residuals = [
        float(np.linalg.norm(preliminary[index] - preliminary[index - 1]))
        for index in range(1, point_count)
    ]
    primitive_residuals.append(
        float(np.linalg.norm(preliminary[-1] @ closure_action - preliminary[0]))
    )
    closure_residual = float(
        np.max(np.abs(preliminary[-1] @ closure_action - preliminary[0]))
    )
    return _IndependentTransport(
        frames=frames,
        minimum_singular_value=float(min(singular_values, default=0.0)),
        maximum_rank_cutoff=float(max(rank_cutoffs, default=0.0)),
        maximum_unitarity_defect=float(max(unitarity_defects, default=0.0)),
        maximum_primitive_link_frobenius_residual=float(
            max(primitive_residuals, default=0.0)
        ),
        closure_phases=(float(phases[0]), float(phases[1])),
        closure_alignment_residual=closure_residual,
        closure_alignment_unitarity_defect=_unitarity_defect(closure_action),
    )


def _polar_right_action(
    source: Complex128Array,
    target: Complex128Array,
    request: Periodic1DRank2Request,
) -> tuple[Complex128Array | None, Float64Array, float]:
    cross = np.asarray(source.conj().T @ target, dtype=np.complex128)
    gram_eigenvalues, gram_eigenvectors = np.linalg.eigh(cross.conj().T @ cross)
    singular_values = np.sqrt(np.maximum(gram_eigenvalues, 0.0))[::-1]
    cutoff = float(
        request.frame_absolute_tolerance
        + request.transport_rank_relative_tolerance * singular_values[0]
    )
    if bool(np.any(singular_values <= cutoff)):
        return None, np.asarray(singular_values, dtype=np.float64), cutoff
    inverse_sqrt = (
        gram_eigenvectors
        @ np.diag(1.0 / np.sqrt(gram_eigenvalues))
        @ gram_eigenvectors.conj().T
    )
    action = np.asarray(cross @ inverse_sqrt, dtype=np.complex128)
    return action, np.asarray(singular_values, dtype=np.float64), cutoff


def _matrix_phase(
    vectors: Complex128Array,
    inverse_vectors: Complex128Array,
    phases: Float64Array,
    fraction: float,
) -> Complex128Array:
    return np.asarray(
        vectors @ np.diag(np.exp(1.0j * phases * fraction)) @ inverse_vectors,
        dtype=np.complex128,
    )


def _unitarity_defect(matrix: Complex128Array) -> float:
    return float(np.max(np.abs(matrix.conj().T @ matrix - np.eye(2))))


def _independent_gauge_attack(
    coordinates: Float64Array,
    matrices: Complex128Array,
    amplitude: float,
) -> Complex128Array:
    theta = amplitude * np.sin(2.0 * np.pi * coordinates)
    rotations = np.empty((coordinates.size, 2, 2), dtype=np.complex128)
    rotations[:, 0, 0] = np.cos(theta)
    rotations[:, 0, 1] = -np.sin(theta)
    rotations[:, 1, 0] = np.sin(theta)
    rotations[:, 1, 1] = np.cos(theta)
    return np.asarray(_adjoint(rotations) @ matrices @ rotations)


def _point(
    *,
    request: Periodic1DRank2Request,
    coordinates: Float64Array,
    retained: Complex128Array,
    traceless: Complex128Array,
    means: Float64Array,
    splitting_scale: float,
    reference_powers: tuple[float, ...],
    reference_nonzero: float,
    reference_parseval: float,
    amplitude: float,
) -> Periodic1DRank2PointAnalysis:
    comparison = _independent_gauge_attack(coordinates, retained, amplitude)
    comparison_traceless = comparison - means[:, None, None] * np.eye(2)
    harmonic = _correlation_harmonic(traceless, comparison_traceless)
    maximum = _harmonic_maximum(harmonic, request)
    correlation = maximum.maximum_value / splitting_scale
    if amplitude == 0.0:
        # The declared gauge attack is exactly the identity at zero amplitude.
        correlation = 1.0
    roundoff_bound = 32.0 * math.ulp(1.0)
    if correlation > 1.0:
        if correlation - 1.0 > roundoff_bound:
            raise FloatingPointError("reference correlation exceeds one")
        correlation = 1.0
    elif correlation < -1.0:
        if -1.0 - correlation > roundoff_bound:
            raise FloatingPointError("reference correlation is below minus one")
        correlation = -1.0
    optimal_scale = max(0.0, correlation)
    minimum_squared_loss = splitting_scale * (1.0 - optimal_scale**2)
    angle = maximum.canonical_maximizing_argument or 0.0
    global_rotation = np.asarray(
        [[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]],
        dtype=np.complex128,
    )
    candidate = means[:, None, None] * np.eye(2) + optimal_scale * (
        global_rotation.conj().T @ traceless @ global_rotation
    )
    reconstructed_loss = float(
        np.mean(np.sum(np.abs(candidate - comparison) ** 2, axis=(1, 2))) / 2.0
    )
    comparison_blocks = _direct_fourier_blocks(coordinates, comparison)
    comparison_powers = _normalized_powers(comparison_blocks)
    representatives = _representatives(coordinates.size)
    paired_powers = tuple(
        Periodic1DRank2HoppingPower(
            displacement=int(displacement),
            reference_normalized_squared_frobenius_norm=reference_power,
            comparison_normalized_squared_frobenius_norm=comparison_power,
        )
        for displacement, reference_power, comparison_power in zip(
            representatives,
            reference_powers,
            comparison_powers,
            strict=True,
        )
    )
    return Periodic1DRank2PointAnalysis(
        amplitude=amplitude,
        maximum_band_defect=float(
            np.max(
                np.abs(np.linalg.eigvalsh(comparison) - np.linalg.eigvalsh(retained))
            )
        ),
        splitting_scale=splitting_scale,
        harmonic_maximum=maximum,
        discrete_maximum_correlation=float(correlation),
        minimum_operator_threshold=math.sqrt(max(0.0, minimum_squared_loss)),
        exact_spectrum_joint_operator_threshold=math.sqrt(
            max(0.0, 2.0 * splitting_scale * (1.0 - correlation))
        ),
        minimum_loss_reconstruction_defect=abs(
            reconstructed_loss - minimum_squared_loss
        ),
        reference_nonzero_hopping_weight=reference_nonzero,
        comparison_nonzero_hopping_weight=math.fsum(
            power
            for displacement, power in zip(
                representatives,
                comparison_powers,
                strict=True,
            )
            if displacement != 0
        ),
        reference_parseval_defect=reference_parseval,
        comparison_parseval_defect=_parseval_defect(comparison, comparison_powers),
        hopping_powers=paired_powers,
    )


def _correlation_harmonic(
    reference: Complex128Array,
    comparison: Complex128Array,
) -> PeriodicHarmonic:
    x_value = reference[:, 0, 1].real
    y_value = -reference[:, 0, 1].imag
    z_value = 0.5 * (reference[:, 0, 0].real - reference[:, 1, 1].real)
    target_x = comparison[:, 0, 1].real
    target_y = -comparison[:, 0, 1].imag
    target_z = 0.5 * (comparison[:, 0, 0].real - comparison[:, 1, 1].real)
    return PeriodicHarmonic(
        offset=float(np.mean(y_value * target_y)),
        cosine_coefficient=float(np.mean(x_value * target_x + z_value * target_z)),
        sine_coefficient=float(np.mean(x_value * target_z - z_value * target_x)),
        harmonic_order=2,
        fundamental_interval_start=-math.pi / 2.0,
    )


def _harmonic_maximum(
    harmonic: PeriodicHarmonic,
    request: Periodic1DRank2Request,
) -> PeriodicHarmonicMaximum:
    amplitude = math.hypot(
        harmonic.cosine_coefficient,
        harmonic.sine_coefficient,
    )
    maximum_value = harmonic.offset + amplitude
    cutoff = request.harmonic_absolute_degeneracy_tolerance + (
        request.harmonic_relative_degeneracy_tolerance
        * max(1.0, abs(harmonic.offset), amplitude)
    )
    if amplitude <= cutoff:
        argument = None
        status = PeriodicHarmonicMaximumStatus.NUMERICALLY_CONSTANT
    else:
        raw = math.atan2(
            harmonic.sine_coefficient,
            harmonic.cosine_coefficient,
        ) / float(harmonic.harmonic_order)
        argument = harmonic.fundamental_interval_start + (
            (raw - harmonic.fundamental_interval_start) % harmonic.fundamental_period
        )
        if argument >= harmonic.fundamental_interval_stop:
            argument = harmonic.fundamental_interval_start
        status = PeriodicHarmonicMaximumStatus.UNIQUE
    return PeriodicHarmonicMaximum(
        harmonic=harmonic,
        maximum_value=maximum_value,
        amplitude=amplitude,
        canonical_maximizing_argument=argument,
        fundamental_period=harmonic.fundamental_period,
        applied_degeneracy_cutoff=cutoff,
        status=status,
    )


def _representatives(
    point_count: int,
) -> np.ndarray[tuple[int], np.dtype[np.int64]]:
    return np.arange(-(point_count // 2), point_count // 2, dtype=np.int64)


def _direct_fourier_blocks(
    coordinates: Float64Array,
    matrices: Complex128Array,
) -> Complex128Array:
    representatives = _representatives(coordinates.size)
    phases = np.exp(-2.0j * np.pi * np.outer(coordinates, representatives))
    return np.asarray(
        np.einsum("kr,kij->rij", phases, matrices, optimize=True)
        / float(coordinates.size),
        dtype=np.complex128,
    )


def _normalized_powers(blocks: Complex128Array) -> tuple[float, ...]:
    return tuple(float(np.sum(np.abs(block) ** 2) / 2.0) for block in blocks)


def _parseval_defect(
    matrices: Complex128Array,
    powers: tuple[float, ...],
) -> float:
    reciprocal_power = float(np.mean(np.sum(np.abs(matrices) ** 2, axis=(1, 2))) / 2.0)
    return abs(reciprocal_power - math.fsum(powers))


def _adjoint(values: Complex128Array) -> Complex128Array:
    return np.swapaxes(values.conjugate(), -1, -2)


__all__ = [
    "Periodic1DRank2IndependentReferenceAnalyzer",
]
