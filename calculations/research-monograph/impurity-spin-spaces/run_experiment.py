#!/usr/bin/env python3
"""Run the controlled spin-space embedding exercise for Appendix I."""

from __future__ import annotations

import argparse
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
type RealMatrixTuple = tuple[tuple[float, ...], ...]
type RealVector = npt.NDArray[np.float64]
type ComplexMatrix = npt.NDArray[np.complex128]
type MatrixTuple = tuple[tuple[complex, ...], ...]
type SpinRepresentation = Literal["spinless", "spin-half"]
type BasisOrdering = Literal["orbital-only", "orbital-major", "spin-major"]


@dataclass(frozen=True, slots=True)
class SpinFrameRotation:
    """Represent one declared proper spin-frame rotation."""

    identifier: str
    axis: tuple[float, float, float]
    angle_radians: float

    def __post_init__(self) -> None:
        if not self.identifier:
            raise ValueError("rotation identifier must be nonempty")
        values = np.asarray(self.axis + (self.angle_radians,), dtype=np.float64)
        if not np.all(np.isfinite(values)):
            raise ValueError("rotation values must be finite")
        if np.linalg.norm(np.asarray(self.axis, dtype=np.float64)) == 0.0:
            raise ValueError("rotation axis must be nonzero")


@dataclass(frozen=True, slots=True)
class SpinSpaceInput:
    """Represent immutable authored inputs for the synthetic finite model."""

    experiment_id: str
    energy_unit: str
    energy_reference: str
    geometry: str
    orbital_labels: tuple[str, ...]
    spin_labels: tuple[str, str]
    spinless_hamiltonian: RealMatrixTuple
    spinless_impurity: RealMatrixTuple
    collinear_splitting: RealMatrixTuple
    antisymmetric_x: RealMatrixTuple
    antisymmetric_y: RealMatrixTuple
    antisymmetric_z: RealMatrixTuple
    rotations: tuple[SpinFrameRotation, ...]
    algebraic_tolerance: float

    def __post_init__(self) -> None:
        if not self.experiment_id:
            raise ValueError("experiment_id must be nonempty")
        if not all((self.energy_unit, self.energy_reference, self.geometry)):
            raise ValueError("represented conventions must be nonempty")
        if len(self.orbital_labels) < 2 or len(set(self.orbital_labels)) != len(
            self.orbital_labels
        ):
            raise ValueError("orbital labels must be unique and nontrivial")
        if len(set(self.spin_labels)) != 2:
            raise ValueError("spin labels must be distinct")
        dimension = len(self.orbital_labels)
        matrices = (
            self.spinless_hamiltonian,
            self.spinless_impurity,
            self.collinear_splitting,
            self.antisymmetric_x,
            self.antisymmetric_y,
            self.antisymmetric_z,
        )
        if any(
            len(matrix) != dimension or any(len(row) != dimension for row in matrix)
            for matrix in matrices
        ):
            raise ValueError("all authored matrices must match the orbital dimension")
        if not self.rotations:
            raise ValueError("at least one spin-frame rotation is required")
        if not np.isfinite(self.algebraic_tolerance) or self.algebraic_tolerance <= 0.0:
            raise ValueError("algebraic_tolerance must be positive and finite")


@dataclass(frozen=True, slots=True)
class SpinBasis:
    """Identify one represented finite orbital-spin state space."""

    state_space_id: str
    orbital_labels: tuple[str, ...]
    spin_representation: SpinRepresentation
    basis_ordering: BasisOrdering
    spin_frame_id: str
    energy_unit: str
    energy_reference: str
    geometry: str

    def __post_init__(self) -> None:
        if not all(
            (
                self.state_space_id,
                self.spin_frame_id,
                self.energy_unit,
                self.energy_reference,
                self.geometry,
            )
        ):
            raise ValueError("basis conventions must be nonempty")
        if not self.orbital_labels or len(set(self.orbital_labels)) != len(
            self.orbital_labels
        ):
            raise ValueError("orbital labels must be unique and nonempty")
        if self.spin_representation == "spinless":
            if self.basis_ordering != "orbital-only":
                raise ValueError("spinless basis must use orbital-only ordering")
        elif self.basis_ordering == "orbital-only":
            raise ValueError("spin-half basis must declare a spinful ordering")

    @property
    def dimension(self) -> int:
        """Return the represented dimension implied by the state space."""
        multiplier = 1 if self.spin_representation == "spinless" else 2
        return multiplier * len(self.orbital_labels)


