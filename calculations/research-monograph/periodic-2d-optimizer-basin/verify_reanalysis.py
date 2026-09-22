#!/usr/bin/env python3
"""Independently verify the offline optimizer-basin reanalysis."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import re
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type ComplexMatrix = npt.NDArray[np.complex128]
type ComplexFrames = npt.NDArray[np.complex128]
type RealMatrix = npt.NDArray[np.float64]


class OfflineReanalysisVerifier:
    """Reconstruct native diagnostics, symmetry basins, and FFT refinement."""

    __slots__ = ()

    _trace_pattern = re.compile(
        r"^\s*(\d+)\s+([-+0-9.Ee]+)\s+([-+0-9.Ee]+)\s+"
        r"([-+0-9.Ee]+)\s+([-+0-9.Ee]+)\s+<-- CONV$",
        re.MULTILINE,
    )

    def execute(self, result_path: Path) -> None:
        result = self._load(result_path)
        if self._integer(result["schema_version"]) != 1:
            raise ValueError("unsupported reanalysis schema")
        repository_root = result_path.parents[3]
        provenance = self._mapping(result["provenance"])
        source_path = repository_root / self._string(provenance["source_result_path"])
        reanalyzer_path = repository_root / self._string(provenance["reanalyzer_path"])
        base_extractor_path = repository_root / self._string(
            provenance["base_extractor_path"]
        )
        self._identity(source_path, provenance["source_result_sha256"], "source")
        self._identity(reanalyzer_path, provenance["reanalyzer_sha256"], "reanalyzer")
        self._identity(
            base_extractor_path,
            provenance["base_extractor_sha256"],
            "base extractor",
        )
        source = self._load(source_path)
        source_configurations = {
            self._string(self._mapping(value)["configuration_id"]): self._mapping(value)
            for value in self._array(source["configurations"])
        }
        method = self._mapping(result["method"])
        diagnostic_counts: dict[str, int] = {}
        for configuration_value in self._array(result["configurations"]):
            configuration = self._mapping(configuration_value)
            identifier = self._string(configuration["configuration_id"])
            self._verify_configuration(
                configuration,
                source_configurations[identifier],
                method,
                diagnostic_counts,
            )
        observed_counts = self._mapping(result["diagnostic_classification_counts"])
        if diagnostic_counts != {
            key: self._integer(value) for key, value in observed_counts.items()
        }:
            raise AssertionError("diagnostic classification counts disagree")
        for refinement_value in self._array(result["common_estimator_refinement"]):
            self._verify_refinement(self._mapping(refinement_value))

    def _verify_configuration(
        self,
        configuration: dict[str, JsonValue],
        source: dict[str, JsonValue],
        method: dict[str, JsonValue],
        diagnostic_counts: dict[str, int],
    ) -> None:
        source_starts = {
            self._string(self._mapping(value)["gauge_id"]): self._mapping(value)
            for value in self._array(source["starts"])
        }
        starts = [
            self._mapping(value) for value in self._array(configuration["starts"])
        ]
        for start in starts:
            gauge_id = self._string(start["gauge_id"])
            source_start = source_starts[gauge_id]
            self._identity(
                Path(self._string(start["source_analysis_result_path"])),
                start["source_analysis_result_sha256"],
                f"{configuration['configuration_id']}/{gauge_id}",
            )
            self._verify_native(start, source_start)
            classification = self._string(
                self._mapping(start["spread_components"])["diagnostic_classification"]
            )
            diagnostic_counts[classification] = (
                diagnostic_counts.get(classification, 0) + 1
            )
        converged = [
            value
            for value in starts
            if value["convergence_criterion_satisfied"] is True
        ]
        expected = self._clusters(
            converged,
            self._real(method["basin_spread_absolute_tolerance"]),
            self._real(method["basin_center_set_periodic_tolerance"]),
        )
        observed = [
            sorted(
                self._string(gauge)
                for gauge in self._array(self._mapping(value)["gauge_ids"])
            )
            for value in self._array(configuration["symmetry_aware_observed_basins"])
        ]
        if sorted(expected) != sorted(observed):
            raise AssertionError("symmetry-aware basin membership disagrees")

    def _verify_native(
        self, start: dict[str, JsonValue], source_start: dict[str, JsonValue]
    ) -> None:
        analysis_path = Path(self._string(start["source_analysis_result_path"]))
        analysis = self._load(analysis_path)
        run_root = Path(
            self._string(self._mapping(analysis["provenance"])["external_run_root"])
        )
        seed_root = run_root / "low_triple"
        text = (seed_root / "low_triple.wout").read_text(encoding="utf-8")
        final = text.rsplit("Final State", maxsplit=1)[1]
        components = self._mapping(start["spread_components"])
        values = {
            "omega_i_cell_squared": self._component(final, r"Omega I\s+=\s+([^\s]+)"),
            "omega_d_cell_squared": self._component(final, r"Omega D\s+=\s+([^\s]+)"),
            "omega_od_cell_squared": self._component(final, r"Omega OD\s+=\s+([^\s]+)"),
            "omega_total_cell_squared": self._component(
                final, r"Omega Total\s+=\s+([^\s]+)"
            ),
        }
        values["omega_tilde_cell_squared"] = (
            values["omega_d_cell_squared"] + values["omega_od_cell_squared"]
        )
        for key, value in values.items():
            self._close(value, self._real(components[key]), 2.0e-12, key)
        trace = [
            (
                int(match.group(1)),
                float(match.group(2)),
                float(match.group(3)),
                float(match.group(4)),
            )
            for match in self._trace_pattern.finditer(text)
        ]
        tail = trace[-min(200, len(trace)) :]
        iterations = np.asarray([value[0] for value in tail], dtype=float)
        deltas = np.asarray([value[1] for value in tail], dtype=float)
        gradients = np.asarray([value[2] for value in tail], dtype=float)
        spreads = np.asarray([value[3] for value in tail], dtype=float)
        slope = float(np.polyfit(iterations, spreads, deg=1)[0])
        trend = slope * (iterations - np.mean(iterations)) + np.mean(spreads)
        metrics = {
            "terminal_spread_slope_per_iteration": slope,
            "terminal_detrended_spread_rms": float(
                np.sqrt(np.mean((spreads - trend) ** 2))
            ),
            "terminal_median_absolute_delta_spread": float(np.median(np.abs(deltas))),
            "terminal_median_rms_gradient": float(np.median(gradients)),
        }
        for key, value in metrics.items():
            self._close(value, self._real(components[key]), 1.0e-15, key)
        expected_classification = self._classification(
            source_start["convergence_criterion_satisfied"] is True,
            metrics,
        )
        if components["diagnostic_classification"] != expected_classification:
            raise AssertionError("trace diagnostic classification disagrees")
        radius_18 = self._hopping_tail(seed_root / "low_triple_hr.dat", 18)
        self._close(
            radius_18,
            self._real(start["radius_18_hopping_tail_energy_units"]),
            1.0e-14,
            "radius-18 hopping tail",
        )

    def _classification(self, converged: bool, metrics: dict[str, float]) -> str:
        if converged:
            return "native_converged"
        if (
            metrics["terminal_median_absolute_delta_spread"] <= 1.0e-8
            and metrics["terminal_median_rms_gradient"] <= 1.0e-3
        ):
            return "near_stationary_without_window_convergence"
        if metrics["terminal_spread_slope_per_iteration"] < -1.0e-8:
            return "continuing_descent_at_iteration_limit"
        if metrics["terminal_detrended_spread_rms"] > 1.0e-5:
            return "oscillatory_or_stalled"
        return "stalled_or_nondescent"

    def _verify_refinement(self, refinement: dict[str, JsonValue]) -> None:
        source_path = Path(self._string(refinement["source_analysis_result_path"]))
        self._identity(
            source_path,
            refinement["source_analysis_result_sha256"],
            self._string(refinement["case_id"]),
        )
        source = self._load(source_path)
        portable = self._mapping(source["portable_evidence"])
        kpoints = self._real_matrix(portable["kpoints_fractional"])
        unitaries = self._complex_tensor(portable["w90_unitaries_real_imaginary"])
        for size_value in self._array(refinement["sizes"]):
            size = self._mapping(size_value)
            input_path = Path(self._string(size["input_path"]))
            self._identity(input_path, size["input_sha256"], str(input_path))
            controls = self._load(input_path)
            frames = self._raw_frames(controls, kpoints) @ unitaries
            records = self._finite_localization(
                controls,
                kpoints,
                frames,
                self._integer(size["fft_size"]),
            )
            total = sum(value[0] for value in records)
            self._close(
                total,
                self._real(size["common_total_spread_cell_squared"]),
                2.0e-10,
                "refined common spread",
            )
            centers = [value[1] for value in records]
            distance = self._center_set_distance(
                cast(JsonValue, [list(value) for value in centers]),
                size["common_centers_modulo_cell"],
                d4=False,
            )
            if distance > 2.0e-10:
                raise AssertionError("refined common centers disagree")
            minimum_norm = min(value[2] for value in records)
            self._close(
                minimum_norm,
                self._real(size["minimum_coefficient_norm"]),
                2.0e-10,
                "refined coefficient norm",
            )

    def _raw_frames(
        self, controls: dict[str, JsonValue], kpoints: RealMatrix
    ) -> ComplexFrames:
        potential = self._mapping(controls["potential"])
        cutoff = self._integer(controls["plane_wave_cutoff"])
        dimension = (2 * cutoff + 1) ** 2
        frames = np.empty((kpoints.shape[0], dimension, 3), dtype=complex)
        for index, point in enumerate(kpoints):
            operator = self._operator(
                cutoff,
                float(point[0]),
                float(point[1]),
                self._real(potential["lambda_x"]),
                self._real(potential["lambda_y"]),
                self._real(potential["lambda_xy"]),
            )
            _, eigenvectors = np.linalg.eigh(operator)
            frames[index] = eigenvectors[:, :3]
        return frames

    @staticmethod
    def _operator(
        cutoff: int,
        kx: float,
        ky: float,
        lambda_x: float,
        lambda_y: float,
        lambda_xy: float,
    ) -> ComplexMatrix:
        indices = np.arange(-cutoff, cutoff + 1)
        p, q = np.meshgrid(indices, indices, indexing="ij")
        flat_p = p.ravel()
        flat_q = q.ravel()
        dp = flat_p[:, None] - flat_p[None, :]
        dq = flat_q[:, None] - flat_q[None, :]
        matrix = np.diag((kx + flat_p) ** 2 + (ky + flat_q) ** 2).astype(complex)
        matrix += (lambda_x / 2.0) * ((np.abs(dp) == 1) & (dq == 0))
        matrix += (lambda_y / 2.0) * ((dp == 0) & (np.abs(dq) == 1))
        matrix += (lambda_xy / 4.0) * ((np.abs(dp) == 1) & (np.abs(dq) == 1))
        return matrix

    def _finite_localization(
        self,
        controls: dict[str, JsonValue],
        kpoints: RealMatrix,
        frames: ComplexFrames,
        fft_size: int,
    ) -> list[tuple[float, tuple[float, float], float]]:
        cutoff = self._integer(controls["plane_wave_cutoff"])
        mesh = self._integer(controls["reciprocal_mesh_size"])
        side = 2 * cutoff + 1
        coordinate = np.arange(fft_size, dtype=float) * mesh / fft_size
        records: list[tuple[float, tuple[float, float], float]] = []
        for orbital in range(3):
            coefficients = np.zeros((fft_size, fft_size), dtype=complex)
            for point, kpoint in enumerate(kpoints):
                ix = int(round(float(kpoint[0]) * mesh)) % mesh
                iy = int(round(float(kpoint[1]) * mesh)) % mesh
                frame = frames[point, :, orbital].reshape(side, side)
                for ip, p in enumerate(range(-cutoff, cutoff + 1)):
                    for iq, q in enumerate(range(-cutoff, cutoff + 1)):
                        coefficients[
                            (p * mesh + ix) % fft_size,
                            (q * mesh + iy) % fft_size,
                        ] += frame[ip, iq] / mesh
            coefficient_norm = float(np.sum(np.abs(coefficients) ** 2))
            wave = np.fft.ifft2(coefficients) * fft_size**2
            probability = np.abs(wave) ** 2
            probability /= np.sum(probability)
            center_x = self._circular_center(
                np.sum(probability, axis=1), coordinate, mesh
            )
            center_y = self._circular_center(
                np.sum(probability, axis=0), coordinate, mesh
            )
            dx = (coordinate - center_x + mesh / 2.0) % mesh - mesh / 2.0
            dy = (coordinate - center_y + mesh / 2.0) % mesh - mesh / 2.0
            spread = float(np.sum(probability * (dx[:, None] ** 2 + dy[None, :] ** 2)))
            records.append(
                (
                    spread,
                    (center_x % 1.0, center_y % 1.0),
                    coefficient_norm,
                )
            )
        return records

    @staticmethod
    def _circular_center(
        marginal: npt.NDArray[np.float64],
        coordinate: npt.NDArray[np.float64],
        period: int,
    ) -> float:
        moment = np.sum(marginal * np.exp(2j * np.pi * coordinate / period))
        return float(np.angle(moment) % (2.0 * np.pi) * period / (2.0 * np.pi))

    def _clusters(
        self,
        starts: list[dict[str, JsonValue]],
        spread_tolerance: float,
        center_tolerance: float,
    ) -> list[list[str]]:
        clusters: list[list[dict[str, JsonValue]]] = []
        for start in sorted(
            starts,
            key=lambda value: (
                self._omega_tilde(value),
                self._string(value["gauge_id"]),
            ),
        ):
            match = next(
                (
                    cluster
                    for cluster in clusters
                    if abs(self._omega_tilde(start) - self._omega_tilde(cluster[0]))
                    <= spread_tolerance
                    and self._center_set_distance(
                        start["native_centers_modulo_cell"],
                        cluster[0]["native_centers_modulo_cell"],
                        d4=True,
                    )
                    <= center_tolerance
                ),
                None,
            )
            if match is None:
                clusters.append([start])
            else:
                match.append(start)
        return [
            sorted(self._string(value["gauge_id"]) for value in cluster)
            for cluster in clusters
        ]

    def _omega_tilde(self, start: dict[str, JsonValue]) -> float:
        return self._real(
            self._mapping(start["spread_components"])["omega_tilde_cell_squared"]
        )

    def _center_set_distance(
        self, first: JsonValue, second: JsonValue, *, d4: bool
    ) -> float:
        left = [self._reals(value) for value in self._array(first)]
        right = [self._reals(value) for value in self._array(second)]
        operations = range(8) if d4 else range(1)
        return min(
            self._ordinary_center_set_distance(self._transform(left, operation), right)
            for operation in operations
        )

    def _transform(
        self, centers: list[tuple[float, ...]], operation: int
    ) -> list[tuple[float, float]]:
        transformed: list[tuple[float, float]] = []
        for x, y in centers:
            values = (
                (x, y),
                (-y, x),
                (-x, -y),
                (y, -x),
                (x, -y),
                (-x, y),
                (y, x),
                (-y, -x),
            )[operation]
            transformed.append((values[0] % 1.0, values[1] % 1.0))
        return transformed

    def _ordinary_center_set_distance(
        self, first: list[tuple[float, ...]], second: list[tuple[float, ...]]
    ) -> float:
        return min(
            max(
                math.sqrt(
                    sum(
                        min(abs(a - b), 1.0 - abs(a - b)) ** 2
                        for a, b in zip(first[index], second[target], strict=True)
                    )
                )
                for index, target in enumerate(permutation)
            )
            for permutation in itertools.permutations(range(len(second)))
        )

    def _hopping_tail(self, path: Path, radius: int) -> float:
        lines = path.read_text(encoding="utf-8").splitlines()
        rank = int(lines[1])
        count = int(lines[2])
        cursor = 3
        degeneracies: list[int] = []
        while len(degeneracies) < count:
            degeneracies.extend(int(value) for value in lines[cursor].split())
            cursor += 1
        blocks: dict[tuple[int, int], ComplexMatrix] = {}
        for line in lines[cursor:]:
            rx, ry, rz, row, column, real, imaginary = line.split()
            if int(rz) != 0:
                raise AssertionError("inactive hopping translation is nonzero")
            matrix = blocks.setdefault(
                (int(rx), int(ry)), np.zeros((rank, rank), dtype=complex)
            )
            matrix[int(row) - 1, int(column) - 1] = complex(
                float(real), float(imaginary)
            )
        return math.sqrt(
            sum(
                float(np.linalg.norm(matrix) ** 2)
                for (rx, ry), matrix in blocks.items()
                if rx * rx + ry * ry > radius
            )
        )

    @staticmethod
    def _component(text: str, pattern: str) -> float:
        match = re.search(pattern, text)
        if match is None:
            raise ValueError(f"missing native component: {pattern}")
        return float(match.group(1))

    def _real_matrix(self, value: JsonValue) -> RealMatrix:
        return np.asarray([self._reals(row) for row in self._array(value)], dtype=float)

    def _complex_tensor(self, value: JsonValue) -> ComplexFrames:
        return np.asarray(
            [
                [
                    [complex(*self._reals(pair)) for pair in self._array(row)]
                    for row in self._array(matrix)
                ]
                for matrix in self._array(value)
            ],
            dtype=complex,
        )

    def _identity(self, path: Path, expected: JsonValue, label: str) -> None:
        digest = self._string(expected)
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != digest:
            raise AssertionError(
                f"{label} identity mismatch: actual={actual}, expected={digest}"
            )

    @staticmethod
    def _close(actual: float, expected: float, tolerance: float, label: str) -> None:
        if abs(actual - expected) > tolerance:
            raise AssertionError(
                f"{label}: actual={actual:.16e}, expected={expected:.16e}"
            )

    def _load(self, path: Path) -> dict[str, JsonValue]:
        return self._mapping(
            cast(JsonValue, json.loads(path.read_text(encoding="utf-8")))
        )

    @staticmethod
    def _mapping(value: JsonValue) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError("expected an object")
        return value

    @staticmethod
    def _array(value: JsonValue) -> list[JsonValue]:
        if not isinstance(value, list):
            raise TypeError("expected an array")
        return value

    @staticmethod
    def _string(value: JsonValue) -> str:
        if not isinstance(value, str):
            raise TypeError("expected a string")
        return value

    @staticmethod
    def _integer(value: JsonValue) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("expected an integer")
        return value

    @staticmethod
    def _real(value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("expected a real number")
        return float(value)

    def _reals(self, value: JsonValue) -> tuple[float, ...]:
        return tuple(self._real(item) for item in self._array(value))


class CommandAdapter:
    """Adapt one result path to the independent verifier."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("result", type=Path)
        arguments = parser.parse_args(argv)
        OfflineReanalysisVerifier().execute(cast(Path, arguments.result).resolve())
        print("periodic_2d_optimizer_basin_reanalysis_verification=PASS")
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
