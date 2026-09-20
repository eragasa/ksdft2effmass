"""Projected reciprocal operators and one-dimensional hopping transforms."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.operators import (
    MODEL_SYSTEM_UNIT_CONVERTER,
    ComplexMatrixQuantity,
    ScalarQuantity,
    VectorQuantity,
)

from .band_frames import ReciprocalBandFramePath1D
from .reciprocal_paths import CenteredUniformReciprocalMesh1D


@dataclass(frozen=True, slots=True, eq=False)
class ReciprocalOperatorSamples1D:
    """Retain square represented operators at ordered reciprocal coordinates."""

    coordinates: VectorQuantity
    reciprocal_period: ScalarQuantity
    matrices: tuple[ComplexMatrixQuantity, ...]

    def __post_init__(self) -> None:
        """Validate coordinate, period, matrix-shape, and unit consistency."""
        if type(self.coordinates) is not VectorQuantity:
            raise TypeError("coordinates must be VectorQuantity")
        if type(self.reciprocal_period) is not ScalarQuantity:
            raise TypeError("reciprocal_period must be ScalarQuantity")
        if self.reciprocal_period.magnitude <= 0.0:
            raise ValueError("reciprocal_period must be positive")
        converter = MODEL_SYSTEM_UNIT_CONVERTER
        if not converter.compatible(self.coordinates.unit, self.reciprocal_period.unit):
            raise ValueError("coordinates and reciprocal_period must be compatible")
        object.__setattr__(
            self,
            "coordinates",
            converter.convert_vector(self.coordinates, self.reciprocal_period.unit),
        )
        if not isinstance(self.matrices, tuple) or not self.matrices:
            raise TypeError("matrices must be a nonempty tuple")
        if len(self.matrices) != self.coordinates.magnitude.size:
            raise ValueError("matrix count must equal coordinate count")
        first = self.matrices[0]
        if type(first) is not ComplexMatrixQuantity:
            raise TypeError("every matrix must be ComplexMatrixQuantity")
        dimension = first.magnitude.shape[0]
        if dimension == 0 or first.magnitude.shape != (dimension, dimension):
            raise ValueError("matrices must be nonempty and square")
        for matrix in self.matrices:
            if type(matrix) is not ComplexMatrixQuantity:
                raise TypeError("every matrix must be ComplexMatrixQuantity")
            if matrix.magnitude.shape != (dimension, dimension):
                raise ValueError("all matrices must have equal square shape")
            if matrix.unit != first.unit:
                raise ValueError("all matrices must use the same unit")

    @property
    def matrix_dimension(self) -> int:
        """Return the represented matrix dimension."""
        return int(self.matrices[0].magnitude.shape[0])


class BandProjectedOperatorPathConstructor1D:
    """Project parent reciprocal operators into a compatible band-frame path."""

    __slots__ = ()

    def execute(
        self,
        parent: ReciprocalOperatorSamples1D,
        frames: ReciprocalBandFramePath1D,
        coordinate_absolute_tolerance: float,
    ) -> ReciprocalOperatorSamples1D:
        """Return ``F(k)^dagger A(k) F(k)`` at every ordered sample."""
        if type(parent) is not ReciprocalOperatorSamples1D:
            raise TypeError("parent must be ReciprocalOperatorSamples1D")
        if type(frames) is not ReciprocalBandFramePath1D:
            raise TypeError("frames must be ReciprocalBandFramePath1D")
        if type(coordinate_absolute_tolerance) is not float:
            raise TypeError("coordinate_absolute_tolerance must be a built-in float")
        if (
            not np.isfinite(coordinate_absolute_tolerance)
            or coordinate_absolute_tolerance < 0.0
        ):
            raise ValueError(
                "coordinate_absolute_tolerance must be finite and nonnegative"
            )
        mesh_coordinates = MODEL_SYSTEM_UNIT_CONVERTER.convert_vector(
            frames.mesh.coordinates, parent.reciprocal_period.unit
        )
        if parent.coordinates.magnitude.shape != mesh_coordinates.magnitude.shape:
            raise ValueError("parent and frame coordinate counts must agree")
        coordinate_defect = float(
            np.max(np.abs(parent.coordinates.magnitude - mesh_coordinates.magnitude))
        )
        if coordinate_defect > coordinate_absolute_tolerance:
            raise ValueError("parent and frame coordinates do not agree")
        if parent.matrix_dimension != frames.ambient_dimension:
            raise ValueError("parent matrix and frame ambient dimensions must agree")
        projected = tuple(
            ComplexMatrixQuantity(
                frame.magnitude.conj().T @ matrix.magnitude @ frame.magnitude,
                matrix.unit,
            )
            for matrix, frame in zip(parent.matrices, frames.frames, strict=True)
        )
        return ReciprocalOperatorSamples1D(
            parent.coordinates, parent.reciprocal_period, projected
        )


@dataclass(frozen=True, slots=True, eq=False)
class BlockHoppingModel1D:
    """Represent matrix-valued cell hoppings in ordered integer representatives."""

    reciprocal_period: ScalarQuantity
    representatives: tuple[int, ...]
    hopping_blocks: tuple[ComplexMatrixQuantity, ...]

    def __post_init__(self) -> None:
        """Validate representative ordering and homogeneous block matrices."""
        if type(self.reciprocal_period) is not ScalarQuantity:
            raise TypeError("reciprocal_period must be ScalarQuantity")
        if self.reciprocal_period.magnitude <= 0.0:
            raise ValueError("reciprocal_period must be positive")
        if not isinstance(self.representatives, tuple) or not self.representatives:
            raise TypeError("representatives must be a nonempty tuple")
        if any(type(value) is not int for value in self.representatives):
            raise TypeError("representatives must contain built-in integers")
        if tuple(sorted(set(self.representatives))) != self.representatives:
            raise ValueError("representatives must be unique and strictly increasing")
        if not isinstance(self.hopping_blocks, tuple) or len(
            self.hopping_blocks
        ) != len(self.representatives):
            raise ValueError("one hopping block is required per representative")
        first = self.hopping_blocks[0]
        if type(first) is not ComplexMatrixQuantity:
            raise TypeError("every hopping block must be ComplexMatrixQuantity")
        dimension = first.magnitude.shape[0]
        if dimension == 0 or first.magnitude.shape != (dimension, dimension):
            raise ValueError("hopping blocks must be nonempty and square")
        for block in self.hopping_blocks:
            if type(block) is not ComplexMatrixQuantity:
                raise TypeError("every hopping block must be ComplexMatrixQuantity")
            if block.magnitude.shape != (dimension, dimension):
                raise ValueError("all hopping blocks must have equal square shape")
            if block.unit != first.unit:
                raise ValueError("all hopping blocks must use the same unit")

    @property
    def matrix_dimension(self) -> int:
        """Return the orbital dimension of each hopping block."""
        return int(self.hopping_blocks[0].magnitude.shape[0])

    @property
    def maximum_range(self) -> int:
        """Return the largest absolute represented cell displacement."""
        return max(abs(value) for value in self.representatives)


@dataclass(frozen=True, slots=True, eq=False)
class ReciprocalOperatorFourierTransformResult1D:
    """Retain a complete uniform-mesh transform and reconstruction check."""

    source: ReciprocalOperatorSamples1D
    mesh: CenteredUniformReciprocalMesh1D
    hopping_model: BlockHoppingModel1D
    reconstructed: ReciprocalOperatorSamples1D
    coordinate_absolute_tolerance: float
    reconstruction_maximum_frobenius_error: float
    reconstruction_absolute_tolerance: float
    reconstruction_passes: bool

    def __post_init__(self) -> None:
        """Validate transform correlations and reconstruction disposition."""
        if type(self.source) is not ReciprocalOperatorSamples1D:
            raise TypeError("source must be ReciprocalOperatorSamples1D")
        if type(self.mesh) is not CenteredUniformReciprocalMesh1D:
            raise TypeError("mesh must be CenteredUniformReciprocalMesh1D")
        if type(self.hopping_model) is not BlockHoppingModel1D:
            raise TypeError("hopping_model must be BlockHoppingModel1D")
        if type(self.reconstructed) is not ReciprocalOperatorSamples1D:
            raise TypeError("reconstructed must be ReciprocalOperatorSamples1D")
        if type(self.coordinate_absolute_tolerance) is not float:
            raise TypeError("coordinate_absolute_tolerance must be a built-in float")
        if (
            not np.isfinite(self.coordinate_absolute_tolerance)
            or self.coordinate_absolute_tolerance < 0.0
        ):
            raise ValueError(
                "coordinate_absolute_tolerance must be finite and nonnegative"
            )
        if type(self.reconstruction_maximum_frobenius_error) is not float:
            raise TypeError(
                "reconstruction_maximum_frobenius_error must be a built-in float"
            )
        if (
            not np.isfinite(self.reconstruction_maximum_frobenius_error)
            or self.reconstruction_maximum_frobenius_error < 0.0
        ):
            raise ValueError(
                "reconstruction_maximum_frobenius_error must be finite and nonnegative"
            )
        if type(self.reconstruction_absolute_tolerance) is not float:
            raise TypeError(
                "reconstruction_absolute_tolerance must be a built-in float"
            )
        if (
            not np.isfinite(self.reconstruction_absolute_tolerance)
            or self.reconstruction_absolute_tolerance < 0.0
        ):
            raise ValueError(
                "reconstruction_absolute_tolerance must be finite and nonnegative"
            )
        if type(self.reconstruction_passes) is not bool:
            raise TypeError("reconstruction_passes must be a built-in bool")
        expected = (
            self.reconstruction_maximum_frobenius_error
            <= self.reconstruction_absolute_tolerance
        )
        if self.reconstruction_passes is not expected:
            raise ValueError("reconstruction_passes must match error and tolerance")
        if self.source.matrix_dimension != self.hopping_model.matrix_dimension:
            raise ValueError("source and hopping-model matrix dimensions must agree")
        if self.reconstructed.matrix_dimension != self.source.matrix_dimension:
            raise ValueError("source and reconstructed matrix dimensions must agree")
        if self.hopping_model.representatives != (
            self.mesh.centered_cell_representatives
        ):
            raise ValueError(
                "complete transform must retain the centered mesh representatives"
            )
        expected_coordinates = MODEL_SYSTEM_UNIT_CONVERTER.convert_vector(
            self.mesh.coordinates, self.source.reciprocal_period.unit
        )
        if (
            self.source.coordinates.magnitude.shape
            != expected_coordinates.magnitude.shape
        ):
            raise ValueError("source must contain every mesh coordinate")
        if (
            float(
                np.max(
                    np.abs(
                        self.source.coordinates.magnitude
                        - expected_coordinates.magnitude
                    )
                )
            )
            > self.coordinate_absolute_tolerance
        ):
            raise ValueError("source coordinates do not match the declared mesh")
        reconstructed_coordinates = MODEL_SYSTEM_UNIT_CONVERTER.convert_vector(
            self.reconstructed.coordinates, self.source.reciprocal_period.unit
        )
        if not np.array_equal(
            reconstructed_coordinates.magnitude, self.source.coordinates.magnitude
        ):
            raise ValueError("reconstructed coordinates must equal source coordinates")
        measured_error = float(
            max(
                np.linalg.norm(candidate.magnitude - reference.magnitude)
                for candidate, reference in zip(
                    self.reconstructed.matrices, self.source.matrices, strict=True
                )
            )
        )
        if measured_error != self.reconstruction_maximum_frobenius_error:
            raise ValueError(
                "reconstruction_maximum_frobenius_error must match represented values"
            )


class BlockHoppingInterpolator1D:
    """Evaluate a finite or complete hopping model at reciprocal coordinates."""

    __slots__ = ()

    def execute(
        self, model: BlockHoppingModel1D, coordinates: VectorQuantity
    ) -> ReciprocalOperatorSamples1D:
        """Evaluate ``sum_R exp(i 2π R k/G) T_R`` without diagonalization."""
        if type(model) is not BlockHoppingModel1D:
            raise TypeError("model must be BlockHoppingModel1D")
        if type(coordinates) is not VectorQuantity:
            raise TypeError("coordinates must be VectorQuantity")
        converted = MODEL_SYSTEM_UNIT_CONVERTER.convert_vector(
            coordinates, model.reciprocal_period.unit
        )
        representatives = np.asarray(model.representatives, dtype=np.float64)
        phases = np.exp(
            2j
            * np.pi
            * np.outer(
                converted.magnitude / model.reciprocal_period.magnitude,
                representatives,
            )
        )
        blocks = np.asarray(
            [block.magnitude for block in model.hopping_blocks],
            dtype=np.complex128,
        )
        matrices = np.einsum("kr,rij->kij", phases, blocks, optimize=True)
        return ReciprocalOperatorSamples1D(
            converted,
            model.reciprocal_period,
            tuple(
                ComplexMatrixQuantity(matrix, model.hopping_blocks[0].unit)
                for matrix in matrices
            ),
        )


class ReciprocalOperatorFourierTransformer1D:
    """Transform complete centered uniform reciprocal samples to cell hoppings."""

    __slots__ = ()

    def execute(
        self,
        source: ReciprocalOperatorSamples1D,
        mesh: CenteredUniformReciprocalMesh1D,
        coordinate_absolute_tolerance: float,
        reconstruction_absolute_tolerance: float,
    ) -> ReciprocalOperatorFourierTransformResult1D:
        """Apply the exact finite-mesh Fourier pair and assess reconstruction."""
        if type(source) is not ReciprocalOperatorSamples1D:
            raise TypeError("source must be ReciprocalOperatorSamples1D")
        if type(mesh) is not CenteredUniformReciprocalMesh1D:
            raise TypeError("mesh must be CenteredUniformReciprocalMesh1D")
        for name, tolerance in (
            ("coordinate_absolute_tolerance", coordinate_absolute_tolerance),
            ("reconstruction_absolute_tolerance", reconstruction_absolute_tolerance),
        ):
            if type(tolerance) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not np.isfinite(tolerance) or tolerance < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
        expected_coordinates = MODEL_SYSTEM_UNIT_CONVERTER.convert_vector(
            mesh.coordinates, source.reciprocal_period.unit
        )
        if source.coordinates.magnitude.shape != expected_coordinates.magnitude.shape:
            raise ValueError("source must contain every mesh coordinate")
        coordinate_defect = float(
            np.max(
                np.abs(source.coordinates.magnitude - expected_coordinates.magnitude)
            )
        )
        if coordinate_defect > coordinate_absolute_tolerance:
            raise ValueError("source coordinates do not match the declared mesh")
        representatives = mesh.centered_cell_representatives
        representative_array = np.asarray(representatives, dtype=np.int64)
        matrices = np.asarray(
            [matrix.magnitude for matrix in source.matrices], dtype=np.complex128
        )
        standard_order = np.fft.fft(matrices, axis=0, norm="forward")
        blocks = np.fft.fftshift(standard_order, axes=0)
        centered_origin_phase = np.where(
            np.remainder(representative_array, 2) == 0,
            1.0,
            -1.0,
        )
        blocks *= centered_origin_phase[:, np.newaxis, np.newaxis]
        model = BlockHoppingModel1D(
            source.reciprocal_period,
            representatives,
            tuple(
                ComplexMatrixQuantity(block, source.matrices[0].unit)
                for block in blocks
            ),
        )
        reconstructed = BlockHoppingInterpolator1D().execute(model, source.coordinates)
        error = float(
            max(
                np.linalg.norm(candidate.magnitude - reference.magnitude)
                for candidate, reference in zip(
                    reconstructed.matrices, source.matrices, strict=True
                )
            )
        )
        return ReciprocalOperatorFourierTransformResult1D(
            source,
            mesh,
            model,
            reconstructed,
            coordinate_absolute_tolerance,
            error,
            reconstruction_absolute_tolerance,
            error <= reconstruction_absolute_tolerance,
        )


@dataclass(frozen=True, slots=True, eq=False)
class BlockHoppingTruncationResult1D:
    """Retain one symmetric finite-range truncation and omitted-block norm."""

    source: BlockHoppingModel1D
    maximum_range: int
    truncated: BlockHoppingModel1D
    omitted_block_l2_norm: float

    def __post_init__(self) -> None:
        """Validate truncation range, retained representatives, and norm."""
        if type(self.source) is not BlockHoppingModel1D:
            raise TypeError("source must be BlockHoppingModel1D")
        if type(self.maximum_range) is not int:
            raise TypeError("maximum_range must be a built-in int")
        if self.maximum_range < 0:
            raise ValueError("maximum_range must be nonnegative")
        if type(self.truncated) is not BlockHoppingModel1D:
            raise TypeError("truncated must be BlockHoppingModel1D")
        expected = tuple(
            value
            for value in self.source.representatives
            if abs(value) <= self.maximum_range
        )
        if self.truncated.representatives != expected:
            raise ValueError("truncated representatives must match maximum_range")
        if type(self.omitted_block_l2_norm) is not float:
            raise TypeError("omitted_block_l2_norm must be a built-in float")
        if (
            not np.isfinite(self.omitted_block_l2_norm)
            or self.omitted_block_l2_norm < 0.0
        ):
            raise ValueError("omitted_block_l2_norm must be finite and nonnegative")
        omitted_squared = sum(
            float(np.linalg.norm(block.magnitude) ** 2)
            for representative, block in zip(
                self.source.representatives,
                self.source.hopping_blocks,
                strict=True,
            )
            if abs(representative) > self.maximum_range
        )
        if not np.isclose(
            self.omitted_block_l2_norm,
            np.sqrt(omitted_squared),
            rtol=0.0,
            atol=np.finfo(np.float64).eps,
        ):
            raise ValueError(
                "omitted_block_l2_norm must match the omitted source blocks"
            )


class BlockHoppingTruncator1D:
    """Apply symmetric cell-range truncation without mutating full hoppings."""

    __slots__ = ()

    def execute(
        self, source: BlockHoppingModel1D, maximum_range: int
    ) -> BlockHoppingTruncationResult1D:
        """Retain blocks with ``|R| <= maximum_range`` and report the omitted norm."""
        if type(source) is not BlockHoppingModel1D:
            raise TypeError("source must be BlockHoppingModel1D")
        if type(maximum_range) is not int:
            raise TypeError("maximum_range must be a built-in int")
        if maximum_range < 0:
            raise ValueError("maximum_range must be nonnegative")
        retained = tuple(
            index
            for index, representative in enumerate(source.representatives)
            if abs(representative) <= maximum_range
        )
        if not retained:
            raise ValueError("truncation retains no represented hopping block")
        omitted_squared = sum(
            float(np.linalg.norm(block.magnitude) ** 2)
            for index, block in enumerate(source.hopping_blocks)
            if index not in retained
        )
        truncated = BlockHoppingModel1D(
            source.reciprocal_period,
            tuple(source.representatives[index] for index in retained),
            tuple(source.hopping_blocks[index] for index in retained),
        )
        return BlockHoppingTruncationResult1D(
            source, maximum_range, truncated, float(np.sqrt(omitted_squared))
        )
