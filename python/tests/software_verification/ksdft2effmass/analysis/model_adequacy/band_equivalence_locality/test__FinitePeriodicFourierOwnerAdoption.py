"""Verify KSD adoption of the owner finite-periodic Fourier contracts."""

from __future__ import annotations

from typing import ClassVar

import numpy as np
import pytest
from numpy.typing import NDArray
from projectkoios.numerics.finite_periodic.meshes import CenteredUniformMesh
from projectkoios.numerics.finite_periodic.numpy.matrix_series import (
    NumpyFiniteFourierMatrixSeries,
)
from projectkoios.numerics.finite_periodic.numpy.tensor_product_evaluation import (
    NumpyTensorProductFourierMatrixEvaluationDefinition,
    NumpyTensorProductFourierMatrixSeriesEvaluator,
)
from projectkoios.numerics.finite_periodic.numpy.transform_diagnostics import (
    NumpyCenteredUniformMeshHermiticityAnalyzer,
    NumpyFinitePeriodicParsevalAnalyzer,
)
from projectkoios.numerics.finite_periodic.numpy.transforms import (
    NumpyCenteredUniformMeshMatrixFourierTransformDefinition,
    NumpyCenteredUniformMeshMatrixFourierTransformer,
)

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.fourier import (
    iter_complete_shell_fields,
)

type ComplexArray = NDArray[np.complex128]
type FloatArray = NDArray[np.float64]
type IntArray = NDArray[np.int64]


def _coordinates(size: int, dimension: int, offset: float) -> FloatArray:
    axis = -0.5 + (np.arange(size, dtype=np.float64) + offset) / float(size)
    return np.stack(np.meshgrid(*(axis,) * dimension, indexing="ij"), axis=-1)


def _coordinate_axes(coordinates: FloatArray) -> tuple[FloatArray, ...]:
    dimension = coordinates.shape[-1]
    if dimension == 2:
        return (coordinates[:, 0, 0], coordinates[0, :, 1])
    return (
        coordinates[:, 0, 0, 0],
        coordinates[0, :, 0, 1],
        coordinates[0, 0, :, 2],
    )


def _matrix_field(coordinates: FloatArray) -> ComplexArray:
    phase = 2.0 * np.pi * np.sum(coordinates, axis=-1)
    field = np.empty((*coordinates.shape[:-1], 2, 2), dtype=np.complex128)
    field[..., 0, 0] = 0.8 + 0.2 * np.cos(phase)
    field[..., 1, 1] = -0.3 + 0.1 * np.sin(phase)
    offdiagonal = 0.17 * np.exp(1.0j * phase)
    field[..., 0, 1] = offdiagonal
    field[..., 1, 0] = offdiagonal.conjugate()
    return field


