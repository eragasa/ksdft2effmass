"""Version-one serialization for the harmonic-oscillator study."""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path
from typing import cast

import numpy as np

from ksdft2effmass.analysis.model_systems.harmonic_oscillator import (
    HarmonicOscillatorComparisonResult,
)

from .records import HarmonicOscillatorStudyResult

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


class HarmonicOscillatorStudyResultSerializer:
    """Serialize the Appendix E study result to canonical version-one JSON.

    This repository-bound serializer retains source paths and SHA-256 identities for
    the explicit input, thin CLI adapter, and current package implementation. It does
    not mutate those files or write the returned bytes.
    """

    __slots__ = ()

    def execute(
        self,
        result: HarmonicOscillatorStudyResult,
        input_path: Path,
        script_path: Path,
        repository_root: Path,
    ) -> bytes:
        """Return canonical UTF-8 JSON bytes for one study result.

        Parameters
        ----------
        result
            Complete evaluated study result.
        input_path
            Existing source input beneath ``repository_root``.
        script_path
            Existing thin runner source beneath ``repository_root``.
        repository_root
            Repository root used to produce portable relative provenance paths.

        Returns
        -------
        bytes
            Sorted, indented, newline-terminated UTF-8 JSON.

        Raises
        ------
        TypeError
            If an argument has the wrong semantic type.
        ValueError
            If a source path is not a file beneath ``repository_root``.
        """
        if not isinstance(result, HarmonicOscillatorStudyResult):
            raise TypeError("result must be HarmonicOscillatorStudyResult")
        root = self.resolved_directory(repository_root, "repository_root")
        input_source = self.contained_file(input_path, root, "input_path")
        script_source = self.contained_file(script_path, root, "script_path")
        implementation_paths = tuple(
            self.contained_file(path, root, "implementation path")
            for path in self.implementation_paths()
        )
        definition = result.definition
        cases = cast(list[JsonValue], [self.case(item) for item in result.comparisons])
        payload: dict[str, JsonValue] = {
            "schema_version": 1,
            "experiment_id": definition.study_id,
            "evidence_status": definition.evidence_status,
            "calculation_status": "calculated illustrative result",
            "dimensionless_convention": {
                "hbar": definition.parameters.hbar.magnitude,
                "mass": definition.parameters.mass.magnitude,
                "omega": definition.parameters.omega.magnitude,
                "oscillator_length": definition.parameters.oscillator_length.magnitude,
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
            "spatial_representation": definition.spatial_representation,
            "comparison_map": definition.comparison_map,
            "cases": cases,
            "cross_grid_comparisons": self.cross_grid(result.comparisons),
            "provenance": {
                "input_path": input_source.relative_to(root).as_posix(),
                "input_sha256": self.sha256(input_source),
                "script_path": script_source.relative_to(root).as_posix(),
                "script_sha256": self.sha256(script_source),
                "implementation_identities": [
                    {
                        "path": path.relative_to(root).as_posix(),
                        "sha256": self.sha256(path),
                    }
                    for path in implementation_paths
                ],
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
    def resolved_directory(path: Path, name: str) -> Path:
        """Require and resolve one existing directory path."""
        if not isinstance(path, Path):
            raise TypeError(f"{name} must be pathlib.Path")
        resolved = path.resolve()
        if not resolved.is_dir():
            raise ValueError(f"{name} must be an existing directory")
        return resolved

    @staticmethod
    def contained_file(path: Path, root: Path, name: str) -> Path:
        """Require and resolve one existing file beneath an explicit root."""
        if not isinstance(path, Path):
            raise TypeError(f"{name} must be pathlib.Path")
        resolved = path.resolve()
        if not resolved.is_file():
            raise ValueError(f"{name} must be an existing file")
        try:
            resolved.relative_to(root)
        except ValueError as error:
            raise ValueError(f"{name} must be beneath repository_root") from error
        return resolved

    @staticmethod
    def implementation_paths() -> tuple[Path, ...]:
        """Return the exact current source files implementing authored results."""
        package_root = Path(__file__).resolve().parents[3]
        analysis_root = (
            package_root / "analysis" / "model_systems" / "harmonic_oscillator"
        )
        operator_root = package_root / "operators"
        return (
            analysis_root.parent / "intervals.py",
            analysis_root / "model.py",
            analysis_root / "comparison.py",
            operator_root / "finite_differences.py",
            operator_root / "ladder_operators.py",
            operator_root / "quantities.py",
            Path(__file__).resolve().with_name("records.py"),
            Path(__file__).resolve().with_name("input.py"),
            Path(__file__).resolve().with_name("evaluation.py"),
            Path(__file__).resolve(),
        )

    @staticmethod
    def sha256(path: Path) -> str:
        """Return the lowercase SHA-256 identity of one explicit source file."""
        return hashlib.sha256(path.read_bytes()).hexdigest()

    @staticmethod
    def matrix(
        value: np.ndarray[tuple[int, int], np.dtype[np.float64]],
    ) -> list[JsonValue]:
        """Convert one finite matrix to its JSON array representation."""
        return cast(list[JsonValue], value.tolist())

    @staticmethod
    def array_sha256(value: np.ndarray[tuple[int, int], np.dtype[np.float64]]) -> str:
        """Hash one matrix as little-endian row-major binary64 bytes."""
        canonical = np.asarray(value, dtype="<f8", order="C")
        return hashlib.sha256(canonical.tobytes(order="C")).hexdigest()

    def case(self, result: HarmonicOscillatorComparisonResult) -> dict[str, JsonValue]:
        """Represent one comparison result in the retained wire contract."""
        request = result.request
        return {
            "case_id": (
                f"b={request.box_half_width.magnitude:g};eta={result.grid_spacing.magnitude:g};"
                f"K={request.retained_dimension}"
            ),
            "box_half_width": request.box_half_width.magnitude,
            "grid_spacing": result.grid_spacing.magnitude,
            "interior_points": result.interior_points,
            "retained_dimension": request.retained_dimension,
            "comparison_map": {
                "definition": (
                    "quadrature-scaled analytic number states followed by "
                    "symmetric Gram orthonormalization"
                ),
                "injection_shape": cast(
                    list[JsonValue],
                    [result.interior_points, request.retained_dimension],
                ),
                "injection_content_sha256": self.array_sha256(
                    result.injection.magnitude
                ),
                "injection_content_encoding": (
                    "IEEE-754 binary64 little-endian row-major"
                ),
                "gram_matrix": self.matrix(result.gram_matrix.magnitude),
                "gram_inverse_square_root": self.matrix(
                    result.gram_inverse_square_root.magnitude
                ),
                "map_direction": "number-state coordinates to grid coordinates",
            },
            "operators_in_common_coordinates": {
                "pulled_back_finite_box": self.matrix(
                    result.pulled_back_hamiltonian.magnitude
                ),
                "exact_retained_ladder": self.matrix(
                    result.reference_hamiltonian.magnitude
                ),
                "finite_box_minus_ladder": self.matrix(result.difference.magnitude),
            },
            "diagnostics": {
                "gram_deviation_frobenius": result.gram_deviation.magnitude,
                "gram_condition_number_2": result.gram_condition_number.magnitude,
                "injection_isometry_error_frobenius": (
                    result.injection_isometry_error.magnitude
                ),
                "absolute_discrepancy_frobenius": (
                    result.absolute_discrepancy.magnitude
                ),
                "relative_discrepancy_frobenius": (
                    result.relative_discrepancy.magnitude
                ),
                "diagonal_discrepancy_frobenius": (
                    result.diagonal_discrepancy.magnitude
                ),
                "off_diagonal_discrepancy_frobenius": (
                    result.off_diagonal_discrepancy.magnitude
                ),
            },
        }

    def cross_grid(
        self, results: tuple[HarmonicOscillatorComparisonResult, ...]
    ) -> list[JsonValue]:
        """Represent fixed-box, fixed-retained-dimension grid differences."""
        records: list[JsonValue] = []
        groups: dict[tuple[float, int], list[HarmonicOscillatorComparisonResult]] = {}
        for result in results:
            groups.setdefault(
                (
                    result.request.box_half_width.magnitude,
                    result.request.retained_dimension,
                ),
                [],
            ).append(result)
        for (box_half_width, retained_dimension), cases in sorted(groups.items()):
            ordered = sorted(
                cases, key=lambda item: item.grid_spacing.magnitude, reverse=True
            )
            for coarse, fine in zip(ordered, ordered[1:], strict=False):
                difference = (
                    coarse.pulled_back_hamiltonian.magnitude
                    - fine.pulled_back_hamiltonian.magnitude
                )
                records.append(
                    {
                        "box_half_width": box_half_width,
                        "retained_dimension": retained_dimension,
                        "coarse_grid_spacing": coarse.grid_spacing.magnitude,
                        "fine_grid_spacing": fine.grid_spacing.magnitude,
                        "coarse_interior_points": coarse.interior_points,
                        "fine_interior_points": fine.interior_points,
                        "coarse_minus_fine_frobenius": float(
                            np.linalg.norm(difference, ord="fro")
                        ),
                    }
                )
        return records
