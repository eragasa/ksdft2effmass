"""Bounded M1/M2 Hamiltonian diagnostics for synthetic finite-strain paths."""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum

import numpy as np
import numpy.typing as npt

from .fourier import evaluate_blocks, fourier_blocks
from .strain import (
    BAIN_DIAMOND_BASIS_OFFSETS,
    SyntheticStrainPath,
    _bonds,
    _metric,
    _path_parameter,
)

FloatArray = npt.NDArray[np.float64]
ComplexArray = npt.NDArray[np.complex128]
IntArray = npt.NDArray[np.int64]
BoolArray = npt.NDArray[np.bool_]

_SEED = np.eye(4, 2, dtype=np.complex128)


class StrainResponseModel(StrEnum):
    """Select a frozen or radial-response four-state strain control."""

    M1_FROZEN = "M1-frozen-four-state-bipartite"
    M2_RADIAL = "M2-fixed-radial-response"


@dataclass(frozen=True, slots=True)
class StrainErrorChannels:
    """Retain normalized matrix and sorted-band discrepancies."""

    maximum_hamiltonian: float
    rms_hamiltonian: float
    maximum_band: float
    rms_band: float


@dataclass(frozen=True, slots=True)
class StrainResponseCutoffDiagnostic:
    """Retain three-channel errors at one complete physical-radius support."""

    tail_tolerance: float
    physical_radius: float | None
    retained_blocks: int | None
    omitted_power: float
    truncation: StrainErrorChannels | None
    total: StrainErrorChannels | None
    delta_omitted_power: float
    delta_truncation: StrainErrorChannels | None
    delta_total: StrainErrorChannels | None


@dataclass(frozen=True, slots=True)
class StrainResponsePointDiagnostic:
    """Retain M1/M2 qualification and approximation channels at one strain."""

    strain_fraction: float
    path_parameter: float
    metric: tuple[tuple[float, ...], ...]
    minimum_parent_bond_length: float
    maximum_parent_bond_length: float
    minimum_hopping_response: float
    maximum_hopping_response: float
    minimum_sampled_external_isolation_gap: float
    minimum_seed_overlap: float
    minimum_frame_overlap_singular_value: float
    maximum_pointwise_frame_alignment_residual: float
    restricted_global_frame_alignment_residual: float
    aligned_strain_perturbation: StrainErrorChannels
    maximum_scalar_strain_component: float
    rms_scalar_strain_component: float
    maximum_traceless_strain_component: float
    rms_traceless_strain_component: float
    delta_onsite_power: float
    delta_offsite_power: float
    interpolation: StrainErrorChannels
    delta_interpolation: StrainErrorChannels
    nyquist_power: float
    delta_nyquist_power: float
    cutoffs: tuple[StrainResponseCutoffDiagnostic, ...]


@dataclass(frozen=True, slots=True)
class SyntheticStrainResponseResult:
    """Retain one bounded M1 or M2 strain-response sequence."""

    path: SyntheticStrainPath
    model: StrainResponseModel
    construction_size: int
    evaluation_size: int
    evaluation_shift: float
    maximum_rotation_amplitude: float
    radial_decay_beta: float
    tail_tolerances: tuple[float, ...]
    points: tuple[StrainResponsePointDiagnostic, ...]
    status: str = "bounded-synthetic-strain-response-development-not-retained-evidence"


def _dimension(path: SyntheticStrainPath) -> int:
    return 2 if path is SyntheticStrainPath.RHOMBIC_2D else 3


def _coordinates(size: int, dimension: int, offset: float) -> FloatArray:
    axis = -0.5 + (np.arange(size, dtype=np.float64) + offset) / float(size)
    return np.stack(np.meshgrid(*(axis,) * dimension, indexing="ij"), axis=-1)


def _parent_translations(path: SyntheticStrainPath) -> IntArray:
    if path is SyntheticStrainPath.RHOMBIC_2D:
        return np.asarray(((0, 0), (1, 0), (0, 1)), dtype=np.int64)
    return np.asarray(((0, 0, 0), (1, 0, 0), (0, 0, 1), (1, -1, 0)), dtype=np.int64)


def _basis_offset(path: SyntheticStrainPath) -> FloatArray:
    if path is SyntheticStrainPath.RHOMBIC_2D:
        return np.asarray((1.0 / 3.0, 1.0 / 3.0), dtype=np.float64)
    return np.asarray(BAIN_DIAMOND_BASIS_OFFSETS[1], dtype=np.float64)


