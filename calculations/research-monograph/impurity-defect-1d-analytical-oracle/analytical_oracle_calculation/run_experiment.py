"""Run the finite-rank resolvent oracle for the synthetic 1D parent."""

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
type ComplexVector = npt.NDArray[np.complex128]
type RealArray = npt.NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class SourceIdentity:
    """Identify one immutable source artifact."""

    path: str
    sha256: str

    def __post_init__(self) -> None:
        if not self.path or len(self.sha256) != 64:
            raise ValueError("source identity is invalid")


@dataclass(frozen=True, slots=True)
class ParentContract:
    """Represent the finite parent convention used by every control."""

    group_id: str
    hopping_range: int
    momentum: float
    energy_unit: str
    ordering: str

    def __post_init__(self) -> None:
        if (
            not self.group_id
            or self.hopping_range < 0
            or not np.isfinite(self.momentum)
            or not self.energy_unit
            or not self.ordering
        ):
            raise ValueError("parent contract is invalid")


@dataclass(frozen=True, slots=True)
class RankOneContract:
    """Represent the rank-one oracle parameter sequence."""

    cell_counts: tuple[int, ...]
    attractive_magnitudes: tuple[float, ...]
    orbital_angle: float
    orbital_phase: float
    defect_site: int
    equation: str
    root_domain: str
    root_selection: str

    def __post_init__(self) -> None:
        if (
            not self.cell_counts
            or any(value < 2 for value in self.cell_counts)
            or tuple(sorted(set(self.cell_counts))) != self.cell_counts
            or not self.attractive_magnitudes
            or any(value <= 0.0 for value in self.attractive_magnitudes)
            or tuple(sorted(set(self.attractive_magnitudes)))
            != self.attractive_magnitudes
            or self.defect_site < 0
            or not self.equation
            or not self.root_domain
            or not self.root_selection
        ):
            raise ValueError("rank-one contract is invalid")

    @property
    def orbital_vector(self) -> ComplexVector:
        """Return the normalized authored two-orbital defect vector."""
        return np.asarray(
            [
                np.cos(self.orbital_angle),
                np.exp(1j * self.orbital_phase) * np.sin(self.orbital_angle),
            ],
            dtype=np.complex128,
        )


@dataclass(frozen=True, slots=True)
class SpecialControls:
    """Represent threshold, no-bound-state, and degeneracy controls."""

    cell_count: int
    attractive_magnitude: float
    repulsive_magnitude: float
    threshold_magnitude: float
    spin_degeneracy: int

    def __post_init__(self) -> None:
        if (
            self.cell_count < 2
            or self.attractive_magnitude <= 0.0
            or self.repulsive_magnitude <= 0.0
            or self.threshold_magnitude != 0.0
            or self.spin_degeneracy != 2
        ):
            raise ValueError("special controls are invalid")


@dataclass(frozen=True, slots=True)
class Tolerances:
    """Represent frozen numerical-verification tolerances."""

    root_interval: float
    secular_residual: float
    energy_agreement: float
    eigen_residual: float
    projector_agreement: float
    edge_margin: float

    def __post_init__(self) -> None:
        if any(
            value <= 0.0
            for value in (
                self.root_interval,
                self.secular_residual,
                self.energy_agreement,
                self.eigen_residual,
                self.projector_agreement,
                self.edge_margin,
            )
        ):
            raise ValueError("tolerances must be positive")


@dataclass(frozen=True, slots=True)
class ExperimentInput:
    """Represent the closed analytical-oracle input."""

    experiment_id: str
    sources: tuple[SourceIdentity, ...]
    parent: ParentContract
    rank_one: RankOneContract
    special: SpecialControls
    tolerances: Tolerances


@dataclass(frozen=True, slots=True)
class HoppingBlock:
    """Retain one immutable two-orbital hopping block."""

    displacement: int
    matrix: ComplexMatrix

    def __post_init__(self) -> None:
        value = np.asarray(self.matrix, dtype=np.complex128)
        if value.shape != (2, 2) or not np.all(np.isfinite(value)):
            raise ValueError("hopping matrix must be finite and 2 by 2")
        immutable = np.frombuffer(
            value.tobytes(order="C"), dtype=np.complex128
        ).reshape(value.shape)
        object.__setattr__(self, "matrix", immutable)


