#!/usr/bin/env python3
"""Run the Appendix E finite harmonic-oscillator comparison."""

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
type RealMatrix = npt.NDArray[np.float64]
type RealVector = npt.NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class ExperimentInput:
    """Represent the closed dimensionless sweep contract."""

    experiment_id: str
    evidence_status: str
    hbar: float
    mass: float
    omega: float
    oscillator_length: float
    box_half_widths: tuple[float, ...]
    grid_spacings: tuple[float, ...]
    retained_dimensions: tuple[int, ...]
    spatial_representation: str
    comparison_map: str

    def __post_init__(self) -> None:
        if not self.experiment_id:
            raise ValueError("experiment_id must be nonempty")
        if self.evidence_status != "illustrative numerical experiment":
            raise ValueError("evidence_status must identify an illustrative experiment")
        scalars = (self.hbar, self.mass, self.omega, self.oscillator_length)
        if not all(np.isfinite(value) and value > 0.0 for value in scalars):
            raise ValueError("dimensionless constants must be positive and finite")
        expected_length = np.sqrt(self.hbar / (self.mass * self.omega))
        if self.oscillator_length != expected_length:
            raise ValueError("oscillator_length must equal sqrt(hbar/(mass*omega))")
        if not self.box_half_widths or not self.grid_spacings:
            raise ValueError("box and grid sweeps must be nonempty")
        if not self.retained_dimensions:
            raise ValueError("retained_dimensions must be nonempty")
        if tuple(sorted(set(self.box_half_widths))) != self.box_half_widths:
            raise ValueError("box_half_widths must be strictly increasing")
        if tuple(sorted(set(self.grid_spacings), reverse=True)) != self.grid_spacings:
            raise ValueError("grid_spacings must be strictly decreasing")
        if tuple(sorted(set(self.retained_dimensions))) != self.retained_dimensions:
            raise ValueError("retained_dimensions must be strictly increasing")
        if not all(
            value > 0.0 and np.isfinite(value) for value in self.box_half_widths
        ):
            raise ValueError("box_half_widths must be positive and finite")
        if not all(value > 0.0 and np.isfinite(value) for value in self.grid_spacings):
            raise ValueError("grid_spacings must be positive and finite")
        if not all(value > 0 for value in self.retained_dimensions):
            raise ValueError("retained_dimensions must be positive")


@dataclass(frozen=True, slots=True)
class ComparisonResult:
    """Represent one aligned finite-box and ladder-space comparison."""

    box_half_width: float
    grid_spacing: float
    interior_points: int
    retained_dimension: int
    grid_coordinates: RealVector
    injection: RealMatrix
    gram_matrix: RealMatrix
    gram_inverse_square_root: RealMatrix
    pulled_back_hamiltonian: RealMatrix
    reference_hamiltonian: RealMatrix
    difference: RealMatrix
    gram_deviation: float
    gram_condition_number: float
    injection_isometry_error: float
    absolute_discrepancy: float
    relative_discrepancy: float
    diagonal_discrepancy: float
    off_diagonal_discrepancy: float


