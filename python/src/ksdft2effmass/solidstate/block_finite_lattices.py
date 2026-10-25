"""Finite periodic operators constructed from one-dimensional block hoppings.

The records in this module keep the finite-lattice representation explicit.  A
``BlockHoppingModel1D`` supplies primitive-cell hopping blocks, while a boundary
phase, finite cell count, basis ordering, energy reference, and gauge identify the
represented supercell operator.  Construction is sparse; dense materialization is an
explicit caller decision.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

import numpy as np
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    ComplexSparseMatrixQuantity,
    Unitless,
)
from scipy import sparse  # type: ignore[import-untyped]

from .boundary_phases import (
    BoundaryTwistLift,
    BoundaryTwistReducer,
    TwistFiber,
    TwistGaugeRepresentation,
)
from .hopping_transforms import BlockHoppingModel1D


@dataclass(frozen=True, slots=True, eq=False)
class BlockFiniteLatticeOperator1D:
    """Represent one sparse block operator on a finite periodic one-dimensional lattice.

    Matrix indices use cell-major order: ``cell * block_dimension + orbital``.
    ``energy_reference`` identifies the additive energy origin; it is not a unit.
    """

    identifier: str
    matrix: ComplexSparseMatrixQuantity
    cell_count: int
    basis_identifier: str
    block_basis_labels: tuple[str, ...]
    twist_fiber: TwistFiber
    energy_reference: str

    def __post_init__(self) -> None:
        """Validate representation identity, shape, and basis metadata."""
        if type(self.identifier) is not str or not self.identifier:
            raise ValueError("identifier must be a nonempty string")
        if not isinstance(self.matrix, ComplexSparseMatrixQuantity):
            raise TypeError("matrix must be a ComplexSparseMatrixQuantity")
        if type(self.cell_count) is not int:
            raise TypeError("cell_count must be a built-in integer")
        if self.cell_count < 1:
            raise ValueError("cell_count must be positive")
        if type(self.basis_identifier) is not str or not self.basis_identifier:
            raise ValueError("basis_identifier must be a nonempty string")
        if not isinstance(self.block_basis_labels, tuple):
            raise TypeError("block_basis_labels must be a tuple")
        if not self.block_basis_labels:
            raise ValueError("block_basis_labels must be nonempty")
        if any(
            type(label) is not str or not label for label in self.block_basis_labels
        ):
            raise ValueError("block basis labels must be nonempty strings")
        if len(set(self.block_basis_labels)) != len(self.block_basis_labels):
            raise ValueError("block basis labels must be unique")
        if not isinstance(self.twist_fiber, TwistFiber):
            raise TypeError("twist_fiber must be a TwistFiber")
        if self.twist_fiber.dimension.value != 1:
            raise ValueError("twist_fiber must be one-dimensional")
        if type(self.energy_reference) is not str or not self.energy_reference:
            raise ValueError("energy_reference must be a nonempty string")
        expected = self.cell_count * len(self.block_basis_labels)
        if self.matrix.shape != (expected, expected):
            raise ValueError("matrix shape must match cell and block dimensions")

    @property
    def block_dimension(self) -> int:
        """Return the number of basis vectors in one primitive cell."""
        return len(self.block_basis_labels)

    @property
    def matrix_dimension(self) -> int:
        """Return the represented finite Hilbert-space dimension."""
        return self.cell_count * self.block_dimension


class BlockHoppingSupercellOperatorConstructor1D:
    """Construct a cell-major finite operator in the uniform-link twist gauge.

    A block at displacement ``R`` contributes to ``(cell, cell + R mod N)`` and is
    multiplied by ``exp(2π i φ R / N)``, where ``φ`` is the one-dimensional twist in
    turns.  The distributed phase makes every translated link carry the same phase.
    """

    __slots__ = ()

    def execute(
        self,
        identifier: str,
        model: BlockHoppingModel1D,
        cell_count: int,
        twist: BoundaryTwistLift,
        basis_identifier: str,
        block_basis_labels: tuple[str, ...],
        energy_reference: str,
    ) -> BlockFiniteLatticeOperator1D:
        """Construct the sparse finite-periodic operator."""
        self._validate_request(model, cell_count, twist, block_basis_labels)
        block_dimension = model.matrix_dimension
        rows: list[int] = []
        columns: list[int] = []
        data: list[complex] = []
        twist_turns = twist.turns[0]
        for displacement, block_quantity in zip(
            model.representatives, model.hopping_blocks, strict=True
        ):
            block = block_quantity.magnitude
            phase = np.exp(2.0j * np.pi * twist_turns * displacement / cell_count)
            nonzero_rows, nonzero_columns = np.nonzero(block)
            for source_cell in range(cell_count):
                target_cell = (source_cell + displacement) % cell_count
                for block_row, block_column in zip(
                    nonzero_rows, nonzero_columns, strict=True
                ):
                    rows.append(source_cell * block_dimension + int(block_row))
                    columns.append(target_cell * block_dimension + int(block_column))
                    data.append(complex(phase * block[block_row, block_column]))
        matrix = sparse.coo_array(
            (np.asarray(data, dtype=np.complex128), (rows, columns)),
            shape=(cell_count * block_dimension, cell_count * block_dimension),
            dtype=np.complex128,
        ).tocsr()
        reduction = BoundaryTwistReducer().execute(twist)
        return BlockFiniteLatticeOperator1D(
            identifier=identifier,
            matrix=ComplexSparseMatrixQuantity.from_csr(
                matrix, model.hopping_blocks[0].unit
            ),
            cell_count=cell_count,
            basis_identifier=basis_identifier,
            block_basis_labels=block_basis_labels,
            twist_fiber=TwistFiber(
                reduction, TwistGaugeRepresentation.CENTERED_UNIFORM_LINK
            ),
            energy_reference=energy_reference,
        )

    @staticmethod
    def _validate_request(
        model: BlockHoppingModel1D,
        cell_count: int,
        twist: BoundaryTwistLift,
        block_basis_labels: tuple[str, ...],
    ) -> None:
        """Validate shared finite-construction inputs."""
        if not isinstance(model, BlockHoppingModel1D):
            raise TypeError("model must be a BlockHoppingModel1D")
        if type(cell_count) is not int:
            raise TypeError("cell_count must be a built-in integer")
        if cell_count < 1:
            raise ValueError("cell_count must be positive")
        if type(twist) is not BoundaryTwistLift:
            raise TypeError("twist must be a BoundaryTwistLift")
        if twist.dimension.value != 1:
            raise ValueError("twist must be one-dimensional")
        if not isinstance(block_basis_labels, tuple):
            raise TypeError("block_basis_labels must be a tuple")
        if len(block_basis_labels) != model.matrix_dimension:
            raise ValueError("block basis label count must equal block dimension")


class BlockHoppingQuotientSeamOperatorConstructor1D:
    """Construct a cell-major finite operator in the quotient-seam twist gauge.

    The phase is carried only by links that cross the chosen quotient seam.  For an
    unwrapped target ``cell + R`` and wrapped target in ``0, ..., N-1``, the integer
    quotient crossing count multiplies the boundary twist.
    """

    __slots__ = ()

    def execute(
        self,
        identifier: str,
        model: BlockHoppingModel1D,
        cell_count: int,
        twist: BoundaryTwistLift,
        basis_identifier: str,
        block_basis_labels: tuple[str, ...],
        energy_reference: str,
    ) -> BlockFiniteLatticeOperator1D:
        """Construct the independently assembled sparse quotient-seam operator."""
        BlockHoppingSupercellOperatorConstructor1D._validate_request(
            model, cell_count, twist, block_basis_labels
        )
        block_dimension = model.matrix_dimension
        rows: list[int] = []
        columns: list[int] = []
        data: list[complex] = []
        twist_turns = twist.turns[0]
        for displacement, block_quantity in zip(
            model.representatives, model.hopping_blocks, strict=True
        ):
            block = block_quantity.magnitude
            nonzero_rows, nonzero_columns = np.nonzero(block)
            for source_cell in range(cell_count):
                unwrapped_target = source_cell + displacement
                target_cell = unwrapped_target % cell_count
                crossing_count = (unwrapped_target - target_cell) // cell_count
                phase = np.exp(2.0j * np.pi * twist_turns * crossing_count)
                for block_row, block_column in zip(
                    nonzero_rows, nonzero_columns, strict=True
                ):
                    rows.append(source_cell * block_dimension + int(block_row))
                    columns.append(target_cell * block_dimension + int(block_column))
                    data.append(complex(phase * block[block_row, block_column]))
        matrix = sparse.coo_array(
            (np.asarray(data, dtype=np.complex128), (rows, columns)),
            shape=(cell_count * block_dimension, cell_count * block_dimension),
            dtype=np.complex128,
        ).tocsr()
        reduction = BoundaryTwistReducer().execute(twist)
        return BlockFiniteLatticeOperator1D(
            identifier=identifier,
            matrix=ComplexSparseMatrixQuantity.from_csr(
                matrix, model.hopping_blocks[0].unit
            ),
            cell_count=cell_count,
            basis_identifier=basis_identifier,
            block_basis_labels=block_basis_labels,
            twist_fiber=TwistFiber(reduction, TwistGaugeRepresentation.QUOTIENT_SEAM),
            energy_reference=energy_reference,
        )


class ReciprocalCoordinateInterval1D(StrEnum):
    """Identify the half-open interval used for reduced reciprocal coordinates."""

    UNIT = "unit_half_open"
    CENTERED = "centered_half_open"


@dataclass(frozen=True, slots=True, eq=False)
class SupercellBlochFoldingTransform1D:
    """Represent the unitary map from folded Bloch blocks to cell-major coordinates.

    Folded blocks are ordered by ``j = 0, ..., N - 1`` with a declared half-open
    representative congruent to ``(φ + j) / N`` modulo one. Within each block,
    orbital order is unchanged.
    """

    cell_count: int
    block_dimension: int
    twist: BoundaryTwistLift
    coordinate_interval: ReciprocalCoordinateInterval1D
    primitive_reduced_momenta: tuple[float, ...]
    matrix: ComplexMatrixQuantity
    maximum_unitarity_residual: float

    def __post_init__(self) -> None:
        """Validate dimensions, deterministic momenta, and immutable matrix storage."""
        if type(self.cell_count) is not int or self.cell_count < 1:
            raise ValueError("cell_count must be a positive built-in integer")
        if type(self.block_dimension) is not int or self.block_dimension < 1:
            raise ValueError("block_dimension must be a positive built-in integer")
        if type(self.twist) is not BoundaryTwistLift or self.twist.dimension.value != 1:
            raise ValueError("twist must be a one-dimensional BoundaryTwistLift")
        if type(self.coordinate_interval) is not ReciprocalCoordinateInterval1D:
            raise TypeError(
                "coordinate_interval must be ReciprocalCoordinateInterval1D"
            )
        if (
            not isinstance(self.primitive_reduced_momenta, tuple)
            or len(self.primitive_reduced_momenta) != self.cell_count
        ):
            raise ValueError("one primitive reduced momentum is required per cell")
        for index, momentum in enumerate(self.primitive_reduced_momenta):
            if type(momentum) is not float or not np.isfinite(momentum):
                raise TypeError("primitive reduced momenta must be finite floats")
            if self.coordinate_interval is ReciprocalCoordinateInterval1D.UNIT:
                in_interval = 0.0 <= momentum < 1.0
            else:
                in_interval = -0.5 <= momentum < 0.5
            if not in_interval:
                raise ValueError(
                    "primitive momentum lies outside its declared interval"
                )
            expected = (self.twist.turns[0] + index) / self.cell_count
            congruence_defect = abs((momentum - expected) - round(momentum - expected))
            if congruence_defect > 32.0 * np.finfo(np.float64).eps:
                raise ValueError(
                    "primitive_reduced_momenta do not match the folding rule"
                )
        if type(self.matrix) is not ComplexMatrixQuantity:
            raise TypeError("matrix must be a ComplexMatrixQuantity")
        if type(self.matrix.unit) is not Unitless:
            raise ValueError("folding transformation matrix must be unitless")
        value = self.matrix.magnitude
        dimension = self.cell_count * self.block_dimension
        if value.shape != (dimension, dimension):
            raise ValueError("matrix shape must match cell and block dimensions")
        if not np.all(np.isfinite(value.real)) or not np.all(np.isfinite(value.imag)):
            raise ValueError("matrix must contain finite values")
        if type(self.maximum_unitarity_residual) is not float:
            raise TypeError("maximum_unitarity_residual must be a built-in float")
        if not np.isfinite(self.maximum_unitarity_residual):
            raise ValueError("maximum_unitarity_residual must be finite")
        measured = float(np.max(np.abs(value.conj().T @ value - np.eye(dimension))))
        if measured != self.maximum_unitarity_residual:
            raise ValueError("maximum_unitarity_residual does not match matrix")
        tolerance = 256.0 * np.finfo(np.float64).eps * dimension
        if measured > tolerance:
            raise ValueError("matrix is not unitary within binary64 roundoff")


def _reduce_reciprocal_coordinate(
    value: float, interval: ReciprocalCoordinateInterval1D
) -> float:
    """Reduce one finite reciprocal coordinate to the requested half-open interval."""
    if interval is ReciprocalCoordinateInterval1D.UNIT:
        return value % 1.0
    return (value + 0.5) % 1.0 - 0.5


class SupercellBlochFoldingTransformConstructor1D:
    """Construct the finite Fourier transform for one twisted block supercell."""

    __slots__ = ()

    def execute(
        self,
        cell_count: int,
        block_dimension: int,
        twist: BoundaryTwistLift,
        coordinate_interval: ReciprocalCoordinateInterval1D,
    ) -> SupercellBlochFoldingTransform1D:
        """Return the deterministic folded-block-to-cell-major unitary map."""
        if type(cell_count) is not int or cell_count < 1:
            raise ValueError("cell_count must be a positive built-in integer")
        if type(block_dimension) is not int or block_dimension < 1:
            raise ValueError("block_dimension must be a positive built-in integer")
        if type(twist) is not BoundaryTwistLift:
            raise TypeError("twist must be a BoundaryTwistLift")
        if type(coordinate_interval) is not ReciprocalCoordinateInterval1D:
            raise TypeError(
                "coordinate_interval must be ReciprocalCoordinateInterval1D"
            )
        momenta = tuple(
            _reduce_reciprocal_coordinate(
                (twist.turns[0] + index) / cell_count, coordinate_interval
            )
            for index in range(cell_count)
        )
        return self.execute_from_momenta(
            cell_count, block_dimension, twist, coordinate_interval, momenta
        )

    def execute_from_momenta(
        self,
        cell_count: int,
        block_dimension: int,
        twist: BoundaryTwistLift,
        coordinate_interval: ReciprocalCoordinateInterval1D,
        primitive_reduced_momenta: tuple[float, ...],
    ) -> SupercellBlochFoldingTransform1D:
        """Construct the map from caller-retained congruent momentum representatives."""
        if type(cell_count) is not int or cell_count < 1:
            raise ValueError("cell_count must be a positive built-in integer")
        if type(block_dimension) is not int or block_dimension < 1:
            raise ValueError("block_dimension must be a positive built-in integer")
        if type(twist) is not BoundaryTwistLift:
            raise TypeError("twist must be a BoundaryTwistLift")
        if twist.dimension.value != 1:
            raise ValueError("twist must be one-dimensional")
        if type(coordinate_interval) is not ReciprocalCoordinateInterval1D:
            raise TypeError(
                "coordinate_interval must be ReciprocalCoordinateInterval1D"
            )
        if (
            not isinstance(primitive_reduced_momenta, tuple)
            or len(primitive_reduced_momenta) != cell_count
        ):
            raise ValueError("one primitive reduced momentum is required per cell")
        for index, momentum in enumerate(primitive_reduced_momenta):
            if type(momentum) is not float or not np.isfinite(momentum):
                raise TypeError("primitive reduced momenta must be finite floats")
            if coordinate_interval is ReciprocalCoordinateInterval1D.UNIT:
                in_interval = 0.0 <= momentum < 1.0
            else:
                in_interval = -0.5 <= momentum < 0.5
            if not in_interval:
                raise ValueError(
                    "primitive momentum lies outside its declared interval"
                )
            expected = (twist.turns[0] + index) / cell_count
            congruence_defect = abs((momentum - expected) - round(momentum - expected))
            if congruence_defect > 32.0 * np.finfo(np.float64).eps:
                raise ValueError(
                    "primitive_reduced_momenta do not match the folding rule"
                )
        momenta = primitive_reduced_momenta
        dimension = cell_count * block_dimension
        matrix = np.zeros((dimension, dimension), dtype=np.complex128)
        normalization = np.sqrt(float(cell_count))
        identity = np.eye(block_dimension, dtype=np.complex128)
        for cell in range(cell_count):
            row = slice(cell * block_dimension, (cell + 1) * block_dimension)
            for index, momentum in enumerate(momenta):
                column = slice(index * block_dimension, (index + 1) * block_dimension)
                matrix[row, column] = (
                    np.exp(2.0j * np.pi * momentum * cell) / normalization * identity
                )
        residual = float(np.max(np.abs(matrix.conj().T @ matrix - np.eye(dimension))))
        return SupercellBlochFoldingTransform1D(
            cell_count=cell_count,
            block_dimension=block_dimension,
            twist=twist,
            coordinate_interval=coordinate_interval,
            primitive_reduced_momenta=momenta,
            matrix=ComplexMatrixQuantity(matrix, Unitless()),
            maximum_unitarity_residual=residual,
        )
