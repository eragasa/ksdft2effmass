"""Run the synthetic blind-alignment follow-on experiment."""

from __future__ import annotations

import hashlib
import json
import platform
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, cast

import numpy as np
import numpy.typing as npt

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type ComplexMatrix = npt.NDArray[np.complex128]
type RealVector = npt.NDArray[np.float64]
type AlignmentStatus = Literal["aligned_full", "aligned_partial", "stopped"]


@dataclass(frozen=True, slots=True)
class InferencePolicy:
    """Represent frozen alignment inference and stopping thresholds."""

    anchor_rank_tolerance: float
    maximum_anchor_condition_number: float
    maximum_principal_angle_radians: float
    minimum_energy_anchor_rank: int
    core_radius_cells: int

    def __post_init__(self) -> None:
        values = (
            self.anchor_rank_tolerance,
            self.maximum_anchor_condition_number,
            self.maximum_principal_angle_radians,
        )
        if any(not np.isfinite(value) or value <= 0.0 for value in values):
            raise ValueError("inference thresholds must be positive and finite")
        if self.minimum_energy_anchor_rank < 1 or self.core_radius_cells < 0:
            raise ValueError("anchor rank and core radius must be nonnegative")


@dataclass(frozen=True, slots=True)
class ObservationInformationContract:
    """Declare which labels and anchors inference may observe."""

    anchor_cross_covariance: str
    site_anchor_labels: str
    orbital_labels: str
    spin_frame: str
    energy_reference: str

    def __post_init__(self) -> None:
        expected = (
            "available_as_authored_matrix",
            "available_on_reference_rows_only",
            "available_on_reference_rows_only",
            "reference_frame_labels_available_candidate_rotation_hidden",
            "exterior_projector_available_scalar_shift_hidden",
        )
        if (
            self.anchor_cross_covariance,
            self.site_anchor_labels,
            self.orbital_labels,
            self.spin_frame,
            self.energy_reference,
        ) != expected:
            raise ValueError("observation information contract is unsupported")

    def as_json(self) -> dict[str, JsonValue]:
        """Return the declared contract as a deterministic JSON record."""
        return {
            "anchor_cross_covariance": self.anchor_cross_covariance,
            "site_anchor_labels": self.site_anchor_labels,
            "orbital_labels": self.orbital_labels,
            "spin_frame": self.spin_frame,
            "energy_reference": self.energy_reference,
        }


@dataclass(frozen=True, slots=True)
class SourceIdentity:
    """Identify one immutable baseline artifact."""

    path: str
    sha256: str

    def __post_init__(self) -> None:
        if not self.path or len(self.sha256) != 64:
            raise ValueError("source path and SHA-256 identity are required")


@dataclass(frozen=True, slots=True)
class NamedDefect:
    """Retain one immutable planted operator and its spin factor."""

    identifier: str
    spin_count: int
    matrix: ComplexMatrix

    def __post_init__(self) -> None:
        if not self.identifier or self.spin_count not in (1, 2):
            raise ValueError("defect identity and spin count are invalid")
        value = np.asarray(self.matrix, dtype=np.complex128)
        if value.ndim != 2 or not np.all(np.isfinite(value)):
            raise ValueError("defect matrix must be finite and two-dimensional")
        immutable = np.frombuffer(
            value.tobytes(order="C"), dtype=np.complex128
        ).reshape(value.shape)
        object.__setattr__(self, "matrix", immutable)


@dataclass(frozen=True, slots=True)
class BaselineData:
    """Retain the accepted parent, defects, hidden maps, and scalar shift."""

    cell_count: int
    reduced_momentum: float
    pristine_spinless: ComplexMatrix
    candidate_to_reference_spinless: ComplexMatrix
    candidate_to_reference_spinor: ComplexMatrix
    energy_shift: float
    defects: tuple[NamedDefect, ...]
    source_identities: tuple[SourceIdentity, ...]

    def __post_init__(self) -> None:
        if self.cell_count < 1 or not np.isfinite(self.reduced_momentum):
            raise ValueError("baseline geometry is invalid")
        if not np.isfinite(self.energy_shift):
            raise ValueError("baseline energy shift must be finite")
        for name in (
            "pristine_spinless",
            "candidate_to_reference_spinless",
            "candidate_to_reference_spinor",
        ):
            value = np.asarray(getattr(self, name), dtype=np.complex128)
            if value.ndim != 2 or not np.all(np.isfinite(value)):
                raise ValueError(f"{name} must be finite and two-dimensional")
            immutable = np.frombuffer(
                value.tobytes(order="C"), dtype=np.complex128
            ).reshape(value.shape)
            object.__setattr__(self, name, immutable)

    def defect(self, identifier: str) -> NamedDefect:
        """Return the uniquely identified planted defect."""
        matches = tuple(item for item in self.defects if item.identifier == identifier)
        if len(matches) != 1:
            raise ValueError(f"baseline defect must occur exactly once: {identifier}")
        return matches[0]


@dataclass(frozen=True, slots=True)
class BlindAlignmentObservation:
    """Represent only information available to the inference action."""

    identifier: str
    reference_hamiltonian: ComplexMatrix
    candidate_hamiltonian: ComplexMatrix
    anchor_cross_covariance: ComplexMatrix
    retained_subspace_overlap: ComplexMatrix
    exterior_energy_anchor: ComplexMatrix
    reference_spin_count: int
    candidate_spin_count: int
    allow_partial_alignment: bool

    def __post_init__(self) -> None:
        if not self.identifier:
            raise ValueError("observation identifier must be nonempty")
        if self.reference_spin_count < 1 or self.candidate_spin_count < 1:
            raise ValueError("spin counts must be positive")
        if type(self.allow_partial_alignment) is not bool:
            raise TypeError("allow_partial_alignment must be Boolean")
        for name in (
            "reference_hamiltonian",
            "candidate_hamiltonian",
            "anchor_cross_covariance",
            "retained_subspace_overlap",
            "exterior_energy_anchor",
        ):
            value = np.asarray(getattr(self, name), dtype=np.complex128)
            if value.ndim != 2 or not np.all(np.isfinite(value)):
                raise ValueError(f"{name} must be finite and two-dimensional")
            immutable = np.frombuffer(
                value.tobytes(order="C"), dtype=np.complex128
            ).reshape(value.shape)
            object.__setattr__(self, name, immutable)


@dataclass(frozen=True, slots=True)
class HiddenAlignmentTruth:
    """Retain oracle values for post hoc verification only."""

    candidate_to_reference: ComplexMatrix
    planted_defect: ComplexMatrix

    def __post_init__(self) -> None:
        for name in ("candidate_to_reference", "planted_defect"):
            value = np.asarray(getattr(self, name), dtype=np.complex128)
            if value.ndim != 2 or not np.all(np.isfinite(value)):
                raise ValueError(f"{name} must be finite and two-dimensional")
            immutable = np.frombuffer(
                value.tobytes(order="C"), dtype=np.complex128
            ).reshape(value.shape)
            object.__setattr__(self, name, immutable)


@dataclass(frozen=True, slots=True)
class AlignmentInferenceResult:
    """Represent a full, partial, or stopped blind-alignment outcome."""

    status: AlignmentStatus
    issue_codes: tuple[str, ...]
    alignment_map: ComplexMatrix | None
    reference_projector: ComplexMatrix | None
    extracted_operator: ComplexMatrix | None
    inferred_energy_shift: float | None
    anchor_rank: int
    anchor_condition_number: float | None
    minimum_anchor_singular_value: float | None
    maximum_principal_angle_radians: float | None
    energy_anchor_rank: float | None

    def __post_init__(self) -> None:
        stopped = self.status == "stopped"
        arrays = (
            self.alignment_map,
            self.reference_projector,
            self.extracted_operator,
        )
        if stopped != bool(self.issue_codes):
            raise ValueError("stopped status must agree with issue codes")
        if stopped and any(value is not None for value in arrays):
            raise ValueError("stopped inference must not return aligned operators")
        if not stopped and any(value is None for value in arrays):
            raise ValueError("successful inference must return aligned operators")
        if self.issue_codes != tuple(sorted(set(self.issue_codes))):
            raise ValueError("issue codes must be sorted and unique")
        for name in ("alignment_map", "reference_projector", "extracted_operator"):
            optional = getattr(self, name)
            if optional is not None:
                value = np.asarray(optional, dtype=np.complex128)
                if value.ndim != 2 or not np.all(np.isfinite(value)):
                    raise ValueError(f"{name} must be finite and two-dimensional")
                immutable = np.frombuffer(
                    value.tobytes(order="C"), dtype=np.complex128
                ).reshape(value.shape)
                object.__setattr__(self, name, immutable)


