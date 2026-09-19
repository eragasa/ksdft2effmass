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
import resource
import subprocess
import sys
import time
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
class ArtifactBinding:
    """Bind one exact repository artifact role, path, and SHA-256 identity."""

    role: str
    path: str
    sha256: str


@dataclass(frozen=True, slots=True)
class StageCAcceptedParentExecutionAuthorization:
    """Represent one future exact protected-execution authorization."""

    authorization_id: str
    checkpoint_path: str
    checkpoint_sha256: str
    human_response_verbatim: str
    repository_root: str
    repository_revision: str
    machine_identity: str
    native_artifact_root: str
    artifacts: tuple[ArtifactBinding, ...]
    operation_inventory: tuple[str, ...]
    attempt_record_path: str
    result_path: str
    verification_log_path: str
    summary_svg_path: str
    report_path: str
    native_evidence_manifest_path: str
    checksum_catalog_path: str
    maximum_matrix_dimension: int
    maximum_execution_schedules: int
    maximum_route_evaluations: int
    maximum_bridge_records: int
    maximum_model_fit_records: int
    maximum_schedule_comparisons: int
    maximum_runtime_seconds: int
    maximum_peak_memory_gib: float
    maximum_retained_output_mib: float
    network_access: bool
    external_executables: tuple[str, ...]
    new_dependencies: tuple[str, ...]
    maximum_attempts: int
    retry_authorized: bool
    overwrite_existing: bool


@dataclass(frozen=True, slots=True)
class StageCResultContext:
    """Own exact claim, authority, source, and resource result metadata."""

    result_id: str
    evidence_status: str
    accepted_parent_read: bool
    source_mode: str
    operation_inventory: tuple[str, ...]
    input_identities: tuple[ArtifactBinding, ...]
    authorization_id: str | None
    authorization_path: str | None
    authorization_sha256: str | None
    checkpoint_path: str | None
    checkpoint_sha256: str | None
    human_response_verbatim: str | None
    repository_root: str | None
    repository_revision: str
    machine_identity: str | None
    native_artifact_root: str
    attempt_record_path: str
    result_path: str
    verification_log_path: str
    summary_svg_path: str
    report_path: str
    native_evidence_manifest_path: str
    checksum_catalog_path: str
    maximum_runtime_seconds: int
    maximum_peak_memory_gib: float
    maximum_retained_output_mib: float
    maximum_attempts: int
    retry_authorized: bool
    overwrite_existing: bool
    started_at: float | None


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

    def read(self, path: Path) -> dict[str, JsonValue]:
        """Read one UTF-8 JSON object from an explicit path."""

        return self.mapping(
            cast(JsonValue, json.loads(path.read_text(encoding="utf-8"))), str(path)
        )

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
        if not isinstance(value, str) or not value:
            raise TypeError(f"{name} must be a nonempty string")
        return value

    def records(
        self, value: JsonValue, name: str
    ) -> tuple[dict[str, JsonValue], ...]:
        records: list[dict[str, JsonValue]] = []
        for index, item in enumerate(self.array(value, name)):
            records.append(self.mapping(item, f"{name}[{index}]"))
        return tuple(records)

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


class AcceptedParentStageCArtifactAdapter:
    """Adapt five closed parent records into the frozen compact parent data."""

    __slots__ = ("_json",)

    def __init__(self) -> None:
        self._json = ParentJsonReader()

    def execute(
        self,
        periodic_input: dict[str, JsonValue],
        periodic_result: dict[str, JsonValue],
        stage_a_result: dict[str, JsonValue],
        stage_b_result: dict[str, JsonValue],
        stage_c_contract: dict[str, JsonValue],
        source_digest: str,
    ) -> ParentFixture:
        """Return compact parent data after exact cross-record checks."""

        versioned_records = (
            ("periodic input", periodic_input),
            ("periodic result", periodic_result),
            ("Stage A result", stage_a_result),
            ("Stage B result", stage_b_result),
            ("Stage C contract", stage_c_contract),
        )
        for name, record in versioned_records:
            if record.get("schema_version") != 1:
                raise ValueError(f"{name} schema version differs")
        anisotropic_input = self._json.mapping(
            periodic_input["anisotropic_control"], "anisotropic input"
        )
        self._validate_anisotropy(anisotropic_input, "periodic input")
        cutoff = self._json.integer(
            periodic_input["plane_wave_reference_cutoff"], "plane-wave cutoff"
        )
        mesh = self._json.integer(
            periodic_input["reciprocal_mesh_size"], "reciprocal mesh"
        )
        if cutoff != 5 or mesh != 15:
            raise ValueError("accepted anisotropic discretization differs")
        anisotropic_result = self._json.mapping(
            periodic_result["anisotropy_control"], "anisotropy result"
        )
        self._validate_anisotropy(anisotropic_result, "periodic result")
        if stage_a_result.get("stage_id") != "A_null_and_folding":
            raise ValueError("Stage A prerequisite identity differs")
        if stage_b_result.get("stage_id") != "B_scalar_onsite_and_D4_multiroute":
            raise ValueError("Stage B parent identity differs")
        if stage_c_contract.get("design_id") != (
            "research-monograph.impurity-defect-2d.stage-c.execution-free.v1"
        ):
            raise ValueError("execution-free Stage C contract identity differs")
        if stage_c_contract.get("status") != (
            "human_authorized_execution_free_design_and_implementation"
        ):
            raise ValueError("execution-free Stage C contract status differs")
        if stage_c_contract.get("execution_authorized_by_this_record") is not False:
            raise ValueError("execution-free Stage C contract grants execution")
        hoppings: list[ParentHopping] = []
        for record in self._json.records(
            stage_b_result["input_hoppings"], "Stage B input hoppings"
        ):
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
            raise ValueError("accepted Stage B compact inventory must contain 61 terms")
        lambda_x = self._json.real(anisotropic_input["lambda_x"], "lambda_x")
        lambda_y = self._json.real(anisotropic_input["lambda_y"], "lambda_y")
        momentum = np.fft.fftfreq(mesh)
        x_energies = tuple(
            self._lowest_band(float(value), lambda_x, cutoff) for value in momentum
        )
        y_energies = tuple(
            self._lowest_band(float(value), lambda_y, cutoff) for value in momentum
        )
        energies = tuple(
            tuple(x_energy + y_energy for y_energy in y_energies)
            for x_energy in x_energies
        )
        return ParentFixture(tuple(hoppings), energies, mesh, 18, source_digest)

    def _validate_anisotropy(
        self, record: dict[str, JsonValue], owner: str
    ) -> None:
        observed = (
            self._json.real(record["lambda_x"], f"{owner} lambda_x"),
            self._json.real(record["lambda_y"], f"{owner} lambda_y"),
            self._json.real(record["lambda_xy"], f"{owner} lambda_xy"),
        )
        if observed != (0.3, 0.7, 0.0):
            raise ValueError(f"{owner} anisotropic parameters differ")

    @staticmethod
    def _lowest_band(momentum: float, strength: float, cutoff: int) -> float:
        indices = np.arange(-cutoff, cutoff + 1, dtype=np.float64)
        matrix = np.diag(np.square(momentum + indices))
        coupling = strength / 2.0
        matrix += np.diag(np.full(2 * cutoff, coupling), 1)
        matrix += np.diag(np.full(2 * cutoff, coupling), -1)
        return float(np.linalg.eigvalsh(matrix)[0])


