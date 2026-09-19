#!/usr/bin/env python3
"""Exercise the accepted-parent Stage C contract with authored fixtures only."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import multiprocessing
import os
import platform
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, cast

import numpy as np
import numpy.typing as npt

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type ComplexMatrix = npt.NDArray[np.complex128]
type FloatPair = tuple[float, float]
type IntPair = tuple[int, int]
type IntMatrix2 = tuple[tuple[int, int], tuple[int, int]]
type MatrixKey = tuple[str, str]


@dataclass(frozen=True, slots=True)
class ParentHopping:
    """Represent one compact scalar-parent hopping coefficient."""

    displacement: IntPair
    value: complex

    def __post_init__(self) -> None:
        if not np.isfinite(self.value.real) or not np.isfinite(self.value.imag):
            raise ValueError("hopping value must be finite")


@dataclass(frozen=True, slots=True)
class LocalBond:
    """Represent one localized real bond change before its Hermitian reverse."""

    start: IntPair
    displacement: IntPair
    value: float

    def __post_init__(self) -> None:
        if self.displacement == (0, 0):
            raise ValueError("localized bond displacement must be nonzero")
        if not np.isfinite(self.value):
            raise ValueError("localized bond value must be finite")


@dataclass(frozen=True, slots=True)
class PointOperation:
    """Represent one exact integer point operation."""

    identifier: str
    matrix: IntMatrix2


@dataclass(frozen=True, slots=True)
class ParentFixture:
    """Own immutable authored parent data used by execution-free behavior."""

    isotropic_hoppings: tuple[ParentHopping, ...]
    anisotropic_energies: tuple[tuple[float, ...], ...]
    reciprocal_mesh_size: int
    hopping_maximum_squared_radius: int
    fixture_sha256: str


@dataclass(frozen=True, slots=True)
class ParentControls:
    """Own the adopted Stage C dimensions, inventories, and criteria."""

    nx: int
    ny: int
    twists: tuple[FloatPair, FloatPair]
    model_classes: tuple[str, ...]
    d4: tuple[PointOperation, ...]
    d2: tuple[PointOperation, ...]
    axis_swap: PointOperation
    defects: tuple[tuple[str, tuple[LocalBond, ...], str], ...]
    route_evaluations: int
    bridge_records: int
    model_fit_records: int
    schedule_comparisons: int
    criteria: dict[str, float]

    @property
    def dimension(self) -> int:
        """Return the exact represented dimension."""

        return self.nx * self.ny


@dataclass(frozen=True, slots=True)
class ParentCase:
    """Own one frozen parent, defect, twist, and orientation case."""

    case_id: str
    parent_family: str
    source_parent_id: str
    target_parent_id: str
    defect_id: str
    source_terms: tuple[LocalBond, ...]
    expected_model_class: str
    twist_id: str
    base_twist: FloatPair
    operation: PointOperation


@dataclass(frozen=True, slots=True)
class ParentScheduleResult:
    """Carry one fresh schedule as immutable JSON and matrix bytes."""

    schedule_id: str
    process_id: int
    payload_json: str
    recovered_matrices: tuple[tuple[MatrixKey, bytes], ...]


class ParentJsonReader:
    """Decode exact JSON primitives into closed software types."""

    __slots__ = ()

    @staticmethod
    def mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be an object")
        return value

    @staticmethod
    def array(value: JsonValue, name: str) -> list[JsonValue]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be an array")
        return value

    @staticmethod
    def text(value: JsonValue, name: str) -> str:
        if not isinstance(value, str):
            raise TypeError(f"{name} must be a string")
        return value

    @staticmethod
    def boolean(value: JsonValue, name: str) -> bool:
        if not isinstance(value, bool):
            raise TypeError(f"{name} must be a boolean")
        return value

    @staticmethod
    def integer(value: JsonValue, name: str) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an integer")
        return value

    @staticmethod
    def real(value: JsonValue, name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be a real number")
        result = float(value)
        if not np.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result

    def integer_pair(self, value: JsonValue, name: str) -> IntPair:
        values = self.array(value, name)
        if len(values) != 2:
            raise ValueError(f"{name} must contain two integers")
        return self.integer(values[0], name), self.integer(values[1], name)


class AcceptedParentStageCDesignDeserializer:
    """Deserialize and enforce the exact human-adopted parent design."""

    ADOPTED_DESIGN_SHA256: ClassVar[str] = (
        "e5103eb95300095d46280fce5539b3e0a168c8c7b41f2f2473d1b3d2d8a48706"
    )
    __slots__ = ("_json",)

    def __init__(self) -> None:
        self._json = ParentJsonReader()

    def execute(self, path: Path) -> tuple[ParentControls, str]:
        encoded = path.read_bytes()
        design_sha256 = hashlib.sha256(encoded).hexdigest()
        if design_sha256 != self.ADOPTED_DESIGN_SHA256:
            raise ValueError("accepted-parent Stage C design identity is not adopted")
        raw = self._json.mapping(cast(JsonValue, json.loads(encoded)), "design")
        if raw.get("design_id") != (
            "research-monograph.impurity-defect-2d.stage-c.accepted-parent.v1"
        ):
            raise ValueError("unexpected accepted-parent Stage C design")
        if raw.get("status") != "human_adopted_proposed_contract":
            raise ValueError("accepted-parent Stage C design is not human-adopted")
        if raw.get("implementation_authorized_by_this_record") is not False:
            raise ValueError("design must not grant implementation authority")
        if raw.get("execution_authorized_by_this_record") is not False:
            raise ValueError("design must not grant execution authority")
        space = self._json.mapping(raw["represented_space"], "represented_space")
        shape = self._json.integer_pair(space["shape"], "shape")
        if shape != (8, 8) or space.get("dimension") != 64:
            raise ValueError("accepted-parent Stage C requires the 8x8 scalar space")
        twists_raw = self._json.array(space["twist_lifts_turns"], "twists")
        if len(twists_raw) != 2:
            raise ValueError("accepted-parent Stage C requires two twists")
        twists = tuple(
            (
                self._json.real(self._json.array(value, "twist")[0], "twist x"),
                self._json.real(self._json.array(value, "twist")[1], "twist y"),
            )
            for value in twists_raw
        )
        inventory = self._json.mapping(raw["case_inventory"], "case_inventory")
        expected_inventory = (208, 104, 1040, 104)
        actual_inventory = (
            self._json.integer(inventory["total_route_evaluations"], "routes"),
            self._json.integer(inventory["total_bridge_records"], "bridges"),
            self._json.integer(inventory["total_model_fit_records"], "fits"),
            self._json.integer(
                inventory["schedule_route_comparisons"], "schedule comparisons"
            ),
        )
        if actual_inventory != expected_inventory:
            raise ValueError("accepted-parent Stage C inventory differs")
        model_classes = tuple(
            self._json.text(value, "model class")
            for value in self._json.array(raw["model_class_order"], "model classes")
        )
        if len(model_classes) != 5:
            raise ValueError("accepted-parent Stage C requires five model classes")
        defects: list[tuple[str, tuple[LocalBond, ...], str]] = []
        for defect_value in self._json.array(raw["planted_defects"], "defects"):
            defect = self._json.mapping(defect_value, "defect")
            terms: list[LocalBond] = []
            for term_value in self._json.array(defect["terms"], "terms"):
                term = self._json.mapping(term_value, "term")
                terms.append(
                    LocalBond(
                        (0, 0),
                        self._json.integer_pair(term["displacement"], "displacement"),
                        self._json.real(term["change"], "change"),
                    )
                )
            defects.append(
                (
                    self._json.text(defect["defect_id"], "defect_id"),
                    tuple(terms),
                    self._json.text(
                        defect["expected_first_accepted_model_class"],
                        "expected model class",
                    ),
                )
            )
        criteria_raw = self._json.mapping(raw["criteria"], "criteria")
        criterion_names = (
            "hopping_hermiticity_maximum_absolute_EG",
            "isotropic_D4_hopping_covariance_maximum_absolute_EG",
            "anisotropic_D2_hopping_covariance_maximum_absolute_EG",
            "alignment_unitarity_maximum_absolute",
            "known_recovery_maximum_absolute_EG",
            "known_recovery_frobenius_EG",
            "gauge_bridge_maximum_absolute_EG",
            "symmetry_covariance_maximum_absolute_EG",
            "axis_swap_covariance_maximum_absolute_EG",
            "fit_maximum_absolute_EG",
            "fit_frobenius_EG",
            "radius_two_exterior_maximum_absolute_EG",
            "schedule_maximum_absolute",
        )
        criteria = {
            name: self._json.real(criteria_raw[name], name) for name in criterion_names
        }
        d4 = (
            PointOperation("identity", ((1, 0), (0, 1))),
            PointOperation("quarter_turn", ((0, -1), (1, 0))),
            PointOperation("half_turn", ((-1, 0), (0, -1))),
            PointOperation("three_quarter_turn", ((0, 1), (-1, 0))),
            PointOperation("reflection_x", ((1, 0), (0, -1))),
            PointOperation("reflection_y", ((-1, 0), (0, 1))),
            PointOperation("reflection_diagonal", ((0, 1), (1, 0))),
            PointOperation("reflection_antidiagonal", ((0, -1), (-1, 0))),
        )
        d2 = (d4[0], d4[2], d4[4], d4[5])
        controls = ParentControls(
            shape[0],
            shape[1],
            cast(tuple[FloatPair, FloatPair], twists),
            model_classes,
            d4,
            d2,
            d4[6],
            tuple(defects),
            *actual_inventory,
            criteria,
        )
        return controls, design_sha256


class AuthoredParentFixtureDeserializer:
    """Deserialize only the maintained non-parent behavioral fixture."""

    __slots__ = ("_json",)

    def __init__(self) -> None:
        self._json = ParentJsonReader()

    def execute(self, path: Path) -> ParentFixture:
        encoded = path.read_bytes()
        raw = self._json.mapping(cast(JsonValue, json.loads(encoded)), "fixture")
        if raw.get("fixture_id") != (
            "research-monograph.impurity-defect-2d.stage-c.accepted-parent."
            "authored-fixture.v1"
        ):
            raise ValueError("unexpected Stage C authored fixture")
        if raw.get("evidence_status") != (
            "authored synthetic software-verification fixture; "
            "not accepted-parent evidence"
        ):
            raise ValueError("fixture evidence status is not execution-free")
        if self._json.boolean(raw["accepted_parent"], "accepted_parent"):
            raise ValueError("accepted-parent fixtures are forbidden in this mode")
        isotropic = self._json.mapping(raw["isotropic_parent"], "isotropic parent")
        hoppings: list[ParentHopping] = []
        for value in self._json.array(isotropic["hoppings"], "isotropic hoppings"):
            record = self._json.mapping(value, "hopping")
            hoppings.append(
                ParentHopping(
                    (
                        self._json.integer(record["rx"], "rx"),
                        self._json.integer(record["ry"], "ry"),
                    ),
                    complex(
                        self._json.real(record["real"], "real"),
                        self._json.real(record["imag"], "imag"),
                    ),
                )
            )
        if len(hoppings) != 61:
            raise ValueError("authored isotropic fixture requires 61 hoppings")
        anisotropic = self._json.mapping(
            raw["anisotropic_parent"], "anisotropic parent"
        )
        mesh = self._json.integer(
            anisotropic["reciprocal_mesh_size"], "reciprocal mesh"
        )
        if mesh != 15:
            raise ValueError("authored anisotropic fixture requires mesh 15")
        energies: list[tuple[float, ...]] = []
        for row_value in self._json.array(
            anisotropic["band_energies"], "band energies"
        ):
            row = tuple(
                self._json.real(value, "band energy")
                for value in self._json.array(row_value, "band row")
            )
            if len(row) != mesh:
                raise ValueError("band-energy row length differs from mesh")
            energies.append(row)
        if len(energies) != mesh:
            raise ValueError("band-energy row count differs from mesh")
        return ParentFixture(
            tuple(hoppings),
            tuple(energies),
            mesh,
            self._json.integer(
                anisotropic["hopping_maximum_squared_radius"], "hopping radius"
            ),
            hashlib.sha256(encoded).hexdigest(),
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


class ParentModelFitter:
    """Fit each oriented frozen real model class and retain locality residuals."""

    __slots__ = ("_matrix",)

    def __init__(self, matrix: ParentMatrixConstructor) -> None:
        self._matrix = matrix

    def execute(
        self,
        controls: ParentControls,
        target: ComplexMatrix,
        twist: FloatPair,
        route: str,
        operation: PointOperation,
        model_class: str,
    ) -> dict[str, JsonValue]:
        basis = self._basis(controls, twist, route, operation, model_class)
        columns = np.column_stack(
            [
                np.concatenate((value.real.ravel(), value.imag.ravel()))
                for _, value in basis
            ]
        )
        vector = np.concatenate((target.real.ravel(), target.imag.ravel()))
        coefficients, _, rank, _ = np.linalg.lstsq(columns, vector, rcond=None)
        fitted = np.zeros_like(target)
        coefficient_record: dict[str, JsonValue] = {}
        for coefficient, (name, value) in zip(coefficients, basis, strict=True):
            fitted += float(coefficient) * value
            coefficient_record[name] = float(coefficient)
        residual = target - fitted
        maximum = self._matrix.maximum(residual)
        frobenius = float(np.linalg.norm(residual, ord="fro"))
        spectral = float(np.linalg.norm(residual, ord=2))
        shell = self._shell(controls, residual)
        core_exterior = self._core_exterior(controls, residual)
        basis_support = np.zeros_like(target)
        for _, value in basis:
            basis_support += np.abs(value)
        target_support_sha256 = self._support_digest(target)
        fitted_support_sha256 = self._support_digest(fitted)
        exact_support_match = target_support_sha256 == fitted_support_sha256
        return {
            "model_class": model_class,
            "coefficients": coefficient_record,
            "basis_rank": int(rank),
            "residual_maximum_absolute": maximum,
            "residual_frobenius": frobenius,
            "residual_spectral": spectral,
            "residual_shells": cast(JsonValue, shell),
            "core_exterior_coupling_frobenius": core_exterior,
            "basis_support_sha256": self._support_digest(basis_support),
            "target_support_sha256": target_support_sha256,
            "fitted_support_sha256": fitted_support_sha256,
            "residual_support_sha256": self._support_digest(residual),
            "exact_support_match": exact_support_match,
            "accepted": (
                maximum <= controls.criteria["fit_maximum_absolute_EG"]
                and frobenius <= controls.criteria["fit_frobenius_EG"]
                and shell["exterior"]["maximum_absolute"]
                <= controls.criteria["radius_two_exterior_maximum_absolute_EG"]
                and exact_support_match
            ),
        }

    def _basis(
        self,
        controls: ParentControls,
        twist: FloatPair,
        route: str,
        operation: PointOperation,
        model_class: str,
    ) -> tuple[tuple[str, ComplexMatrix], ...]:
        def transformed(term: LocalBond) -> ComplexMatrix:
            return self._matrix.defect(
                controls,
                (self._matrix.transform_bond(term, operation),),
                twist,
                route,
            )

        origin = self._matrix.transform_bond(
            LocalBond((0, 0), (1, 0), 0.0), operation
        ).start
        x_site = self._matrix.transform_bond(
            LocalBond((1, 0), (1, 0), 0.0), operation
        ).start
        y_site = self._matrix.transform_bond(
            LocalBond((0, 1), (1, 0), 0.0), operation
        ).start
        onsite = ("origin_onsite", self._matrix.onsite(controls, origin))
        x_onsite = (
            "positive_x_neighbor_onsite",
            self._matrix.onsite(controls, x_site),
        )
        y_onsite = (
            "positive_y_neighbor_onsite",
            self._matrix.onsite(controls, y_site),
        )
        x_bond = transformed(LocalBond((0, 0), (1, 0), 1.0))
        y_bond = transformed(LocalBond((0, 0), (0, 1), 1.0))
        diagonal = transformed(LocalBond((0, 0), (1, 1), 1.0))
        if model_class == "point_scalar_onsite":
            return (onsite,)
        if model_class == "finite_support_diagonal_onsite":
            return onsite, x_onsite, y_onsite
        if model_class == "onsite_plus_isotropic_nearest_neighbor":
            return onsite, ("isotropic_nearest_neighbor", x_bond + y_bond)
        if model_class == "onsite_plus_directional_nearest_neighbor":
            return (
                onsite,
                ("positive_x_bond", x_bond),
                (
                    "positive_y_bond",
                    y_bond,
                ),
            )
        if model_class == "finite_range_nonlocal_radius_two":
            return (
                onsite,
                ("positive_x_bond", x_bond),
                ("positive_y_bond", y_bond),
                ("positive_diagonal_bond", diagonal),
            )
        raise ValueError(f"unsupported model class {model_class}")

    @staticmethod
    def _shell(
        controls: ParentControls, residual: ComplexMatrix
    ) -> dict[str, dict[str, float]]:
        values: dict[str, list[complex]] = {
            "0": [],
            "1": [],
            "2": [],
            "exterior": [],
        }
        for row in range(controls.dimension):
            rx, ry = divmod(row, controls.ny)
            for column in range(controls.dimension):
                value = complex(residual[row, column])
                if value == 0.0:
                    continue
                cx, cy = divmod(column, controls.ny)
                shell = max(
                    min(rx, controls.nx - rx),
                    min(ry, controls.ny - ry),
                    min(cx, controls.nx - cx),
                    min(cy, controls.ny - cy),
                )
                key = str(shell) if shell <= 2 else "exterior"
                values[key].append(value)
        return {
            key: {
                "maximum_absolute": max((abs(value) for value in entries), default=0.0),
                "frobenius": float(np.sqrt(sum(abs(value) ** 2 for value in entries))),
            }
            for key, entries in values.items()
        }

    @staticmethod
    def _core_exterior(controls: ParentControls, matrix: ComplexMatrix) -> float:
        core: list[int] = []
        for index in range(controls.dimension):
            x, y = divmod(index, controls.ny)
            if max(min(x, controls.nx - x), min(y, controls.ny - y)) <= 2:
                core.append(index)
        exterior = [index for index in range(controls.dimension) if index not in core]
        return float(
            np.sqrt(
                np.linalg.norm(matrix[np.ix_(core, exterior)], ord="fro") ** 2
                + np.linalg.norm(matrix[np.ix_(exterior, core)], ord="fro") ** 2
            )
        )

    @staticmethod
    def _support_digest(matrix: ComplexMatrix) -> str:
        support = np.argwhere(np.abs(matrix) > 1.0e-12)
        return hashlib.sha256(
            np.ascontiguousarray(support, dtype="<i8").tobytes()
        ).hexdigest()


class RouteIndependenceGate:
    """Reject a route constructor that declares another route as its source."""

    __slots__ = ()

    @staticmethod
    def execute(route: str, source: str) -> None:
        expected = {
            "A_centered_uniform": "compact_parent_inputs",
            "B_reduced_seam": "compact_parent_inputs",
        }
        if route not in expected:
            raise ValueError(f"unsupported route provenance {route}")
        if source != expected[route]:
            raise ValueError("DEFECT_2D.ROUTE_INDEPENDENCE_VIOLATION")


class ParentScheduleExecutor:
    """Execute one complete route order in one spawned process."""

    __slots__ = ()

    def execute(
        self,
        controls: ParentControls,
        fixture: ParentFixture,
        schedule_id: str,
        route_order: tuple[str, str],
    ) -> ParentScheduleResult:
        hopping = ParentHoppingConstructor()
        matrix = ParentMatrixConstructor()
        fitter = ParentModelFitter(matrix)
        anisotropic_full = hopping.anisotropic(fixture)
        anisotropic = hopping.compact(
            anisotropic_full, fixture.hopping_maximum_squared_radius
        )
        swapped = hopping.swapped(anisotropic)
        parents = {
            "isotropic_lambda_0p5_0p5_0": fixture.isotropic_hoppings,
            "anisotropic_lambda_0p3_0p7_0": anisotropic,
            "anisotropic_lambda_0p7_0p3_0": swapped,
        }
        preprocessing = self._preprocessing(
            controls, fixture, anisotropic_full, anisotropic, swapped
        )
        cases = self._cases(controls)
        attack = matrix.attack(controls)
        identity = np.eye(controls.dimension, dtype=np.complex128)
        route_records: list[dict[str, JsonValue]] = []
        matrices: dict[tuple[str, str, str], ComplexMatrix] = {}
        recovered_bytes: list[tuple[MatrixKey, bytes]] = []
        provenance_gate = RouteIndependenceGate()
        for route in route_order:
            provenance_gate.execute(route, "compact_parent_inputs")
            for case in cases:
                case_id = case.case_id
                base_twist = case.base_twist
                operation = case.operation
                transformed_twist_lift = matrix.transform_twist(base_twist, operation)
                transformed_twist = (
                    transformed_twist_lift
                    if route == "A_centered_uniform"
                    else matrix.reduce_twist(transformed_twist_lift)
                )
                source_twist = (
                    base_twist
                    if route == "A_centered_uniform"
                    else matrix.reduce_twist(base_twist)
                )
                source_parent_id = case.source_parent_id
                target_parent_id = case.target_parent_id
                source_terms = case.source_terms
                target_terms = tuple(
                    matrix.transform_bond(term, operation) for term in source_terms
                )
                source_parent = matrix.parent(
                    controls, parents[source_parent_id], source_twist, route
                )
                target_parent = matrix.parent(
                    controls, parents[target_parent_id], transformed_twist, route
                )
                source_defect = matrix.defect(
                    controls, source_terms, source_twist, route
                )
                target_defect = matrix.defect(
                    controls, target_terms, transformed_twist, route
                )
                source_full = source_parent + source_defect
                target_full = target_parent + target_defect
                permutation = matrix.permutation(controls, operation)
                if route == "A_centered_uniform":
                    covariance_residual = (
                        target_full - permutation @ source_full @ permutation.conj().T
                    )
                else:
                    source_gauge = matrix.gauge(controls, base_twist)
                    target_gauge = matrix.gauge(controls, transformed_twist_lift)
                    source_uniform = source_gauge.conj().T @ source_full @ source_gauge
                    target_uniform = target_gauge.conj().T @ target_full @ target_gauge
                    covariance_residual = (
                        target_uniform
                        - permutation @ source_uniform @ permutation.conj().T
                    )
                if route == "A_centered_uniform":
                    route_attack = attack
                else:
                    target_gauge = matrix.gauge(controls, transformed_twist_lift)
                    route_attack = target_gauge @ attack @ target_gauge.conj().T
                attacked = (
                    route_attack @ target_full @ route_attack.conj().T
                    + 0.137 * identity
                )
                aligned = (
                    route_attack.conj().T @ (attacked - 0.137 * identity) @ route_attack
                )
                recovered = aligned - target_parent
                recovery = recovered - target_defect
                fits: list[dict[str, JsonValue]] = []
                selected: str | None = None
                for model_class in controls.model_classes:
                    fit = fitter.execute(
                        controls,
                        recovered,
                        transformed_twist,
                        route,
                        operation,
                        model_class,
                    )
                    fits.append(fit)
                    if selected is None and fit["accepted"] is True:
                        selected = model_class
                record = {
                    "route": route,
                    "case_id": case_id,
                    "parent_family": case.parent_family,
                    "source_parent_id": source_parent_id,
                    "target_parent_id": target_parent_id,
                    "defect_id": case.defect_id,
                    "twist_id": case.twist_id,
                    "operation": operation.identifier,
                    "transformed_twist_lift": cast(
                        JsonValue, list(transformed_twist_lift)
                    ),
                    "comparison_twist": cast(JsonValue, list(transformed_twist)),
                    "parent_sha256": matrix.digest(target_parent),
                    "defect_sha256": matrix.digest(target_defect),
                    "full_sha256": matrix.digest(target_full),
                    "attacked_sha256": matrix.digest(attacked),
                    "recovered_sha256": matrix.digest(recovered),
                    "parent_hermiticity_maximum_absolute": matrix.maximum(
                        target_parent - target_parent.conj().T
                    ),
                    "defect_hermiticity_maximum_absolute": matrix.maximum(
                        target_defect - target_defect.conj().T
                    ),
                    "alignment_unitarity_maximum_absolute": matrix.maximum(
                        route_attack.conj().T @ route_attack - identity
                    ),
                    "recovery_maximum_absolute": matrix.maximum(recovery),
                    "recovery_frobenius": float(np.linalg.norm(recovery, ord="fro")),
                    "covariance_maximum_absolute": matrix.maximum(covariance_residual),
                    "covariance_frobenius": float(
                        np.linalg.norm(covariance_residual, ord="fro")
                    ),
                    "selected_model_class": selected,
                    "expected_model_class": case.expected_model_class,
                    "fits": cast(JsonValue, fits),
                }
                route_records.append(record)
                matrices[(route, case_id, "parent")] = target_parent
                matrices[(route, case_id, "defect")] = target_defect
                matrices[(route, case_id, "full")] = target_full
                matrices[(route, case_id, "attacked")] = attacked
                matrices[(route, case_id, "recovered")] = recovered
                recovered_bytes.append(
                    (
                        (route, case_id),
                        np.ascontiguousarray(recovered, dtype="<c16").tobytes(),
                    )
                )
        route_records.sort(key=self._record_key)
        bridge_records = self._bridges(controls, cases, matrices)
        adverse = self._adverse(
            controls, parents, route_records, matrix, fitter, attack
        )
        payload: dict[str, JsonValue] = {
            "schedule_id": schedule_id,
            "route_order": cast(JsonValue, list(route_order)),
            "fresh_spawned_process": True,
            "preprocessing": preprocessing,
            "route_records": cast(JsonValue, route_records),
            "bridge_records": cast(JsonValue, bridge_records),
            "adverse_controls": cast(JsonValue, adverse),
        }
        return ParentScheduleResult(
            schedule_id,
            os.getpid(),
            json.dumps(payload, sort_keys=True, separators=(",", ":")),
            tuple(sorted(recovered_bytes, key=lambda value: value[0])),
        )

    @staticmethod
    def _record_key(record: dict[str, JsonValue]) -> tuple[str, str]:
        return cast(str, record["case_id"]), cast(str, record["route"])

    def _preprocessing(
        self,
        controls: ParentControls,
        fixture: ParentFixture,
        full: tuple[ParentHopping, ...],
        compact: tuple[ParentHopping, ...],
        swapped: tuple[ParentHopping, ...],
    ) -> dict[str, JsonValue]:
        constructor = ParentHoppingConstructor()
        matrix = ParentMatrixConstructor()
        isotropic_metrics = constructor.validate(
            fixture.isotropic_hoppings, controls.d4
        )
        full_metrics = constructor.validate(full, controls.d2)
        compact_metrics = constructor.validate(compact, controls.d2)
        swapped_metrics = constructor.validate(swapped, controls.d2)
        truncation: list[JsonValue] = []
        for twist_id, twist in zip(("gamma", "generic"), controls.twists, strict=True):
            full_matrix = matrix.parent(controls, full, twist, "A_centered_uniform")
            compact_matrix = matrix.parent(
                controls, compact, twist, "A_centered_uniform"
            )
            residual = full_matrix - compact_matrix
            truncation.append(
                {
                    "twist_id": twist_id,
                    "maximum_absolute": matrix.maximum(residual),
                    "frobenius": float(np.linalg.norm(residual, ord="fro")),
                }
            )
        return {
            "fixture_sha256": fixture.fixture_sha256,
            "isotropic": isotropic_metrics,
            "pretruncation": full_metrics,
            "compact": compact_metrics,
            "axis_swapped": swapped_metrics,
            "truncation": truncation,
        }

    def _cases(self, controls: ParentControls) -> tuple[ParentCase, ...]:
        result: list[ParentCase] = []
        for defect_id, terms, expected in controls.defects:
            for twist_id, twist in zip(
                ("gamma", "generic"), controls.twists, strict=True
            ):
                for operation in controls.d4:
                    result.append(
                        ParentCase(
                            f"isotropic__{defect_id}__{twist_id}__"
                            f"{operation.identifier}",
                            "isotropic_D4",
                            "isotropic_lambda_0p5_0p5_0",
                            "isotropic_lambda_0p5_0p5_0",
                            defect_id,
                            terms,
                            expected,
                            twist_id,
                            twist,
                            operation,
                        )
                    )
                for operation in controls.d2:
                    result.append(
                        ParentCase(
                            f"anisotropic_D2__{defect_id}__{twist_id}__"
                            f"{operation.identifier}",
                            "anisotropic_D2",
                            "anisotropic_lambda_0p3_0p7_0",
                            "anisotropic_lambda_0p3_0p7_0",
                            defect_id,
                            terms,
                            expected,
                            twist_id,
                            twist,
                            operation,
                        )
                    )
                result.append(
                    ParentCase(
                        f"axis_swap__{defect_id}__{twist_id}__reflection_diagonal",
                        "anisotropic_axis_swap",
                        "anisotropic_lambda_0p3_0p7_0",
                        "anisotropic_lambda_0p7_0p3_0",
                        defect_id,
                        terms,
                        expected,
                        twist_id,
                        twist,
                        controls.axis_swap,
                    )
                )
        if len(result) != 52:
            raise ValueError("accepted-parent Stage C requires 52 cases per schedule")
        return tuple(result)

    def _bridges(
        self,
        controls: ParentControls,
        cases: tuple[ParentCase, ...],
        matrices: dict[tuple[str, str, str], ComplexMatrix],
    ) -> list[dict[str, JsonValue]]:
        matrix = ParentMatrixConstructor()
        result: list[dict[str, JsonValue]] = []
        for case in cases:
            case_id = case.case_id
            operation = case.operation
            base_twist = case.base_twist
            lift = matrix.transform_twist(base_twist, operation)
            gauge = matrix.gauge(controls, lift)
            record: dict[str, JsonValue] = {"case_id": case_id}
            for subject in ("parent", "defect", "full", "attacked", "recovered"):
                route_a = matrices[("A_centered_uniform", case_id, subject)]
                route_b = matrices[("B_reduced_seam", case_id, subject)]
                residual = route_b - gauge @ route_a @ gauge.conj().T
                record[f"{subject}_maximum_absolute"] = matrix.maximum(residual)
                record[f"{subject}_frobenius"] = float(
                    np.linalg.norm(residual, ord="fro")
                )
            result.append(record)
        return result

    def _adverse(
        self,
        controls: ParentControls,
        parents: dict[str, tuple[ParentHopping, ...]],
        route_records: list[dict[str, JsonValue]],
        matrix: ParentMatrixConstructor,
        fitter: ParentModelFitter,
        attack: ComplexMatrix,
    ) -> list[dict[str, JsonValue]]:
        gamma = controls.twists[0]
        generic = controls.twists[1]
        identity_operation = controls.d4[0]
        quarter = controls.d4[1]
        directional_terms = controls.defects[0][1]
        nonlocal_terms = controls.defects[1][1]
        directional = matrix.defect(
            controls, directional_terms, gamma, "A_centered_uniform"
        )
        isotropic_fit = fitter.execute(
            controls,
            directional,
            gamma,
            "A_centered_uniform",
            identity_operation,
            "onsite_plus_isotropic_nearest_neighbor",
        )
        nonlocal_matrix = matrix.defect(
            controls, nonlocal_terms, gamma, "A_centered_uniform"
        )
        directional_fit = fitter.execute(
            controls,
            nonlocal_matrix,
            gamma,
            "A_centered_uniform",
            identity_operation,
            "onsite_plus_directional_nearest_neighbor",
        )
        omitted = matrix.defect(
            controls,
            (directional_terms[0],),
            gamma,
            "A_centered_uniform",
            include_reverse=False,
        )
        route_a_defect = matrix.defect(
            controls, directional_terms, generic, "A_centered_uniform"
        )
        route_b_defect = matrix.defect(
            controls, directional_terms, generic, "B_reduced_seam"
        )
        isotropic_parent = parents["isotropic_lambda_0p5_0p5_0"]
        source_iso = matrix.parent(
            controls, isotropic_parent, generic, "A_centered_uniform"
        )
        rotated_lift = matrix.transform_twist(generic, quarter)
        fixed_twist_target = matrix.parent(
            controls, isotropic_parent, generic, "A_centered_uniform"
        )
        permutation = matrix.permutation(controls, quarter)
        fixed_twist = (
            fixed_twist_target - permutation @ source_iso @ permutation.conj().T
        )
        anisotropic_parent = parents["anisotropic_lambda_0p3_0p7_0"]
        source_anis = matrix.parent(
            controls, anisotropic_parent, generic, "A_centered_uniform"
        )
        invalid_d4_target = matrix.parent(
            controls, anisotropic_parent, rotated_lift, "A_centered_uniform"
        )
        invalid_d4 = (
            invalid_d4_target - permutation @ source_anis @ permutation.conj().T
        )
        swap = controls.axis_swap
        swap_permutation = matrix.permutation(controls, swap)
        swap_lift = matrix.transform_twist(generic, swap)
        unswapped_target = matrix.parent(
            controls, anisotropic_parent, swap_lift, "A_centered_uniform"
        )
        unswapped = (
            unswapped_target
            - swap_permutation @ source_anis @ swap_permutation.conj().T
        )
        identity = np.eye(controls.dimension, dtype=np.complex128)
        alignment_unitarity = matrix.maximum(attack.conj().T @ attack - identity)
        if (
            alignment_unitarity
            > controls.criteria["alignment_unitarity_maximum_absolute"]
        ):
            raise ValueError("authored attack is not unitary")
        route_b_records = [
            record for record in route_records if record["route"] == "B_reduced_seam"
        ]
        route_violation_status = "missing_failure"
        try:
            RouteIndependenceGate().execute(
                "B_reduced_seam", "A_centered_uniform_matrix"
            )
        except ValueError as error:
            route_violation_status = str(error)
        return [
            {
                "control_id": "prealignment_subtraction",
                "status": "DEFECT_2D.SITE_MAP_UNRESOLVED",
                "value": None,
            },
            {
                "control_id": "omit_energy_reference_correction",
                "status": "discriminating",
                "value": float(np.linalg.norm(0.137 * identity, ord="fro")),
            },
            {
                "control_id": "directional_as_isotropic",
                "status": "discriminating",
                "value": isotropic_fit["residual_frobenius"],
            },
            {
                "control_id": "nonlocal_as_directional",
                "status": "discriminating",
                "value": directional_fit["residual_frobenius"],
            },
            {
                "control_id": "omit_hermitian_reverse",
                "status": "discriminating",
                "value": matrix.maximum(omitted - omitted.conj().T),
            },
            {
                "control_id": "compare_raw_gauges_without_bridge",
                "status": "discriminating",
                "value": matrix.maximum(route_b_defect - route_a_defect),
            },
            {
                "control_id": "hold_generic_twist_fixed_under_quarter_turn",
                "status": "discriminating",
                "value": matrix.maximum(fixed_twist),
            },
            {
                "control_id": "claim_D4_for_anisotropic_parent",
                "status": "discriminating",
                "value": matrix.maximum(invalid_d4),
            },
            {
                "control_id": "axis_swap_defect_without_parent_swap",
                "status": "discriminating",
                "value": matrix.maximum(unswapped),
            },
            {
                "control_id": "construct_route_B_from_route_A",
                "status": route_violation_status,
                "value": float(len(route_b_records)),
            },
        ]


class AcceptedParentStageCToyStudy:
    """Compose two fresh schedules and evaluate the adopted contract."""

    __slots__ = ()

    def execute(
        self,
        controls: ParentControls,
        fixture: ParentFixture,
        design_sha256: str,
    ) -> dict[str, JsonValue]:
        schedules = (
            ("A_then_B", ("A_centered_uniform", "B_reduced_seam")),
            ("B_then_A", ("B_reduced_seam", "A_centered_uniform")),
        )
        context = multiprocessing.get_context("spawn")
        action = ParentScheduleExecutor()
        with (
            concurrent.futures.ProcessPoolExecutor(
                max_workers=1, mp_context=context
            ) as first_executor,
            concurrent.futures.ProcessPoolExecutor(
                max_workers=1, mp_context=context
            ) as second_executor,
        ):
            futures = (
                first_executor.submit(action.execute, controls, fixture, *schedules[0]),
                second_executor.submit(
                    action.execute, controls, fixture, *schedules[1]
                ),
            )
            schedule_results = [future.result() for future in futures]
        process_ids = {result.process_id for result in schedule_results}
        if len(process_ids) != 2 or os.getpid() in process_ids:
            raise RuntimeError(
                "Stage C parent schedules did not use distinct processes"
            )
        schedules_payload: list[dict[str, JsonValue]] = []
        matrices: dict[str, dict[MatrixKey, ComplexMatrix]] = {}
        for result in schedule_results:
            payload = cast(JsonValue, json.loads(result.payload_json))
            if not isinstance(payload, dict):
                raise TypeError("schedule payload must be a JSON object")
            schedules_payload.append(payload)
            matrices[result.schedule_id] = {
                key: np.frombuffer(value, dtype="<c16").reshape(
                    (controls.dimension, controls.dimension)
                )
                for key, value in result.recovered_matrices
            }
        schedules_payload.sort(key=lambda value: cast(str, value["schedule_id"]))
        schedule_comparisons: list[JsonValue] = []
        maximum_schedule = 0.0
        first = matrices["A_then_B"]
        second = matrices["B_then_A"]
        matrix_action = ParentMatrixConstructor()
        for key in sorted(first):
            residual = first[key] - second[key]
            maximum = matrix_action.maximum(residual)
            maximum_schedule = max(maximum_schedule, maximum)
            schedule_comparisons.append(
                {
                    "route": key[0],
                    "case_id": key[1],
                    "maximum_absolute": maximum,
                    "frobenius": float(np.linalg.norm(residual, ord="fro")),
                }
            )
        if len(schedule_comparisons) != controls.schedule_comparisons:
            raise ValueError("schedule-comparison inventory differs")
        summary, criteria = self._evaluate(
            controls, schedules_payload, maximum_schedule
        )
        return {
            "schema_version": 1,
            "result_id": (
                "research-monograph.impurity-defect-2d.stage-c."
                "accepted-parent-authored-fixture.v1"
            ),
            "evidence_status": (
                "authored synthetic execution-free software-verification behavior; "
                "not accepted-parent evidence"
            ),
            "accepted_parent_read": False,
            "design_sha256": design_sha256,
            "fixture_sha256": fixture.fixture_sha256,
            "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "software_versions": {
                "python": platform.python_version(),
                "numpy": np.__version__,
            },
            "inventory": {
                "execution_schedules": 2,
                "route_evaluations": controls.route_evaluations,
                "bridge_records": controls.bridge_records,
                "model_fit_records": controls.model_fit_records,
                "schedule_comparisons": controls.schedule_comparisons,
            },
            "schedules": cast(JsonValue, schedules_payload),
            "schedule_comparisons": schedule_comparisons,
            "criteria": cast(JsonValue, criteria),
            "summary": summary,
        }

    def _evaluate(
        self,
        controls: ParentControls,
        schedules: list[dict[str, JsonValue]],
        maximum_schedule: float,
    ) -> tuple[dict[str, JsonValue], list[dict[str, JsonValue]]]:
        route_records = [
            cast(dict[str, JsonValue], record)
            for schedule in schedules
            for record in cast(list[JsonValue], schedule["route_records"])
        ]
        bridges = [
            cast(dict[str, JsonValue], record)
            for schedule in schedules
            for record in cast(list[JsonValue], schedule["bridge_records"])
        ]
        preprocessing = [
            cast(dict[str, JsonValue], schedule["preprocessing"])
            for schedule in schedules
        ]
        if len(route_records) != controls.route_evaluations:
            raise ValueError("route-evaluation inventory differs")
        if len(bridges) != controls.bridge_records:
            raise ValueError("bridge inventory differs")
        fit_count = sum(
            len(cast(list[JsonValue], record["fits"])) for record in route_records
        )
        if fit_count != controls.model_fit_records:
            raise ValueError("model-fit inventory differs")
        maximum_parent_hermiticity = max(
            cast(float, record["parent_hermiticity_maximum_absolute"])
            for record in route_records
        )
        maximum_defect_hermiticity = max(
            cast(float, record["defect_hermiticity_maximum_absolute"])
            for record in route_records
        )
        hopping_records = [
            cast(dict[str, JsonValue], value[name])
            for value in preprocessing
            for name in ("isotropic", "pretruncation", "compact", "axis_swapped")
        ]
        maximum_hopping_hermiticity = max(
            cast(float, record["hermiticity_maximum_absolute"])
            for record in hopping_records
        )
        isotropic_hopping_symmetry = max(
            cast(
                float,
                cast(dict[str, JsonValue], value["isotropic"])[
                    "symmetry_maximum_absolute"
                ],
            )
            for value in preprocessing
        )
        anisotropic_hopping_symmetry = max(
            cast(
                float,
                cast(dict[str, JsonValue], value[name])["symmetry_maximum_absolute"],
            )
            for value in preprocessing
            for name in ("pretruncation", "compact", "axis_swapped")
        )
        maximum_alignment = max(
            cast(float, record["alignment_unitarity_maximum_absolute"])
            for record in route_records
        )
        maximum_recovery = max(
            cast(float, record["recovery_maximum_absolute"]) for record in route_records
        )
        maximum_recovery_frobenius = max(
            cast(float, record["recovery_frobenius"]) for record in route_records
        )
        isotropic_covariance = max(
            cast(float, record["covariance_maximum_absolute"])
            for record in route_records
            if record["parent_family"] == "isotropic_D4"
        )
        anisotropic_covariance = max(
            cast(float, record["covariance_maximum_absolute"])
            for record in route_records
            if record["parent_family"] == "anisotropic_D2"
        )
        axis_swap_covariance = max(
            cast(float, record["covariance_maximum_absolute"])
            for record in route_records
            if record["parent_family"] == "anisotropic_axis_swap"
        )
        maximum_covariance = max(
            isotropic_covariance, anisotropic_covariance, axis_swap_covariance
        )
        maximum_bridge = max(
            cast(float, value)
            for record in bridges
            for key, value in record.items()
            if key.endswith("_maximum_absolute")
        )
        selected_fits: list[dict[str, JsonValue]] = []
        for record in route_records:
            selected = record["selected_model_class"]
            for fit_value in cast(list[JsonValue], record["fits"]):
                fit = cast(dict[str, JsonValue], fit_value)
                if fit["model_class"] == selected:
                    selected_fits.append(fit)
        if len(selected_fits) != controls.route_evaluations:
            raise ValueError("selected-fit inventory differs")
        selected_fit_maximum = max(
            cast(float, fit["residual_maximum_absolute"]) for fit in selected_fits
        )
        selected_fit_frobenius = max(
            cast(float, fit["residual_frobenius"]) for fit in selected_fits
        )
        selected_exterior = max(
            cast(
                float,
                cast(
                    dict[str, JsonValue],
                    cast(dict[str, JsonValue], fit["residual_shells"])["exterior"],
                )["maximum_absolute"],
            )
            for fit in selected_fits
        )
        exact_support_agreement = all(
            fit["exact_support_match"] is True for fit in selected_fits
        )
        selection_agreement = all(
            record["selected_model_class"] == record["expected_model_class"]
            for record in route_records
        )
        compact_digests = [
            cast(str, cast(dict[str, JsonValue], value["compact"])["sha256"])
            for value in preprocessing
        ]
        preprocessing_agreement = compact_digests[0] == compact_digests[1]
        adverse = cast(list[dict[str, JsonValue]], schedules[0]["adverse_controls"])
        adverse_values = {
            cast(str, record["control_id"]): record["value"] for record in adverse
        }
        adverse_pass = (
            adverse[0]["status"] == "DEFECT_2D.SITE_MAP_UNRESOLVED"
            and cast(float, adverse_values["omit_energy_reference_correction"]) >= 1.0
            and cast(float, adverse_values["directional_as_isotropic"]) >= 0.03
            and cast(float, adverse_values["nonlocal_as_directional"]) >= 0.03
            and cast(float, adverse_values["omit_hermitian_reverse"]) >= 0.03
            and cast(float, adverse_values["compare_raw_gauges_without_bridge"]) >= 0.01
            and cast(
                float,
                adverse_values["hold_generic_twist_fixed_under_quarter_turn"],
            )
            >= 1.0e-6
            and cast(float, adverse_values["claim_D4_for_anisotropic_parent"]) >= 1.0e-3
            and cast(float, adverse_values["axis_swap_defect_without_parent_swap"])
            >= 1.0e-3
            and adverse[9]["status"] == "DEFECT_2D.ROUTE_INDEPENDENCE_VIOLATION"
        )
        criteria: list[dict[str, JsonValue]] = [
            self._criterion(
                "hopping_and_matrix_hermiticity",
                max(
                    maximum_hopping_hermiticity,
                    maximum_parent_hermiticity,
                    maximum_defect_hermiticity,
                ),
                controls.criteria["hopping_hermiticity_maximum_absolute_EG"],
                "<=",
            ),
            self._criterion(
                "isotropic_D4_hopping_covariance",
                isotropic_hopping_symmetry,
                controls.criteria[
                    "isotropic_D4_hopping_covariance_maximum_absolute_EG"
                ],
                "<=",
            ),
            self._criterion(
                "anisotropic_D2_hopping_covariance",
                anisotropic_hopping_symmetry,
                controls.criteria[
                    "anisotropic_D2_hopping_covariance_maximum_absolute_EG"
                ],
                "<=",
            ),
            self._criterion(
                "alignment_unitarity",
                maximum_alignment,
                controls.criteria["alignment_unitarity_maximum_absolute"],
                "<=",
            ),
            self._criterion(
                "known_recovery_maximum",
                maximum_recovery,
                controls.criteria["known_recovery_maximum_absolute_EG"],
                "<=",
            ),
            self._criterion(
                "known_recovery_frobenius",
                maximum_recovery_frobenius,
                controls.criteria["known_recovery_frobenius_EG"],
                "<=",
            ),
            self._criterion(
                "isotropic_D4_covariance",
                isotropic_covariance,
                controls.criteria["symmetry_covariance_maximum_absolute_EG"],
                "<=",
            ),
            self._criterion(
                "anisotropic_D2_covariance",
                anisotropic_covariance,
                controls.criteria["symmetry_covariance_maximum_absolute_EG"],
                "<=",
            ),
            self._criterion(
                "axis_swap_covariance",
                axis_swap_covariance,
                controls.criteria["axis_swap_covariance_maximum_absolute_EG"],
                "<=",
            ),
            self._criterion(
                "gauge_bridge",
                maximum_bridge,
                controls.criteria["gauge_bridge_maximum_absolute_EG"],
                "<=",
            ),
            self._criterion(
                "selected_fit_maximum",
                selected_fit_maximum,
                controls.criteria["fit_maximum_absolute_EG"],
                "<=",
            ),
            self._criterion(
                "selected_fit_frobenius",
                selected_fit_frobenius,
                controls.criteria["fit_frobenius_EG"],
                "<=",
            ),
            self._criterion(
                "selected_radius_two_exterior",
                selected_exterior,
                controls.criteria["radius_two_exterior_maximum_absolute_EG"],
                "<=",
            ),
            {
                "criterion": "exact_support_and_first_model_class_selection",
                "value": 1.0
                if exact_support_agreement and selection_agreement
                else 0.0,
                "comparison": "==",
                "threshold": 1.0,
                "passed": exact_support_agreement and selection_agreement,
            },
            {
                "criterion": "schedule_preprocessing_agreement",
                "value": 1.0 if preprocessing_agreement else 0.0,
                "comparison": "==",
                "threshold": 1.0,
                "passed": preprocessing_agreement,
            },
            self._criterion(
                "schedule_invariance",
                maximum_schedule,
                controls.criteria["schedule_maximum_absolute"],
                "==",
            ),
            {
                "criterion": "adverse_controls_discriminate",
                "value": 1.0 if adverse_pass else 0.0,
                "comparison": "==",
                "threshold": 1.0,
                "passed": adverse_pass,
            },
        ]
        summary: dict[str, JsonValue] = {
            "maximum_hopping_parent_or_defect_hermiticity": max(
                maximum_hopping_hermiticity,
                maximum_parent_hermiticity,
                maximum_defect_hermiticity,
            ),
            "maximum_hopping_symmetry_absolute": max(
                isotropic_hopping_symmetry, anisotropic_hopping_symmetry
            ),
            "maximum_alignment_unitarity": maximum_alignment,
            "maximum_recovery_absolute": maximum_recovery,
            "maximum_recovery_frobenius": maximum_recovery_frobenius,
            "maximum_covariance_absolute": maximum_covariance,
            "maximum_bridge_absolute": maximum_bridge,
            "maximum_selected_fit_absolute": selected_fit_maximum,
            "maximum_selected_fit_frobenius": selected_fit_frobenius,
            "maximum_selected_exterior_absolute": selected_exterior,
            "maximum_schedule_absolute": maximum_schedule,
            "preprocessing_schedule_agreement": preprocessing_agreement,
            "model_selection_agreement": selection_agreement,
            "adverse_controls_passed": adverse_pass,
            "all_criteria_passed": all(
                cast(bool, criterion["passed"]) for criterion in criteria
            ),
        }
        return summary, criteria

    @staticmethod
    def _criterion(
        identifier: str, value: float, threshold: float, comparison: str
    ) -> dict[str, JsonValue]:
        if comparison == "<=":
            passed = value <= threshold
        elif comparison == "==":
            passed = value == threshold
        else:
            raise ValueError(f"unsupported comparison {comparison}")
        return {
            "criterion": identifier,
            "value": value,
            "comparison": comparison,
            "threshold": threshold,
            "passed": passed,
        }


class AcceptedParentStageCResultSerializer:
    """Serialize one authored-fixture result deterministically and without overwrite."""

    __slots__ = ()

    @staticmethod
    def execute(result: dict[str, JsonValue], output: Path) -> None:
        if output.exists():
            raise FileExistsError(f"refusing to overwrite {output}")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
        )


class AcceptedParentStageCToyWorkflow:
    """Compose adopted design, authored fixture, schedules, and serialization."""

    __slots__ = ()

    def execute(
        self, design: Path, fixture: Path, output: Path
    ) -> dict[str, JsonValue]:
        controls, design_sha256 = AcceptedParentStageCDesignDeserializer().execute(
            design
        )
        fixture_record = AuthoredParentFixtureDeserializer().execute(fixture)
        result = AcceptedParentStageCToyStudy().execute(
            controls, fixture_record, design_sha256
        )
        AcceptedParentStageCResultSerializer().execute(result, output)
        return result


def main() -> None:
    """Adapt argparse inputs into the authored-fixture Stage C parent Workflow."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--accepted-parent-design", type=Path, required=True)
    parser.add_argument("--authored-parent-fixture", type=Path, required=True)
    parser.add_argument("--authored-parent-output", type=Path, required=True)
    arguments = parser.parse_args()
    result = AcceptedParentStageCToyWorkflow().execute(
        arguments.accepted_parent_design,
        arguments.authored_parent_fixture,
        arguments.authored_parent_output,
    )
    inventory = cast(dict[str, JsonValue], result["inventory"])
    summary = cast(dict[str, JsonValue], result["summary"])
    print(
        "stage_c_accepted_parent_authored_criteria="
        f"{'PASS' if summary['all_criteria_passed'] else 'FAIL'}"
    )
    print(f"route_evaluations={inventory['route_evaluations']}")
    print(f"model_fit_records={inventory['model_fit_records']}")


if __name__ == "__main__":
    main()