@dataclass(frozen=True, slots=True)
class RepresentedSpinOperator:
    """Store one immutable finite operator and all comparison-critical metadata."""

    identifier: str
    basis: SpinBasis
    matrix: MatrixTuple

    def __post_init__(self) -> None:
        if not self.identifier:
            raise ValueError("operator identifier must be nonempty")
        if len(self.matrix) != self.basis.dimension or any(
            len(row) != self.basis.dimension for row in self.matrix
        ):
            raise ValueError("matrix shape must agree with the represented basis")
        flat = np.asarray(self.matrix, dtype=np.complex128)
        if not np.all(np.isfinite(flat)):
            raise ValueError("represented matrix entries must be finite")


@dataclass(frozen=True, slots=True)
class CompatibilityResult:
    """Record whether two represented operators admit direct comparison."""

    compatible: bool
    issue_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.compatible == bool(self.issue_codes):
            raise ValueError("compatibility status must agree with issue codes")
        if self.issue_codes != tuple(sorted(set(self.issue_codes))):
            raise ValueError("issue codes must be sorted and unique")


@dataclass(frozen=True, slots=True)
class DifferenceResult:
    """Record a represented signed difference or a structured stop."""

    status: Literal["computed", "stopped"]
    issue_codes: tuple[str, ...]
    frobenius_norm: float | None

    def __post_init__(self) -> None:
        if self.status == "computed":
            if self.issue_codes or self.frobenius_norm is None:
                raise ValueError("computed difference requires exactly one norm")
        elif not self.issue_codes or self.frobenius_norm is not None:
            raise ValueError("stopped difference requires issues and no norm")


class SpinSpaceInputDeserializer:
    """Deserialize the closed version-1 experiment input."""

    __slots__ = ()

    def execute(self, payload: bytes) -> SpinSpaceInput:
        value = cast(JsonValue, json.loads(payload.decode("utf-8")))
        root = self._mapping(value, "input")
        if self._integer(root["schema_version"], "schema_version") != 1:
            raise ValueError("unsupported input schema version")
        if root["evidence_status"] != "synthetic test data":
            raise ValueError("evidence_status must identify synthetic test data")
        conventions = self._mapping(root["conventions"], "conventions")
        if conventions["canonical_tensor_order"] != "orbital-major":
            raise ValueError("canonical tensor order must be orbital-major")
        generators = self._mapping(
            root["time_reversal_spinor_antisymmetric_generators"], "generators"
        )
        rotations_value = root["spin_frame_rotations"]
        if not isinstance(rotations_value, list):
            raise TypeError("spin_frame_rotations must be a JSON array")
        rotations = tuple(self._rotation(item) for item in rotations_value)
        spin_labels = self._strings(
            conventions["canonical_spin_basis"], "canonical_spin_basis"
        )
        if len(spin_labels) != 2:
            raise ValueError("canonical_spin_basis must contain two labels")
        return SpinSpaceInput(
            experiment_id=self._string(root["experiment_id"], "experiment_id"),
            energy_unit=self._string(conventions["energy_unit"], "energy_unit"),
            energy_reference=self._string(
                conventions["energy_reference"], "energy_reference"
            ),
            geometry=self._string(conventions["geometry"], "geometry"),
            orbital_labels=self._strings(
                conventions["orbital_basis_order"], "orbital_basis_order"
            ),
            spin_labels=(spin_labels[0], spin_labels[1]),
            spinless_hamiltonian=self._matrix(
                root["spinless_hamiltonian"], "spinless_hamiltonian"
            ),
            spinless_impurity=self._matrix(
                root["spinless_impurity_operator"], "spinless_impurity_operator"
            ),
            collinear_splitting=self._matrix(
                root["collinear_splitting_operator"],
                "collinear_splitting_operator",
            ),
            antisymmetric_x=self._matrix(generators["x"], "generator_x"),
            antisymmetric_y=self._matrix(generators["y"], "generator_y"),
            antisymmetric_z=self._matrix(generators["z"], "generator_z"),
            rotations=rotations,
            algebraic_tolerance=self._real(
                root["algebraic_tolerance"], "algebraic_tolerance"
            ),
        )

    def _rotation(self, value: JsonValue) -> SpinFrameRotation:
        record = self._mapping(value, "rotation")
        axis = self._reals(record["axis"], "axis")
        if len(axis) != 3:
            raise ValueError("rotation axis must have three components")
        return SpinFrameRotation(
            identifier=self._string(record["id"], "rotation id"),
            axis=(axis[0], axis[1], axis[2]),
            angle_radians=self._real(record["angle_radians"], "angle_radians"),
        )

    @staticmethod
    def _mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be a JSON object")
        return value

    @staticmethod
    def _string(value: JsonValue, name: str) -> str:
        if not isinstance(value, str) or not value:
            raise TypeError(f"{name} must be a nonempty string")
        return value

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

    def _strings(self, value: JsonValue, name: str) -> tuple[str, ...]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return tuple(self._string(item, name) for item in value)

    def _matrix(self, value: JsonValue, name: str) -> RealMatrixTuple:
        if not isinstance(value, list) or not value:
            raise TypeError(f"{name} must be a nonempty matrix")
        rows: list[tuple[float, ...]] = []
        for row in value:
            if not isinstance(row, list):
                raise TypeError(f"{name} rows must be JSON arrays")
            rows.append(tuple(self._real(item, name) for item in row))
        return tuple(rows)


