#!/usr/bin/env python3
"""Independently verify an authorized retained defect-2D Stage A result."""

from __future__ import annotations

import argparse
import cmath
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


@dataclass(frozen=True, slots=True)
class ParentCoefficient:
    """Independently decoded scalar parent coefficient."""

    displacement_x: int
    displacement_y: int
    amplitude: complex


@dataclass(frozen=True, slots=True)
class FoldingExpectation:
    """One exact design-owned folding case."""

    nx: int
    ny: int
    phi_x: float
    phi_y: float


@dataclass(frozen=True, slots=True)
class VerificationSeamOracle:
    """Frozen analytical seam-phase oracle."""

    size: int
    twist: float
    noncrossing_source: int
    positive_crossing_source: int
    positive_displacement: int
    negative_crossing_source: int
    negative_displacement: int


@dataclass(frozen=True, slots=True)
class VerificationExecutionAuthorization:
    """Independent representation of the exact execution binding."""

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
class VerificationMetadata:
    """Independently decoded represented-comparison metadata."""

    geometry: tuple[int, int]
    boundary_phase: tuple[float, float]
    site_map_known: bool
    energy_reference_relation_known: bool


@dataclass(frozen=True, slots=True)
class StopExpectation:
    """One frozen Stage A incompatibility expectation."""

    control: str
    pristine: VerificationMetadata
    candidate: VerificationMetadata
    expected_issue_code: str


@dataclass(frozen=True, slots=True)
class VerificationControls:
    """Accepted Stage A values required by the independent verifier."""

    study_id: str
    parent_relative_path: str
    parent_sha256: str
    maximum_radius_squared: int
    translation: tuple[int, int]
    phase_steps: tuple[float, float]
    energy_shift: float
    algebraic_tolerance: float
    folding_tolerance: float
    independent_relative_tolerance: float
    stop_expectations: tuple[StopExpectation, ...]
    folding_expectations: tuple[FoldingExpectation, ...]
    seam_oracle: VerificationSeamOracle