def _bond_lengths(path: SyntheticStrainPath, metric: FloatArray) -> FloatArray:
    translations = _parent_translations(path).astype(np.float64)
    vectors = _basis_offset(path)[None, :] - translations
    squared = np.einsum("bi,ij,bj->b", vectors, metric, vectors)
    return np.sqrt(squared)


def _hopping_responses(
    path: SyntheticStrainPath,
    model: StrainResponseModel,
    fraction: float,
    beta: float,
) -> FloatArray:
    count = _dimension(path) + 1
    if model is StrainResponseModel.M1_FROZEN:
        return np.ones(count, dtype=np.float64)
    reference = _bond_lengths(path, _metric(path, 0.0))
    strained = _bond_lengths(path, _metric(path, fraction))
    return np.exp(-beta * (strained / reference - 1.0))


def _parent_field(
    path: SyntheticStrainPath,
    coordinates: FloatArray,
    responses: FloatArray,
) -> ComplexArray:
    translations = _parent_translations(path).astype(np.float64)
    arguments = np.einsum("...d,bd->...b", coordinates, translations)
    gamma = np.sum(responses * np.exp(-2.0j * np.pi * arguments), axis=-1) / float(
        len(translations)
    )
    shape = coordinates.shape[:-1]
    sublattice = np.empty((*shape, 2, 2), dtype=np.complex128)
    sublattice[..., 0, 0] = 0.0
    sublattice[..., 0, 1] = gamma
    sublattice[..., 1, 0] = gamma.conjugate()
    sublattice[..., 1, 1] = 0.0
    result = np.zeros((*shape, 4, 4), dtype=np.complex128)
    identity = np.eye(2, dtype=np.complex128)
    result[..., :2, :2] = -1.20 * identity + 0.30 * sublattice
    result[..., 2:, 2:] = 1.20 * identity + 0.10 * sublattice
    result[..., :2, 2:] = 0.08 * identity
    result[..., 2:, :2] = 0.08 * identity
    return result


def _retained_frame(
    parent: ComplexArray,
) -> tuple[ComplexArray, FloatArray, FloatArray]:
    eigenvalues, eigenvectors = np.linalg.eigh(parent)
    low = eigenvectors[..., :, :2]
    projector = low @ np.swapaxes(low.conjugate(), -1, -2)
    projected_seed = projector @ _SEED
    gram = np.swapaxes(projected_seed.conjugate(), -1, -2) @ projected_seed
    gram_values, gram_vectors = np.linalg.eigh(gram)
    inverse_root = (
        gram_vectors * (1.0 / np.sqrt(gram_values))[..., None, :]
    ) @ np.swapaxes(gram_vectors.conjugate(), -1, -2)
    return projected_seed @ inverse_root, eigenvalues, gram_values


def _retained_field(frame: ComplexArray, parent: ComplexArray) -> ComplexArray:
    return np.swapaxes(frame.conjugate(), -1, -2) @ parent @ frame


def _gauge_rotations(
    path: SyntheticStrainPath, coordinates: FloatArray, amplitude: float
) -> ComplexArray:
    bonds = _bonds(path).astype(np.float64)
    arguments = np.einsum("...d,bd->...b", coordinates, bonds)
    angles = amplitude * np.mean(np.sin(2.0 * np.pi * arguments), axis=-1)
    result = np.empty((*angles.shape, 2, 2), dtype=np.complex128)
    result[..., 0, 0] = np.cos(angles)
    result[..., 0, 1] = -np.sin(angles)
    result[..., 1, 0] = np.sin(angles)
    result[..., 1, 1] = np.cos(angles)
    return result


def _pointwise_alignment(
    moving: ComplexArray, reference: ComplexArray
) -> tuple[ComplexArray, float, float]:
    overlaps = np.swapaxes(moving.conjugate(), -1, -2) @ reference
    left, singular, right = np.linalg.svd(overlaps)
    unitaries = left @ right
    aligned = moving @ unitaries
    residual = float(np.max(np.linalg.norm(aligned - reference, axis=(-2, -1))))
    return unitaries, float(np.min(singular)), residual


def _global_alignment_residual(moving: ComplexArray, reference: ComplexArray) -> float:
    overlaps = np.swapaxes(moving.conjugate(), -1, -2) @ reference
    aggregate = np.sum(overlaps.reshape((-1, 2, 2)), axis=0)
    left, _, right = np.linalg.svd(aggregate)
    unitary = left @ right
    difference = moving @ unitary - reference
    return float(np.sqrt(np.mean(np.sum(np.abs(difference) ** 2, axis=(-2, -1))) / 2.0))