class SpinOperatorCompatibilityAnalyzer:
    """Check direct represented-operator compatibility before subtraction."""

    __slots__ = ()

    def execute(
        self, reference: RepresentedSpinOperator, candidate: RepresentedSpinOperator
    ) -> CompatibilityResult:
        issues: list[str] = []
        left = reference.basis
        right = candidate.basis
        fields = (
            ("STATE_SPACE", left.state_space_id, right.state_space_id),
            ("DIMENSION", left.dimension, right.dimension),
            ("ORBITAL_ORDER", left.orbital_labels, right.orbital_labels),
            (
                "SPIN_REPRESENTATION",
                left.spin_representation,
                right.spin_representation,
            ),
            ("BASIS_ORDER", left.basis_ordering, right.basis_ordering),
            ("SPIN_FRAME", left.spin_frame_id, right.spin_frame_id),
            ("ENERGY_UNIT", left.energy_unit, right.energy_unit),
            ("ENERGY_REFERENCE", left.energy_reference, right.energy_reference),
            ("GEOMETRY", left.geometry, right.geometry),
        )
        for code, first, second in fields:
            if first != second:
                issues.append(f"SPIN.COMPATIBILITY.{code}")
        ordered = tuple(sorted(issues))
        return CompatibilityResult(not ordered, ordered)


class SpinOperatorDifferencer:
    """Compute candidate minus reference only after represented compatibility."""

    __slots__ = ("_compatibility",)

    def __init__(self) -> None:
        self._compatibility = SpinOperatorCompatibilityAnalyzer()

    def execute(
        self, reference: RepresentedSpinOperator, candidate: RepresentedSpinOperator
    ) -> DifferenceResult:
        compatibility = self._compatibility.execute(reference, candidate)
        if not compatibility.compatible:
            return DifferenceResult("stopped", compatibility.issue_codes, None)
        difference = self._array(candidate) - self._array(reference)
        return DifferenceResult("computed", (), float(np.linalg.norm(difference)))

    @staticmethod
    def _array(record: RepresentedSpinOperator) -> ComplexMatrix:
        return np.asarray(record.matrix, dtype=np.complex128)


class SpinSpaceResultSerializer:
    """Serialize the calculated result into canonical JSON bytes."""

    __slots__ = ()

    def execute(self, payload: dict[str, JsonValue]) -> bytes:
        serialized = json.dumps(payload, indent=2, sort_keys=True, allow_nan=False)
        return (serialized + "\n").encode("utf-8")