@dataclass(frozen=True, slots=True)
class ExactCase:
    """Represent one exact full-rank observation request."""

    identifier: str
    defect_id: str
    spin_count: int
    minimum_anchor_singular_value: float


@dataclass(frozen=True, slots=True)
class NoiseSweep:
    """Represent a frozen well-conditioned observation-noise sequence."""

    identifier: str
    defect_id: str
    spin_count: int
    minimum_anchor_singular_value: float
    unitary_noise_radians: tuple[float, ...]
    generator_seed: int


@dataclass(frozen=True, slots=True)
class GaugeCase:
    """Represent one undercomplete, gauge-equivalent anchor problem."""

    identifier: str
    defect_id: str
    spin_count: int
    identified_site_count: int
    minimum_nonzero_anchor_singular_value: float
    complement_rotation_radians: float
    generator_seed: int


@dataclass(frozen=True, slots=True)
class StoppingCase:
    """Represent one authored incompatible or unstable observation."""

    identifier: str
    kind: str
    numeric_value: float | int | None


@dataclass(frozen=True, slots=True)
class DebuggingDiagnostics:
    """Represent frozen neighboring probes for the five stopping controls."""

    conditioning_minimum_singular_values: tuple[float, ...]
    conditioning_additive_anchor_noise: float
    conditioning_noise_seed: int
    principal_angle_radians: tuple[float, ...]
    rank_drop: int
    energy_anchor_ranks: tuple[int, ...]

    def __post_init__(self) -> None:
        if (
            not self.conditioning_minimum_singular_values
            or not self.principal_angle_radians
            or not self.energy_anchor_ranks
        ):
            raise ValueError("diagnostic sweeps must be nonempty")
        if self.conditioning_additive_anchor_noise <= 0.0:
            raise ValueError("conditioning noise must be positive")
        if self.rank_drop < 1 or any(rank < 0 for rank in self.energy_anchor_ranks):
            raise ValueError("diagnostic ranks are invalid")


@dataclass(frozen=True, slots=True)
class BlindAlignmentInput:
    """Represent the complete version-1 experiment input."""

    experiment_id: str
    baseline_input: SourceIdentity
    baseline_result: SourceIdentity
    observation_information: ObservationInformationContract
    policy: InferencePolicy
    exact_cases: tuple[ExactCase, ...]
    noise_sweep: NoiseSweep
    gauge_case: GaugeCase
    stopping_cases: tuple[StoppingCase, ...]
    diagnostics: DebuggingDiagnostics
    algebraic_tolerance: float


