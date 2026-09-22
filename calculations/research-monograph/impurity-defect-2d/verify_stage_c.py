#!/usr/bin/env python3
"""Independently verify an authored-toy Stage C result without runner imports."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type ComplexMatrix = npt.NDArray[np.complex128]
type FloatPair = tuple[float, float]
type IntPair = tuple[int, int]


class IndependentStageCVerifier:
    """Reconstruct Stage C matrices and analytic fit oracles independently."""

    __slots__ = ()

    @staticmethod
    def _mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be an object")
        return value

    @staticmethod
    def _array(value: JsonValue, name: str) -> list[JsonValue]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be an array")
        return value

    @staticmethod
    def _number(value: JsonValue, name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be numeric")
        result = float(value)
        if not np.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result

    @staticmethod
    def _index(site: IntPair) -> int:
        return (site[0] % 8) * 8 + (site[1] % 8)

    def _bond(
        self,
        displacement: IntPair,
        value: float,
        twist: FloatPair,
        route: str,
        include_reverse: bool = True,
    ) -> ComplexMatrix:
        result = np.zeros((64, 64), dtype=np.complex128)
        row = self._index((0, 0))
        column = self._index(displacement)
        if route == "A_centered_uniform":
            phase = np.exp(
                2.0j
                * np.pi
                * (twist[0] * displacement[0] + twist[1] * displacement[1])
                / 8.0
            )
        elif route == "B_reduced_seam":
            qx, _ = divmod(displacement[0], 8)
            qy, _ = divmod(displacement[1], 8)
            phase = np.exp(2.0j * np.pi * (qx * twist[0] + qy * twist[1]))
        else:
            raise ValueError(f"unsupported route {route}")
        result[row, column] = value * phase
        if include_reverse:
            result[column, row] = value * phase.conjugate()
        return result

    def _case_matrix(self, case_id: str, twist: FloatPair, route: str) -> ComplexMatrix:
        if case_id == "directional_nearest_neighbor":
            return self._bond((1, 0), 0.04, twist, route) + self._bond(
                (0, 1), -0.03, twist, route
            )
        if case_id == "finite_range_diagonal_nonlocal":
            return self._bond((1, 1), 0.025, twist, route)
        raise ValueError(f"unexpected case {case_id}")

    @staticmethod
    def _digest(matrix: ComplexMatrix) -> str:
        return hashlib.sha256(
            np.ascontiguousarray(matrix, dtype="<c16").tobytes()
        ).hexdigest()

    @staticmethod
    def _maximum(matrix: ComplexMatrix) -> float:
        return float(np.max(np.abs(matrix), initial=0.0))

    @staticmethod
    def _expected_fit(case_id: str, model_class: str) -> tuple[float, bool]:
        if case_id == "directional_nearest_neighbor":
            residuals = {
                "point_scalar_onsite": np.sqrt(2.0 * (0.04**2 + 0.03**2)),
                "finite_support_diagonal_onsite": np.sqrt(2.0 * (0.04**2 + 0.03**2)),
                "onsite_plus_isotropic_nearest_neighbor": 0.07,
                "onsite_plus_directional_nearest_neighbor": 0.0,
                "finite_range_nonlocal_radius_two": 0.0,
            }
            return float(residuals[model_class]), model_class in (
                "onsite_plus_directional_nearest_neighbor",
                "finite_range_nonlocal_radius_two",
            )
        residuals = {
            "point_scalar_onsite": np.sqrt(2.0) * 0.025,
            "finite_support_diagonal_onsite": np.sqrt(2.0) * 0.025,
            "onsite_plus_isotropic_nearest_neighbor": np.sqrt(2.0) * 0.025,
            "onsite_plus_directional_nearest_neighbor": np.sqrt(2.0) * 0.025,
            "finite_range_nonlocal_radius_two": 0.0,
        }
        return float(residuals[model_class]), model_class == (
            "finite_range_nonlocal_radius_two"
        )

    def execute(self, design_path: Path, result_path: Path) -> dict[str, JsonValue]:
        design_bytes = design_path.read_bytes()
        design = self._mapping(
            cast(JsonValue, json.loads(design_bytes)), "Stage C design"
        )
        result = self._mapping(
            cast(JsonValue, json.loads(result_path.read_text())), "Stage C result"
        )
        if result.get("design_sha256") != hashlib.sha256(design_bytes).hexdigest():
            raise ValueError("Stage C result design digest differs")
        if result.get("accepted_parent_read") is not False:
            raise ValueError("the authored-toy result must not read an accepted parent")
        if result.get("result_id") != (
            "research-monograph.impurity-defect-2d.stage-c.authored-toy.v1"
        ):
            raise ValueError("unexpected Stage C result identity")
        twists: dict[str, FloatPair] = {
            "gamma": (0.0, 0.0),
            "generic": (0.37, -0.23),
        }
        expected_models = {
            "directional_nearest_neighbor": (
                "onsite_plus_directional_nearest_neighbor"
            ),
            "finite_range_diagonal_nonlocal": "finite_range_nonlocal_radius_two",
        }
        maximum_difference = 0.0
        route_record_count = 0
        fit_record_count = 0
        schedule_digests: dict[tuple[str, str, str], dict[str, str]] = {}
        schedules = self._array(result["schedules"], "schedules")
        if len(schedules) != 2:
            raise ValueError("expected two Stage C schedules")
        for schedule_value in schedules:
            schedule = self._mapping(schedule_value, "schedule")
            schedule_id = cast(str, schedule["schedule_id"])
            if schedule.get("fresh_spawned_process") is not True:
                raise ValueError("Stage C schedule lacks fresh-process evidence")
            records = self._array(schedule["route_records"], "route_records")
            if len(records) != 8:
                raise ValueError("each schedule must retain eight route records")
            for record_value in records:
                record = self._mapping(record_value, "route record")
                route = cast(str, record["route"])
                case_id = cast(str, record["case_id"])
                twist_id = cast(str, record["twist_id"])
                expected = self._case_matrix(case_id, twists[twist_id], route)
                digest = self._digest(expected)
                if record["matrix_sha256"] != digest:
                    raise ValueError("independent Stage C matrix digest differs")
                schedule_digests.setdefault((route, case_id, twist_id), {})[
                    schedule_id
                ] = digest
                hermiticity = self._maximum(expected - expected.conj().T)
                maximum_difference = max(
                    maximum_difference,
                    abs(
                        self._number(
                            record["hermiticity_maximum_absolute"], "Hermiticity"
                        )
                        - hermiticity
                    ),
                )
                if record["selected_model_class"] != expected_models[case_id]:
                    raise ValueError("first accepted Stage C model class differs")
                fits = self._array(record["fits"], "fits")
                if len(fits) != 5:
                    raise ValueError("each route record must retain five model fits")
                for fit_value in fits:
                    fit = self._mapping(fit_value, "fit")
                    model_class = cast(str, fit["model_class"])
                    expected_frobenius, expected_accepted = self._expected_fit(
                        case_id, model_class
                    )
                    observed = self._number(fit["residual_frobenius"], "fit residual")
                    maximum_difference = max(
                        maximum_difference, abs(observed - expected_frobenius)
                    )
                    if fit["accepted"] is not expected_accepted:
                        raise ValueError("model-class acceptance differs")
                    fit_record_count += 1
                route_record_count += 1
        for digests in schedule_digests.values():
            if digests.get("A_then_B") != digests.get("B_then_A"):
                raise ValueError("Stage C schedule digest differs")
        bridge_count = 0
        maximum_bridge_difference = 0.0
        for bridge_value in self._array(result["bridges"], "bridges"):
            bridge = self._mapping(bridge_value, "bridge")
            case_id = cast(str, bridge["case_id"])
            twist_id = cast(str, bridge["twist_id"])
            twist = twists[twist_id]
            route_a = self._case_matrix(case_id, twist, "A_centered_uniform")
            route_b = self._case_matrix(case_id, twist, "B_reduced_seam")
            phases = np.asarray(
                [
                    np.exp(2.0j * np.pi * (x * twist[0] + y * twist[1]) / 8.0)
                    for x in range(8)
                    for y in range(8)
                ],
                dtype=np.complex128,
            )
            reconstructed = route_b - phases[:, None] * route_a * phases.conj()[None, :]
            expected_maximum = self._maximum(reconstructed)
            difference = abs(
                self._number(bridge["maximum_absolute"], "bridge maximum")
                - expected_maximum
            )
            maximum_bridge_difference = max(maximum_bridge_difference, difference)
            maximum_difference = max(maximum_difference, difference)
            bridge_count += 1
        symmetry_records = self._array(result["symmetry_records"], "symmetry records")
        if len(symmetry_records) != 16:
            raise ValueError("expected sixteen Stage C symmetry records")
        for value in symmetry_records:
            record = self._mapping(value, "symmetry record")
            maximum_difference = max(
                maximum_difference,
                abs(self._number(record["maximum_absolute"], "symmetry maximum")),
            )
        adverse_values = {
            cast(str, self._mapping(value, "adverse")["control_id"]): self._number(
                self._mapping(value, "adverse")["value"], "adverse value"
            )
            for value in self._array(result["adverse_controls"], "adverse controls")
        }
        expected_adverse = {
            "directional_as_isotropic": 0.07,
            "nonlocal_as_directional": float(np.sqrt(2.0) * 0.025),
            "omit_hermitian_reverse": 0.04,
        }
        for identifier, expected_adverse_value in expected_adverse.items():
            maximum_difference = max(
                maximum_difference,
                abs(adverse_values[identifier] - expected_adverse_value),
            )
        raw_a = self._case_matrix(
            "directional_nearest_neighbor", twists["generic"], "A_centered_uniform"
        )
        raw_b = self._case_matrix(
            "directional_nearest_neighbor", twists["generic"], "B_reduced_seam"
        )
        maximum_difference = max(
            maximum_difference,
            abs(adverse_values["omit_gauge_bridge"] - self._maximum(raw_b - raw_a)),
        )
        criteria = self._array(result["criteria"], "criteria")
        if len(criteria) != 10 or not all(
            self._mapping(value, "criterion").get("passed") is True
            for value in criteria
        ):
            raise ValueError("Stage C retained criteria do not all pass")
        tolerance = self._number(
            self._mapping(design["criteria"], "design criteria")[
                "independent_reconstruction_absolute"
            ],
            "independent tolerance",
        )
        passed = maximum_difference <= tolerance
        return {
            "reconstruction_status": "PASS" if passed else "FAIL",
            "criteria_status": "PASS",
            "maximum_independent_difference": maximum_difference,
            "independent_tolerance": tolerance,
            "route_record_count": route_record_count,
            "fit_record_count": fit_record_count,
            "bridge_record_count": bridge_count,
            "maximum_bridge_reconstruction_difference": maximum_bridge_difference,
        }


def main() -> None:
    """Adapt command-line arguments into the independent Stage C verifier."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--design", type=Path, required=True)
    parser.add_argument("--toy-result", type=Path, required=True)
    arguments = parser.parse_args()
    result = IndependentStageCVerifier().execute(arguments.design, arguments.toy_result)
    print(f"defect_2d_stage_c_toy_reconstruction={result['reconstruction_status']}")
    print(f"defect_2d_stage_c_toy_criteria={result['criteria_status']}")
    print(
        "maximum_independent_difference="
        f"{cast(float, result['maximum_independent_difference']):.16e}"
    )


if __name__ == "__main__":
    main()