def _direct_blocks(
    coordinates: FloatArray, field: ComplexArray, dimension: int, size: int
) -> tuple[IntArray, ComplexArray]:
    integer_axis = np.arange(-size // 2, size // 2, dtype=np.int64)
    displacements = np.stack(
        np.meshgrid(*(integer_axis,) * dimension, indexing="ij"), axis=-1
    ).reshape((-1, dimension))
    flat_coordinates = coordinates.reshape((-1, dimension))
    phases = np.exp(
        -2.0j * np.pi * np.einsum("rd,pd->rp", displacements, flat_coordinates)
    )
    blocks = np.einsum(
        "rp,pij->rij",
        phases,
        field.reshape((-1, 2, 2)),
        optimize=True,
    ) / float(size**dimension)
    return displacements, np.asarray(blocks, dtype=np.complex128)


def _direct_evaluation(
    displacements: IntArray, blocks: ComplexArray, coordinates: FloatArray
) -> ComplexArray:
    phases = np.exp(
        2.0j
        * np.pi
        * np.einsum(
            "...d,rd->...r",
            coordinates,
            displacements,
        )
    )
    return np.asarray(
        np.einsum("...r,rij->...ij", phases, blocks, optimize=True),
        dtype=np.complex128,
    )


class TestFinitePeriodicFourierOwnerAdoption:
    """Check origin phases, owner diagnostics, and KSD-selected shells."""

    dimensions: ClassVar[tuple[int, ...]] = (2, 3)

    @pytest.mark.parametrize("dimension", dimensions)
    def test_tensor_transform_matches_direct_finite_sum(self, dimension: int) -> None:
        size = 4
        coordinates = _coordinates(size, dimension, 0.5)
        field = _matrix_field(coordinates)

        mesh = CenteredUniformMesh(dimension, size, (0.5,) * dimension)
        definition = (
            NumpyCenteredUniformMeshMatrixFourierTransformDefinition.from_array(
                mesh,
                field,
            )
        )
        transform = NumpyCenteredUniformMeshMatrixFourierTransformer().transform(
            definition
        )
        displacements = transform.series.integer_modes
        blocks = transform.series.matrix_coefficients
        expected_displacements, expected_blocks = _direct_blocks(
            coordinates, field, dimension, size
        )

        assert np.array_equal(displacements, expected_displacements)
        assert blocks == pytest.approx(expected_blocks, abs=2.0e-15)
        reconstructed = (
            NumpyTensorProductFourierMatrixSeriesEvaluator()
            .evaluate(
                NumpyTensorProductFourierMatrixEvaluationDefinition.from_arrays(
                    mesh,
                    transform.series,
                    _coordinate_axes(coordinates),
                )
            )
            .matrix_values
        )
        assert reconstructed == pytest.approx(field, abs=2.0e-15)
        parseval = NumpyFinitePeriodicParsevalAnalyzer().analyze(
            definition,
            transform,
        )
        assert parseval.absolute_defect < 2.0e-15
        hermiticity = NumpyCenteredUniformMeshHermiticityAnalyzer().analyze(transform)
        assert hermiticity.twisted_cyclic_maximum_frobenius_defect < 2.0e-15
        assert hermiticity.ordinary_maximum_frobenius_defect < 2.0e-15

    @pytest.mark.parametrize("dimension", dimensions)
    def test_shell_fields_and_nyquist_power_match_direct_sums(
        self, dimension: int
    ) -> None:
        size = 4
        construction = _coordinates(size, dimension, 0.5)
        evaluation = _coordinates(5, dimension, 0.5 + 1.0 / 3.0)
        field = _matrix_field(construction)
        mesh = CenteredUniformMesh(dimension, size, (0.5,) * dimension)
        transform = NumpyCenteredUniformMeshMatrixFourierTransformer().transform(
            NumpyCenteredUniformMeshMatrixFourierTransformDefinition.from_array(
                mesh,
                field,
            )
        )
        displacements = transform.series.integer_modes
        blocks = transform.series.matrix_coefficients
        nyquist = np.any(displacements == -size // 2, axis=1)
        ordinary_displacements = displacements[~nyquist]
        ordinary_blocks = blocks[~nyquist]
        ordinary_series = NumpyFiniteFourierMatrixSeries.from_arrays(
            dimension,
            ordinary_displacements,
            ordinary_blocks,
        )
        metric_indices = np.sum(ordinary_displacements**2, axis=1)
        shells = tuple(int(value) for value in sorted(set(metric_indices.tolist())))

        observed_fields = tuple(
            iter_complete_shell_fields(
                mesh,
                ordinary_series,
                _coordinate_axes(evaluation),
                metric_indices,
                shells,
            )
        )

        for shell, observed in zip(shells, observed_fields, strict=True):
            retained = metric_indices <= shell
            expected = _direct_evaluation(
                ordinary_displacements[retained],
                ordinary_blocks[retained],
                evaluation,
            )
            assert observed == pytest.approx(expected, abs=3.0e-15)
        expected_nyquist_power = float(np.sum(np.abs(blocks[nyquist]) ** 2) / 2.0)
        assert expected_nyquist_power >= 0.0