class BlindAlignmentInputDeserializer:
    """Deserialize the closed synthetic input contract."""

    __slots__ = ()

    def execute(self, payload: bytes) -> BlindAlignmentInput:
        root = self._mapping(cast(JsonValue, json.loads(payload)), "input")
        if self._integer(root["schema_version"], "schema_version") != 1:
            raise ValueError("unsupported input schema version")
        if root["evidence_status"] != "synthetic test data":
            raise ValueError("evidence status must identify synthetic test data")
        sources = self._mapping(root["baseline_sources"], "baseline_sources")
        information = self._mapping(
            root["observation_information_contract"],
            "observation_information_contract",
        )
        policy = self._mapping(root["inference_policy"], "inference_policy")
        exact_records = self._records(root["exact_cases"], "exact_cases")
        noise = self._mapping(root["noise_sweep"], "noise_sweep")
        gauge = self._mapping(root["gauge_equivalent_case"], "gauge_equivalent_case")
        diagnostic = self._mapping(
            root["debugging_diagnostics"], "debugging_diagnostics"
        )
        stop_records = self._records(root["stopping_cases"], "stopping_cases")
        stops: list[StoppingCase] = []
        for record in stop_records:
            kind = self._string(record["kind"], "stopping kind")
            numeric: float | int | None = None
            for key in (
                "minimum_anchor_singular_value",
                "maximum_principal_angle_radians",
                "candidate_dimension_delta",
                "candidate_spin_count",
            ):
                if key in record:
                    value = record[key]
                    numeric = (
                        self._integer(value, key)
                        if key in {"candidate_dimension_delta", "candidate_spin_count"}
                        else self._real(value, key)
                    )
            stops.append(
                StoppingCase(self._string(record["id"], "stopping id"), kind, numeric)
            )
        return BlindAlignmentInput(
            experiment_id=self._string(root["experiment_id"], "experiment_id"),
            baseline_input=SourceIdentity(
                self._string(sources["input_path"], "baseline input path"),
                self._string(sources["input_sha256"], "baseline input sha256"),
            ),
            baseline_result=SourceIdentity(
                self._string(sources["result_path"], "baseline result path"),
                self._string(sources["result_sha256"], "baseline result sha256"),
            ),
            observation_information=ObservationInformationContract(
                self._string(
                    information["anchor_cross_covariance"],
                    "anchor cross covariance information",
                ),
                self._string(
                    information["site_anchor_labels"], "site anchor information"
                ),
                self._string(information["orbital_labels"], "orbital information"),
                self._string(information["spin_frame"], "spin information"),
                self._string(information["energy_reference"], "energy information"),
            ),
            policy=InferencePolicy(
                self._real(policy["anchor_rank_tolerance"], "anchor rank tolerance"),
                self._real(
                    policy["maximum_anchor_condition_number"],
                    "maximum anchor condition",
                ),
                self._real(
                    policy["maximum_principal_angle_radians"],
                    "maximum principal angle",
                ),
                self._integer(
                    policy["minimum_energy_anchor_rank"],
                    "minimum energy anchor rank",
                ),
                self._integer(policy["core_radius_cells"], "core radius"),
            ),
            exact_cases=tuple(
                ExactCase(
                    self._string(record["id"], "exact id"),
                    self._string(record["defect_id"], "exact defect"),
                    self._integer(record["spin_count"], "exact spin count"),
                    self._real(
                        record["minimum_anchor_singular_value"],
                        "exact minimum singular value",
                    ),
                )
                for record in exact_records
            ),
            noise_sweep=NoiseSweep(
                self._string(noise["id"], "noise id"),
                self._string(noise["defect_id"], "noise defect"),
                self._integer(noise["spin_count"], "noise spin count"),
                self._real(
                    noise["minimum_anchor_singular_value"],
                    "noise singular value",
                ),
                self._reals(noise["unitary_noise_radians"], "noise radians"),
                self._integer(noise["generator_seed"], "noise seed"),
            ),
            gauge_case=GaugeCase(
                self._string(gauge["id"], "gauge id"),
                self._string(gauge["defect_id"], "gauge defect"),
                self._integer(gauge["spin_count"], "gauge spin count"),
                self._integer(gauge["identified_site_count"], "identified site count"),
                self._real(
                    gauge["minimum_nonzero_anchor_singular_value"],
                    "gauge singular value",
                ),
                self._real(
                    gauge["complement_rotation_radians"],
                    "complement rotation",
                ),
                self._integer(gauge["generator_seed"], "gauge seed"),
            ),
            stopping_cases=tuple(stops),
            diagnostics=DebuggingDiagnostics(
                self._reals(
                    diagnostic["conditioning_minimum_singular_values"],
                    "conditioning minimum singular values",
                ),
                self._real(
                    diagnostic["conditioning_additive_anchor_noise"],
                    "conditioning additive noise",
                ),
                self._integer(
                    diagnostic["conditioning_noise_seed"],
                    "conditioning noise seed",
                ),
                self._reals(
                    diagnostic["principal_angle_radians"],
                    "principal angles",
                ),
                self._integer(diagnostic["rank_drop"], "rank drop"),
                self._integers(
                    diagnostic["energy_anchor_ranks"], "energy anchor ranks"
                ),
            ),
            algebraic_tolerance=self._real(
                root["algebraic_tolerance"], "algebraic tolerance"
            ),
        )

    @staticmethod
    def _mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be a JSON object")
        return value

    def _records(self, value: JsonValue, name: str) -> tuple[dict[str, JsonValue], ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return tuple(self._mapping(item, name) for item in value)

    @staticmethod
    def _string(value: JsonValue, name: str) -> str:
        if not isinstance(value, str) or not value:
            raise TypeError(f"{name} must be a nonempty string")
        return value

    @staticmethod
    def _integer(value: JsonValue, name: str) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an integer")
        return value

    @staticmethod
    def _real(value: JsonValue, name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be numeric")
        result = float(value)
        if not np.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result

    def _reals(self, value: JsonValue, name: str) -> tuple[float, ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return tuple(self._real(item, name) for item in value)

    def _integers(self, value: JsonValue, name: str) -> tuple[int, ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return tuple(self._integer(item, name) for item in value)


class BaselineLoader:
    """Load the exact accepted baseline without importing its runner."""

    __slots__ = ()

    def execute(
        self, specification: BlindAlignmentInput, repository_root: Path
    ) -> BaselineData:
        input_path = repository_root / specification.baseline_input.path
        result_path = repository_root / specification.baseline_result.path
        self._verify_identity(input_path, specification.baseline_input.sha256)
        self._verify_identity(result_path, specification.baseline_result.sha256)
        source = self._load(input_path)
        retained = self._load(result_path)
        extraction = self._mapping(source["extraction_control"], "extraction")
        alignment = self._mapping(source["alignment_control"], "alignment")
        parent = self._mapping(source["parent_sources"], "parent")
        size = self._integer(extraction["supercell_size"], "supercell size")
        momentum = (
            self._real(extraction["reduced_momentum_times_supercell"], "momentum")
            / size
        )
        composite_path = repository_root / self._string(
            parent["composite_result_path"], "composite path"
        )
        self._verify_identity(
            composite_path,
            self._string(parent["composite_result_sha256"], "composite sha256"),
        )
        hoppings = self._load_hoppings(
            composite_path,
            self._string(parent["composite_group_id"], "group id"),
            self._integer(parent["parent_hopping_range_cells"], "hopping range"),
        )
        pristine = self._supercell(hoppings, size, momentum)
        map_spinless = self._candidate_to_reference(size, momentum, 1, alignment)
        map_spinor = self._candidate_to_reference(size, momentum, 2, alignment)
        defects: list[NamedDefect] = []
        for record in self._records(
            retained["extraction_controls"], "extraction controls"
        ):
            identifier = self._string(record["id"], "defect id")
            spin_count = self._integer(record["spin_count"], "spin count")
            defects.append(
                NamedDefect(
                    identifier,
                    spin_count,
                    self._compact_matrix(
                        record["compact_planted_blocks"],
                        size,
                        2 * spin_count,
                    ),
                )
            )
        return BaselineData(
            size,
            momentum,
            pristine,
            map_spinless,
            map_spinor,
            self._real(alignment["energy_reference_shift"], "energy shift"),
            tuple(defects),
            (
                specification.baseline_input,
                specification.baseline_result,
                SourceIdentity(
                    composite_path.relative_to(repository_root).as_posix(),
                    self._sha256(composite_path),
                ),
            ),
        )

    def _load_hoppings(
        self, path: Path, group_id: str, hopping_range: int
    ) -> tuple[tuple[int, ComplexMatrix], ...]:
        root = self._load(path)
        groups = self._records(root["groups"], "groups")
        matches = [group for group in groups if group["id"] == group_id]
        if len(matches) != 1:
            raise ValueError("composite group must occur once")
        records = self._records(matches[0]["smooth_hopping_blocks"], "hopping blocks")
        values: list[tuple[int, ComplexMatrix]] = []
        for record in records:
            representative = self._integer(
                record["representative_cells"], "representative"
            )
            if abs(representative) <= hopping_range:
                values.append(
                    (
                        representative,
                        self._complex_matrix(record["matrix"], "hopping matrix"),
                    )
                )
        values.sort(key=lambda item: item[0])
        return tuple(values)

    def _candidate_to_reference(
        self,
        size: int,
        momentum: float,
        spin_count: int,
        control: dict[str, JsonValue],
    ) -> ComplexMatrix:
        translation_cells = self._integer(control["translation_cells"], "translation")
        translation = np.zeros((size, size), dtype=np.complex128)
        for source in range(size):
            raw_target = source + translation_cells
            target = raw_target % size
            crossings = (raw_target - target) // size
            translation[target, source] = np.exp(
                2j * np.pi * momentum * size * crossings
            )
        angle = self._real(control["orbital_rotation_angle_radians"], "orbital angle")
        rotation = np.asarray(
            [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]],
            dtype=np.complex128,
        )
        permutation_values = self._integers(
            control["orbital_permutation"], "orbital permutation"
        )
        permutation = np.eye(2, dtype=np.complex128)[
            np.asarray(permutation_values, dtype=np.int64)
        ]
        orbital_phases = np.diag(
            np.exp(
                1j
                * np.asarray(
                    self._reals(control["orbital_phases_radians"], "orbital phases")
                )
            )
        )
        generator = np.asarray(
            np.kron(
                translation,
                orbital_phases @ permutation @ rotation,
            ),
            dtype=np.complex128,
        )
        phase_step = self._real(control["site_phase_step_radians"], "site phase")
        diagonal = np.asarray(
            [
                np.exp(1j * phase_step * (site + 0.5 * orbital))
                for site in range(size)
                for orbital in range(2)
            ],
            dtype=np.complex128,
        )
        reference_to_candidate = np.diag(diagonal) @ generator
        if spin_count == 2:
            axis = np.asarray(
                self._reals(control["spin_rotation_axis"], "spin axis"),
                dtype=np.float64,
            )
            axis /= np.linalg.norm(axis)
            spin_angle = self._real(
                control["spin_rotation_angle_radians"], "spin angle"
            )
            pauli_x, pauli_y, pauli_z = self._pauli()
            spin_generator = axis[0] * pauli_x + axis[1] * pauli_y + axis[2] * pauli_z
            spin_rotation = (
                np.cos(spin_angle / 2.0) * np.eye(2)
                - 1j * np.sin(spin_angle / 2.0) * spin_generator
            )
            reference_to_candidate = np.asarray(
                np.kron(reference_to_candidate, spin_rotation),
                dtype=np.complex128,
            )
        return reference_to_candidate.conj().T

    def _compact_matrix(
        self, value: JsonValue, size: int, block_size: int
    ) -> ComplexMatrix:
        result = np.zeros((size * block_size, size * block_size), dtype=np.complex128)
        for record in self._records(value, "compact blocks"):
            row = self._integer(record["row_site"], "row site")
            column = self._integer(record["column_site"], "column site")
            result[
                block_size * row : block_size * (row + 1),
                block_size * column : block_size * (column + 1),
            ] = self._complex_matrix(record["matrix"], "compact block")
        return result

    @staticmethod
    def _supercell(
        hoppings: tuple[tuple[int, ComplexMatrix], ...], size: int, momentum: float
    ) -> ComplexMatrix:
        result = np.zeros((2 * size, 2 * size), dtype=np.complex128)
        for source in range(size):
            for representative, block in hoppings:
                raw_target = source + representative
                target = raw_target % size
                crossings = (raw_target - target) // size
                phase = np.exp(2j * np.pi * momentum * size * crossings)
                result[
                    2 * source : 2 * source + 2,
                    2 * target : 2 * target + 2,
                ] += phase * block
        return result

    @staticmethod
    def _pauli() -> tuple[ComplexMatrix, ComplexMatrix, ComplexMatrix]:
        return (
            np.asarray([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128),
            np.asarray([[0.0, -1j], [1j, 0.0]], dtype=np.complex128),
            np.asarray([[1.0, 0.0], [0.0, -1.0]], dtype=np.complex128),
        )

    @staticmethod
    def _load(path: Path) -> dict[str, JsonValue]:
        value = cast(JsonValue, json.loads(path.read_text(encoding="utf-8")))
        if not isinstance(value, dict):
            raise TypeError("JSON root must be an object")
        return value

    @staticmethod
    def _mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be an object")
        return value

    def _records(self, value: JsonValue, name: str) -> tuple[dict[str, JsonValue], ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be an array")
        return tuple(self._mapping(item, name) for item in value)

    @staticmethod
    def _string(value: JsonValue, name: str) -> str:
        if not isinstance(value, str) or not value:
            raise TypeError(f"{name} must be a nonempty string")
        return value

    @staticmethod
    def _integer(value: JsonValue, name: str) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an integer")
        return value

    def _integers(self, value: JsonValue, name: str) -> tuple[int, ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be an array")
        return tuple(self._integer(item, name) for item in value)

    @staticmethod
    def _real(value: JsonValue, name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be numeric")
        return float(value)

    def _reals(self, value: JsonValue, name: str) -> tuple[float, ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be an array")
        return tuple(self._real(item, name) for item in value)

    def _complex_matrix(self, value: JsonValue, name: str) -> ComplexMatrix:
        if not isinstance(value, list) or not value:
            raise TypeError(f"{name} must be a nonempty matrix")
        rows: list[list[complex]] = []
        for row in value:
            if not isinstance(row, list):
                raise TypeError(f"{name} rows must be arrays")
            parsed: list[complex] = []
            for pair in row:
                if not isinstance(pair, list) or len(pair) != 2:
                    raise TypeError(f"{name} values must be complex pairs")
                parsed.append(
                    complex(self._real(pair[0], name), self._real(pair[1], name))
                )
            rows.append(parsed)
        return np.asarray(rows, dtype=np.complex128)

    @staticmethod
    def _verify_identity(path: Path, expected: str) -> None:
        if BaselineLoader._sha256(path) != expected:
            raise ValueError(f"source identity mismatch: {path}")

    @staticmethod
    def _sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()


class BlindAlignmentInferer:
    """Infer an alignment solely from observations and frozen policy."""

    __slots__ = ()

    def execute(
        self, observation: BlindAlignmentObservation, policy: InferencePolicy
    ) -> AlignmentInferenceResult:
        reference_dimension = observation.reference_hamiltonian.shape[0]
        candidate_dimension = observation.candidate_hamiltonian.shape[0]
        if (
            observation.reference_hamiltonian.shape
            != (reference_dimension, reference_dimension)
            or observation.candidate_hamiltonian.shape
            != (candidate_dimension, candidate_dimension)
            or observation.anchor_cross_covariance.shape
            != (reference_dimension, candidate_dimension)
        ):
            raise ValueError(
                "observation matrix dimensions are internally inconsistent"
            )
        if reference_dimension != candidate_dimension:
            return self._stopped("BLIND_ALIGNMENT.RANK_MISMATCH")
        if observation.reference_spin_count != observation.candidate_spin_count:
            return self._stopped("BLIND_ALIGNMENT.SPIN_MISMATCH")
        subspace_singular = np.linalg.svd(
            observation.retained_subspace_overlap, compute_uv=False
        )
        minimum_subspace = float(np.min(np.clip(subspace_singular, 0.0, 1.0)))
        maximum_angle = float(np.arccos(minimum_subspace))
        if maximum_angle > policy.maximum_principal_angle_radians:
            return self._stopped(
                "BLIND_ALIGNMENT.SUBSPACE_ANGLE_EXCEEDED",
                maximum_principal_angle=maximum_angle,
            )
        left, singular, right_adjoint = np.linalg.svd(
            observation.anchor_cross_covariance, full_matrices=False
        )
        active = singular > policy.anchor_rank_tolerance
        rank = int(np.sum(active))
        if rank == 0:
            return self._stopped(
                "BLIND_ALIGNMENT.ANCHOR_RANK_ZERO",
                maximum_principal_angle=maximum_angle,
            )
        minimum_active = float(np.min(singular[active]))
        condition = float(np.max(singular[active]) / minimum_active)
        if condition > policy.maximum_anchor_condition_number:
            return self._stopped(
                "BLIND_ALIGNMENT.ANCHOR_ILL_CONDITIONED",
                rank=rank,
                condition=condition,
                minimum_singular=minimum_active,
                maximum_principal_angle=maximum_angle,
            )
        if rank < reference_dimension and not observation.allow_partial_alignment:
            return self._stopped(
                "BLIND_ALIGNMENT.ANCHOR_RANK_DEFICIENT",
                rank=rank,
                condition=condition,
                minimum_singular=minimum_active,
                maximum_principal_angle=maximum_angle,
            )
        alignment = left[:, active] @ right_adjoint[active, :]
        projector = alignment @ alignment.conj().T
        energy_anchor = projector @ observation.exterior_energy_anchor @ projector
        energy_rank = float(
            np.sum(
                np.linalg.svd(energy_anchor, compute_uv=False)
                > policy.anchor_rank_tolerance
            )
        )
        energy_weight = float(np.trace(energy_anchor).real)
        if energy_rank < policy.minimum_energy_anchor_rank:
            return self._stopped(
                "BLIND_ALIGNMENT.ENERGY_ANCHOR_INSUFFICIENT",
                rank=rank,
                condition=condition,
                minimum_singular=minimum_active,
                maximum_principal_angle=maximum_angle,
                energy_rank=energy_rank,
            )
        aligned_candidate = (
            alignment @ observation.candidate_hamiltonian @ alignment.conj().T
        )
        reference_compressed = projector @ observation.reference_hamiltonian @ projector
        shift = float(
            np.trace(
                energy_anchor
                @ (aligned_candidate - reference_compressed)
                @ energy_anchor
            ).real
            / energy_weight
        )
        extracted = aligned_candidate - shift * projector - reference_compressed
        return AlignmentInferenceResult(
            "aligned_full" if rank == reference_dimension else "aligned_partial",
            (),
            alignment,
            projector,
            extracted,
            shift,
            rank,
            condition,
            minimum_active,
            maximum_angle,
            energy_rank,
        )

    def execute_reconciled_partial(
        self, observation: BlindAlignmentObservation, policy: InferencePolicy
    ) -> AlignmentInferenceResult:
        """Infer a declared rectangular partial isometry after rank reconciliation."""
        reference_dimension = observation.reference_hamiltonian.shape[0]
        candidate_dimension = observation.candidate_hamiltonian.shape[0]
        if (
            reference_dimension <= candidate_dimension
            or not observation.allow_partial_alignment
            or observation.anchor_cross_covariance.shape
            != (reference_dimension, candidate_dimension)
            or observation.retained_subspace_overlap.shape
            != (reference_dimension, candidate_dimension)
        ):
            raise ValueError("rectangular reconciliation contract is invalid")
        if observation.reference_spin_count != observation.candidate_spin_count:
            return self._stopped("BLIND_ALIGNMENT.SPIN_MISMATCH")
        subspace_singular = np.linalg.svd(
            observation.retained_subspace_overlap, compute_uv=False
        )
        maximum_angle = float(
            np.arccos(float(np.min(np.clip(subspace_singular, 0.0, 1.0))))
        )
        if maximum_angle > policy.maximum_principal_angle_radians:
            return self._stopped(
                "BLIND_ALIGNMENT.SUBSPACE_ANGLE_EXCEEDED",
                maximum_principal_angle=maximum_angle,
            )
        left, singular, right_adjoint = np.linalg.svd(
            observation.anchor_cross_covariance, full_matrices=False
        )
        active = singular > policy.anchor_rank_tolerance
        rank = int(np.sum(active))
        if rank != candidate_dimension:
            return self._stopped(
                "BLIND_ALIGNMENT.ANCHOR_RANK_DEFICIENT",
                rank=rank,
                maximum_principal_angle=maximum_angle,
            )
        minimum_active = float(np.min(singular[active]))
        condition = float(np.max(singular[active]) / minimum_active)
        if condition > policy.maximum_anchor_condition_number:
            return self._stopped(
                "BLIND_ALIGNMENT.ANCHOR_ILL_CONDITIONED",
                rank=rank,
                condition=condition,
                minimum_singular=minimum_active,
                maximum_principal_angle=maximum_angle,
            )
        alignment = left[:, active] @ right_adjoint[active, :]
        projector = alignment @ alignment.conj().T
        energy_anchor = projector @ observation.exterior_energy_anchor @ projector
        energy_rank = float(
            np.sum(
                np.linalg.svd(energy_anchor, compute_uv=False)
                > policy.anchor_rank_tolerance
            )
        )
        energy_weight = float(np.trace(energy_anchor).real)
        if energy_rank < policy.minimum_energy_anchor_rank:
            return self._stopped(
                "BLIND_ALIGNMENT.ENERGY_ANCHOR_INSUFFICIENT",
                rank=rank,
                condition=condition,
                minimum_singular=minimum_active,
                maximum_principal_angle=maximum_angle,
                energy_rank=energy_rank,
            )
        aligned_candidate = (
            alignment @ observation.candidate_hamiltonian @ alignment.conj().T
        )
        reference_compressed = projector @ observation.reference_hamiltonian @ projector
        shift = float(
            np.trace(
                energy_anchor
                @ (aligned_candidate - reference_compressed)
                @ energy_anchor
            ).real
            / energy_weight
        )
        extracted = aligned_candidate - shift * projector - reference_compressed
        return AlignmentInferenceResult(
            "aligned_partial",
            (),
            alignment,
            projector,
            extracted,
            shift,
            rank,
            condition,
            minimum_active,
            maximum_angle,
            energy_rank,
        )

    @staticmethod
    def _stopped(
        issue: str,
        *,
        rank: int = 0,
        condition: float | None = None,
        minimum_singular: float | None = None,
        maximum_principal_angle: float | None = None,
        energy_rank: float | None = None,
    ) -> AlignmentInferenceResult:
        return AlignmentInferenceResult(
            "stopped",
            (issue,),
            None,
            None,
            None,
            None,
            rank,
            condition,
            minimum_singular,
            maximum_principal_angle,
            energy_rank,
        )


class BlindAlignmentExperiment:
    """Generate observations, invoke inference, and evaluate against hidden truth."""

    __slots__ = ("_inferer",)

    def __init__(self) -> None:
        self._inferer = BlindAlignmentInferer()

    def execute(
        self,
        specification: BlindAlignmentInput,
        baseline: BaselineData,
        input_path: Path,
        script_path: Path,
    ) -> bytes:
        exact_records: list[JsonValue] = []
        for case in specification.exact_cases:
            observation, truth = self._full_observation(
                case.identifier,
                case.defect_id,
                case.spin_count,
                case.minimum_anchor_singular_value,
                0.0,
                0,
                baseline,
                specification.policy,
            )
            outcome = self._inferer.execute(observation, specification.policy)
            exact_records.append(
                self._evaluate(
                    outcome,
                    truth,
                    baseline.energy_shift,
                    case.identifier,
                    baseline.cell_count,
                )
            )
        noise_records: list[JsonValue] = []
        noise = specification.noise_sweep
        for radians in noise.unitary_noise_radians:
            observation, truth = self._full_observation(
                f"{noise.identifier}-{radians:.1e}",
                noise.defect_id,
                noise.spin_count,
                noise.minimum_anchor_singular_value,
                radians,
                noise.generator_seed,
                baseline,
                specification.policy,
            )
            outcome = self._inferer.execute(observation, specification.policy)
            record = self._evaluate(
                outcome,
                truth,
                baseline.energy_shift,
                f"{noise.identifier}-{radians:.1e}",
                baseline.cell_count,
            )
            if not isinstance(record, dict):
                raise TypeError("evaluated record must be an object")
            record["unitary_noise_radians"] = radians
            noise_records.append(record)
        gauge_record = self._gauge_case(
            specification.gauge_case, baseline, specification.policy
        )
        stopping_records = self._stopping_cases(
            specification.stopping_cases, baseline, specification.policy
        )
        diagnostic_records = self._debugging_diagnostics(
            specification.diagnostics, baseline, specification.policy
        )
        repository_root = script_path.parents[3]
        payload: dict[str, JsonValue] = {
            "schema_version": 1,
            "experiment_id": specification.experiment_id,
            "evidence_status": "synthetic test data",
            "calculation_status": "calculated synthetic numerical-verification result",
            "information_boundary": {
                "declared_observation_contract": (
                    specification.observation_information.as_json()
                ),
                "inference_inputs": [
                    "reference Hamiltonian",
                    "candidate Hamiltonian",
                    "anchor cross-covariance",
                    "retained-subspace overlap",
                    "exterior energy anchor",
                    "spin-space metadata",
                    "frozen inference policy",
                ],
                "withheld_from_inference": [
                    "authored candidate-to-reference map",
                    "authored scalar energy shift",
                    "planted defect operator",
                    "authored translation, orbital, phase, and spin parameters",
                ],
                "oracle_use": "Post hoc evaluation only.",
            },
            "policy": {
                "anchor_rank_tolerance": specification.policy.anchor_rank_tolerance,
                "maximum_anchor_condition_number": (
                    specification.policy.maximum_anchor_condition_number
                ),
                "maximum_principal_angle_radians": (
                    specification.policy.maximum_principal_angle_radians
                ),
                "minimum_energy_anchor_rank": (
                    specification.policy.minimum_energy_anchor_rank
                ),
                "core_radius_cells": specification.policy.core_radius_cells,
            },
            "exact_full_rank_cases": exact_records,
            "noise_sweep": noise_records,
            "gauge_equivalent_case": gauge_record,
            "stopping_cases": stopping_records,
            "debugging_diagnostics": diagnostic_records,
            "error_accounting": {
                "observation_error": (
                    "Controlled by the authored unitary perturbation of the anchor "
                    "cross-covariance and reported independently."
                ),
                "alignment_error": (
                    "Reported against the hidden map only after inference."
                ),
                "energy_reference_error": (
                    "Reported separately from unitary-map and extraction errors."
                ),
                "extraction_error": (
                    "Reported against the planted full or compressed operator."
                ),
                "model_class_error": (
                    "Reported as a distinct onsite-class residual for every "
                    "successful extraction."
                ),
                "scientific_validation": "Not performed.",
                "uncertainty_quantification": "Not performed.",
            },
            "source_identities": [
                {"path": item.path, "sha256": item.sha256}
                for item in baseline.source_identities
            ],
            "limitations": [
                "All observations, defects, and hidden maps are synthetic.",
                "The cross-covariance and subspace-overlap records are authored "
                "observables rather than outputs of independent electronic-structure "
                "calculations.",
                "Partial alignment establishes only compressed active-sector "
                "recovery; no full operator is identified on the anchor-null "
                "complement.",
                "No silicon, dopant, DFT, production Wannier, scientific-validation, "
                "transferability, or UQ claim is made.",
            ],
            "provenance": {
                "input_path": input_path.relative_to(repository_root).as_posix(),
                "input_sha256": self._sha256(input_path),
                "script_path": script_path.relative_to(repository_root).as_posix(),
                "script_sha256": self._sha256(script_path),
                "implementation_path": Path(__file__)
                .resolve()
                .relative_to(repository_root)
                .as_posix(),
                "implementation_sha256": self._sha256(Path(__file__).resolve()),
                "python_version": platform.python_version(),
                "numpy_version": np.__version__,
            },
        }
        return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()

    def _full_observation(
        self,
        identifier: str,
        defect_id: str,
        spin_count: int,
        minimum_singular: float,
        noise_radians: float,
        seed: int,
        baseline: BaselineData,
        policy: InferencePolicy,
    ) -> tuple[BlindAlignmentObservation, HiddenAlignmentTruth]:
        host, transform, defect = self._case_matrices(defect_id, spin_count, baseline)
        dimension = host.shape[0]
        noise = self._unitary_noise(dimension, noise_radians, seed)
        singular = np.linspace(1.0, minimum_singular, dimension)
        anchors = np.diag(singular) @ noise @ transform
        candidate = transform.conj().T @ (
            host + defect
        ) @ transform + baseline.energy_shift * np.eye(dimension)
        exterior = self._exterior_projector(
            baseline.cell_count, 2 * spin_count, policy.core_radius_cells
        )
        observation = BlindAlignmentObservation(
            identifier,
            host,
            candidate,
            anchors,
            np.eye(dimension, dtype=np.complex128),
            exterior,
            spin_count,
            spin_count,
            False,
        )
        return observation, HiddenAlignmentTruth(transform, defect)

    def _gauge_case(
        self, case: GaugeCase, baseline: BaselineData, policy: InferencePolicy
    ) -> dict[str, JsonValue]:
        host, transform, defect = self._case_matrices(
            case.defect_id, case.spin_count, baseline
        )
        dimension = host.shape[0]
        active_dimension = case.identified_site_count * 2 * case.spin_count
        if active_dimension >= dimension:
            raise ValueError("gauge case must leave a nonempty complement")
        singular = np.zeros(dimension)
        singular[:active_dimension] = np.linspace(
            1.0, case.minimum_nonzero_anchor_singular_value, active_dimension
        )
        anchors = np.diag(singular) @ transform
        candidate = transform.conj().T @ (
            host + defect
        ) @ transform + baseline.energy_shift * np.eye(dimension)
        exterior = self._exterior_projector(
            baseline.cell_count, 2 * case.spin_count, policy.core_radius_cells
        )
        observation = BlindAlignmentObservation(
            case.identifier,
            host,
            candidate,
            anchors,
            np.eye(dimension, dtype=np.complex128),
            exterior,
            case.spin_count,
            case.spin_count,
            True,
        )
        truth = HiddenAlignmentTruth(transform, defect)
        outcome = self._inferer.execute(observation, policy)
        record = self._evaluate(
            outcome,
            truth,
            baseline.energy_shift,
            case.identifier,
            baseline.cell_count,
        )
        if outcome.alignment_map is None or outcome.reference_projector is None:
            raise ValueError("gauge-equivalent case must return a partial map")
        projector = outcome.reference_projector
        complement = np.eye(dimension) - projector
        complement_values, complement_vectors = np.linalg.eigh(complement)
        complement_basis = complement_vectors[:, complement_values > 0.5]
        complement_noise = self._unitary_noise(
            complement_basis.shape[1],
            case.complement_rotation_radians,
            case.generator_seed,
        )
        complement_rotation = (
            projector + complement_basis @ complement_noise @ complement_basis.conj().T
        )
        first_completion = transform
        second_completion = complement_rotation @ transform
        first_extraction = (
            first_completion
            @ (candidate - baseline.energy_shift * np.eye(dimension))
            @ first_completion.conj().T
            - host
        )
        second_extraction = (
            second_completion
            @ (candidate - baseline.energy_shift * np.eye(dimension))
            @ second_completion.conj().T
            - host
        )
        record["identified_dimension"] = active_dimension
        record["unidentified_complement_dimension"] = dimension - active_dimension
        record["full_completion_extraction_disagreement"] = self._norm(
            first_extraction - second_extraction
        )
        record["compressed_completion_extraction_disagreement"] = self._norm(
            projector @ (first_extraction - second_extraction) @ projector
        )
        record["partial_map_agreement_between_completions"] = self._norm(
            projector @ first_completion - projector @ second_completion
        )
        return record

    def _stopping_cases(
        self,
        cases: tuple[StoppingCase, ...],
        baseline: BaselineData,
        policy: InferencePolicy,
    ) -> list[JsonValue]:
        records: list[JsonValue] = []
        for case in cases:
            observation, _ = self._full_observation(
                case.identifier,
                "orbital-onsite",
                1,
                0.75,
                0.0,
                0,
                baseline,
                policy,
            )
            if case.kind == "anchor-condition":
                if not isinstance(case.numeric_value, float):
                    raise TypeError("anchor-condition value must be real")
                dimension = observation.reference_hamiltonian.shape[0]
                anchors = (
                    np.diag(np.linspace(1.0, case.numeric_value, dimension))
                    @ baseline.candidate_to_reference_spinless
                )
                observation = self._replace_observation(
                    observation, anchor_cross_covariance=anchors
                )
            elif case.kind == "principal-angle":
                if not isinstance(case.numeric_value, float):
                    raise TypeError("principal-angle value must be real")
                dimension = observation.reference_hamiltonian.shape[0]
                singular = np.ones(dimension)
                singular[-1] = np.cos(case.numeric_value)
                observation = self._replace_observation(
                    observation,
                    retained_subspace_overlap=np.diag(singular),
                )
            elif case.kind == "rank-mismatch":
                if not isinstance(case.numeric_value, int):
                    raise TypeError("rank delta must be integer")
                candidate_dimension = (
                    observation.candidate_hamiltonian.shape[0] + case.numeric_value
                )
                observation = BlindAlignmentObservation(
                    observation.identifier,
                    observation.reference_hamiltonian,
                    observation.candidate_hamiltonian[
                        :candidate_dimension, :candidate_dimension
                    ],
                    observation.anchor_cross_covariance[:, :candidate_dimension],
                    observation.retained_subspace_overlap[:, :candidate_dimension],
                    observation.exterior_energy_anchor,
                    observation.reference_spin_count,
                    observation.candidate_spin_count,
                    False,
                )
            elif case.kind == "spin-mismatch":
                if not isinstance(case.numeric_value, int):
                    raise TypeError("spin count must be integer")
                observation = self._replace_observation(
                    observation, candidate_spin_count=case.numeric_value
                )
            elif case.kind == "energy-anchor":
                dimension = observation.reference_hamiltonian.shape[0]
                observation = self._replace_observation(
                    observation,
                    exterior_energy_anchor=np.zeros(
                        (dimension, dimension), dtype=np.complex128
                    ),
                )
            else:
                raise ValueError(f"unknown stopping kind: {case.kind}")
            outcome = self._inferer.execute(observation, policy)
            records.append(
                {
                    "id": case.identifier,
                    "kind": case.kind,
                    "status": outcome.status,
                    "issue_codes": list(outcome.issue_codes),
                    "alignment_map": None,
                    "extracted_operator": None,
                    "inferred_energy_shift": outcome.inferred_energy_shift,
                    "anchor_rank": outcome.anchor_rank,
                    "anchor_condition_number": outcome.anchor_condition_number,
                    "minimum_anchor_singular_value": (
                        outcome.minimum_anchor_singular_value
                    ),
                    "maximum_principal_angle_radians": (
                        outcome.maximum_principal_angle_radians
                    ),
                    "energy_anchor_rank": outcome.energy_anchor_rank,
                }
            )
        return records

    def _debugging_diagnostics(
        self,
        diagnostics: DebuggingDiagnostics,
        baseline: BaselineData,
        policy: InferencePolicy,
    ) -> dict[str, JsonValue]:
        condition_records: list[JsonValue] = []
        for minimum in diagnostics.conditioning_minimum_singular_values:
            identifier = f"conditioning-{minimum:.1e}"
            observation, truth = self._full_observation(
                identifier,
                "orbital-onsite",
                1,
                minimum,
                0.0,
                0,
                baseline,
                policy,
            )
            dimension = observation.reference_hamiltonian.shape[0]
            additive = self._normalized_complex_noise(
                dimension,
                dimension,
                diagnostics.conditioning_noise_seed,
            )
            observation = self._replace_observation(
                observation,
                anchor_cross_covariance=(
                    observation.anchor_cross_covariance
                    + diagnostics.conditioning_additive_anchor_noise * additive
                ),
            )
            outcome = self._inferer.execute(observation, policy)
            if outcome.status == "stopped":
                record = self._diagnostic_stop_record(identifier, outcome)
            else:
                record = self._evaluate(
                    outcome,
                    truth,
                    baseline.energy_shift,
                    identifier,
                    baseline.cell_count,
                )
            record["requested_minimum_anchor_singular_value"] = minimum
            record["additive_anchor_noise_spectral_norm"] = (
                diagnostics.conditioning_additive_anchor_noise
            )
            condition_records.append(record)

        angle_records: list[JsonValue] = []
        for angle in diagnostics.principal_angle_radians:
            identifier = f"principal-angle-{angle:.2f}"
            observation, truth = self._full_observation(
                identifier,
                "orbital-onsite",
                1,
                0.75,
                0.0,
                0,
                baseline,
                policy,
            )
            dimension = observation.reference_hamiltonian.shape[0]
            overlap_singular = np.ones(dimension)
            overlap_singular[-1] = np.cos(angle)
            observation = self._replace_observation(
                observation,
                retained_subspace_overlap=np.diag(overlap_singular),
            )
            outcome = self._inferer.execute(observation, policy)
            if outcome.status == "stopped":
                record = self._diagnostic_stop_record(identifier, outcome)
            else:
                record = self._evaluate(
                    outcome,
                    truth,
                    baseline.energy_shift,
                    identifier,
                    baseline.cell_count,
                )
            record["requested_principal_angle_radians"] = angle
            record["minimum_subspace_overlap_singular_value"] = float(np.cos(angle))
            record["diagnostic_reference_basis_indices"] = [dimension - 1]
            angle_records.append(record)

        rank_record = self._rank_reconciliation_diagnostic(
            diagnostics.rank_drop, baseline, policy
        )
        spin_record = self._spin_reconciliation_diagnostic(baseline, policy)

        energy_records: list[JsonValue] = []
        for requested_rank in diagnostics.energy_anchor_ranks:
            identifier = f"energy-anchor-rank-{requested_rank}"
            observation, truth = self._full_observation(
                identifier,
                "orbital-onsite",
                1,
                0.75,
                0.0,
                0,
                baseline,
                policy,
            )
            exterior_indices = np.flatnonzero(
                np.diag(observation.exterior_energy_anchor).real > 0.5
            )
            if requested_rank > exterior_indices.size:
                raise ValueError("requested energy-anchor rank exceeds exterior rank")
            energy_anchor = np.zeros_like(observation.exterior_energy_anchor)
            selected = exterior_indices[:requested_rank]
            energy_anchor[selected, selected] = 1.0
            observation = self._replace_observation(
                observation, exterior_energy_anchor=energy_anchor
            )
            outcome = self._inferer.execute(observation, policy)
            if outcome.status == "stopped":
                record = self._diagnostic_stop_record(identifier, outcome)
            else:
                record = self._evaluate(
                    outcome,
                    truth,
                    baseline.energy_shift,
                    identifier,
                    baseline.cell_count,
                )
            record["requested_energy_anchor_rank"] = requested_rank
            energy_records.append(record)

        return {
            "conditioning_boundary": condition_records,
            "principal_angle_boundary": angle_records,
            "rank_reconciliation": rank_record,
            "spin_reconciliation": spin_record,
            "energy_anchor_boundary": energy_records,
            "interpretation": (
                "Neighboring admissible probes diagnose the stopping boundaries; "
                "they do not weaken or replace the original negative controls."
            ),
        }

    def _rank_reconciliation_diagnostic(
        self, rank_drop: int, baseline: BaselineData, policy: InferencePolicy
    ) -> dict[str, JsonValue]:
        host = baseline.pristine_spinless
        transform = baseline.candidate_to_reference_spinless
        reference_dimension = host.shape[0]
        candidate_dimension = reference_dimension - rank_drop
        if candidate_dimension < 1:
            raise ValueError("rank diagnostic must retain a nonempty sector")
        isometry = transform[:, :candidate_dimension]
        projector = isometry @ isometry.conj().T
        candidate = (
            isometry.conj().T @ host @ isometry
            + baseline.energy_shift * np.eye(candidate_dimension)
        )
        singular = np.linspace(1.0, 0.75, candidate_dimension)
        observation = BlindAlignmentObservation(
            "rank-reconciled-partial-isometry",
            host,
            candidate,
            isometry @ np.diag(singular),
            isometry,
            projector,
            1,
            1,
            True,
        )
        direct = self._inferer.execute(observation, policy)
        if direct.issue_codes != ("BLIND_ALIGNMENT.RANK_MISMATCH",):
            raise ValueError("direct unequal-rank comparison must stop")
        reconciled = self._inferer.execute_reconciled_partial(observation, policy)
        truth = HiddenAlignmentTruth(isometry, np.zeros_like(host, dtype=np.complex128))
        record = self._evaluate(
            reconciled,
            truth,
            baseline.energy_shift,
            "rank-reconciled-partial-isometry",
            baseline.cell_count,
        )
        record["direct_comparison_issue_code"] = direct.issue_codes[0]
        record["reference_dimension"] = reference_dimension
        record["candidate_dimension"] = candidate_dimension
        record["dropped_dimension"] = rank_drop
        record["resolution"] = "explicit_rectangular_partial_isometry"
        return record

    def _spin_reconciliation_diagnostic(
        self, baseline: BaselineData, policy: InferencePolicy
    ) -> dict[str, JsonValue]:
        mismatch_observation, _ = self._full_observation(
            "spin-mismatch-diagnostic",
            "orbital-onsite",
            1,
            0.75,
            0.0,
            0,
            baseline,
            policy,
        )
        mismatch_observation = self._replace_observation(
            mismatch_observation, candidate_spin_count=2
        )
        direct = self._inferer.execute(mismatch_observation, policy)
        if direct.issue_codes != ("BLIND_ALIGNMENT.SPIN_MISMATCH",):
            raise ValueError("direct spin-space comparison must stop")
        observation, truth = self._full_observation(
            "spin-lifted-reconciliation",
            "spin-mixing",
            2,
            0.65,
            0.0,
            0,
            baseline,
            policy,
        )
        reconciled = self._inferer.execute(observation, policy)
        resolution = self._evaluate(
            reconciled,
            truth,
            baseline.energy_shift,
            "spin-lifted-reconciliation",
            baseline.cell_count,
        )
        defect = truth.planted_defect
        spatial_dimension = defect.shape[0] // 2
        tensor = defect.reshape(spatial_dimension, 2, spatial_dimension, 2)
        spin_independent = 0.5 * np.einsum("asbs->ab", tensor)
        lifted = np.kron(spin_independent, np.eye(2))
        return {
            "direct_comparison_status": direct.status,
            "direct_comparison_issue_code": direct.issue_codes[0],
            "resolution": "explicit_spin_lift_to_common_spinor_space",
            "spin_independent_restriction_residual": self._norm(defect - lifted),
            "lossless_spin_restriction_available": False,
            "lifted_alignment": resolution,
        }

    @staticmethod
    def _diagnostic_stop_record(
        identifier: str, outcome: AlignmentInferenceResult
    ) -> dict[str, JsonValue]:
        if outcome.status != "stopped":
            raise ValueError("diagnostic stop record requires a stopped outcome")
        return {
            "id": identifier,
            "status": outcome.status,
            "issue_codes": list(outcome.issue_codes),
            "anchor_rank": outcome.anchor_rank,
            "anchor_condition_number": outcome.anchor_condition_number,
            "minimum_anchor_singular_value": outcome.minimum_anchor_singular_value,
            "maximum_principal_angle_radians": (
                outcome.maximum_principal_angle_radians
            ),
            "energy_anchor_rank": outcome.energy_anchor_rank,
            "alignment_map": None,
            "inferred_energy_shift": None,
            "extracted_operator": None,
        }

    @staticmethod
    def _normalized_complex_noise(rows: int, columns: int, seed: int) -> ComplexMatrix:
        rng = np.random.default_rng(seed)
        values = rng.normal(size=(rows, columns)) + 1j * rng.normal(
            size=(rows, columns)
        )
        norm = float(np.linalg.norm(values, 2))
        if norm == 0.0:
            raise ValueError("additive anchor noise must be nonzero")
        return np.asarray(values / norm, dtype=np.complex128)

    @staticmethod
    def _replace_observation(
        original: BlindAlignmentObservation,
        *,
        anchor_cross_covariance: ComplexMatrix | None = None,
        retained_subspace_overlap: ComplexMatrix | None = None,
        exterior_energy_anchor: ComplexMatrix | None = None,
        candidate_spin_count: int | None = None,
    ) -> BlindAlignmentObservation:
        return BlindAlignmentObservation(
            original.identifier,
            original.reference_hamiltonian,
            original.candidate_hamiltonian,
            (
                original.anchor_cross_covariance
                if anchor_cross_covariance is None
                else anchor_cross_covariance
            ),
            (
                original.retained_subspace_overlap
                if retained_subspace_overlap is None
                else retained_subspace_overlap
            ),
            (
                original.exterior_energy_anchor
                if exterior_energy_anchor is None
                else exterior_energy_anchor
            ),
            original.reference_spin_count,
            (
                original.candidate_spin_count
                if candidate_spin_count is None
                else candidate_spin_count
            ),
            original.allow_partial_alignment,
        )

    def _evaluate(
        self,
        outcome: AlignmentInferenceResult,
        truth: HiddenAlignmentTruth,
        true_shift: float,
        identifier: str,
        cell_count: int,
    ) -> dict[str, JsonValue]:
        if (
            outcome.status == "stopped"
            or outcome.alignment_map is None
            or outcome.reference_projector is None
            or outcome.extracted_operator is None
            or outcome.inferred_energy_shift is None
        ):
            raise ValueError("evaluation requires a successful inference")
        alignment = outcome.alignment_map
        projector = outcome.reference_projector
        expected_map = projector @ truth.candidate_to_reference
        phase = np.angle(np.trace(expected_map.conj().T @ alignment))
        map_defect = self._norm(alignment - np.exp(1j * phase) * expected_map)
        target = projector @ truth.planted_defect @ projector
        extraction_defect = self._norm(outcome.extracted_operator - target)
        if target.shape[0] % cell_count != 0:
            raise ValueError("operator dimension must be divisible by cell count")
        block_size = target.shape[0] // cell_count
        extracted_model = np.zeros_like(outcome.extracted_operator)
        extracted_model[:block_size, :block_size] = outcome.extracted_operator[
            :block_size, :block_size
        ]
        planted_model = np.zeros_like(target)
        planted_model[:block_size, :block_size] = target[:block_size, :block_size]
        active_values, active_vectors = np.linalg.eigh(projector)
        active_basis = active_vectors[:, active_values > 0.5]
        extracted_active = (
            active_basis.conj().T @ outcome.extracted_operator @ active_basis
        )
        target_active = active_basis.conj().T @ target @ active_basis
        extracted_eigenvalues, extracted_vectors = np.linalg.eigh(extracted_active)
        target_eigenvalues, target_vectors = np.linalg.eigh(target_active)
        lowest_mask = np.abs(target_eigenvalues - target_eigenvalues[0]) <= 1.0e-11
        lowest_dimension = int(np.sum(lowest_mask))
        target_lowest_projector = (
            target_vectors[:, :lowest_dimension]
            @ target_vectors[:, :lowest_dimension].conj().T
        )
        extracted_lowest_projector = (
            extracted_vectors[:, :lowest_dimension]
            @ extracted_vectors[:, :lowest_dimension].conj().T
        )
        lowest_fidelity: float | None = None
        if lowest_dimension == 1:
            lowest_fidelity = float(
                np.clip(
                    abs(np.vdot(extracted_vectors[:, 0], target_vectors[:, 0])) ** 2,
                    0.0,
                    1.0,
                )
            )
        return {
            "id": identifier,
            "status": outcome.status,
            "issue_codes": [],
            "dimension": truth.planted_defect.shape[0],
            "anchor_rank": outcome.anchor_rank,
            "anchor_condition_number": outcome.anchor_condition_number,
            "minimum_anchor_singular_value": outcome.minimum_anchor_singular_value,
            "maximum_principal_angle_radians": (
                outcome.maximum_principal_angle_radians
            ),
            "energy_anchor_rank": outcome.energy_anchor_rank,
            "inferred_energy_shift": outcome.inferred_energy_shift,
            "energy_shift_error": outcome.inferred_energy_shift - true_shift,
            "phase_quotiented_alignment_frobenius_defect": map_defect,
            "extraction_frobenius_defect": extraction_defect,
            "extraction_relative_frobenius_defect": (
                extraction_defect / self._norm(target)
                if self._norm(target) > 0.0
                else 0.0
            ),
            "planted_onsite_model_class_residual": self._norm(target - planted_model),
            "extracted_onsite_model_class_residual": self._norm(
                outcome.extracted_operator - extracted_model
            ),
            "active_spectral_maximum_absolute_defect": float(
                np.max(np.abs(extracted_eigenvalues - target_eigenvalues))
            ),
            "active_lowest_state_fidelity": lowest_fidelity,
            "active_lowest_eigenspace_dimension": lowest_dimension,
            "active_lowest_eigenspace_projector_defect": self._norm(
                extracted_lowest_projector - target_lowest_projector
            ),
            "alignment_map_sha256": self._matrix_sha256(alignment),
            "extracted_operator_sha256": self._matrix_sha256(
                outcome.extracted_operator
            ),
        }

    @staticmethod
    def _case_matrices(
        defect_id: str, spin_count: int, baseline: BaselineData
    ) -> tuple[ComplexMatrix, ComplexMatrix, ComplexMatrix]:
        defect = baseline.defect(defect_id)
        if defect.spin_count != spin_count:
            raise ValueError("selected defect spin count is inconsistent")
        if spin_count == 1:
            return (
                baseline.pristine_spinless,
                baseline.candidate_to_reference_spinless,
                defect.matrix,
            )
        return (
            np.asarray(
                np.kron(baseline.pristine_spinless, np.eye(2)),
                dtype=np.complex128,
            ),
            baseline.candidate_to_reference_spinor,
            defect.matrix,
        )

    @staticmethod
    def _unitary_noise(dimension: int, radians: float, seed: int) -> ComplexMatrix:
        if radians == 0.0:
            return np.eye(dimension, dtype=np.complex128)
        generator = np.zeros((dimension, dimension), dtype=np.complex128)
        rng = np.random.default_rng(seed)
        for index in range(dimension - 1):
            value = rng.normal() + 1j * rng.normal()
            generator[index, index + 1] = value
            generator[index + 1, index] = value.conjugate()
        norm = float(np.linalg.norm(generator, 2))
        if norm == 0.0:
            raise ValueError("noise generator must be nonzero")
        values, vectors = np.linalg.eigh(generator / norm)
        return np.asarray(
            vectors @ np.diag(np.exp(1j * radians * values)) @ vectors.conj().T,
            dtype=np.complex128,
        )

    @staticmethod
    def _exterior_projector(
        cell_count: int, block_size: int, core_radius: int
    ) -> ComplexMatrix:
        coordinates = np.arange(cell_count, dtype=np.int64)
        coordinates = np.where(
            coordinates <= cell_count // 2,
            coordinates,
            coordinates - cell_count,
        )
        result = np.zeros(
            (cell_count * block_size, cell_count * block_size),
            dtype=np.complex128,
        )
        for site, coordinate in enumerate(coordinates):
            if abs(coordinate) > core_radius:
                begin = block_size * site
                result[begin : begin + block_size, begin : begin + block_size] = np.eye(
                    block_size
                )
        return result

    @staticmethod
    def _matrix_sha256(matrix: ComplexMatrix) -> str:
        canonical = np.stack((matrix.real, matrix.imag), axis=-1).astype(
            "<f8", copy=True
        )
        canonical[canonical == 0.0] = 0.0
        return hashlib.sha256(canonical.tobytes(order="C")).hexdigest()

    @staticmethod
    def _norm(matrix: ComplexMatrix) -> float:
        return float(np.linalg.norm(matrix))

    @staticmethod
    def _sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()
