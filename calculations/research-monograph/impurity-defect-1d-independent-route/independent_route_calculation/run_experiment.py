"""Run independent real-space and Bloch-fiber defect-extraction routes."""

from __future__ import annotations

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
class SourceIdentity:
    """Identify one frozen source artifact."""

    path: str
    sha256: str

    def __post_init__(self) -> None:
        if not self.path or len(self.sha256) != 64:
            raise ValueError("source identity is invalid")


@dataclass(frozen=True, slots=True)
class RouteContract:
    """Represent the common spaces and discretization of both routes."""

    group_id: str
    cell_count: int
    reduced_momentum_times_supercell: float
    real_space_range: int
    bloch_range: int
    site_ordering: str
    spin_ordering: str
    fiber_ordering: str
    energy_unit: str
    energy_reference: str

    def __post_init__(self) -> None:
        if (
            not self.group_id
            or self.cell_count < 2
            or self.real_space_range < 0
            or self.bloch_range < 0
            or not np.isfinite(self.reduced_momentum_times_supercell)
        ):
            raise ValueError("route contract is invalid")
        if self.real_space_range != self.bloch_range:
            raise ValueError("nominal routes must use the same hopping range")

    @property
    def reduced_momentum(self) -> float:
        """Return primitive reciprocal-lattice units for the supercell fiber."""
        return self.reduced_momentum_times_supercell / self.cell_count


@dataclass(frozen=True, slots=True)
class AdversarialControls:
    """Represent frozen changes that invalidate or separate the routes."""

    truncation_range: int
    domain_fiber_count: int
    nonuniform_weight_amplitude: float
    alignment_translation_delta: int

    def __post_init__(self) -> None:
        if (
            self.truncation_range < 0
            or self.domain_fiber_count < 1
            or self.nonuniform_weight_amplitude <= 0.0
            or self.alignment_translation_delta == 0
        ):
            raise ValueError("adversarial controls are invalid")


@dataclass(frozen=True, slots=True)
class ReconciliationControls:
    """Represent explicit common-space rules for stopped mismatches."""

    common_hopping_range: int
    common_domain_cell_count: int
    weighted_coordinate_rule: str
    alignment_map_rule: str

    def __post_init__(self) -> None:
        if self.common_hopping_range < 0:
            raise ValueError("common hopping range must be nonnegative")
        if self.common_domain_cell_count < 2:
            raise ValueError("common domain must contain at least two cells")
        if self.weighted_coordinate_rule != "explicit-inverse-and-induced-metric":
            raise ValueError("unsupported weighted-coordinate rule")
        if self.alignment_map_rule != "explicit-relative-unitary":
            raise ValueError("unsupported alignment-map rule")


@dataclass(frozen=True, slots=True)
class ExperimentInput:
    """Represent the closed independent-route input contract."""

    experiment_id: str
    baseline_input: SourceIdentity
    baseline_result: SourceIdentity
    composite_result: SourceIdentity
    route: RouteContract
    control_ids: tuple[str, ...]
    adversarial: AdversarialControls
    reconciliation: ReconciliationControls
    algebraic_tolerance: float
    eigenspace_tolerance: float


@dataclass(frozen=True, slots=True)
class HoppingBlock:
    """Retain one primitive-cell displacement and orbital block."""

    displacement: int
    matrix: ComplexMatrix

    def __post_init__(self) -> None:
        value = np.asarray(self.matrix, dtype=np.complex128)
        if value.shape != (2, 2) or not np.all(np.isfinite(value)):
            raise ValueError("hopping block must be finite 2 by 2")
        immutable = np.frombuffer(
            value.tobytes(order="C"), dtype=np.complex128
        ).reshape(value.shape)
        object.__setattr__(self, "matrix", immutable)


@dataclass(frozen=True, slots=True)
class DefectControl:
    """Retain one accepted planted represented operator."""

    identifier: str
    spin_count: int
    matrix: ComplexMatrix

    def __post_init__(self) -> None:
        if not self.identifier or self.spin_count not in (1, 2):
            raise ValueError("defect control metadata is invalid")
        value = np.asarray(self.matrix, dtype=np.complex128)
        if value.ndim != 2 or value.shape[0] != value.shape[1]:
            raise ValueError("defect operator must be square")
        immutable = np.frombuffer(
            value.tobytes(order="C"), dtype=np.complex128
        ).reshape(value.shape)
        object.__setattr__(self, "matrix", immutable)


@dataclass(frozen=True, slots=True)
class AlignmentSettings:
    """Retain authored coordinate and energy-reference settings."""

    translation_cells: int
    orbital_permutation: tuple[int, int]
    orbital_rotation_angle: float
    orbital_phases: tuple[float, float]
    site_phase_step: float
    spin_axis: tuple[float, float, float]
    spin_angle: float
    energy_shift: float


@dataclass(frozen=True, slots=True)
class BaselineData:
    """Retain immutable inputs shared by the independently implemented routes."""

    hoppings: tuple[HoppingBlock, ...]
    defects: tuple[DefectControl, ...]
    alignment: AlignmentSettings
    source_identities: tuple[SourceIdentity, ...]

    def defect(self, identifier: str) -> DefectControl:
        """Return one uniquely identified accepted defect control."""
        matches = tuple(item for item in self.defects if item.identifier == identifier)
        if len(matches) != 1:
            raise ValueError(f"defect must occur exactly once: {identifier}")
        return matches[0]


@dataclass(frozen=True, slots=True)
class RealSpaceRouteResult:
    """Retain outputs owned by direct supercell construction and subtraction."""

    pristine: ComplexMatrix
    aligned_physical: ComplexMatrix
    extracted: ComplexMatrix

    def __post_init__(self) -> None:
        for name in ("pristine", "aligned_physical", "extracted"):
            value = np.asarray(getattr(self, name), dtype=np.complex128)
            immutable = np.frombuffer(
                value.tobytes(order="C"), dtype=np.complex128
            ).reshape(value.shape)
            object.__setattr__(self, name, immutable)