class ExperimentInputDeserializer:
    """Deserialize the closed version-1 experiment input."""

    __slots__ = ()

    def execute(self, payload: bytes) -> ExperimentInput:
        value = cast(JsonValue, json.loads(payload.decode("utf-8")))
        root = self._mapping(value, "input")
        expected = {
            "schema_version",
            "experiment_id",
            "evidence_status",
            "dimensionless_convention",
            "box_half_widths",
            "grid_spacings",
            "retained_dimensions",
            "spatial_representation",
            "comparison_map",
        }
        if set(root) != expected:
            raise ValueError("experiment input fields do not match schema version 1")
        if self._integer(root["schema_version"], "schema_version") != 1:
            raise ValueError("unsupported experiment input schema version")
        constants = self._mapping(
            root["dimensionless_convention"], "dimensionless_convention"
        )
        if set(constants) != {"hbar", "mass", "omega", "oscillator_length"}:
            raise ValueError("dimensionless_convention fields are not closed")
        return ExperimentInput(
            experiment_id=self._string(root["experiment_id"], "experiment_id"),
            evidence_status=self._string(root["evidence_status"], "evidence_status"),
            hbar=self._real(constants["hbar"], "hbar"),
            mass=self._real(constants["mass"], "mass"),
            omega=self._real(constants["omega"], "omega"),
            oscillator_length=self._real(
                constants["oscillator_length"], "oscillator_length"
            ),
            box_half_widths=self._real_sequence(
                root["box_half_widths"], "box_half_widths"
            ),
            grid_spacings=self._real_sequence(root["grid_spacings"], "grid_spacings"),
            retained_dimensions=self._integer_sequence(
                root["retained_dimensions"], "retained_dimensions"
            ),
            spatial_representation=self._string(
                root["spatial_representation"], "spatial_representation"
            ),
            comparison_map=self._string(root["comparison_map"], "comparison_map"),
        )

    @staticmethod
    def _mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        if not isinstance(value, dict) or not all(
            isinstance(key, str) for key in value
        ):
            raise TypeError(f"{name} must be a JSON object")
        return value

    @staticmethod
    def _string(value: JsonValue, name: str) -> str:
        if not isinstance(value, str) or not value:
            raise TypeError(f"{name} must be a nonempty string")
        return value

    @staticmethod
    def _real(value: JsonValue, name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be a JSON number")
        result = float(value)
        if not np.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result

    @staticmethod
    def _integer(value: JsonValue, name: str) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be a JSON integer")
        return value

    def _real_sequence(self, value: JsonValue, name: str) -> tuple[float, ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return tuple(self._real(item, name) for item in value)

    def _integer_sequence(self, value: JsonValue, name: str) -> tuple[int, ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return tuple(self._integer(item, name) for item in value)


class HarmonicOscillatorComparator:
    """Compare one finite Dirichlet representation in retained ladder coordinates."""

    __slots__ = ()

    def execute(
        self,
        experiment: ExperimentInput,
        box_half_width: float,
        requested_spacing: float,
        retained_dimension: int,
    ) -> ComparisonResult:
        intervals_float = 2.0 * box_half_width / requested_spacing
        intervals = int(round(intervals_float))
        if not np.isclose(intervals_float, intervals, rtol=0.0, atol=1.0e-12):
            raise ValueError("each requested spacing must divide the box width")
        interior_points = intervals - 1
        if retained_dimension > interior_points:
            raise ValueError("retained dimension exceeds the spatial dimension")
        spacing = 2.0 * box_half_width / (interior_points + 1)
        coordinates = -box_half_width + spacing * np.arange(
            1, interior_points + 1, dtype=np.float64
        )
        sampled_states = np.sqrt(spacing) * self._oscillator_states(
            coordinates / experiment.oscillator_length,
            retained_dimension,
            experiment.oscillator_length,
        )
        gram = sampled_states.T @ sampled_states
        gram_eigenvalues, gram_eigenvectors = np.linalg.eigh(gram)
        if gram_eigenvalues[0] <= 0.0:
            raise ValueError("sampled-state Gram matrix is not positive definite")
        gram_inverse_square_root = (
            gram_eigenvectors
            @ np.diag(np.power(gram_eigenvalues, -0.5))
            @ gram_eigenvectors.T
        )
        injection = sampled_states @ gram_inverse_square_root
        hamiltonian = self._finite_box_hamiltonian(
            coordinates,
            spacing,
            experiment.hbar,
            experiment.mass,
            experiment.omega,
        )
        pulled_back = injection.T @ hamiltonian @ injection
        reference = np.diag(
            experiment.hbar
            * experiment.omega
            * (np.arange(retained_dimension, dtype=np.float64) + 0.5)
        )
        difference = pulled_back - reference
        diagonal = np.diag(np.diag(difference))
        off_diagonal = difference - diagonal
        absolute = float(np.linalg.norm(difference, ord="fro"))
        reference_scale = float(np.linalg.norm(reference, ord="fro"))
        return ComparisonResult(
            box_half_width=box_half_width,
            grid_spacing=spacing,
            interior_points=interior_points,
            retained_dimension=retained_dimension,
            grid_coordinates=coordinates,
            injection=injection,
            gram_matrix=gram,
            gram_inverse_square_root=gram_inverse_square_root,
            pulled_back_hamiltonian=pulled_back,
            reference_hamiltonian=reference,
            difference=difference,
            gram_deviation=float(np.linalg.norm(gram - np.eye(retained_dimension))),
            gram_condition_number=float(gram_eigenvalues[-1] / gram_eigenvalues[0]),
            injection_isometry_error=float(
                np.linalg.norm(injection.T @ injection - np.eye(retained_dimension))
            ),
            absolute_discrepancy=absolute,
            relative_discrepancy=absolute / reference_scale,
            diagonal_discrepancy=float(np.linalg.norm(diagonal, ord="fro")),
            off_diagonal_discrepancy=float(np.linalg.norm(off_diagonal, ord="fro")),
        )

    @staticmethod
    def _oscillator_states(
        dimensionless_coordinates: RealVector,
        retained_dimension: int,
        oscillator_length: float,
    ) -> RealMatrix:
        states = np.empty(
            (dimensionless_coordinates.size, retained_dimension), dtype=np.float64
        )
        states[:, 0] = (
            np.pi ** (-0.25)
            * np.exp(-0.5 * np.square(dimensionless_coordinates))
            / np.sqrt(oscillator_length)
        )
        if retained_dimension > 1:
            states[:, 1] = np.sqrt(2.0) * dimensionless_coordinates * states[:, 0]
        for degree in range(1, retained_dimension - 1):
            states[:, degree + 1] = (
                np.sqrt(2.0 / (degree + 1.0))
                * dimensionless_coordinates
                * states[:, degree]
                - np.sqrt(degree / (degree + 1.0)) * states[:, degree - 1]
            )
        return states

    @staticmethod
    def _finite_box_hamiltonian(
        coordinates: RealVector,
        spacing: float,
        hbar: float,
        mass: float,
        omega: float,
    ) -> RealMatrix:
        points = coordinates.size
        kinetic_prefactor = hbar * hbar / (2.0 * mass * spacing * spacing)
        diagonal = 2.0 * kinetic_prefactor + 0.5 * mass * omega * omega * np.square(
            coordinates
        )
        hamiltonian = np.diag(diagonal)
        if points > 1:
            off_diagonal = np.full(points - 1, -kinetic_prefactor)
            hamiltonian += np.diag(off_diagonal, 1)
            hamiltonian += np.diag(off_diagonal, -1)
        return hamiltonian


class ExperimentResultSerializer:
    """Serialize the sweep and every comparison map to canonical JSON text."""

    __slots__ = ()

    def execute(
        self,
        experiment: ExperimentInput,
        results: tuple[ComparisonResult, ...],
        input_path: Path,
        script_path: Path,
    ) -> bytes:
        repository_root = script_path.parents[3]
        cases = cast(list[JsonValue], [self._case(result) for result in results])
        cross_grid = self._cross_grid(results)
        payload: dict[str, JsonValue] = {
            "schema_version": 1,
            "experiment_id": experiment.experiment_id,
            "evidence_status": experiment.evidence_status,
            "calculation_status": "calculated illustrative result",
            "dimensionless_convention": {
                "hbar": experiment.hbar,
                "mass": experiment.mass,
                "omega": experiment.omega,
                "oscillator_length": experiment.oscillator_length,
                "energy_unit": "hbar*omega",
                "length_unit": "oscillator_length",
            },
            "state_spaces": {
                "spatial": "interior coordinates of the finite Dirichlet grid",
                "comparison": "ordered real-line number states |0>,...,|K-1>",
                "map_direction": "comparison coordinates to spatial coordinates",
                "basis_ordering": (
                    "increasing grid coordinate and increasing number state"
                ),
            },
            "spatial_representation": experiment.spatial_representation,
            "comparison_map": experiment.comparison_map,
            "cases": cases,
            "cross_grid_comparisons": cross_grid,
            "provenance": {
                "input_path": input_path.relative_to(repository_root).as_posix(),
                "input_sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
                "script_path": script_path.relative_to(repository_root).as_posix(),
                "script_sha256": hashlib.sha256(script_path.read_bytes()).hexdigest(),
                "python_version": platform.python_version(),
                "numpy_version": np.__version__,
                "floating_point": "IEEE-754 binary64 through numpy.float64",
                "linear_algebra": "numpy.linalg.eigh and numpy.linalg.norm",
            },
            "limitations": [
                "The finite grid matrix is not the continuum differential operator.",
                (
                    "The discrepancy combines finite-box boundary and spatial-"
                    "discretization effects unless one control is held fixed."
                ),
                (
                    "The retained dimension changes the comparison space and is not "
                    "an error bar."
                ),
                (
                    "The result is illustrative numerical verification, not "
                    "semiconductor evidence or scientific validation."
                ),
            ],
        }
        return (
            json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
        ).encode("utf-8")

    @staticmethod
    def _matrix(value: RealMatrix) -> list[JsonValue]:
        return cast(list[JsonValue], value.tolist())

    @staticmethod
    def _array_sha256(value: RealMatrix) -> str:
        canonical = np.asarray(value, dtype="<f8", order="C")
        return hashlib.sha256(canonical.tobytes(order="C")).hexdigest()

    def _case(self, result: ComparisonResult) -> dict[str, JsonValue]:
        return {
            "case_id": (
                f"b={result.box_half_width:g};eta={result.grid_spacing:g};"
                f"K={result.retained_dimension}"
            ),
            "box_half_width": result.box_half_width,
            "grid_spacing": result.grid_spacing,
            "interior_points": result.interior_points,
            "retained_dimension": result.retained_dimension,
            "comparison_map": {
                "definition": (
                    "quadrature-scaled analytic number states followed by "
                    "symmetric Gram orthonormalization"
                ),
                "injection_shape": cast(
                    list[JsonValue],
                    [result.interior_points, result.retained_dimension],
                ),
                "injection_content_sha256": self._array_sha256(result.injection),
                "injection_content_encoding": (
                    "IEEE-754 binary64 little-endian row-major"
                ),
                "gram_matrix": self._matrix(result.gram_matrix),
                "gram_inverse_square_root": self._matrix(
                    result.gram_inverse_square_root
                ),
                "map_direction": "number-state coordinates to grid coordinates",
            },
            "operators_in_common_coordinates": {
                "pulled_back_finite_box": self._matrix(result.pulled_back_hamiltonian),
                "exact_retained_ladder": self._matrix(result.reference_hamiltonian),
                "finite_box_minus_ladder": self._matrix(result.difference),
            },
            "diagnostics": {
                "gram_deviation_frobenius": result.gram_deviation,
                "gram_condition_number_2": result.gram_condition_number,
                "injection_isometry_error_frobenius": (result.injection_isometry_error),
                "absolute_discrepancy_frobenius": result.absolute_discrepancy,
                "relative_discrepancy_frobenius": result.relative_discrepancy,
                "diagonal_discrepancy_frobenius": (result.diagonal_discrepancy),
                "off_diagonal_discrepancy_frobenius": (result.off_diagonal_discrepancy),
            },
        }

    def _cross_grid(self, results: tuple[ComparisonResult, ...]) -> list[JsonValue]:
        records: list[JsonValue] = []
        groups: dict[tuple[float, int], list[ComparisonResult]] = {}
        for result in results:
            groups.setdefault(
                (result.box_half_width, result.retained_dimension), []
            ).append(result)
        for (box_half_width, retained_dimension), cases in sorted(groups.items()):
            ordered = sorted(cases, key=lambda item: item.grid_spacing, reverse=True)
            for coarse, fine in zip(ordered, ordered[1:], strict=False):
                difference = (
                    coarse.pulled_back_hamiltonian - fine.pulled_back_hamiltonian
                )
                records.append(
                    {
                        "box_half_width": box_half_width,
                        "retained_dimension": retained_dimension,
                        "coarse_grid_spacing": coarse.grid_spacing,
                        "fine_grid_spacing": fine.grid_spacing,
                        "coarse_interior_points": coarse.interior_points,
                        "fine_interior_points": fine.interior_points,
                        "coarse_minus_fine_frobenius": float(
                            np.linalg.norm(difference, ord="fro")
                        ),
                    }
                )
        return records


class HarmonicOscillatorExperiment:
    """Execute the declared parameter sweep without hidden state."""

    __slots__ = ("_comparator", "_serializer")

    def __init__(self) -> None:
        self._comparator = HarmonicOscillatorComparator()
        self._serializer = ExperimentResultSerializer()

    def execute(
        self, experiment: ExperimentInput, input_path: Path, script_path: Path
    ) -> bytes:
        results = tuple(
            self._comparator.execute(experiment, box, spacing, retained)
            for box in experiment.box_half_widths
            for spacing in experiment.grid_spacings
            for retained in experiment.retained_dimensions
        )
        return self._serializer.execute(experiment, results, input_path, script_path)


class CommandAdapter:
    """Adapt command-line paths to the owned experiment objects."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("--input", type=Path, required=True)
        parser.add_argument("--output", type=Path, required=True)
        args = parser.parse_args(argv)
        input_path = cast(Path, args.input).resolve()
        output_path = cast(Path, args.output).resolve()
        script_path = Path(__file__).resolve()
        experiment = ExperimentInputDeserializer().execute(input_path.read_bytes())
        payload = HarmonicOscillatorExperiment().execute(
            experiment, input_path, script_path
        )
        output_path.write_bytes(payload)
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