class VerificationJsonDecoder:
    """Decode retained JSON without importing runner code."""

    __slots__ = ()

    def load(self, path: Path) -> dict[str, JsonValue]:
        value = cast(JsonValue, json.loads(path.read_text(encoding="utf-8")))
        return self.mapping(value, str(path))

    @staticmethod
    def mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be an object")
        return value

    @staticmethod
    def records(value: JsonValue, name: str) -> tuple[dict[str, JsonValue], ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be an array")
        result: list[dict[str, JsonValue]] = []
        for index, item in enumerate(value):
            if not isinstance(item, dict):
                raise TypeError(f"{name}[{index}] must be an object")
            result.append(item)
        return tuple(result)

    @staticmethod
    def array(value: JsonValue, name: str) -> list[JsonValue]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be an array")
        return value

    @staticmethod
    def text(value: JsonValue, name: str) -> str:
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
    def number(value: JsonValue, name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be numeric")
        result = float(value)
        if not np.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result

    def integer_pair(self, value: JsonValue, name: str) -> tuple[int, int]:
        items = self.array(value, name)
        if len(items) != 2:
            raise ValueError(f"{name} must contain two values")
        return self.integer(items[0], f"{name}[0]"), self.integer(
            items[1], f"{name}[1]"
        )

    def real_pair(self, value: JsonValue, name: str) -> tuple[float, float]:
        items = self.array(value, name)
        if len(items) != 2:
            raise ValueError(f"{name} must contain two values")
        return self.number(items[0], f"{name}[0]"), self.number(items[1], f"{name}[1]")


class StageAVerifier:
    """Reconstruct Stage A with Kronecker seam matrices and direct checks."""

    __slots__ = ("_decoder",)

    def __init__(self) -> None:
        self._decoder = VerificationJsonDecoder()

    def execute(self, result_path: Path, repository_root: Path) -> None:
        root = repository_root.resolve(strict=True)
        if not repository_root.is_absolute() or root != repository_root:
            raise ValueError("repository_root must be canonical and absolute")
        canonical_result = self._existing_inside(root, result_path)
        result = self._decoder.load(canonical_result)
        self._verify_result_header(result)
        provenance = self._decoder.mapping(result["provenance"], "provenance")
        design_path = self._resolve_bound(
            root, self._decoder.text(provenance["design_path"], "design_path")
        )
        parent_path = self._resolve_bound(
            root, self._decoder.text(provenance["parent_path"], "parent_path")
        )
        authorization_path = self._resolve_bound(
            root,
            self._decoder.text(provenance["authorization_path"], "authorization_path"),
        )
        checkpoint_path = self._resolve_bound(
            root,
            self._decoder.text(provenance["checkpoint_path"], "checkpoint_path"),
        )
        runner_path = self._resolve_bound(
            root, self._decoder.text(provenance["script_path"], "script_path")
        )
        self._assert_digest(design_path, provenance["design_sha256"])
        self._assert_digest(parent_path, provenance["parent_sha256"])
        self._assert_digest(authorization_path, provenance["authorization_sha256"])
        self._assert_digest(checkpoint_path, provenance["checkpoint_sha256"])
        self._assert_digest(runner_path, provenance["script_sha256"])
        authorization = self._authorization(authorization_path)
        controls = self._controls(design_path)
        self._verify_authorization_binding(
            authorization=authorization,
            repository_root=root,
            result_path=canonical_result,
            design_path=design_path,
            parent_path=parent_path,
            runner_path=runner_path,
            checkpoint_path=checkpoint_path,
            controls=controls,
        )
        if result["authorization_id"] != authorization.authorization_id:
            raise ValueError("result authorization identity does not match")
        if result["study_id"] != controls.study_id:
            raise ValueError("result study identity does not match the design")
        if parent_path != self._resolve_bound(root, controls.parent_relative_path):
            raise ValueError("result parent path does not match the design")
        if self._sha256(parent_path) != controls.parent_sha256:
            raise ValueError("DEFECT_2D.PARENT_IDENTITY_MISMATCH")
        coefficients = self._coefficients(parent_path, controls.maximum_radius_squared)
        case_records = self._decoder.records(result["cases"], "cases")
        if len(case_records) != len(controls.folding_expectations):
            raise ValueError("folding case count differs from the accepted design")
        maximum_reconstruction_defect = 0.0
        criterion_failures: list[JsonValue] = []
        for index, (record, expectation) in enumerate(
            zip(case_records, controls.folding_expectations, strict=True)
        ):
            defect, failures = self._verify_case(
                index, record, expectation, controls, coefficients
            )
            maximum_reconstruction_defect = max(maximum_reconstruction_defect, defect)
            criterion_failures.extend(failures)
        self._verify_seam_oracle(result["seam_phase_oracle"], controls.seam_oracle)
        self._verify_criterion_record(
            result["criterion_evaluation"], criterion_failures
        )
        self._verify_stops(result["structured_stops"], controls.stop_expectations)
        limitations = result["limitations"]
        if not isinstance(limitations, list) or len(limitations) != 4:
            raise ValueError("Stage A must retain four limitations")
        criterion_status = "pass" if not criterion_failures else "fail"
        print("defect_2d_stage_a_reconstruction=PASS")
        print(f"defect_2d_stage_a_criteria={criterion_status.upper()}")
        print(
            f"maximum_independent_reconstruction_defect={maximum_reconstruction_defect:.3e}"
        )

    def _verify_result_header(self, result: dict[str, JsonValue]) -> None:
        expected: dict[str, JsonValue] = {
            "schema_version": 1,
            "stage_id": "A_null_and_folding",
            "evidence_status": "synthetic test data",
            "calculation_status": "calculated synthetic numerical-verification result",
        }
        for key, value in expected.items():
            if result.get(key) != value:
                raise ValueError(f"result field {key!r} is invalid")

    def _controls(self, design_path: Path) -> VerificationControls:
        design = self._decoder.load(design_path)
        if design["design_status"] != "frozen_human_accepted_for_implementation":
            raise ValueError("design status is incompatible with Stage A")
        if design["execution_authorized_by_this_record"] is not False:
            raise ValueError("the design improperly authorizes execution")
        parent = self._decoder.mapping(design["parent_sources"], "parent_sources")
        represented = self._decoder.mapping(
            design["represented_spaces"], "represented_spaces"
        )
        scalar = self._decoder.mapping(represented["scalar_parent"], "scalar_parent")
        folding = self._decoder.mapping(design["folding_controls"], "folding_controls")
        seam = self._decoder.mapping(
            folding["seam_phase_oracle"], "folding_controls.seam_phase_oracle"
        )
        attacks = self._decoder.mapping(
            design["alignment_attacks"], "alignment_attacks"
        )
        tolerances = self._decoder.mapping(design["tolerances"], "tolerances")
        stop_expectations = tuple(
            self._stop_expectation(record)
            for record in self._decoder.records(
                design["stage_a_incompatible_controls"],
                "stage_a_incompatible_controls",
            )
        )
        shapes = tuple(
            self._decoder.integer_pair(item, "supercell_shape")
            for item in self._decoder.array(
                folding["supercell_shapes"], "folding_controls.supercell_shapes"
            )
        )
        twists = tuple(
            self._decoder.real_pair(item, "boundary_phase_turns")
            for item in self._decoder.array(
                folding["boundary_phase_turns"],
                "folding_controls.boundary_phase_turns",
            )
        )
        folding_expectations = tuple(
            FoldingExpectation(nx, ny, phi_x, phi_y)
            for nx, ny in shapes
            for phi_x, phi_y in twists
        )
        return VerificationControls(
            study_id=self._decoder.text(design["study_id"], "study_id"),
            parent_relative_path=self._decoder.text(
                parent["periodic_2d_scalar_result_path"], "parent path"
            ),
            parent_sha256=self._decoder.text(
                parent["periodic_2d_scalar_result_sha256"], "parent sha256"
            ),
            maximum_radius_squared=self._decoder.integer(
                scalar["hopping_maximum_squared_radius"], "hopping radius"
            ),
            translation=self._decoder.integer_pair(
                attacks["translation_cells"], "translation_cells"
            ),
            phase_steps=self._decoder.real_pair(
                attacks["site_phase_steps_radians"], "site_phase_steps_radians"
            ),
            energy_shift=self._decoder.number(
                attacks["energy_reference_shift"], "energy_reference_shift"
            ),
            algebraic_tolerance=self._decoder.number(
                tolerances["algebraic_absolute"], "algebraic_absolute"
            ),
            folding_tolerance=self._decoder.number(
                tolerances["folding_unitarity"], "folding_unitarity"
            ),
            independent_relative_tolerance=self._decoder.number(
                tolerances["independent_reconstruction_relative"],
                "independent_reconstruction_relative",
            ),
            stop_expectations=stop_expectations,
            folding_expectations=folding_expectations,
            seam_oracle=VerificationSeamOracle(
                size=self._decoder.integer(seam["size"], "seam size"),
                twist=self._decoder.number(seam["twist_turns"], "seam twist"),
                noncrossing_source=self._decoder.integer(
                    seam["noncrossing_source"], "noncrossing_source"
                ),
                positive_crossing_source=self._decoder.integer(
                    seam["positive_crossing_source"], "positive_crossing_source"
                ),
                positive_displacement=self._decoder.integer(
                    seam["positive_displacement"], "positive_displacement"
                ),
                negative_crossing_source=self._decoder.integer(
                    seam["negative_crossing_source"], "negative_crossing_source"
                ),
                negative_displacement=self._decoder.integer(
                    seam["negative_displacement"], "negative_displacement"
                ),
            ),
        )

    def _stop_expectation(self, record: dict[str, JsonValue]) -> StopExpectation:
        return StopExpectation(
            control=self._decoder.text(record["control"], "control"),
            pristine=self._metadata(record["pristine"], "pristine"),
            candidate=self._metadata(record["candidate"], "candidate"),
            expected_issue_code=self._decoder.text(
                record["expected_issue_code"], "expected_issue_code"
            ),
        )

    def _metadata(self, value: JsonValue, name: str) -> VerificationMetadata:
        record = self._decoder.mapping(value, name)
        return VerificationMetadata(
            geometry=self._decoder.integer_pair(record["geometry"], f"{name}.geometry"),
            boundary_phase=self._decoder.real_pair(
                record["boundary_phase_turns"], f"{name}.boundary_phase_turns"
            ),
            site_map_known=self._decoder.boolean(
                record["site_map_known"], f"{name}.site_map_known"
            ),
            energy_reference_relation_known=self._decoder.boolean(
                record["energy_reference_relation_known"],
                f"{name}.energy_reference_relation_known",
            ),
        )

    def _coefficients(
        self, parent_path: Path, maximum_radius_squared: int
    ) -> tuple[ParentCoefficient, ...]:
        parent = self._decoder.load(parent_path)
        continuation = self._decoder.records(
            parent["coupling_continuation"], "coupling_continuation"
        )
        selected = [
            record
            for record in continuation
            if self._decoder.number(record["lambda_xy"], "lambda_xy") == 0.0
        ]
        if len(selected) != 1:
            raise ValueError("independent route found an ambiguous scalar parent")
        records = self._decoder.records(
            selected[0]["hopping_coefficients"], "hopping_coefficients"
        )
        coefficients: list[ParentCoefficient] = []
        for record in records:
            rx = self._decoder.integer(record["rx"], "rx")
            ry = self._decoder.integer(record["ry"], "ry")
            if rx * rx + ry * ry <= maximum_radius_squared:
                coefficients.append(
                    ParentCoefficient(
                        displacement_x=rx,
                        displacement_y=ry,
                        amplitude=complex(
                            self._decoder.number(record["real"], "real"),
                            self._decoder.number(record["imag"], "imag"),
                        ),
                    )
                )
        if not coefficients:
            raise ValueError("independent route found no retained coefficients")
        return tuple(coefficients)

    def _verify_case(
        self,
        index: int,
        record: dict[str, JsonValue],
        expectation: FoldingExpectation,
        controls: VerificationControls,
        coefficients: tuple[ParentCoefficient, ...],
    ) -> tuple[float, list[JsonValue]]:
        nx, ny = self._decoder.integer_pair(record["shape"], "shape")
        phi_x, phi_y = self._decoder.real_pair(
            record["boundary_phase_turns"], "boundary_phase_turns"
        )
        if (nx, ny, phi_x, phi_y) != (
            expectation.nx,
            expectation.ny,
            expectation.phi_x,
            expectation.phi_y,
        ):
            raise ValueError(f"folding case[{index}] differs from the accepted design")
        dimension = nx * ny
        if (
            self._decoder.integer(record["represented_dimension"], "dimension")
            != dimension
        ):
            raise ValueError("represented dimension is inconsistent with shape")
        hamiltonian: ComplexMatrix = np.zeros(
            (dimension, dimension), dtype=np.complex128
        )
        for coefficient in coefficients:
            hamiltonian += coefficient.amplitude * np.kron(
                self._seam_shift(nx, coefficient.displacement_x, phi_x),
                self._seam_shift(ny, coefficient.displacement_y, phi_y),
            )
        folding = np.kron(self._fourier(nx, phi_x), self._fourier(ny, phi_y))
        expected = self._energy_grid(nx, ny, phi_x, phi_y, coefficients)
        represented = folding.conj().T @ hamiltonian @ folding
        diagonal = np.diag(np.diag(represented))
        recomputed = {
            "unitarity_maximum_absolute_defect": self._maximum_absolute(
                folding.conj().T @ folding - np.eye(dimension, dtype=np.complex128)
            ),
            "hermiticity_maximum_absolute_defect": self._maximum_absolute(
                hamiltonian - hamiltonian.conj().T
            ),
            "off_block_maximum_absolute": self._maximum_absolute(
                represented - diagonal
            ),
            "primitive_block_maximum_absolute_defect": self._maximum_absolute(
                represented - np.diag(expected)
            ),
            "eigenvalue_maximum_absolute_defect": float(
                np.max(
                    np.abs(np.sort(np.linalg.eigvalsh(hamiltonian)) - np.sort(expected))
                )
            ),
        }
        retained_folding = self._decoder.mapping(record["folding"], "folding")
        maximum_difference = 0.0
        for key, expected_value in recomputed.items():
            observed = self._decoder.number(retained_folding[key], key)
            np.testing.assert_allclose(
                observed,
                expected_value,
                rtol=controls.independent_relative_tolerance,
                atol=5.0e-13,
            )
            maximum_difference = max(maximum_difference, abs(observed - expected_value))
        failures: list[JsonValue] = []
        if recomputed["unitarity_maximum_absolute_defect"] > controls.folding_tolerance:
            failures.append(f"case[{index}].folding.unitarity_maximum_absolute_defect")
        for key in (
            "hermiticity_maximum_absolute_defect",
            "off_block_maximum_absolute",
            "primitive_block_maximum_absolute_defect",
            "eigenvalue_maximum_absolute_defect",
        ):
            if recomputed[key] > controls.algebraic_tolerance:
                failures.append(f"case[{index}].folding.{key}")
        null_expected = self._null_metrics(
            hamiltonian,
            nx,
            ny,
            controls.translation,
            controls.phase_steps,
            controls.energy_shift,
        )
        retained_null = self._decoder.mapping(
            record["null_extraction"], "null_extraction"
        )
        for key, expected_value in null_expected.items():
            observed = self._decoder.number(retained_null[key], key)
            np.testing.assert_allclose(
                observed,
                expected_value,
                rtol=controls.independent_relative_tolerance,
                atol=5.0e-13,
            )
            maximum_difference = max(maximum_difference, abs(observed - expected_value))
            if expected_value > controls.algebraic_tolerance:
                failures.append(f"case[{index}].null.{key}")
        return maximum_difference, failures

    @staticmethod
    def _seam_shift(size: int, displacement: int, twist: float) -> ComplexMatrix:
        result = np.zeros((size, size), dtype=np.complex128)
        for source in range(size):
            quotient, target = divmod(source + displacement, size)
            result[source, target] = np.exp(2.0j * np.pi * quotient * twist)
        return result

    @staticmethod
    def _fourier(size: int, twist: float) -> ComplexMatrix:
        positions = np.arange(size, dtype=np.float64)[:, np.newaxis]
        indices = np.arange(size, dtype=np.float64)[np.newaxis, :]
        result: ComplexMatrix = np.exp(
            2.0j * np.pi * positions * (indices + twist) / float(size)
        ).astype(np.complex128)
        result /= np.sqrt(float(size))
        return result

    @staticmethod
    def _energy_grid(
        nx: int,
        ny: int,
        phi_x: float,
        phi_y: float,
        coefficients: tuple[ParentCoefficient, ...],
    ) -> npt.NDArray[np.float64]:
        kx = (np.arange(nx, dtype=np.float64) + phi_x) / float(nx)
        ky = (np.arange(ny, dtype=np.float64) + phi_y) / float(ny)
        values = np.zeros((nx, ny), dtype=np.complex128)
        for coefficient in coefficients:
            values += coefficient.amplitude * np.exp(
                2.0j
                * np.pi
                * (
                    coefficient.displacement_x * kx[:, np.newaxis]
                    + coefficient.displacement_y * ky[np.newaxis, :]
                )
            )
        if np.max(np.abs(values.imag)) > 1.0e-11:
            raise ValueError("independent primitive energy is not real")
        return values.real.reshape(nx * ny)

    def _null_metrics(
        self,
        pristine: ComplexMatrix,
        nx: int,
        ny: int,
        translation: tuple[int, int],
        phase_steps: tuple[float, float],
        energy_shift: float,
    ) -> dict[str, float]:
        permutation_x = self._forward_permutation(nx, translation[0])
        permutation_y = self._forward_permutation(ny, translation[1])
        permutation = np.kron(permutation_x, permutation_y)
        x = np.repeat(np.arange(nx, dtype=np.float64), ny)
        y = np.tile(np.arange(ny, dtype=np.float64), nx)
        diagonal = np.diag(np.exp(1.0j * (phase_steps[0] * x + phase_steps[1] * y)))
        transform = permutation @ diagonal
        identity = np.eye(nx * ny, dtype=np.complex128)
        raw = transform @ pristine @ transform.conj().T + energy_shift * identity
        recovered = (
            transform.conj().T @ (raw - energy_shift * identity) @ transform - pristine
        )
        return {
            "transform_unitarity_maximum_absolute_defect": self._maximum_absolute(
                transform.conj().T @ transform - identity
            ),
            "recovered_maximum_absolute_defect": self._maximum_absolute(recovered),
            "recovered_frobenius_defect": float(np.linalg.norm(recovered, ord="fro")),
        }

    @staticmethod
    def _forward_permutation(size: int, displacement: int) -> ComplexMatrix:
        result = np.zeros((size, size), dtype=np.complex128)
        for source in range(size):
            result[(source + displacement) % size, source] = 1.0
        return result

    def _verify_seam_oracle(
        self, value: JsonValue, control: VerificationSeamOracle
    ) -> None:
        record = self._decoder.mapping(value, "seam_phase_oracle")
        if self._decoder.integer(record["size"], "seam size") != control.size:
            raise ValueError("seam oracle size differs from the accepted design")
        if self._decoder.number(record["twist_turns"], "seam twist") != control.twist:
            raise ValueError("seam oracle twist differs from the accepted design")
        cases = self._decoder.records(record["cases"], "seam cases")
        expected = (
            (
                "noncrossing",
                control.noncrossing_source,
                1,
                1.0 + 0.0j,
            ),
            (
                "positive_crossing",
                control.positive_crossing_source,
                control.positive_displacement,
                cmath.exp(2.0j * np.pi * control.twist),
            ),
            (
                "negative_crossing",
                control.negative_crossing_source,
                control.negative_displacement,
                cmath.exp(-2.0j * np.pi * control.twist),
            ),
        )
        if len(cases) != len(expected):
            raise ValueError("seam oracle case count differs from the design")
        for case, (name, source, displacement, expected_value) in zip(
            cases, expected, strict=True
        ):
            _, target = divmod(source + displacement, control.size)
            if (
                case["case"] != name
                or self._decoder.integer(case["source"], "seam source") != source
                or self._decoder.integer(case["target"], "seam target") != target
                or self._decoder.integer(case["displacement"], "seam displacement")
                != displacement
            ):
                raise ValueError(f"seam oracle metadata differs for {name}")
            observed = complex(
                self._decoder.number(case["real"], "seam real"),
                self._decoder.number(case["imag"], "seam imag"),
            )
            np.testing.assert_allclose(observed, expected_value, rtol=0.0, atol=5.0e-15)

    def _verify_criterion_record(
        self, value: JsonValue, failures: list[JsonValue]
    ) -> None:
        record = self._decoder.mapping(value, "criterion_evaluation")
        expected_status = "pass" if not failures else "fail"
        if record["status"] != expected_status:
            raise ValueError(
                "criterion status disagrees with independent reconstruction"
            )
        represented = self._decoder.array(record["failed_criteria"], "failed_criteria")
        if represented != failures:
            raise ValueError("failed-criterion inventory disagrees with reconstruction")

    def _verify_stops(
        self, value: JsonValue, expectations: tuple[StopExpectation, ...]
    ) -> None:
        records = self._decoder.records(value, "structured_stops")
        if len(records) != len(expectations):
            raise ValueError("structured stop count differs from the accepted design")
        for record, expectation in zip(records, expectations, strict=True):
            control = self._decoder.text(record["control"], "control")
            pristine = self._metadata(record["pristine_metadata"], "pristine_metadata")
            candidate = self._metadata(
                record["candidate_metadata"], "candidate_metadata"
            )
            if (
                control != expectation.control
                or pristine != expectation.pristine
                or candidate != expectation.candidate
            ):
                raise ValueError(
                    "structured stop inputs differ from the accepted design"
                )
            issue = self._compatibility_issue(pristine, candidate)
            retained_issue = self._decoder.text(record["issue_code"], "issue_code")
            if issue != retained_issue or issue != expectation.expected_issue_code:
                raise ValueError(
                    f"independent stop reconstruction failed for {control}"
                )
            if record.get("residual") is not None:
                raise ValueError("an incompatible control returned a residual")

    @staticmethod
    def _compatibility_issue(
        pristine: VerificationMetadata,
        candidate: VerificationMetadata,
    ) -> str | None:
        if pristine.geometry != candidate.geometry:
            return "DEFECT_2D.GEOMETRY_MISMATCH"
        if pristine.boundary_phase != candidate.boundary_phase:
            return "DEFECT_2D.BOUNDARY_PHASE_MISMATCH"
        if not pristine.site_map_known or not pristine.energy_reference_relation_known:
            raise ValueError("pristine compatibility metadata is unresolved")
        if not candidate.site_map_known:
            return "DEFECT_2D.SITE_MAP_UNRESOLVED"
        if not candidate.energy_reference_relation_known:
            return "DEFECT_2D.ENERGY_REFERENCE_UNKNOWN"
        return None

    def _authorization(self, path: Path) -> VerificationExecutionAuthorization:
        root = self._decoder.load(path)
        expected: dict[str, JsonValue] = {
            "schema_version": 2,
            "authorization_kind": "defect-2d-stage-execution",
            "stage_id": "A_null_and_folding",
            "execution_authorized": True,
        }
        for key, value in expected.items():
            if root.get(key) != value:
                raise ValueError(f"authorization field {key!r} is invalid")
        resources = self._decoder.mapping(
            root["resource_envelope"], "resource_envelope"
        )
        return VerificationExecutionAuthorization(
            authorization_id=self._decoder.text(
                root["authorization_id"], "authorization_id"
            ),
            checkpoint_path=self._decoder.text(
                root["checkpoint_path"], "checkpoint_path"
            ),
            checkpoint_sha256=self._decoder.text(
                root["checkpoint_sha256"], "checkpoint_sha256"
            ),
            repository_root=self._decoder.text(
                root["repository_root"], "repository_root"
            ),
            design_path=self._decoder.text(root["design_path"], "design_path"),
            design_sha256=self._decoder.text(root["design_sha256"], "design_sha256"),
            runner_path=self._decoder.text(root["runner_path"], "runner_path"),
            runner_sha256=self._decoder.text(root["runner_sha256"], "runner_sha256"),
            parent_path=self._decoder.text(root["parent_path"], "parent_path"),
            parent_sha256=self._decoder.text(root["parent_sha256"], "parent_sha256"),
            output_path=self._decoder.text(root["output_path"], "output_path"),
            maximum_matrix_dimension=self._decoder.integer(
                resources["maximum_matrix_dimension"], "maximum_matrix_dimension"
            ),
            maximum_runtime_seconds=self._decoder.integer(
                resources["maximum_runtime_seconds"], "maximum_runtime_seconds"
            ),
            maximum_peak_memory_gib=self._decoder.number(
                resources["maximum_peak_memory_gib"], "maximum_peak_memory_gib"
            ),
            network_access=self._decoder.boolean(
                resources["network_access"], "network_access"
            ),
            human_response_verbatim=self._decoder.text(
                root["human_response_verbatim"], "human_response_verbatim"
            ),
        )

    def _verify_authorization_binding(
        self,
        *,
        authorization: VerificationExecutionAuthorization,
        repository_root: Path,
        result_path: Path,
        design_path: Path,
        parent_path: Path,
        runner_path: Path,
        checkpoint_path: Path,
        controls: VerificationControls,
    ) -> None:
        if authorization.repository_root != str(repository_root):
            raise ValueError("authorization repository root differs")
        expected_design = (
            repository_root
            / "calculations/research-monograph/impurity-defect-2d/study-design.json"
        ).resolve(strict=True)
        expected_runner = (
            repository_root
            / "calculations/research-monograph/impurity-defect-2d/run_stage_a.py"
        ).resolve(strict=True)
        if design_path != expected_design or runner_path != expected_runner:
            raise ValueError("result does not use the authoritative Stage A sources")
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
        for represented, actual, digest in bindings:
            if self._resolve_bound(repository_root, represented) != actual:
                raise ValueError(f"authorization path binding differs for {actual}")
            if self._sha256(actual) != digest:
                raise ValueError(f"authorization digest binding differs for {actual}")
        if (
            self._resolve_bound(repository_root, authorization.output_path)
            != result_path
        ):
            raise ValueError("authorization output binding differs from the result")
        if authorization.parent_sha256 != controls.parent_sha256:
            raise ValueError("authorization parent identity differs from the design")
        maximum_dimension = max(
            case.nx * case.ny for case in controls.folding_expectations
        )
        if authorization.maximum_matrix_dimension != maximum_dimension:
            raise ValueError("authorization matrix dimension differs from Stage A")
        if not 0 < authorization.maximum_runtime_seconds <= 120:
            raise ValueError("authorization runtime exceeds the Stage A envelope")
        if not 0.0 < authorization.maximum_peak_memory_gib <= 2.0:
            raise ValueError("authorization memory exceeds the Stage A envelope")
        if authorization.network_access:
            raise ValueError("Stage A does not authorize network access")
        checkpoint = self._decoder.load(checkpoint_path)
        expected_checkpoint: dict[str, JsonValue] = {
            "status": "resolved",
            "task_id": "research-monograph.exercises.impurity.defect-2d",
            "human_response": authorization.human_response_verbatim,
        }
        for key, value in expected_checkpoint.items():
            if checkpoint.get(key) != value:
                raise ValueError(f"execution checkpoint field {key!r} is invalid")
        self._decoder.text(checkpoint.get("authorized_scope"), "authorized_scope")
        self._decoder.text(checkpoint.get("blocked_scope"), "blocked_scope")
        authoritative = self._decoder.array(
            checkpoint["authoritative_files"], "authoritative_files"
        )
        authoritative_paths = {
            self._decoder.text(item, "authoritative file") for item in authoritative
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
    def _resolve_bound(repository_root: Path, represented: str) -> Path:
        path = Path(represented)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError("retained paths must be canonical repository-relative")
        resolved = (repository_root / path).resolve(strict=True)
        if not resolved.is_relative_to(repository_root):
            raise ValueError("retained path escapes repository root")
        if resolved.relative_to(repository_root).as_posix() != represented:
            raise ValueError("retained path is not canonical")
        return resolved

    @staticmethod
    def _maximum_absolute(value: ComplexMatrix) -> float:
        return float(np.max(np.abs(value), initial=0.0))

    @staticmethod
    def _sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def _assert_digest(self, path: Path, represented: JsonValue) -> None:
        expected = self._decoder.text(represented, f"digest for {path}")
        if self._sha256(path) != expected:
            raise ValueError(f"content identity mismatch for {path}")


def main() -> None:
    """Adapt command-line arguments to the independent verifier."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--result", required=True, type=Path)
    parser.add_argument("--repository-root", required=True, type=Path)
    arguments = parser.parse_args()
    StageAVerifier().execute(arguments.result, arguments.repository_root)


if __name__ == "__main__":
    main()
