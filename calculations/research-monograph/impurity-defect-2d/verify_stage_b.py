#!/usr/bin/env python3
"""Independently verify a retained multi-route Stage B result."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type ComplexMatrix = npt.NDArray[np.complex128]
type IntMatrix2 = tuple[tuple[int, int], tuple[int, int]]
type FloatPair = tuple[float, float]


@dataclass(frozen=True, slots=True)
class VerificationHopping:
    """One serialized hopping decoded for independent reconstruction."""

    rx: int
    ry: int
    value: complex


@dataclass(frozen=True, slots=True)
class VerificationOperation:
    """One independently frozen D4 action."""

    identifier: str
    matrix: IntMatrix2


@dataclass(frozen=True, slots=True)
class VerificationControls:
    """Exact controls reconstructed from the retained result contract."""

    nx: int
    ny: int
    twists: tuple[FloatPair, FloatPair]
    algebraic: float
    covariance: float
    route: float
    tie: float
    twist: float
    adverse: float


@dataclass(frozen=True, slots=True)
class VerificationResult:
    """Independent reconstruction disposition and maximum discrepancy."""

    reconstruction_status: str
    criteria_status: str
    maximum_metric_difference: float
    failures: tuple[str, ...]


class VerificationJson:
    """Decode the retained closed JSON representation."""

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
    def string(value: JsonValue, name: str) -> str:
        if not isinstance(value, str):
            raise TypeError(f"{name} must be a string")
        return value

    @staticmethod
    def integer(value: JsonValue, name: str) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an integer")
        return value

    @staticmethod
    def real(value: JsonValue, name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be numeric")
        result = float(value)
        if not np.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result

    def real_pair(self, value: JsonValue, name: str) -> FloatPair:
        items = self.array(value, name)
        if len(items) != 2:
            raise ValueError(f"{name} must contain two entries")
        return self.real(items[0], name), self.real(items[1], name)


class IndependentStageBReconstruction:
    """Reconstruct route matrices with shift factors, never importing the runner."""

    __slots__ = ("_json",)

    _OPERATIONS: tuple[VerificationOperation, ...] = (
        VerificationOperation("identity", ((1, 0), (0, 1))),
        VerificationOperation("quarter_turn", ((0, -1), (1, 0))),
        VerificationOperation("half_turn", ((-1, 0), (0, -1))),
        VerificationOperation("three_quarter_turn", ((0, 1), (-1, 0))),
        VerificationOperation("reflection_x", ((1, 0), (0, -1))),
        VerificationOperation("reflection_y", ((-1, 0), (0, 1))),
        VerificationOperation("reflection_diagonal", ((0, 1), (1, 0))),
        VerificationOperation("reflection_antidiagonal", ((0, -1), (-1, 0))),
    )

    def __init__(self) -> None:
        self._json = VerificationJson()

    def execute(self, payload: dict[str, JsonValue]) -> VerificationResult:
        if payload.get("stage_id") != "B_scalar_onsite_and_D4_multiroute":
            raise ValueError("result is not multi-route Stage B")
        controls = self._controls(payload)
        hoppings = self._hoppings(payload)
        schedules = self._json.array(payload["schedules"], "schedules")
        failures: list[str] = []
        maximum = 0.0
        parent_failures, parent_maximum = self._verify_parent(
            controls, hoppings, payload
        )
        failures.extend(parent_failures)
        maximum = max(maximum, parent_maximum)
        if len(schedules) != 2:
            failures.append("schedule inventory")
        for expected_schedule, schedule_value in zip(
            ("A_then_B", "B_then_A"), schedules, strict=True
        ):
            schedule = self._json.mapping(schedule_value, "schedule")
            if schedule.get("schedule_id") != expected_schedule:
                failures.append(f"{expected_schedule}: identity")
            route_values = self._json.mapping(schedule["routes"], "routes")
            reconstructed: dict[
                str, dict[str, tuple[ComplexMatrix, ComplexMatrix, ComplexMatrix]]
            ] = {}
            for route_id in ("A_centered_uniform", "B_reduced_seam"):
                route = self._json.mapping(route_values[route_id], route_id)
                route_failures, route_maximum, matrices = self._verify_route(
                    controls, hoppings, route_id, route
                )
                failures.extend(
                    f"{expected_schedule}.{route_id}.{failure}"
                    for failure in route_failures
                )
                maximum = max(maximum, route_maximum)
                reconstructed[route_id] = matrices
            bridge_failures, bridge_maximum = self._verify_bridges(
                controls,
                schedule,
                reconstructed["A_centered_uniform"],
                reconstructed["B_reduced_seam"],
            )
            failures.extend(
                f"{expected_schedule}.bridge.{failure}" for failure in bridge_failures
            )
            maximum = max(maximum, bridge_maximum)
        order_failures = self._verify_order(payload)
        failures.extend(order_failures)
        criterion = self._json.mapping(
            payload["criterion_evaluation"], "criterion_evaluation"
        )
        expected_criteria = "pass" if not failures else "fail"
        retained_criteria = self._json.string(criterion["status"], "criteria status")
        criteria_status = "PASS" if retained_criteria == expected_criteria else "FAIL"
        if criteria_status == "FAIL":
            failures.append("criterion disposition differs from reconstruction")
        return VerificationResult(
            reconstruction_status="PASS" if not failures else "FAIL",
            criteria_status=criteria_status,
            maximum_metric_difference=maximum,
            failures=tuple(failures),
        )

    def _controls(self, payload: dict[str, JsonValue]) -> VerificationControls:
        record = self._json.mapping(payload["controls"], "controls")
        shape = self._json.array(record["shape"], "shape")
        twists = self._json.array(record["twists"], "twists")
        if len(shape) != 2 or len(twists) != 2:
            raise ValueError("invalid retained shape or twist inventory")
        return VerificationControls(
            nx=self._json.integer(shape[0], "nx"),
            ny=self._json.integer(shape[1], "ny"),
            twists=(
                self._json.real_pair(twists[0], "Gamma twist"),
                self._json.real_pair(twists[1], "generic twist"),
            ),
            algebraic=self._json.real(record["algebraic_tolerance"], "algebraic"),
            covariance=self._json.real(record["covariance_tolerance"], "covariance"),
            route=self._json.real(record["route_tolerance"], "route"),
            tie=self._json.real(record["tie_tolerance"], "tie"),
            twist=self._json.real(record["twist_tolerance"], "twist"),
            adverse=self._json.real(record["adverse_floor"], "adverse"),
        )

    def _hoppings(
        self, payload: dict[str, JsonValue]
    ) -> tuple[VerificationHopping, ...]:
        result: list[VerificationHopping] = []
        for value in self._json.array(payload["input_hoppings"], "input_hoppings"):
            record = self._json.mapping(value, "hopping")
            result.append(
                VerificationHopping(
                    self._json.integer(record["rx"], "rx"),
                    self._json.integer(record["ry"], "ry"),
                    complex(
                        self._json.real(record["real"], "real"),
                        self._json.real(record["imag"], "imag"),
                    ),
                )
            )
        if not result:
            raise ValueError("retained hopping inventory is empty")
        return tuple(result)

    def _verify_parent(
        self,
        controls: VerificationControls,
        hoppings: tuple[VerificationHopping, ...],
        payload: dict[str, JsonValue],
    ) -> tuple[list[str], float]:
        failures: list[str] = []
        maximum_hermiticity = 0.0
        maximum_d4 = 0.0
        by_displacement = {
            (hopping.rx, hopping.ry): hopping.value for hopping in hoppings
        }
        if len(by_displacement) != len(hoppings):
            failures.append("parent duplicate displacement")
        for displacement, value in by_displacement.items():
            reverse = (-displacement[0], -displacement[1])
            if reverse not in by_displacement:
                failures.append(f"parent missing reverse {displacement}")
                continue
            maximum_hermiticity = max(
                maximum_hermiticity,
                abs(by_displacement[reverse] - value.conjugate()),
            )
            for operation in self._OPERATIONS:
                transformed = (
                    operation.matrix[0][0] * displacement[0]
                    + operation.matrix[0][1] * displacement[1],
                    operation.matrix[1][0] * displacement[0]
                    + operation.matrix[1][1] * displacement[1],
                )
                if transformed not in by_displacement:
                    failures.append(f"parent missing D4 image {transformed}")
                    continue
                maximum_d4 = max(maximum_d4, abs(by_displacement[transformed] - value))
        retained = self._json.mapping(payload["parent_checks"], "parent_checks")
        differences = (
            abs(
                self._json.real(
                    retained["maximum_hermiticity_defect"],
                    "maximum_hermiticity_defect",
                )
                - maximum_hermiticity
            ),
            abs(
                self._json.real(retained["maximum_D4_defect"], "maximum_D4_defect")
                - maximum_d4
            ),
        )
        if retained.get("unique_displacements") != len(by_displacement):
            failures.append("parent unique displacement count")
        if max(differences) > 1.0e-10:
            failures.append("parent retained metrics")
        if maximum_hermiticity > controls.algebraic:
            failures.append("parent Hermiticity")
        if maximum_d4 > controls.algebraic:
            failures.append("parent D4 covariance")
        return failures, max(differences)

    def _verify_route(
        self,
        controls: VerificationControls,
        hoppings: tuple[VerificationHopping, ...],
        route_id: str,
        retained: dict[str, JsonValue],
    ) -> tuple[
        list[str],
        float,
        dict[str, tuple[ComplexMatrix, ComplexMatrix, ComplexMatrix]],
    ]:
        failures: list[str] = []
        maximum = 0.0
        matrices: dict[str, tuple[ComplexMatrix, ComplexMatrix, ComplexMatrix]] = {}
        cases = self._json.array(retained["known_map_cases"], "known_map_cases")
        if len(cases) != 18:
            failures.append("known inventory")
        for index, value in enumerate(cases):
            record = self._json.mapping(value, "known case")
            case_id = self._json.string(record["case_id"], "case_id")
            operation = self._operation(case_id)
            twist = controls.twists[1] if "generic" in case_id else controls.twists[0]
            lift = self._transform_twist(twist, operation.matrix)
            pristine = self._route_matrix(controls, hoppings, route_id, lift)
            site = self._site(
                controls,
                operation.matrix,
                (0, 0) if case_id.startswith("central") else (1, 2),
            )
            plant = self._plant(controls, site, -0.25)
            hdef = pristine + plant
            attack = self._attack(controls)
            identity = np.eye(controls.nx * controls.ny, dtype=np.complex128)
            candidate = attack @ hdef @ attack.conj().T + 0.137 * identity
            recovered = (
                attack.conj().T @ (candidate - 0.137 * identity) @ attack - pristine
            )
            difference = recovered - plant
            expected_metrics = {
                "hermiticity_maximum_absolute": self._maximum(
                    recovered - recovered.conj().T
                ),
                "recovery_maximum_absolute": self._maximum(difference),
                "recovery_frobenius": float(np.linalg.norm(difference, ord="fro")),
                "amplitude_absolute_defect": float(
                    abs(
                        recovered[
                            site[0] * controls.ny + site[1],
                            site[0] * controls.ny + site[1],
                        ]
                        + 0.25
                    )
                ),
            }
            for name, expected_metric in expected_metrics.items():
                retained_value = self._json.real(record[name], name)
                delta = abs(retained_value - expected_metric)
                maximum = max(maximum, delta)
                if delta > 1.0e-10:
                    failures.append(f"known[{index}].{name}")
            for name in (
                "pristine_sha256",
                "planted_sha256",
                "candidate_sha256",
                "recovered_sha256",
            ):
                value = record.get(name)
                if not isinstance(value, str) or len(value) != 64:
                    failures.append(f"known[{index}].{name}.format")
            matrices[case_id] = (pristine, plant, candidate)
        blind_failures, blind_maximum = self._verify_blind(
            controls, hoppings, route_id, retained
        )
        failures.extend(blind_failures)
        maximum = max(maximum, blind_maximum)
        return failures, maximum, matrices

    def _verify_blind(
        self,
        controls: VerificationControls,
        hoppings: tuple[VerificationHopping, ...],
        route_id: str,
        retained: dict[str, JsonValue],
    ) -> tuple[list[str], float]:
        failures: list[str] = []
        maximum = 0.0
        cases = self._json.array(retained["blind_cases"], "blind_cases")
        if len(cases) != 2:
            return ["blind inventory"], maximum
        attack = self._attack(controls)
        identity = np.eye(controls.nx * controls.ny, dtype=np.complex128)
        for index, (twist, value) in enumerate(
            zip(controls.twists, cases, strict=True)
        ):
            record = self._json.mapping(value, "blind case")
            pristine = self._route_matrix(controls, hoppings, route_id, twist)
            plant = self._plant(controls, (1, 2), -0.25)
            candidate = attack @ (pristine + plant) @ attack.conj().T + 0.137 * identity
            candidate_lift = self._transform_twist(twist, self._OPERATIONS[-1].matrix)
            reference_metadata = (
                twist if route_id.startswith("A_") else self._reduced(twist)
            )
            candidate_metadata = (
                candidate_lift
                if route_id.startswith("A_")
                else self._reduced(candidate_lift)
            )
            reconstructed = self._blind_candidates(
                controls,
                route_id,
                pristine,
                candidate,
                reference_metadata,
                candidate_metadata,
            )
            retained_candidates = self._json.array(record["candidates"], "candidates")
            if len(retained_candidates) != len(reconstructed):
                failures.append(f"blind[{index}].candidate inventory")
                continue
            for candidate_index, (left_value, right) in enumerate(
                zip(retained_candidates, reconstructed, strict=True)
            ):
                left = self._json.mapping(left_value, "candidate")
                if (
                    left.get("operation") != right["operation"]
                    or left.get("translation") != right["translation"]
                ):
                    failures.append(f"blind[{index}].candidate[{candidate_index}].map")
                for name in (
                    "transformed_twist_lift",
                    "comparison_twist",
                    "integer_lift",
                ):
                    if left.get(name) != right[name]:
                        failures.append(
                            f"blind[{index}].candidate[{candidate_index}].{name}"
                        )
                for name in ("objective", "energy_shift_diagnostic"):
                    delta = abs(
                        self._json.real(left[name], name) - cast(float, right[name])
                    )
                    maximum = max(maximum, delta)
                    if delta > 1.0e-10:
                        failures.append(
                            f"blind[{index}].candidate[{candidate_index}].{name}"
                        )
            minimum = min(cast(float, item["objective"]) for item in reconstructed)
            ambiguity = [
                item
                for item in reconstructed
                if cast(float, item["objective"]) <= minimum + controls.tie
            ]
            if record.get("ambiguity_count") != len(ambiguity):
                failures.append(f"blind[{index}].ambiguity count")
            retained_ambiguity = self._json.array(
                record["ambiguity_set"], "ambiguity_set"
            )
            expected_maps = [
                (item["operation"], item["translation"]) for item in ambiguity
            ]
            retained_maps = [
                (
                    self._json.mapping(item, "ambiguity item")["operation"],
                    self._json.mapping(item, "ambiguity item")["translation"],
                )
                for item in retained_ambiguity
            ]
            if retained_maps != expected_maps:
                failures.append(f"blind[{index}].ambiguity identities")
            if record.get("issue_code") != "DEFECT_2D.SITE_MAP_UNRESOLVED":
                failures.append(f"blind[{index}].issue code")
            if (
                record.get("selected_map") is not None
                or record.get("extracted_operator") is not None
            ):
                failures.append(f"blind[{index}].stop payload")
        return failures, maximum

    def _verify_bridges(
        self,
        controls: VerificationControls,
        schedule: dict[str, JsonValue],
        route_a: dict[str, tuple[ComplexMatrix, ComplexMatrix, ComplexMatrix]],
        route_b: dict[str, tuple[ComplexMatrix, ComplexMatrix, ComplexMatrix]],
    ) -> tuple[list[str], float]:
        failures: list[str] = []
        maximum = 0.0
        records = self._json.array(schedule["bridges"], "bridges")
        if len(records) != 18:
            return ["inventory"], maximum
        attack = self._attack(controls)
        identity = np.eye(controls.nx * controls.ny, dtype=np.complex128)
        for index, value in enumerate(records):
            record = self._json.mapping(value, "bridge")
            case_id = self._json.string(record["case_id"], "case_id")
            operation = self._operation(case_id)
            twist = controls.twists[1] if "generic" in case_id else controls.twists[0]
            lift = self._transform_twist(twist, operation.matrix)
            gauge = self._gauge(controls, lift)
            attacked_gauge = attack @ gauge @ attack.conj().T
            a_pristine, a_plant, a_candidate = route_a[case_id]
            b_pristine, b_plant, b_candidate = route_b[case_id]
            a_hdef = a_pristine + a_plant
            b_hdef = b_pristine + b_plant
            canonical = b_hdef - gauge @ a_hdef @ gauge.conj().T
            attacked = (b_candidate - 0.137 * identity) - (
                attacked_gauge
                @ (a_candidate - 0.137 * identity)
                @ attacked_gauge.conj().T
            )
            expected = {
                "canonical_maximum_absolute": self._maximum(canonical),
                "attacked_maximum_absolute": self._maximum(attacked),
                "plant_maximum_absolute": self._maximum(b_plant - a_plant),
                "pristine_eigenvalue_maximum_absolute": float(
                    np.max(
                        np.abs(
                            np.sort(np.linalg.eigvalsh(b_pristine))
                            - np.sort(np.linalg.eigvalsh(a_pristine))
                        )
                    )
                ),
            }
            for name, expected_value in expected.items():
                delta = abs(self._json.real(record[name], name) - expected_value)
                maximum = max(maximum, delta)
                if delta > controls.route:
                    failures.append(f"[{index}].{name}")
        return failures, maximum

    def _verify_order(self, payload: dict[str, JsonValue]) -> list[str]:
        failures: list[str] = []
        comparison = self._json.mapping(payload["order_comparison"], "order comparison")
        expected_lengths = {
            "known_case_comparisons": 36,
            "bridge_comparisons": 18,
            "blind_comparisons": 6,
        }
        for name, expected in expected_lengths.items():
            values = self._json.array(comparison[name], name)
            if len(values) != expected:
                failures.append(f"order.{name}.inventory")
        for index, value in enumerate(
            self._json.array(comparison["known_case_comparisons"], "known comparisons")
        ):
            record = self._json.mapping(value, "known comparison")
            if record.get("same_recovered_sha256") is not True:
                failures.append(f"order.known[{index}]")
        for index, value in enumerate(
            self._json.array(comparison["blind_comparisons"], "blind comparisons")
        ):
            record = self._json.mapping(value, "blind comparison")
            if (
                record.get("same_ambiguity_set") is not True
                or record.get("same_disposition") is not True
            ):
                failures.append(f"order.blind[{index}]")
        return failures

    def _route_matrix(
        self,
        controls: VerificationControls,
        hoppings: tuple[VerificationHopping, ...],
        route_id: str,
        twist_lift: FloatPair,
    ) -> ComplexMatrix:
        if route_id.startswith("A_"):
            return self._fourier_uniform(controls, hoppings, twist_lift)
        result = np.zeros((controls.nx * controls.ny,) * 2, dtype=np.complex128)
        reduced = self._reduced(twist_lift)
        for hopping in hoppings:
            shift_x = self._seam_shift(controls.nx, hopping.rx, reduced[0])
            shift_y = self._seam_shift(controls.ny, hopping.ry, reduced[1])
            result += hopping.value * np.kron(shift_x, shift_y)
        return result

    @staticmethod
    def _fourier_uniform(
        controls: VerificationControls,
        hoppings: tuple[VerificationHopping, ...],
        twist_lift: FloatPair,
    ) -> ComplexMatrix:
        x = np.arange(controls.nx, dtype=np.float64)
        y = np.arange(controls.ny, dtype=np.float64)
        fourier_x = np.exp(2.0j * np.pi * np.outer(x, x) / controls.nx) / np.sqrt(
            controls.nx
        )
        fourier_y = np.exp(2.0j * np.pi * np.outer(y, y) / controls.ny) / np.sqrt(
            controls.ny
        )
        fourier = np.kron(fourier_x, fourier_y)
        dispersion = np.zeros((controls.nx, controls.ny), dtype=np.complex128)
        for kx in range(controls.nx):
            for ky in range(controls.ny):
                for hopping in hoppings:
                    dispersion[kx, ky] += hopping.value * np.exp(
                        2.0j
                        * np.pi
                        * (
                            (kx + twist_lift[0]) * hopping.rx / controls.nx
                            + (ky + twist_lift[1]) * hopping.ry / controls.ny
                        )
                    )
        return fourier @ np.diag(dispersion.reshape(-1)) @ fourier.conj().T

    @staticmethod
    def _seam_shift(size: int, displacement: int, twist: float) -> ComplexMatrix:
        result = np.zeros((size, size), dtype=np.complex128)
        for source in range(size):
            quotient, target = divmod(source + displacement, size)
            result[source, target] = np.exp(2.0j * np.pi * quotient * twist)
        return result

    def _blind_candidates(
        self,
        controls: VerificationControls,
        route_id: str,
        reference: ComplexMatrix,
        candidate: ComplexMatrix,
        reference_twist: FloatPair,
        candidate_twist: FloatPair,
    ) -> list[dict[str, JsonValue]]:
        result: list[dict[str, JsonValue]] = []
        for operation in self._OPERATIONS:
            transformed = self._transform_twist(reference_twist, operation.matrix)
            compatible = (
                all(
                    abs(a - b) <= controls.twist
                    for a, b in zip(transformed, candidate_twist, strict=True)
                )
                if route_id.startswith("A_")
                else all(
                    min(abs(a - b + n) for n in (-1.0, 0.0, 1.0)) <= controls.twist
                    for a, b in zip(transformed, candidate_twist, strict=True)
                )
            )
            if not compatible:
                continue
            reduced = self._reduced(transformed)
            comparison_twist = transformed if route_id.startswith("A_") else reduced
            integer_lift = (
                (0, 0)
                if route_id.startswith("A_")
                else (
                    int(round(transformed[0] - reduced[0])),
                    int(round(transformed[1] - reduced[1])),
                )
            )
            for tx in range(controls.nx):
                for ty in range(controls.ny):
                    permutation = self._permutation(
                        controls, operation.matrix, (tx, ty)
                    )
                    mapped = permutation.conj().T @ candidate @ permutation
                    phases = self._phases(reference, mapped, controls.algebraic)
                    diagonal = np.diag(phases)
                    aligned = diagonal.conj().T @ mapped @ diagonal
                    off = aligned - np.diag(np.diag(aligned))
                    reference_off = reference - np.diag(np.diag(reference))
                    result.append(
                        {
                            "operation": operation.identifier,
                            "translation": cast(JsonValue, [tx, ty]),
                            "transformed_twist_lift": cast(
                                JsonValue, list(transformed)
                            ),
                            "comparison_twist": cast(JsonValue, list(comparison_twist)),
                            "integer_lift": cast(JsonValue, list(integer_lift)),
                            "objective": float(
                                np.linalg.norm(off - reference_off, ord="fro")
                            ),
                            "energy_shift_diagnostic": float(
                                np.median(np.real(np.diag(aligned - reference)))
                            ),
                        }
                    )
        return result

    @staticmethod
    def _phases(
        reference: ComplexMatrix, mapped: ComplexMatrix, tolerance: float
    ) -> npt.NDArray[np.complex128]:
        dimension = int(reference.shape[0])
        phases = np.zeros(dimension, dtype=np.complex128)
        phases[0] = 1.0
        frontier = [0]
        while frontier:
            source = frontier.pop()
            for target in range(dimension - 1, -1, -1):
                if source == target or abs(reference[source, target]) <= tolerance:
                    continue
                if abs(mapped[source, target]) <= tolerance:
                    continue
                ratio = reference[source, target] / mapped[source, target]
                ratio /= abs(ratio)
                if phases[target] == 0.0:
                    phases[target] = phases[source] * ratio
                    frontier.append(target)
        if np.any(phases == 0.0):
            raise ValueError("independent phase graph is disconnected")
        return phases / np.abs(phases)

    def _attack(self, controls: VerificationControls) -> ComplexMatrix:
        permutation = self._permutation(controls, self._OPERATIONS[-1].matrix, (2, 3))
        phases = np.asarray(
            [
                np.exp(1.0j * (0.137 * x - 0.191 * y))
                for x in range(controls.nx)
                for y in range(controls.ny)
            ],
            dtype=np.complex128,
        )
        result: ComplexMatrix = permutation @ np.diag(phases)
        return result

    @staticmethod
    def _permutation(
        controls: VerificationControls,
        matrix: IntMatrix2,
        translation: tuple[int, int],
    ) -> ComplexMatrix:
        result = np.zeros((controls.nx * controls.ny,) * 2, dtype=np.complex128)
        for x in range(controls.nx):
            for y in range(controls.ny):
                tx = (
                    matrix[0][0] * x + matrix[0][1] * y + translation[0]
                ) % controls.nx
                ty = (
                    matrix[1][0] * x + matrix[1][1] * y + translation[1]
                ) % controls.ny
                result[tx * controls.ny + ty, x * controls.ny + y] = 1.0
        return result

    @staticmethod
    def _gauge(controls: VerificationControls, twist: FloatPair) -> ComplexMatrix:
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
    def _plant(
        controls: VerificationControls, site: tuple[int, int], strength: float
    ) -> ComplexMatrix:
        result = np.zeros((controls.nx * controls.ny,) * 2, dtype=np.complex128)
        result[site[0] * controls.ny + site[1], site[0] * controls.ny + site[1]] = (
            strength
        )
        return result

    def _operation(self, case_id: str) -> VerificationOperation:
        if case_id.startswith("central"):
            return self._OPERATIONS[0]
        identifier = case_id.rsplit("__", maxsplit=1)[-1]
        for operation in self._OPERATIONS:
            if operation.identifier == identifier:
                return operation
        raise ValueError(f"unknown operation in {case_id}")

    @staticmethod
    def _transform_twist(twist: FloatPair, matrix: IntMatrix2) -> FloatPair:
        return (
            matrix[0][0] * twist[0] + matrix[0][1] * twist[1],
            matrix[1][0] * twist[0] + matrix[1][1] * twist[1],
        )

    @staticmethod
    def _reduced(twist: FloatPair) -> FloatPair:
        return twist[0] % 1.0, twist[1] % 1.0

    @staticmethod
    def _site(
        controls: VerificationControls,
        matrix: IntMatrix2,
        site: tuple[int, int],
    ) -> tuple[int, int]:
        return (
            (matrix[0][0] * site[0] + matrix[0][1] * site[1]) % controls.nx,
            (matrix[1][0] * site[0] + matrix[1][1] * site[1]) % controls.ny,
        )

    @staticmethod
    def _maximum(matrix: ComplexMatrix) -> float:
        return float(np.max(np.abs(matrix), initial=0.0))


class StageBVerifier:
    """Validate provenance confinement and independent numerical reconstruction."""

    __slots__ = ("_reconstruction",)

    def __init__(self) -> None:
        self._reconstruction = IndependentStageBReconstruction()

    def execute(self, result_path: Path, repository_root: Path) -> VerificationResult:
        root = repository_root.resolve(strict=True)
        if not repository_root.is_absolute() or root != repository_root:
            raise ValueError("repository_root must be canonical and absolute")
        result = result_path if result_path.is_absolute() else root / result_path
        result = result.resolve(strict=True)
        if not result.is_relative_to(root):
            raise ValueError("result path escapes repository root")
        payload = cast(JsonValue, json.loads(result.read_text(encoding="utf-8")))
        if not isinstance(payload, dict):
            raise TypeError("result must be a JSON object")
        provenance_value = payload.get("provenance")
        if not isinstance(provenance_value, dict):
            raise TypeError("result provenance must be an object")
        for key, value in provenance_value.items():
            if not key.endswith("_path"):
                continue
            if not isinstance(value, str):
                raise TypeError(f"provenance {key} must be a string")
            represented = Path(value)
            if represented.is_absolute() or ".." in represented.parts:
                raise ValueError(f"provenance {key} is not canonical relative")
            resolved = (root / represented).resolve(strict=True)
            if not resolved.is_relative_to(root):
                raise ValueError(f"provenance {key} escapes repository root")
            digest_key = key.removesuffix("_path") + "_sha256"
            expected_digest = provenance_value.get(digest_key)
            if isinstance(expected_digest, str):
                actual = hashlib.sha256(resolved.read_bytes()).hexdigest()
                if actual != expected_digest:
                    raise ValueError(f"provenance digest differs for {key}")
        return self._reconstruction.execute(payload)


def main() -> None:
    """Adapt command-line paths to the independent verifier."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--result", required=True, type=Path)
    parser.add_argument("--repository-root", required=True, type=Path)
    arguments = parser.parse_args()
    result = StageBVerifier().execute(arguments.result, arguments.repository_root)
    print(f"defect_2d_stage_b_reconstruction={result.reconstruction_status}")
    print(f"defect_2d_stage_b_criteria={result.criteria_status}")
    print(
        "maximum_independent_reconstruction_difference="
        f"{result.maximum_metric_difference:.16e}"
    )
    for failure in result.failures:
        print(f"failure={failure}")
    if result.reconstruction_status != "PASS" or result.criteria_status != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