def _aligned_attacked_field(
    retained: ComplexArray, alignment: ComplexArray, rotations: ComplexArray
) -> ComplexArray:
    aligned = np.swapaxes(alignment.conjugate(), -1, -2) @ retained @ alignment
    return np.swapaxes(rotations.conjugate(), -1, -2) @ aligned @ rotations


def _errors(approximation: ComplexArray, direct: ComplexArray) -> StrainErrorChannels:
    difference = approximation - direct
    matrix = np.linalg.norm(difference, axis=(-2, -1)) / math.sqrt(2.0)
    band = np.abs(np.linalg.eigvalsh(approximation) - np.linalg.eigvalsh(direct))
    return StrainErrorChannels(
        maximum_hamiltonian=float(np.max(matrix)),
        rms_hamiltonian=float(np.sqrt(np.mean(matrix**2))),
        maximum_band=float(np.max(band)),
        rms_band=float(np.sqrt(np.mean(band**2))),
    )


def _powers(blocks: ComplexArray) -> FloatArray:
    return np.sum(np.abs(blocks) ** 2, axis=(-2, -1)) / 2.0


def _select_support(
    squared_radii: FloatArray,
    powers: FloatArray,
    nyquist_power: float,
    tolerance: float,
) -> tuple[BoolArray | None, float | None, int | None, float]:
    order = np.argsort(squared_radii, kind="stable")
    radii = squared_radii[order]
    ordered_power = powers[order]
    total = float(np.sum(powers)) + nyquist_power
    retained = 0.0
    index = 0
    while index < len(radii):
        radius = float(radii[index])
        stop = index + 1
        tie = 1.0e-12 * max(1.0, abs(radius))
        while stop < len(radii) and abs(float(radii[stop]) - radius) <= tie:
            stop += 1
        retained += float(np.sum(ordered_power[index:stop]))
        omitted = max(nyquist_power, total - retained)
        if omitted <= tolerance:
            support = squared_radii <= radius + tie
            return (
                support,
                math.sqrt(max(0.0, radius)),
                int(np.count_nonzero(support)),
                omitted,
            )
        index = stop
    return None, None, None, total


def _validate_definition(
    path: SyntheticStrainPath,
    model: StrainResponseModel,
    construction_size: int,
    evaluation_size: int,
    evaluation_shift: float,
    strain_fractions: tuple[float, ...],
    amplitude: float,
    beta: float,
    tail_tolerances: tuple[float, ...],
) -> None:
    if type(path) is not SyntheticStrainPath:
        raise TypeError("path must be SyntheticStrainPath")
    if type(model) is not StrainResponseModel:
        raise TypeError("model must be StrainResponseModel")
    if (
        type(construction_size) is not int
        or construction_size < 4
        or construction_size % 2
    ):
        raise ValueError(
            "construction_size must be an even built-in integer at least four"
        )
    if type(evaluation_size) is not int or evaluation_size < 3:
        raise ValueError("evaluation_size must be a built-in integer at least three")
    if type(evaluation_shift) is not float or not 0.0 < evaluation_shift < 1.0:
        raise ValueError("evaluation_shift must be a built-in float in (0, 1)")
    if not strain_fractions or strain_fractions != tuple(sorted(set(strain_fractions))):
        raise ValueError("strain_fractions must be nonempty, sorted, and unique")
    if any(
        type(value) is not float or not 0.0 <= value <= 1.0
        for value in strain_fractions
    ):
        raise ValueError("strain fractions must be built-in floats in [0, 1]")
    if type(amplitude) is not float or not 0.0 <= amplitude <= math.pi / 4.0:
        raise ValueError("amplitude must be a built-in float in [0, pi/4]")
    if type(beta) is not float or beta < 0.0:
        raise ValueError("beta must be a nonnegative built-in float")
    if model is StrainResponseModel.M1_FROZEN and beta != 0.0:
        raise ValueError("M1 requires beta=0")
    if model is StrainResponseModel.M2_RADIAL and beta != 1.0:
        raise ValueError("the frozen M2 development contract requires beta=1")
    if not tail_tolerances or any(
        type(value) is not float or value <= 0.0 for value in tail_tolerances
    ):
        raise ValueError("tail tolerances must be positive built-in floats")


