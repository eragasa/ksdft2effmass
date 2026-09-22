#!/usr/bin/env python3
"""Run authorized Stage A of the controlled two-dimensional defect study."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type ComplexMatrix = npt.NDArray[np.complex128]


@dataclass(frozen=True, slots=True)
class Hopping:
    """One scalar parent hopping coefficient."""

    rx: int
    ry: int
    value: complex


@dataclass(frozen=True, slots=True)
class FoldingCase:
    """One frozen supercell and boundary-twist case."""

    nx: int
    ny: int
    phi_x: float
    phi_y: float


@dataclass(frozen=True, slots=True)
class SeamOracleControl:
    """Frozen analytical seam-phase control."""

    size: int
    twist: float
    noncrossing_source: int
    positive_crossing_source: int
    positive_displacement: int
    negative_crossing_source: int
    negative_displacement: int


@dataclass(frozen=True, slots=True)
class RepresentationMetadata:
    """Compatibility metadata checked before represented subtraction."""

    geometry: tuple[int, int]
    boundary_phase: tuple[float, float]
    site_map_known: bool
    energy_reference_relation_known: bool


@dataclass(frozen=True, slots=True)
class CompatibilityControl:
    """One frozen incompatible represented-comparison case."""

    control: str
    pristine: RepresentationMetadata
    candidate: RepresentationMetadata
    expected_issue_code: str


@dataclass(frozen=True, slots=True)
class StageAExecutionAuthorization:
    """Exact machine-readable binding to a resolved human checkpoint."""

    authorization_id: str
    checkpoint_path: str
    checkpoint_sha256: str
    repository_root: str
    design_path: str
    design_sha256: str
    runner_path: str
    runner_sha256: str
    parent_path: str
    parent_sha256: str
    output_path: str
    maximum_matrix_dimension: int
    maximum_runtime_seconds: int
    maximum_peak_memory_gib: float
    network_access: bool
    human_response_verbatim: str


@dataclass(frozen=True, slots=True)
class StageAControls:
    """Closed controls needed by the Stage A runner."""

    study_id: str
    parent_path: str
    parent_sha256: str
    hopping_radius_squared: int
    cases: tuple[FoldingCase, ...]
    translation_x: int
    translation_y: int
    phase_step_x: float
    phase_step_y: float
    energy_shift: float
    algebraic_tolerance: float
    folding_tolerance: float
    compatibility_controls: tuple[CompatibilityControl, ...]
    seam_oracle: SeamOracleControl


class ClosedJsonReader:
    """Decode exact JSON representations into closed Python values."""

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
    def records(value: JsonValue, name: str) -> tuple[dict[str, JsonValue], ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        records: list[dict[str, JsonValue]] = []
        for index, item in enumerate(value):
            if not isinstance(item, dict):
                raise TypeError(f"{name}[{index}] must be a JSON object")
            records.append(item)
        return tuple(records)

    @staticmethod
    def array(value: JsonValue, name: str) -> list[JsonValue]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return value

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
            raise TypeError(f"{name} must be a number")
        result = float(value)
        if not np.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result

    def integer_pair(self, value: JsonValue, name: str) -> tuple[int, int]:
        items = self.array(value, name)
        if len(items) != 2:
            raise ValueError(f"{name} must have two entries")
        return self.integer(items[0], f"{name}[0]"), self.integer(
            items[1], f"{name}[1]"
        )

    def real_pair(self, value: JsonValue, name: str) -> tuple[float, float]:
        items = self.array(value, name)
        if len(items) != 2:
            raise ValueError(f"{name} must have two entries")
        return self.real(items[0], f"{name}[0]"), self.real(items[1], f"{name}[1]")


class StageAInputDeserializer:
    """Load the accepted design, separate authorization, and scalar parent."""

    __slots__ = ("_json",)

    def __init__(self) -> None:
        self._json = ClosedJsonReader()

    def controls(self, design_path: Path) -> StageAControls:
        root = self._json.read(design_path)
        if self._json.integer(root["schema_version"], "schema_version") != 1:
            raise ValueError("unsupported design schema version")
        if root["design_status"] != "frozen_human_accepted_for_implementation":
            raise ValueError("the design is not accepted for implementation")
        if root["execution_authorized_by_this_record"] is not False:
            raise ValueError("the design must not authorize execution")
        parent = self._json.mapping(root["parent_sources"], "parent_sources")
        spaces = self._json.mapping(root["represented_spaces"], "represented_spaces")
        scalar = self._json.mapping(spaces["scalar_parent"], "scalar_parent")
        folding = self._json.mapping(root["folding_controls"], "folding_controls")
        seam = self._json.mapping(
            folding["seam_phase_oracle"], "folding_controls.seam_phase_oracle"
        )
        attacks = self._json.mapping(root["alignment_attacks"], "alignment_attacks")
        tolerances = self._json.mapping(root["tolerances"], "tolerances")
        compatibility_controls = tuple(
            self._compatibility_control(record)
            for record in self._json.records(
                root["stage_a_incompatible_controls"],
                "stage_a_incompatible_controls",
            )
        )
        shapes = tuple(
            self._json.integer_pair(item, "supercell_shape")
            for item in self._json.array(
                folding["supercell_shapes"], "folding_controls.supercell_shapes"
            )
        )
        twists = tuple(
            self._json.real_pair(item, "boundary_phase_turns")
            for item in self._json.array(
                folding["boundary_phase_turns"],
                "folding_controls.boundary_phase_turns",
            )
        )
        cases = tuple(
            FoldingCase(nx=nx, ny=ny, phi_x=phi_x, phi_y=phi_y)
            for nx, ny in shapes
            for phi_x, phi_y in twists
        )
        translation = self._json.integer_pair(
            attacks["translation_cells"], "alignment_attacks.translation_cells"
        )
        phase_steps = self._json.real_pair(
            attacks["site_phase_steps_radians"],
            "alignment_attacks.site_phase_steps_radians",
        )
        return StageAControls(
            study_id=self._json.string(root["study_id"], "study_id"),
            parent_path=self._json.string(
                parent["periodic_2d_scalar_result_path"],
                "periodic_2d_scalar_result_path",
            ),
            parent_sha256=self._json.string(
                parent["periodic_2d_scalar_result_sha256"],
                "periodic_2d_scalar_result_sha256",
            ),
            hopping_radius_squared=self._json.integer(
                scalar["hopping_maximum_squared_radius"],
                "hopping_maximum_squared_radius",
            ),
            cases=cases,
            translation_x=translation[0],
            translation_y=translation[1],
            phase_step_x=phase_steps[0],
            phase_step_y=phase_steps[1],
            energy_shift=self._json.real(
                attacks["energy_reference_shift"], "energy_reference_shift"
            ),
            algebraic_tolerance=self._json.real(
                tolerances["algebraic_absolute"], "algebraic_absolute"
            ),
            folding_tolerance=self._json.real(
                tolerances["folding_unitarity"], "folding_unitarity"
            ),
            compatibility_controls=compatibility_controls,
            seam_oracle=SeamOracleControl(
                size=self._json.integer(seam["size"], "seam size"),
                twist=self._json.real(seam["twist_turns"], "seam twist"),
                noncrossing_source=self._json.integer(
                    seam["noncrossing_source"], "noncrossing_source"
                ),
                positive_crossing_source=self._json.integer(
                    seam["positive_crossing_source"], "positive_crossing_source"
                ),
                positive_displacement=self._json.integer(
                    seam["positive_displacement"], "positive_displacement"
                ),
                negative_crossing_source=self._json.integer(
                    seam["negative_crossing_source"], "negative_crossing_source"
                ),
                negative_displacement=self._json.integer(
                    seam["negative_displacement"], "negative_displacement"
                ),
            ),
        )

    def _compatibility_control(
        self, record: dict[str, JsonValue]
    ) -> CompatibilityControl:
        return CompatibilityControl(
            control=self._json.string(record["control"], "control"),
            pristine=self._metadata(record["pristine"], "pristine"),
            candidate=self._metadata(record["candidate"], "candidate"),
            expected_issue_code=self._json.string(
                record["expected_issue_code"], "expected_issue_code"
            ),
        )

    def _metadata(self, value: JsonValue, name: str) -> RepresentationMetadata:
        record = self._json.mapping(value, name)
        return RepresentationMetadata(
            geometry=self._json.integer_pair(record["geometry"], f"{name}.geometry"),
            boundary_phase=self._json.real_pair(
                record["boundary_phase_turns"], f"{name}.boundary_phase_turns"
            ),
            site_map_known=self._json.boolean(
                record["site_map_known"], f"{name}.site_map_known"
            ),
            energy_reference_relation_known=self._json.boolean(
                record["energy_reference_relation_known"],
                f"{name}.energy_reference_relation_known",
            ),
        )

    def authorization(self, path: Path) -> StageAExecutionAuthorization:
        root = self._json.read(path)
        expected: dict[str, JsonValue] = {
            "schema_version": 2,
            "authorization_kind": "defect-2d-stage-execution",
            "stage_id": "A_null_and_folding",
            "execution_authorized": True,
        }
        for key, value in expected.items():
            if root.get(key) != value:
                raise ValueError(f"authorization field {key!r} is invalid")
        resources = self._json.mapping(root["resource_envelope"], "resource_envelope")
        return StageAExecutionAuthorization(
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
            parent_path=self._json.string(root["parent_path"], "parent_path"),
            parent_sha256=self._json.string(root["parent_sha256"], "parent_sha256"),
            output_path=self._json.string(root["output_path"], "output_path"),
            maximum_matrix_dimension=self._json.integer(
                resources["maximum_matrix_dimension"], "maximum_matrix_dimension"
            ),
            maximum_runtime_seconds=self._json.integer(
                resources["maximum_runtime_seconds"], "maximum_runtime_seconds"
            ),
            maximum_peak_memory_gib=self._json.real(
                resources["maximum_peak_memory_gib"], "maximum_peak_memory_gib"
            ),
            network_access=self._json.boolean(
                resources["network_access"], "network_access"
            ),
            human_response_verbatim=self._json.string(
                root["human_response_verbatim"], "human_response_verbatim"
            ),
        )

    def hoppings(
        self, parent_path: Path, maximum_radius_squared: int
    ) -> tuple[Hopping, ...]:
        root = self._json.read(parent_path)
        continuation = self._json.records(
            root["coupling_continuation"], "coupling_continuation"
        )
        matches = [
            record
            for record in continuation
            if self._json.real(record["lambda_xy"], "lambda_xy") == 0.0
        ]
        if len(matches) != 1:
            raise ValueError("the scalar parent must contain one lambda_xy=0 entry")
        hopping_records = self._json.records(
            matches[0]["hopping_coefficients"], "hopping_coefficients"
        )
        hoppings = tuple(
            Hopping(
                rx=self._json.integer(record["rx"], "rx"),
                ry=self._json.integer(record["ry"], "ry"),
                value=complex(
                    self._json.real(record["real"], "real"),
                    self._json.real(record["imag"], "imag"),
                ),
            )
            for record in hopping_records
            if self._json.integer(record["rx"], "rx") ** 2
            + self._json.integer(record["ry"], "ry") ** 2
            <= maximum_radius_squared
        )
        if not hoppings:
            raise ValueError("the retained parent hopping set is empty")
        return hoppings


class StageACompatibilityAssessment:
    """Exercise incompatible comparisons without constructing a residual."""

    __slots__ = ()

    def execute(self, controls: tuple[CompatibilityControl, ...]) -> list[JsonValue]:
        records: list[JsonValue] = []
        for control in controls:
            issue = self._issue(control.pristine, control.candidate)
            if issue is None:
                raise AssertionError(
                    f"incompatible control {control.control} did not stop"
                )
            if issue != control.expected_issue_code:
                raise AssertionError(
                    f"incompatible control {control.control} reached {issue}, "
                    f"not {control.expected_issue_code}"
                )
            records.append(
                {
                    "control": control.control,
                    "pristine_metadata": self._metadata(control.pristine),
                    "candidate_metadata": self._metadata(control.candidate),
                    "issue_code": issue,
                    "residual": None,
                }
            )
        return records

    @staticmethod
    def _issue(
        pristine: RepresentationMetadata, candidate: RepresentationMetadata
    ) -> str | None:
        if pristine.geometry != candidate.geometry:
            return "DEFECT_2D.GEOMETRY_MISMATCH"
        if pristine.boundary_phase != candidate.boundary_phase:
            return "DEFECT_2D.BOUNDARY_PHASE_MISMATCH"
        if not candidate.site_map_known:
            return "DEFECT_2D.SITE_MAP_UNRESOLVED"
        if not candidate.energy_reference_relation_known:
            return "DEFECT_2D.ENERGY_REFERENCE_UNKNOWN"
        return None

    @staticmethod
    def _metadata(metadata: RepresentationMetadata) -> dict[str, JsonValue]:
        return {
            "geometry": [metadata.geometry[0], metadata.geometry[1]],
            "boundary_phase_turns": [
                metadata.boundary_phase[0],
                metadata.boundary_phase[1],
            ],
            "site_map_known": metadata.site_map_known,
            "energy_reference_relation_known": (
                metadata.energy_reference_relation_known
            ),
        }


class StageACalculation:
    """Construct Stage A through explicit site-and-hop enumeration."""

    __slots__ = ()

    def execute(
        self, controls: StageAControls, hoppings: tuple[Hopping, ...]
    ) -> list[JsonValue]:
        records: list[JsonValue] = []
        for case in controls.cases:
            hamiltonian = self._supercell(case, hoppings)
            folding = self._folding(case)
            expected = self._primitive_energies(case, hoppings)
            represented = folding.conj().T @ hamiltonian @ folding
            diagonal = np.diag(np.diag(represented))
            expected_diagonal = np.diag(expected)
            null_record = self._null_extraction(case, hamiltonian, controls)
            record: dict[str, JsonValue] = {
                "shape": [case.nx, case.ny],
                "boundary_phase_turns": [case.phi_x, case.phi_y],
                "represented_dimension": case.nx * case.ny,
                "folding": {
                    "unitarity_maximum_absolute_defect": self._maximum_absolute(
                        folding.conj().T @ folding
                        - np.eye(case.nx * case.ny, dtype=np.complex128)
                    ),
                    "hermiticity_maximum_absolute_defect": self._maximum_absolute(
                        hamiltonian - hamiltonian.conj().T
                    ),
                    "off_block_maximum_absolute": self._maximum_absolute(
                        represented - diagonal
                    ),
                    "primitive_block_maximum_absolute_defect": self._maximum_absolute(
                        represented - expected_diagonal
                    ),
                    "eigenvalue_maximum_absolute_defect": float(
                        np.max(
                            np.abs(
                                np.sort(np.linalg.eigvalsh(hamiltonian))
                                - np.sort(expected)
                            )
                        )
                    ),
                },
                "null_extraction": null_record,
            }
            records.append(record)
        return records

    def seam_oracle(self, control: SeamOracleControl) -> dict[str, JsonValue]:
        """Exercise the production seam assembly against frozen crossings."""

        cases = (
            ("noncrossing", control.noncrossing_source, 1),
            (
                "positive_crossing",
                control.positive_crossing_source,
                control.positive_displacement,
            ),
            (
                "negative_crossing",
                control.negative_crossing_source,
                control.negative_displacement,
            ),
        )
        records: list[JsonValue] = []
        folding_case = FoldingCase(
            nx=control.size,
            ny=1,
            phi_x=control.twist,
            phi_y=0.0,
        )
        for name, source, displacement in cases:
            matrix = self._supercell(
                folding_case, (Hopping(displacement, 0, 1.0 + 0.0j),)
            )
            _, target = divmod(source + displacement, control.size)
            value = matrix[source, target]
            records.append(
                {
                    "case": name,
                    "source": source,
                    "target": target,
                    "displacement": displacement,
                    "real": float(value.real),
                    "imag": float(value.imag),
                }
            )
        return {
            "size": control.size,
            "twist_turns": control.twist,
            "cases": records,
        }

    @staticmethod
    def _supercell(case: FoldingCase, hoppings: tuple[Hopping, ...]) -> ComplexMatrix:
        dimension = case.nx * case.ny
        result = np.zeros((dimension, dimension), dtype=np.complex128)
        for x in range(case.nx):
            for y in range(case.ny):
                row = x * case.ny + y
                for hopping in hoppings:
                    target_x = x + hopping.rx
                    target_y = y + hopping.ry
                    quotient_x, wrapped_x = divmod(target_x, case.nx)
                    quotient_y, wrapped_y = divmod(target_y, case.ny)
                    column = wrapped_x * case.ny + wrapped_y
                    phase = np.exp(
                        2.0j
                        * np.pi
                        * (quotient_x * case.phi_x + quotient_y * case.phi_y)
                    )
                    result[row, column] += hopping.value * phase
        return result

    @staticmethod
    def _folding(case: FoldingCase) -> ComplexMatrix:
        dimension = case.nx * case.ny
        result = np.empty((dimension, dimension), dtype=np.complex128)
        scale = 1.0 / np.sqrt(float(dimension))
        for x in range(case.nx):
            for y in range(case.ny):
                row = x * case.ny + y
                for jx in range(case.nx):
                    kx = (jx + case.phi_x) / case.nx
                    for jy in range(case.ny):
                        ky = (jy + case.phi_y) / case.ny
                        column = jx * case.ny + jy
                        result[row, column] = scale * np.exp(
                            2.0j * np.pi * (kx * x + ky * y)
                        )
        return result

    @staticmethod
    def _primitive_energies(
        case: FoldingCase, hoppings: tuple[Hopping, ...]
    ) -> npt.NDArray[np.float64]:
        energies = np.empty(case.nx * case.ny, dtype=np.float64)
        for jx in range(case.nx):
            kx = (jx + case.phi_x) / case.nx
            for jy in range(case.ny):
                ky = (jy + case.phi_y) / case.ny
                value = sum(
                    hopping.value
                    * np.exp(2.0j * np.pi * (kx * hopping.rx + ky * hopping.ry))
                    for hopping in hoppings
                )
                if abs(value.imag) > 1.0e-11:
                    raise ValueError("the primitive scalar energy is not real")
                energies[jx * case.ny + jy] = value.real
        return energies

    def _null_extraction(
        self,
        case: FoldingCase,
        pristine: ComplexMatrix,
        controls: StageAControls,
    ) -> dict[str, JsonValue]:
        dimension = case.nx * case.ny
        transform = np.zeros((dimension, dimension), dtype=np.complex128)
        for x in range(case.nx):
            for y in range(case.ny):
                source = x * case.ny + y
                target_x = (x + controls.translation_x) % case.nx
                target_y = (y + controls.translation_y) % case.ny
                target = target_x * case.ny + target_y
                transform[target, source] = np.exp(
                    1.0j * (controls.phase_step_x * x + controls.phase_step_y * y)
                )
        identity = np.eye(dimension, dtype=np.complex128)
        raw_defect = (
            transform @ pristine @ transform.conj().T + controls.energy_shift * identity
        )
        recovered = (
            transform.conj().T
            @ (raw_defect - controls.energy_shift * identity)
            @ transform
            - pristine
        )
        return {
            "transform_unitarity_maximum_absolute_defect": self._maximum_absolute(
                transform.conj().T @ transform - identity
            ),
            "recovered_maximum_absolute_defect": self._maximum_absolute(recovered),
            "recovered_frobenius_defect": float(np.linalg.norm(recovered, ord="fro")),
        }

    @staticmethod
    def _maximum_absolute(value: ComplexMatrix) -> float:
        return float(np.max(np.abs(value), initial=0.0))


class StageACriterionEvaluator:
    """Classify numerical criteria without discarding reproduced failures."""

    __slots__ = ("_json",)

    def __init__(self) -> None:
        self._json = ClosedJsonReader()

    def execute(
        self, records: list[JsonValue], controls: StageAControls
    ) -> dict[str, JsonValue]:
        failures: list[JsonValue] = []
        for index, value in enumerate(records):
            record = self._json.mapping(value, f"case[{index}]")
            folding = self._json.mapping(record["folding"], f"case[{index}].folding")
            null = self._json.mapping(
                record["null_extraction"], f"case[{index}].null_extraction"
            )
            criteria = (
                (
                    "folding.unitarity_maximum_absolute_defect",
                    folding["unitarity_maximum_absolute_defect"],
                    controls.folding_tolerance,
                ),
                (
                    "folding.hermiticity_maximum_absolute_defect",
                    folding["hermiticity_maximum_absolute_defect"],
                    controls.algebraic_tolerance,
                ),
                (
                    "folding.off_block_maximum_absolute",
                    folding["off_block_maximum_absolute"],
                    controls.algebraic_tolerance,
                ),
                (
                    "folding.primitive_block_maximum_absolute_defect",
                    folding["primitive_block_maximum_absolute_defect"],
                    controls.algebraic_tolerance,
                ),
                (
                    "folding.eigenvalue_maximum_absolute_defect",
                    folding["eigenvalue_maximum_absolute_defect"],
                    controls.algebraic_tolerance,
                ),
                (
                    "null.transform_unitarity_maximum_absolute_defect",
                    null["transform_unitarity_maximum_absolute_defect"],
                    controls.algebraic_tolerance,
                ),
                (
                    "null.recovered_maximum_absolute_defect",
                    null["recovered_maximum_absolute_defect"],
                    controls.algebraic_tolerance,
                ),
                (
                    "null.recovered_frobenius_defect",
                    null["recovered_frobenius_defect"],
                    controls.algebraic_tolerance,
                ),
            )
            for name, represented, tolerance in criteria:
                observed = self._json.real(represented, name)
                if observed > tolerance:
                    failures.append(f"case[{index}].{name}")
        return {
            "status": "pass" if not failures else "fail",
            "failed_criteria": failures,
        }


class StageAResultSerializer:
    """Create and retain the canonical Stage A result."""

    __slots__ = ()

    def payload(
        self,
        controls: StageAControls,
        authorization: StageAExecutionAuthorization,
        repository_root: Path,
        design_path: Path,
        parent_path: Path,
        authorization_path: Path,
        checkpoint_path: Path,
        script_path: Path,
        case_records: list[JsonValue],
        stop_records: list[JsonValue],
        seam_record: dict[str, JsonValue],
        criterion_record: dict[str, JsonValue],
    ) -> dict[str, JsonValue]:
        return {
            "schema_version": 1,
            "study_id": controls.study_id,
            "stage_id": "A_null_and_folding",
            "evidence_status": "synthetic test data",
            "calculation_status": "calculated synthetic numerical-verification result",
            "authorization_id": authorization.authorization_id,
            "provenance": {
                "design_path": self._relative(repository_root, design_path),
                "design_sha256": self._sha256(design_path),
                "parent_path": self._relative(repository_root, parent_path),
                "parent_sha256": self._sha256(parent_path),
                "authorization_path": self._relative(
                    repository_root, authorization_path
                ),
                "authorization_sha256": self._sha256(authorization_path),
                "checkpoint_path": self._relative(repository_root, checkpoint_path),
                "checkpoint_sha256": self._sha256(checkpoint_path),
                "script_path": self._relative(repository_root, script_path),
                "script_sha256": self._sha256(script_path),
                "python_version": platform.python_version(),
                "numpy_version": np.__version__,
            },
            "retained_hopping_maximum_squared_radius": controls.hopping_radius_squared,
            "tolerances": {
                "algebraic_absolute": controls.algebraic_tolerance,
                "folding_unitarity": controls.folding_tolerance,
            },
            "cases": case_records,
            "seam_phase_oracle": seam_record,
            "criterion_evaluation": criterion_record,
            "structured_stops": stop_records,
            "limitations": [
                (
                    "Stage A contains only scalar folding, seam, null, and "
                    "stopping controls."
                ),
                (
                    "No planted nonzero defect, blind alignment, model-class fit, "
                    "finite-size conclusion, or composite parent is evaluated."
                ),
                "Passing Stage A would not authorize or establish Stages B-E.",
                (
                    "The evidence is synthetic numerical verification, not material "
                    "validation or uncertainty quantification."
                ),
            ],
        }

    def write(self, output_path: Path, payload: dict[str, JsonValue]) -> None:
        if output_path.exists():
            raise FileExistsError(f"refusing to overwrite {output_path}")
        output_path.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

    @staticmethod
    def _sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    @staticmethod
    def _relative(repository_root: Path, path: Path) -> str:
        return path.relative_to(repository_root).as_posix()


class StageARunner:
    """Validate authority and execute the bounded Stage A calculation."""

    __slots__ = (
        "_calculation",
        "_compatibility",
        "_criteria",
        "_deserializer",
        "_json",
        "_serializer",
    )

    def __init__(self) -> None:
        self._deserializer = StageAInputDeserializer()
        self._calculation = StageACalculation()
        self._compatibility = StageACompatibilityAssessment()
        self._criteria = StageACriterionEvaluator()
        self._json = ClosedJsonReader()
        self._serializer = StageAResultSerializer()

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
        canonical_design = self._existing_inside(root, design_path)
        expected_design = (
            root
            / "calculations/research-monograph/impurity-defect-2d/study-design.json"
        ).resolve(strict=True)
        if canonical_design != expected_design:
            raise ValueError("design path is not the authoritative Stage A design")
        canonical_authorization = self._existing_inside(root, authorization_path)
        canonical_output = self._output_inside(root, output_path)
        if canonical_output.exists():
            raise FileExistsError(f"refusing to overwrite {canonical_output}")
        controls = self._deserializer.controls(canonical_design)
        authorization = self._deserializer.authorization(canonical_authorization)
        script_path = Path(__file__).resolve(strict=True)
        parent_path = self._bound_existing(root, controls.parent_path, "parent_path")
        checkpoint_path = self._bound_existing(
            root, authorization.checkpoint_path, "checkpoint_path"
        )
        self._validate_authorization(
            authorization=authorization,
            repository_root=root,
            design_path=canonical_design,
            runner_path=script_path,
            parent_path=parent_path,
            output_path=canonical_output,
            checkpoint_path=checkpoint_path,
            controls=controls,
        )
        hoppings = self._deserializer.hoppings(
            parent_path, controls.hopping_radius_squared
        )
        cases = self._calculation.execute(controls, hoppings)
        seam = self._calculation.seam_oracle(controls.seam_oracle)
        stops = self._compatibility.execute(controls.compatibility_controls)
        criteria = self._criteria.execute(cases, controls)
        payload = self._serializer.payload(
            controls=controls,
            authorization=authorization,
            repository_root=root,
            design_path=canonical_design,
            parent_path=parent_path,
            authorization_path=canonical_authorization,
            checkpoint_path=checkpoint_path,
            script_path=script_path,
            case_records=cases,
            stop_records=stops,
            seam_record=seam,
            criterion_record=criteria,
        )
        self._serializer.write(canonical_output, payload)

    def _validate_authorization(
        self,
        *,
        authorization: StageAExecutionAuthorization,
        repository_root: Path,
        design_path: Path,
        runner_path: Path,
        parent_path: Path,
        output_path: Path,
        checkpoint_path: Path,
        controls: StageAControls,
    ) -> None:
        if authorization.repository_root != str(repository_root):
            raise ValueError(
                "authorization does not bind the canonical repository root"
            )
        bindings = (
            (authorization.design_path, design_path, authorization.design_sha256),
            (authorization.runner_path, runner_path, authorization.runner_sha256),
            (authorization.parent_path, parent_path, authorization.parent_sha256),
            (
                authorization.checkpoint_path,
                checkpoint_path,
                authorization.checkpoint_sha256,
            ),
        )
        for represented, actual, expected_digest in bindings:
            if (
                self._bound_existing(
                    repository_root, represented, f"binding for {actual.name}"
                )
                != actual
            ):
                raise ValueError(f"authorization path binding differs for {actual}")
            if self._sha256(actual) != expected_digest:
                raise ValueError(f"authorization digest binding differs for {actual}")
        if (
            self._bound_output(repository_root, authorization.output_path)
            != output_path
        ):
            raise ValueError("authorization does not bind the requested output path")
        if controls.parent_sha256 != authorization.parent_sha256:
            raise ValueError("authorization parent identity differs from the design")
        maximum_dimension = max(case.nx * case.ny for case in controls.cases)
        if authorization.maximum_matrix_dimension != maximum_dimension:
            raise ValueError("authorization matrix dimension differs from Stage A")
        if not 0 < authorization.maximum_runtime_seconds <= 120:
            raise ValueError("authorization runtime exceeds the Stage A envelope")
        if not 0.0 < authorization.maximum_peak_memory_gib <= 2.0:
            raise ValueError("authorization memory exceeds the Stage A envelope")
        if authorization.network_access:
            raise ValueError("Stage A does not authorize network access")
        checkpoint = self._json.read(checkpoint_path)
        expected_checkpoint: dict[str, JsonValue] = {
            "status": "resolved",
            "task_id": "research-monograph.exercises.impurity.defect-2d",
            "human_response": authorization.human_response_verbatim,
        }
        for key, value in expected_checkpoint.items():
            if checkpoint.get(key) != value:
                raise ValueError(f"execution checkpoint field {key!r} is invalid")
        self._json.string(checkpoint.get("authorized_scope"), "authorized_scope")
        self._json.string(checkpoint.get("blocked_scope"), "blocked_scope")
        authoritative = self._json.array(
            checkpoint["authoritative_files"], "authoritative_files"
        )
        authoritative_paths = {
            self._json.string(item, "authoritative file") for item in authoritative
        }
        required = {
            "calculations/research-monograph/impurity-defect-2d/preflight.md",
            "calculations/research-monograph/impurity-defect-2d/protocol.md",
            "calculations/research-monograph/impurity-defect-2d/run_stage_a.py",
            "calculations/research-monograph/impurity-defect-2d/study-design.json",
        }
        if not required.issubset(authoritative_paths):
            raise ValueError("execution checkpoint omits an authoritative Stage A file")

    @staticmethod
    def _existing_inside(repository_root: Path, represented: Path) -> Path:
        candidate = (
            represented if represented.is_absolute() else repository_root / represented
        )
        resolved = candidate.resolve(strict=True)
        if not resolved.is_relative_to(repository_root):
            raise ValueError(f"path escapes repository root: {represented}")
        return resolved

    @staticmethod
    def _output_inside(repository_root: Path, represented: Path) -> Path:
        candidate = (
            represented if represented.is_absolute() else repository_root / represented
        )
        parent = candidate.parent.resolve(strict=True)
        resolved = parent / candidate.name
        if not resolved.is_relative_to(repository_root):
            raise ValueError(f"output path escapes repository root: {represented}")
        return resolved

    @staticmethod
    def _bound_existing(repository_root: Path, represented: str, name: str) -> Path:
        path = Path(represented)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"{name} must be canonical repository-relative")
        resolved = (repository_root / path).resolve(strict=True)
        if not resolved.is_relative_to(repository_root):
            raise ValueError(f"{name} escapes repository root")
        if resolved.relative_to(repository_root).as_posix() != represented:
            raise ValueError(f"{name} is not canonical")
        return resolved

    @staticmethod
    def _bound_output(repository_root: Path, represented: str) -> Path:
        path = Path(represented)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError("output_path must be canonical repository-relative")
        parent = (repository_root / path).parent.resolve(strict=True)
        resolved = parent / path.name
        if not resolved.is_relative_to(repository_root):
            raise ValueError("output_path escapes repository root")
        if resolved.relative_to(repository_root).as_posix() != represented:
            raise ValueError("output_path is not canonical")
        return resolved

    @staticmethod
    def _sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    """Adapt command-line arguments to the Stage A runner."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--design", required=True, type=Path)
    parser.add_argument("--execution-authorization", required=True, type=Path)
    parser.add_argument("--repository-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()
    StageARunner().execute(
        design_path=arguments.design,
        authorization_path=arguments.execution_authorization,
        repository_root=arguments.repository_root,
        output_path=arguments.output,
    )


if __name__ == "__main__":
    main()
