#!/usr/bin/env python3
"""Execute authored-toy Stage C directional/nonlocal software behavior only."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import multiprocessing
import os
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type ComplexMatrix = npt.NDArray[np.complex128]
type FloatPair = tuple[float, float]
type IntPair = tuple[int, int]
type IntMatrix2 = tuple[tuple[int, int], tuple[int, int]]
type MatrixRecordKey = tuple[str, str, str]


@dataclass(frozen=True, slots=True)
class BondTerm:
    """Represent one authored real bond change before adding its reverse."""

    start: IntPair
    displacement: IntPair
    value: float

    def __post_init__(self) -> None:
        if self.displacement == (0, 0):
            raise ValueError("a bond displacement must be nonzero")
        if not np.isfinite(self.value):
            raise ValueError("a bond value must be finite")


@dataclass(frozen=True, slots=True)
class D4Operation:
    """Represent one exact integer point operation."""

    identifier: str
    matrix: IntMatrix2


@dataclass(frozen=True, slots=True)
class StageCControls:
    """Own immutable authored-toy dimensions, inventories, and tolerances."""

    nx: int
    ny: int
    twists: tuple[FloatPair, FloatPair]
    cases: tuple[tuple[str, tuple[BondTerm, ...], str], ...]
    model_classes: tuple[str, ...]
    operations: tuple[D4Operation, ...]
    hermiticity_tolerance: float
    bridge_tolerance: float
    symmetry_tolerance: float
    fit_maximum_tolerance: float
    fit_frobenius_tolerance: float
    wrong_model_floor: float
    omitted_reverse_floor: float
    omitted_bridge_floor: float

    @property
    def dimension(self) -> int:
        """Return the exact scalar site-space dimension."""

        return self.nx * self.ny


@dataclass(frozen=True, slots=True)
class StageCScheduleResult:
    """Carry one fresh-process schedule as immutable JSON and matrix bytes."""

    schedule_id: str
    route_order: tuple[str, str]
    process_id: int
    route_records_json: str
    matrix_bytes: tuple[tuple[MatrixRecordKey, bytes], ...]


class ClosedJsonReader:
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
            raise ValueError(f"{name} must have length two")
        result: list[int] = []
        for item in values:
            if isinstance(item, bool) or not isinstance(item, int):
                raise TypeError(f"{name} entries must be integers")
            result.append(item)
        return result[0], result[1]

    def real_pair(self, value: JsonValue, name: str) -> FloatPair:
        values = self.array(value, name)
        if len(values) != 2:
            raise ValueError(f"{name} must have length two")
        return self.real(values[0], name), self.real(values[1], name)


class StageCDesignDeserializer:
    """Deserialize the exact human-authorized Stage C toy design."""

    __slots__ = ("_json",)

    def __init__(self) -> None:
        self._json = ClosedJsonReader()

    def execute(self, path: Path) -> tuple[StageCControls, str]:
        encoded = path.read_bytes()
        raw = cast(JsonValue, json.loads(encoded))
        design = self._json.mapping(raw, "design")
        if design.get("design_id") != (
            "research-monograph.impurity-defect-2d.stage-c.execution-free.v1"
        ):
            raise ValueError("unexpected Stage C design identity")
        if design.get("execution_authorized_by_this_record") is not False:
            raise ValueError("the execution-free design must not authorize execution")
        toy = self._json.mapping(design["toy_space"], "toy_space")
        shape = self._json.integer_pair(toy["shape"], "toy_space.shape")
        if shape != (8, 8) or toy.get("dimension") != 64:
            raise ValueError("Stage C authored toy requires the frozen 8x8 space")
        twist_values = self._json.array(
            toy["twist_lifts_turns"], "toy_space.twist_lifts_turns"
        )
        if len(twist_values) != 2:
            raise ValueError("Stage C requires exactly two twists")
        criteria = self._json.mapping(design["criteria"], "criteria")
        cases: list[tuple[str, tuple[BondTerm, ...], str]] = []
        for case_value in self._json.array(design["planted_cases"], "planted_cases"):
            case = self._json.mapping(case_value, "planted case")
            terms: list[BondTerm] = []
            for term_value in self._json.array(case["terms"], "case terms"):
                term = self._json.mapping(term_value, "term")
                terms.append(
                    BondTerm(
                        (0, 0),
                        self._json.integer_pair(term["displacement"], "displacement"),
                        self._json.real(term["change"], "change"),
                    )
                )
            cases.append(
                (
                    self._json.text(case["case_id"], "case_id"),
                    tuple(terms),
                    self._json.text(
                        case["expected_first_accepted_model_class"],
                        "expected_first_accepted_model_class",
                    ),
                )
            )
        model_classes = tuple(
            self._json.text(value, "model class")
            for value in self._json.array(design["model_class_order"], "model classes")
        )
        operations = (
            D4Operation("identity", ((1, 0), (0, 1))),
            D4Operation("quarter_turn", ((0, -1), (1, 0))),
            D4Operation("half_turn", ((-1, 0), (0, -1))),
            D4Operation("three_quarter_turn", ((0, 1), (-1, 0))),
            D4Operation("reflection_x", ((1, 0), (0, -1))),
            D4Operation("reflection_y", ((-1, 0), (0, 1))),
            D4Operation("reflection_diagonal", ((0, 1), (1, 0))),
            D4Operation("reflection_antidiagonal", ((0, -1), (-1, 0))),
        )
        controls = StageCControls(
            shape[0],
            shape[1],
            (
                self._json.real_pair(twist_values[0], "Gamma twist"),
                self._json.real_pair(twist_values[1], "generic twist"),
            ),
            tuple(cases),
            model_classes,
            operations,
            self._json.real(
                criteria["hermiticity_maximum_absolute"], "Hermiticity tolerance"
            ),
            self._json.real(criteria["bridge_maximum_absolute"], "bridge tolerance"),
            self._json.real(
                criteria["symmetry_covariance_maximum_absolute"],
                "symmetry tolerance",
            ),
            self._json.real(criteria["fit_maximum_absolute"], "fit max tolerance"),
            self._json.real(criteria["fit_frobenius"], "fit Frobenius tolerance"),
            self._json.real(
                criteria["wrong_model_frobenius_floor"], "wrong-model floor"
            ),
            self._json.real(
                criteria["omitted_reverse_hermiticity_floor"],
                "omitted-reverse floor",
            ),
            self._json.real(
                criteria["omitted_bridge_maximum_floor"], "omitted-bridge floor"
            ),
        )
        if tuple(operation.identifier for operation in operations) != tuple(
            self._json.text(value, "symmetry operation")
            for value in self._json.array(
                self._json.mapping(design["symmetry_contract"], "symmetry_contract")[
                    "operations"
                ],
                "symmetry operations",
            )
        ):
            raise ValueError("D4 operation inventory differs from the frozen design")
        return controls, hashlib.sha256(encoded).hexdigest()


class StageCMatrixActions:
    """Construct local operators in the two frozen twist gauges."""

    __slots__ = ()

    @staticmethod
    def _index(controls: StageCControls, site: IntPair) -> int:
        return (site[0] % controls.nx) * controls.ny + (site[1] % controls.ny)

    def onsite(self, controls: StageCControls, site: IntPair) -> ComplexMatrix:
        result = np.zeros((controls.dimension,) * 2, dtype=np.complex128)
        index = self._index(controls, site)
        result[index, index] = 1.0
        return result

    def bond(
        self,
        controls: StageCControls,
        term: BondTerm,
        twist: FloatPair,
        route: str,
        include_reverse: bool = True,
    ) -> ComplexMatrix:
        result = np.zeros((controls.dimension,) * 2, dtype=np.complex128)
        row = self._index(controls, term.start)
        target_unwrapped = (
            term.start[0] + term.displacement[0],
            term.start[1] + term.displacement[1],
        )
        column = self._index(controls, target_unwrapped)
        if route == "A_centered_uniform":
            phase = np.exp(
                2.0j
                * np.pi
                * (
                    twist[0] * term.displacement[0] / controls.nx
                    + twist[1] * term.displacement[1] / controls.ny
                )
            )
        elif route == "B_reduced_seam":
            qx, _ = divmod(target_unwrapped[0], controls.nx)
            qy, _ = divmod(target_unwrapped[1], controls.ny)
            phase = np.exp(2.0j * np.pi * (qx * twist[0] + qy * twist[1]))
        else:
            raise ValueError(f"unsupported route {route}")
        result[row, column] += term.value * phase
        if include_reverse:
            result[column, row] += term.value * phase.conjugate()
        return result

    def defect(
        self,
        controls: StageCControls,
        terms: tuple[BondTerm, ...],
        twist: FloatPair,
        route: str,
    ) -> ComplexMatrix:
        result = np.zeros((controls.dimension,) * 2, dtype=np.complex128)
        for term in terms:
            result += self.bond(controls, term, twist, route)
        return result

    @staticmethod
    def site_gauge(controls: StageCControls, twist: FloatPair) -> ComplexMatrix:
        phases = [
            np.exp(
                2.0j * np.pi * (x * twist[0] / controls.nx + y * twist[1] / controls.ny)
            )
            for x in range(controls.nx)
            for y in range(controls.ny)
        ]
        return np.diag(np.asarray(phases, dtype=np.complex128))

    def permutation(
        self, controls: StageCControls, operation: D4Operation
    ) -> ComplexMatrix:
        result = np.zeros((controls.dimension,) * 2, dtype=np.complex128)
        for x in range(controls.nx):
            for y in range(controls.ny):
                tx = (
                    operation.matrix[0][0] * x + operation.matrix[0][1] * y
                ) % controls.nx
                ty = (
                    operation.matrix[1][0] * x + operation.matrix[1][1] * y
                ) % controls.ny
                result[
                    self._index(controls, (tx, ty)), self._index(controls, (x, y))
                ] = 1.0
        return result

    @staticmethod
    def transform_term(term: BondTerm, operation: D4Operation) -> BondTerm:
        matrix = operation.matrix
        return BondTerm(
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

    @staticmethod
    def maximum(matrix: ComplexMatrix) -> float:
        return float(np.max(np.abs(matrix), initial=0.0))

    @staticmethod
    def digest(matrix: ComplexMatrix) -> str:
        return hashlib.sha256(
            np.ascontiguousarray(matrix, dtype="<c16").tobytes()
        ).hexdigest()


class StageCModelFitter:
    """Fit the frozen real model classes and retain residual diagnostics."""

    __slots__ = ("_matrix",)

    def __init__(self, matrix: StageCMatrixActions) -> None:
        self._matrix = matrix

    def execute(
        self,
        controls: StageCControls,
        target: ComplexMatrix,
        twist: FloatPair,
        route: str,
        model_class: str,
    ) -> tuple[dict[str, JsonValue], ComplexMatrix]:
        basis = self._basis(controls, twist, route, model_class)
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
        accepted = (
            maximum <= controls.fit_maximum_tolerance
            and frobenius <= controls.fit_frobenius_tolerance
        )
        return (
            {
                "model_class": model_class,
                "coefficients": coefficient_record,
                "basis_rank": int(rank),
                "residual_maximum_absolute": maximum,
                "residual_frobenius": frobenius,
                "residual_shell_maximum": cast(
                    JsonValue, self._shell_maximum(controls, residual)
                ),
                "accepted": accepted,
            },
            residual,
        )

    def _basis(
        self,
        controls: StageCControls,
        twist: FloatPair,
        route: str,
        model_class: str,
    ) -> tuple[tuple[str, ComplexMatrix], ...]:
        onsite = ("origin_onsite", self._matrix.onsite(controls, (0, 0)))
        x_onsite = ("positive_x_neighbor_onsite", self._matrix.onsite(controls, (1, 0)))
        y_onsite = ("positive_y_neighbor_onsite", self._matrix.onsite(controls, (0, 1)))
        x_bond_value = self._matrix.bond(
            controls, BondTerm((0, 0), (1, 0), 1.0), twist, route
        )
        y_bond_value = self._matrix.bond(
            controls, BondTerm((0, 0), (0, 1), 1.0), twist, route
        )
        diagonal_value = self._matrix.bond(
            controls, BondTerm((0, 0), (1, 1), 1.0), twist, route
        )
        if model_class == "point_scalar_onsite":
            return (onsite,)
        if model_class == "finite_support_diagonal_onsite":
            return onsite, x_onsite, y_onsite
        if model_class == "onsite_plus_isotropic_nearest_neighbor":
            return onsite, ("isotropic_nearest_neighbor", x_bond_value + y_bond_value)
        if model_class == "onsite_plus_directional_nearest_neighbor":
            return (
                onsite,
                ("positive_x_bond", x_bond_value),
                (
                    "positive_y_bond",
                    y_bond_value,
                ),
            )
        if model_class == "finite_range_nonlocal_radius_two":
            return (
                onsite,
                ("positive_x_bond", x_bond_value),
                ("positive_y_bond", y_bond_value),
                ("positive_diagonal_bond", diagonal_value),
            )
        raise ValueError(f"unsupported model class {model_class}")

    @staticmethod
    def _shell_maximum(
        controls: StageCControls, matrix: ComplexMatrix
    ) -> dict[str, float]:
        result = {"0": 0.0, "1": 0.0, "2": 0.0, "exterior": 0.0}
        for row in range(controls.dimension):
            rx, ry = divmod(row, controls.ny)
            for column in range(controls.dimension):
                value = abs(matrix[row, column])
                if value == 0.0:
                    continue
                cx, cy = divmod(column, controls.ny)
                distances = (
                    min(rx, controls.nx - rx),
                    min(ry, controls.ny - ry),
                    min(cx, controls.nx - cx),
                    min(cy, controls.ny - cy),
                )
                shell = max(distances)
                key = str(shell) if shell <= 2 else "exterior"
                result[key] = max(result[key], float(value))
        return result


class StageCScheduleExecutor:
    """Execute one route order inside its own spawned process."""

    __slots__ = ()

    def execute(
        self,
        controls: StageCControls,
        schedule_id: str,
        route_order: tuple[str, str],
    ) -> StageCScheduleResult:
        matrix_actions = StageCMatrixActions()
        fitter = StageCModelFitter(matrix_actions)
        matrices: list[tuple[MatrixRecordKey, bytes]] = []
        route_records: list[JsonValue] = []
        for route in route_order:
            for case_id, terms, expected in controls.cases:
                for twist_id, twist in zip(
                    ("gamma", "generic"), controls.twists, strict=True
                ):
                    target = matrix_actions.defect(controls, terms, twist, route)
                    key = (route, case_id, twist_id)
                    matrices.append(
                        (
                            key,
                            np.ascontiguousarray(target, dtype="<c16").tobytes(),
                        )
                    )
                    hermiticity = matrix_actions.maximum(target - target.conj().T)
                    fits: list[JsonValue] = []
                    selected: str | None = None
                    exterior = 0.0
                    for model_class in controls.model_classes:
                        fit, _ = fitter.execute(
                            controls, target, twist, route, model_class
                        )
                        fits.append(cast(JsonValue, fit))
                        shell = cast(
                            dict[str, JsonValue], fit["residual_shell_maximum"]
                        )
                        exterior = max(exterior, cast(float, shell["exterior"]))
                        if selected is None and fit["accepted"] is True:
                            selected = model_class
                    route_records.append(
                        {
                            "route": route,
                            "case_id": case_id,
                            "twist_id": twist_id,
                            "matrix_sha256": matrix_actions.digest(target),
                            "hermiticity_maximum_absolute": hermiticity,
                            "selected_model_class": selected,
                            "expected_model_class": expected,
                            "maximum_exterior_residual": exterior,
                            "fits": fits,
                        }
                    )
        return StageCScheduleResult(
            schedule_id,
            route_order,
            os.getpid(),
            json.dumps(route_records, sort_keys=True, separators=(",", ":")),
            tuple(matrices),
        )


class StageCToyStudy:
    """Execute the bounded authored-toy Stage C software contract."""

    __slots__ = ("_matrix", "_fitter")

    def __init__(self) -> None:
        self._matrix = StageCMatrixActions()
        self._fitter = StageCModelFitter(self._matrix)

    def execute(
        self, controls: StageCControls, design_sha256: str
    ) -> dict[str, JsonValue]:
        schedules = (
            ("A_then_B", ("A_centered_uniform", "B_reduced_seam")),
            ("B_then_A", ("B_reduced_seam", "A_centered_uniform")),
        )
        context = multiprocessing.get_context("spawn")
        executor_action = StageCScheduleExecutor()
        with (
            concurrent.futures.ProcessPoolExecutor(
                max_workers=1, mp_context=context
            ) as first_executor,
            concurrent.futures.ProcessPoolExecutor(
                max_workers=1, mp_context=context
            ) as second_executor,
        ):
            futures = (
                first_executor.submit(executor_action.execute, controls, *schedules[0]),
                second_executor.submit(
                    executor_action.execute, controls, *schedules[1]
                ),
            )
            schedule_results = [future.result() for future in futures]
        process_ids = {result.process_id for result in schedule_results}
        if len(process_ids) != 2 or os.getpid() in process_ids:
            raise RuntimeError(
                "Stage C schedules did not run in distinct spawned processes"
            )
        schedule_matrices: dict[str, dict[MatrixRecordKey, ComplexMatrix]] = {}
        schedule_records: list[JsonValue] = []
        all_hermiticity: list[float] = []
        selections_agree = True
        maximum_exterior = 0.0
        for schedule_result in schedule_results:
            decoded = cast(JsonValue, json.loads(schedule_result.route_records_json))
            if not isinstance(decoded, list):
                raise TypeError("spawned schedule result must be a JSON array")
            matrices = {
                key: np.frombuffer(value, dtype="<c16").reshape(
                    (controls.dimension, controls.dimension)
                )
                for key, value in schedule_result.matrix_bytes
            }
            schedule_matrices[schedule_result.schedule_id] = matrices
            for record_value in decoded:
                if not isinstance(record_value, dict):
                    raise TypeError("route record must be a JSON object")
                all_hermiticity.append(
                    cast(float, record_value["hermiticity_maximum_absolute"])
                )
                maximum_exterior = max(
                    maximum_exterior,
                    cast(float, record_value["maximum_exterior_residual"]),
                )
                selections_agree = selections_agree and (
                    record_value["selected_model_class"]
                    == record_value["expected_model_class"]
                )
            schedule_records.append(
                {
                    "schedule_id": schedule_result.schedule_id,
                    "route_order": cast(JsonValue, list(schedule_result.route_order)),
                    "fresh_spawned_process": True,
                    "route_records": decoded,
                }
            )
        schedule_difference = 0.0
        first = schedule_matrices["A_then_B"]
        second = schedule_matrices["B_then_A"]
        for key, matrix in first.items():
            schedule_difference = max(
                schedule_difference, self._matrix.maximum(matrix - second[key])
            )
        bridges: list[JsonValue] = []
        bridge_maximum = 0.0
        for schedule_id, matrices in schedule_matrices.items():
            for case_id, _, _ in controls.cases:
                for twist_id, twist in zip(
                    ("gamma", "generic"), controls.twists, strict=True
                ):
                    route_a = matrices[("A_centered_uniform", case_id, twist_id)]
                    route_b = matrices[("B_reduced_seam", case_id, twist_id)]
                    gauge = self._matrix.site_gauge(controls, twist)
                    residual = route_b - gauge @ route_a @ gauge.conj().T
                    maximum = self._matrix.maximum(residual)
                    bridge_maximum = max(bridge_maximum, maximum)
                    bridges.append(
                        {
                            "schedule_id": schedule_id,
                            "case_id": case_id,
                            "twist_id": twist_id,
                            "maximum_absolute": maximum,
                            "frobenius": float(np.linalg.norm(residual, ord="fro")),
                        }
                    )
        symmetry_records, symmetry_maximum = self._symmetry(controls)
        adverse = self._adverse(controls)
        criteria = [
            {
                "criterion": "hermiticity",
                "value": max(all_hermiticity),
                "comparison": "<=",
                "threshold": controls.hermiticity_tolerance,
                "passed": max(all_hermiticity) <= controls.hermiticity_tolerance,
            },
            {
                "criterion": "gauge_bridge",
                "value": bridge_maximum,
                "comparison": "<=",
                "threshold": controls.bridge_tolerance,
                "passed": bridge_maximum <= controls.bridge_tolerance,
            },
            {
                "criterion": "D4_oriented_covariance",
                "value": symmetry_maximum,
                "comparison": "<=",
                "threshold": controls.symmetry_tolerance,
                "passed": symmetry_maximum <= controls.symmetry_tolerance,
            },
            {
                "criterion": "schedule_invariance",
                "value": schedule_difference,
                "comparison": "==",
                "threshold": 0.0,
                "passed": schedule_difference == 0.0,
            },
            {
                "criterion": "first_model_class_selection",
                "value": 1.0 if selections_agree else 0.0,
                "comparison": "==",
                "threshold": 1.0,
                "passed": selections_agree,
            },
            {
                "criterion": "radius_two_exterior",
                "value": maximum_exterior,
                "comparison": "==",
                "threshold": 0.0,
                "passed": maximum_exterior == 0.0,
            },
            {
                "criterion": "directional_as_isotropic_discriminates",
                "value": cast(float, adverse[0]["value"]),
                "comparison": ">=",
                "threshold": controls.wrong_model_floor,
                "passed": cast(float, adverse[0]["value"])
                >= controls.wrong_model_floor,
            },
            {
                "criterion": "nonlocal_as_directional_discriminates",
                "value": cast(float, adverse[1]["value"]),
                "comparison": ">=",
                "threshold": controls.wrong_model_floor,
                "passed": cast(float, adverse[1]["value"])
                >= controls.wrong_model_floor,
            },
            {
                "criterion": "omitted_reverse_discriminates",
                "value": cast(float, adverse[2]["value"]),
                "comparison": ">=",
                "threshold": controls.omitted_reverse_floor,
                "passed": cast(float, adverse[2]["value"])
                >= controls.omitted_reverse_floor,
            },
            {
                "criterion": "omitted_bridge_discriminates",
                "value": cast(float, adverse[3]["value"]),
                "comparison": ">=",
                "threshold": controls.omitted_bridge_floor,
                "passed": cast(float, adverse[3]["value"])
                >= controls.omitted_bridge_floor,
            },
        ]
        return {
            "schema_version": 1,
            "result_id": (
                "research-monograph.impurity-defect-2d.stage-c.authored-toy.v1"
            ),
            "evidence_status": (
                "synthetic execution-free software-verification behavior"
            ),
            "accepted_parent_read": False,
            "design_sha256": design_sha256,
            "space": {
                "shape": [controls.nx, controls.ny],
                "dimension": controls.dimension,
                "ordering": "site-x outer, site-y inner",
                "units": "E_G=1, G=1, a=2*pi",
            },
            "schedules": schedule_records,
            "bridges": bridges,
            "symmetry_records": symmetry_records,
            "adverse_controls": cast(JsonValue, adverse),
            "criteria": cast(JsonValue, criteria),
            "summary": {
                "route_record_count": 16,
                "bridge_record_count": 8,
                "symmetry_record_count": 16,
                "fit_record_count": 80,
                "maximum_hermiticity": max(all_hermiticity),
                "maximum_bridge": bridge_maximum,
                "maximum_symmetry_covariance": symmetry_maximum,
                "maximum_schedule_difference": schedule_difference,
                "maximum_exterior_residual": maximum_exterior,
                "all_criteria_passed": all(
                    record["passed"] is True for record in criteria
                ),
            },
        }

    def _symmetry(self, controls: StageCControls) -> tuple[list[JsonValue], float]:
        records: list[JsonValue] = []
        maximum = 0.0
        for case_id, terms, _ in controls.cases:
            source = self._matrix.defect(
                controls, terms, controls.twists[0], "A_centered_uniform"
            )
            for operation in controls.operations:
                permutation = self._matrix.permutation(controls, operation)
                transformed_terms = tuple(
                    self._matrix.transform_term(term, operation) for term in terms
                )
                reconstructed = self._matrix.defect(
                    controls,
                    transformed_terms,
                    controls.twists[0],
                    "A_centered_uniform",
                )
                residual = reconstructed - permutation @ source @ permutation.conj().T
                value = self._matrix.maximum(residual)
                maximum = max(maximum, value)
                records.append(
                    {
                        "case_id": case_id,
                        "operation": operation.identifier,
                        "maximum_absolute": value,
                        "frobenius": float(np.linalg.norm(residual, ord="fro")),
                    }
                )
        return records, maximum

    def _adverse(self, controls: StageCControls) -> list[dict[str, JsonValue]]:
        directional = controls.cases[0][1]
        nonlocal_terms = controls.cases[1][1]
        gamma = controls.twists[0]
        generic = controls.twists[1]
        directional_matrix = self._matrix.defect(
            controls, directional, gamma, "A_centered_uniform"
        )
        isotropic, _ = self._fitter.execute(
            controls,
            directional_matrix,
            gamma,
            "A_centered_uniform",
            "onsite_plus_isotropic_nearest_neighbor",
        )
        nonlocal_matrix = self._matrix.defect(
            controls, nonlocal_terms, gamma, "A_centered_uniform"
        )
        directional_fit, _ = self._fitter.execute(
            controls,
            nonlocal_matrix,
            gamma,
            "A_centered_uniform",
            "onsite_plus_directional_nearest_neighbor",
        )
        omitted = self._matrix.bond(
            controls, directional[0], gamma, "A_centered_uniform", include_reverse=False
        )
        omitted_hermiticity = self._matrix.maximum(omitted - omitted.conj().T)
        route_a = self._matrix.defect(
            controls, directional, generic, "A_centered_uniform"
        )
        route_b = self._matrix.defect(controls, directional, generic, "B_reduced_seam")
        raw_route_difference = self._matrix.maximum(route_b - route_a)
        return [
            {
                "control_id": "directional_as_isotropic",
                "quantity": "residual_frobenius",
                "value": isotropic["residual_frobenius"],
            },
            {
                "control_id": "nonlocal_as_directional",
                "quantity": "residual_frobenius",
                "value": directional_fit["residual_frobenius"],
            },
            {
                "control_id": "omit_hermitian_reverse",
                "quantity": "hermiticity_maximum_absolute",
                "value": omitted_hermiticity,
            },
            {
                "control_id": "omit_gauge_bridge",
                "quantity": "raw_route_maximum_absolute",
                "value": raw_route_difference,
            },
        ]


class StageCResultSerializer:
    """Serialize the authored-toy result as deterministic compact JSON."""

    __slots__ = ()

    @staticmethod
    def execute(result: dict[str, JsonValue], output: Path) -> None:
        if output.exists():
            raise FileExistsError(f"refusing to overwrite {output}")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


class StageCToyWorkflow:
    """Compose exact design loading, authored-toy execution, and serialization."""

    __slots__ = ()

    def execute(self, design: Path, output: Path) -> dict[str, JsonValue]:
        controls, design_sha256 = StageCDesignDeserializer().execute(design)
        result = StageCToyStudy().execute(controls, design_sha256)
        StageCResultSerializer().execute(result, output)
        return result


def main() -> None:
    """Adapt command-line arguments into the Stage C authored-toy Workflow."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--design", type=Path, required=True)
    parser.add_argument("--toy-output", type=Path, required=True)
    arguments = parser.parse_args()
    result = StageCToyWorkflow().execute(arguments.design, arguments.toy_output)
    summary = cast(dict[str, JsonValue], result["summary"])
    print(
        f"stage_c_toy_criteria={'PASS' if summary['all_criteria_passed'] else 'FAIL'}"
    )
    print(f"route_records={summary['route_record_count']}")
    print(f"fit_records={summary['fit_record_count']}")


if __name__ == "__main__":
    main()