@dataclass(frozen=True, slots=True)
class BlochFiberRouteResult:
    """Retain outputs owned by direct primitive-fiber assembly and subtraction."""

    folding_map: ComplexMatrix
    pristine: ComplexMatrix
    aligned_physical: ComplexMatrix
    extracted: ComplexMatrix

    def __post_init__(self) -> None:
        for name in ("folding_map", "pristine", "aligned_physical", "extracted"):
            value = np.asarray(getattr(self, name), dtype=np.complex128)
            immutable = np.frombuffer(
                value.tobytes(order="C"), dtype=np.complex128
            ).reshape(value.shape)
            object.__setattr__(self, name, immutable)


class ExperimentInputDeserializer:
    """Deserialize and validate the closed JSON input."""

    __slots__ = ()

    def execute(self, payload: bytes) -> ExperimentInput:
        root = self._mapping(cast(JsonValue, json.loads(payload)), "input")
        if self._integer(root["schema_version"], "schema_version") != 1:
            raise ValueError("unsupported schema version")
        if root["evidence_status"] != "synthetic test data":
            raise ValueError("evidence status must identify synthetic test data")
        sources = self._mapping(root["baseline_sources"], "baseline_sources")
        route = self._mapping(root["route_contract"], "route_contract")
        adversarial = self._mapping(
            root["adversarial_controls"], "adversarial_controls"
        )
        reconciliation = self._mapping(
            root["reconciliation_controls"], "reconciliation_controls"
        )
        return ExperimentInput(
            self._string(root["experiment_id"], "experiment_id"),
            SourceIdentity(
                self._string(sources["input_path"], "baseline input path"),
                self._string(sources["input_sha256"], "baseline input sha256"),
            ),
            SourceIdentity(
                self._string(sources["result_path"], "baseline result path"),
                self._string(sources["result_sha256"], "baseline result sha256"),
            ),
            SourceIdentity(
                self._string(sources["composite_result_path"], "composite path"),
                self._string(sources["composite_result_sha256"], "composite sha256"),
            ),
            RouteContract(
                self._string(route["composite_group_id"], "group id"),
                self._integer(route["supercell_size"], "cell count"),
                self._real(route["reduced_momentum_times_supercell"], "momentum"),
                self._integer(
                    route["real_space_hopping_range_cells"], "real-space range"
                ),
                self._integer(route["bloch_fiber_hopping_range_cells"], "Bloch range"),
                self._string(route["site_orbital_ordering"], "site ordering"),
                self._string(route["spinful_ordering"], "spin ordering"),
                self._string(route["fiber_ordering"], "fiber ordering"),
                self._string(route["energy_unit"], "energy unit"),
                self._string(route["energy_reference"], "energy reference"),
            ),
            self._strings(root["control_ids"], "control ids"),
            AdversarialControls(
                self._integer(
                    adversarial["truncation_mismatch_bloch_range_cells"],
                    "truncation range",
                ),
                self._integer(
                    adversarial["domain_mismatch_fiber_count"], "domain count"
                ),
                self._real(
                    adversarial["nonuniform_weight_amplitude"], "weight amplitude"
                ),
                self._integer(
                    adversarial["alignment_translation_delta_cells"],
                    "translation delta",
                ),
            ),
            ReconciliationControls(
                self._integer(
                    reconciliation["common_hopping_range_cells"],
                    "common hopping range",
                ),
                self._integer(
                    reconciliation["common_domain_cell_count"],
                    "common domain cell count",
                ),
                self._string(
                    reconciliation["weighted_fiber_coordinate_rule"],
                    "weighted coordinate rule",
                ),
                self._string(
                    reconciliation["alignment_map_rule"],
                    "alignment map rule",
                ),
            ),
            self._real(root["algebraic_tolerance"], "algebraic tolerance"),
            self._real(root["eigenspace_tolerance"], "eigenspace tolerance"),
        )

    @staticmethod
    def _mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be an object")
        return value

    @staticmethod
    def _string(value: JsonValue, name: str) -> str:
        if not isinstance(value, str) or not value:
            raise TypeError(f"{name} must be a nonempty string")
        return value

    def _strings(self, value: JsonValue, name: str) -> tuple[str, ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be an array")
        result = tuple(self._string(item, name) for item in value)
        if len(result) != len(set(result)):
            raise ValueError(f"{name} must be unique")
        return result

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


class AlignmentMapBuilder:
    """Build the accepted candidate-to-reference coordinate maps."""

    __slots__ = ()

    def execute(
        self,
        cell_count: int,
        momentum: float,
        settings: AlignmentSettings,
        spin_count: int,
        translation_delta: int = 0,
    ) -> ComplexMatrix:
        translation = np.zeros((cell_count, cell_count), dtype=np.complex128)
        cells = settings.translation_cells + translation_delta
        for source in range(cell_count):
            raw = source + cells
            target = raw % cell_count
            crossings = (raw - target) // cell_count
            translation[target, source] = np.exp(
                2j * np.pi * momentum * cell_count * crossings
            )
        angle = settings.orbital_rotation_angle
        rotation = np.asarray(
            [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]],
            dtype=np.complex128,
        )
        permutation = np.eye(2)[
            np.asarray(settings.orbital_permutation, dtype=np.int64)
        ]
        phases = np.diag(np.exp(1j * np.asarray(settings.orbital_phases)))
        reference_to_candidate = np.asarray(
            np.kron(translation, phases @ permutation @ rotation),
            dtype=np.complex128,
        )
        site_phases = np.asarray(
            [
                np.exp(1j * settings.site_phase_step * (site + 0.5 * orbital))
                for site in range(cell_count)
                for orbital in range(2)
            ]
        )
        reference_to_candidate = np.diag(site_phases) @ reference_to_candidate
        if spin_count == 2:
            axis = np.asarray(settings.spin_axis, dtype=np.float64)
            axis /= np.linalg.norm(axis)
            pauli_x = np.asarray([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128)
            pauli_y = np.asarray([[0.0, -1j], [1j, 0.0]], dtype=np.complex128)
            pauli_z = np.asarray([[1.0, 0.0], [0.0, -1.0]], dtype=np.complex128)
            generator = axis[0] * pauli_x + axis[1] * pauli_y + axis[2] * pauli_z
            spin_rotation = (
                np.cos(settings.spin_angle / 2.0) * np.eye(2)
                - 1j * np.sin(settings.spin_angle / 2.0) * generator
            )
            reference_to_candidate = np.asarray(
                np.kron(reference_to_candidate, spin_rotation),
                dtype=np.complex128,
            )
        return reference_to_candidate.conj().T


class BaselineLoader:
    """Load exact accepted sources without importing either extraction route."""

    __slots__ = ("_map_builder",)

    def __init__(self) -> None:
        self._map_builder = AlignmentMapBuilder()

    def execute(self, specification: ExperimentInput, root: Path) -> BaselineData:
        identities = (
            specification.baseline_input,
            specification.baseline_result,
            specification.composite_result,
        )
        for identity in identities:
            path = root / identity.path
            if self._sha256(path) != identity.sha256:
                raise ValueError(f"source identity mismatch: {identity.path}")
        baseline_input = self._load(root / specification.baseline_input.path)
        baseline_result = self._load(root / specification.baseline_result.path)
        composite = self._load(root / specification.composite_result.path)
        parent = self._mapping(baseline_input["parent_sources"], "parent sources")
        if (
            parent["composite_result_path"] != specification.composite_result.path
            or parent["composite_result_sha256"]
            != specification.composite_result.sha256
            or parent["composite_group_id"] != specification.route.group_id
            or parent["parent_hopping_range_cells"]
            != specification.route.real_space_range
        ):
            raise ValueError("route contract disagrees with accepted parent input")
        extraction = self._mapping(
            baseline_input["extraction_control"], "extraction control"
        )
        if (
            extraction["supercell_size"] != specification.route.cell_count
            or extraction["reduced_momentum_times_supercell"]
            != specification.route.reduced_momentum_times_supercell
        ):
            raise ValueError("route geometry disagrees with accepted baseline")
        groups = self._records(composite["groups"], "groups")
        matches = [
            item for item in groups if item["id"] == specification.route.group_id
        ]
        if len(matches) != 1:
            raise ValueError("composite group must occur exactly once")
        hoppings: list[HoppingBlock] = []
        for record in self._records(
            matches[0]["smooth_hopping_blocks"], "hopping records"
        ):
            displacement = self._integer(record["representative_cells"], "displacement")
            if abs(displacement) <= specification.route.real_space_range:
                hoppings.append(
                    HoppingBlock(
                        displacement,
                        self._complex_matrix(record["matrix"], "hopping matrix"),
                    )
                )
        if tuple(item.displacement for item in hoppings) != tuple(
            range(
                -specification.route.real_space_range,
                specification.route.real_space_range + 1,
            )
        ):
            raise ValueError("retained hopping range is incomplete")
        defects: list[DefectControl] = []
        result_controls = self._records(
            baseline_result["extraction_controls"], "extraction controls"
        )
        for identifier in specification.control_ids:
            matches = [item for item in result_controls if item["id"] == identifier]
            if len(matches) != 1:
                raise ValueError(f"accepted control must occur once: {identifier}")
            record = matches[0]
            spin_count = self._integer(record["spin_count"], "spin count")
            defects.append(
                DefectControl(
                    identifier,
                    spin_count,
                    self._compact_operator(
                        record["compact_planted_blocks"],
                        specification.route.cell_count,
                        2 * spin_count,
                    ),
                )
            )
        alignment = self._mapping(
            baseline_input["alignment_control"], "alignment control"
        )
        settings = AlignmentSettings(
            self._integer(alignment["translation_cells"], "translation"),
            self._pair_of_integers(
                alignment["orbital_permutation"], "orbital permutation"
            ),
            self._real(alignment["orbital_rotation_angle_radians"], "rotation"),
            self._pair_of_reals(alignment["orbital_phases_radians"], "orbital phases"),
            self._real(alignment["site_phase_step_radians"], "site phase"),
            self._triple_of_reals(alignment["spin_rotation_axis"], "spin axis"),
            self._real(alignment["spin_rotation_angle_radians"], "spin angle"),
            self._real(alignment["energy_reference_shift"], "energy shift"),
        )
        return BaselineData(tuple(hoppings), tuple(defects), settings, identities)

    def _compact_operator(
        self, value: JsonValue, cell_count: int, block_size: int
    ) -> ComplexMatrix:
        result = np.zeros(
            (cell_count * block_size, cell_count * block_size),
            dtype=np.complex128,
        )
        for record in self._records(value, "compact blocks"):
            row = self._integer(record["row_site"], "row site")
            column = self._integer(record["column_site"], "column site")
            result[
                block_size * row : block_size * (row + 1),
                block_size * column : block_size * (column + 1),
            ] = self._complex_matrix(record["matrix"], "defect block")
        return result

    @staticmethod
    def _load(path: Path) -> dict[str, JsonValue]:
        value = cast(JsonValue, json.loads(path.read_text(encoding="utf-8")))
        if not isinstance(value, dict):
            raise TypeError("source root must be an object")
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
    def _integer(value: JsonValue, name: str) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an integer")
        return value

    @staticmethod
    def _real(value: JsonValue, name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be numeric")
        return float(value)

    def _pair_of_integers(self, value: JsonValue, name: str) -> tuple[int, int]:
        if not isinstance(value, list) or len(value) != 2:
            raise TypeError(f"{name} must have length two")
        return (self._integer(value[0], name), self._integer(value[1], name))

    def _pair_of_reals(self, value: JsonValue, name: str) -> tuple[float, float]:
        if not isinstance(value, list) or len(value) != 2:
            raise TypeError(f"{name} must have length two")
        return (self._real(value[0], name), self._real(value[1], name))

    def _triple_of_reals(
        self, value: JsonValue, name: str
    ) -> tuple[float, float, float]:
        if not isinstance(value, list) or len(value) != 3:
            raise TypeError(f"{name} must have length three")
        return (
            self._real(value[0], name),
            self._real(value[1], name),
            self._real(value[2], name),
        )

    def _complex_matrix(self, value: JsonValue, name: str) -> ComplexMatrix:
        if not isinstance(value, list) or not value:
            raise TypeError(f"{name} must be a nonempty array")
        rows: list[list[complex]] = []
        for row in value:
            if not isinstance(row, list):
                raise TypeError(f"{name} row must be an array")
            parsed: list[complex] = []
            for pair in row:
                if not isinstance(pair, list) or len(pair) != 2:
                    raise TypeError(f"{name} entries must be complex pairs")
                parsed.append(
                    complex(self._real(pair[0], name), self._real(pair[1], name))
                )
            rows.append(parsed)
        return np.asarray(rows, dtype=np.complex128)

    @staticmethod
    def _sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()


class RealSpaceExtractionRoute:
    """Construct and subtract finite supercell matrices directly in site space."""

    __slots__ = ()

    def execute(
        self,
        hoppings: tuple[HoppingBlock, ...],
        cell_count: int,
        momentum: float,
        spin_count: int,
        raw_candidate: ComplexMatrix,
        candidate_to_reference: ComplexMatrix,
        energy_shift: float,
    ) -> RealSpaceRouteResult:
        spinless = np.zeros((2 * cell_count, 2 * cell_count), dtype=np.complex128)
        for source in range(cell_count):
            for hopping in hoppings:
                raw = source + hopping.displacement
                target = raw % cell_count
                crossings = (raw - target) // cell_count
                phase = np.exp(2j * np.pi * momentum * cell_count * crossings)
                spinless[
                    2 * source : 2 * source + 2,
                    2 * target : 2 * target + 2,
                ] += phase * hopping.matrix
        pristine = (
            spinless
            if spin_count == 1
            else np.asarray(np.kron(spinless, np.eye(2)), dtype=np.complex128)
        )
        aligned = (
            candidate_to_reference
            @ (raw_candidate - energy_shift * np.eye(raw_candidate.shape[0]))
            @ candidate_to_reference.conj().T
        )
        return RealSpaceRouteResult(pristine, aligned, aligned - pristine)


class BlochFiberExtractionRoute:
    """Construct primitive Bloch fibers and subtract directly in fiber space."""

    __slots__ = ()

    def execute(
        self,
        hoppings: tuple[HoppingBlock, ...],
        cell_count: int,
        momentum: float,
        spin_count: int,
        raw_candidate: ComplexMatrix,
        candidate_to_reference: ComplexMatrix,
        energy_shift: float,
    ) -> BlochFiberRouteResult:
        site_folding = np.zeros((2 * cell_count, 2 * cell_count), dtype=np.complex128)
        pristine_spinless = np.zeros_like(site_folding)
        for folded_index in range(cell_count):
            primitive_momentum = (momentum + folded_index / cell_count) % 1.0
            fiber = np.zeros((2, 2), dtype=np.complex128)
            for hopping in hoppings:
                fiber += (
                    np.exp(2j * np.pi * primitive_momentum * hopping.displacement)
                    * hopping.matrix
                )
            begin = 2 * folded_index
            pristine_spinless[begin : begin + 2, begin : begin + 2] = fiber
            for site in range(cell_count):
                phase = np.exp(2j * np.pi * primitive_momentum * site) / np.sqrt(
                    cell_count
                )
                site_folding[
                    2 * site : 2 * site + 2,
                    begin : begin + 2,
                ] = phase * np.eye(2)
        folding = (
            site_folding
            if spin_count == 1
            else np.asarray(np.kron(site_folding, np.eye(2)), dtype=np.complex128)
        )
        pristine = (
            pristine_spinless
            if spin_count == 1
            else np.asarray(np.kron(pristine_spinless, np.eye(2)), dtype=np.complex128)
        )
        candidate_to_fiber = folding.conj().T @ candidate_to_reference
        aligned = (
            candidate_to_fiber
            @ (raw_candidate - energy_shift * np.eye(raw_candidate.shape[0]))
            @ candidate_to_fiber.conj().T
        )
        return BlochFiberRouteResult(folding, pristine, aligned, aligned - pristine)


class IndependentRouteExperiment:
    """Author common observations and compare independently implemented routes."""

    __slots__ = ("_bloch", "_map_builder", "_real")

    def __init__(self) -> None:
        self._real = RealSpaceExtractionRoute()
        self._bloch = BlochFiberExtractionRoute()
        self._map_builder = AlignmentMapBuilder()

    def execute(
        self,
        specification: ExperimentInput,
        baseline: BaselineData,
        input_path: Path,
        script_path: Path,
    ) -> bytes:
        nominal: list[JsonValue] = []
        for identifier in specification.control_ids:
            defect = baseline.defect(identifier)
            nominal.append(self._nominal_control(defect, specification, baseline))
        adversarial, reconciled = self._adversarial_controls(specification, baseline)
        root = script_path.parents[3]
        payload: dict[str, JsonValue] = {
            "schema_version": 1,
            "experiment_id": specification.experiment_id,
            "evidence_status": "synthetic test data",
            "calculation_status": "calculated synthetic numerical-verification result",
            "route_contract": {
                "route_a": (
                    "direct finite-supercell assembly and site-space subtraction"
                ),
                "route_b": (
                    "direct primitive Bloch-fiber assembly and fiber-space subtraction"
                ),
                "shared_observations": [
                    "raw scrambled candidate Hamiltonian",
                    "declared candidate-to-reference alignment map",
                    "declared scalar energy-reference shift",
                    "frozen parent hopping blocks",
                    "accepted planted defect control",
                ],
                "implementation_independence": (
                    "Neither route imports or calls the other route. Route A sums "
                    "finite supercell matrix elements; Route B evaluates primitive "
                    "Bloch fibers and a discrete folding transform."
                ),
            },
            "represented_space": {
                "cell_count": specification.route.cell_count,
                "reduced_momentum": specification.route.reduced_momentum,
                "site_ordering": specification.route.site_ordering,
                "spin_ordering": specification.route.spin_ordering,
                "fiber_ordering": specification.route.fiber_ordering,
                "energy_unit": specification.route.energy_unit,
                "energy_reference": specification.route.energy_reference,
            },
            "nominal_controls": nominal,
            "adversarial_controls": adversarial,
            "reconciliation_controls": reconciled,
            "error_accounting": {
                "representation_error": (
                    "Direct supercell versus direct Bloch-fiber pristine operator."
                ),
                "alignment_error": (
                    "Aligned candidate versus the authored physical operator."
                ),
                "mesh_and_quadrature_error": (
                    "Folding-map unitarity and declared domain or weight compatibility."
                ),
                "truncation_error": (
                    "Difference caused by unequal retained hopping ranges."
                ),
                "route_error": (
                    "Site extraction transformed to fiber space versus direct "
                    "fiber extraction."
                ),
                "spectral_error": (
                    "Maximum eigenvalue discrepancy of reconstructed physical "
                    "operators."
                ),
                "wavefunction_error": (
                    "Lowest-eigenspace projector defect, with single-state "
                    "fidelity only when nondegenerate."
                ),
                "scientific_validation": "Not performed.",
                "uncertainty_quantification": "Not performed.",
            },
            "source_identities": [
                {"path": item.path, "sha256": item.sha256}
                for item in baseline.source_identities
            ],
            "limitations": [
                (
                    "All parent observations, defects, maps, and route controls are "
                    "synthetic or inherited synthetic records."
                ),
                (
                    "Route agreement checks algebraic commutativity under one finite "
                    "periodic representation; it does not establish material validity."
                ),
                (
                    "The Bloch-fiber route is independently implemented but uses the "
                    "same frozen mathematical input data by design."
                ),
                (
                    "No continuum limit, silicon calculation, scientific validation, "
                    "transferability, or UQ claim is made."
                ),
            ],
            "provenance": {
                "input_path": input_path.relative_to(root).as_posix(),
                "input_sha256": self._sha256(input_path),
                "script_path": script_path.relative_to(root).as_posix(),
                "script_sha256": self._sha256(script_path),
                "implementation_path": Path(__file__)
                .resolve()
                .relative_to(root)
                .as_posix(),
                "implementation_sha256": self._sha256(Path(__file__).resolve()),
                "python_version": platform.python_version(),
                "numpy_version": np.__version__,
            },
        }
        return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()

    def _nominal_control(
        self,
        defect: DefectControl,
        specification: ExperimentInput,
        baseline: BaselineData,
    ) -> dict[str, JsonValue]:
        contract = specification.route
        transform = self._map_builder.execute(
            contract.cell_count,
            contract.reduced_momentum,
            baseline.alignment,
            defect.spin_count,
        )
        zero_candidate = np.zeros_like(defect.matrix)
        host_route = self._real.execute(
            baseline.hoppings,
            contract.cell_count,
            contract.reduced_momentum,
            defect.spin_count,
            zero_candidate,
            np.eye(defect.matrix.shape[0], dtype=np.complex128),
            0.0,
        ).pristine
        raw_candidate = transform.conj().T @ (
            host_route + defect.matrix
        ) @ transform + baseline.alignment.energy_shift * np.eye(defect.matrix.shape[0])
        route_a = self._real.execute(
            baseline.hoppings,
            contract.cell_count,
            contract.reduced_momentum,
            defect.spin_count,
            raw_candidate,
            transform,
            baseline.alignment.energy_shift,
        )
        route_b = self._bloch.execute(
            baseline.hoppings,
            contract.cell_count,
            contract.reduced_momentum,
            defect.spin_count,
            raw_candidate,
            transform,
            baseline.alignment.energy_shift,
        )
        return self._comparison_record(
            defect.identifier,
            defect.spin_count,
            defect.matrix,
            route_a,
            route_b,
            specification.eigenspace_tolerance,
        )

    def _adversarial_controls(
        self, specification: ExperimentInput, baseline: BaselineData
    ) -> tuple[list[JsonValue], list[JsonValue]]:
        contract = specification.route
        adversarial = specification.adversarial
        defect = baseline.defect("range-two-nonlocal")
        transform = self._map_builder.execute(
            contract.cell_count,
            contract.reduced_momentum,
            baseline.alignment,
            1,
        )
        zero = np.zeros_like(defect.matrix)
        host = self._real.execute(
            baseline.hoppings,
            contract.cell_count,
            contract.reduced_momentum,
            1,
            zero,
            np.eye(defect.matrix.shape[0], dtype=np.complex128),
            0.0,
        ).pristine
        raw_candidate = transform.conj().T @ (
            host + defect.matrix
        ) @ transform + baseline.alignment.energy_shift * np.eye(defect.matrix.shape[0])
        route_a = self._real.execute(
            baseline.hoppings,
            contract.cell_count,
            contract.reduced_momentum,
            1,
            raw_candidate,
            transform,
            baseline.alignment.energy_shift,
        )
        truncated_hoppings = tuple(
            item
            for item in baseline.hoppings
            if abs(item.displacement) <= adversarial.truncation_range
        )
        route_b_truncated = self._bloch.execute(
            truncated_hoppings,
            contract.cell_count,
            contract.reduced_momentum,
            1,
            raw_candidate,
            transform,
            baseline.alignment.energy_shift,
        )
        route_a_fiber = (
            route_b_truncated.folding_map.conj().T
            @ route_a.extracted
            @ route_b_truncated.folding_map
        )
        truncation_spectral_discrepancy = self._spectral_defect(
            route_b_truncated.folding_map.conj().T
            @ route_a.aligned_physical
            @ route_b_truncated.folding_map,
            route_b_truncated.aligned_physical,
        )
        truncation_record: dict[str, JsonValue] = {
            "id": "hopping-truncation-mismatch",
            "status": "noncommuting",
            "issue_codes": ["INDEPENDENT_ROUTE.HOPPING_TRUNCATION_MISMATCH"],
            "real_space_hopping_range_cells": contract.real_space_range,
            "bloch_fiber_hopping_range_cells": adversarial.truncation_range,
            "truncation_operator_discrepancy": self._norm(
                route_b_truncated.pristine
                - route_b_truncated.folding_map.conj().T
                @ route_a.pristine
                @ route_b_truncated.folding_map
            ),
            "route_noncommutativity_frobenius": self._norm(
                route_a_fiber - route_b_truncated.extracted
            ),
            "reconstructed_spectral_maximum_absolute_discrepancy": (
                truncation_spectral_discrepancy
            ),
            "reconciliation_id": "hopping-common-parent-reconciliation",
        }
        altered_transform = self._map_builder.execute(
            contract.cell_count,
            contract.reduced_momentum,
            baseline.alignment,
            1,
            adversarial.alignment_translation_delta,
        )
        map_record: dict[str, JsonValue] = {
            "id": "unmatched-alignment-map",
            "status": "stopped",
            "issue_codes": ["INDEPENDENT_ROUTE.ALIGNMENT_MAP_MISMATCH"],
            "alignment_map_frobenius_discrepancy": self._norm(
                transform - altered_transform
            ),
            "extracted_operator": None,
            "reconciliation_id": "alignment-relative-map-reconciliation",
        }
        domain_record: dict[str, JsonValue] = {
            "id": "fiber-domain-mismatch",
            "status": "stopped",
            "issue_codes": ["INDEPENDENT_ROUTE.FIBER_DOMAIN_MISMATCH"],
            "real_space_cell_count": contract.cell_count,
            "bloch_fiber_count": adversarial.domain_fiber_count,
            "extracted_operator": None,
            "reconciliation_id": "fiber-domain-common-space-reconciliation",
        }
        route_b_nominal = self._bloch.execute(
            baseline.hoppings,
            contract.cell_count,
            contract.reduced_momentum,
            1,
            raw_candidate,
            transform,
            baseline.alignment.energy_shift,
        )
        weights = 1.0 + adversarial.nonuniform_weight_amplitude * np.cos(
            2.0 * np.pi * np.arange(contract.cell_count) / contract.cell_count
        )
        weighted = route_b_nominal.folding_map @ np.diag(np.repeat(np.sqrt(weights), 2))
        weight_record: dict[str, JsonValue] = {
            "id": "nonuniform-fiber-weights",
            "status": "stopped",
            "issue_codes": ["INDEPENDENT_ROUTE.QUADRATURE_WEIGHT_MISMATCH"],
            "nonuniform_weight_amplitude": adversarial.nonuniform_weight_amplitude,
            "folding_map_unitarity_defect": self._norm(
                weighted.conj().T @ weighted - np.eye(weighted.shape[1])
            ),
            "extracted_operator": None,
            "reconciliation_id": "nonuniform-weight-dual-map-reconciliation",
        }
        reconciled: list[JsonValue] = [
            self._common_parent_reconciliation(specification, baseline, defect),
            self._common_domain_reconciliation(specification, baseline, defect),
            self._weighted_coordinate_reconciliation(
                specification,
                defect,
                route_a,
                route_b_nominal,
                weighted,
                weights,
            ),
            self._alignment_map_reconciliation(
                specification,
                defect,
                route_a,
                route_b_nominal,
                raw_candidate,
                transform,
                altered_transform,
                baseline.alignment.energy_shift,
            ),
        ]
        return [truncation_record, domain_record, weight_record, map_record], reconciled

    def _common_parent_reconciliation(
        self,
        specification: ExperimentInput,
        baseline: BaselineData,
        defect: DefectControl,
    ) -> dict[str, JsonValue]:
        common_range = specification.reconciliation.common_hopping_range
        if common_range != specification.adversarial.truncation_range:
            raise ValueError("common-parent range must match the changed route")
        common_hoppings = tuple(
            item for item in baseline.hoppings if abs(item.displacement) <= common_range
        )
        contract = specification.route
        transform = self._map_builder.execute(
            contract.cell_count,
            contract.reduced_momentum,
            baseline.alignment,
            1,
        )
        zero = np.zeros_like(defect.matrix)
        common_host = self._real.execute(
            common_hoppings,
            contract.cell_count,
            contract.reduced_momentum,
            1,
            zero,
            np.eye(defect.matrix.shape[0], dtype=np.complex128),
            0.0,
        ).pristine
        nominal_host = self._real.execute(
            baseline.hoppings,
            contract.cell_count,
            contract.reduced_momentum,
            1,
            zero,
            np.eye(defect.matrix.shape[0], dtype=np.complex128),
            0.0,
        ).pristine
        raw_candidate = transform.conj().T @ (
            common_host + defect.matrix
        ) @ transform + baseline.alignment.energy_shift * np.eye(defect.matrix.shape[0])
        route_a = self._real.execute(
            common_hoppings,
            contract.cell_count,
            contract.reduced_momentum,
            1,
            raw_candidate,
            transform,
            baseline.alignment.energy_shift,
        )
        route_b = self._bloch.execute(
            common_hoppings,
            contract.cell_count,
            contract.reduced_momentum,
            1,
            raw_candidate,
            transform,
            baseline.alignment.energy_shift,
        )
        record = self._comparison_record(
            "range-two-nonlocal",
            1,
            defect.matrix,
            route_a,
            route_b,
            specification.eigenspace_tolerance,
        )
        record["id"] = "hopping-common-parent-reconciliation"
        record["control_class"] = "truncation-reconciliation"
        record["status"] = "reconciled"
        record["reconciles_issue_code"] = (
            "INDEPENDENT_ROUTE.HOPPING_TRUNCATION_MISMATCH"
        )
        record["nominal_hopping_range_cells"] = contract.real_space_range
        record["common_hopping_range_cells"] = common_range
        record["parent_change_from_nominal_frobenius"] = self._norm(
            common_host - nominal_host
        )
        return record

    def _common_domain_reconciliation(
        self,
        specification: ExperimentInput,
        baseline: BaselineData,
        defect: DefectControl,
    ) -> dict[str, JsonValue]:
        common_count = specification.reconciliation.common_domain_cell_count
        if common_count != specification.adversarial.domain_fiber_count:
            raise ValueError("common-domain reconciliation must match stopped domain")
        if common_count >= specification.route.cell_count:
            raise ValueError("common-domain control must reduce the nominal domain")
        dimension = 2 * common_count
        excluded_rows = defect.matrix[dimension:, :]
        excluded_columns = defect.matrix[:, dimension:]
        excluded_norm = self._norm(excluded_rows) + self._norm(excluded_columns)
        if excluded_norm != 0.0:
            raise ValueError("common-domain restriction would truncate the defect")
        plant = np.asarray(defect.matrix[:dimension, :dimension], dtype=np.complex128)
        momentum = specification.route.reduced_momentum_times_supercell / common_count
        transform = self._map_builder.execute(
            common_count,
            momentum,
            baseline.alignment,
            1,
        )
        zero = np.zeros_like(plant)
        host = self._real.execute(
            baseline.hoppings,
            common_count,
            momentum,
            1,
            zero,
            np.eye(dimension, dtype=np.complex128),
            0.0,
        ).pristine
        raw_candidate = transform.conj().T @ (
            host + plant
        ) @ transform + baseline.alignment.energy_shift * np.eye(dimension)
        route_a = self._real.execute(
            baseline.hoppings,
            common_count,
            momentum,
            1,
            raw_candidate,
            transform,
            baseline.alignment.energy_shift,
        )
        route_b = self._bloch.execute(
            baseline.hoppings,
            common_count,
            momentum,
            1,
            raw_candidate,
            transform,
            baseline.alignment.energy_shift,
        )
        record = self._comparison_record(
            "range-two-nonlocal",
            1,
            plant,
            route_a,
            route_b,
            specification.eigenspace_tolerance,
        )
        record["id"] = "fiber-domain-common-space-reconciliation"
        record["control_class"] = "domain-reconciliation"
        record["status"] = "reconciled"
        record["reconciles_issue_code"] = "INDEPENDENT_ROUTE.FIBER_DOMAIN_MISMATCH"
        record["nominal_real_space_cell_count"] = specification.route.cell_count
        record["common_cell_and_fiber_count"] = common_count
        record["excluded_defect_norm"] = excluded_norm
        return record

    def _weighted_coordinate_reconciliation(
        self,
        specification: ExperimentInput,
        defect: DefectControl,
        route_a: RealSpaceRouteResult,
        route_b: BlochFiberRouteResult,
        weighted_synthesis: ComplexMatrix,
        weights: npt.NDArray[np.float64],
    ) -> dict[str, JsonValue]:
        repeated_sqrt = np.repeat(np.sqrt(weights), 2)
        coordinate_scale = np.diag(repeated_sqrt)
        coordinate_scale_inverse = np.diag(1.0 / repeated_sqrt)
        weighted_inverse = coordinate_scale_inverse @ route_b.folding_map.conj().T
        identity = np.eye(weighted_synthesis.shape[0], dtype=np.complex128)
        weighted_pristine = (
            coordinate_scale_inverse @ route_b.pristine @ coordinate_scale
        )
        weighted_physical = (
            coordinate_scale_inverse @ route_b.aligned_physical @ coordinate_scale
        )
        weighted_extracted = weighted_physical - weighted_pristine
        transformed_route_a = weighted_inverse @ route_a.extracted @ weighted_synthesis
        target = weighted_inverse @ defect.matrix @ weighted_synthesis
        induced_metric = weighted_synthesis.conj().T @ weighted_synthesis
        return {
            "id": "nonuniform-weight-dual-map-reconciliation",
            "control_class": "quadrature-reconciliation",
            "status": "reconciled",
            "issue_codes": [],
            "reconciles_issue_code": ("INDEPENDENT_ROUTE.QUADRATURE_WEIGHT_MISMATCH"),
            "coordinate_rule": specification.reconciliation.weighted_coordinate_rule,
            "dimension": weighted_synthesis.shape[0],
            "minimum_weight": float(np.min(weights)),
            "maximum_weight": float(np.max(weights)),
            "weighted_synthesis_unitarity_defect": self._norm(
                weighted_synthesis.conj().T @ weighted_synthesis - identity
            ),
            "explicit_inverse_defect": self._norm(
                weighted_inverse @ weighted_synthesis - identity
            ),
            "adjoint_inverse_discrepancy": self._norm(
                weighted_synthesis.conj().T - weighted_inverse
            ),
            "induced_metric_self_adjoint_defect": self._norm(
                weighted_physical.conj().T @ induced_metric
                - induced_metric @ weighted_physical
            ),
            "route_b_planted_recovery_defect": self._norm(weighted_extracted - target),
            "route_noncommutativity_frobenius": self._norm(
                transformed_route_a - weighted_extracted
            ),
        }

    def _alignment_map_reconciliation(
        self,
        specification: ExperimentInput,
        defect: DefectControl,
        route_a: RealSpaceRouteResult,
        route_b: BlochFiberRouteResult,
        raw_candidate: ComplexMatrix,
        nominal_map: ComplexMatrix,
        altered_map: ComplexMatrix,
        energy_shift: float,
    ) -> dict[str, JsonValue]:
        relative_map = nominal_map @ altered_map.conj().T
        identity = np.eye(relative_map.shape[0], dtype=np.complex128)
        centered_candidate = raw_candidate - energy_shift * identity
        altered_physical = altered_map @ centered_candidate @ altered_map.conj().T
        altered_pristine = relative_map.conj().T @ route_a.pristine @ relative_map
        altered_extracted = altered_physical - altered_pristine
        reconciled = relative_map @ altered_extracted @ relative_map.conj().T
        folding = route_b.folding_map
        route_a_fiber = folding.conj().T @ route_a.extracted @ folding
        reconciled_fiber = folding.conj().T @ reconciled @ folding
        return {
            "id": "alignment-relative-map-reconciliation",
            "control_class": "alignment-reconciliation",
            "status": "reconciled",
            "issue_codes": [],
            "reconciles_issue_code": "INDEPENDENT_ROUTE.ALIGNMENT_MAP_MISMATCH",
            "coordinate_rule": specification.reconciliation.alignment_map_rule,
            "dimension": defect.matrix.shape[0],
            "relative_map_unitarity_defect": self._norm(
                relative_map.conj().T @ relative_map - identity
            ),
            "reconciled_physical_operator_defect": self._norm(
                relative_map @ altered_physical @ relative_map.conj().T
                - route_a.aligned_physical
            ),
            "route_b_planted_recovery_defect": self._norm(
                reconciled_fiber - folding.conj().T @ defect.matrix @ folding
            ),
            "route_noncommutativity_frobenius": self._norm(
                route_a_fiber - reconciled_fiber
            ),
        }

    def _comparison_record(
        self,
        identifier: str,
        spin_count: int,
        plant: ComplexMatrix,
        route_a: RealSpaceRouteResult,
        route_b: BlochFiberRouteResult,
        eigenspace_tolerance: float,
    ) -> dict[str, JsonValue]:
        folding = route_b.folding_map
        route_a_pristine_fiber = folding.conj().T @ route_a.pristine @ folding
        route_a_extracted_fiber = folding.conj().T @ route_a.extracted @ folding
        target_fiber = folding.conj().T @ plant @ folding
        route_defect = self._norm(route_a_extracted_fiber - route_b.extracted)
        target_norm = self._norm(target_fiber)
        values_a, vectors_a = np.linalg.eigh(
            folding.conj().T @ route_a.aligned_physical @ folding
        )
        values_b, vectors_b = np.linalg.eigh(route_b.aligned_physical)
        lowest_dimension = int(
            np.sum(np.abs(values_b - values_b[0]) <= eigenspace_tolerance)
        )
        projector_a = (
            vectors_a[:, :lowest_dimension] @ vectors_a[:, :lowest_dimension].conj().T
        )
        projector_b = (
            vectors_b[:, :lowest_dimension] @ vectors_b[:, :lowest_dimension].conj().T
        )
        fidelity: float | None = None
        if lowest_dimension == 1:
            fidelity = float(
                np.clip(abs(np.vdot(vectors_a[:, 0], vectors_b[:, 0])) ** 2, 0.0, 1.0)
            )
        return {
            "id": identifier,
            "control_class": self._control_class(identifier),
            "spin_count": spin_count,
            "status": "commuting",
            "issue_codes": [],
            "dimension": plant.shape[0],
            "folding_map_unitarity_defect": self._norm(
                folding.conj().T @ folding - np.eye(folding.shape[1])
            ),
            "representation_frobenius_discrepancy": self._norm(
                route_a_pristine_fiber - route_b.pristine
            ),
            "alignment_frobenius_defect": self._norm(
                route_a.aligned_physical - (route_a.pristine + plant)
            ),
            "route_a_planted_recovery_defect": self._norm(route_a.extracted - plant),
            "route_b_planted_recovery_defect": self._norm(
                route_b.extracted - target_fiber
            ),
            "route_noncommutativity_frobenius": route_defect,
            "route_relative_noncommutativity": (
                route_defect / target_norm if target_norm > 0.0 else 0.0
            ),
            "spectral_maximum_absolute_discrepancy": float(
                np.max(np.abs(values_a - values_b))
            ),
            "lowest_eigenspace_dimension": lowest_dimension,
            "lowest_eigenspace_projector_defect": self._norm(projector_a - projector_b),
            "lowest_state_fidelity": fidelity,
            "route_a_extracted_sha256": self._matrix_sha256(route_a.extracted),
            "route_b_extracted_sha256": self._matrix_sha256(route_b.extracted),
            "target_fiber_sha256": self._matrix_sha256(target_fiber),
        }

    @staticmethod
    def _control_class(identifier: str) -> str:
        if identifier == "null":
            return "null"
        if identifier in {"scalar-onsite", "orbital-onsite"}:
            return "local"
        if identifier in {"nearest-neighbor", "range-two-nonlocal"}:
            return "nonlocal"
        if identifier == "collinear-spin":
            return "collinear"
        if identifier == "spin-mixing":
            return "spin-mixing"
        raise ValueError(f"unknown control identifier: {identifier}")

    @staticmethod
    def _spectral_defect(first: ComplexMatrix, second: ComplexMatrix) -> float:
        return float(
            np.max(np.abs(np.linalg.eigvalsh(first) - np.linalg.eigvalsh(second)))
        )

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
