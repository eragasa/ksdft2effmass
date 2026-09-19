"""Independent verification of retained Appendix E harmonic-oscillator results.

The verifier reconstructs analytic number states with SciPy Hermite polynomials,
forms the finite-difference Hamiltonian independently of the production comparator,
and checks maps, common-coordinate operators, diagnostics, source identities, and
limitations. It intentionally imports no harmonic-oscillator analysis or campaign
implementation module.

A successful verification establishes only the recorded numerical-verification checks
under their explicit binary64 tolerances. It does not establish continuum convergence,
semiconductor relevance, scientific validation, uncertainty quantification, or human
acceptance.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt
from scipy.special import eval_hermite  # type: ignore[import-untyped]

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type RealMatrix = npt.NDArray[np.float64]

LEGACY_RUNNER_SHA256 = (
    "2da2a247f28e6bc513bbb6d5a710b551acd0302ad9b504dc3dd7cedd999c4229"
)


class HarmonicOscillatorResultVerifier:
    """Verify retained maps, operators, diagnostics, and cross-grid comparisons.

    The verifier is a stateless ActionObject. Its independent analytical construction
    uses ``scipy.special.eval_hermite`` rather than the production three-term
    recurrence.
    """

    __slots__ = ()

    def execute(self, result_path: Path, repository_root: Path) -> None:
        """Verify one retained version-one result in an explicit repository.

        Parameters
        ----------
        result_path
            Existing UTF-8 JSON result path.
        repository_root
            Repository root against which retained relative source paths are resolved.

        Raises
        ------
        TypeError
            If represented JSON fields have incorrect semantic types.
        ValueError
            If the wire contract or a current authored implementation identity is
            invalid.
        AssertionError
            If an exact or tolerance-qualified verification criterion fails.
        """
        if not isinstance(result_path, Path):
            raise TypeError("result_path must be pathlib.Path")
        if not isinstance(repository_root, Path):
            raise TypeError("repository_root must be pathlib.Path")
        payload = self.mapping(
            cast(JsonValue, json.loads(result_path.read_text(encoding="utf-8"))),
            "result",
        )
        assert self.integer(payload["schema_version"], "schema_version") == 1
        assert payload["evidence_status"] == "illustrative numerical experiment"
        assert payload["calculation_status"] == "calculated illustrative result"
        constants = self.mapping(
            payload["dimensionless_convention"], "dimensionless_convention"
        )
        hbar = self.real(constants["hbar"], "hbar")
        mass = self.real(constants["mass"], "mass")
        omega = self.real(constants["omega"], "omega")
        oscillator_length = self.real(
            constants["oscillator_length"], "oscillator_length"
        )
        assert oscillator_length == np.sqrt(hbar / (mass * omega))

        cases_value = payload["cases"]
        if not isinstance(cases_value, list) or not cases_value:
            raise TypeError("cases must be a nonempty JSON array")
        pulled_back_by_key: dict[tuple[float, float, int], RealMatrix] = {}
        for case_value in cases_value:
            case = self.mapping(case_value, "case")
            box = self.real(case["box_half_width"], "box_half_width")
            spacing = self.real(case["grid_spacing"], "grid_spacing")
            points = self.integer(case["interior_points"], "interior_points")
            retained = self.integer(case["retained_dimension"], "retained_dimension")
            self.verify_case(
                case,
                box,
                spacing,
                points,
                retained,
                hbar,
                mass,
                omega,
                oscillator_length,
            )
            operators = self.mapping(
                case["operators_in_common_coordinates"], "operators"
            )
            pulled_back_by_key[(box, spacing, retained)] = self.matrix(
                operators["pulled_back_finite_box"], "pulled_back_finite_box"
            )

        cross_value = payload["cross_grid_comparisons"]
        if not isinstance(cross_value, list):
            raise TypeError("cross_grid_comparisons must be a JSON array")
        for record_value in cross_value:
            record = self.mapping(record_value, "cross_grid_comparison")
            box = self.real(record["box_half_width"], "box_half_width")
            retained = self.integer(record["retained_dimension"], "retained_dimension")
            coarse = self.real(record["coarse_grid_spacing"], "coarse_grid_spacing")
            fine = self.real(record["fine_grid_spacing"], "fine_grid_spacing")
            expected = float(
                np.linalg.norm(
                    pulled_back_by_key[(box, coarse, retained)]
                    - pulled_back_by_key[(box, fine, retained)],
                    ord="fro",
                )
            )
            observed = self.real(
                record["coarse_minus_fine_frobenius"],
                "coarse_minus_fine_frobenius",
            )
            np.testing.assert_allclose(observed, expected, rtol=8.0e-15, atol=0.0)

        provenance = self.mapping(payload["provenance"], "provenance")
        input_path = repository_root / self.string(
            provenance["input_path"], "input_path"
        )
        script_path = repository_root / self.string(
            provenance["script_path"], "script_path"
        )
        assert (
            hashlib.sha256(input_path.read_bytes()).hexdigest()
            == provenance["input_sha256"]
        )
        recorded_script_sha256 = self.string(
            provenance["script_sha256"], "script_sha256"
        )
        implementation_identities = provenance.get("implementation_identities")
        if implementation_identities is None:
            if recorded_script_sha256 != LEGACY_RUNNER_SHA256:
                raise ValueError("unrecognized historical runner identity")
        else:
            if not isinstance(implementation_identities, list):
                raise ValueError("implementation_identities must be a JSON array")
            expected_paths = {
                "python/src/ksdft2effmass/analysis/model_systems/intervals.py",
                (
                    "python/src/ksdft2effmass/analysis/model_systems/"
                    "harmonic_oscillator/model.py"
                ),
                (
                    "python/src/ksdft2effmass/analysis/model_systems/"
                    "harmonic_oscillator/comparison.py"
                ),
                "python/src/ksdft2effmass/operators/finite_differences.py",
                "python/src/ksdft2effmass/operators/ladder_operators.py",
                "python/src/ksdft2effmass/operators/quantities.py",
                (
                    "python/src/ksdft2effmass/campaigns/research_monograph/"
                    "harmonic_oscillator/records.py"
                ),
                (
                    "python/src/ksdft2effmass/campaigns/research_monograph/"
                    "harmonic_oscillator/input.py"
                ),
                (
                    "python/src/ksdft2effmass/campaigns/research_monograph/"
                    "harmonic_oscillator/evaluation.py"
                ),
                (
                    "python/src/ksdft2effmass/campaigns/research_monograph/"
                    "harmonic_oscillator/serialization.py"
                ),
            }
            observed_paths = {
                self.string(
                    self.mapping(value, "implementation identity")["path"],
                    "implementation path",
                )
                for value in implementation_identities
            }
            if observed_paths != expected_paths:
                raise ValueError("implementation identity paths do not match")
            if (
                hashlib.sha256(script_path.read_bytes()).hexdigest()
                != recorded_script_sha256
            ):
                raise ValueError("current runner identity differs")
            for value in implementation_identities:
                identity = self.mapping(value, "implementation identity")
                implementation_path = repository_root / self.string(
                    identity["path"], "implementation path"
                )
                implementation_sha256 = self.string(
                    identity["sha256"], "implementation sha256"
                )
                if (
                    hashlib.sha256(implementation_path.read_bytes()).hexdigest()
                    != implementation_sha256
                ):
                    raise ValueError("current implementation identity differs")
        assert payload["limitations"] == [
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
        ]

    def verify_case(
        self,
        case: dict[str, JsonValue],
        box: float,
        spacing: float,
        points: int,
        retained: int,
        hbar: float,
        mass: float,
        omega: float,
        oscillator_length: float,
    ) -> None:
        """Verify one retained case by independent analytic reconstruction.

        Parameters
        ----------
        case
            Decoded version-one case object.
        box
            Finite interval half-width.
        spacing
            Realized uniform grid spacing.
        points
            Number of interior Dirichlet-grid points.
        retained
            Number of retained analytic states.
        hbar
            Reduced Planck constant.
        mass
            Particle mass.
        omega
            Oscillator angular frequency.
        oscillator_length
            Derived oscillator length.

        Raises
        ------
        TypeError
            If a represented case field has the wrong semantic type.
        ValueError
            If a represented numerical field has invalid shape or nonfinite content.
        AssertionError
            If an independent exact or tolerance-qualified criterion fails.
        """
        expected_spacing = 2.0 * box / (points + 1)
        assert spacing == expected_spacing
        coordinates = -box + spacing * np.arange(1, points + 1, dtype=np.float64)

        mapping = self.mapping(case["comparison_map"], "comparison_map")
        assert mapping["definition"] == (
            "quadrature-scaled analytic number states followed by "
            "symmetric Gram orthonormalization"
        )
        assert mapping["injection_shape"] == [points, retained]
        assert mapping["injection_content_encoding"] == (
            "IEEE-754 binary64 little-endian row-major"
        )
        gram = self.matrix(mapping["gram_matrix"], "gram_matrix")
        gram_inverse = self.matrix(
            mapping["gram_inverse_square_root"], "gram_inverse_square_root"
        )
        dimensionless = coordinates / oscillator_length
        independent_sampled = np.empty((points, retained), dtype=np.float64)
        for degree in range(retained):
            normalization = 1.0 / np.sqrt(
                oscillator_length
                * np.sqrt(np.pi)
                * float(2**degree)
                * float(math.factorial(degree))
            )
            independent_sampled[:, degree] = (
                np.sqrt(spacing)
                * normalization
                * eval_hermite(degree, dimensionless)
                * np.exp(-0.5 * np.square(dimensionless))
            )
        states = np.empty((points, retained), dtype=np.float64)
        states[:, 0] = (
            np.pi ** (-0.25)
            * np.exp(-0.5 * np.square(dimensionless))
            / np.sqrt(oscillator_length)
        )
        if retained > 1:
            states[:, 1] = np.sqrt(2.0) * dimensionless * states[:, 0]
        for degree in range(1, retained - 1):
            states[:, degree + 1] = (
                np.sqrt(2.0 / (degree + 1.0)) * dimensionless * states[:, degree]
                - np.sqrt(degree / (degree + 1.0)) * states[:, degree - 1]
            )
        sampled = np.sqrt(spacing) * states
        np.testing.assert_allclose(
            sampled, independent_sampled, rtol=2.0e-14, atol=2.0e-15
        )
        expected_gram = sampled.T @ sampled
        eigenvalues, eigenvectors = np.linalg.eigh(expected_gram)
        assert eigenvalues[0] > 0.0
        expected_inverse = (
            eigenvectors @ np.diag(np.power(eigenvalues, -0.5)) @ eigenvectors.T
        )
        injection = sampled @ expected_inverse
        canonical_injection = np.asarray(injection, dtype="<f8", order="C")
        assert (
            hashlib.sha256(canonical_injection.tobytes(order="C")).hexdigest()
            == (mapping["injection_content_sha256"])
        )
        np.testing.assert_allclose(gram, expected_gram, rtol=2.0e-13, atol=2.0e-14)
        np.testing.assert_allclose(
            gram_inverse, expected_inverse, rtol=2.0e-12, atol=2.0e-13
        )
        np.testing.assert_allclose(
            injection.T @ injection,
            np.eye(retained),
            rtol=2.0e-13,
            atol=2.0e-13,
        )

        kinetic_prefactor = hbar * hbar / (2.0 * mass * spacing * spacing)
        diagonal = 2.0 * kinetic_prefactor + 0.5 * mass * omega * omega * np.square(
            coordinates
        )
        hamiltonian = np.diag(diagonal)
        hamiltonian += np.diag(np.full(points - 1, -kinetic_prefactor), 1)
        hamiltonian += np.diag(np.full(points - 1, -kinetic_prefactor), -1)
        expected_pulled_back = injection.T @ hamiltonian @ injection
        expected_reference = np.diag(
            hbar * omega * (np.arange(retained, dtype=np.float64) + 0.5)
        )
        expected_difference = expected_pulled_back - expected_reference

        operators = self.mapping(case["operators_in_common_coordinates"], "operators")
        pulled_back = self.matrix(
            operators["pulled_back_finite_box"], "pulled_back_finite_box"
        )
        reference = self.matrix(
            operators["exact_retained_ladder"], "exact_retained_ladder"
        )
        difference = self.matrix(
            operators["finite_box_minus_ladder"], "finite_box_minus_ladder"
        )
        operator_scale = float(np.linalg.norm(expected_pulled_back, ord="fro"))
        tolerance = 256.0 * np.finfo(np.float64).eps * max(operator_scale, 1.0)
        np.testing.assert_allclose(pulled_back, expected_pulled_back, atol=tolerance)
        np.testing.assert_array_equal(reference, expected_reference)
        np.testing.assert_allclose(difference, expected_difference, atol=tolerance)
        np.testing.assert_allclose(pulled_back, pulled_back.T, atol=tolerance)

        diagnostics = self.mapping(case["diagnostics"], "diagnostics")
        diagonal_difference = np.diag(np.diag(difference))
        off_diagonal_difference = difference - diagonal_difference
        absolute = float(np.linalg.norm(difference, ord="fro"))
        relative = absolute / float(np.linalg.norm(reference, ord="fro"))
        diagonal_norm = float(np.linalg.norm(diagonal_difference, ord="fro"))
        off_diagonal_norm = float(np.linalg.norm(off_diagonal_difference, ord="fro"))
        expected_diagnostics = {
            "gram_deviation_frobenius": float(
                np.linalg.norm(gram - np.eye(retained), ord="fro")
            ),
            "gram_condition_number_2": float(np.linalg.cond(gram, p=2)),
            "injection_isometry_error_frobenius": float(
                np.linalg.norm(injection.T @ injection - np.eye(retained), ord="fro")
            ),
            "absolute_discrepancy_frobenius": absolute,
            "relative_discrepancy_frobenius": relative,
            "diagonal_discrepancy_frobenius": diagonal_norm,
            "off_diagonal_discrepancy_frobenius": off_diagonal_norm,
        }
        for name, expected in expected_diagnostics.items():
            observed = self.real(diagnostics[name], name)
            np.testing.assert_allclose(observed, expected, rtol=2.0e-12, atol=2.0e-14)
        np.testing.assert_allclose(
            absolute * absolute,
            diagonal_norm * diagonal_norm + off_diagonal_norm * off_diagonal_norm,
            rtol=2.0e-13,
            atol=2.0e-14,
        )

    @staticmethod
    def mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        """Return ``value`` as a JSON object or raise ``TypeError``."""
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be a JSON object")
        return value

    @staticmethod
    def string(value: JsonValue, name: str) -> str:
        """Return ``value`` as a nonempty string or raise ``TypeError``."""
        if not isinstance(value, str) or not value:
            raise TypeError(f"{name} must be a nonempty string")
        return value

    @staticmethod
    def real(value: JsonValue, name: str) -> float:
        """Return ``value`` as a finite float, excluding Boolean values."""
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be a JSON number")
        result = float(value)
        if not np.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result

    @staticmethod
    def integer(value: JsonValue, name: str) -> int:
        """Return ``value`` as an integer, excluding Boolean values."""
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be a JSON integer")
        return value

    @staticmethod
    def matrix(value: JsonValue, name: str) -> RealMatrix:
        """Return ``value`` as a finite two-dimensional binary64 matrix."""
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        matrix = np.asarray(value, dtype=np.float64)
        if matrix.ndim != 2 or not np.all(np.isfinite(matrix)):
            raise ValueError(f"{name} must be a finite matrix")
        return matrix
