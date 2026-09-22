"""Finite hopping and matrix construction for accepted-parent Stage C."""

from __future__ import annotations

import hashlib
import json

import numpy as np

from .model import (
    ComplexMatrix,
    FloatPair,
    IntPair,
    JsonValue,
    LocalBond,
    ParentControls,
    ParentFixture,
    ParentHopping,
    PointOperation,
)


class ParentHoppingConstructor:
    """Construct and validate compact parent hopping inventories."""

    __slots__ = ()

    @staticmethod
    def anisotropic(fixture: ParentFixture) -> tuple[ParentHopping, ...]:
        n = fixture.reciprocal_mesh_size
        energies = np.asarray(fixture.anisotropic_energies, dtype=np.float64)
        ix = np.arange(n, dtype=np.float64)[:, None]
        iy = np.arange(n, dtype=np.float64)[None, :]
        result: list[ParentHopping] = []
        for rx in range(-(n // 2), n // 2 + 1):
            for ry in range(-(n // 2), n // 2 + 1):
                phase = np.exp(2.0j * np.pi * (ix * rx + iy * ry) / float(n))
                value = complex(np.sum(energies * phase) / float(n * n))
                result.append(ParentHopping((rx, ry), value))
        return tuple(result)

    @staticmethod
    def compact(
        hoppings: tuple[ParentHopping, ...], maximum_squared_radius: int
    ) -> tuple[ParentHopping, ...]:
        result = tuple(
            hopping
            for hopping in hoppings
            if hopping.displacement[0] ** 2 + hopping.displacement[1] ** 2
            <= maximum_squared_radius
        )
        if len(result) != 61:
            raise ValueError("radius-18 compact inventory must contain 61 records")
        return result

    @staticmethod
    def swapped(hoppings: tuple[ParentHopping, ...]) -> tuple[ParentHopping, ...]:
        return tuple(
            sorted(
                (
                    ParentHopping(
                        (hopping.displacement[1], hopping.displacement[0]),
                        hopping.value,
                    )
                    for hopping in hoppings
                ),
                key=lambda value: value.displacement,
            )
        )

    @staticmethod
    def validate(
        hoppings: tuple[ParentHopping, ...], operations: tuple[PointOperation, ...]
    ) -> dict[str, JsonValue]:
        values = {hopping.displacement: hopping.value for hopping in hoppings}
        if len(values) != len(hoppings):
            raise ValueError("duplicate parent hopping displacement")
        hermiticity = 0.0
        symmetry = 0.0
        for displacement, value in values.items():
            reverse = (-displacement[0], -displacement[1])
            if reverse not in values:
                raise ValueError(f"missing Hermitian hopping partner {reverse}")
            hermiticity = max(hermiticity, abs(values[reverse] - value.conjugate()))
            for operation in operations:
                matrix = operation.matrix
                target = (
                    matrix[0][0] * displacement[0] + matrix[0][1] * displacement[1],
                    matrix[1][0] * displacement[0] + matrix[1][1] * displacement[1],
                )
                if target not in values:
                    raise ValueError(f"missing symmetry hopping partner {target}")
                symmetry = max(symmetry, abs(values[target] - value))
        return {
            "count": len(hoppings),
            "sha256": ParentHoppingConstructor.digest(hoppings),
            "hermiticity_maximum_absolute": hermiticity,
            "symmetry_maximum_absolute": symmetry,
        }

    @staticmethod
    def digest(hoppings: tuple[ParentHopping, ...]) -> str:
        payload = [
            [
                hopping.displacement[0],
                hopping.displacement[1],
                float(hopping.value.real),
                float(hopping.value.imag),
            ]
            for hopping in hoppings
        ]
        return hashlib.sha256(
            json.dumps(payload, separators=(",", ":")).encode()
        ).hexdigest()


class ParentMatrixConstructor:
    """Construct parent, defect, gauge, permutation, and attack matrices."""

    __slots__ = ()

    @staticmethod
    def index(controls: ParentControls, site: IntPair) -> int:
        return (site[0] % controls.nx) * controls.ny + (site[1] % controls.ny)

    def parent(
        self,
        controls: ParentControls,
        hoppings: tuple[ParentHopping, ...],
        twist: FloatPair,
        route: str,
    ) -> ComplexMatrix:
        if route == "A_centered_uniform":
            return self.uniform_parent(controls, hoppings, twist)
        if route == "B_reduced_seam":
            return self.seam_parent(controls, hoppings, twist)
        raise ValueError(f"unsupported route {route}")

    def uniform_parent(
        self,
        controls: ParentControls,
        hoppings: tuple[ParentHopping, ...],
        twist: FloatPair,
    ) -> ComplexMatrix:
        result = np.zeros((controls.dimension,) * 2, dtype=np.complex128)
        for x in range(controls.nx):
            for y in range(controls.ny):
                row = self.index(controls, (x, y))
                for hopping in hoppings:
                    dx, dy = hopping.displacement
                    column = self.index(controls, (x + dx, y + dy))
                    phase = np.exp(
                        2.0j
                        * np.pi
                        * (twist[0] * dx / controls.nx + twist[1] * dy / controls.ny)
                    )
                    result[row, column] += hopping.value * phase
        return result

    def seam_parent(
        self,
        controls: ParentControls,
        hoppings: tuple[ParentHopping, ...],
        twist: FloatPair,
    ) -> ComplexMatrix:
        result = np.zeros((controls.dimension,) * 2, dtype=np.complex128)
        for x in range(controls.nx):
            for y in range(controls.ny):
                row = self.index(controls, (x, y))
                for hopping in hoppings:
                    dx, dy = hopping.displacement
                    tx = x + dx
                    ty = y + dy
                    column = self.index(controls, (tx, ty))
                    qx, _ = divmod(tx, controls.nx)
                    qy, _ = divmod(ty, controls.ny)
                    phase = np.exp(2.0j * np.pi * (qx * twist[0] + qy * twist[1]))
                    result[row, column] += hopping.value * phase
        return result

    def defect(
        self,
        controls: ParentControls,
        terms: tuple[LocalBond, ...],
        twist: FloatPair,
        route: str,
        include_reverse: bool = True,
    ) -> ComplexMatrix:
        if route == "A_centered_uniform":
            return self.uniform_defect(controls, terms, twist, include_reverse)
        if route == "B_reduced_seam":
            return self.seam_defect(controls, terms, twist, include_reverse)
        raise ValueError(f"unsupported route {route}")

    def uniform_defect(
        self,
        controls: ParentControls,
        terms: tuple[LocalBond, ...],
        twist: FloatPair,
        include_reverse: bool,
    ) -> ComplexMatrix:
        result = np.zeros((controls.dimension,) * 2, dtype=np.complex128)
        for term in terms:
            row = self.index(controls, term.start)
            dx, dy = term.displacement
            target = (term.start[0] + dx, term.start[1] + dy)
            column = self.index(controls, target)
            phase = np.exp(
                2.0j
                * np.pi
                * (twist[0] * dx / controls.nx + twist[1] * dy / controls.ny)
            )
            result[row, column] += term.value * phase
            if include_reverse:
                result[column, row] += term.value * phase.conjugate()
        return result

    def seam_defect(
        self,
        controls: ParentControls,
        terms: tuple[LocalBond, ...],
        twist: FloatPair,
        include_reverse: bool,
    ) -> ComplexMatrix:
        result = np.zeros((controls.dimension,) * 2, dtype=np.complex128)
        for term in terms:
            row = self.index(controls, term.start)
            dx, dy = term.displacement
            target = (term.start[0] + dx, term.start[1] + dy)
            column = self.index(controls, target)
            qx, _ = divmod(target[0], controls.nx)
            qy, _ = divmod(target[1], controls.ny)
            phase = np.exp(2.0j * np.pi * (qx * twist[0] + qy * twist[1]))
            result[row, column] += term.value * phase
            if include_reverse:
                result[column, row] += term.value * phase.conjugate()
        return result

    def onsite(self, controls: ParentControls, site: IntPair) -> ComplexMatrix:
        result = np.zeros((controls.dimension,) * 2, dtype=np.complex128)
        index = self.index(controls, site)
        result[index, index] = 1.0
        return result

    @staticmethod
    def transform_twist(twist: FloatPair, operation: PointOperation) -> FloatPair:
        matrix = operation.matrix
        return (
            matrix[0][0] * twist[0] + matrix[0][1] * twist[1],
            matrix[1][0] * twist[0] + matrix[1][1] * twist[1],
        )

    @staticmethod
    def reduce_twist(twist: FloatPair) -> FloatPair:
        return twist[0] % 1.0, twist[1] % 1.0

    @staticmethod
    def transform_bond(term: LocalBond, operation: PointOperation) -> LocalBond:
        matrix = operation.matrix
        return LocalBond(
            (
                matrix[0][0] * term.start[0] + matrix[0][1] * term.start[1],
                matrix[1][0] * term.start[0] + matrix[1][1] * term.start[1],
            ),
            (
                matrix[0][0] * term.displacement[0]
                + matrix[0][1] * term.displacement[1],
                matrix[1][0] * term.displacement[0]
                + matrix[1][1] * term.displacement[1],
            ),
            term.value,
        )

    def permutation(
        self, controls: ParentControls, operation: PointOperation
    ) -> ComplexMatrix:
        result = np.zeros((controls.dimension,) * 2, dtype=np.complex128)
        for x in range(controls.nx):
            for y in range(controls.ny):
                matrix = operation.matrix
                target = (
                    matrix[0][0] * x + matrix[0][1] * y,
                    matrix[1][0] * x + matrix[1][1] * y,
                )
                result[self.index(controls, target), self.index(controls, (x, y))] = 1.0
        return result

    def attack(self, controls: ParentControls) -> ComplexMatrix:
        operation = PointOperation("reflection_antidiagonal", ((0, -1), (-1, 0)))
        permutation = np.zeros(
            (controls.dimension, controls.dimension), dtype=np.complex128
        )
        for x in range(controls.nx):
            for y in range(controls.ny):
                matrix = operation.matrix
                target = (
                    matrix[0][0] * x + matrix[0][1] * y + 2,
                    matrix[1][0] * x + matrix[1][1] * y + 3,
                )
                permutation[
                    self.index(controls, target), self.index(controls, (x, y))
                ] = 1.0
        phases = np.asarray(
            [
                np.exp(1.0j * (0.137 * x - 0.191 * y))
                for x in range(controls.nx)
                for y in range(controls.ny)
            ],
            dtype=np.complex128,
        )
        return np.asarray(permutation @ np.diag(phases), dtype=np.complex128)

    @staticmethod
    def gauge(controls: ParentControls, twist: FloatPair) -> ComplexMatrix:
        phases = np.asarray(
            [
                np.exp(
                    2.0j
                    * np.pi
                    * (x * twist[0] / controls.nx + y * twist[1] / controls.ny)
                )
                for x in range(controls.nx)
                for y in range(controls.ny)
            ],
            dtype=np.complex128,
        )
        return np.diag(phases)

    @staticmethod
    def maximum(matrix: ComplexMatrix) -> float:
        return float(np.max(np.abs(matrix), initial=0.0))

    @staticmethod
    def digest(matrix: ComplexMatrix) -> str:
        return hashlib.sha256(
            np.ascontiguousarray(matrix, dtype="<c16").tobytes()
        ).hexdigest()
