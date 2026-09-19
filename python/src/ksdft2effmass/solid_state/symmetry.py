"""Integral lattice operations and finite-shape compatibility analysis.

An operation is explicit input rather than a symmetry inferred from spatial dimension.
The initial geometry-compatibility action supports signed axis permutations, covering
the reflection and axis-swap operations required by the accepted scalar studies.
"""

from __future__ import annotations

from dataclasses import dataclass

from .boundary_phases import BoundaryTwistLift, LatticeFloatComponents
from .geometry import (
    FiniteLatticeShape,
    LatticeCoordinate,
    LatticeDimension,
    LatticeDisplacement,
    LatticeIntegerComponents,
)

type IntegerMatrix = (
    tuple[tuple[int]]
    | tuple[tuple[int, int], tuple[int, int]]
    | tuple[
        tuple[int, int, int],
        tuple[int, int, int],
        tuple[int, int, int],
    ]
)
"""Closed exact integer matrix representation for one to three dimensions."""


@dataclass(frozen=True, slots=True)
class IntegralLatticeOperation:
    """Represent one unimodular integral lattice operation.

    Parameters
    ----------
    identifier
        Nonempty operation identity.
    dimension
        Exact supported spatial dimension.
    matrix
        Exact square built-in-integer matrix with determinant ``+1`` or ``-1``.
    """

    identifier: str
    dimension: LatticeDimension
    matrix: IntegerMatrix

    def __post_init__(self) -> None:
        """Validate identity, exact shape, integer entries, and unimodularity."""
        if type(self.identifier) is not str:
            raise TypeError("identifier must be a string")
        if not self.identifier:
            raise ValueError("identifier must be nonempty")
        if type(self.dimension) is not LatticeDimension:
            raise TypeError("dimension must be LatticeDimension")
        if type(self.matrix) is not tuple:
            raise TypeError("matrix must be a tuple of tuples")
        if len(self.matrix) != self.dimension.value:
            raise ValueError("matrix row count must match dimension")
        for row in self.matrix:
            if type(row) is not tuple:
                raise TypeError("matrix rows must be tuples")
            if len(row) != self.dimension.value:
                raise ValueError("matrix column count must match dimension")
            if any(type(value) is not int for value in row):
                raise TypeError("matrix entries must be built-in integers")
        if abs(self.determinant) != 1:
            raise ValueError("integral lattice operation must be unimodular")

    @property
    def determinant(self) -> int:
        """Return the exact determinant for the one-, two-, or three-axis matrix."""
        matrix = self.matrix
        if len(matrix) == 1:
            return matrix[0][0]
        if len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        return (
            matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
            - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
            + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
        )


class LatticeCoordinateTransformer:
    """Apply an integral operation to one compatible lattice coordinate."""

    __slots__ = ()

    def execute(
        self, operation: IntegralLatticeOperation, coordinate: LatticeCoordinate
    ) -> LatticeCoordinate:
        """Return ``operation.matrix`` times ``coordinate.components``."""
        if type(operation) is not IntegralLatticeOperation:
            raise TypeError("operation must be IntegralLatticeOperation")
        if type(coordinate) is not LatticeCoordinate:
            raise TypeError("coordinate must be LatticeCoordinate")
        if operation.dimension is not coordinate.dimension:
            raise ValueError("operation and coordinate dimensions must agree")
        values = tuple(
            sum(
                operation.matrix[row][column] * coordinate.components[column]
                for column in range(operation.dimension.value)
            )
            for row in range(operation.dimension.value)
        )
        if operation.dimension is LatticeDimension.ONE:
            closed: LatticeIntegerComponents = (values[0],)
        elif operation.dimension is LatticeDimension.TWO:
            closed = (values[0], values[1])
        else:
            closed = (values[0], values[1], values[2])
        return LatticeCoordinate(operation.dimension, closed)


class LatticeDisplacementTransformer:
    """Apply an integral operation to one compatible lattice displacement."""

    __slots__ = ()

    def execute(
        self, operation: IntegralLatticeOperation, displacement: LatticeDisplacement
    ) -> LatticeDisplacement:
        """Return ``operation.matrix`` times ``displacement.components``."""
        if type(operation) is not IntegralLatticeOperation:
            raise TypeError("operation must be IntegralLatticeOperation")
        if type(displacement) is not LatticeDisplacement:
            raise TypeError("displacement must be LatticeDisplacement")
        if operation.dimension is not displacement.dimension:
            raise ValueError("operation and displacement dimensions must agree")
        values = tuple(
            sum(
                operation.matrix[row][column] * displacement.components[column]
                for column in range(operation.dimension.value)
            )
            for row in range(operation.dimension.value)
        )
        if operation.dimension is LatticeDimension.ONE:
            closed: LatticeIntegerComponents = (values[0],)
        elif operation.dimension is LatticeDimension.TWO:
            closed = (values[0], values[1])
        else:
            closed = (values[0], values[1], values[2])
        return LatticeDisplacement(operation.dimension, closed)


