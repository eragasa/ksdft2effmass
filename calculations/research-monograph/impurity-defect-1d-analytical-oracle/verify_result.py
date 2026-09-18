#!/usr/bin/env python3
"""Independently verify the finite-rank analytical-oracle result."""

from __future__ import annotations

import argparse
import hashlib
import json
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


class AnalyticalOracleResultVerifier:
    """Reconstruct the oracle and matrix route without importing the runner."""

    __slots__ = ()

    def execute(self, result_path: Path, repository_root: Path) -> None:
        retained = self._load(result_path)
        if self._integer(retained["schema_version"], "schema version") != 1:
            raise ValueError("unsupported result schema")
        if retained["evidence_status"] != "synthetic test data":
            raise ValueError("evidence status mismatch")
        provenance = self._mapping(retained["provenance"], "provenance")
        input_path = repository_root / self._string(
            provenance["input_path"], "input path"
        )
        script_path = repository_root / self._string(
            provenance["script_path"], "script path"
        )
        self._assert_text(
            self._sha256(input_path), provenance["input_sha256"], "input sha256"
        )
        self._assert_text(
            self._sha256(script_path), provenance["script_sha256"], "script sha256"
        )
        source = self._load(input_path)
        source_records = self._records(source["source_identities"], "sources")
        retained_sources = self._records(
            retained["source_identities"], "retained sources"
        )
        if source_records != retained_sources:
            raise ValueError("retained source identities differ from input")
        for record in source_records:
            path_text = self._string(record["path"], "source path")
            digest = self._string(record["sha256"], "source sha256")
            if self._sha256(repository_root / path_text) != digest:
                raise ValueError(f"source identity mismatch: {path_text}")
        composite = self._load(
            repository_root / self._string(source_records[0]["path"], "parent path")
        )
        parent_contract = self._mapping(source["parent_contract"], "parent")
        group_id = self._string(parent_contract["composite_group_id"], "group id")
        hopping_range = self._integer(
            parent_contract["hopping_range_cells"], "hopping range"
        )
        momentum = self._real(parent_contract["supercell_momentum"], "momentum")
        hoppings = self._hoppings(composite, group_id, hopping_range)
        rank_one = self._mapping(source["rank_one_contract"], "rank one")
        cell_counts = self._integers(rank_one["supercell_sizes"], "cell counts")
        magnitudes = self._reals(rank_one["attractive_magnitudes"], "magnitudes")
        angle = self._real(rank_one["orbital_angle_radians"], "angle")
        phase = self._real(rank_one["orbital_relative_phase_radians"], "phase")
        orbital = np.asarray(
            [np.cos(angle), np.exp(1j * phase) * np.sin(angle)],
            dtype=np.complex128,
        )
        site = self._integer(rank_one["defect_site"], "defect site")
        tolerances = self._mapping(source["tolerances"], "tolerances")
        root_tolerance = self._real(tolerances["root_interval"], "root tolerance")
        edge_margin = self._real(tolerances["bound_state_edge_margin"], "edge margin")
        expected_sweep: list[JsonValue] = []
        for cell_count in cell_counts:
            for magnitude in magnitudes:
                expected_sweep.append(
                    self._rank_one_record(
                        hoppings,
                        cell_count,
                        momentum,
                        orbital,
                        site,
                        magnitude,
                        root_tolerance,
                        edge_margin,
                    )
                )
        self._assert_json(retained["rank_one_sweep"], expected_sweep, "rank one sweep")
        special = self._mapping(source["special_controls"], "special")
        expected_special = self._special_records(
            hoppings,
            momentum,
            orbital,
            site,
            special,
            root_tolerance,
            edge_margin,
        )
        self._assert_json(
            retained["special_controls"], expected_special, "special controls"
        )
        records = tuple(self._mapping(item, "sweep record") for item in expected_sweep)
        expected_summary: dict[str, JsonValue] = {
            "case_count": len(records),
            "maximum_energy_absolute_discrepancy": max(
                self._real(item["energy_absolute_discrepancy"], "energy error")
                for item in records
            ),
            "maximum_projector_frobenius_defect": max(
                self._real(item["projector_frobenius_defect"], "projector error")
                for item in records
            ),
            "maximum_oracle_secular_residual": max(
                self._real(item["oracle_secular_residual"], "secular residual")
                for item in records
            ),
            "all_attractive_bound_state_counts": [1],
        }
        self._assert_json(retained["summary"], expected_summary, "summary")
        contract = self._mapping(retained["oracle_contract"], "oracle contract")
        independence = self._string(
            contract["independence_boundary"], "independence boundary"
        )
        if "does not diagonalize the full defect Hamiltonian" not in independence:
            raise ValueError("oracle independence boundary is missing")
        limitations = retained["limitations"]
        if not isinstance(limitations, list) or len(limitations) != 4:
            raise ValueError("four limitations are required")

    def _rank_one_record(
        self,
        hoppings: tuple[tuple[int, ComplexMatrix], ...],
        cell_count: int,
        momentum: float,
        orbital: ComplexVector,
        site: int,
        magnitude: float,
        root_tolerance: float,
        edge_margin: float,
    ) -> dict[str, JsonValue]:
        edge = self._lower_edge(hoppings, cell_count, momentum)
        energy, lower, upper, residual, iterations = self._root(
            hoppings,
            cell_count,
            momentum,
            orbital,
            magnitude,
            edge,
            root_tolerance,
        )
        host = self._host(hoppings, cell_count, momentum)
        site_vector = self._site_vector(cell_count, site, orbital)
        defect = -magnitude * np.outer(site_vector, site_vector.conj())
        physical = host + defect
        values, vectors = np.linalg.eigh(physical)
        oracle_vector = self._bound_vector(
            hoppings, cell_count, momentum, energy, orbital, site
        )
        numerical_vector = vectors[:, 0]
        oracle_projector = np.outer(oracle_vector, oracle_vector.conj())
        numerical_projector = np.outer(numerical_vector, numerical_vector.conj())
        return {
            "id": f"rank-one-N{cell_count}-g{magnitude:.3f}",
            "status": "oracle_agreement",
            "cell_count": cell_count,
            "attractive_magnitude": magnitude,
            "operator_rank": int(np.linalg.matrix_rank(defect, tol=1.0e-12)),
            "host_lower_edge": edge,
            "host_edge_route_discrepancy": abs(
                edge - float(np.min(np.linalg.eigvalsh(host)))
            ),
            "oracle_energy": energy,
            "numerical_energy": float(values[0]),
            "binding_below_host_edge": edge - energy,
            "energy_absolute_discrepancy": abs(energy - float(values[0])),
            "oracle_secular_residual": residual,
            "oracle_final_bracket_width": upper - lower,
            "oracle_iteration_count": iterations,
            "numerical_bound_state_count": int(np.sum(values < edge - edge_margin)),
            "oracle_eigen_residual": self._norm(
                physical @ oracle_vector - energy * oracle_vector
            ),
            "projector_frobenius_defect": self._norm(
                oracle_projector - numerical_projector
            ),
            "state_fidelity": float(
                np.clip(
                    abs(np.vdot(oracle_vector, numerical_vector)) ** 2,
                    0.0,
                    1.0,
                )
            ),
            "defect_sha256": self._matrix_sha256(defect),
            "oracle_projector_sha256": self._matrix_sha256(oracle_projector),
        }

    def _special_records(
        self,
        hoppings: tuple[tuple[int, ComplexMatrix], ...],
        momentum: float,
        orbital: ComplexVector,
        site: int,
        special: dict[str, JsonValue],
        root_tolerance: float,
        edge_margin: float,
    ) -> dict[str, JsonValue]:
        cell_count = self._integer(special["cell_count"], "special cell count")
        attractive = self._real(special["attractive_magnitude"], "special attraction")
        repulsive = self._real(special["repulsive_magnitude"], "repulsion")
        threshold = self._real(special["threshold_magnitude"], "threshold")
        spin_count = self._integer(special["spin_degeneracy"], "spin count")
        host = self._host(hoppings, cell_count, momentum)
        edge = self._lower_edge(hoppings, cell_count, momentum)
        site_vector = self._site_vector(cell_count, site, orbital)
        threshold_count = int(np.sum(np.linalg.eigvalsh(host) < edge - edge_margin))
        probe = edge - max(edge_margin, 1.0e-4)
        green, green_imaginary = self._green(
            hoppings, cell_count, momentum, probe, orbital
        )
        repulsive_defect = repulsive * np.outer(site_vector, site_vector.conj())
        repulsive_count = int(
            np.sum(np.linalg.eigvalsh(host + repulsive_defect) < edge - edge_margin)
        )
        energy, _lower, _upper, _residual, _iterations = self._root(
            hoppings,
            cell_count,
            momentum,
            orbital,
            attractive,
            edge,
            root_tolerance,
        )
        spin_identity = np.eye(spin_count)
        spin_host = np.asarray(np.kron(host, spin_identity), dtype=np.complex128)
        spin_defect = -attractive * np.asarray(
            np.kron(np.outer(site_vector, site_vector.conj()), spin_identity),
            dtype=np.complex128,
        )
        values, vectors = np.linalg.eigh(spin_host + spin_defect)
        base_oracle = self._bound_vector(
            hoppings, cell_count, momentum, energy, orbital, site
        )
        oracle_columns = np.column_stack(
            [
                np.kron(base_oracle, spin_identity[:, index])
                for index in range(spin_count)
            ]
        )
        oracle_projector = oracle_columns @ oracle_columns.conj().T
        numerical_columns = vectors[:, :spin_count]
        numerical_projector = numerical_columns @ numerical_columns.conj().T
        degenerate: dict[str, JsonValue] = {
            "id": "spin-degenerate-rank-two-oracle",
            "status": "oracle_agreement",
            "cell_count": cell_count,
            "attractive_magnitude": attractive,
            "operator_rank": int(np.linalg.matrix_rank(spin_defect, tol=1.0e-12)),
            "oracle_eigenspace_rank": spin_count,
            "numerical_eigenspace_rank": spin_count,
            "numerical_bound_state_count": int(np.sum(values < edge - edge_margin)),
            "oracle_energy": energy,
            "maximum_energy_absolute_discrepancy": float(
                np.max(np.abs(values[:spin_count] - energy))
            ),
            "numerical_energy_splitting": float(np.ptp(values[:spin_count])),
            "projector_frobenius_defect": self._norm(
                oracle_projector - numerical_projector
            ),
            "individual_state_fidelity": None,
            "comparison_rule": "equal-rank eigenspace projectors",
            "oracle_projector_sha256": self._matrix_sha256(oracle_projector),
        }
        return {
            "threshold": {
                "id": "zero-coupling-threshold",
                "status": "threshold_no_isolated_state",
                "attractive_magnitude": threshold,
                "oracle_root_energy": None,
                "numerical_bound_state_count": threshold_count,
                "edge_state_is_not_counted_as_bound": True,
            },
            "repulsive": {
                "id": "repulsive-no-lower-bound-state",
                "status": "no_bound_state_below_lower_edge",
                "repulsive_magnitude": repulsive,
                "oracle_root_energy": None,
                "secular_value_near_lower_edge": 1.0 + repulsive * green,
                "secular_imaginary_part": green_imaginary,
                "numerical_bound_state_count": repulsive_count,
                "scope": "below the finite-host lower edge only",
            },
            "spin_degenerate": degenerate,
            "unequal_rank": {
                "id": "spin-degenerate-rank-one-comparison",
                "status": "stopped",
                "issue_codes": ["ANALYTICAL_ORACLE.EIGENSPACE_RANK_MISMATCH"],
                "numerical_eigenspace_rank": spin_count,
                "oracle_eigenspace_rank": 1,
                "projector_frobenius_defect": None,
                "state_fidelity": None,
            },
        }

    def _root(
        self,
        hoppings: tuple[tuple[int, ComplexMatrix], ...],
        cell_count: int,
        momentum: float,
        orbital: ComplexVector,
        magnitude: float,
        edge: float,
        interval_tolerance: float,
    ) -> tuple[float, float, float, float, int]:
        def secular(energy: float) -> float:
            green, _imaginary = self._green(
                hoppings, cell_count, momentum, energy, orbital
            )
            return 1.0 - magnitude * green

        upper = edge - max(interval_tolerance, 1.0e-8)
        if secular(upper) >= 0.0:
            raise ValueError("independent root is not bracketed")
        distance = max(1.0, 4.0 * magnitude)
        lower = edge - distance
        while secular(lower) <= 0.0:
            distance *= 2.0
            lower = edge - distance
            if distance > 1.0e6:
                raise ValueError("independent bracketing failed")
        iterations = 0
        while iterations < 256:
            midpoint = 0.5 * (lower + upper)
            if midpoint == lower or midpoint == upper:
                break
            if secular(midpoint) > 0.0:
                lower = midpoint
            else:
                upper = midpoint
            iterations += 1
            if upper - lower <= interval_tolerance * 0.01:
                break
        energy = 0.5 * (lower + upper)
        return energy, lower, upper, abs(secular(energy)), iterations

    def _green(
        self,
        hoppings: tuple[tuple[int, ComplexMatrix], ...],
        cell_count: int,
        momentum: float,
        energy: float,
        orbital: ComplexVector,
    ) -> tuple[float, float]:
        value = 0.0 + 0.0j
        for index in range(cell_count):
            primitive = (momentum + index / cell_count) % 1.0
            solved = np.linalg.solve(
                self._bloch(hoppings, primitive) - energy * np.eye(2), orbital
            )
            value += complex(np.vdot(orbital, solved) / cell_count)
        return float(value.real), float(value.imag)

    def _bound_vector(
        self,
        hoppings: tuple[tuple[int, ComplexMatrix], ...],
        cell_count: int,
        momentum: float,
        energy: float,
        orbital: ComplexVector,
        site: int,
    ) -> ComplexVector:
        result = np.zeros(2 * cell_count, dtype=np.complex128)
        for index in range(cell_count):
            primitive = (momentum + index / cell_count) % 1.0
            fiber = np.linalg.solve(
                self._bloch(hoppings, primitive) - energy * np.eye(2), orbital
            ) / np.sqrt(cell_count)
            fiber *= np.exp(-2j * np.pi * primitive * site)
            for target in range(cell_count):
                result[2 * target : 2 * target + 2] += (
                    np.exp(2j * np.pi * primitive * target)
                    / np.sqrt(cell_count)
                    * fiber
                )
        return result / np.linalg.norm(result)

    def _lower_edge(
        self,
        hoppings: tuple[tuple[int, ComplexMatrix], ...],
        cell_count: int,
        momentum: float,
    ) -> float:
        return min(
            float(
                np.min(
                    np.linalg.eigvalsh(
                        self._bloch(hoppings, (momentum + index / cell_count) % 1.0)
                    )
                )
            )
            for index in range(cell_count)
        )

    @staticmethod
    def _bloch(
        hoppings: tuple[tuple[int, ComplexMatrix], ...], momentum: float
    ) -> ComplexMatrix:
        result = sum(
            (
                np.exp(2j * np.pi * momentum * displacement) * matrix
                for displacement, matrix in hoppings
            ),
            start=np.zeros((2, 2), dtype=np.complex128),
        )
        return np.asarray(0.5 * (result + result.conj().T), dtype=np.complex128)

    @staticmethod
    def _host(
        hoppings: tuple[tuple[int, ComplexMatrix], ...],
        cell_count: int,
        momentum: float,
    ) -> ComplexMatrix:
        result = np.zeros((2 * cell_count, 2 * cell_count), dtype=np.complex128)
        for source in range(cell_count):
            for displacement, matrix in hoppings:
                raw = source + displacement
                target = raw % cell_count
                crossings = (raw - target) // cell_count
                result[
                    2 * source : 2 * source + 2,
                    2 * target : 2 * target + 2,
                ] += np.exp(2j * np.pi * momentum * cell_count * crossings) * matrix
        return np.asarray(0.5 * (result + result.conj().T), dtype=np.complex128)

    @staticmethod
    def _site_vector(
        cell_count: int, site: int, orbital: ComplexVector
    ) -> ComplexVector:
        result = np.zeros(2 * cell_count, dtype=np.complex128)
        result[2 * site : 2 * site + 2] = orbital
        return result

    def _hoppings(
        self, composite: dict[str, JsonValue], group_id: str, hopping_range: int
    ) -> tuple[tuple[int, ComplexMatrix], ...]:
        groups = self._records(composite["groups"], "groups")
        matches = [item for item in groups if item["id"] == group_id]
        if len(matches) != 1:
            raise ValueError("parent group mismatch")
        result: list[tuple[int, ComplexMatrix]] = []
        for record in self._records(matches[0]["smooth_hopping_blocks"], "hoppings"):
            displacement = self._integer(record["representative_cells"], "displacement")
            if abs(displacement) <= hopping_range:
                result.append(
                    (
                        displacement,
                        self._complex_matrix(record["matrix"], "hopping"),
                    )
                )
        return tuple(result)

    def _assert_json(self, actual: JsonValue, expected: JsonValue, path: str) -> None:
        if isinstance(expected, dict):
            if not isinstance(actual, dict) or set(actual) != set(expected):
                raise ValueError(f"field mismatch at {path}")
            for key, value in expected.items():
                self._assert_json(actual[key], value, f"{path}.{key}")
            return
        if isinstance(expected, list):
            if not isinstance(actual, list) or len(actual) != len(expected):
                raise ValueError(f"array mismatch at {path}")
            for index, (actual_item, expected_item) in enumerate(
                zip(actual, expected, strict=True)
            ):
                self._assert_json(actual_item, expected_item, f"{path}[{index}]")
            return
        if isinstance(expected, float):
            np.testing.assert_allclose(
                self._real(actual, path), expected, rtol=5.0e-12, atol=5.0e-14
            )
            return
        if actual != expected:
            raise ValueError(f"value mismatch at {path}")

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
        result = float(value)
        if not np.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result

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
                raise TypeError(f"{name} row must be an array")
            parsed: list[complex] = []
            for pair in row:
                if not isinstance(pair, list) or len(pair) != 2:
                    raise TypeError(f"{name} entry must be a complex pair")
                parsed.append(
                    complex(self._real(pair[0], name), self._real(pair[1], name))
                )
            rows.append(parsed)
        return np.asarray(rows, dtype=np.complex128)

    def _assert_text(self, expected: str, actual: JsonValue, name: str) -> None:
        if self._string(actual, name) != expected:
            raise ValueError(f"{name} mismatch")

    @staticmethod
    def _sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    """Adapt one retained result into the independent verifier."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    AnalyticalOracleResultVerifier().execute(arguments.result.resolve(), root)
    print("independent verification: PASS")


if __name__ == "__main__":
    main()