def calculate_synthetic_strain_response(
    path: SyntheticStrainPath,
    model: StrainResponseModel,
    construction_size: int,
    evaluation_size: int,
    evaluation_shift: float,
    strain_fractions: tuple[float, ...],
    maximum_rotation_amplitude: float,
    radial_decay_beta: float,
    tail_tolerances: tuple[float, ...],
) -> SyntheticStrainResponseResult:
    """Calculate one bounded M1 or M2 synthetic strain-response sequence."""
    _validate_definition(
        path,
        model,
        construction_size,
        evaluation_size,
        evaluation_shift,
        strain_fractions,
        maximum_rotation_amplitude,
        radial_decay_beta,
        tail_tolerances,
    )
    dimension = _dimension(path)
    construction = _coordinates(construction_size, dimension, 0.5)
    evaluation = _coordinates(evaluation_size, dimension, 0.5 + evaluation_shift)
    rotations = _gauge_rotations(path, construction, maximum_rotation_amplitude)
    rotations_eval = _gauge_rotations(path, evaluation, maximum_rotation_amplitude)

    reference_responses = _hopping_responses(path, model, 0.0, radial_decay_beta)
    reference_parent = _parent_field(path, construction, reference_responses)
    reference_frame, _, _ = _retained_frame(reference_parent)
    reference_retained = _retained_field(reference_frame, reference_parent)
    reference_attacked = (
        np.swapaxes(rotations.conjugate(), -1, -2) @ reference_retained @ rotations
    )
    reference_parent_eval = _parent_field(path, evaluation, reference_responses)
    reference_frame_eval, _, _ = _retained_frame(reference_parent_eval)
    reference_retained_eval = _retained_field(
        reference_frame_eval, reference_parent_eval
    )
    reference_attacked_eval = (
        np.swapaxes(rotations_eval.conjugate(), -1, -2)
        @ reference_retained_eval
        @ rotations_eval
    )

    points: list[StrainResponsePointDiagnostic] = []
    for fraction in strain_fractions:
        metric = _metric(path, fraction)
        responses = _hopping_responses(path, model, fraction, radial_decay_beta)
        parent = _parent_field(path, construction, responses)
        frame, eigenvalues, seed_values = _retained_frame(parent)
        retained = _retained_field(frame, parent)
        alignment, minimum_singular, pointwise_residual = _pointwise_alignment(
            frame, reference_frame
        )
        attacked = _aligned_attacked_field(retained, alignment, rotations)

        parent_eval = _parent_field(path, evaluation, responses)
        frame_eval, _, _ = _retained_frame(parent_eval)
        retained_eval = _retained_field(frame_eval, parent_eval)
        alignment_eval, _, _ = _pointwise_alignment(frame_eval, reference_frame_eval)
        attacked_eval = _aligned_attacked_field(
            retained_eval, alignment_eval, rotations_eval
        )
        delta = attacked - reference_attacked
        delta_eval = attacked_eval - reference_attacked_eval

        displacements, blocks = fourier_blocks(attacked, dimension, 0.5)
        delta_displacements, delta_blocks = fourier_blocks(delta, dimension, 0.5)
        if not np.array_equal(displacements, delta_displacements):
            raise RuntimeError("Hamiltonian and strain-difference inventories differ")
        nyquist = np.any(displacements == -construction_size // 2, axis=1)
        ordinary_displacements = displacements[~nyquist]
        ordinary_blocks = blocks[~nyquist]
        ordinary_delta_blocks = delta_blocks[~nyquist]
        power = _powers(ordinary_blocks)
        delta_power = _powers(ordinary_delta_blocks)
        onsite = np.all(ordinary_displacements == 0, axis=1)
        nyquist_power = float(np.sum(_powers(blocks[nyquist])))
        delta_nyquist_power = float(np.sum(_powers(delta_blocks[nyquist])))
        full_eval = evaluate_blocks(
            ordinary_displacements, ordinary_blocks, evaluation, construction_size
        )
        full_delta_eval = evaluate_blocks(
            ordinary_displacements,
            ordinary_delta_blocks,
            evaluation,
            construction_size,
        )
        interpolation = _errors(full_eval, attacked_eval)
        delta_interpolation = _errors(full_delta_eval, delta_eval)
        squared_radii = np.einsum(
            "ri,ij,rj->r", ordinary_displacements, metric, ordinary_displacements
        )

        cutoffs: list[StrainResponseCutoffDiagnostic] = []
        for tolerance in tail_tolerances:
            support, radius, count, omitted = _select_support(
                squared_radii, power, nyquist_power, tolerance
            )
            if support is None:
                cutoffs.append(
                    StrainResponseCutoffDiagnostic(
                        tail_tolerance=tolerance,
                        physical_radius=None,
                        retained_blocks=None,
                        omitted_power=omitted,
                        truncation=None,
                        total=None,
                        delta_omitted_power=float(np.sum(delta_power))
                        + delta_nyquist_power,
                        delta_truncation=None,
                        delta_total=None,
                    )
                )
                continue
            truncated_eval = evaluate_blocks(
                ordinary_displacements[support],
                ordinary_blocks[support],
                evaluation,
                construction_size,
            )
            truncated_delta_eval = evaluate_blocks(
                ordinary_displacements[support],
                ordinary_delta_blocks[support],
                evaluation,
                construction_size,
            )
            delta_omitted = float(np.sum(delta_power[~support])) + delta_nyquist_power
            cutoffs.append(
                StrainResponseCutoffDiagnostic(
                    tail_tolerance=tolerance,
                    physical_radius=radius,
                    retained_blocks=count,
                    omitted_power=omitted,
                    truncation=_errors(truncated_eval, full_eval),
                    total=_errors(truncated_eval, attacked_eval),
                    delta_omitted_power=delta_omitted,
                    delta_truncation=_errors(truncated_delta_eval, full_delta_eval),
                    delta_total=_errors(truncated_delta_eval, delta_eval),
                )
            )

        trace = np.trace(delta_eval, axis1=-2, axis2=-1) / 2.0
        traceless = delta_eval - trace[..., None, None] * np.eye(2, dtype=np.complex128)
        scalar_magnitude = np.abs(trace)
        traceless_magnitude = np.linalg.norm(traceless, axis=(-2, -1)) / math.sqrt(2.0)
        lengths = _bond_lengths(path, metric)
        points.append(
            StrainResponsePointDiagnostic(
                strain_fraction=fraction,
                path_parameter=_path_parameter(path, fraction),
                metric=tuple(tuple(float(value) for value in row) for row in metric),
                minimum_parent_bond_length=float(np.min(lengths)),
                maximum_parent_bond_length=float(np.max(lengths)),
                minimum_hopping_response=float(np.min(responses)),
                maximum_hopping_response=float(np.max(responses)),
                minimum_sampled_external_isolation_gap=float(
                    np.min(eigenvalues[..., 2] - eigenvalues[..., 1])
                ),
                minimum_seed_overlap=float(np.min(seed_values)),
                minimum_frame_overlap_singular_value=minimum_singular,
                maximum_pointwise_frame_alignment_residual=pointwise_residual,
                restricted_global_frame_alignment_residual=_global_alignment_residual(
                    frame, reference_frame
                ),
                aligned_strain_perturbation=_errors(
                    attacked_eval, reference_attacked_eval
                ),
                maximum_scalar_strain_component=float(np.max(scalar_magnitude)),
                rms_scalar_strain_component=float(
                    np.sqrt(np.mean(scalar_magnitude**2))
                ),
                maximum_traceless_strain_component=float(np.max(traceless_magnitude)),
                rms_traceless_strain_component=float(
                    np.sqrt(np.mean(traceless_magnitude**2))
                ),
                delta_onsite_power=float(np.sum(delta_power[onsite])),
                delta_offsite_power=float(np.sum(delta_power[~onsite]))
                + delta_nyquist_power,
                interpolation=interpolation,
                delta_interpolation=delta_interpolation,
                nyquist_power=nyquist_power,
                delta_nyquist_power=delta_nyquist_power,
                cutoffs=tuple(cutoffs),
            )
        )
    return SyntheticStrainResponseResult(
        path=path,
        model=model,
        construction_size=construction_size,
        evaluation_size=evaluation_size,
        evaluation_shift=evaluation_shift,
        maximum_rotation_amplitude=maximum_rotation_amplitude,
        radial_decay_beta=radial_decay_beta,
        tail_tolerances=tail_tolerances,
        points=tuple(points),
    )


__all__ = [
    "StrainErrorChannels",
    "StrainResponseCutoffDiagnostic",
    "StrainResponseModel",
    "StrainResponsePointDiagnostic",
    "SyntheticStrainResponseResult",
    "calculate_synthetic_strain_response",
]