class BoundaryTwistTransformer:
    """Apply an integral lattice operation to an unreduced boundary twist."""

    __slots__ = ()

    def execute(
        self, operation: IntegralLatticeOperation, twist: BoundaryTwistLift
    ) -> BoundaryTwistLift:
        """Return the transformed unreduced twist without quotient reduction."""
        if type(operation) is not IntegralLatticeOperation:
            raise TypeError("operation must be IntegralLatticeOperation")
        if type(twist) is not BoundaryTwistLift:
            raise TypeError("twist must be BoundaryTwistLift")
        if operation.dimension is not twist.dimension:
            raise ValueError("operation and twist dimensions must agree")
        values = tuple(
            sum(
                float(operation.matrix[row][column]) * twist.turns[column]
                for column in range(operation.dimension.value)
            )
            for row in range(operation.dimension.value)
        )
        if operation.dimension is LatticeDimension.ONE:
            closed: LatticeFloatComponents = (values[0],)
        elif operation.dimension is LatticeDimension.TWO:
            closed = (values[0], values[1])
        else:
            closed = (values[0], values[1], values[2])
        return BoundaryTwistLift(operation.dimension, closed)


@dataclass(frozen=True, slots=True)
class LatticeOperationCompatibilityResult:
    """Record signed-axis-permutation compatibility between finite shapes.

    Parameters
    ----------
    compatible
        Exact Boolean that is true only when ``issue_codes`` is empty.
    issue_codes
        Sorted unique stable issue codes.
    """

    compatible: bool
    issue_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate status and deterministic issue ordering."""
        if type(self.compatible) is not bool:
            raise TypeError("compatible must be bool")
        if type(self.issue_codes) is not tuple or any(
            type(value) is not str for value in self.issue_codes
        ):
            raise TypeError("issue_codes must be a tuple of strings")
        if self.issue_codes != tuple(sorted(set(self.issue_codes))):
            raise ValueError("issue_codes must be sorted and unique")
        if self.compatible == bool(self.issue_codes):
            raise ValueError("compatible status must agree with issue_codes")


class LatticeOperationCompatibilityAuditor:
    """Audit whether a signed axis permutation maps one finite shape to another."""

    __slots__ = ()

    def execute(
        self,
        source: FiniteLatticeShape,
        target: FiniteLatticeShape,
        operation: IntegralLatticeOperation,
    ) -> LatticeOperationCompatibilityResult:
        """Return deterministic dimensional and axis-extent compatibility findings."""
        if type(source) is not FiniteLatticeShape:
            raise TypeError("source must be FiniteLatticeShape")
        if type(target) is not FiniteLatticeShape:
            raise TypeError("target must be FiniteLatticeShape")
        if type(operation) is not IntegralLatticeOperation:
            raise TypeError("operation must be IntegralLatticeOperation")
        issues: set[str] = set()
        if source.dimension is not target.dimension:
            issues.add("SOLID_STATE.LATTICE_OPERATION.TARGET_DIMENSION")
        if source.dimension is not operation.dimension:
            issues.add("SOLID_STATE.LATTICE_OPERATION.OPERATION_DIMENSION")
        if issues:
            return LatticeOperationCompatibilityResult(False, tuple(sorted(issues)))
        dimension = source.dimension.value
        source_axes: list[int] = []
        for row in operation.matrix:
            nonzero = [index for index, value in enumerate(row) if value != 0]
            if len(nonzero) != 1 or abs(row[nonzero[0]]) != 1:
                issues.add("SOLID_STATE.LATTICE_OPERATION.NOT_SIGNED_PERMUTATION")
                break
            source_axes.append(nonzero[0])
        if len(set(source_axes)) != dimension:
            issues.add("SOLID_STATE.LATTICE_OPERATION.NOT_SIGNED_PERMUTATION")
        if not issues:
            for target_axis, source_axis in enumerate(source_axes):
                if target.extents[target_axis] != source.extents[source_axis]:
                    issues.add("SOLID_STATE.LATTICE_OPERATION.EXTENT_MISMATCH")
        ordered = tuple(sorted(issues))
        return LatticeOperationCompatibilityResult(not ordered, ordered)
