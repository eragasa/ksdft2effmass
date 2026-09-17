#!/usr/bin/env python3
"""Independently verify the retained spin-space embedding result."""

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


class SpinSpaceResultVerifier:
    """Verify source identities and independently reconstruct every exact check."""

    __slots__ = ()

    def execute(self, result_path: Path, repository_root: Path) -> None:
        result = self._mapping(
            cast(JsonValue, json.loads(result_path.read_text(encoding="utf-8"))),
            "result",
        )
        if self._integer(result["schema_version"], "schema_version") != 1:
            raise ValueError("unsupported result schema version")
        if result["evidence_status"] != "synthetic test data":
            raise ValueError("result evidence status mismatch")
        if (
            result["calculation_status"]
            != "calculated synthetic numerical-verification result"
        ):
            raise ValueError("result calculation status mismatch")
        provenance = self._mapping(result["provenance"], "provenance")
        input_path = repository_root / self._string(
            provenance["input_path"], "input_path"
        )
        script_path = repository_root / self._string(
            provenance["script_path"], "script_path"
        )
        if self._sha256(input_path) != self._string(
            provenance["input_sha256"], "input_sha256"
        ):
            raise ValueError("input identity mismatch")
        if self._sha256(script_path) != self._string(
            provenance["script_sha256"], "script_sha256"
        ):
            raise ValueError("runner identity mismatch")
        source = self._mapping(
            cast(JsonValue, json.loads(input_path.read_text(encoding="utf-8"))),
            "input",
        )
        tolerance = self._real(source["algebraic_tolerance"], "tolerance")
        if tolerance <= 0.0:
            raise ValueError("tolerance must be positive")
        matrices = self._source_matrices(source)
        operators = self._mapping(result["operators"], "operators")
        self._verify_operators(source, operators, matrices, tolerance)
        checks = self._mapping(result["checks"], "checks")
        np.testing.assert_allclose(
            self._real(checks["algebraic_tolerance"], "recorded tolerance"),
            tolerance,
            rtol=0.0,
            atol=0.0,
        )
        self._verify_hermiticity(checks, matrices, tolerance)
        self._verify_embedding(checks, matrices, tolerance)
        self._verify_block_ordering(checks, matrices, tolerance)
        self._verify_scalar_models(checks, matrices, tolerance)
        self._verify_time_reversal(checks, matrices, tolerance)
        self._verify_rotations(source, checks, matrices, tolerance)
        self._verify_stopping_controls(checks)
        limitations = result["limitations"]
        if not isinstance(limitations, list) or len(limitations) != 4:
            raise ValueError("four explicit limitations are required")

    def _source_matrices(
        self, source: dict[str, JsonValue]
    ) -> dict[str, ComplexMatrix]:
        delta0 = self._real_matrix(
            source["spinless_impurity_operator"], "spinless_impurity_operator"
        )
        h0 = self._real_matrix(source["spinless_hamiltonian"], "spinless_hamiltonian")
        splitting = self._real_matrix(
            source["collinear_splitting_operator"], "collinear_splitting_operator"
        )
        generators = self._mapping(
            source["time_reversal_spinor_antisymmetric_generators"], "generators"
        )
        bx = 1j * self._real_matrix(generators["x"], "generator_x")
        by = 1j * self._real_matrix(generators["y"], "generator_y")
        bz = 1j * self._real_matrix(generators["z"], "generator_z")
        identity = np.eye(2, dtype=np.complex128)
        pauli_x, pauli_y, pauli_z = self._pauli()
        degenerate_hamiltonian = np.kron(h0, identity)
        degenerate_impurity = np.kron(delta0, identity)
        collinear = degenerate_impurity + np.kron(splitting, pauli_z)
        spinor = (
            degenerate_impurity
            + np.kron(bx, pauli_x)
            + np.kron(by, pauli_y)
            + np.kron(bz, pauli_z)
        )
        return {
            "h0": h0,
            "delta0": delta0,
            "splitting": splitting,
            "bx": bx,
            "by": by,
            "bz": bz,
            "degenerate_hamiltonian": degenerate_hamiltonian,
            "degenerate_impurity": degenerate_impurity,
            "collinear": collinear,
            "spinor": spinor,
        }

    def _verify_operators(
        self,
        source: dict[str, JsonValue],
        operators: dict[str, JsonValue],
        matrices: dict[str, ComplexMatrix],
        tolerance: float,
    ) -> None:
        dimension = matrices["delta0"].shape[0]
        permutation = self._permutation(dimension)
        expected = {
            "spinless_hamiltonian": matrices["h0"],
            "spinless_impurity": matrices["delta0"],
            "spin_degenerate_hamiltonian": matrices["degenerate_hamiltonian"],
            "spin_degenerate_impurity": matrices["degenerate_impurity"],
            "collinear_impurity_orbital_major": matrices["collinear"],
            "collinear_impurity_spin_major": (
                permutation.conj().T @ matrices["collinear"] @ permutation
            ),
            "time_reversal_spinor_impurity": matrices["spinor"],
        }
        for identifier, matrix in expected.items():
            record = self._mapping(operators[identifier], identifier)
            observed_matrix = self._complex_matrix(
                record["matrix"], f"{identifier} matrix"
            )
            np.testing.assert_allclose(
                observed_matrix, matrix, rtol=0.0, atol=tolerance
            )
            if (
                self._integer(record["dimension"], "operator dimension")
                != matrix.shape[0]
            ):
                raise ValueError(f"{identifier} dimension metadata mismatch")
        spinless = self._mapping(operators["spinless_impurity"], "spinless")
        if spinless["spin_representation"] != "spinless":
            raise ValueError("spinless metadata mismatch")
        if spinless["basis_ordering"] != "orbital-only":
            raise ValueError("spinless ordering metadata mismatch")
        collinear_spin_major = self._mapping(
            operators["collinear_impurity_spin_major"], "spin-major"
        )
        if collinear_spin_major["basis_ordering"] != "spin-major":
            raise ValueError("spin-major metadata mismatch")
        conventions = self._mapping(source["conventions"], "source conventions")
        result_conventions = {
            "energy_unit": spinless["energy_unit"],
            "energy_reference": spinless["energy_reference"],
            "geometry": spinless["geometry"],
        }
        for name, observed_metadata in result_conventions.items():
            if observed_metadata != conventions[name]:
                raise ValueError(f"{name} metadata mismatch")

    def _verify_hermiticity(
        self,
        checks: dict[str, JsonValue],
        matrices: dict[str, ComplexMatrix],
        tolerance: float,
    ) -> None:
        records = self._mapping(
            checks["hermiticity_maximum_absolute_residuals"], "hermiticity"
        )
        expected = {
            "spinless_hamiltonian": matrices["h0"],
            "spinless_impurity": matrices["delta0"],
            "spin_degenerate_impurity": matrices["degenerate_impurity"],
            "collinear_impurity": matrices["collinear"],
            "time_reversal_spinor_impurity": matrices["spinor"],
        }
        for identifier, matrix in expected.items():
            residual = float(np.max(np.abs(matrix - matrix.conj().T)))
            self._equal(
                self._real(records[identifier], identifier), residual, tolerance
            )
            if residual > tolerance:
                raise ValueError(f"{identifier} is not Hermitian")

    def _verify_embedding(
        self,
        checks: dict[str, JsonValue],
        matrices: dict[str, ComplexMatrix],
        tolerance: float,
    ) -> None:
        record = self._mapping(checks["spin_embedding"], "spin_embedding")
        delta0 = matrices["delta0"]
        lifted = matrices["degenerate_impurity"]
        dimension = delta0.shape[0]
        identity = np.eye(dimension, dtype=np.complex128)
        up = np.kron(identity, np.asarray([[1.0], [0.0]], dtype=np.complex128))
        down = np.kron(identity, np.asarray([[0.0], [1.0]], dtype=np.complex128))
        expected = {
            "up_pullback_frobenius_defect": np.linalg.norm(
                up.conj().T @ lifted @ up - delta0
            ),
            "down_pullback_frobenius_defect": np.linalg.norm(
                down.conj().T @ lifted @ down - delta0
            ),
            "cross_spin_block_frobenius_norm": np.linalg.norm(
                up.conj().T @ lifted @ down
            ),
            "spinless_frobenius_norm": np.linalg.norm(delta0),
            "lifted_frobenius_norm": np.linalg.norm(lifted),
            "expected_lifted_frobenius_norm": np.sqrt(2.0) * np.linalg.norm(delta0),
            "frobenius_scaling_absolute_defect": abs(
                np.linalg.norm(lifted) - np.sqrt(2.0) * np.linalg.norm(delta0)
            ),
            "spinless_rms_per_state": np.linalg.norm(delta0) / np.sqrt(dimension),
            "lifted_rms_per_state": np.linalg.norm(lifted) / np.sqrt(2 * dimension),
        }
        for name, value in expected.items():
            self._equal(self._real(record[name], name), float(value), tolerance)
        for name in (
            "up_pullback_frobenius_defect",
            "down_pullback_frobenius_defect",
            "cross_spin_block_frobenius_norm",
            "frobenius_scaling_absolute_defect",
        ):
            if self._real(record[name], name) > tolerance:
                raise ValueError(f"embedding check failed: {name}")

    def _verify_block_ordering(
        self,
        checks: dict[str, JsonValue],
        matrices: dict[str, ComplexMatrix],
        tolerance: float,
    ) -> None:
        record = self._mapping(checks["block_ordering"], "block_ordering")
        dimension = matrices["delta0"].shape[0]
        permutation = self._permutation(dimension)
        orbital_major = matrices["collinear"]
        spin_major = permutation.conj().T @ orbital_major @ permutation
        recovered = permutation @ spin_major @ permutation.conj().T
        expected = {
            "permutation_unitarity_frobenius_defect": np.linalg.norm(
                permutation.conj().T @ permutation - np.eye(2 * dimension)
            ),
            "spin_up_block_frobenius_defect": np.linalg.norm(
                spin_major[:dimension, :dimension]
                - (matrices["delta0"] + matrices["splitting"])
            ),
            "spin_down_block_frobenius_defect": np.linalg.norm(
                spin_major[dimension:, dimension:]
                - (matrices["delta0"] - matrices["splitting"])
            ),
            "off_diagonal_spin_block_frobenius_norm": (
                np.linalg.norm(spin_major[:dimension, dimension:])
                + np.linalg.norm(spin_major[dimension:, :dimension])
            ),
            "unaligned_ordering_frobenius_defect": np.linalg.norm(
                spin_major - orbital_major
            ),
            "aligned_ordering_frobenius_defect": np.linalg.norm(
                recovered - orbital_major
            ),
            "eigenvalue_maximum_absolute_defect": np.max(
                np.abs(
                    np.linalg.eigvalsh(spin_major) - np.linalg.eigvalsh(orbital_major)
                )
            ),
        }
        for name, value in expected.items():
            self._equal(self._real(record[name], name), float(value), tolerance)
        if expected["unaligned_ordering_frobenius_defect"] <= tolerance:
            raise ValueError("authored ordering control is not discriminating")
        if expected["aligned_ordering_frobenius_defect"] > tolerance:
            raise ValueError("ordering alignment did not recover the operator")

    def _verify_scalar_models(
        self,
        checks: dict[str, JsonValue],
        matrices: dict[str, ComplexMatrix],
        tolerance: float,
    ) -> None:
        records = {
            self._string(record["id"], "scalar id"): record
            for record in self._records(checks["scalar_model_class"], "scalar models")
        }
        expected_matrices = {
            "spin-degenerate": matrices["degenerate_impurity"],
            "collinear": matrices["collinear"],
            "time-reversal-spinor": matrices["spinor"],
        }
        expected_residuals = {
            "spin-degenerate": 0.0,
            "collinear": float(np.sqrt(2.0) * np.linalg.norm(matrices["splitting"])),
            "time-reversal-spinor": float(
                np.sqrt(
                    2.0
                    * sum(
                        np.linalg.norm(matrices[name]) ** 2
                        for name in ("bx", "by", "bz")
                    )
                )
            ),
        }
        dimension = matrices["delta0"].shape[0]
        for identifier, matrix in expected_matrices.items():
            reshaped = matrix.reshape(dimension, 2, dimension, 2)
            fitted = 0.5 * (reshaped[:, 0, :, 0] + reshaped[:, 1, :, 1])
            approximation = np.kron(fitted, np.eye(2, dtype=np.complex128))
            residual = float(np.linalg.norm(matrix - approximation))
            record = records[identifier]
            expected = expected_residuals[identifier]
            values = {
                "fitted_orbital_operator_frobenius_defect": np.linalg.norm(
                    fitted - matrices["delta0"]
                ),
                "absolute_frobenius_residual": residual,
                "expected_absolute_frobenius_residual": expected,
                "analytic_residual_absolute_defect": abs(residual - expected),
                "relative_frobenius_residual": residual / np.linalg.norm(matrix),
                "rms_per_state_residual": residual / np.sqrt(matrix.shape[0]),
            }
            for name, value in values.items():
                self._equal(self._real(record[name], name), float(value), tolerance)
            if abs(residual - expected) > tolerance:
                raise ValueError(f"analytic scalar residual failed for {identifier}")
        if (
            self._real(
                records["spin-degenerate"]["absolute_frobenius_residual"],
                "degenerate scalar residual",
            )
            > tolerance
        ):
            raise ValueError("scalar model must exactly recover the degenerate lift")
        for identifier in ("collinear", "time-reversal-spinor"):
            if (
                self._real(
                    records[identifier]["absolute_frobenius_residual"],
                    f"{identifier} scalar residual",
                )
                <= tolerance
            ):
                raise ValueError(f"scalar model must fail for {identifier}")

    def _verify_time_reversal(
        self,
        checks: dict[str, JsonValue],
        matrices: dict[str, ComplexMatrix],
        tolerance: float,
    ) -> None:
        record = self._mapping(checks["time_reversal"], "time_reversal")
        dimension = matrices["delta0"].shape[0]
        time_reversal: ComplexMatrix = np.asarray(
            np.kron(
                np.eye(dimension, dtype=np.complex128),
                np.asarray([[0.0, 1.0], [-1.0, 0.0]], dtype=np.complex128),
            ),
            dtype=np.complex128,
        )
        expected = {
            "spin_degenerate_frobenius_residual": self._time_reversal_residual(
                matrices["degenerate_impurity"], time_reversal
            ),
            "collinear_frobenius_residual": self._time_reversal_residual(
                matrices["collinear"], time_reversal
            ),
            "collinear_expected_frobenius_residual": float(
                2.0 * np.sqrt(2.0) * np.linalg.norm(matrices["splitting"])
            ),
            "time_reversal_spinor_frobenius_residual": self._time_reversal_residual(
                matrices["spinor"], time_reversal
            ),
        }
        for name, value in expected.items():
            self._equal(self._real(record[name], name), float(value), tolerance)
        if expected["spin_degenerate_frobenius_residual"] > tolerance:
            raise ValueError("degenerate lift must be time-reversal invariant")
        if expected["time_reversal_spinor_frobenius_residual"] > tolerance:
            raise ValueError("spinor construction must be time-reversal invariant")
        if (
            abs(
                expected["collinear_frobenius_residual"]
                - expected["collinear_expected_frobenius_residual"]
            )
            > tolerance
        ):
            raise ValueError("collinear time-reversal oracle mismatch")

    def _verify_rotations(
        self,
        source: dict[str, JsonValue],
        checks: dict[str, JsonValue],
        matrices: dict[str, ComplexMatrix],
        tolerance: float,
    ) -> None:
        records = {
            self._string(record["id"], "rotation id"): record
            for record in self._records(checks["spin_frame_covariance"], "rotations")
        }
        rotations = self._records(source["spin_frame_rotations"], "source rotations")
        pauli = self._pauli()
        matrix = matrices["spinor"]
        dimension = matrices["delta0"].shape[0]
        canonical_time_reversal = np.kron(
            np.eye(dimension),
            np.asarray([[0.0, 1.0], [-1.0, 0.0]], dtype=np.complex128),
        )
        for rotation in rotations:
            identifier = self._string(rotation["id"], "rotation id")
            axis = np.asarray(self._reals(rotation["axis"], "axis"))
            axis /= np.linalg.norm(axis)
            angle = self._real(rotation["angle_radians"], "angle")
            generator = sum(
                (axis[index] * pauli[index] for index in range(3)),
                start=np.zeros((2, 2), dtype=np.complex128),
            )
            spin_rotation = (
                np.cos(angle / 2.0) * np.eye(2) - 1j * np.sin(angle / 2.0) * generator
            )
            full_rotation = np.kron(np.eye(dimension), spin_rotation)
            rotated = full_rotation.conj().T @ matrix @ full_rotation
            recovered = full_rotation @ rotated @ full_rotation.conj().T
            rotated_time_reversal = (
                full_rotation.conj().T @ canonical_time_reversal @ full_rotation.conj()
            )
            expected = {
                "spin_rotation_unitarity_frobenius_defect": np.linalg.norm(
                    spin_rotation.conj().T @ spin_rotation - np.eye(2)
                ),
                "unaligned_frobenius_defect": np.linalg.norm(rotated - matrix),
                "aligned_frobenius_defect": np.linalg.norm(recovered - matrix),
                "eigenvalue_maximum_absolute_defect": np.max(
                    np.abs(np.linalg.eigvalsh(rotated) - np.linalg.eigvalsh(matrix))
                ),
                "frobenius_norm_absolute_defect": abs(
                    np.linalg.norm(rotated) - np.linalg.norm(matrix)
                ),
                "rotated_time_reversal_frobenius_residual": (
                    self._time_reversal_residual(rotated, rotated_time_reversal)
                ),
                "hermiticity_maximum_absolute_residual": np.max(
                    np.abs(rotated - rotated.conj().T)
                ),
            }
            record = records[identifier]
            if record["direct_compatibility"] is not False:
                raise ValueError("different spin frames must not compare directly")
            if record["direct_difference_status"] != "stopped":
                raise ValueError("unaligned spin-frame difference must stop")
            issues = self._strings(record["direct_issue_codes"], "rotation issues")
            if issues != ("SPIN.COMPATIBILITY.SPIN_FRAME",):
                raise ValueError("spin-frame stop code mismatch")
            for name, value in expected.items():
                self._equal(self._real(record[name], name), float(value), tolerance)
            if expected["unaligned_frobenius_defect"] <= tolerance:
                raise ValueError("rotation control is not discriminating")
            for name in (
                "aligned_frobenius_defect",
                "eigenvalue_maximum_absolute_defect",
                "frobenius_norm_absolute_defect",
                "rotated_time_reversal_frobenius_residual",
                "hermiticity_maximum_absolute_residual",
            ):
                if expected[name] > tolerance:
                    raise ValueError(f"rotation covariance failed: {identifier} {name}")

    def _verify_stopping_controls(self, checks: dict[str, JsonValue]) -> None:
        records = {
            self._string(record["id"], "stop id"): record
            for record in self._records(checks["stopping_controls"], "stops")
        }
        expected = {
            "spinless-versus-spinful": (
                "SPIN.COMPATIBILITY.BASIS_ORDER",
                "SPIN.COMPATIBILITY.DIMENSION",
                "SPIN.COMPATIBILITY.SPIN_FRAME",
                "SPIN.COMPATIBILITY.SPIN_REPRESENTATION",
                "SPIN.COMPATIBILITY.STATE_SPACE",
            ),
            "unaligned-block-order": ("SPIN.COMPATIBILITY.BASIS_ORDER",),
            "different-energy-reference": ("SPIN.COMPATIBILITY.ENERGY_REFERENCE",),
        }
        if set(records) != set(expected):
            raise ValueError("stopping-control identities mismatch")
        for identifier, issue_codes in expected.items():
            record = records[identifier]
            if record["status"] != "stopped" or record["frobenius_norm"] is not None:
                raise ValueError(f"stopping control did not stop: {identifier}")
            if self._strings(record["issue_codes"], "issue_codes") != issue_codes:
                raise ValueError(f"stopping-control issues mismatch: {identifier}")

    @staticmethod
    def _pauli() -> tuple[ComplexMatrix, ComplexMatrix, ComplexMatrix]:
        return (
            np.asarray([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128),
            np.asarray([[0.0, -1j], [1j, 0.0]], dtype=np.complex128),
            np.asarray([[1.0, 0.0], [0.0, -1.0]], dtype=np.complex128),
        )

    @staticmethod
    def _permutation(dimension: int) -> ComplexMatrix:
        result = np.zeros((2 * dimension, 2 * dimension), dtype=np.complex128)
        for orbital in range(dimension):
            result[2 * orbital, orbital] = 1.0
            result[2 * orbital + 1, dimension + orbital] = 1.0
        return result

    @staticmethod
    def _time_reversal_residual(
        matrix: ComplexMatrix, unitary_part: ComplexMatrix
    ) -> float:
        transformed = unitary_part @ matrix.conj() @ unitary_part.conj().T
        return float(np.linalg.norm(transformed - matrix))

    @staticmethod
    def _equal(observed: float, expected: float, tolerance: float) -> None:
        np.testing.assert_allclose(observed, expected, rtol=0.0, atol=tolerance)

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

    def _strings(self, value: JsonValue, name: str) -> tuple[str, ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return tuple(self._string(item, name) for item in value)

    @staticmethod
    def _integer(value: JsonValue, name: str) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be a JSON integer")
        return value

    @staticmethod
    def _real(value: JsonValue, name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be a JSON number")
        result = float(value)
        if not np.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result

    def _reals(self, value: JsonValue, name: str) -> tuple[float, ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return tuple(self._real(item, name) for item in value)

    def _real_matrix(self, value: JsonValue, name: str) -> ComplexMatrix:
        if not isinstance(value, list) or not value:
            raise TypeError(f"{name} must be a nonempty matrix")
        rows: list[list[float]] = []
        for row in value:
            if not isinstance(row, list):
                raise TypeError(f"{name} rows must be JSON arrays")
            rows.append([self._real(item, name) for item in row])
        return np.asarray(rows, dtype=np.complex128)

    def _complex_matrix(self, value: JsonValue, name: str) -> ComplexMatrix:
        if not isinstance(value, list) or not value:
            raise TypeError(f"{name} must be a nonempty matrix")
        rows: list[list[complex]] = []
        for row in value:
            if not isinstance(row, list):
                raise TypeError(f"{name} rows must be JSON arrays")
            values: list[complex] = []
            for pair in row:
                if not isinstance(pair, list) or len(pair) != 2:
                    raise TypeError(f"{name} entries must be [real, imaginary]")
                values.append(
                    complex(
                        self._real(pair[0], name),
                        self._real(pair[1], name),
                    )
                )
            rows.append(values)
        return np.asarray(rows, dtype=np.complex128)

    @staticmethod
    def _sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    """Adapt one result path into the owned verification action."""
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    arguments = parser.parse_args()
    result_path = arguments.result.resolve()
    repository_root = Path(__file__).resolve().parents[3]
    SpinSpaceResultVerifier().execute(result_path, repository_root)
    print("impurity spin-space embedding result: PASS")


if __name__ == "__main__":
    main()
