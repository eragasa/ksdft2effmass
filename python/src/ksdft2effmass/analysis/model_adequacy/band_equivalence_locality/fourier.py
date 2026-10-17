"""Matrix-free tensor Fourier conversion and complete-shell evaluation.

This module owns numerical representation mechanics only. It preserves exact mesh-origin
phases, twisted Nyquist relations, sparse shell streaming, and the separate
interpolation, truncation, and total-error channels. Family thresholds and evidence
dispositions remain with the development action.
"""

from __future__ import annotations

import math
from collections.abc import Iterator

import numpy as np
from numpy.typing import NDArray

from .records import ErrorChannels

type ComplexArray = NDArray[np.complex128]
type FloatArray = NDArray[np.float64]
type IntArray = NDArray[np.int64]


def fourier_blocks(
    field: ComplexArray, dimension: int, mesh_offset: float
) -> tuple[IntArray, ComplexArray]:
    """Transform one uniform mesh while retaining its exact origin phase."""
    size = field.shape[0]
    axes = tuple(range(dimension))
    coefficients = np.fft.fftshift(np.fft.fftn(field, axes=axes), axes=axes) / float(
        size**dimension
    )
    integer_axis = np.arange(-size // 2, size // 2, dtype=np.int64)
    displacements = np.stack(
        np.meshgrid(*(integer_axis,) * dimension, indexing="ij"), axis=-1
    )
    q_origin = -0.5 + mesh_offset / float(size)
    origin_phase = np.exp(-2.0j * np.pi * q_origin * np.sum(displacements, axis=-1))
    coefficients *= origin_phase[..., None, None]
    matrix_size = field.shape[-1]
    return (
        displacements.reshape((-1, dimension)),
        coefficients.reshape((-1, matrix_size, matrix_size)),
    )


def evaluate_blocks(
    displacements: IntArray,
    blocks: ComplexArray,
    coordinates: FloatArray,
    construction_size: int,
) -> ComplexArray:
    """Evaluate sparse tensor blocks without a dense point-by-block phase matrix."""
    dimension = coordinates.shape[-1]
    matrix_size = blocks.shape[-1]
    grid = np.zeros(
        (*(construction_size,) * dimension, matrix_size, matrix_size),
        dtype=np.complex128,
    )
    indices = tuple(
        (displacements[:, axis] + construction_size // 2).astype(np.int64)
        for axis in range(dimension)
    )
    grid[indices] = blocks
    integer = np.arange(-construction_size // 2, construction_size // 2)
    if dimension == 2:
        phase_first = np.exp(
            2.0j * np.pi * coordinates[:, 0, 0, None] * integer[None, :]
        )
        phase_second = np.exp(
            2.0j * np.pi * coordinates[0, :, 1, None] * integer[None, :]
        )
        return np.asarray(
            np.einsum(
                "ar,bs,rsij->abij",
                phase_first,
                phase_second,
                grid,
                optimize=True,
            ),
            dtype=np.complex128,
        )
    if dimension == 3:
        phase_first = np.exp(
            2.0j * np.pi * coordinates[:, 0, 0, 0, None] * integer[None, :]
        )
        phase_second = np.exp(
            2.0j * np.pi * coordinates[0, :, 0, 1, None] * integer[None, :]
        )
        phase_third = np.exp(
            2.0j * np.pi * coordinates[0, 0, :, 2, None] * integer[None, :]
        )
        intermediate = np.einsum("ar,rstij->astij", phase_first, grid, optimize=True)
        intermediate = np.einsum(
            "bs,astij->abtij", phase_second, intermediate, optimize=True
        )
        return np.asarray(
            np.einsum("ct,abtij->abcij", phase_third, intermediate, optimize=True),
            dtype=np.complex128,
        )
    raise ValueError("only two- and three-dimensional tensor meshes are supported")


def iter_shell_fields(
    displacements: IntArray,
    blocks: ComplexArray,
    coordinates: FloatArray,
    construction_size: int,
    metric_indices: IntArray,
    shells: tuple[int, ...],
) -> Iterator[ComplexArray]:
    """Yield cumulative shell fields while retaining only one field in memory."""
    dimension = coordinates.shape[-1]
    if dimension == 3:
        for shell in shells:
            selected = metric_indices <= shell
            yield evaluate_blocks(
                displacements[selected],
                blocks[selected],
                coordinates,
                construction_size,
            )
        return
    if dimension != 2:
        raise ValueError("only two- and three-dimensional tensor meshes are supported")

    flat_coordinates = coordinates.reshape((-1, dimension))
    matrix_size = blocks.shape[-1]
    cumulative = np.zeros(
        (flat_coordinates.shape[0], matrix_size, matrix_size), dtype=np.complex128
    )
    for shell in shells:
        selected = metric_indices == shell
        shell_displacements = displacements[selected]
        shell_blocks = blocks[selected]
        maximum_phase_elements = 1_000_000
        batch_size = max(1, maximum_phase_elements // max(1, shell_blocks.shape[0]))
        for start in range(0, flat_coordinates.shape[0], batch_size):
            stop = min(start + batch_size, flat_coordinates.shape[0])
            phases = np.exp(
                2.0j
                * np.pi
                * np.einsum(
                    "pd,rd->pr",
                    flat_coordinates[start:stop],
                    shell_displacements,
                )
            )
            cumulative[start:stop] += np.einsum(
                "pr,rij->pij", phases, shell_blocks, optimize=True
            )
        yield cumulative.reshape((*coordinates.shape[:-1], matrix_size, matrix_size))


def maximum_matrix_defect(left: ComplexArray, right: ComplexArray) -> float:
    return float(np.max(np.linalg.norm(left - right, axis=(-2, -1))))


def error_channels(approximation: ComplexArray, direct: ComplexArray) -> ErrorChannels:
    difference = approximation - direct
    matrix_norms = np.linalg.norm(difference, axis=(-2, -1)) / math.sqrt(2.0)
    approximation_bands = np.linalg.eigvalsh(approximation)
    direct_bands = np.linalg.eigvalsh(direct)
    band_difference = np.abs(approximation_bands - direct_bands)
    return ErrorChannels(
        maximum_hamiltonian=float(np.max(matrix_norms)),
        rms_hamiltonian=float(np.sqrt(np.mean(matrix_norms**2))),
        maximum_band=float(np.max(band_difference)),
        rms_band=float(np.sqrt(np.mean(band_difference**2))),
    )


def fourier_hermiticity_defects(
    size: int, displacements: IntArray, blocks: ComplexArray
) -> tuple[float, float]:
    """Return twisted cyclic and post-Nyquist ordinary Hermiticity defects."""
    lookup = {
        tuple(int(value) for value in displacement): block
        for displacement, block in zip(displacements, blocks, strict=True)
    }
    lower = -size // 2
    upper = size // 2 - 1
    twisted = 0.0
    ordinary = 0.0
    for displacement, block in zip(displacements, blocks, strict=True):
        target: list[int] = []
        wraps = 0
        boundary = False
        for value in displacement:
            negative = -int(value)
            if negative > upper:
                negative -= size
                wraps += 1
                boundary = True
            elif negative < lower:
                negative += size
                wraps += 1
                boundary = True
            target.append(negative)
        expected = ((-1.0) ** wraps) * block.conjugate().T
        defect = float(np.linalg.norm(lookup[tuple(target)] - expected))
        twisted = max(twisted, defect)
        if not boundary and not np.any(displacement == lower):
            ordinary = max(ordinary, defect)
    return twisted, ordinary


__all__ = [
    "error_channels",
    "evaluate_blocks",
    "fourier_blocks",
    "fourier_hermiticity_defects",
    "iter_shell_fields",
    "maximum_matrix_defect",
]
