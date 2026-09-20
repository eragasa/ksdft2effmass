"""Wire decoding and accepted-artifact adaptation for Stage C."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import ClassVar, cast

import numpy as np

from .model import (
    ArtifactBinding,
    FloatPair,
    IntPair,
    JsonValue,
    LocalBond,
    ParentControls,
    ParentFixture,
    ParentHopping,
    PointOperation,
)


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

    def records(self, value: JsonValue, name: str) -> tuple[dict[str, JsonValue], ...]:
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

    def _validate_anisotropy(self, record: dict[str, JsonValue], owner: str) -> None:
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

    def execute(self, path: Path) -> tuple[ParentFixture, tuple[ArtifactBinding, ...]]:
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
        records = tuple(self._json.mapping(sources[role], role) for role in self._ROLES)
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