@dataclass(frozen=True, slots=True)
class ParentData:
    """Retain the accepted parent and verified source identities."""

    hoppings: tuple[HoppingBlock, ...]
    sources: tuple[SourceIdentity, ...]


@dataclass(frozen=True, slots=True)
class RootResult:
    """Record one independently resolved rank-one secular root."""

    energy: float
    lower_bracket: float
    upper_bracket: float
    secular_residual: float
    iteration_count: int

    def __post_init__(self) -> None:
        if (
            not np.isfinite(self.energy)
            or self.lower_bracket > self.energy
            or self.energy > self.upper_bracket
            or self.secular_residual < 0.0
            or self.iteration_count < 1
        ):
            raise ValueError("root result is invalid")


class ExperimentInputDeserializer:
    """Deserialize the versioned analytical-oracle input."""

    __slots__ = ()

    def execute(self, payload: bytes) -> ExperimentInput:
        root = self._mapping(cast(JsonValue, json.loads(payload)), "input")
        if self._integer(root["schema_version"], "schema version") != 1:
            raise ValueError("unsupported schema version")
        if root["evidence_status"] != "synthetic test data":
            raise ValueError("evidence status mismatch")
        sources = tuple(
            SourceIdentity(
                self._string(item["path"], "source path"),
                self._string(item["sha256"], "source sha256"),
            )
            for item in self._records(root["source_identities"], "sources")
        )
        parent = self._mapping(root["parent_contract"], "parent")
        rank_one = self._mapping(root["rank_one_contract"], "rank one")
        special = self._mapping(root["special_controls"], "special")
        tolerances = self._mapping(root["tolerances"], "tolerances")
        return ExperimentInput(
            self._string(root["experiment_id"], "experiment id"),
            sources,
            ParentContract(
                self._string(parent["composite_group_id"], "group id"),
                self._integer(parent["hopping_range_cells"], "hopping range"),
                self._real(parent["supercell_momentum"], "momentum"),
                self._string(parent["energy_unit"], "energy unit"),
                self._string(parent["site_orbital_ordering"], "ordering"),
            ),
            RankOneContract(
                self._integers(rank_one["supercell_sizes"], "cell counts"),
                self._reals(rank_one["attractive_magnitudes"], "attractive magnitudes"),
                self._real(rank_one["orbital_angle_radians"], "orbital angle"),
                self._real(rank_one["orbital_relative_phase_radians"], "orbital phase"),
                self._integer(rank_one["defect_site"], "defect site"),
                self._string(rank_one["resolvent_equation"], "equation"),
                self._string(rank_one["root_domain"], "root domain"),
                self._string(rank_one["root_selection"], "root selection"),
            ),
            SpecialControls(
                self._integer(special["cell_count"], "special cell count"),
                self._real(special["attractive_magnitude"], "special attraction"),
                self._real(special["repulsive_magnitude"], "repulsion"),
                self._real(special["threshold_magnitude"], "threshold"),
                self._integer(special["spin_degeneracy"], "spin degeneracy"),
            ),
            Tolerances(
                self._real(tolerances["root_interval"], "root interval"),
                self._real(tolerances["secular_residual"], "secular residual"),
                self._real(tolerances["energy_agreement"], "energy agreement"),
                self._real(tolerances["eigen_residual"], "eigen residual"),
                self._real(tolerances["projector_agreement"], "projector agreement"),
                self._real(tolerances["bound_state_edge_margin"], "edge margin"),
            ),
        )

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
        result = float(value)
        if not np.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result

    def _reals(self, value: JsonValue, name: str) -> tuple[float, ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be an array")
        return tuple(self._real(item, name) for item in value)


class ParentDataLoader:
    """Load and verify the accepted two-orbital parent."""

    __slots__ = ()

    def execute(
        self, specification: ExperimentInput, repository_root: Path
    ) -> ParentData:
        for identity in specification.sources:
            if self._sha256(repository_root / identity.path) != identity.sha256:
                raise ValueError(f"source identity mismatch: {identity.path}")
        composite_source = specification.sources[0]
        composite = self._load(repository_root / composite_source.path)
        groups = self._records(composite["groups"], "groups")
        matches = [
            item for item in groups if item["id"] == specification.parent.group_id
        ]
        if len(matches) != 1:
            raise ValueError("parent group must occur exactly once")
        hoppings: list[HoppingBlock] = []
        for record in self._records(
            matches[0]["smooth_hopping_blocks"], "hopping blocks"
        ):
            displacement = self._integer(record["representative_cells"], "displacement")
            if abs(displacement) <= specification.parent.hopping_range:
                hoppings.append(
                    HoppingBlock(
                        displacement,
                        self._complex_matrix(record["matrix"], "hopping matrix"),
                    )
                )
        expected = tuple(
            range(
                -specification.parent.hopping_range,
                specification.parent.hopping_range + 1,
            )
        )
        if tuple(item.displacement for item in hoppings) != expected:
            raise ValueError("parent hopping range is incomplete")
        return ParentData(tuple(hoppings), specification.sources)

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

    def _complex_matrix(self, value: JsonValue, name: str) -> ComplexMatrix:
        if not isinstance(value, list) or not value:
            raise TypeError(f"{name} must be a nonempty matrix")
        rows: list[list[complex]] = []
        for row in value:
            if not isinstance(row, list):
                raise TypeError(f"{name} row must be an array")
            parsed: list[complex] = []
            for pair in row:
                if not isinstance(pair, list) or len(pair) != 2:
                    raise TypeError(f"{name} entry must be a complex pair")
                real = pair[0]
                imaginary = pair[1]
                if (
                    isinstance(real, bool)
                    or not isinstance(real, int | float)
                    or isinstance(imaginary, bool)
                    or not isinstance(imaginary, int | float)
                ):
                    raise TypeError(f"{name} components must be numeric")
                parsed.append(complex(float(real), float(imaginary)))
            rows.append(parsed)
        return np.asarray(rows, dtype=np.complex128)

    @staticmethod
    def _sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()


class SupercellOperatorBuilder:
    """Assemble the finite site-space parent independently of the oracle."""

    __slots__ = ()

    def execute(
        self,
        parent: ParentData,
        cell_count: int,
        momentum: float,
    ) -> ComplexMatrix:
        result = np.zeros((2 * cell_count, 2 * cell_count), dtype=np.complex128)
        for source in range(cell_count):
            for hopping in parent.hoppings:
                raw = source + hopping.displacement
                target = raw % cell_count
                crossings = (raw - target) // cell_count
                phase = np.exp(2j * np.pi * momentum * cell_count * crossings)
                result[
                    2 * source : 2 * source + 2,
                    2 * target : 2 * target + 2,
                ] += phase * hopping.matrix
        antihermitian = np.linalg.norm(result - result.conj().T)
        if antihermitian > 1.0e-11:
            raise ValueError("supercell parent is not Hermitian")
        return np.asarray(0.5 * (result + result.conj().T), dtype=np.complex128)


class FiniteRankResolventEvaluator:
    """Evaluate Bloch fibers and finite-host resolvents without a large eigensolve."""

    __slots__ = ()

    def bloch_matrix(self, parent: ParentData, momentum: float) -> ComplexMatrix:
        result = np.zeros((2, 2), dtype=np.complex128)
        for hopping in parent.hoppings:
            result += (
                np.exp(2j * np.pi * momentum * hopping.displacement) * hopping.matrix
            )
        antihermitian = np.linalg.norm(result - result.conj().T)
        if antihermitian > 1.0e-11:
            raise ValueError("Bloch parent is not Hermitian")
        return np.asarray(0.5 * (result + result.conj().T), dtype=np.complex128)

    def lower_edge(
        self,
        parent: ParentData,
        cell_count: int,
        supercell_momentum: float,
    ) -> float:
        edge = np.inf
        for index in range(cell_count):
            momentum = (supercell_momentum + index / cell_count) % 1.0
            edge = min(
                edge,
                float(np.min(np.linalg.eigvalsh(self.bloch_matrix(parent, momentum)))),
            )
        return float(edge)

    def local_green(
        self,
        parent: ParentData,
        cell_count: int,
        supercell_momentum: float,
        energy: float,
        orbital: ComplexVector,
    ) -> tuple[float, float, float]:
        value = 0.0 + 0.0j
        derivative = 0.0
        for index in range(cell_count):
            momentum = (supercell_momentum + index / cell_count) % 1.0
            shifted = self.bloch_matrix(parent, momentum) - energy * np.eye(2)
            solved = np.linalg.solve(shifted, orbital)
            value += complex(np.vdot(orbital, solved) / cell_count)
            derivative += float(np.vdot(solved, solved).real) / cell_count
        return float(value.real), float(value.imag), derivative

    def bound_vector(
        self,
        parent: ParentData,
        cell_count: int,
        supercell_momentum: float,
        energy: float,
        orbital: ComplexVector,
        defect_site: int,
    ) -> ComplexVector:
        result = np.zeros(2 * cell_count, dtype=np.complex128)
        for index in range(cell_count):
            momentum = (supercell_momentum + index / cell_count) % 1.0
            shifted = self.bloch_matrix(parent, momentum) - energy * np.eye(2)
            fiber = np.linalg.solve(shifted, orbital) / np.sqrt(cell_count)
            fiber *= np.exp(-2j * np.pi * momentum * defect_site)
            for site in range(cell_count):
                result[2 * site : 2 * site + 2] += (
                    np.exp(2j * np.pi * momentum * site) / np.sqrt(cell_count) * fiber
                )
        return result / np.linalg.norm(result)


class RankOneRootResolver:
    """Resolve the unique attractive secular root below the finite-host edge."""

    __slots__ = ("_resolvent",)

    def __init__(self, resolvent: FiniteRankResolventEvaluator) -> None:
        self._resolvent = resolvent

    def execute(
        self,
        parent: ParentData,
        cell_count: int,
        momentum: float,
        orbital: ComplexVector,
        magnitude: float,
        edge: float,
        interval_tolerance: float,
    ) -> RootResult:
        if magnitude <= 0.0:
            raise ValueError("attractive magnitude must be positive")

        def secular(energy: float) -> float:
            green, imaginary, _derivative = self._resolvent.local_green(
                parent, cell_count, momentum, energy, orbital
            )
            if abs(imaginary) > 1.0e-9 * max(1.0, abs(green)):
                raise ValueError(
                    "resolvent acquired an unexpected relative imaginary part"
                )
            return 1.0 - magnitude * green

        upper = edge - max(interval_tolerance, 1.0e-8)
        upper_value = secular(upper)
        if upper_value >= 0.0:
            raise ValueError("root is not bracketed below the host edge")
        distance = max(1.0, 4.0 * magnitude)
        lower = edge - distance
        lower_value = secular(lower)
        while lower_value <= 0.0:
            distance *= 2.0
            lower = edge - distance
            lower_value = secular(lower)
            if distance > 1.0e6:
                raise ValueError("failed to bracket the secular root")
        iterations = 0
        while iterations < 256:
            midpoint = 0.5 * (lower + upper)
            if midpoint == lower or midpoint == upper:
                break
            value = secular(midpoint)
            if value > 0.0:
                lower = midpoint
            else:
                upper = midpoint
            iterations += 1
            if upper - lower <= interval_tolerance * 0.01:
                break
        energy = 0.5 * (lower + upper)
        residual = abs(secular(energy))
        return RootResult(energy, lower, upper, residual, iterations)


class AnalyticalOracleExperiment:
    """Compare finite-rank resolvent roots with independent matrix eigensolves."""

    __slots__ = ("_builder", "_resolvent", "_root")

    def __init__(self) -> None:
        self._builder = SupercellOperatorBuilder()
        self._resolvent = FiniteRankResolventEvaluator()
        self._root = RankOneRootResolver(self._resolvent)

    def execute(
        self,
        specification: ExperimentInput,
        parent: ParentData,
        input_path: Path,
        script_path: Path,
    ) -> bytes:
        sweep: list[JsonValue] = []
        for cell_count in specification.rank_one.cell_counts:
            for magnitude in specification.rank_one.attractive_magnitudes:
                sweep.append(
                    self._rank_one_record(specification, parent, cell_count, magnitude)
                )
        special = self._special_records(specification, parent)
        sweep_records = tuple(cast(dict[str, JsonValue], item) for item in sweep)
        energy_errors = [
            self._real(item["energy_absolute_discrepancy"]) for item in sweep_records
        ]
        projector_errors = [
            self._real(item["projector_frobenius_defect"]) for item in sweep_records
        ]
        secular_residuals = [
            self._real(item["oracle_secular_residual"]) for item in sweep_records
        ]
        bound_state_counts = [
            cast(JsonValue, value)
            for value in sorted(
                {
                    self._integer(item["numerical_bound_state_count"])
                    for item in sweep_records
                }
            )
        ]
        root = script_path.parents[3]
        payload: dict[str, JsonValue] = {
            "schema_version": 1,
            "experiment_id": specification.experiment_id,
            "evidence_status": "synthetic test data",
            "calculation_status": (
                "calculated synthetic numerical-verification result"
            ),
            "oracle_contract": {
                "finite_rank_identity": specification.rank_one.equation,
                "root_domain": specification.rank_one.root_domain,
                "root_selection": specification.rank_one.root_selection,
                "oracle_route": (
                    "direct 2 by 2 Bloch-fiber resolvent sum and scalar bisection"
                ),
                "numerical_route": (
                    "independent dense site-space assembly and Hermitian eigensolve"
                ),
                "independence_boundary": (
                    "The oracle does not diagonalize the full defect Hamiltonian; "
                    "the numerical route does not call the resolvent root resolver."
                ),
            },
            "represented_space": {
                "group_id": specification.parent.group_id,
                "hopping_range_cells": specification.parent.hopping_range,
                "supercell_momentum": specification.parent.momentum,
                "energy_unit": specification.parent.energy_unit,
                "ordering": specification.parent.ordering,
                "orbital_vector": [
                    [float(value.real), float(value.imag)]
                    for value in specification.rank_one.orbital_vector
                ],
                "defect_site": specification.rank_one.defect_site,
            },
            "rank_one_sweep": sweep,
            "special_controls": special,
            "summary": {
                "case_count": len(sweep),
                "maximum_energy_absolute_discrepancy": max(energy_errors),
                "maximum_projector_frobenius_defect": max(projector_errors),
                "maximum_oracle_secular_residual": max(secular_residuals),
                "all_attractive_bound_state_counts": bound_state_counts,
            },
            "error_accounting": {
                "oracle_root_error": "retained secular residual and final bracket",
                "numerical_spectral_error": (
                    "oracle root versus independently diagonalized defect energy"
                ),
                "state_error": (
                    "equal-rank projector defect and nondegenerate fidelity"
                ),
                "finite_size_dependence": (
                    "reported by supercell size without a continuum-limit claim"
                ),
                "model_reduction_error": "Not evaluated in this exercise.",
                "scientific_validation": "Not performed.",
                "uncertainty_quantification": "Not performed.",
            },
            "source_identities": [
                {"path": item.path, "sha256": item.sha256} for item in parent.sources
            ],
            "limitations": [
                "The parent, finite-rank defects, and all observations are synthetic.",
                (
                    "The resolvent identity verifies finite represented operators, not a "
                    "continuum impurity model."
                ),
                (
                    "The supercell sequence measures finite-size dependence but does not "
                    "establish convergence to an infinite system."
                ),
                (
                    "No silicon, dopant, DFT, material validation, transferability, "
                    "scientific validation, or UQ claim is made."
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

    def _rank_one_record(
        self,
        specification: ExperimentInput,
        parent: ParentData,
        cell_count: int,
        magnitude: float,
    ) -> dict[str, JsonValue]:
        momentum = specification.parent.momentum
        orbital = specification.rank_one.orbital_vector
        edge = self._resolvent.lower_edge(parent, cell_count, momentum)
        root = self._root.execute(
            parent,
            cell_count,
            momentum,
            orbital,
            magnitude,
            edge,
            specification.tolerances.root_interval,
        )
        host = self._builder.execute(parent, cell_count, momentum)
        site_vector = self._site_vector(
            cell_count, specification.rank_one.defect_site, orbital
        )
        defect = -magnitude * np.outer(site_vector, site_vector.conj())
        physical = host + defect
        values, vectors = np.linalg.eigh(physical)
        oracle_vector = self._resolvent.bound_vector(
            parent,
            cell_count,
            momentum,
            root.energy,
            orbital,
            specification.rank_one.defect_site,
        )
        numerical_vector = vectors[:, 0]
        fidelity = float(
            np.clip(abs(np.vdot(oracle_vector, numerical_vector)) ** 2, 0.0, 1.0)
        )
        oracle_projector = np.outer(oracle_vector, oracle_vector.conj())
        numerical_projector = np.outer(numerical_vector, numerical_vector.conj())
        numerical_host_edge = float(np.min(np.linalg.eigvalsh(host)))
        bound_count = int(np.sum(values < edge - specification.tolerances.edge_margin))
        energy_error = abs(root.energy - float(values[0]))
        eigen_residual = self._norm(
            physical @ oracle_vector - root.energy * oracle_vector
        )
        projector_defect = self._norm(oracle_projector - numerical_projector)
        if (
            energy_error > specification.tolerances.energy_agreement
            or root.secular_residual > specification.tolerances.secular_residual
            or eigen_residual > specification.tolerances.eigen_residual
            or projector_defect > specification.tolerances.projector_agreement
            or bound_count != 1
        ):
            raise ValueError("rank-one oracle comparison failed its frozen rule")
        return {
            "id": f"rank-one-N{cell_count}-g{magnitude:.3f}",
            "status": "oracle_agreement",
            "cell_count": cell_count,
            "attractive_magnitude": magnitude,
            "operator_rank": int(np.linalg.matrix_rank(defect, tol=1.0e-12)),
            "host_lower_edge": edge,
            "host_edge_route_discrepancy": abs(edge - numerical_host_edge),
            "oracle_energy": root.energy,
            "numerical_energy": float(values[0]),
            "binding_below_host_edge": edge - root.energy,
            "energy_absolute_discrepancy": energy_error,
            "oracle_secular_residual": root.secular_residual,
            "oracle_final_bracket_width": root.upper_bracket - root.lower_bracket,
            "oracle_iteration_count": root.iteration_count,
            "numerical_bound_state_count": bound_count,
            "oracle_eigen_residual": eigen_residual,
            "projector_frobenius_defect": projector_defect,
            "state_fidelity": fidelity,
            "defect_sha256": self._matrix_sha256(defect),
            "oracle_projector_sha256": self._matrix_sha256(oracle_projector),
        }

    def _special_records(
        self, specification: ExperimentInput, parent: ParentData
    ) -> dict[str, JsonValue]:
        control = specification.special
        momentum = specification.parent.momentum
        orbital = specification.rank_one.orbital_vector
        host = self._builder.execute(parent, control.cell_count, momentum)
        edge = self._resolvent.lower_edge(parent, control.cell_count, momentum)
        site_vector = self._site_vector(
            control.cell_count, specification.rank_one.defect_site, orbital
        )
        threshold_values = np.linalg.eigvalsh(host)
        threshold_count = int(
            np.sum(threshold_values < edge - specification.tolerances.edge_margin)
        )
        probe = edge - max(specification.tolerances.edge_margin, 1.0e-4)
        green, green_imaginary, _derivative = self._resolvent.local_green(
            parent, control.cell_count, momentum, probe, orbital
        )
        repulsive_defect = control.repulsive_magnitude * np.outer(
            site_vector, site_vector.conj()
        )
        repulsive_values = np.linalg.eigvalsh(host + repulsive_defect)
        repulsive_count = int(
            np.sum(repulsive_values < edge - specification.tolerances.edge_margin)
        )
        if threshold_count != 0 or repulsive_count != 0:
            raise ValueError(
                "threshold or repulsive control produced a lower bound state"
            )
        degenerate = self._degenerate_record(specification, parent)
        return {
            "threshold": {
                "id": "zero-coupling-threshold",
                "status": "threshold_no_isolated_state",
                "attractive_magnitude": control.threshold_magnitude,
                "oracle_root_energy": None,
                "numerical_bound_state_count": threshold_count,
                "edge_state_is_not_counted_as_bound": True,
            },
            "repulsive": {
                "id": "repulsive-no-lower-bound-state",
                "status": "no_bound_state_below_lower_edge",
                "repulsive_magnitude": control.repulsive_magnitude,
                "oracle_root_energy": None,
                "secular_value_near_lower_edge": 1.0
                + control.repulsive_magnitude * green,
                "secular_imaginary_part": green_imaginary,
                "numerical_bound_state_count": repulsive_count,
                "scope": "below the finite-host lower edge only",
            },
            "spin_degenerate": degenerate,
            "unequal_rank": {
                "id": "spin-degenerate-rank-one-comparison",
                "status": "stopped",
                "issue_codes": ["ANALYTICAL_ORACLE.EIGENSPACE_RANK_MISMATCH"],
                "numerical_eigenspace_rank": control.spin_degeneracy,
                "oracle_eigenspace_rank": 1,
                "projector_frobenius_defect": None,
                "state_fidelity": None,
            },
        }

    def _degenerate_record(
        self, specification: ExperimentInput, parent: ParentData
    ) -> dict[str, JsonValue]:
        control = specification.special
        momentum = specification.parent.momentum
        orbital = specification.rank_one.orbital_vector
        edge = self._resolvent.lower_edge(parent, control.cell_count, momentum)
        root = self._root.execute(
            parent,
            control.cell_count,
            momentum,
            orbital,
            control.attractive_magnitude,
            edge,
            specification.tolerances.root_interval,
        )
        host = self._builder.execute(parent, control.cell_count, momentum)
        site_vector = self._site_vector(
            control.cell_count, specification.rank_one.defect_site, orbital
        )
        spin_identity = np.eye(control.spin_degeneracy)
        spin_host = np.asarray(np.kron(host, spin_identity), dtype=np.complex128)
        spin_defect = -control.attractive_magnitude * np.asarray(
            np.kron(np.outer(site_vector, site_vector.conj()), spin_identity),
            dtype=np.complex128,
        )
        values, vectors = np.linalg.eigh(spin_host + spin_defect)
        base_oracle = self._resolvent.bound_vector(
            parent,
            control.cell_count,
            momentum,
            root.energy,
            orbital,
            specification.rank_one.defect_site,
        )
        oracle_columns = np.column_stack(
            [
                np.kron(base_oracle, spin_identity[:, index])
                for index in range(control.spin_degeneracy)
            ]
        )
        oracle_projector = oracle_columns @ oracle_columns.conj().T
        numerical_columns = vectors[:, : control.spin_degeneracy]
        numerical_projector = numerical_columns @ numerical_columns.conj().T
        bound_count = int(np.sum(values < edge - specification.tolerances.edge_margin))
        energy_error = float(
            np.max(np.abs(values[: control.spin_degeneracy] - root.energy))
        )
        projector_defect = self._norm(oracle_projector - numerical_projector)
        if (
            bound_count != control.spin_degeneracy
            or energy_error > specification.tolerances.energy_agreement
            or projector_defect > specification.tolerances.projector_agreement
        ):
            raise ValueError("degenerate oracle comparison failed its frozen rule")
        return {
            "id": "spin-degenerate-rank-two-oracle",
            "status": "oracle_agreement",
            "cell_count": control.cell_count,
            "attractive_magnitude": control.attractive_magnitude,
            "operator_rank": int(np.linalg.matrix_rank(spin_defect, tol=1.0e-12)),
            "oracle_eigenspace_rank": control.spin_degeneracy,
            "numerical_eigenspace_rank": control.spin_degeneracy,
            "numerical_bound_state_count": bound_count,
            "oracle_energy": root.energy,
            "maximum_energy_absolute_discrepancy": energy_error,
            "numerical_energy_splitting": float(
                np.ptp(values[: control.spin_degeneracy])
            ),
            "projector_frobenius_defect": projector_defect,
            "individual_state_fidelity": None,
            "comparison_rule": "equal-rank eigenspace projectors",
            "oracle_projector_sha256": self._matrix_sha256(oracle_projector),
        }

    @staticmethod
    def _site_vector(
        cell_count: int, defect_site: int, orbital: ComplexVector
    ) -> ComplexVector:
        if defect_site >= cell_count:
            raise ValueError("defect site lies outside the supercell")
        result = np.zeros(2 * cell_count, dtype=np.complex128)
        result[2 * defect_site : 2 * defect_site + 2] = orbital
        return result

    @staticmethod
    def _matrix_sha256(matrix: ComplexMatrix) -> str:
        canonical = np.stack((matrix.real, matrix.imag), axis=-1).astype(
            "<f8", copy=True
        )
        canonical[canonical == 0.0] = 0.0
        return hashlib.sha256(canonical.tobytes(order="C")).hexdigest()

    @staticmethod
    def _norm(value: ComplexMatrix | ComplexVector | RealArray) -> float:
        return float(np.linalg.norm(value))

    @staticmethod
    def _real(value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("retained value must be numeric")
        return float(value)

    @staticmethod
    def _integer(value: JsonValue) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("retained value must be an integer")
        return value

    @staticmethod
    def _sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()
