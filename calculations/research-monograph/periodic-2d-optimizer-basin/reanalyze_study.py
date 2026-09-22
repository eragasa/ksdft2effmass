#!/usr/bin/env python3
"""Reanalyze retained runs with spread components, symmetry, and grid refinement."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

import numpy as np

BASE_DIRECTORY = Path(__file__).resolve().parents[1] / "periodic-2d"
if str(BASE_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(BASE_DIRECTORY))

from extract_wannier90 import CorrectedWannier90Extractor, JsonValue  # noqa: E402


class NativeSpreadTraceAnalyzer:
    """Extract final spread components and descriptive terminal trace metrics."""

    __slots__ = ()

    _trace_pattern = re.compile(
        r"^\s*(\d+)\s+([-+0-9.Ee]+)\s+([-+0-9.Ee]+)\s+"
        r"([-+0-9.Ee]+)\s+([-+0-9.Ee]+)\s+<-- CONV$",
        re.MULTILINE,
    )

    def execute(self, wout_path: Path, converged: bool) -> dict[str, JsonValue]:
        text = wout_path.read_text(encoding="utf-8")
        final = text.rsplit("Final State", maxsplit=1)[1]
        components = {
            name: self._component(final, pattern)
            for name, pattern in (
                ("omega_i_cell_squared", r"Omega I\s+=\s+([^\s]+)"),
                ("omega_d_cell_squared", r"Omega D\s+=\s+([^\s]+)"),
                ("omega_od_cell_squared", r"Omega OD\s+=\s+([^\s]+)"),
                ("omega_total_cell_squared", r"Omega Total\s+=\s+([^\s]+)"),
            )
        }
        components["omega_tilde_cell_squared"] = self._real(
            components["omega_d_cell_squared"]
        ) + self._real(components["omega_od_cell_squared"])
        trace = [
            (
                int(match.group(1)),
                float(match.group(2)),
                float(match.group(3)),
                float(match.group(4)),
            )
            for match in self._trace_pattern.finditer(text)
        ]
        if not trace:
            raise ValueError(f"iteration trace is absent from {wout_path}")
        tail = trace[-min(200, len(trace)) :]
        iterations = np.asarray([value[0] for value in tail], dtype=float)
        deltas = np.asarray([value[1] for value in tail], dtype=float)
        gradients = np.asarray([value[2] for value in tail], dtype=float)
        spreads = np.asarray([value[3] for value in tail], dtype=float)
        slope = float(np.polyfit(iterations, spreads, deg=1)[0])
        trend = slope * (iterations - np.mean(iterations)) + np.mean(spreads)
        detrended_rms = float(np.sqrt(np.mean((spreads - trend) ** 2)))
        median_delta = float(np.median(np.abs(deltas)))
        median_gradient = float(np.median(gradients))
        if converged:
            classification = "native_converged"
        elif median_delta <= 1.0e-8 and median_gradient <= 1.0e-3:
            classification = "near_stationary_without_window_convergence"
        elif slope < -1.0e-8:
            classification = "continuing_descent_at_iteration_limit"
        elif detrended_rms > 1.0e-5:
            classification = "oscillatory_or_stalled"
        else:
            classification = "stalled_or_nondescent"
        return {
            **components,
            "trace_point_count": len(trace),
            "terminal_window_point_count": len(tail),
            "terminal_spread_slope_per_iteration": slope,
            "terminal_detrended_spread_rms": detrended_rms,
            "terminal_median_absolute_delta_spread": median_delta,
            "terminal_median_rms_gradient": median_gradient,
            "terminal_minimum_spread_cell_squared": float(np.min(spreads)),
            "terminal_maximum_spread_cell_squared": float(np.max(spreads)),
            "diagnostic_classification": classification,
            "classification_status": "exploratory descriptive diagnostic",
        }

    @staticmethod
    def _component(text: str, pattern: str) -> float:
        match = re.search(pattern, text)
        if match is None:
            raise ValueError(f"final spread component is absent: {pattern}")
        return float(match.group(1))

    @staticmethod
    def _real(value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("expected a real number")
        return float(value)


class SquareSymmetryBasinClassifier:
    """Classify converged endpoints after periodic, permutation, and D4 matching."""

    __slots__ = ()

    def execute(
        self,
        starts: list[dict[str, JsonValue]],
        spread_tolerance: float,
        center_tolerance: float,
    ) -> list[JsonValue]:
        basins: list[dict[str, JsonValue]] = []
        ordered = sorted(
            starts,
            key=lambda value: (
                self._real(
                    self._mapping(value["spread_components"])[
                        "omega_tilde_cell_squared"
                    ]
                ),
                self._string(value["gauge_id"]),
            ),
        )
        for start in ordered:
            match: dict[str, JsonValue] | None = None
            for basin in basins:
                spread_difference = abs(
                    self._omega_tilde(start)
                    - self._real(basin["representative_omega_tilde_cell_squared"])
                )
                center_distance = self._d4_center_set_distance(
                    start["native_centers_modulo_cell"],
                    basin["representative_native_centers_modulo_cell"],
                )
                if (
                    spread_difference <= spread_tolerance
                    and center_distance <= center_tolerance
                ):
                    match = basin
                    break
            if match is None:
                match = {
                    "basin_id": f"symmetry_basin_{len(basins) + 1:02d}",
                    "representative_gauge_id": start["gauge_id"],
                    "representative_omega_tilde_cell_squared": self._omega_tilde(start),
                    "representative_native_centers_modulo_cell": start[
                        "native_centers_modulo_cell"
                    ],
                    "gauge_ids": [],
                    "occupancy": 0,
                }
                basins.append(match)
            self._array(match["gauge_ids"]).append(start["gauge_id"])
            match["occupancy"] = self._integer(match["occupancy"]) + 1
        return cast(list[JsonValue], basins)

    def _d4_center_set_distance(self, first: JsonValue, second: JsonValue) -> float:
        left = [self._reals(value) for value in self._array(first)]
        right = [self._reals(value) for value in self._array(second)]
        return min(
            self._center_set_distance(self._transform(left, operation), right)
            for operation in range(8)
        )

    def _transform(
        self, centers: list[tuple[float, ...]], operation: int
    ) -> list[tuple[float, float]]:
        result: list[tuple[float, float]] = []
        for center in centers:
            x, y = center
            candidates = (
                (x, y),
                (-y, x),
                (-x, -y),
                (y, -x),
                (x, -y),
                (-x, y),
                (y, x),
                (-y, -x),
            )
            transformed = candidates[operation]
            result.append((transformed[0] % 1.0, transformed[1] % 1.0))
        return result

    def _center_set_distance(
        self, first: list[tuple[float, ...]], second: list[tuple[float, ...]]
    ) -> float:
        return min(
            max(
                self._periodic_distance(first[index], second[target])
                for index, target in enumerate(permutation)
            )
            for permutation in itertools.permutations(range(len(second)))
        )

    @staticmethod
    def _periodic_distance(
        first: tuple[float, ...], second: tuple[float, ...]
    ) -> float:
        differences = [
            min(abs(left - right), 1.0 - abs(left - right))
            for left, right in zip(first, second, strict=True)
        ]
        return math.sqrt(sum(value * value for value in differences))

    def _omega_tilde(self, start: dict[str, JsonValue]) -> float:
        return self._real(
            self._mapping(start["spread_components"])["omega_tilde_cell_squared"]
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


class CommonEstimatorRefinement:
    """Recompute selected common estimators at three declared FFT sizes."""

    __slots__ = ()

    def execute(
        self,
        cases: list[tuple[str, dict[str, JsonValue]]],
        base_extractor_path: Path,
        input_directory: Path,
    ) -> list[JsonValue]:
        input_directory.mkdir(exist_ok=True)
        extractor = CorrectedWannier90Extractor()
        records: list[JsonValue] = []
        for case_id, start in cases:
            source_path = Path(self._string(start["source_analysis_result_path"]))
            source = self._load(source_path)
            portable = self._mapping(source["portable_evidence"])
            controls = self._mapping(
                cast(
                    JsonValue,
                    json.loads(self._string(portable["input_payload_utf8"])),
                )
            )
            run_root = Path(
                self._string(self._mapping(source["provenance"])["external_run_root"])
            )
            sizes: list[JsonValue] = []
            for fft_size in (256, 512, 1024):
                controls["localization_fft_size"] = fft_size
                input_path = input_directory / f"{case_id}-fft{fft_size}.json"
                input_path.write_text(
                    json.dumps(controls, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8",
                )
                extracted = extractor.execute(
                    input_path,
                    run_root,
                    base_extractor_path,
                )
                localization = self._mapping(extracted["localization"])
                common = [
                    self._mapping(value)
                    for value in self._array(
                        localization["common_finite_supercell_estimator"]
                    )
                ]
                sizes.append(
                    {
                        "fft_size": fft_size,
                        "input_path": input_path.as_posix(),
                        "input_sha256": self._sha256(input_path),
                        "common_total_spread_cell_squared": sum(
                            self._real(value["spread_cell_squared"]) for value in common
                        ),
                        "common_centers_modulo_cell": [
                            value["center_modulo_cell"] for value in common
                        ],
                        "minimum_coefficient_norm": min(
                            self._real(value["coefficient_norm"]) for value in common
                        ),
                    }
                )
            records.append(
                {
                    "case_id": case_id,
                    "configuration_id": start["configuration_id"],
                    "gauge_id": start["gauge_id"],
                    "convergence_criterion_satisfied": start[
                        "convergence_criterion_satisfied"
                    ],
                    "source_analysis_result_path": str(source_path),
                    "source_analysis_result_sha256": self._sha256(source_path),
                    "sizes": sizes,
                    "refinement_512_to_1024": self._difference(sizes[1], sizes[2]),
                }
            )
        return records

    def _difference(self, first: JsonValue, second: JsonValue) -> dict[str, JsonValue]:
        lower = self._mapping(first)
        upper = self._mapping(second)
        lower_spread = self._real(lower["common_total_spread_cell_squared"])
        upper_spread = self._real(upper["common_total_spread_cell_squared"])
        return {
            "relative_total_spread_difference": abs(lower_spread - upper_spread)
            / max(abs(upper_spread), 1.0e-15),
            "center_set_periodic_distance": self._center_set_distance(
                lower["common_centers_modulo_cell"],
                upper["common_centers_modulo_cell"],
            ),
        }

    def _center_set_distance(self, first: JsonValue, second: JsonValue) -> float:
        left = [self._reals(value) for value in self._array(first)]
        right = [self._reals(value) for value in self._array(second)]
        return min(
            max(
                math.sqrt(
                    sum(
                        min(abs(a - b), 1.0 - abs(a - b)) ** 2
                        for a, b in zip(left[index], right[target], strict=True)
                    )
                )
                for index, target in enumerate(permutation)
            )
            for permutation in itertools.permutations(range(len(right)))
        )

    @staticmethod
    def _sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

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
    def _real(value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("expected a real number")
        return float(value)

    def _reals(self, value: JsonValue) -> tuple[float, ...]:
        return tuple(self._real(item) for item in self._array(value))


class OptimizerBasinReanalysis:
    """Coordinate non-destructive reanalysis of the retained study evidence."""

    __slots__ = ()

    def execute(
        self,
        result_path: Path,
        base_extractor_path: Path,
        output_path: Path,
    ) -> dict[str, JsonValue]:
        source = self._load(result_path)
        configurations = [
            self._mapping(value) for value in self._array(source["configurations"])
        ]
        trace_analyzer = NativeSpreadTraceAnalyzer()
        classifier = SquareSymmetryBasinClassifier()
        configuration_records: list[JsonValue] = []
        start_lookup: dict[tuple[str, str], dict[str, JsonValue]] = {}
        for configuration in configurations:
            starts: list[JsonValue] = []
            for start_value in self._array(configuration["starts"]):
                start = dict(self._mapping(start_value))
                analysis = self._load(Path(self._string(start["analysis_result_path"])))
                run_root = Path(
                    self._string(
                        self._mapping(analysis["provenance"])["external_run_root"]
                    )
                )
                wout_path = run_root / "low_triple" / "low_triple.wout"
                spread = trace_analyzer.execute(
                    wout_path,
                    converged=start["convergence_criterion_satisfied"] is True,
                )
                represented = self._mapping(analysis["represented_comparison"])
                radius_18 = next(
                    self._real(self._mapping(value)["omitted_block_frobenius_l2_norm"])
                    for value in self._array(represented["shell_study"])
                    if self._integer(self._mapping(value)["maximum_squared_radius"])
                    == 18
                )
                record: dict[str, JsonValue] = {
                    "configuration_id": configuration["configuration_id"],
                    "gauge_id": start["gauge_id"],
                    "convergence_criterion_satisfied": start[
                        "convergence_criterion_satisfied"
                    ],
                    "native_centers_modulo_cell": start["native_centers_modulo_cell"],
                    "spread_components": spread,
                    "radius_18_hopping_tail_energy_units": radius_18,
                    "source_analysis_result_path": start["analysis_result_path"],
                    "source_analysis_result_sha256": start["analysis_result_sha256"],
                }
                starts.append(record)
                start_lookup[
                    (
                        self._string(configuration["configuration_id"]),
                        self._string(start["gauge_id"]),
                    )
                ] = record
            converged = [
                self._mapping(value)
                for value in starts
                if self._mapping(value)["convergence_criterion_satisfied"] is True
            ]
            basins = classifier.execute(converged, 1.0e-8, 1.0e-5)
            best = min(
                converged,
                key=lambda value: (
                    self._real(
                        self._mapping(value["spread_components"])[
                            "omega_tilde_cell_squared"
                        ]
                    ),
                    self._string(value["gauge_id"]),
                ),
            )
            configuration_records.append(
                {
                    "configuration_id": configuration["configuration_id"],
                    "plane_wave_cutoff": configuration["plane_wave_cutoff"],
                    "reciprocal_mesh_size": configuration["reciprocal_mesh_size"],
                    "transverse_lattice_length": configuration[
                        "transverse_lattice_length"
                    ],
                    "starts": starts,
                    "symmetry_aware_observed_basin_count": len(basins),
                    "symmetry_aware_observed_basins": basins,
                    "best_observed_converged_by_omega_tilde": best,
                }
            )
        refinement_cases = [
            (
                "mesh_n19_best_converged",
                start_lookup[("mesh_n19_p4_c19", "y02_soft")],
            ),
            (
                "mesh_n23_best_converged",
                start_lookup[("mesh_n23_p4_c23", "rough_smooth")],
            ),
            (
                "cutoff_p5_best_converged",
                start_lookup[("cutoff_p5_n19_c19", "rough_smooth")],
            ),
            (
                "mesh_n19_nonconverged_strong",
                start_lookup[("mesh_n19_p4_c19", "strong_mixed")],
            ),
        ]
        estimator_records = CommonEstimatorRefinement().execute(
            refinement_cases,
            base_extractor_path,
            output_path.parent / "estimator-inputs",
        )
        diagnostic_counts: dict[str, int] = {}
        for configuration_value in configuration_records:
            for start_value in self._array(
                self._mapping(configuration_value)["starts"]
            ):
                classification = self._string(
                    self._mapping(self._mapping(start_value)["spread_components"])[
                        "diagnostic_classification"
                    ]
                )
                diagnostic_counts[classification] = (
                    diagnostic_counts.get(classification, 0) + 1
                )
        payload: dict[str, JsonValue] = {
            "schema_version": 1,
            "experiment_id": "periodic-2d-optimizer-basin-reanalysis-v1",
            "evidence_status": "calculated offline synthetic numerical reanalysis",
            "generated_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat(),
            "authority": "current human instruction: recommendation authorized",
            "provenance": {
                "source_result_path": result_path.relative_to(
                    output_path.parents[3]
                ).as_posix(),
                "source_result_sha256": self._sha256(result_path),
                "reanalyzer_path": Path(__file__)
                .relative_to(output_path.parents[3])
                .as_posix(),
                "reanalyzer_sha256": self._sha256(Path(__file__).resolve()),
                "base_extractor_path": base_extractor_path.relative_to(
                    output_path.parents[3]
                ).as_posix(),
                "base_extractor_sha256": self._sha256(base_extractor_path),
            },
            "method": {
                "spread_components": (
                    "native final Omega_I, Omega_D, Omega_OD, and "
                    "Omega_tilde=Omega_D+Omega_OD"
                ),
                "trace_terminal_window": 200,
                "trace_classification": (
                    "exploratory descriptive; not a predeclared acceptance gate"
                ),
                "basin_spread_metric": "Omega_tilde",
                "basin_spread_absolute_tolerance": 1.0e-8,
                "basin_center_set_periodic_tolerance": 1.0e-5,
                "basin_symmetry_quotient": (
                    "orbital permutation, periodic wrapping, and eight D4 operations"
                ),
                "hopping_tail_common_maximum_squared_radius": 18,
                "common_estimator_fft_sizes": [256, 512, 1024],
            },
            "diagnostic_classification_counts": {
                key: diagnostic_counts[key] for key in sorted(diagnostic_counts)
            },
            "configurations": configuration_records,
            "common_estimator_refinement": estimator_records,
            "claim_boundary": (
                "This offline reanalysis refines numerical diagnosis of retained "
                "synthetic runs. Post-hoc trace classes and symmetry-aware observed "
                "basins are descriptive and do not prove optimizer completeness, a "
                "global minimum, material validity, or uncertainty quantification."
            ),
        }
        output_path.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        return payload

    @staticmethod
    def _sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

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


class CommandAdapter:
    """Adapt CLI paths to the offline reanalysis action."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("--result", type=Path, required=True)
        parser.add_argument("--base-extractor", type=Path, required=True)
        parser.add_argument("--output", type=Path, required=True)
        arguments = parser.parse_args(argv)
        result = OptimizerBasinReanalysis().execute(
            cast(Path, arguments.result).resolve(),
            cast(Path, arguments.base_extractor).resolve(),
            cast(Path, arguments.output).resolve(),
        )
        print(
            json.dumps(
                {
                    "diagnostic_classification_counts": result[
                        "diagnostic_classification_counts"
                    ],
                    "refined_case_count": len(
                        result["common_estimator_refinement"]
                        if isinstance(result["common_estimator_refinement"], list)
                        else []
                    ),
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