class AuthoredAcceptedParentAdapterFixtureDeserializer:
    """Decode an authored multi-record fixture through the accepted adapter."""

    __slots__ = ("_adapter", "_json")

    _ROLES: ClassVar[tuple[str, ...]] = (
        "accepted_periodic_parent_input",
        "accepted_periodic_parent_result",
        "accepted_stage_a_prerequisite",
        "accepted_stage_b_parent_and_route_evidence",
        "accepted_execution_free_stage_c_contract",
    )

    def __init__(self) -> None:
        self._adapter = AcceptedParentStageCArtifactAdapter()
        self._json = ParentJsonReader()

    def execute(
        self, path: Path
    ) -> tuple[ParentFixture, tuple[ArtifactBinding, ...]]:
        encoded = path.read_bytes()
        root = self._json.mapping(cast(JsonValue, json.loads(encoded)), "fixture")
        if root.get("schema_version") != 1:
            raise ValueError("adapter fixture schema version differs")
        if root.get("fixture_id") != (
            "research-monograph.impurity-defect-2d.stage-c.accepted-parent."
            "adapter-authored-fixture.v1"
        ):
            raise ValueError("unexpected Stage C adapter fixture")
        if root.get("evidence_status") != (
            "authored synthetic adapter fixture; not accepted-parent evidence"
        ):
            raise ValueError("adapter fixture evidence status differs")
        if self._json.boolean(root["accepted_parent"], "accepted_parent"):
            raise ValueError("accepted-parent artifacts are forbidden in fixture mode")
        sources = self._json.mapping(root["sources"], "sources")
        if set(sources) != set(self._ROLES):
            raise ValueError("adapter fixture source inventory differs")
        records = tuple(
            self._json.mapping(sources[role], role) for role in self._ROLES
        )
        bindings = tuple(
            ArtifactBinding(
                role,
                f"embedded://{role}",
                hashlib.sha256(
                    json.dumps(
                        record, sort_keys=True, separators=(",", ":"), allow_nan=False
                    ).encode("utf-8")
                ).hexdigest(),
            )
            for role, record in zip(self._ROLES, records, strict=True)
        )
        source_digest = hashlib.sha256(
            "".join(binding.sha256 for binding in bindings).encode("ascii")
        ).hexdigest()
        fixture = self._adapter.execute(
            records[0], records[1], records[2], records[3], records[4], source_digest
        )
        if hashlib.sha256(encoded).hexdigest() == source_digest:
            raise ValueError(
                "fixture and normalized source identities must be distinct"
            )
        return fixture, bindings


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


