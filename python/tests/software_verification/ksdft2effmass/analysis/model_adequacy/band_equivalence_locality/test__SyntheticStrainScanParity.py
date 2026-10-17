"""Independent finite-sum parity for sampled synthetic-strain scan channels."""

import math
from itertools import product

import numpy as np
import pytest
from projectkoios.numerics.numpy.typing import Complex128Array as ComplexArray
from projectkoios.numerics.numpy.typing import Float64Array as FloatArray
from projectkoios.numerics.numpy.typing import Int64Array as IntArray

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain import (
    SyntheticStrainCalculator,
    SyntheticStrainPath,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain_response import (  # noqa: E501
    StrainWitnessControl,
    calculate_strain_witness_scan,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


def _dimension(path: SyntheticStrainPath) -> int:
    return 2 if path is SyntheticStrainPath.RHOMBIC_2D else 3


def _metric(path: SyntheticStrainPath, fraction: float) -> FloatArray:
    if path is SyntheticStrainPath.RHOMBIC_2D:
        angle = math.pi / 3.0 + fraction * math.pi / 6.0
        return np.asarray(
            ((1.0, math.cos(angle)), (math.cos(angle), 1.0)),
            dtype=np.float64,
        ) / math.sin(angle)
    ratio = math.sqrt(2.0) + fraction * (1.0 - math.sqrt(2.0))
    transverse = (2.0 / ratio) ** (1.0 / 3.0)
    longitudinal = ratio * transverse
    basis = np.column_stack(
        (
            (transverse / 2.0, transverse / 2.0, longitudinal / 2.0),
            (-transverse / 2.0, transverse / 2.0, longitudinal / 2.0),
            (transverse / 2.0, -transverse / 2.0, longitudinal / 2.0),
        )
    )
    return np.asarray(basis.T @ basis, dtype=np.float64)


def _bonds(path: SyntheticStrainPath) -> IntArray:
    if path is SyntheticStrainPath.RHOMBIC_2D:
        return np.asarray(((1, 0), (0, 1), (1, -1)), dtype=np.int64)
    return np.asarray(
        (
            (1, 0, 0),
            (1, -1, 0),
            (1, 0, -1),
            (1, -1, -1),
            (0, 1, 0),
            (0, 0, 1),
        ),
        dtype=np.int64,
    )


def _gauge_field(
    path: SyntheticStrainPath, size: int, amplitude: float
) -> tuple[FloatArray, ComplexArray]:
    dimension = _dimension(path)
    axis = -0.5 + (np.arange(size, dtype=np.float64) + 0.5) / float(size)
    coordinates = np.stack(np.meshgrid(*(axis,) * dimension, indexing="ij"), axis=-1)
    arguments = np.einsum(
        "...d,bd->...b",
        coordinates,
        _bonds(path).astype(np.float64),
    )
    angles = amplitude * np.mean(np.sin(2.0 * np.pi * arguments), axis=-1)
    field = np.empty((*angles.shape, 2, 2), dtype=np.complex128)
    field[..., 0, 0] = np.cos(2.0 * angles)
    field[..., 0, 1] = -np.sin(2.0 * angles)
    field[..., 1, 0] = -np.sin(2.0 * angles)
    field[..., 1, 1] = -np.cos(2.0 * angles)
    return coordinates, field


def _direct_fourier_power(
    coordinates: FloatArray, field: ComplexArray, size: int
) -> tuple[IntArray, FloatArray, float]:
    dimension = coordinates.shape[-1]
    integer_axis = range(-size // 2, size // 2)
    displacements = np.asarray(
        tuple(product(integer_axis, repeat=dimension)),
        dtype=np.int64,
    )
    flat_coordinates = coordinates.reshape((-1, dimension))
    flat_field = field.reshape((-1, 2, 2))
    phases = np.exp(
        -2.0j
        * np.pi
        * np.einsum(
            "qd,rd->qr",
            flat_coordinates,
            displacements.astype(np.float64),
        )
    )
    blocks = np.einsum("qr,qij->rij", phases, flat_field) / float(
        flat_coordinates.shape[0]
    )
    powers = np.sum(np.abs(blocks) ** 2, axis=(-2, -1)) / 2.0
    nyquist = np.any(displacements == -size // 2, axis=1)
    return (
        displacements[~nyquist],
        np.asarray(powers[~nyquist], dtype=np.float64),
        float(np.sum(powers[nyquist])),
    )


def _first_passing(
    squared_radii: FloatArray,
    powers: FloatArray,
    nyquist_power: float,
    tolerance: float,
) -> tuple[float | None, int | None]:
    order = np.argsort(squared_radii, kind="stable")
    cumulative = 0.0
    index = 0
    while index < order.size:
        radius_squared = float(squared_radii[order[index]])
        tie_tolerance = 1.0e-12 * max(1.0, abs(radius_squared))
        stop = index + 1
        while (
            stop < order.size
            and abs(float(squared_radii[order[stop]]) - radius_squared) <= tie_tolerance
        ):
            stop += 1
        cumulative += float(np.sum(powers[order[index:stop]]))
        if max(nyquist_power, 1.0 - cumulative) <= tolerance:
            retained = int(
                np.count_nonzero(squared_radii <= radius_squared + tie_tolerance)
            )
            return math.sqrt(max(0.0, radius_squared)), retained
        index = stop
    return None, None


def _independent_witness_requirements(
    path: SyntheticStrainPath,
    size: int,
    amplitude: float,
) -> tuple[float, float, float]:
    _, comparison = _gauge_field(path, size, amplitude)
    reference = np.broadcast_to(
        np.diag(np.asarray((1.0, -1.0), dtype=np.complex128)),
        comparison.shape,
    )

    def correlation(angle: float) -> float:
        rotation = np.asarray(
            (
                (math.cos(angle), -math.sin(angle)),
                (math.sin(angle), math.cos(angle)),
            ),
            dtype=np.complex128,
        )
        rotated = rotation.T @ reference @ rotation
        return float(
            np.mean(
                np.einsum(
                    "...ij,...ij->...",
                    rotated.conjugate(),
                    comparison,
                ).real
            )
            / 2.0
        )

    positive = correlation(math.pi / 4.0)
    negative = correlation(-math.pi / 4.0)
    constant = (positive + negative) / 2.0
    cosine = correlation(0.0) - constant
    sine = (positive - negative) / 2.0
    maximum_correlation = constant + math.hypot(cosine, sine)
    splitting_scale = 1.0
    optimized = math.sqrt(
        max(0.0, splitting_scale * (1.0 - max(0.0, maximum_correlation) ** 2))
    )
    fixed_candidate = math.sqrt(
        max(0.0, 2.0 * splitting_scale * (1.0 - maximum_correlation))
    )
    return maximum_correlation, optimized, fixed_candidate


class TestSyntheticStrainScanParity:
    """Reconstruct applicable scan channels without production-private helpers."""

    @pytest.mark.parametrize(
        "path",
        (SyntheticStrainPath.RHOMBIC_2D, SyntheticStrainPath.BAIN_3D),
    )
    def test_geometry_scan__explicit_finite_sum__reconstructs_first_passing_shells(
        self, path: SyntheticStrainPath
    ) -> None:
        fractions = (0.0, 0.5, 1.0)
        tolerances = (1.0e-1, 1.0e-2, 1.0e-3)
        size = 8
        amplitude = math.pi / 4.0
        result = SyntheticStrainCalculator().execute(
            path,
            size,
            fractions,
            amplitude,
            tolerances,
        )
        coordinates, field = _gauge_field(path, size, amplitude)
        displacements, powers, nyquist = _direct_fourier_power(
            coordinates,
            field,
            size,
        )

        for point in result.points:
            metric = _metric(path, point.strain_fraction)
            squared_radii = np.einsum(
                "ri,ij,rj->r",
                displacements.astype(np.float64),
                metric,
                displacements.astype(np.float64),
            )
            independently_reconstructed = tuple(
                _first_passing(squared_radii, powers, nyquist, tolerance)
                for tolerance in tolerances
            )
            assert point.first_passing_radius == pytest.approx(
                tuple(item[0] for item in independently_reconstructed),
                rel=0.0,
                abs=2.0e-14,
            )
            assert point.first_passing_blocks == tuple(
                item[1] for item in independently_reconstructed
            )
            assert np.linalg.det(metric) == pytest.approx(1.0, rel=0.0, abs=2e-15)

    @pytest.mark.parametrize(
        "path",
        (SyntheticStrainPath.RHOMBIC_2D, SyntheticStrainPath.BAIN_3D),
    )
    def test_witness_scan__independent_harmonic_reconstruction__matches_requirements(
        self, path: SyntheticStrainPath
    ) -> None:
        size = 8
        amplitude = math.pi / 4.0
        result = calculate_strain_witness_scan(
            path,
            StrainWitnessControl.GEOMETRY_ONLY,
            size,
            (0.0, 0.5, 1.0),
            amplitude,
        )
        correlation, optimized, fixed_candidate = _independent_witness_requirements(
            path,
            size,
            amplitude,
        )

        for point in result.points:
            assert point.volume_defect < 2.0e-15
            assert point.maximum_direct_band_defect < 3.0e-16
            assert point.finite_mesh_maximum_correlation == pytest.approx(
                correlation,
                rel=0.0,
                abs=2.0e-15,
            )
            assert point.pointwise_optimized_operator_threshold == pytest.approx(
                optimized,
                rel=0.0,
                abs=2.0e-15,
            )
            assert point.fixed_candidate_operator_threshold == pytest.approx(
                fixed_candidate,
                rel=0.0,
                abs=2.0e-15,
            )
