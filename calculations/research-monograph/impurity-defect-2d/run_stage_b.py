#!/usr/bin/env python3
"""Run an exactly authorized data-complete multi-route Stage B study."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from dataclasses import dataclass
from multiprocessing import get_context
from multiprocessing.connection import Connection
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
class Hopping:
    """One retained scalar-parent hopping coefficient."""

    rx: int
    ry: int
    value: complex


@dataclass(frozen=True, slots=True)
class D4Operation:
    """One frozen point-group operation."""

    identifier: str
    matrix: IntMatrix2
    target: tuple[int, int]


@dataclass(frozen=True, slots=True)
class Plant:
    """One scalar point-onsite plant."""

    identifier: str
    site: tuple[int, int]
    strength: float


@dataclass(frozen=True, slots=True)
class StageBControls:
    """Closed multi-route numerical and inventory controls."""

    design_id: str
    nx: int
    ny: int
    twists: tuple[FloatPair, FloatPair]
    central: Plant
    off_axis: Plant
    operations: tuple[D4Operation, ...]
    attack_matrix: IntMatrix2
    attack_translation: tuple[int, int]
    attack_phase_steps: FloatPair
    energy_shift: float
    algebraic_tolerance: float
    covariance_tolerance: float
    route_tolerance: float
    tie_tolerance: float
    twist_tolerance: float
    adverse_floor: float
    expected_gamma_count: int
    expected_generic_count: int

    @classmethod
    def authored_toy(cls) -> StageBControls:
        """Return the frozen geometry with no accepted-parent dependency."""

        matrices: tuple[IntMatrix2, ...] = (
            ((1, 0), (0, 1)),
            ((0, -1), (1, 0)),
            ((-1, 0), (0, -1)),
            ((0, 1), (-1, 0)),
            ((1, 0), (0, -1)),
            ((-1, 0), (0, 1)),
            ((0, 1), (1, 0)),
            ((0, -1), (-1, 0)),
        )
        identifiers = (
            "identity",
            "quarter_turn",
            "half_turn",
            "three_quarter_turn",
            "reflection_x",
            "reflection_y",
            "reflection_diagonal",
            "reflection_antidiagonal",
        )
        targets = ((1, 2), (6, 1), (7, 6), (2, 7), (1, 6), (7, 2), (2, 1), (6, 7))
        return cls(
            design_id="research-monograph.impurity-defect-2d.stage-b.multiroute-design.v1",
            nx=8,
            ny=8,
            twists=((0.0, 0.0), (0.37, -0.23)),
            central=Plant("central", (0, 0), -0.25),
            off_axis=Plant("off_axis", (1, 2), -0.25),
            operations=tuple(
                D4Operation(identifier, matrix, target)
                for identifier, matrix, target in zip(
                    identifiers, matrices, targets, strict=True
                )
            ),
            attack_matrix=matrices[-1],
            attack_translation=(2, 3),
            attack_phase_steps=(0.137, -0.191),
            energy_shift=0.137,
            algebraic_tolerance=1.0e-11,
            covariance_tolerance=1.0e-10,
            route_tolerance=1.0e-10,
            tie_tolerance=1.0e-10,
            twist_tolerance=1.0e-14,
            adverse_floor=1.0e-6,
            expected_gamma_count=512,
            expected_generic_count=64,
        )


@dataclass(frozen=True, slots=True)
class StageBExecutionAuthorization:
    """Exact future binding for accepted-parent execution."""

    authorization_id: str
    checkpoint_path: str
    checkpoint_sha256: str
    repository_root: str
    design_path: str
    design_sha256: str
    runner_path: str
    runner_sha256: str
    verifier_path: str
    verifier_sha256: str
    plotter_path: str
    plotter_sha256: str
    result_schema_path: str
    result_schema_sha256: str
    native_manifest_path: str
    native_manifest_sha256: str
    parent_input_path: str
    parent_input_sha256: str
    parent_path: str
    parent_sha256: str
    stage_a_result_path: str
    stage_a_result_sha256: str
    output_path: str
    maximum_matrix_dimension: int
    maximum_execution_schedules: int
    maximum_known_map_route_evaluations: int
    maximum_total_blind_candidate_evaluations: int
    maximum_runtime_seconds: int
    maximum_peak_memory_gib: float
    maximum_retained_output_mib: float
    network_access: bool
    human_response_verbatim: str


class ClosedJsonReader:
    """Decode JSON through explicit closed representation checks."""

    __slots__ = ()

    def read(self, path: Path) -> dict[str, JsonValue]:
        value = cast(JsonValue, json.loads(path.read_text(encoding="utf-8")))
        return self.mapping(value, str(path))

    @staticmethod
    def mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be a JSON object")
        return value

    @staticmethod
    def array(value: JsonValue, name: str) -> list[JsonValue]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return value

    @staticmethod
    def records(value: JsonValue, name: str) -> tuple[dict[str, JsonValue], ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        result: list[dict[str, JsonValue]] = []
        for index, item in enumerate(value):
            if not isinstance(item, dict):
                raise TypeError(f"{name}[{index}] must be a JSON object")
            result.append(item)
        return tuple(result)

    @staticmethod
    def string(value: JsonValue, name: str) -> str:
        if not isinstance(value, str) or not value:
            raise TypeError(f"{name} must be a nonempty string")
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
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be numeric")
        result = float(value)
        if not np.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result

    def integer_pair(self, value: JsonValue, name: str) -> tuple[int, int]:
        items = self.array(value, name)
        if len(items) != 2:
            raise ValueError(f"{name} must contain two entries")
        return self.integer(items[0], f"{name}[0]"), self.integer(
            items[1], f"{name}[1]"
        )

    def real_pair(self, value: JsonValue, name: str) -> FloatPair:
        items = self.array(value, name)
        if len(items) != 2:
            raise ValueError(f"{name} must contain two entries")
        return self.real(items[0], f"{name}[0]"), self.real(items[1], f"{name}[1]")

    def matrix_2(self, value: JsonValue, name: str) -> IntMatrix2:
        rows = self.array(value, name)
        if len(rows) != 2:
            raise ValueError(f"{name} must contain two rows")
        return self.integer_pair(rows[0], f"{name}[0]"), self.integer_pair(
            rows[1], f"{name}[1]"
        )


class StageBInputDeserializer:
    """Load the adopted multi-route design, future authority, and parent hops."""

    __slots__ = ("_json",)

    def __init__(self) -> None:
        self._json = ClosedJsonReader()

    def controls(self, path: Path) -> StageBControls:
        root = self._json.read(path)
        if root.get("design_id") != (
            "research-monograph.impurity-defect-2d.stage-b.multiroute-design.v1"
        ):
            raise ValueError("not the adopted multi-route Stage B design")
        if (
            root.get("design_status")
            != "human_accepted_for_execution_free_implementation"
        ):
            raise ValueError(
                "multi-route Stage B design is not implementation-authorized"
            )
        represented = self._json.mapping(root["represented_space"], "represented_space")
        shape = self._json.integer_pair(represented["shape"], "shape")
        if shape != (8, 8):
            raise ValueError("Stage B shape differs from 8x8")
        shared = self._json.mapping(root["shared_controls"], "shared_controls")
        twist_values = self._json.array(shared["base_twist_lifts_turns"], "base twists")
        if len(twist_values) != 2:
            raise ValueError("Stage B requires two base twists")
        plants = self._json.mapping(shared["plants"], "plants")
        central = self._plant(
            "central", self._json.mapping(plants["central"], "central")
        )
        off_axis = self._plant(
            "off_axis", self._json.mapping(plants["off_axis"], "off_axis")
        )
        identifiers = tuple(
            self._json.string(item, "D4 operation")
            for item in self._json.array(shared["D4_operation_order"], "D4 order")
        )
        matrices = tuple(
            self._json.matrix_2(item, "D4 matrix")
            for item in self._json.array(shared["D4_matrices"], "D4 matrices")
        )
        targets = tuple(
            self._json.integer_pair(item, "D4 target")
            for item in self._json.array(shared["off_axis_orbit"], "off-axis orbit")
        )
        if not len(identifiers) == len(matrices) == len(targets) == 8:
            raise ValueError("Stage B requires exactly eight ordered D4 operations")
        attack = self._json.mapping(shared["known_map_attack"], "known_map_attack")
        criteria = self._json.mapping(root["criteria"], "criteria")
        inventory = self._json.mapping(root["case_inventory"], "case_inventory")
        if inventory.get("execution_schedules") != 2:
            raise ValueError("Stage B requires two execution schedules")
        blind_contract = self._json.mapping(
            root["blind_alignment_contract"], "blind_alignment_contract"
        )
        expected_counts = self._json.mapping(
            blind_contract["expected_route_local_counts"],
            "expected_route_local_counts",
        )
        return StageBControls(
            design_id=self._json.string(root["design_id"], "design_id"),
            nx=shape[0],
            ny=shape[1],
            twists=(
                self._json.real_pair(twist_values[0], "Gamma twist"),
                self._json.real_pair(twist_values[1], "generic twist"),
            ),
            central=central,
            off_axis=off_axis,
            operations=tuple(
                D4Operation(identifier, matrix, target)
                for identifier, matrix, target in zip(
                    identifiers, matrices, targets, strict=True
                )
            ),
            attack_matrix=matrices[-1],
            attack_translation=self._json.integer_pair(
                attack["translation_cells"], "translation_cells"
            ),
            attack_phase_steps=(0.137, -0.191),
            energy_shift=self._json.real(
                attack["energy_reference_shift"], "energy_reference_shift"
            ),
            algebraic_tolerance=self._json.real(
                criteria["algebraic_absolute"], "algebraic_absolute"
            ),
            covariance_tolerance=self._json.real(
                criteria["symmetry_covariance_absolute"], "symmetry_covariance_absolute"
            ),
            route_tolerance=self._json.real(
                criteria["route_equivalence_absolute"], "route_equivalence_absolute"
            ),
            tie_tolerance=self._json.real(
                criteria["blind_objective_tie_absolute"], "blind_objective_tie_absolute"
            ),
            twist_tolerance=self._json.real(
                criteria["twist_compatibility_absolute"], "twist_compatibility_absolute"
            ),
            adverse_floor=self._json.real(
                criteria["fixed_twist_adverse_floor"], "fixed_twist_adverse_floor"
            ),
            expected_gamma_count=self._json.integer(
                expected_counts["gamma"], "expected gamma count"
            ),
            expected_generic_count=self._json.integer(
                expected_counts["generic"], "expected generic count"
            ),
        )

    def authorization(self, path: Path) -> StageBExecutionAuthorization:
        root = self._json.read(path)
        expected: dict[str, JsonValue] = {
            "schema_version": 2,
            "authorization_kind": "defect-2d-stage-execution",
            "stage_id": "B_scalar_onsite_and_D4_multiroute",
            "execution_authorized": True,
        }
        for key, value in expected.items():
            if root.get(key) != value:
                raise ValueError(f"authorization field {key!r} is invalid")
        resources = self._json.mapping(root["resource_envelope"], "resource_envelope")
        return StageBExecutionAuthorization(
            authorization_id=self._json.string(
                root["authorization_id"], "authorization_id"
            ),
            checkpoint_path=self._json.string(
                root["checkpoint_path"], "checkpoint_path"
            ),
            checkpoint_sha256=self._json.string(
                root["checkpoint_sha256"], "checkpoint_sha256"
            ),
            repository_root=self._json.string(
                root["repository_root"], "repository_root"
            ),
            design_path=self._json.string(root["design_path"], "design_path"),
            design_sha256=self._json.string(root["design_sha256"], "design_sha256"),
            runner_path=self._json.string(root["runner_path"], "runner_path"),
            runner_sha256=self._json.string(root["runner_sha256"], "runner_sha256"),
            verifier_path=self._json.string(root["verifier_path"], "verifier_path"),
            verifier_sha256=self._json.string(
                root["verifier_sha256"], "verifier_sha256"
            ),
            plotter_path=self._json.string(root["plotter_path"], "plotter_path"),
            plotter_sha256=self._json.string(root["plotter_sha256"], "plotter_sha256"),
            result_schema_path=self._json.string(
                root["result_schema_path"], "result_schema_path"
            ),
            result_schema_sha256=self._json.string(
                root["result_schema_sha256"], "result_schema_sha256"
            ),
            native_manifest_path=self._json.string(
                root["native_manifest_path"], "native_manifest_path"
            ),
            native_manifest_sha256=self._json.string(
                root["native_manifest_sha256"], "native_manifest_sha256"
            ),
            parent_input_path=self._json.string(
                root["parent_input_path"], "parent_input_path"
            ),
            parent_input_sha256=self._json.string(
                root["parent_input_sha256"], "parent_input_sha256"
            ),
            parent_path=self._json.string(root["parent_path"], "parent_path"),
            parent_sha256=self._json.string(root["parent_sha256"], "parent_sha256"),
            stage_a_result_path=self._json.string(
                root["stage_a_result_path"], "stage_a_result_path"
            ),
            stage_a_result_sha256=self._json.string(
                root["stage_a_result_sha256"], "stage_a_result_sha256"
            ),
            output_path=self._json.string(root["output_path"], "output_path"),
            maximum_matrix_dimension=self._json.integer(
                resources["maximum_matrix_dimension"], "maximum_matrix_dimension"
            ),
            maximum_execution_schedules=self._json.integer(
                resources["maximum_execution_schedules"],
                "maximum_execution_schedules",
            ),
            maximum_known_map_route_evaluations=self._json.integer(
                resources["maximum_known_map_route_evaluations"],
                "maximum_known_map_route_evaluations",
            ),
            maximum_total_blind_candidate_evaluations=self._json.integer(
                resources["maximum_total_blind_candidate_evaluations"],
                "maximum_total_blind_candidate_evaluations",
            ),
            maximum_runtime_seconds=self._json.integer(
                resources["maximum_runtime_seconds"], "maximum_runtime_seconds"
            ),
            maximum_peak_memory_gib=self._json.real(
                resources["maximum_peak_memory_gib"], "maximum_peak_memory_gib"
            ),
            maximum_retained_output_mib=self._json.real(
                resources["maximum_retained_output_mib"], "maximum_retained_output_mib"
            ),
            network_access=self._json.boolean(
                resources["network_access"], "network_access"
            ),
            human_response_verbatim=self._json.string(
                root["human_response_verbatim"], "human_response_verbatim"
            ),
        )

    def hoppings(
        self,
        path: Path,
        parent_input_path: Path,
        maximum_radius_squared: int,
    ) -> tuple[Hopping, ...]:
        parent_input = self._json.read(parent_input_path)
        isotropic = self._json.mapping(
            parent_input["isotropic_potential"], "isotropic_potential"
        )
        if (
            self._json.real(isotropic["lambda_x"], "lambda_x") != 0.5
            or self._json.real(isotropic["lambda_y"], "lambda_y") != 0.5
        ):
            raise ValueError("parent isotropic lambda_x and lambda_y must equal 0.5")
        coupling_sequence = self._json.array(
            parent_input["coupling_sequence"], "coupling_sequence"
        )
        if 0.0 not in [
            self._json.real(value, "coupling_sequence value")
            for value in coupling_sequence
        ]:
            raise ValueError("parent coupling sequence does not contain lambda_xy=0")
        root = self._json.read(path)
        entries = self._json.records(
            root["coupling_continuation"], "coupling_continuation"
        )
        selected = [
            entry
            for entry in entries
            if self._json.real(entry["lambda_xy"], "lambda_xy") == 0.0
        ]
        if len(selected) != 1:
            raise ValueError("parent must have exactly one lambda_xy=0 entry")
        result: list[Hopping] = []
        for record in self._json.records(
            selected[0]["hopping_coefficients"], "hoppings"
        ):
            rx = self._json.integer(record["rx"], "rx")
            ry = self._json.integer(record["ry"], "ry")
            if rx * rx + ry * ry <= maximum_radius_squared:
                result.append(
                    Hopping(
                        rx,
                        ry,
                        complex(
                            self._json.real(record["real"], "real"),
                            self._json.real(record["imag"], "imag"),
                        ),
                    )
                )
        if not result:
            raise ValueError("retained parent hopping inventory is empty")
        return tuple(result)

    def _plant(self, identifier: str, record: dict[str, JsonValue]) -> Plant:
        return Plant(
            identifier,
            self._json.integer_pair(record["site"], f"{identifier}.site"),
            self._json.real(record["strength"], f"{identifier}.strength"),
        )


class StageBMatrixActions:
    """Own exact site, gauge, attack, and finite-matrix transformations."""

    __slots__ = ()

    @staticmethod
    def uniform(
        controls: StageBControls,
        hoppings: tuple[Hopping, ...],
        twist_lift: FloatPair,
    ) -> ComplexMatrix:
        result = np.zeros((controls.nx * controls.ny,) * 2, dtype=np.complex128)
        for x in range(controls.nx):
            for y in range(controls.ny):
                row = x * controls.ny + y
                for hopping in hoppings:
                    tx = (x + hopping.rx) % controls.nx
                    ty = (y + hopping.ry) % controls.ny
                    phase = np.exp(
                        2.0j
                        * np.pi
                        * (
                            twist_lift[0] * hopping.rx / controls.nx
                            + twist_lift[1] * hopping.ry / controls.ny
                        )
                    )
                    result[row, tx * controls.ny + ty] += hopping.value * phase
        return result

    @staticmethod
    def seam(
        controls: StageBControls,
        hoppings: tuple[Hopping, ...],
        reduced_twist: FloatPair,
    ) -> ComplexMatrix:
        result = np.zeros((controls.nx * controls.ny,) * 2, dtype=np.complex128)
        for x in range(controls.nx):
            for y in range(controls.ny):
                row = x * controls.ny + y
                for hopping in hoppings:
                    qx, tx = divmod(x + hopping.rx, controls.nx)
                    qy, ty = divmod(y + hopping.ry, controls.ny)
                    phase = np.exp(
                        2.0j * np.pi * (qx * reduced_twist[0] + qy * reduced_twist[1])
                    )
                    result[row, tx * controls.ny + ty] += hopping.value * phase
        return result

    @staticmethod
    def site_gauge(controls: StageBControls, twist_lift: FloatPair) -> ComplexMatrix:
        phases = [
            np.exp(
                2.0j
                * np.pi
                * (x * twist_lift[0] / controls.nx + y * twist_lift[1] / controls.ny)
            )
            for x in range(controls.nx)
            for y in range(controls.ny)
        ]
        return np.diag(np.asarray(phases, dtype=np.complex128))

    @staticmethod
    def permutation(
        controls: StageBControls,
        matrix: IntMatrix2,
        translation: tuple[int, int] = (0, 0),
    ) -> ComplexMatrix:
        result = np.zeros((controls.nx * controls.ny,) * 2, dtype=np.complex128)
        for x in range(controls.nx):
            for y in range(controls.ny):
                tx, ty = StageBMatrixActions.affine_site(
                    controls, matrix, (x, y), translation
                )
                result[tx * controls.ny + ty, x * controls.ny + y] = 1.0
        return result

    @staticmethod
    def attack(controls: StageBControls) -> ComplexMatrix:
        permutation = StageBMatrixActions.permutation(
            controls, controls.attack_matrix, controls.attack_translation
        )
        phases = [
            np.exp(
                1.0j
                * (
                    controls.attack_phase_steps[0] * x
                    + controls.attack_phase_steps[1] * y
                )
            )
            for x in range(controls.nx)
            for y in range(controls.ny)
        ]
        result: ComplexMatrix = permutation @ np.diag(
            np.asarray(phases, dtype=np.complex128)
        )
        return result

    @staticmethod
    def plant(
        controls: StageBControls, site: tuple[int, int], strength: float
    ) -> ComplexMatrix:
        result = np.zeros((controls.nx * controls.ny,) * 2, dtype=np.complex128)
        index = site[0] * controls.ny + site[1]
        result[index, index] = strength
        return result

    @staticmethod
    def transformed_twist(twist: FloatPair, matrix: IntMatrix2) -> FloatPair:
        return (
            matrix[0][0] * twist[0] + matrix[0][1] * twist[1],
            matrix[1][0] * twist[0] + matrix[1][1] * twist[1],
        )

    @staticmethod
    def reduced_twist(twist: FloatPair) -> FloatPair:
        return twist[0] % 1.0, twist[1] % 1.0

    @staticmethod
    def affine_site(
        controls: StageBControls,
        matrix: IntMatrix2,
        site: tuple[int, int],
        translation: tuple[int, int],
    ) -> tuple[int, int]:
        return (
            (matrix[0][0] * site[0] + matrix[0][1] * site[1] + translation[0])
            % controls.nx,
            (matrix[1][0] * site[0] + matrix[1][1] * site[1] + translation[1])
            % controls.ny,
        )

    @staticmethod
    def matrix_sha256(matrix: ComplexMatrix) -> str:
        return hashlib.sha256(
            np.ascontiguousarray(matrix, dtype="<c16").tobytes()
        ).hexdigest()

    @staticmethod
    def maximum(matrix: ComplexMatrix) -> float:
        return float(np.max(np.abs(matrix), initial=0.0))


class StageBParentValidator:
    """Validate Hermiticity and D4 closure of the retained hopping inventory."""

    __slots__ = ()

    def execute(
        self, controls: StageBControls, hoppings: tuple[Hopping, ...]
    ) -> dict[str, JsonValue]:
        by_displacement: dict[tuple[int, int], complex] = {}
        for hopping in hoppings:
            key = (hopping.rx, hopping.ry)
            if key in by_displacement:
                raise ValueError(f"duplicate retained hopping displacement {key}")
            by_displacement[key] = hopping.value
        maximum_hermiticity = 0.0
        maximum_d4 = 0.0
        for displacement, value in by_displacement.items():
            reverse = (-displacement[0], -displacement[1])
            if reverse not in by_displacement:
                raise ValueError(f"missing Hermitian partner for {displacement}")
            maximum_hermiticity = max(
                maximum_hermiticity,
                abs(by_displacement[reverse] - value.conjugate()),
            )
            for operation in controls.operations:
                transformed = (
                    operation.matrix[0][0] * displacement[0]
                    + operation.matrix[0][1] * displacement[1],
                    operation.matrix[1][0] * displacement[0]
                    + operation.matrix[1][1] * displacement[1],
                )
                if transformed not in by_displacement:
                    raise ValueError(
                        f"retained hopping inventory is not D4-closed at {transformed}"
                    )
                maximum_d4 = max(maximum_d4, abs(by_displacement[transformed] - value))
        if maximum_hermiticity > controls.algebraic_tolerance:
            raise ValueError("retained hopping inventory fails Hermiticity")
        if maximum_d4 > controls.algebraic_tolerance:
            raise ValueError("retained hopping inventory fails D4 covariance")
        return {
            "unique_displacements": len(by_displacement),
            "maximum_hermiticity_defect": maximum_hermiticity,
            "maximum_D4_defect": maximum_d4,
        }


class StageBBlindAlignment:
    """Enumerate every blind candidate without plant or authored-map access."""

    __slots__ = ("_matrix",)

    def __init__(self) -> None:
        self._matrix = StageBMatrixActions()

    def execute(
        self,
        controls: StageBControls,
        route: str,
        reference: ComplexMatrix,
        candidate: ComplexMatrix,
        reference_twist: FloatPair,
        candidate_twist: FloatPair,
    ) -> dict[str, JsonValue]:
        if not self._connected(reference, controls.algebraic_tolerance):
            return {
                "issue_code": "DEFECT_2D.PHASE_GRAPH_DISCONNECTED",
                "candidate_count": 0,
                "candidates": [],
                "ambiguity_count": 0,
                "ambiguity_set": [],
                "selected_map": None,
                "extracted_operator": None,
            }
        records: list[JsonValue] = []
        for operation in controls.operations:
            transformed = self._matrix.transformed_twist(
                reference_twist, operation.matrix
            )
            if not self._compatible(
                route, transformed, candidate_twist, controls.twist_tolerance
            ):
                continue
            reduced = self._matrix.reduced_twist(transformed)
            comparison_twist = transformed if route == "A_centered_uniform" else reduced
            integer_lift = (
                (0, 0)
                if route == "A_centered_uniform"
                else (
                    int(round(transformed[0] - reduced[0])),
                    int(round(transformed[1] - reduced[1])),
                )
            )
            for tx in range(controls.nx):
                for ty in range(controls.ny):
                    permutation = self._matrix.permutation(
                        controls, operation.matrix, (tx, ty)
                    )
                    mapped = permutation.conj().T @ candidate @ permutation
                    phases = self._phases(
                        reference, mapped, controls.algebraic_tolerance
                    )
                    diagonal = np.diag(phases)
                    aligned = diagonal.conj().T @ mapped @ diagonal
                    off_diagonal = aligned - np.diag(np.diag(aligned))
                    reference_off = reference - np.diag(np.diag(reference))
                    objective = float(
                        np.linalg.norm(off_diagonal - reference_off, ord="fro")
                    )
                    diagonal_difference = np.real(np.diag(aligned - reference))
                    records.append(
                        {
                            "operation": operation.identifier,
                            "translation": cast(JsonValue, [tx, ty]),
                            "transformed_twist_lift": cast(
                                JsonValue, list(transformed)
                            ),
                            "comparison_twist": cast(JsonValue, list(comparison_twist)),
                            "integer_lift": cast(JsonValue, list(integer_lift)),
                            "objective": objective,
                            "energy_shift_diagnostic": float(
                                np.median(diagonal_difference)
                            ),
                        }
                    )
        typed_records = [cast(dict[str, JsonValue], record) for record in records]
        minimum = min(
            (cast(float, record["objective"]) for record in typed_records),
            default=float("inf"),
        )
        ambiguity = [
            record
            for record in typed_records
            if cast(float, record["objective"]) <= minimum + controls.tie_tolerance
        ]
        shifts = [
            cast(float, record["energy_shift_diagnostic"]) for record in ambiguity
        ]
        return {
            "issue_code": "DEFECT_2D.SITE_MAP_UNRESOLVED",
            "candidate_count": len(records),
            "candidates": records,
            "minimum_objective": minimum,
            "ambiguity_count": len(ambiguity),
            "ambiguity_set": cast(JsonValue, ambiguity),
            "common_shift_median": float(np.median(np.asarray(shifts))),
            "common_shift_maximum_deviation": max(
                (abs(value - float(np.median(np.asarray(shifts)))) for value in shifts),
                default=0.0,
            ),
            "selected_map": None,
            "extracted_operator": None,
        }

    @staticmethod
    def _compatible(
        route: str, left: FloatPair, right: FloatPair, tolerance: float
    ) -> bool:
        if route == "A_centered_uniform":
            return all(
                abs(a - b) <= tolerance for a, b in zip(left, right, strict=True)
            )
        return all(
            min(abs(a - b + shift) for shift in (-1.0, 0.0, 1.0)) <= tolerance
            for a, b in zip(left, right, strict=True)
        )

    @staticmethod
    def _connected(matrix: ComplexMatrix, tolerance: float) -> bool:
        dimension = int(matrix.shape[0])
        visited = {0}
        queue = [0]
        while queue:
            source = queue.pop(0)
            for target in range(dimension):
                if (
                    target not in visited
                    and source != target
                    and abs(matrix[source, target]) > tolerance
                ):
                    visited.add(target)
                    queue.append(target)
        return len(visited) == dimension

    @staticmethod
    def _phases(
        reference: ComplexMatrix, mapped: ComplexMatrix, tolerance: float
    ) -> npt.NDArray[np.complex128]:
        phases = np.zeros(reference.shape[0], dtype=np.complex128)
        phases[0] = 1.0
        queue = [0]
        while queue:
            source = queue.pop(0)
            for target in range(reference.shape[0]):
                if source == target or abs(reference[source, target]) <= tolerance:
                    continue
                if abs(mapped[source, target]) <= tolerance:
                    continue
                ratio = reference[source, target] / mapped[source, target]
                ratio /= abs(ratio)
                proposal = phases[source] * ratio
                if phases[target] == 0.0:
                    phases[target] = proposal
                    queue.append(target)
        if np.any(phases == 0.0):
            raise ValueError("DEFECT_2D.PHASE_GRAPH_DISCONNECTED")
        return phases / np.abs(phases)


class StageBMultiRouteStudy:
    """Execute two routes, their bridge, and both order schedules."""

    __slots__ = ("_blind", "_matrix", "_parent_validator")

    def __init__(self) -> None:
        self._matrix = StageBMatrixActions()
        self._blind = StageBBlindAlignment()
        self._parent_validator = StageBParentValidator()

    def execute(
        self, controls: StageBControls, hoppings: tuple[Hopping, ...]
    ) -> dict[str, JsonValue]:
        parent_checks = self._parent_validator.execute(controls, hoppings)
        schedule_ab = self._schedule_in_fresh_process(
            controls, hoppings, ("A", "B"), "A_then_B"
        )
        schedule_ba = self._schedule_in_fresh_process(
            controls, hoppings, ("B", "A"), "B_then_A"
        )
        order_comparison = self._compare_schedules(schedule_ab, schedule_ba)
        criteria = self._criteria(controls, schedule_ab, schedule_ba, order_comparison)
        return {
            "parent_checks": parent_checks,
            "inventory": {
                "execution_schedules": 2,
                "matrix_routes": 2,
                "known_map_route_evaluations": 72,
                "matched_bridge_records": 36,
                "blind_candidate_evaluations": 2304,
                "known_case_order_comparisons": 36,
                "bridge_order_comparisons": 18,
                "blind_summary_order_comparisons": 6,
            },
            "input_hoppings": cast(
                JsonValue,
                [
                    {
                        "rx": hopping.rx,
                        "ry": hopping.ry,
                        "real": float(hopping.value.real),
                        "imag": float(hopping.value.imag),
                    }
                    for hopping in hoppings
                ],
            ),
            "schedules": cast(JsonValue, [schedule_ab, schedule_ba]),
            "order_comparison": order_comparison,
            "criterion_evaluation": criteria,
        }

    def _schedule_in_fresh_process(
        self,
        controls: StageBControls,
        hoppings: tuple[Hopping, ...],
        order: tuple[str, str],
        identifier: str,
    ) -> dict[str, JsonValue]:
        context = get_context("spawn")
        receiver, sender = context.Pipe(duplex=False)
        process = context.Process(
            target=_stage_b_schedule_process,
            args=(sender, controls, hoppings, order, identifier),
        )
        process.start()
        sender.close()
        if not receiver.poll(120.0):
            process.terminate()
            process.join()
            raise TimeoutError(f"Stage B schedule {identifier} exceeded 120 seconds")
        encoded = receiver.recv_bytes()
        receiver.close()
        process.join()
        if process.exitcode != 0:
            raise RuntimeError(
                f"Stage B schedule {identifier} exited with {process.exitcode}"
            )
        decoded = cast(JsonValue, json.loads(encoded.decode("utf-8")))
        if not isinstance(decoded, dict):
            raise TypeError("Stage B schedule process returned a non-object")
        error = decoded.get("process_error")
        if isinstance(error, str):
            raise RuntimeError(f"Stage B schedule {identifier} failed: {error}")
        return decoded

    def _schedule(
        self,
        controls: StageBControls,
        hoppings: tuple[Hopping, ...],
        order: tuple[str, str],
        identifier: str,
    ) -> dict[str, JsonValue]:
        route_records: dict[str, JsonValue] = {}
        route_matrices: dict[
            str,
            dict[
                str, tuple[ComplexMatrix, ComplexMatrix, ComplexMatrix, ComplexMatrix]
            ],
        ] = {}
        for route_code in order:
            route_name = "A_centered_uniform" if route_code == "A" else "B_reduced_seam"
            records, matrices = self._route(controls, hoppings, route_name)
            route_records[route_name] = records
            route_matrices[route_name] = matrices
        bridges = self._bridges(
            controls,
            route_matrices["A_centered_uniform"],
            route_matrices["B_reduced_seam"],
        )
        blind_bridges = self._blind_bridges(route_records)
        return {
            "schedule_id": identifier,
            "execution_order": cast(JsonValue, list(order)),
            "routes": route_records,
            "bridges": cast(JsonValue, bridges),
            "blind_bridges": cast(JsonValue, blind_bridges),
        }

    def _route(
        self,
        controls: StageBControls,
        hoppings: tuple[Hopping, ...],
        route: str,
    ) -> tuple[
        dict[str, JsonValue],
        dict[str, tuple[ComplexMatrix, ComplexMatrix, ComplexMatrix, ComplexMatrix]],
    ]:
        known: list[JsonValue] = []
        matrices: dict[
            str, tuple[ComplexMatrix, ComplexMatrix, ComplexMatrix, ComplexMatrix]
        ] = {}
        identity_operation = controls.operations[0]
        for twist_id, twist in zip(("gamma", "generic"), controls.twists, strict=True):
            record, retained = self._known_case(
                controls,
                hoppings,
                route,
                controls.central,
                identity_operation,
                twist_id,
                twist,
            )
            known.append(record)
            matrices[cast(str, record["case_id"])] = retained
        for twist_id, twist in zip(("gamma", "generic"), controls.twists, strict=True):
            base = self._canonical(
                controls, hoppings, route, controls.off_axis, identity_operation, twist
            )
            for operation in controls.operations:
                record, retained = self._known_case(
                    controls,
                    hoppings,
                    route,
                    controls.off_axis,
                    operation,
                    twist_id,
                    twist,
                )
                target_hdef = retained[2]
                if route == "A_centered_uniform":
                    symmetry = self._matrix.permutation(controls, operation.matrix)
                else:
                    base_gauge = self._matrix.site_gauge(controls, twist)
                    transformed_lift = self._matrix.transformed_twist(
                        twist, operation.matrix
                    )
                    target_gauge = self._matrix.site_gauge(controls, transformed_lift)
                    symmetry = (
                        target_gauge
                        @ self._matrix.permutation(controls, operation.matrix)
                        @ base_gauge.conj().T
                    )
                covariance_difference = (
                    target_hdef - symmetry @ base[2] @ symmetry.conj().T
                )
                record["covariance"] = {
                    "maximum_absolute": self._matrix.maximum(covariance_difference),
                    "frobenius": float(
                        np.linalg.norm(covariance_difference, ord="fro")
                    ),
                    "eigenvalue_maximum_absolute": float(
                        np.max(
                            np.abs(
                                np.sort(np.linalg.eigvalsh(target_hdef))
                                - np.sort(np.linalg.eigvalsh(base[2]))
                            )
                        )
                    ),
                }
                known.append(record)
                matrices[cast(str, record["case_id"])] = retained
        blind_records: list[JsonValue] = []
        for twist_id, twist in zip(("gamma", "generic"), controls.twists, strict=True):
            pristine, _, hdef = self._canonical(
                controls, hoppings, route, controls.off_axis, identity_operation, twist
            )
            attack = self._matrix.attack(controls)
            identity = np.eye(controls.nx * controls.ny, dtype=np.complex128)
            candidate = (
                attack @ hdef @ attack.conj().T + controls.energy_shift * identity
            )
            candidate_lift = self._matrix.transformed_twist(
                twist, controls.attack_matrix
            )
            reference_metadata = (
                twist
                if route == "A_centered_uniform"
                else self._matrix.reduced_twist(twist)
            )
            candidate_metadata = (
                candidate_lift
                if route == "A_centered_uniform"
                else self._matrix.reduced_twist(candidate_lift)
            )
            blind = self._blind.execute(
                controls,
                route,
                pristine,
                candidate,
                reference_metadata,
                candidate_metadata,
            )
            blind["case_id"] = f"blind__{twist_id}"
            blind["reference_twist"] = cast(JsonValue, list(reference_metadata))
            blind["candidate_twist"] = cast(JsonValue, list(candidate_metadata))
            blind_records.append(blind)
        adverse = self._adverse(controls, hoppings, route)
        return (
            {
                "route_id": route,
                "known_map_cases": known,
                "blind_cases": blind_records,
                "adverse_controls": adverse,
            },
            matrices,
        )

    def _canonical(
        self,
        controls: StageBControls,
        hoppings: tuple[Hopping, ...],
        route: str,
        plant: Plant,
        operation: D4Operation,
        base_twist: FloatPair,
    ) -> tuple[ComplexMatrix, ComplexMatrix, ComplexMatrix]:
        twist_lift = self._matrix.transformed_twist(base_twist, operation.matrix)
        pristine = (
            self._matrix.uniform(controls, hoppings, twist_lift)
            if route == "A_centered_uniform"
            else self._matrix.seam(
                controls, hoppings, self._matrix.reduced_twist(twist_lift)
            )
        )
        site = self._matrix.affine_site(controls, operation.matrix, plant.site, (0, 0))
        planted = self._matrix.plant(controls, site, plant.strength)
        return pristine, planted, pristine + planted

    def _known_case(
        self,
        controls: StageBControls,
        hoppings: tuple[Hopping, ...],
        route: str,
        plant: Plant,
        operation: D4Operation,
        twist_id: str,
        base_twist: FloatPair,
    ) -> tuple[
        dict[str, JsonValue],
        tuple[ComplexMatrix, ComplexMatrix, ComplexMatrix, ComplexMatrix],
    ]:
        pristine, planted, hdef = self._canonical(
            controls, hoppings, route, plant, operation, base_twist
        )
        attack = self._matrix.attack(controls)
        identity = np.eye(controls.nx * controls.ny, dtype=np.complex128)
        candidate = attack @ hdef @ attack.conj().T + controls.energy_shift * identity
        recovered = (
            attack.conj().T @ (candidate - controls.energy_shift * identity) @ attack
            - pristine
        )
        difference = recovered - planted
        support_rows, support_columns = np.where(
            np.abs(recovered) > controls.algebraic_tolerance
        )
        support = [
            [int(row), int(column)]
            for row, column in zip(support_rows, support_columns, strict=True)
        ]
        twist_lift = self._matrix.transformed_twist(base_twist, operation.matrix)
        reduced = self._matrix.reduced_twist(twist_lift)
        integer_lift = [
            int(round(twist_lift[index] - reduced[index])) for index in range(2)
        ]
        site = self._matrix.affine_site(controls, operation.matrix, plant.site, (0, 0))
        index = site[0] * controls.ny + site[1]
        case_id = (
            f"central__{twist_id}"
            if plant.identifier == "central"
            else f"off_axis__{twist_id}__{operation.identifier}"
        )
        return (
            {
                "case_id": case_id,
                "plant_id": plant.identifier,
                "operation": operation.identifier,
                "twist_lift": cast(JsonValue, list(twist_lift)),
                "reduced_twist": cast(JsonValue, list(reduced)),
                "integer_lift": cast(JsonValue, integer_lift),
                "support_site": cast(JsonValue, list(site)),
                "pristine_sha256": self._matrix.matrix_sha256(pristine),
                "planted_sha256": self._matrix.matrix_sha256(planted),
                "candidate_sha256": self._matrix.matrix_sha256(candidate),
                "recovered_sha256": self._matrix.matrix_sha256(recovered),
                "hermiticity_maximum_absolute": self._matrix.maximum(
                    recovered - recovered.conj().T
                ),
                "recovery_maximum_absolute": self._matrix.maximum(difference),
                "recovery_frobenius": float(np.linalg.norm(difference, ord="fro")),
                "support": cast(JsonValue, support),
                "support_exact": support == [[index, index]],
                "amplitude_real": float(recovered[index, index].real),
                "amplitude_imag": float(recovered[index, index].imag),
                "amplitude_absolute_defect": float(
                    abs(recovered[index, index] - plant.strength)
                ),
                "covariance": None,
            },
            (pristine, planted, hdef, candidate),
        )

    def _bridges(
        self,
        controls: StageBControls,
        route_a: dict[
            str, tuple[ComplexMatrix, ComplexMatrix, ComplexMatrix, ComplexMatrix]
        ],
        route_b: dict[
            str, tuple[ComplexMatrix, ComplexMatrix, ComplexMatrix, ComplexMatrix]
        ],
    ) -> list[JsonValue]:
        attack = self._matrix.attack(controls)
        identity = np.eye(controls.nx * controls.ny, dtype=np.complex128)
        result: list[JsonValue] = []
        for case_id in route_a:
            operation = self._operation_for_case(controls, case_id)
            base_twist = (
                controls.twists[1] if "generic" in case_id else controls.twists[0]
            )
            twist_lift = self._matrix.transformed_twist(base_twist, operation.matrix)
            gauge = self._matrix.site_gauge(controls, twist_lift)
            attacked_gauge = attack @ gauge @ attack.conj().T
            a_pristine, a_plant, a_hdef, a_candidate = route_a[case_id]
            b_pristine, b_plant, b_hdef, b_candidate = route_b[case_id]
            canonical = b_hdef - gauge @ a_hdef @ gauge.conj().T
            attacked = (b_candidate - controls.energy_shift * identity) - (
                attacked_gauge
                @ (a_candidate - controls.energy_shift * identity)
                @ attacked_gauge.conj().T
            )
            result.append(
                {
                    "case_id": case_id,
                    "canonical_maximum_absolute": self._matrix.maximum(canonical),
                    "canonical_frobenius": float(np.linalg.norm(canonical, ord="fro")),
                    "attacked_maximum_absolute": self._matrix.maximum(attacked),
                    "attacked_frobenius": float(np.linalg.norm(attacked, ord="fro")),
                    "plant_maximum_absolute": self._matrix.maximum(b_plant - a_plant),
                    "pristine_eigenvalue_maximum_absolute": float(
                        np.max(
                            np.abs(
                                np.sort(np.linalg.eigvalsh(b_pristine))
                                - np.sort(np.linalg.eigvalsh(a_pristine))
                            )
                        )
                    ),
                }
            )
        return result

    @staticmethod
    def _blind_bridges(route_records: dict[str, JsonValue]) -> list[JsonValue]:
        route_a = cast(dict[str, JsonValue], route_records["A_centered_uniform"])
        route_b = cast(dict[str, JsonValue], route_records["B_reduced_seam"])
        result: list[JsonValue] = []
        for a_value, b_value in zip(
            cast(list[JsonValue], route_a["blind_cases"]),
            cast(list[JsonValue], route_b["blind_cases"]),
            strict=True,
        ):
            a_record = cast(dict[str, JsonValue], a_value)
            b_record = cast(dict[str, JsonValue], b_value)
            a_maps = [
                {
                    "operation": cast(dict[str, JsonValue], value)["operation"],
                    "translation": cast(dict[str, JsonValue], value)["translation"],
                }
                for value in cast(list[JsonValue], a_record["ambiguity_set"])
            ]
            b_maps = [
                {
                    "operation": cast(dict[str, JsonValue], value)["operation"],
                    "translation": cast(dict[str, JsonValue], value)["translation"],
                }
                for value in cast(list[JsonValue], b_record["ambiguity_set"])
            ]
            result.append(
                {
                    "case_id": a_record["case_id"],
                    "same_ordered_map_identities": a_maps == b_maps,
                    "same_disposition": a_record["issue_code"]
                    == b_record["issue_code"],
                    "shift_median_absolute_difference": abs(
                        cast(float, a_record["common_shift_median"])
                        - cast(float, b_record["common_shift_median"])
                    ),
                }
            )
        return result

    def _adverse(
        self,
        controls: StageBControls,
        hoppings: tuple[Hopping, ...],
        route: str,
    ) -> dict[str, JsonValue]:
        identity_operation = controls.operations[0]
        quarter = controls.operations[1]
        twist = controls.twists[1]
        base = self._canonical(
            controls, hoppings, route, controls.off_axis, identity_operation, twist
        )[2]
        target = self._canonical(
            controls, hoppings, route, controls.off_axis, quarter, twist
        )[2]
        wrong_pristine = (
            self._matrix.uniform(controls, hoppings, twist)
            if route == "A_centered_uniform"
            else self._matrix.seam(
                controls, hoppings, self._matrix.reduced_twist(twist)
            )
        )
        wrong_site = self._matrix.affine_site(
            controls, quarter.matrix, controls.off_axis.site, (0, 0)
        )
        wrong = wrong_pristine + self._matrix.plant(
            controls, wrong_site, controls.off_axis.strength
        )
        if route == "A_centered_uniform":
            symmetry = self._matrix.permutation(controls, quarter.matrix)
        else:
            target_lift = self._matrix.transformed_twist(twist, quarter.matrix)
            symmetry = (
                self._matrix.site_gauge(controls, target_lift)
                @ self._matrix.permutation(controls, quarter.matrix)
                @ self._matrix.site_gauge(controls, twist).conj().T
            )
        rotated = symmetry @ base @ symmetry.conj().T
        omitted_maximum = abs(controls.energy_shift)
        omitted_frobenius = np.sqrt(float(controls.nx * controls.ny)) * omitted_maximum
        return {
            "prealignment": {
                "issue_code": "DEFECT_2D.SITE_MAP_UNRESOLVED",
                "residual": None,
            },
            "omitted_shift": {
                "maximum_absolute": omitted_maximum,
                "frobenius": omitted_frobenius,
            },
            "fixed_twist": {
                "correct_maximum_absolute": self._matrix.maximum(target - rotated),
                "adverse_maximum_absolute": self._matrix.maximum(wrong - rotated),
            },
            "blind_information_boundary": {
                "plant_fields_present": False,
                "known_map_fields_present": False,
            },
        }

    def _compare_schedules(
        self,
        first: dict[str, JsonValue],
        second: dict[str, JsonValue],
    ) -> dict[str, JsonValue]:
        first_routes = cast(dict[str, JsonValue], first["routes"])
        second_routes = cast(dict[str, JsonValue], second["routes"])
        route_comparisons: list[JsonValue] = []
        for route_id in ("A_centered_uniform", "B_reduced_seam"):
            left = cast(dict[str, JsonValue], first_routes[route_id])
            right = cast(dict[str, JsonValue], second_routes[route_id])
            left_cases = cast(list[JsonValue], left["known_map_cases"])
            right_cases = cast(list[JsonValue], right["known_map_cases"])
            for left_case_value, right_case_value in zip(
                left_cases, right_cases, strict=True
            ):
                left_case = cast(dict[str, JsonValue], left_case_value)
                right_case = cast(dict[str, JsonValue], right_case_value)
                route_comparisons.append(
                    {
                        "route_id": route_id,
                        "case_id": left_case["case_id"],
                        "same_recovered_sha256": (
                            left_case["recovered_sha256"]
                            == right_case["recovered_sha256"]
                        ),
                        "recovery_maximum_difference": abs(
                            cast(float, left_case["recovery_maximum_absolute"])
                            - cast(float, right_case["recovery_maximum_absolute"])
                        ),
                    }
                )
        bridge_comparisons: list[JsonValue] = []
        for left_value, right_value in zip(
            cast(list[JsonValue], first["bridges"]),
            cast(list[JsonValue], second["bridges"]),
            strict=True,
        ):
            left = cast(dict[str, JsonValue], left_value)
            right = cast(dict[str, JsonValue], right_value)
            bridge_comparisons.append(
                {
                    "case_id": left["case_id"],
                    "canonical_maximum_difference": abs(
                        cast(float, left["canonical_maximum_absolute"])
                        - cast(float, right["canonical_maximum_absolute"])
                    ),
                    "attacked_maximum_difference": abs(
                        cast(float, left["attacked_maximum_absolute"])
                        - cast(float, right["attacked_maximum_absolute"])
                    ),
                }
            )
        blind_comparisons: list[JsonValue] = []
        for route_id in ("A_centered_uniform", "B_reduced_seam"):
            left_route = cast(dict[str, JsonValue], first_routes[route_id])
            right_route = cast(dict[str, JsonValue], second_routes[route_id])
            for left_value, right_value in zip(
                cast(list[JsonValue], left_route["blind_cases"]),
                cast(list[JsonValue], right_route["blind_cases"]),
                strict=True,
            ):
                left = cast(dict[str, JsonValue], left_value)
                right = cast(dict[str, JsonValue], right_value)
                blind_comparisons.append(
                    {
                        "route_id": route_id,
                        "case_id": left["case_id"],
                        "same_ambiguity_set": left["ambiguity_set"]
                        == right["ambiguity_set"],
                        "same_disposition": left["issue_code"] == right["issue_code"],
                    }
                )
        for left_value, right_value in zip(
            cast(list[JsonValue], first["blind_bridges"]),
            cast(list[JsonValue], second["blind_bridges"]),
            strict=True,
        ):
            left = cast(dict[str, JsonValue], left_value)
            right = cast(dict[str, JsonValue], right_value)
            blind_comparisons.append(
                {
                    "route_id": "cross_route_bridge",
                    "case_id": left["case_id"],
                    "same_ambiguity_set": left["same_ordered_map_identities"]
                    == right["same_ordered_map_identities"],
                    "same_disposition": left["same_disposition"]
                    == right["same_disposition"],
                }
            )
        return {
            "known_case_comparisons": route_comparisons,
            "bridge_comparisons": bridge_comparisons,
            "blind_comparisons": blind_comparisons,
        }

    def _criteria(
        self,
        controls: StageBControls,
        first: dict[str, JsonValue],
        second: dict[str, JsonValue],
        order: dict[str, JsonValue],
    ) -> dict[str, JsonValue]:
        failures: list[JsonValue] = []
        for schedule_index, schedule in enumerate((first, second)):
            routes = cast(dict[str, JsonValue], schedule["routes"])
            for route_id in ("A_centered_uniform", "B_reduced_seam"):
                route = cast(dict[str, JsonValue], routes[route_id])
                known = cast(list[JsonValue], route["known_map_cases"])
                if len(known) != 18:
                    failures.append(
                        f"schedule[{schedule_index}].{route_id}.known_inventory"
                    )
                for case_index, case_value in enumerate(known):
                    case = cast(dict[str, JsonValue], case_value)
                    for metric in (
                        "hermiticity_maximum_absolute",
                        "recovery_maximum_absolute",
                        "recovery_frobenius",
                        "amplitude_absolute_defect",
                    ):
                        if cast(float, case[metric]) > controls.algebraic_tolerance:
                            failures.append(
                                f"schedule[{schedule_index}].{route_id}.known[{case_index}].{metric}"
                            )
                    if case["support_exact"] is not True:
                        failures.append(
                            f"schedule[{schedule_index}].{route_id}.known[{case_index}].support"
                        )
                    covariance_value = case["covariance"]
                    if covariance_value is not None:
                        covariance = cast(dict[str, JsonValue], covariance_value)
                        if (
                            cast(float, covariance["maximum_absolute"])
                            > controls.covariance_tolerance
                        ):
                            failures.append(
                                f"schedule[{schedule_index}].{route_id}.known[{case_index}].covariance"
                            )
                blind = cast(list[JsonValue], route["blind_cases"])
                expected = (
                    controls.expected_gamma_count,
                    controls.expected_generic_count,
                )
                if len(blind) != 2:
                    failures.append(
                        f"schedule[{schedule_index}].{route_id}.blind_inventory"
                    )
                for blind_index, (record_value, expected_count) in enumerate(
                    zip(blind, expected, strict=True)
                ):
                    record = cast(dict[str, JsonValue], record_value)
                    if record["ambiguity_count"] != expected_count:
                        failures.append(
                            f"schedule[{schedule_index}].{route_id}.blind[{blind_index}].ambiguity"
                        )
                    if (
                        record["selected_map"] is not None
                        or record["extracted_operator"] is not None
                    ):
                        failures.append(
                            f"schedule[{schedule_index}].{route_id}.blind[{blind_index}].payload"
                        )
                adverse = cast(dict[str, JsonValue], route["adverse_controls"])
                fixed = cast(dict[str, JsonValue], adverse["fixed_twist"])
                if (
                    cast(float, fixed["correct_maximum_absolute"])
                    > controls.covariance_tolerance
                ):
                    failures.append(
                        f"schedule[{schedule_index}].{route_id}.adverse.correct_twist"
                    )
                if (
                    cast(float, fixed["adverse_maximum_absolute"])
                    < controls.adverse_floor
                ):
                    failures.append(
                        f"schedule[{schedule_index}].{route_id}.adverse.discrimination"
                    )
            blind_bridges = cast(list[JsonValue], schedule["blind_bridges"])
            if len(blind_bridges) != 2:
                failures.append(f"schedule[{schedule_index}].blind_bridge_inventory")
            for bridge_index, bridge_value in enumerate(blind_bridges):
                blind_bridge = cast(dict[str, JsonValue], bridge_value)
                if blind_bridge["same_ordered_map_identities"] is not True:
                    failures.append(
                        f"schedule[{schedule_index}].blind_bridge[{bridge_index}].maps"
                    )
                if blind_bridge["same_disposition"] is not True:
                    failures.append(
                        f"schedule[{schedule_index}].blind_bridge[{bridge_index}].disposition"
                    )
                if (
                    cast(float, blind_bridge["shift_median_absolute_difference"])
                    > controls.route_tolerance
                ):
                    failures.append(
                        f"schedule[{schedule_index}].blind_bridge[{bridge_index}].shift"
                    )
            bridges = cast(list[JsonValue], schedule["bridges"])
            if len(bridges) != 18:
                failures.append(f"schedule[{schedule_index}].bridge_inventory")
            for bridge_index, bridge_value in enumerate(bridges):
                bridge = cast(dict[str, JsonValue], bridge_value)
                for metric in (
                    "canonical_maximum_absolute",
                    "attacked_maximum_absolute",
                    "plant_maximum_absolute",
                    "pristine_eigenvalue_maximum_absolute",
                ):
                    if cast(float, bridge[metric]) > controls.route_tolerance:
                        failures.append(
                            f"schedule[{schedule_index}].bridge[{bridge_index}].{metric}"
                        )
        for index, value in enumerate(
            cast(list[JsonValue], order["known_case_comparisons"])
        ):
            record = cast(dict[str, JsonValue], value)
            if record["same_recovered_sha256"] is not True:
                failures.append(f"order.known[{index}].digest")
        for index, value in enumerate(
            cast(list[JsonValue], order["blind_comparisons"])
        ):
            record = cast(dict[str, JsonValue], value)
            if (
                record["same_ambiguity_set"] is not True
                or record["same_disposition"] is not True
            ):
                failures.append(f"order.blind[{index}]")
        return {
            "status": "pass" if not failures else "fail",
            "failed_criteria": failures,
        }

    @staticmethod
    def _operation_for_case(controls: StageBControls, case_id: str) -> D4Operation:
        if case_id.startswith("central"):
            return controls.operations[0]
        identifier = case_id.rsplit("__", maxsplit=1)[-1]
        for operation in controls.operations:
            if operation.identifier == identifier:
                return operation
        raise ValueError(f"unknown case operation in {case_id}")


def _stage_b_schedule_process(
    sender: Connection,
    controls: StageBControls,
    hoppings: tuple[Hopping, ...],
    order: tuple[str, str],
    identifier: str,
) -> None:
    """Adapt a spawned-process boundary to one isolated schedule calculation."""

    try:
        payload = StageBMultiRouteStudy()._schedule(
            controls, hoppings, order, identifier
        )
        encoded = json.dumps(payload, sort_keys=True).encode("utf-8")
    except Exception as error:
        encoded = json.dumps(
            {"process_error": f"{type(error).__name__}: {error}"}, sort_keys=True
        ).encode("utf-8")
    sender.send_bytes(encoded)
    sender.close()


class StageBResultSerializer:
    """Serialize canonical data-complete output without overwrite."""

    __slots__ = ()

    @staticmethod
    def payload(
        controls: StageBControls,
        study: dict[str, JsonValue],
        provenance: dict[str, JsonValue],
    ) -> dict[str, JsonValue]:
        return {
            "schema_version": 1,
            "design_id": controls.design_id,
            "stage_id": "B_scalar_onsite_and_D4_multiroute",
            "evidence_status": "calculated synthetic numerical-verification result",
            "provenance": provenance,
            "controls": {
                "shape": [controls.nx, controls.ny],
                "twists": cast(JsonValue, [list(value) for value in controls.twists]),
                "algebraic_tolerance": controls.algebraic_tolerance,
                "covariance_tolerance": controls.covariance_tolerance,
                "route_tolerance": controls.route_tolerance,
                "tie_tolerance": controls.tie_tolerance,
                "twist_tolerance": controls.twist_tolerance,
                "adverse_floor": controls.adverse_floor,
            },
            **study,
            "limitations": [
                "The result concerns one synthetic 8x8 scalar represented parent.",
                (
                    "Order sensitivity is a software/protocol failure, not a "
                    "physical effect."
                ),
                (
                    "No directional, nonlocal, finite-size, material, validation, "
                    "or UQ claim is made."
                ),
            ],
        }

    @staticmethod
    def write(
        path: Path,
        payload: dict[str, JsonValue],
        maximum_bytes: int | None = None,
    ) -> None:
        if path.exists():
            raise FileExistsError(f"refusing to overwrite {path}")
        encoded = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
        if maximum_bytes is not None and len(encoded) > maximum_bytes:
            raise ValueError("serialized result exceeds the authorized output bound")
        path.write_bytes(encoded)


class StageBOrderAdverseToy:
    """Demonstrate schedule sensitivity from a deliberately shared twist cache."""

    __slots__ = ("_matrix",)

    def __init__(self) -> None:
        self._matrix = StageBMatrixActions()

    def execute(
        self, controls: StageBControls, hoppings: tuple[Hopping, ...]
    ) -> dict[str, JsonValue]:
        lift = controls.twists[1]
        reduced = self._matrix.reduced_twist(lift)
        gauge = self._matrix.site_gauge(controls, lift)
        clean_a = self._matrix.uniform(controls, hoppings, lift)
        clean_b = self._matrix.seam(controls, hoppings, reduced)
        clean_bridge = clean_b - gauge @ clean_a @ gauge.conj().T
        mutated_a_then_b_a = clean_a
        mutated_a_then_b_b = self._matrix.seam(controls, hoppings, lift)
        mutated_b_then_a_b = clean_b
        mutated_b_then_a_a = self._matrix.uniform(controls, hoppings, reduced)
        mutated_bridge = (
            mutated_b_then_a_b - gauge @ mutated_b_then_a_a @ gauge.conj().T
        )
        return {
            "status": "synthetic test data",
            "mutation": (
                "the first route writes its twist representative into a shared "
                "cache and the second route consumes it"
            ),
            "clean_bridge_maximum_absolute": self._matrix.maximum(clean_bridge),
            "clean_schedule_route_A_maximum_absolute": 0.0,
            "clean_schedule_route_B_maximum_absolute": 0.0,
            "mutated_schedule_route_A_maximum_absolute": self._matrix.maximum(
                mutated_a_then_b_a - mutated_b_then_a_a
            ),
            "mutated_schedule_route_B_maximum_absolute": self._matrix.maximum(
                mutated_a_then_b_b - mutated_b_then_a_b
            ),
            "mutated_B_then_A_bridge_maximum_absolute": self._matrix.maximum(
                mutated_bridge
            ),
            "interpretation": (
                "the mutation is discriminating; any clean schedule effect is a "
                "software or protocol failure, not a physical result"
            ),
        }


class StageBExecutionFreeToy:
    """Produce authored toy behavioral data without accepted-parent inputs."""

    __slots__ = ("_study",)

    def __init__(self) -> None:
        self._study = StageBMultiRouteStudy()

    def execute(self, output_path: Path) -> None:
        controls = StageBControls.authored_toy()
        hoppings = (
            Hopping(0, 0, 4.0 + 0.0j),
            Hopping(1, 0, -1.0 + 0.0j),
            Hopping(-1, 0, -1.0 + 0.0j),
            Hopping(0, 1, -1.0 + 0.0j),
            Hopping(0, -1, -1.0 + 0.0j),
        )
        study = self._study.execute(controls, hoppings)
        study["execution_free_order_adverse"] = StageBOrderAdverseToy().execute(
            controls, hoppings
        )
        provenance: dict[str, JsonValue] = {
            "evidence_status": "synthetic test data",
            "accepted_parent_read": False,
            "accepted_stage_a_result_read": False,
            "python_version": platform.python_version(),
            "numpy_version": np.__version__,
        }
        StageBResultSerializer.write(
            output_path,
            StageBResultSerializer.payload(controls, study, provenance),
        )


class StageBRunner:
    """Validate future exact authority before reading the accepted parent."""

    __slots__ = ("_deserializer", "_json", "_study")

    def __init__(self) -> None:
        self._deserializer = StageBInputDeserializer()
        self._json = ClosedJsonReader()
        self._study = StageBMultiRouteStudy()

    def execute(
        self,
        design_path: Path,
        authorization_path: Path,
        repository_root: Path,
        output_path: Path,
    ) -> None:
        root = repository_root.resolve(strict=True)
        if not repository_root.is_absolute() or root != repository_root:
            raise ValueError("repository_root must be canonical and absolute")
        design = self._existing(root, design_path)
        design_relative = (
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-b-multiroute-design.json"
        )
        expected_design = (root / design_relative).resolve(strict=True)
        if design != expected_design:
            raise ValueError("design path is not the authoritative multi-route design")
        output = self._output(root, output_path)
        if output.exists():
            raise FileExistsError(f"refusing to overwrite {output}")
        authorization_path = self._existing(root, authorization_path)
        controls = self._deserializer.controls(design)
        authorization = self._deserializer.authorization(authorization_path)
        runner = Path(__file__).resolve(strict=True)
        verifier = (runner.parent / "verify_stage_b.py").resolve(strict=True)
        plotter = (runner.parent / "plot_stage_b.py").resolve(strict=True)
        result_schema = (runner.parent / "stage-b-result.schema.json").resolve(
            strict=True
        )
        native_manifest = (
            runner.parent / "stage-b-native-evidence-manifest.json"
        ).resolve(strict=True)
        parent_input = self._bound_existing(
            root, authorization.parent_input_path, "parent_input_path"
        )
        parent = self._bound_existing(root, authorization.parent_path, "parent_path")
        stage_a = self._bound_existing(
            root, authorization.stage_a_result_path, "stage_a_result_path"
        )
        checkpoint = self._bound_existing(
            root, authorization.checkpoint_path, "checkpoint_path"
        )
        authority_bindings = (
            (authorization.design_path, design, authorization.design_sha256),
            (authorization.runner_path, runner, authorization.runner_sha256),
            (authorization.verifier_path, verifier, authorization.verifier_sha256),
            (authorization.plotter_path, plotter, authorization.plotter_sha256),
            (
                authorization.result_schema_path,
                result_schema,
                authorization.result_schema_sha256,
            ),
            (
                authorization.native_manifest_path,
                native_manifest,
                authorization.native_manifest_sha256,
            ),
            (
                authorization.checkpoint_path,
                checkpoint,
                authorization.checkpoint_sha256,
            ),
        )
        if authorization.repository_root != str(root):
            raise ValueError("authorization repository root differs")
        for represented, actual, digest in authority_bindings:
            if (
                self._bound_existing(root, represented, "authorization binding")
                != actual
            ):
                raise ValueError(f"authorization path differs for {actual}")
            if self._sha256(actual) != digest:
                raise ValueError(f"authorization digest differs for {actual}")
        if self._bound_output(root, authorization.output_path) != output:
            raise ValueError("authorization output differs")
        if authorization.network_access:
            raise ValueError("network access is not authorized")
        if authorization.maximum_matrix_dimension != 64:
            raise ValueError("matrix dimension authorization differs from the design")
        if authorization.maximum_execution_schedules != 2:
            raise ValueError("schedule authorization differs from the design")
        if authorization.maximum_known_map_route_evaluations != 72:
            raise ValueError("known-map authorization differs from the design")
        if authorization.maximum_total_blind_candidate_evaluations != 2304:
            raise ValueError("blind-candidate authorization differs from the design")
        if not 0 < authorization.maximum_runtime_seconds <= 600:
            raise ValueError("runtime authorization exceeds the design")
        if not 0.0 < authorization.maximum_peak_memory_gib <= 2.0:
            raise ValueError("memory authorization exceeds the design")
        if not 0.0 < authorization.maximum_retained_output_mib <= 30.0:
            raise ValueError("output authorization exceeds the design")
        checkpoint_record = self._json.read(checkpoint)
        if checkpoint_record.get("status") != "resolved":
            raise ValueError("execution checkpoint is not resolved")
        if (
            checkpoint_record.get("human_response")
            != authorization.human_response_verbatim
        ):
            raise ValueError("execution checkpoint response differs")
        if (
            checkpoint_record.get("task_id")
            != "research-monograph.exercises.impurity.defect-2d"
        ):
            raise ValueError("execution checkpoint task differs")
        allowed_execution_decisions = {
            "AUTHORIZE_EXACT_STAGE_B_MULTIROUTE_EXECUTION",
            "AUTHORIZE_ONE_CORRECTED_STAGE_B_RETRY",
            "AUTHORIZE_ONE_SCHEMA_CORRECTED_STAGE_B_ATTEMPT",
        }
        if checkpoint_record.get("normalized_decision") not in (
            allowed_execution_decisions
        ):
            raise ValueError("checkpoint does not authorize Stage B execution")
        data_bindings = (
            (
                authorization.parent_input_path,
                parent_input,
                authorization.parent_input_sha256,
            ),
            (authorization.parent_path, parent, authorization.parent_sha256),
            (
                authorization.stage_a_result_path,
                stage_a,
                authorization.stage_a_result_sha256,
            ),
        )
        for represented, actual, digest in data_bindings:
            if (
                self._bound_existing(root, represented, "authorization data binding")
                != actual
            ):
                raise ValueError(f"authorization data path differs for {actual}")
            if self._sha256(actual) != digest:
                raise ValueError(f"authorization data digest differs for {actual}")
        hoppings = self._deserializer.hoppings(parent, parent_input, 18)
        study = self._study.execute(controls, hoppings)
        provenance: dict[str, JsonValue] = {
            "authorization_id": authorization.authorization_id,
            "design_path": design.relative_to(root).as_posix(),
            "design_sha256": self._sha256(design),
            "runner_path": runner.relative_to(root).as_posix(),
            "runner_sha256": self._sha256(runner),
            "verifier_path": verifier.relative_to(root).as_posix(),
            "verifier_sha256": self._sha256(verifier),
            "plotter_path": plotter.relative_to(root).as_posix(),
            "plotter_sha256": self._sha256(plotter),
            "result_schema_path": result_schema.relative_to(root).as_posix(),
            "result_schema_sha256": self._sha256(result_schema),
            "native_manifest_path": native_manifest.relative_to(root).as_posix(),
            "native_manifest_sha256": self._sha256(native_manifest),
            "parent_input_path": parent_input.relative_to(root).as_posix(),
            "parent_input_sha256": self._sha256(parent_input),
            "parent_path": parent.relative_to(root).as_posix(),
            "parent_sha256": self._sha256(parent),
            "stage_a_result_path": stage_a.relative_to(root).as_posix(),
            "stage_a_result_sha256": self._sha256(stage_a),
            "authorization_path": authorization_path.relative_to(root).as_posix(),
            "authorization_sha256": self._sha256(authorization_path),
            "checkpoint_path": checkpoint.relative_to(root).as_posix(),
            "checkpoint_sha256": self._sha256(checkpoint),
            "python_version": platform.python_version(),
            "numpy_version": np.__version__,
        }
        StageBResultSerializer.write(
            output,
            StageBResultSerializer.payload(controls, study, provenance),
            maximum_bytes=int(
                authorization.maximum_retained_output_mib * 1024.0 * 1024.0
            ),
        )

    @staticmethod
    def _existing(root: Path, represented: Path) -> Path:
        candidate = represented if represented.is_absolute() else root / represented
        result = candidate.resolve(strict=True)
        if not result.is_relative_to(root):
            raise ValueError("path escapes repository root")
        return result

    @staticmethod
    def _output(root: Path, represented: Path) -> Path:
        candidate = represented if represented.is_absolute() else root / represented
        result = candidate.parent.resolve(strict=True) / candidate.name
        if not result.is_relative_to(root):
            raise ValueError("output escapes repository root")
        return result

    @staticmethod
    def _bound_existing(root: Path, represented: str, name: str) -> Path:
        path = Path(represented)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"{name} must be canonical repository-relative")
        result = (root / path).resolve(strict=True)
        if (
            not result.is_relative_to(root)
            or result.relative_to(root).as_posix() != represented
        ):
            raise ValueError(f"{name} is not canonical and confined")
        return result

    @staticmethod
    def _bound_output(root: Path, represented: str) -> Path:
        path = Path(represented)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError("output must be canonical repository-relative")
        result = (root / path).parent.resolve(strict=True) / path.name
        if (
            not result.is_relative_to(root)
            or result.relative_to(root).as_posix() != represented
        ):
            raise ValueError("output is not canonical and confined")
        return result

    @staticmethod
    def _sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    """Adapt the command line to toy evidence or the fail-closed runner."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--design", type=Path)
    parser.add_argument("--execution-authorization", type=Path)
    parser.add_argument("--repository-root", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--execution-free-toy-output", type=Path)
    arguments = parser.parse_args()
    if arguments.execution_free_toy_output is not None:
        if any(
            value is not None
            for value in (
                arguments.design,
                arguments.execution_authorization,
                arguments.repository_root,
                arguments.output,
            )
        ):
            parser.error("toy output cannot be combined with execution arguments")
        StageBExecutionFreeToy().execute(arguments.execution_free_toy_output)
        return
    if any(
        value is None
        for value in (
            arguments.design,
            arguments.execution_authorization,
            arguments.repository_root,
            arguments.output,
        )
    ):
        parser.error(
            "execution requires --design, --execution-authorization, "
            "--repository-root, and --output"
        )
    StageBRunner().execute(
        cast(Path, arguments.design),
        cast(Path, arguments.execution_authorization),
        cast(Path, arguments.repository_root),
        cast(Path, arguments.output),
    )


if __name__ == "__main__":
    main()