class StageCResultProvenanceSerializer:
    """Serialize exact source, authority, implementation, and resource metadata."""

    __slots__ = ()

    @staticmethod
    def execute(context: StageCResultContext) -> dict[str, JsonValue]:
        runner = Path(__file__).resolve(strict=True)
        implementation_paths = (
            ("runner", runner),
            ("protected_workflow", runner),
            ("verifier", runner.with_name("verify_stage_c_parent.py")),
            ("plotter", runner.with_name("plot_stage_c_parent.py")),
            ("result_schema", runner.with_name("stage-c-result.schema.json")),
            (
                "execution_authorization_schema",
                runner.with_name("stage-c-execution-authorization.schema.json"),
            ),
        )
        repository = (
            Path(context.repository_root)
            if context.repository_root is not None
            else None
        )
        implementation = [
            {
                "role": role,
                "path": (
                    path.relative_to(repository).as_posix()
                    if repository is not None and path.is_relative_to(repository)
                    else path.name
                ),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
            for role, path in implementation_paths
        ]
        authorization: JsonValue
        if context.authorization_id is None:
            authorization = None
        else:
            authorization = {
                "authorization_id": context.authorization_id,
                "authorization_path": context.authorization_path,
                "authorization_sha256": context.authorization_sha256,
                "checkpoint_path": context.checkpoint_path,
                "checkpoint_sha256": context.checkpoint_sha256,
                "human_response_verbatim": context.human_response_verbatim,
            }
        runtime: float | None = None
        peak_memory: int | None = None
        if context.started_at is not None:
            runtime = time.perf_counter() - context.started_at
            usage = max(
                resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
            )
            peak_memory = int(usage if platform.system() == "Darwin" else usage * 1024)
        return {
            "source_mode": context.source_mode,
            "authorization": authorization,
            "repository": {
                "root": context.repository_root,
                "revision": context.repository_revision,
                "machine_identity": context.machine_identity,
                "native_artifact_root": context.native_artifact_root,
            },
            "operation_inventory": list(context.operation_inventory),
            "input_identities": [
                {"role": value.role, "path": value.path, "sha256": value.sha256}
                for value in context.input_identities
            ],
            "implementation_identities": cast(JsonValue, implementation),
            "retained_output_paths": {
                "attempt_record": context.attempt_record_path,
                "result": context.result_path,
                "verification_log": context.verification_log_path,
                "summary_svg": context.summary_svg_path,
                "report": context.report_path,
                "native_evidence_manifest": context.native_evidence_manifest_path,
                "checksum_catalog": context.checksum_catalog_path,
            },
            "resource_envelope": {
                "maximum_runtime_seconds": context.maximum_runtime_seconds,
                "maximum_peak_memory_gib": context.maximum_peak_memory_gib,
                "maximum_retained_output_mib": context.maximum_retained_output_mib,
                "network_access": False,
                "external_executables": [],
                "new_dependencies": [],
            },
            "attempt_policy": {
                "maximum_attempts": context.maximum_attempts,
                "retry_authorized": context.retry_authorized,
                "overwrite_existing": context.overwrite_existing,
            },
            "execution_observation": {
                "runtime_seconds": runtime,
                "peak_memory_bytes": peak_memory,
                "output_bytes": 0,
            },
        }


class AcceptedParentStageCEvaluator:
    """Compose two fresh schedules and evaluate the adopted contract."""

    __slots__ = ()

    def execute(
        self,
        controls: ParentControls,
        fixture: ParentFixture,
        design_sha256: str,
        context: StageCResultContext,
    ) -> dict[str, JsonValue]:
        schedules = (
            ("A_then_B", ("A_centered_uniform", "B_reduced_seam")),
            ("B_then_A", ("B_reduced_seam", "A_centered_uniform")),
        )
        process_context = multiprocessing.get_context("spawn")
        action = ParentScheduleExecutor()
        with (
            concurrent.futures.ProcessPoolExecutor(
                max_workers=1, mp_context=process_context
            ) as first_executor,
            concurrent.futures.ProcessPoolExecutor(
                max_workers=1, mp_context=process_context
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
            "result_id": context.result_id,
            "evidence_status": context.evidence_status,
            "accepted_parent_read": context.accepted_parent_read,
            "design_sha256": design_sha256,
            "fixture_sha256": fixture.fixture_sha256,
            "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "provenance": StageCResultProvenanceSerializer.execute(context),
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


class AcceptedParentStageCExecutionAuthorizationDeserializer:
    """Deserialize the exact closed future execution-authorization record."""

    __slots__ = ("_json",)

    _ARTIFACT_BINDINGS: ClassVar[tuple[tuple[str, str], ...]] = (
        (
            "accepted_parent_design",
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-c-accepted-parent-design.json",
        ),
        (
            "runner",
            "calculations/research-monograph/impurity-defect-2d/"
            "run_stage_c_parent.py",
        ),
        (
            "protected_workflow",
            "calculations/research-monograph/impurity-defect-2d/"
            "run_stage_c_parent.py",
        ),
        (
            "verifier",
            "calculations/research-monograph/impurity-defect-2d/"
            "verify_stage_c_parent.py",
        ),
        (
            "plotter",
            "calculations/research-monograph/impurity-defect-2d/"
            "plot_stage_c_parent.py",
        ),
        (
            "result_schema",
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-c-result.schema.json",
        ),
        (
            "execution_authorization_schema",
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-c-execution-authorization.schema.json",
        ),
        (
            "accepted_periodic_parent_input",
            "calculations/research-monograph/periodic-2d/input.json",
        ),
        (
            "accepted_periodic_parent_result",
            "calculations/research-monograph/periodic-2d/result.json",
        ),
        (
            "accepted_stage_a_prerequisite",
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-a-result.json",
        ),
        (
            "accepted_stage_b_parent_and_route_evidence",
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-b-result.json",
        ),
        (
            "accepted_execution_free_stage_c_contract",
            "calculations/research-monograph/impurity-defect-2d/stage-c-design.json",
        ),
    )
    OPERATION_INVENTORY: ClassVar[tuple[str, ...]] = (
        "validate_authority",
        "consume_attempt",
        "validate_accepted_input_identities",
        "evaluate_stage_c",
        "serialize_result",
        "independently_verify_result",
        "render_summary_svg",
        "write_report",
        "write_native_evidence_manifest",
        "write_checksum_catalog",
        "finalize_attempt",
    )

    def __init__(self) -> None:
        self._json = ParentJsonReader()

    def execute(self, path: Path) -> StageCAcceptedParentExecutionAuthorization:
        root = self._json.read(path)
        expected_keys = {
            "schema_version",
            "authorization_kind",
            "stage_id",
            "execution_authorized",
            "authorization_id",
            "checkpoint",
            "repository",
            "artifacts",
            "operation_inventory",
            "outputs",
            "resource_envelope",
            "attempt_policy",
        }
        if set(root) != expected_keys:
            raise ValueError("execution authorization field inventory differs")
        expected: dict[str, JsonValue] = {
            "schema_version": 1,
            "authorization_kind": "defect-2d-stage-c-accepted-parent-execution",
            "stage_id": "C_directional_and_nonlocal_model_classes",
            "execution_authorized": True,
        }
        for key, value in expected.items():
            if root.get(key) != value:
                raise ValueError(f"execution authorization field {key!r} differs")
        checkpoint = self._json.mapping(root["checkpoint"], "checkpoint")
        repository = self._json.mapping(root["repository"], "repository")
        outputs = self._json.mapping(root["outputs"], "outputs")
        resources = self._json.mapping(root["resource_envelope"], "resources")
        attempt = self._json.mapping(root["attempt_policy"], "attempt policy")
        artifact_records = self._json.records(root["artifacts"], "artifacts")
        operation_inventory = tuple(
            self._json.text(value, "operation")
            for value in self._json.array(
                root["operation_inventory"], "operation inventory"
            )
        )
        if operation_inventory != self.OPERATION_INVENTORY:
            raise ValueError("execution operation inventory differs")
        self._require_exact_keys(
            checkpoint,
            {"path", "sha256", "human_response_verbatim"},
            "checkpoint",
        )
        self._require_exact_keys(
            repository,
            {"root", "revision", "machine_identity", "native_artifact_root"},
            "repository",
        )
        self._require_exact_keys(
            outputs,
            {
                "attempt_record",
                "result",
                "verification_log",
                "summary_svg",
                "report",
                "native_evidence_manifest",
                "checksum_catalog",
            },
            "outputs",
        )
        self._require_exact_keys(
            resources,
            {
                "maximum_matrix_dimension",
                "maximum_execution_schedules",
                "maximum_route_evaluations",
                "maximum_bridge_records",
                "maximum_model_fit_records",
                "maximum_schedule_comparisons",
                "maximum_runtime_seconds",
                "maximum_peak_memory_gib",
                "maximum_retained_output_mib",
                "network_access",
                "external_executables",
                "new_dependencies",
            },
            "resource envelope",
        )
        self._require_exact_keys(
            attempt,
            {"maximum_attempts", "retry_authorized", "overwrite_existing"},
            "attempt policy",
        )
        for record in artifact_records:
            self._require_exact_keys(record, {"role", "path", "sha256"}, "artifact")
        artifacts = tuple(
            ArtifactBinding(
                self._json.text(record["role"], "artifact role"),
                self._json.text(record["path"], "artifact path"),
                self._sha256(record["sha256"], "artifact sha256"),
            )
            for record in artifact_records
        )
        if tuple((value.role, value.path) for value in artifacts) != (
            self._ARTIFACT_BINDINGS
        ):
            raise ValueError("execution authorization artifact bindings differ")
        external = tuple(
            self._json.text(value, "external executable")
            for value in self._json.array(
                resources["external_executables"], "external executables"
            )
        )
        dependencies = tuple(
            self._json.text(value, "new dependency")
            for value in self._json.array(resources["new_dependencies"], "dependencies")
        )
        return StageCAcceptedParentExecutionAuthorization(
            authorization_id=self._json.text(
                root["authorization_id"], "authorization_id"
            ),
            checkpoint_path=self._json.text(checkpoint["path"], "checkpoint path"),
            checkpoint_sha256=self._sha256(
                checkpoint["sha256"], "checkpoint sha256"
            ),
            human_response_verbatim=self._json.text(
                checkpoint["human_response_verbatim"], "human response"
            ),
            repository_root=self._json.text(repository["root"], "repository root"),
            repository_revision=self._revision(repository["revision"]),
            machine_identity=self._json.text(
                repository["machine_identity"], "machine identity"
            ),
            native_artifact_root=self._json.text(
                repository["native_artifact_root"], "native artifact root"
            ),
            artifacts=artifacts,
            operation_inventory=operation_inventory,
            attempt_record_path=self._json.text(
                outputs["attempt_record"], "attempt record path"
            ),
            result_path=self._json.text(outputs["result"], "result path"),
            verification_log_path=self._json.text(
                outputs["verification_log"], "verification log path"
            ),
            summary_svg_path=self._json.text(
                outputs["summary_svg"], "summary SVG path"
            ),
            report_path=self._json.text(outputs["report"], "report path"),
            native_evidence_manifest_path=self._json.text(
                outputs["native_evidence_manifest"], "native manifest path"
            ),
            checksum_catalog_path=self._json.text(
                outputs["checksum_catalog"], "checksum catalog path"
            ),
            maximum_matrix_dimension=self._json.integer(
                resources["maximum_matrix_dimension"], "maximum matrix dimension"
            ),
            maximum_execution_schedules=self._json.integer(
                resources["maximum_execution_schedules"], "maximum schedules"
            ),
            maximum_route_evaluations=self._json.integer(
                resources["maximum_route_evaluations"], "maximum route evaluations"
            ),
            maximum_bridge_records=self._json.integer(
                resources["maximum_bridge_records"], "maximum bridge records"
            ),
            maximum_model_fit_records=self._json.integer(
                resources["maximum_model_fit_records"], "maximum model fits"
            ),
            maximum_schedule_comparisons=self._json.integer(
                resources["maximum_schedule_comparisons"],
                "maximum schedule comparisons",
            ),
            maximum_runtime_seconds=self._json.integer(
                resources["maximum_runtime_seconds"], "maximum runtime"
            ),
            maximum_peak_memory_gib=self._json.real(
                resources["maximum_peak_memory_gib"], "maximum memory"
            ),
            maximum_retained_output_mib=self._json.real(
                resources["maximum_retained_output_mib"], "maximum output"
            ),
            network_access=self._json.boolean(
                resources["network_access"], "network access"
            ),
            external_executables=external,
            new_dependencies=dependencies,
            maximum_attempts=self._json.integer(
                attempt["maximum_attempts"], "maximum attempts"
            ),
            retry_authorized=self._json.boolean(
                attempt["retry_authorized"], "retry authorized"
            ),
            overwrite_existing=self._json.boolean(
                attempt["overwrite_existing"], "overwrite existing"
            ),
        )

    @staticmethod
    def _require_exact_keys(
        value: dict[str, JsonValue], expected: set[str], label: str
    ) -> None:
        if set(value) != expected:
            raise ValueError(f"{label} must use the exact closed fields")

    def _revision(self, value: JsonValue) -> str:
        revision = self._json.text(value, "repository revision")
        if len(revision) not in (40, 64) or any(
            character not in "0123456789abcdef" for character in revision
        ):
            raise ValueError("repository revision is not a lowercase object ID")
        return revision

    def _sha256(self, value: JsonValue, name: str) -> str:
        digest = self._json.text(value, name)
        if len(digest) != 64 or any(
            character not in "0123456789abcdef" for character in digest
        ):
            raise ValueError(f"{name} is not lowercase SHA-256")
        return digest


@dataclass(frozen=True, slots=True)
class StageCOperationPaths:
    """Own canonical retained paths for one complete protected operation."""

    attempt_record: Path
    result: Path
    verification_log: Path
    summary_svg: Path
    report: Path
    native_evidence_manifest: Path
    checksum_catalog: Path

    @classmethod
    def authored(cls, directory: Path) -> StageCOperationPaths:
        """Return the complete authored-sandbox retained path inventory."""

        return cls(
            directory / "stage-c-accepted-parent-attempt.jsonl",
            directory / "stage-c-accepted-parent-result.json",
            directory / "stage-c-accepted-parent-verification.log",
            directory / "stage-c-accepted-parent-summary.svg",
            directory / "stage-c-accepted-parent-report.md",
            directory / "stage-c-accepted-parent-native-evidence-manifest.json",
            directory / "stage-c-accepted-parent-SHA256SUMS",
        )

    def produced_outputs(self) -> tuple[tuple[str, Path], ...]:
        """Return outputs covered by the finalized checksum catalog."""

        return (
            ("result", self.result),
            ("verification_log", self.verification_log),
            ("summary_svg", self.summary_svg),
            ("report", self.report),
            ("native_evidence_manifest", self.native_evidence_manifest),
        )


@dataclass(frozen=True, slots=True)
class ValidatedStageCExecution:
    """Carry validated authority, canonical artifacts, and retained paths."""

    authorization: StageCAcceptedParentExecutionAuthorization
    authorization_path: Path
    artifact_paths: tuple[tuple[str, Path], ...]
    outputs: StageCOperationPaths


class AcceptedParentStageCAuthorityValidator:
    """Validate complete authority before semantic accepted-parent reads."""

    __slots__ = ("_deserializer", "_json")

    DATA_ROLES: ClassVar[frozenset[str]] = frozenset(
        {
            "accepted_periodic_parent_input",
            "accepted_periodic_parent_result",
            "accepted_stage_a_prerequisite",
            "accepted_stage_b_parent_and_route_evidence",
            "accepted_execution_free_stage_c_contract",
        }
    )

    def __init__(self) -> None:
        self._deserializer = AcceptedParentStageCExecutionAuthorizationDeserializer()
        self._json = ParentJsonReader()

    def execute(
        self,
        design_path: Path,
        authorization_path: Path,
        repository_root: Path,
        output_path: Path,
    ) -> ValidatedStageCExecution:
        root = repository_root.resolve(strict=True)
        if not repository_root.is_absolute() or root != repository_root:
            raise ValueError("repository root must be canonical and absolute")
        authorization_file = self._existing(root, authorization_path)
        if authorization_file.relative_to(root).as_posix() != (
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-c-accepted-parent-execution-authorization.json"
        ):
            raise ValueError("execution authorization path differs")
        authorization = self._deserializer.execute(authorization_file)
        if authorization.authorization_id != (
            "research-monograph.impurity-defect-2d.stage-c."
            "accepted-parent-execution.hc17.v1"
        ):
            raise ValueError("execution authorization identity differs")
        if authorization.checkpoint_path != (
            ".pi/checkpoints/research-monograph-impurity-defect-2d-"
            "stage-c-accepted-parent-execution.json"
        ):
            raise ValueError("execution checkpoint path differs")
        if authorization.repository_root != (
            "/Users/eugene/worktrees/ksdft2effmass-calculations"
        ) or authorization.repository_root != str(root):
            raise ValueError("authorization repository root differs")
        if authorization.repository_revision != (
            "9def2718ee763faf2060eb692739600485de5c72"
        ) or authorization.repository_revision != self.repository_revision(root):
            raise ValueError("authorization repository revision differs")
        if authorization.machine_identity != "minerva" or (
            authorization.machine_identity != platform.node()
        ):
            raise ValueError("authorization machine identity differs")
        if authorization.native_artifact_root != (
            "/Users/eugene/projects/ksdft2effmass"
        ):
            raise ValueError("authorization native artifact root differs")
        native_root = Path(authorization.native_artifact_root).resolve(strict=True)
        if str(native_root) != authorization.native_artifact_root:
            raise ValueError("native artifact root must be canonical and existing")
        self._validate_resources(authorization)
        actual_outputs = (
            authorization.attempt_record_path,
            authorization.result_path,
            authorization.verification_log_path,
            authorization.summary_svg_path,
            authorization.report_path,
            authorization.native_evidence_manifest_path,
            authorization.checksum_catalog_path,
        )
        expected_outputs = (
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-c-accepted-parent-attempt.jsonl",
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-c-accepted-parent-result.json",
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-c-accepted-parent-verification.log",
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-c-accepted-parent-summary.svg",
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-c-accepted-parent-report.md",
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-c-accepted-parent-native-evidence-manifest.json",
            "calculations/research-monograph/impurity-defect-2d/"
            "stage-c-accepted-parent-SHA256SUMS",
        )
        if actual_outputs != expected_outputs:
            raise ValueError("authorization retained output paths differ")
        resolved_outputs = tuple(
            self._bound_output(root, represented) for represented in actual_outputs
        )
        outputs = StageCOperationPaths(*resolved_outputs)
        actual_output = self._output(root, output_path)
        if actual_output != outputs.result:
            raise ValueError("authorization result path differs")
        for retained in resolved_outputs:
            if retained.exists():
                raise FileExistsError(
                    f"refusing consumed or existing output {retained}"
                )
        bindings = {value.role: value for value in authorization.artifacts}
        implementation_paths = {
            "accepted_parent_design": self._existing(root, design_path),
            "runner": Path(__file__).resolve(strict=True),
            "protected_workflow": Path(__file__).resolve(strict=True),
            "verifier": Path(__file__).with_name("verify_stage_c_parent.py").resolve(
                strict=True
            ),
            "plotter": Path(__file__).with_name("plot_stage_c_parent.py").resolve(
                strict=True
            ),
            "result_schema": Path(__file__).with_name(
                "stage-c-result.schema.json"
            ).resolve(strict=True),
            "execution_authorization_schema": Path(__file__).with_name(
                "stage-c-execution-authorization.schema.json"
            ).resolve(strict=True),
        }
        artifact_paths: list[tuple[str, Path]] = []
        for role, path in implementation_paths.items():
            binding = bindings[role]
            self._validate_binding(root, binding, path)
            artifact_paths.append((role, path))
        checkpoint = self._bound_existing(root, authorization.checkpoint_path)
        if hashlib.sha256(checkpoint.read_bytes()).hexdigest() != (
            authorization.checkpoint_sha256
        ):
            raise ValueError("execution checkpoint identity differs")
        checkpoint_record = self._json.read(checkpoint)
        if checkpoint_record.get("status") != "resolved":
            raise ValueError("execution checkpoint is not resolved")
        if checkpoint_record.get("task_id") != (
            "research-monograph.exercises.impurity.defect-2d"
        ):
            raise ValueError("execution checkpoint task differs")
        if checkpoint_record.get("normalized_decision") != (
            "AUTHORIZE_ONE_ACCEPTED_PARENT_STAGE_C_EXECUTION"
        ):
            raise ValueError("checkpoint does not authorize accepted-parent Stage C")
        if checkpoint_record.get("human_response") != (
            authorization.human_response_verbatim
        ):
            raise ValueError("execution checkpoint response differs")
        artifact_paths.append(("checkpoint", checkpoint))
        for binding in authorization.artifacts:
            if binding.role in self.DATA_ROLES:
                artifact_paths.append(
                    (binding.role, self._bound_existing(root, binding.path))
                )
        return ValidatedStageCExecution(
            authorization, authorization_file, tuple(artifact_paths), outputs
        )

    @staticmethod
    def validate_accepted_input_identities(
        execution: ValidatedStageCExecution,
    ) -> None:
        bindings = {value.role: value for value in execution.authorization.artifacts}
        for role, path in execution.artifact_paths:
            if role not in AcceptedParentStageCAuthorityValidator.DATA_ROLES:
                continue
            if hashlib.sha256(path.read_bytes()).hexdigest() != bindings[role].sha256:
                raise ValueError(f"accepted input identity differs for {role}")

    @staticmethod
    def path(execution: ValidatedStageCExecution, role: str) -> Path:
        matches = tuple(
            path for found, path in execution.artifact_paths if found == role
        )
        if len(matches) != 1:
            raise ValueError(f"validated artifact {role!r} is not unique")
        return matches[0]

    def _validate_resources(
        self, authorization: StageCAcceptedParentExecutionAuthorization
    ) -> None:
        exact = (
            authorization.maximum_matrix_dimension,
            authorization.maximum_execution_schedules,
            authorization.maximum_route_evaluations,
            authorization.maximum_bridge_records,
            authorization.maximum_model_fit_records,
            authorization.maximum_schedule_comparisons,
        )
        if exact != (64, 2, 208, 104, 1040, 104):
            raise ValueError("authorization operation scale differs")
        if not 0 < authorization.maximum_runtime_seconds <= 600:
            raise ValueError("authorization runtime exceeds the design")
        if not 0.0 < authorization.maximum_peak_memory_gib <= 2.0:
            raise ValueError("authorization memory exceeds the design")
        if not 0.0 < authorization.maximum_retained_output_mib <= 20.0:
            raise ValueError("authorization output exceeds the design")
        if authorization.network_access:
            raise ValueError("network access is not authorized")
        if authorization.external_executables:
            raise ValueError("external executables are not authorized")
        if authorization.new_dependencies:
            raise ValueError("new dependencies are not authorized")
        if authorization.maximum_attempts != 1:
            raise ValueError("authorization must bind exactly one attempt")
        if authorization.retry_authorized:
            raise ValueError("retry is not authorized")
        if authorization.overwrite_existing:
            raise ValueError("overwrite is not authorized")

    def _validate_binding(
        self, root: Path, binding: ArtifactBinding, actual: Path
    ) -> None:
        if self._bound_existing(root, binding.path) != actual:
            raise ValueError(f"authorization path differs for {binding.role}")
        if hashlib.sha256(actual.read_bytes()).hexdigest() != binding.sha256:
            raise ValueError(f"authorization identity differs for {binding.role}")

    @staticmethod
    def repository_revision(root: Path) -> str:
        marker = root / ".git"
        if marker.is_file():
            text = marker.read_text().strip()
            prefix = "gitdir: "
            if not text.startswith(prefix):
                raise ValueError("repository gitdir marker differs")
            represented = Path(text.removeprefix(prefix))
            git_directory = (
                represented if represented.is_absolute() else root / represented
            ).resolve(strict=True)
        elif marker.is_dir():
            git_directory = marker.resolve(strict=True)
        else:
            raise ValueError("repository Git metadata is absent")
        head = (git_directory / "HEAD").read_text().strip()
        if not head.startswith("ref: "):
            return AcceptedParentStageCAuthorityValidator._object_id(head)
        reference = head.removeprefix("ref: ")
        common_marker = git_directory / "commondir"
        common_directory = (
            (git_directory / common_marker.read_text().strip()).resolve(strict=True)
            if common_marker.is_file()
            else git_directory
        )
        for directory in (git_directory, common_directory):
            candidate = directory / reference
            if candidate.is_file():
                return AcceptedParentStageCAuthorityValidator._object_id(
                    candidate.read_text().strip()
                )
        packed = common_directory / "packed-refs"
        if packed.is_file():
            for line in packed.read_text().splitlines():
                if not line or line.startswith(("#", "^")):
                    continue
                object_id, represented_reference = line.split(" ", maxsplit=1)
                if represented_reference == reference:
                    return AcceptedParentStageCAuthorityValidator._object_id(object_id)
        raise ValueError("repository HEAD reference is unresolved")

    @staticmethod
    def _object_id(value: str) -> str:
        if len(value) not in (40, 64) or any(
            character not in "0123456789abcdef" for character in value
        ):
            raise ValueError("repository HEAD is not a lowercase object ID")
        return value

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
    def _bound_existing(root: Path, represented: str) -> Path:
        path = Path(represented)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError("bound path must be canonical repository-relative")
        result = (root / path).resolve(strict=True)
        if result.relative_to(root).as_posix() != represented:
            raise ValueError("bound path is not canonical")
        return result

    @staticmethod
    def _bound_output(root: Path, represented: str) -> Path:
        path = Path(represented)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError("bound output must be canonical repository-relative")
        result = (root / path).parent.resolve(strict=True) / path.name
        if not result.is_relative_to(root):
            raise ValueError("bound output escapes repository root")
        if result.relative_to(root).as_posix() != represented:
            raise ValueError("bound output is not canonical")
        return result


class AcceptedParentStageCResultSerializer:
    """Serialize one bounded result deterministically and without overwrite."""

    __slots__ = ()

    @staticmethod
    def execute(
        result: dict[str, JsonValue], output: Path, maximum_bytes: int | None = None
    ) -> None:
        provenance = cast(dict[str, JsonValue], result["provenance"])
        observation = cast(dict[str, JsonValue], provenance["execution_observation"])
        encoded = b""
        for _ in range(4):
            encoded = (
                json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
            ).encode("utf-8")
            if observation["output_bytes"] == len(encoded):
                break
            observation["output_bytes"] = len(encoded)
        if observation["output_bytes"] != len(encoded):
            raise RuntimeError("serialized output-byte identity did not stabilize")
        if maximum_bytes is not None and len(encoded) > maximum_bytes:
            raise ValueError("serialized result exceeds the authorized output bound")
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("xb") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())


class ExclusiveRetainedArtifactWriter:
    """Create one retained artifact exclusively and durably."""

    __slots__ = ()

    @staticmethod
    def execute(path: Path, content: bytes) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())


class StageCAttemptJournal:
    """Consume one attempt atomically and append its terminal identity."""

    __slots__ = ()

    @staticmethod
    def start(
        path: Path,
        authorization_id: str,
        authorization_sha256: str,
        operation_inventory: tuple[str, ...],
        evidence_status: str,
    ) -> str:
        event: dict[str, JsonValue] = {
            "schema_version": 1,
            "event": "STARTED",
            "authorization_id": authorization_id,
            "authorization_sha256": authorization_sha256,
            "operation_inventory": list(operation_inventory),
            "evidence_status": evidence_status,
        }
        encoded = StageCAttemptJournal._encode(event)
        ExclusiveRetainedArtifactWriter.execute(path, encoded)
        return hashlib.sha256(encoded).hexdigest()

    @staticmethod
    def succeed(
        path: Path,
        started_sha256: str,
        outputs: tuple[tuple[str, Path], ...],
    ) -> None:
        identities: list[JsonValue] = [
            {
                "role": role,
                "path": output.name,
                "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
                "bytes": output.stat().st_size,
            }
            for role, output in outputs
        ]
        StageCAttemptJournal._append(
            path,
            {
                "schema_version": 1,
                "event": "TERMINAL",
                "status": "SUCCESS",
                "started_event_sha256": started_sha256,
                "output_identities": identities,
                "error": None,
            },
        )

    @staticmethod
    def fail(path: Path, started_sha256: str, error: BaseException) -> None:
        description = f"{type(error).__name__}: {error}"
        StageCAttemptJournal._append(
            path,
            {
                "schema_version": 1,
                "event": "TERMINAL",
                "status": "FAILURE",
                "started_event_sha256": started_sha256,
                "output_identities": [],
                "error": {
                    "type": type(error).__name__,
                    "message": str(error)[:4096],
                    "sha256": hashlib.sha256(description.encode("utf-8")).hexdigest(),
                },
            },
        )

    @staticmethod
    def _append(path: Path, event: dict[str, JsonValue]) -> None:
        with path.open("ab") as stream:
            stream.write(StageCAttemptJournal._encode(event))
            stream.flush()
            os.fsync(stream.fileno())

    @staticmethod
    def _encode(event: dict[str, JsonValue]) -> bytes:
        return (
            json.dumps(event, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n"
        ).encode("utf-8")


class StageCProtectedOperationFinalizer:
    """Produce verification, visualization, report, manifest, and checksums."""

    __slots__ = ()

    @staticmethod
    def verify_accepted(
        execution: ValidatedStageCExecution, repository_root: Path
    ) -> None:
        process = subprocess.run(
            [
                sys.executable,
                str(Path(__file__).with_name("verify_stage_c_parent.py")),
                "--execution-authorization",
                str(execution.authorization_path),
                "--repository-root",
                str(repository_root),
                "--result",
                str(execution.outputs.result),
            ],
            cwd=repository_root,
            check=False,
            capture_output=True,
            text=True,
        )
        if process.returncode != 0:
            raise RuntimeError(f"independent verification failed: {process.stderr}")
        ExclusiveRetainedArtifactWriter.execute(
            execution.outputs.verification_log, process.stdout.encode("utf-8")
        )

    @staticmethod
    def verify_authored(
        design: Path, fixture: Path, result: Path, output: Path, root: Path
    ) -> None:
        process = subprocess.run(
            [
                sys.executable,
                str(Path(__file__).with_name("verify_stage_c_parent.py")),
                "--accepted-parent-design",
                str(design),
                "--authored-adapter-fixture",
                str(fixture),
                "--result",
                str(result),
            ],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )
        if process.returncode != 0:
            raise RuntimeError(
                f"independent authored verification failed: {process.stderr}"
            )
        ExclusiveRetainedArtifactWriter.execute(
            output, process.stdout.encode("utf-8")
        )

    @staticmethod
    def plot(result: Path, output: Path, root: Path) -> None:
        process = subprocess.run(
            [
                sys.executable,
                str(Path(__file__).with_name("plot_stage_c_parent.py")),
                "--result",
                str(result),
                "--output",
                str(output),
            ],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )
        if process.returncode != 0:
            raise RuntimeError(f"summary plotting failed: {process.stderr}")

    @staticmethod
    def report(result: Path, verification: Path, output: Path) -> None:
        payload = cast(JsonValue, json.loads(result.read_text(encoding="utf-8")))
        if not isinstance(payload, dict):
            raise TypeError("retained Stage C result must be an object")
        verification_payload = cast(
            JsonValue, json.loads(verification.read_text(encoding="utf-8"))
        )
        if not isinstance(verification_payload, dict):
            raise TypeError("verification report must be an object")
        accepted = payload.get("accepted_parent_read") is True
        evidence = payload.get("evidence_status")
        summary = payload.get("summary")
        criteria_passed = (
            isinstance(summary, dict) and summary.get("all_criteria_passed") is True
        )
        content = (
            "# Stage C accepted-parent operation report\n\n"
            f"- Accepted-parent read: `{str(accepted).lower()}`\n"
            f"- Evidence status: `{evidence}`\n"
            f"- Runner criteria passed: `{str(criteria_passed).lower()}`\n"
            "- Independent verification: "
            f"`{verification_payload.get('verification')}`\n\n"
            "This compact report does not establish material validation, scientific "
            "validation, uncertainty quantification, publication readiness, or "
            "authority for Stage D.\n"
        )
        ExclusiveRetainedArtifactWriter.execute(output, content.encode("utf-8"))

    @staticmethod
    def manifest(
        result: Path,
        verification: Path,
        svg: Path,
        report: Path,
        output: Path,
        evidence_status: str,
    ) -> None:
        records: list[JsonValue] = [
            {
                "role": role,
                "path": path.name,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "bytes": path.stat().st_size,
            }
            for role, path in (
                ("result", result),
                ("verification_log", verification),
                ("summary_svg", svg),
                ("report", report),
            )
        ]
        payload: dict[str, JsonValue] = {
            "schema_version": 1,
            "manifest_kind": "stage-c-accepted-parent-native-evidence",
            "evidence_status": evidence_status,
            "artifacts": records,
            "dense_matrices_retained": False,
        }
        ExclusiveRetainedArtifactWriter.execute(
            output,
            (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"),
        )

    @staticmethod
    def validate_total_size(outputs: StageCOperationPaths, maximum_bytes: int) -> None:
        retained = tuple(path for _, path in outputs.produced_outputs()) + (
            outputs.checksum_catalog,
            outputs.attempt_record,
        )
        terminal_event_reserve = 64 * 1024
        if (
            sum(path.stat().st_size for path in retained) + terminal_event_reserve
            > maximum_bytes
        ):
            raise ValueError("retained operation package exceeds authorized size")

    @staticmethod
    def checksums(outputs: StageCOperationPaths) -> None:
        lines = [
            f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}"
            for _, path in outputs.produced_outputs()
        ]
        ExclusiveRetainedArtifactWriter.execute(
            outputs.checksum_catalog, ("\n".join(lines) + "\n").encode("utf-8")
        )


class StageCResultContextPreparer:
    """Prepare exact authored or accepted result contexts."""

    __slots__ = ()

    _ATTEMPT = (
        "calculations/research-monograph/impurity-defect-2d/"
        "stage-c-accepted-parent-attempt.jsonl"
    )
    _RESULT = (
        "calculations/research-monograph/impurity-defect-2d/"
        "stage-c-accepted-parent-result.json"
    )
    _VERIFICATION = (
        "calculations/research-monograph/impurity-defect-2d/"
        "stage-c-accepted-parent-verification.log"
    )
    _SVG = (
        "calculations/research-monograph/impurity-defect-2d/"
        "stage-c-accepted-parent-summary.svg"
    )
    _REPORT = (
        "calculations/research-monograph/impurity-defect-2d/"
        "stage-c-accepted-parent-report.md"
    )
    _MANIFEST = (
        "calculations/research-monograph/impurity-defect-2d/"
        "stage-c-accepted-parent-native-evidence-manifest.json"
    )
    _CHECKSUM = (
        "calculations/research-monograph/impurity-defect-2d/"
        "stage-c-accepted-parent-SHA256SUMS"
    )

    @classmethod
    def authored(
        cls,
        result_id: str,
        source_mode: str,
        identities: tuple[ArtifactBinding, ...],
    ) -> StageCResultContext:
        root = Path(__file__).resolve(strict=True).parents[3]
        return StageCResultContext(
            result_id=result_id,
            evidence_status=(
                "authored synthetic execution-free software-verification behavior; "
                "not accepted-parent evidence"
            ),
            accepted_parent_read=False,
            source_mode=source_mode,
            operation_inventory=("evaluate_stage_c", "serialize_result"),
            input_identities=identities,
            authorization_id=None,
            authorization_path=None,
            authorization_sha256=None,
            checkpoint_path=None,
            checkpoint_sha256=None,
            human_response_verbatim=None,
            repository_root=str(root),
            repository_revision=AcceptedParentStageCAuthorityValidator.repository_revision(
                root
            ),
            machine_identity=platform.node(),
            native_artifact_root="/Users/eugene/projects/ksdft2effmass",
            attempt_record_path=cls._ATTEMPT,
            result_path=cls._RESULT,
            verification_log_path=cls._VERIFICATION,
            summary_svg_path=cls._SVG,
            report_path=cls._REPORT,
            native_evidence_manifest_path=cls._MANIFEST,
            checksum_catalog_path=cls._CHECKSUM,
            maximum_runtime_seconds=600,
            maximum_peak_memory_gib=2.0,
            maximum_retained_output_mib=20.0,
            maximum_attempts=0,
            retry_authorized=False,
            overwrite_existing=False,
            started_at=None,
        )

    @staticmethod
    def authored_operation(
        identities: tuple[ArtifactBinding, ...], outputs: StageCOperationPaths
    ) -> StageCResultContext:
        """Prepare a complete nonexecuting authored-operation context."""

        root = Path(__file__).resolve(strict=True).parents[3]
        return StageCResultContext(
            result_id=(
                "research-monograph.impurity-defect-2d.stage-c."
                "accepted-parent-operation-authored-fixture.v1"
            ),
            evidence_status=(
                "authored synthetic complete-operation software-verification "
                "behavior; not accepted-parent evidence"
            ),
            accepted_parent_read=False,
            source_mode="authored_complete_operation_fixture",
            operation_inventory=(
                AcceptedParentStageCExecutionAuthorizationDeserializer.OPERATION_INVENTORY
            ),
            input_identities=identities,
            authorization_id=None,
            authorization_path=None,
            authorization_sha256=None,
            checkpoint_path=None,
            checkpoint_sha256=None,
            human_response_verbatim=None,
            repository_root=str(root),
            repository_revision=AcceptedParentStageCAuthorityValidator.repository_revision(
                root
            ),
            machine_identity=platform.node(),
            native_artifact_root="/Users/eugene/projects/ksdft2effmass",
            attempt_record_path=str(outputs.attempt_record),
            result_path=str(outputs.result),
            verification_log_path=str(outputs.verification_log),
            summary_svg_path=str(outputs.summary_svg),
            report_path=str(outputs.report),
            native_evidence_manifest_path=str(outputs.native_evidence_manifest),
            checksum_catalog_path=str(outputs.checksum_catalog),
            maximum_runtime_seconds=600,
            maximum_peak_memory_gib=2.0,
            maximum_retained_output_mib=20.0,
            maximum_attempts=1,
            retry_authorized=False,
            overwrite_existing=False,
            started_at=None,
        )

    @staticmethod
    def accepted(execution: ValidatedStageCExecution) -> StageCResultContext:
        authorization = execution.authorization
        data_roles = AcceptedParentStageCAuthorityValidator.DATA_ROLES
        identities = tuple(
            value for value in authorization.artifacts if value.role in data_roles
        )
        return StageCResultContext(
            result_id=(
                "research-monograph.impurity-defect-2d.stage-c.accepted-parent.v1"
            ),
            evidence_status=(
                "calculated result from one explicitly authorized accepted-parent "
                "Stage C execution; numerical-verification evidence only, not "
                "material or scientific-validation evidence"
            ),
            accepted_parent_read=True,
            source_mode="accepted_parent_execution",
            operation_inventory=authorization.operation_inventory,
            input_identities=identities,
            authorization_id=authorization.authorization_id,
            authorization_path=execution.authorization_path.relative_to(
                Path(authorization.repository_root)
            ).as_posix(),
            authorization_sha256=hashlib.sha256(
                execution.authorization_path.read_bytes()
            ).hexdigest(),
            checkpoint_path=authorization.checkpoint_path,
            checkpoint_sha256=authorization.checkpoint_sha256,
            human_response_verbatim=authorization.human_response_verbatim,
            repository_root=authorization.repository_root,
            repository_revision=authorization.repository_revision,
            machine_identity=authorization.machine_identity,
            native_artifact_root=authorization.native_artifact_root,
            attempt_record_path=authorization.attempt_record_path,
            result_path=authorization.result_path,
            verification_log_path=authorization.verification_log_path,
            summary_svg_path=authorization.summary_svg_path,
            report_path=authorization.report_path,
            native_evidence_manifest_path=authorization.native_evidence_manifest_path,
            checksum_catalog_path=authorization.checksum_catalog_path,
            maximum_runtime_seconds=authorization.maximum_runtime_seconds,
            maximum_peak_memory_gib=authorization.maximum_peak_memory_gib,
            maximum_retained_output_mib=authorization.maximum_retained_output_mib,
            maximum_attempts=authorization.maximum_attempts,
            retry_authorized=authorization.retry_authorized,
            overwrite_existing=authorization.overwrite_existing,
            started_at=time.perf_counter(),
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
        repository_root = Path(__file__).resolve(strict=True).parents[3]
        identities = (
            ArtifactBinding(
                "authored_parent_fixture",
                fixture.resolve(strict=True)
                .relative_to(repository_root)
                .as_posix(),
                hashlib.sha256(fixture.read_bytes()).hexdigest(),
            ),
        )
        context = StageCResultContextPreparer.authored(
            (
                "research-monograph.impurity-defect-2d.stage-c."
                "accepted-parent-authored-fixture.v1"
            ),
            "authored_parent_fixture",
            identities,
        )
        result = AcceptedParentStageCEvaluator().execute(
            controls, fixture_record, design_sha256, context
        )
        AcceptedParentStageCResultSerializer.execute(result, output)
        return result


class AcceptedParentStageCAdapterFixtureWorkflow:
    """Exercise the accepted-artifact adapter with authored records only."""

    __slots__ = ()

    def execute(
        self, design: Path, fixture: Path, output: Path
    ) -> dict[str, JsonValue]:
        controls, design_sha256 = AcceptedParentStageCDesignDeserializer().execute(
            design
        )
        fixture_record, identities = (
            AuthoredAcceptedParentAdapterFixtureDeserializer().execute(fixture)
        )
        context = StageCResultContextPreparer.authored(
            (
                "research-monograph.impurity-defect-2d.stage-c."
                "accepted-parent-adapter-authored-fixture.v1"
            ),
            "authored_accepted_parent_adapter_fixture",
            identities,
        )
        result = AcceptedParentStageCEvaluator().execute(
            controls, fixture_record, design_sha256, context
        )
        AcceptedParentStageCResultSerializer.execute(result, output)
        return result


class AuthoredStageCOperationWorkflow:
    """Exercise the complete protected operation using authored records only."""

    __slots__ = ()

    def execute(
        self, design: Path, fixture: Path, output_directory: Path
    ) -> dict[str, JsonValue]:
        output_directory.mkdir(parents=True, exist_ok=True)
        outputs = StageCOperationPaths.authored(output_directory.resolve(strict=True))
        inventory = (
            AcceptedParentStageCExecutionAuthorizationDeserializer.OPERATION_INVENTORY
        )
        authorization_sha256 = hashlib.sha256(
            str(fixture.resolve(strict=True)).encode("utf-8")
        ).hexdigest()
        started = StageCAttemptJournal.start(
            outputs.attempt_record,
            "authored.nonexecuting.stage-c.complete-operation.v1",
            authorization_sha256,
            inventory,
            "authored synthetic operation fixture; not execution authority",
        )
        try:
            controls, design_sha256 = AcceptedParentStageCDesignDeserializer().execute(
                design
            )
            fixture_record, identities = (
                AuthoredAcceptedParentAdapterFixtureDeserializer().execute(fixture)
            )
            context = StageCResultContextPreparer.authored_operation(
                identities, outputs
            )
            result = AcceptedParentStageCEvaluator().execute(
                controls, fixture_record, design_sha256, context
            )
            maximum_bytes = 20 * 1024 * 1024
            AcceptedParentStageCResultSerializer.execute(
                result, outputs.result, maximum_bytes
            )
            root = Path(__file__).resolve(strict=True).parents[3]
            StageCProtectedOperationFinalizer.verify_authored(
                design, fixture, outputs.result, outputs.verification_log, root
            )
            StageCProtectedOperationFinalizer.plot(
                outputs.result, outputs.summary_svg, root
            )
            StageCProtectedOperationFinalizer.report(
                outputs.result, outputs.verification_log, outputs.report
            )
            StageCProtectedOperationFinalizer.manifest(
                outputs.result,
                outputs.verification_log,
                outputs.summary_svg,
                outputs.report,
                outputs.native_evidence_manifest,
                "authored synthetic complete-operation evidence; not "
                "accepted-parent evidence",
            )
            StageCProtectedOperationFinalizer.checksums(outputs)
            StageCProtectedOperationFinalizer.validate_total_size(
                outputs, maximum_bytes
            )
            StageCAttemptJournal.succeed(
                outputs.attempt_record,
                started,
                outputs.produced_outputs()
                + (("checksum_catalog", outputs.checksum_catalog),),
            )
            return result
        except BaseException as error:
            StageCAttemptJournal.fail(outputs.attempt_record, started, error)
            raise


class AcceptedParentStageCExecutionWorkflow:
    """Compose one separately authorized accepted-parent operation."""

    __slots__ = ("_adapter", "_authority", "_json")

    def __init__(self) -> None:
        self._adapter = AcceptedParentStageCArtifactAdapter()
        self._authority = AcceptedParentStageCAuthorityValidator()
        self._json = ParentJsonReader()

    def execute(
        self,
        design: Path,
        authorization: Path,
        repository_root: Path,
        output: Path,
    ) -> dict[str, JsonValue]:
        execution = self._authority.execute(
            design, authorization, repository_root, output
        )
        authorization_sha256 = hashlib.sha256(
            execution.authorization_path.read_bytes()
        ).hexdigest()
        started = StageCAttemptJournal.start(
            execution.outputs.attempt_record,
            execution.authorization.authorization_id,
            authorization_sha256,
            execution.authorization.operation_inventory,
            "one protected accepted-parent Stage C attempt consumed",
        )
        try:
            self._authority.validate_accepted_input_identities(execution)
            context = StageCResultContextPreparer.accepted(execution)
            controls, design_sha256 = AcceptedParentStageCDesignDeserializer().execute(
                self._authority.path(execution, "accepted_parent_design")
            )
            source_roles = (
                "accepted_periodic_parent_input",
                "accepted_periodic_parent_result",
                "accepted_stage_a_prerequisite",
                "accepted_stage_b_parent_and_route_evidence",
                "accepted_execution_free_stage_c_contract",
            )
            records = tuple(
                self._json.read(self._authority.path(execution, role))
                for role in source_roles
            )
            digest = hashlib.sha256(
                "".join(
                    value.sha256
                    for value in execution.authorization.artifacts
                    if value.role in source_roles
                ).encode("ascii")
            ).hexdigest()
            fixture = self._adapter.execute(
                records[0], records[1], records[2], records[3], records[4], digest
            )
            original_directory = Path.cwd()
            try:
                os.chdir(execution.authorization.native_artifact_root)
                result = AcceptedParentStageCEvaluator().execute(
                    controls, fixture, design_sha256, context
                )
            finally:
                os.chdir(original_directory)
            self._validate_observed_resources(result, execution.authorization)
            maximum_bytes = int(
                execution.authorization.maximum_retained_output_mib
                * 1024.0
                * 1024.0
            )
            AcceptedParentStageCResultSerializer.execute(
                result, execution.outputs.result, maximum_bytes
            )
            StageCProtectedOperationFinalizer.verify_accepted(
                execution, repository_root
            )
            StageCProtectedOperationFinalizer.plot(
                execution.outputs.result,
                execution.outputs.summary_svg,
                repository_root,
            )
            StageCProtectedOperationFinalizer.report(
                execution.outputs.result,
                execution.outputs.verification_log,
                execution.outputs.report,
            )
            StageCProtectedOperationFinalizer.manifest(
                execution.outputs.result,
                execution.outputs.verification_log,
                execution.outputs.summary_svg,
                execution.outputs.report,
                execution.outputs.native_evidence_manifest,
                "calculated numerical-verification evidence; not scientific validation",
            )
            StageCProtectedOperationFinalizer.checksums(execution.outputs)
            StageCProtectedOperationFinalizer.validate_total_size(
                execution.outputs, maximum_bytes
            )
            StageCAttemptJournal.succeed(
                execution.outputs.attempt_record,
                started,
                execution.outputs.produced_outputs()
                + (("checksum_catalog", execution.outputs.checksum_catalog),),
            )
            return result
        except BaseException as error:
            StageCAttemptJournal.fail(execution.outputs.attempt_record, started, error)
            raise

    @staticmethod
    def _validate_observed_resources(
        result: dict[str, JsonValue],
        authorization: StageCAcceptedParentExecutionAuthorization,
    ) -> None:
        provenance = cast(dict[str, JsonValue], result["provenance"])
        observation = cast(
            dict[str, JsonValue], provenance["execution_observation"]
        )
        runtime = cast(float, observation["runtime_seconds"])
        peak_memory = cast(int, observation["peak_memory_bytes"])
        if runtime > authorization.maximum_runtime_seconds:
            raise TimeoutError("accepted-parent Stage C exceeded authorized runtime")
        maximum_memory = int(
            authorization.maximum_peak_memory_gib * 1024.0 * 1024.0 * 1024.0
        )
        if peak_memory > maximum_memory:
            raise MemoryError("accepted-parent Stage C exceeded authorized memory")


def main() -> None:
    """Adapt argparse inputs into one explicit Stage C parent Workflow."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--accepted-parent-design", type=Path, required=True)
    parser.add_argument("--authored-parent-fixture", type=Path)
    parser.add_argument("--authored-parent-output", type=Path)
    parser.add_argument("--authored-adapter-fixture", type=Path)
    parser.add_argument("--authored-adapter-output", type=Path)
    parser.add_argument("--authored-operation-fixture", type=Path)
    parser.add_argument("--authored-operation-directory", type=Path)
    parser.add_argument("--execution-authorization", type=Path)
    parser.add_argument("--repository-root", type=Path)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    authored_mode = arguments.authored_parent_fixture is not None or (
        arguments.authored_parent_output is not None
    )
    adapter_mode = arguments.authored_adapter_fixture is not None or (
        arguments.authored_adapter_output is not None
    )
    operation_mode = arguments.authored_operation_fixture is not None or (
        arguments.authored_operation_directory is not None
    )
    execution_mode = any(
        value is not None
        for value in (
            arguments.execution_authorization,
            arguments.repository_root,
            arguments.output,
        )
    )
    if sum((authored_mode, adapter_mode, operation_mode, execution_mode)) != 1:
        parser.error(
            "select exactly one authored, adapter, operation, or execution mode"
        )
    if authored_mode:
        if (
            arguments.authored_parent_fixture is None
            or arguments.authored_parent_output is None
        ):
            parser.error("authored mode requires fixture and output")
        result = AcceptedParentStageCToyWorkflow().execute(
            arguments.accepted_parent_design,
            arguments.authored_parent_fixture,
            arguments.authored_parent_output,
        )
    elif adapter_mode:
        if (
            arguments.authored_adapter_fixture is None
            or arguments.authored_adapter_output is None
        ):
            parser.error("adapter mode requires fixture and output")
        result = AcceptedParentStageCAdapterFixtureWorkflow().execute(
            arguments.accepted_parent_design,
            arguments.authored_adapter_fixture,
            arguments.authored_adapter_output,
        )
    elif operation_mode:
        if (
            arguments.authored_operation_fixture is None
            or arguments.authored_operation_directory is None
        ):
            parser.error("authored operation mode requires fixture and directory")
        result = AuthoredStageCOperationWorkflow().execute(
            arguments.accepted_parent_design,
            arguments.authored_operation_fixture,
            arguments.authored_operation_directory,
        )
    else:
        if (
            arguments.execution_authorization is None
            or arguments.repository_root is None
            or arguments.output is None
        ):
            parser.error(
                "execution mode requires authorization, repository root, and output"
            )
        result = AcceptedParentStageCExecutionWorkflow().execute(
            arguments.accepted_parent_design,
            arguments.execution_authorization,
            arguments.repository_root,
            arguments.output,
        )
    inventory = cast(dict[str, JsonValue], result["inventory"])
    summary = cast(dict[str, JsonValue], result["summary"])
    print(
        "stage_c_parent_criteria="
        f"{'PASS' if summary['all_criteria_passed'] else 'FAIL'}"
    )
    print(f"route_evaluations={inventory['route_evaluations']}")
    print(f"model_fit_records={inventory['model_fit_records']}")


if __name__ == "__main__":
    main()