class SpinSpaceEmbeddingExperiment:
    """Execute exact spin embeddings, covariance checks, and stopping controls."""

    __slots__ = ("_compatibility", "_differencer", "_serializer")

    def __init__(self) -> None:
        self._compatibility = SpinOperatorCompatibilityAnalyzer()
        self._differencer = SpinOperatorDifferencer()
        self._serializer = SpinSpaceResultSerializer()

    def execute(
        self, specification: SpinSpaceInput, input_path: Path, script_path: Path
    ) -> bytes:
        matrices = self._matrices(specification)
        bases = self._bases(specification)
        operators = self._operators(specification, bases, matrices)
        checks = self._checks(specification, bases, operators, matrices)
        repository_root = script_path.parents[3]
        payload: dict[str, JsonValue] = {
            "schema_version": 1,
            "experiment_id": specification.experiment_id,
            "evidence_status": "synthetic test data",
            "calculation_status": "calculated synthetic numerical-verification result",
            "conventions": {
                "energy_unit": specification.energy_unit,
                "energy_reference": specification.energy_reference,
                "geometry": specification.geometry,
                "orbital_basis_order": list(specification.orbital_labels),
                "canonical_spin_basis": list(specification.spin_labels),
                "canonical_tensor_order": "orbital-major",
                "signed_difference_order": "candidate_minus_reference",
            },
            "operators": {
                name: self._operator_json(record) for name, record in operators.items()
            },
            "checks": checks,
            "error_accounting": {
                "represented_construction_and_roundoff": (
                    "Reported by exact lift, block, covariance, Hermiticity, "
                    "time-reversal, and analytic-residual defects."
                ),
                "state_space_and_alignment": (
                    "Reported by structured compatibility stops and aligned versus "
                    "unaligned ordering and spin-frame defects."
                ),
                "model_class": (
                    "Reported by best spin-independent scalar-model residuals; it is "
                    "not combined with representation error."
                ),
                "parent_model": (
                    "Not assessed; every matrix is authored synthetic data."
                ),
                "scientific_validation": "Not performed.",
                "uncertainty_quantification": "Not performed.",
            },
            "limitations": [
                "The finite matrices are synthetic test data, not Kohn-Sham or "
                "material operators.",
                "The exact comparison maps are known by construction and do not "
                "test physical orbital alignment.",
                "Time-reversal checks exercise declared finite-matrix conventions, "
                "not a material symmetry analysis.",
                "Passing checks do not validate phosphorus, boron, silicon, SOC, "
                "or transferability.",
            ],
            "provenance": {
                "input_path": input_path.resolve()
                .relative_to(repository_root)
                .as_posix(),
                "input_sha256": self._sha256(input_path),
                "script_path": script_path.resolve()
                .relative_to(repository_root)
                .as_posix(),
                "script_sha256": self._sha256(script_path),
                "python_version": platform.python_version(),
                "numpy_version": np.__version__,
            },
        }
        return self._serializer.execute(payload)

    def _matrices(self, specification: SpinSpaceInput) -> dict[str, ComplexMatrix]:
        h0 = np.asarray(specification.spinless_hamiltonian, dtype=np.complex128)
        delta0 = np.asarray(specification.spinless_impurity, dtype=np.complex128)
        splitting = np.asarray(specification.collinear_splitting, dtype=np.complex128)
        generators = tuple(
            np.asarray(value, dtype=np.complex128)
            for value in (
                specification.antisymmetric_x,
                specification.antisymmetric_y,
                specification.antisymmetric_z,
            )
        )
        self._require_hermitian(h0, "spinless_hamiltonian")
        self._require_hermitian(delta0, "spinless_impurity")
        self._require_hermitian(splitting, "collinear_splitting")
        for identifier, generator in zip(("x", "y", "z"), generators, strict=True):
            if not np.allclose(
                generator + generator.T,
                0.0,
                rtol=0.0,
                atol=specification.algebraic_tolerance,
            ):
                raise ValueError(f"{identifier} generator must be antisymmetric")
        bx, by, bz = (1j * generator for generator in generators)
        pauli_x, pauli_y, pauli_z = self._pauli()
        identity = np.eye(2, dtype=np.complex128)
        degenerate_hamiltonian = np.kron(h0, identity)
        degenerate_impurity = np.kron(delta0, identity)
        collinear_impurity = degenerate_impurity + np.kron(splitting, pauli_z)
        spinor_impurity = (
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
            "collinear_impurity": collinear_impurity,
            "spinor_impurity": spinor_impurity,
        }

    def _bases(self, specification: SpinSpaceInput) -> dict[str, SpinBasis]:
        return {
            "spinless": SpinBasis(
                state_space_id="synthetic_orbital_space",
                orbital_labels=specification.orbital_labels,
                spin_representation="spinless",
                basis_ordering="orbital-only",
                spin_frame_id="not_applicable",
                energy_unit=specification.energy_unit,
                energy_reference=specification.energy_reference,
                geometry=specification.geometry,
            ),
            "orbital_major": SpinBasis(
                state_space_id="synthetic_orbital_tensor_spin_half",
                orbital_labels=specification.orbital_labels,
                spin_representation="spin-half",
                basis_ordering="orbital-major",
                spin_frame_id="z-canonical",
                energy_unit=specification.energy_unit,
                energy_reference=specification.energy_reference,
                geometry=specification.geometry,
            ),
            "spin_major": SpinBasis(
                state_space_id="synthetic_orbital_tensor_spin_half",
                orbital_labels=specification.orbital_labels,
                spin_representation="spin-half",
                basis_ordering="spin-major",
                spin_frame_id="z-canonical",
                energy_unit=specification.energy_unit,
                energy_reference=specification.energy_reference,
                geometry=specification.geometry,
            ),
        }

    def _operators(
        self,
        specification: SpinSpaceInput,
        bases: dict[str, SpinBasis],
        matrices: dict[str, ComplexMatrix],
    ) -> dict[str, RepresentedSpinOperator]:
        permutation = self._spin_major_permutation(len(specification.orbital_labels))
        collinear_spin_major = (
            permutation.conj().T @ matrices["collinear_impurity"] @ permutation
        )
        return {
            "spinless_hamiltonian": self._record(
                "spinless_hamiltonian", bases["spinless"], matrices["h0"]
            ),
            "spinless_impurity": self._record(
                "spinless_impurity", bases["spinless"], matrices["delta0"]
            ),
            "spin_degenerate_hamiltonian": self._record(
                "spin_degenerate_hamiltonian",
                bases["orbital_major"],
                matrices["degenerate_hamiltonian"],
            ),
            "spin_degenerate_impurity": self._record(
                "spin_degenerate_impurity",
                bases["orbital_major"],
                matrices["degenerate_impurity"],
            ),
            "collinear_impurity_orbital_major": self._record(
                "collinear_impurity_orbital_major",
                bases["orbital_major"],
                matrices["collinear_impurity"],
            ),
            "collinear_impurity_spin_major": self._record(
                "collinear_impurity_spin_major",
                bases["spin_major"],
                collinear_spin_major,
            ),
            "time_reversal_spinor_impurity": self._record(
                "time_reversal_spinor_impurity",
                bases["orbital_major"],
                matrices["spinor_impurity"],
            ),
        }

    def _checks(
        self,
        specification: SpinSpaceInput,
        bases: dict[str, SpinBasis],
        operators: dict[str, RepresentedSpinOperator],
        matrices: dict[str, ComplexMatrix],
    ) -> dict[str, JsonValue]:
        dimension = len(specification.orbital_labels)
        identity_orbital = np.eye(dimension, dtype=np.complex128)
        up = np.asarray([[1.0], [0.0]], dtype=np.complex128)
        down = np.asarray([[0.0], [1.0]], dtype=np.complex128)
        embed_up = np.kron(identity_orbital, up)
        embed_down = np.kron(identity_orbital, down)
        lifted = matrices["degenerate_impurity"]
        delta0 = matrices["delta0"]
        spin_embedding: dict[str, JsonValue] = {
            "up_pullback_frobenius_defect": self._norm(
                embed_up.conj().T @ lifted @ embed_up - delta0
            ),
            "down_pullback_frobenius_defect": self._norm(
                embed_down.conj().T @ lifted @ embed_down - delta0
            ),
            "cross_spin_block_frobenius_norm": self._norm(
                embed_up.conj().T @ lifted @ embed_down
            ),
            "spinless_frobenius_norm": self._norm(delta0),
            "lifted_frobenius_norm": self._norm(lifted),
            "expected_lifted_frobenius_norm": float(
                np.sqrt(2.0) * np.linalg.norm(delta0)
            ),
            "frobenius_scaling_absolute_defect": abs(
                self._norm(lifted) - float(np.sqrt(2.0) * np.linalg.norm(delta0))
            ),
            "spinless_rms_per_state": self._norm(delta0) / np.sqrt(dimension),
            "lifted_rms_per_state": self._norm(lifted) / np.sqrt(2 * dimension),
        }
        permutation = self._spin_major_permutation(dimension)
        collinear = matrices["collinear_impurity"]
        spin_major = permutation.conj().T @ collinear @ permutation
        recovered = permutation @ spin_major @ permutation.conj().T
        upper = spin_major[:dimension, :dimension]
        lower = spin_major[dimension:, dimension:]
        block_ordering: dict[str, JsonValue] = {
            "permutation_unitarity_frobenius_defect": self._norm(
                permutation.conj().T @ permutation - np.eye(2 * dimension)
            ),
            "spin_up_block_frobenius_defect": self._norm(
                upper - (delta0 + matrices["splitting"])
            ),
            "spin_down_block_frobenius_defect": self._norm(
                lower - (delta0 - matrices["splitting"])
            ),
            "off_diagonal_spin_block_frobenius_norm": self._norm(
                spin_major[:dimension, dimension:]
            )
            + self._norm(spin_major[dimension:, :dimension]),
            "unaligned_ordering_frobenius_defect": self._norm(spin_major - collinear),
            "aligned_ordering_frobenius_defect": self._norm(recovered - collinear),
            "eigenvalue_maximum_absolute_defect": self._eigenvalue_defect(
                spin_major, collinear
            ),
        }
        scalar_models: list[JsonValue] = [
            self._scalar_model_record("spin-degenerate", lifted, delta0, 0.0),
            self._scalar_model_record(
                "collinear",
                collinear,
                delta0,
                float(np.sqrt(2.0) * np.linalg.norm(matrices["splitting"])),
            ),
            self._scalar_model_record(
                "time-reversal-spinor",
                matrices["spinor_impurity"],
                delta0,
                float(
                    np.sqrt(
                        2.0
                        * sum(
                            np.linalg.norm(matrices[name]) ** 2
                            for name in ("bx", "by", "bz")
                        )
                    )
                ),
            ),
        ]
        time_reversal_matrix: ComplexMatrix = np.asarray(
            np.kron(
                identity_orbital,
                np.asarray([[0.0, 1.0], [-1.0, 0.0]], dtype=np.complex128),
            ),
            dtype=np.complex128,
        )
        time_reversal: dict[str, JsonValue] = {
            "spin_degenerate_frobenius_residual": self._time_reversal_residual(
                lifted, time_reversal_matrix
            ),
            "collinear_frobenius_residual": self._time_reversal_residual(
                collinear, time_reversal_matrix
            ),
            "collinear_expected_frobenius_residual": float(
                2.0 * np.sqrt(2.0) * np.linalg.norm(matrices["splitting"])
            ),
            "time_reversal_spinor_frobenius_residual": (
                self._time_reversal_residual(
                    matrices["spinor_impurity"], time_reversal_matrix
                )
            ),
        }
        covariance: list[JsonValue] = [
            self._rotation_record(
                rotation,
                bases["orbital_major"],
                matrices["spinor_impurity"],
                time_reversal_matrix,
            )
            for rotation in specification.rotations
        ]
        stopping = self._stopping_controls(specification, bases, operators)
        hermiticity: dict[str, JsonValue] = {
            name: self._hermiticity_residual(matrix)
            for name, matrix in (
                ("spinless_hamiltonian", matrices["h0"]),
                ("spinless_impurity", delta0),
                ("spin_degenerate_impurity", lifted),
                ("collinear_impurity", collinear),
                ("time_reversal_spinor_impurity", matrices["spinor_impurity"]),
            )
        }
        return {
            "hermiticity_maximum_absolute_residuals": hermiticity,
            "spin_embedding": spin_embedding,
            "block_ordering": block_ordering,
            "scalar_model_class": scalar_models,
            "time_reversal": time_reversal,
            "spin_frame_covariance": covariance,
            "stopping_controls": stopping,
            "algebraic_tolerance": specification.algebraic_tolerance,
        }

    def _rotation_record(
        self,
        rotation: SpinFrameRotation,
        canonical_basis: SpinBasis,
        matrix: ComplexMatrix,
        time_reversal_matrix: ComplexMatrix,
    ) -> dict[str, JsonValue]:
        pauli = self._pauli()
        axis = np.asarray(rotation.axis, dtype=np.float64)
        axis /= np.linalg.norm(axis)
        generator = sum(
            (axis[index] * pauli[index] for index in range(3)),
            start=np.zeros((2, 2), dtype=np.complex128),
        )
        spin_rotation = (
            np.cos(rotation.angle_radians / 2.0) * np.eye(2)
            - 1j * np.sin(rotation.angle_radians / 2.0) * generator
        )
        full_rotation = np.kron(
            np.eye(len(canonical_basis.orbital_labels), dtype=np.complex128),
            spin_rotation,
        )
        rotated = full_rotation.conj().T @ matrix @ full_rotation
        recovered = full_rotation @ rotated @ full_rotation.conj().T
        rotated_time_reversal = (
            full_rotation.conj().T @ time_reversal_matrix @ full_rotation.conj()
        )
        rotated_basis = SpinBasis(
            state_space_id=canonical_basis.state_space_id,
            orbital_labels=canonical_basis.orbital_labels,
            spin_representation=canonical_basis.spin_representation,
            basis_ordering=canonical_basis.basis_ordering,
            spin_frame_id=rotation.identifier,
            energy_unit=canonical_basis.energy_unit,
            energy_reference=canonical_basis.energy_reference,
            geometry=canonical_basis.geometry,
        )
        canonical_record = self._record("canonical", canonical_basis, matrix)
        rotated_record = self._record("rotated", rotated_basis, rotated)
        compatibility = self._compatibility.execute(canonical_record, rotated_record)
        difference = self._differencer.execute(canonical_record, rotated_record)
        return {
            "id": rotation.identifier,
            "axis": [float(value) for value in axis],
            "angle_radians": rotation.angle_radians,
            "spin_rotation_unitarity_frobenius_defect": self._norm(
                spin_rotation.conj().T @ spin_rotation - np.eye(2)
            ),
            "direct_compatibility": compatibility.compatible,
            "direct_issue_codes": list(compatibility.issue_codes),
            "direct_difference_status": difference.status,
            "unaligned_frobenius_defect": self._norm(rotated - matrix),
            "aligned_frobenius_defect": self._norm(recovered - matrix),
            "eigenvalue_maximum_absolute_defect": self._eigenvalue_defect(
                rotated, matrix
            ),
            "frobenius_norm_absolute_defect": abs(
                self._norm(rotated) - self._norm(matrix)
            ),
            "rotated_time_reversal_frobenius_residual": (
                self._time_reversal_residual(rotated, rotated_time_reversal)
            ),
            "hermiticity_maximum_absolute_residual": self._hermiticity_residual(
                rotated
            ),
        }

    def _stopping_controls(
        self,
        specification: SpinSpaceInput,
        bases: dict[str, SpinBasis],
        operators: dict[str, RepresentedSpinOperator],
    ) -> list[JsonValue]:
        spinless = operators["spinless_impurity"]
        degenerate = operators["spin_degenerate_impurity"]
        spin_major = operators["collinear_impurity_spin_major"]
        orbital_major = operators["collinear_impurity_orbital_major"]
        wrong_reference_basis = SpinBasis(
            state_space_id=bases["orbital_major"].state_space_id,
            orbital_labels=specification.orbital_labels,
            spin_representation="spin-half",
            basis_ordering="orbital-major",
            spin_frame_id="z-canonical",
            energy_unit=specification.energy_unit,
            energy_reference="different_zero",
            geometry=specification.geometry,
        )
        wrong_reference = RepresentedSpinOperator(
            "wrong_energy_reference",
            wrong_reference_basis,
            degenerate.matrix,
        )
        cases = (
            ("spinless-versus-spinful", spinless, degenerate),
            ("unaligned-block-order", orbital_major, spin_major),
            ("different-energy-reference", degenerate, wrong_reference),
        )
        records: list[JsonValue] = []
        for identifier, reference, candidate in cases:
            result = self._differencer.execute(reference, candidate)
            records.append(
                {
                    "id": identifier,
                    "status": result.status,
                    "issue_codes": list(result.issue_codes),
                    "frobenius_norm": result.frobenius_norm,
                }
            )
        return records

    def _scalar_model_record(
        self,
        identifier: str,
        matrix: ComplexMatrix,
        expected_scalar: ComplexMatrix,
        expected_residual: float,
    ) -> dict[str, JsonValue]:
        dimension = expected_scalar.shape[0]
        reshaped = matrix.reshape(dimension, 2, dimension, 2)
        fitted = 0.5 * (reshaped[:, 0, :, 0] + reshaped[:, 1, :, 1])
        represented = np.kron(fitted, np.eye(2, dtype=np.complex128))
        residual = self._norm(matrix - represented)
        scale = self._norm(matrix)
        return {
            "id": identifier,
            "fitted_orbital_operator_frobenius_defect": self._norm(
                fitted - expected_scalar
            ),
            "absolute_frobenius_residual": residual,
            "expected_absolute_frobenius_residual": expected_residual,
            "analytic_residual_absolute_defect": abs(residual - expected_residual),
            "relative_frobenius_residual": residual / scale,
            "rms_per_state_residual": residual / np.sqrt(matrix.shape[0]),
        }

    @staticmethod
    def _operator_json(record: RepresentedSpinOperator) -> dict[str, JsonValue]:
        basis = record.basis
        return {
            "identifier": record.identifier,
            "state_space_id": basis.state_space_id,
            "dimension": basis.dimension,
            "orbital_labels": list(basis.orbital_labels),
            "spin_representation": basis.spin_representation,
            "basis_ordering": basis.basis_ordering,
            "spin_frame_id": basis.spin_frame_id,
            "energy_unit": basis.energy_unit,
            "energy_reference": basis.energy_reference,
            "geometry": basis.geometry,
            "matrix": SpinSpaceEmbeddingExperiment._complex_matrix_json(
                np.asarray(record.matrix, dtype=np.complex128)
            ),
        }

    @staticmethod
    def _record(
        identifier: str, basis: SpinBasis, matrix: ComplexMatrix
    ) -> RepresentedSpinOperator:
        immutable = tuple(
            tuple(complex(value) for value in row)
            for row in np.asarray(matrix, dtype=np.complex128)
        )
        return RepresentedSpinOperator(identifier, basis, immutable)

    @staticmethod
    def _complex_matrix_json(matrix: ComplexMatrix) -> list[JsonValue]:
        return [
            [[float(value.real), float(value.imag)] for value in row] for row in matrix
        ]

    @staticmethod
    def _pauli() -> tuple[ComplexMatrix, ComplexMatrix, ComplexMatrix]:
        return (
            np.asarray([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128),
            np.asarray([[0.0, -1j], [1j, 0.0]], dtype=np.complex128),
            np.asarray([[1.0, 0.0], [0.0, -1.0]], dtype=np.complex128),
        )

    @staticmethod
    def _spin_major_permutation(dimension: int) -> ComplexMatrix:
        permutation = np.zeros((2 * dimension, 2 * dimension), dtype=np.complex128)
        for orbital in range(dimension):
            for spin in range(2):
                orbital_major = 2 * orbital + spin
                spin_major = spin * dimension + orbital
                permutation[orbital_major, spin_major] = 1.0
        return permutation

    @staticmethod
    def _time_reversal_residual(
        matrix: ComplexMatrix, unitary_part: ComplexMatrix
    ) -> float:
        transformed = unitary_part @ matrix.conj() @ unitary_part.conj().T
        return float(np.linalg.norm(transformed - matrix))

    @staticmethod
    def _hermiticity_residual(matrix: ComplexMatrix) -> float:
        return float(np.max(np.abs(matrix - matrix.conj().T)))

    @staticmethod
    def _eigenvalue_defect(first: ComplexMatrix, second: ComplexMatrix) -> float:
        return float(
            np.max(np.abs(np.linalg.eigvalsh(first) - np.linalg.eigvalsh(second)))
        )

    @staticmethod
    def _norm(matrix: ComplexMatrix) -> float:
        return float(np.linalg.norm(matrix))

    @staticmethod
    def _require_hermitian(matrix: ComplexMatrix, name: str) -> None:
        if not np.allclose(matrix, matrix.conj().T, rtol=0.0, atol=1.0e-14):
            raise ValueError(f"{name} must be Hermitian")

    @staticmethod
    def _sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    """Adapt command-line paths into the owned experiment action."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    input_path = arguments.input.resolve()
    output_path = arguments.output.resolve()
    specification = SpinSpaceInputDeserializer().execute(input_path.read_bytes())
    output_path.write_bytes(
        SpinSpaceEmbeddingExperiment().execute(
            specification, input_path, Path(__file__).resolve()
        )
    )


if __name__ == "__main__":
    main()
