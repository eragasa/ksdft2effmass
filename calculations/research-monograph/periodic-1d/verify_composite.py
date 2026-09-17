#!/usr/bin/env python3
"""Independently verify the retained direct composite-band result."""

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
type ComplexArray3 = npt.NDArray[np.complex128]


class CompositeResultVerifier:
    """Verify stored composite operators and declared covariance diagnostics."""

    __slots__ = ()

    def execute(self, result_path: Path) -> None:
        root = self._mapping(
            cast(JsonValue, json.loads(result_path.read_text(encoding="utf-8")))
        )
        if root["schema_version"] != 1:
            raise ValueError("unexpected composite result schema version")
        if root["evidence_status"] != "illustrative numerical verification":
            raise ValueError("unexpected composite evidence status")
        provenance = self._mapping(root["provenance"])
        repository_root = result_path.parents[3]
        self._verify_provenance(repository_root, provenance)
        input_path = repository_root / self._string(provenance["input_path"])
        input_root = self._mapping(
            cast(JsonValue, json.loads(input_path.read_text(encoding="utf-8")))
        )
        mesh_size = self._integer(input_root["reciprocal_mesh_size"])
        period = self._real(input_root["period"])
        groups = self._records(root["groups"])
        if {self._string(group["id"]) for group in groups} != {
            "low_pair",
            "higher_pair",
        }:
            raise ValueError("unexpected composite band groups")
        for group in groups:
            self._verify_group(group, mesh_size, period)

    def _verify_provenance(
        self, repository_root: Path, provenance: dict[str, JsonValue]
    ) -> None:
        for prefix in ("input", "script"):
            relative_path = self._string(provenance[f"{prefix}_path"])
            expected = self._string(provenance[f"{prefix}_sha256"])
            observed = hashlib.sha256(
                (repository_root / relative_path).read_bytes()
            ).hexdigest()
            if observed != expected:
                raise ValueError(f"{prefix} identity mismatch")

    def _verify_group(
        self, group: dict[str, JsonValue], mesh_size: int, period: float
    ) -> None:
        identifier = self._string(group["id"])
        if group["external_isolation_status"] != "pass":
            raise ValueError(f"{identifier}: retained subspace is not isolated")
        if self._real(group["external_minimum_gap"]) <= 1.0e-8:
            raise ValueError(f"{identifier}: external gap is below threshold")
        if self._real(group["neighbor_overlap_minimum_singular_value"]) <= 0.7:
            raise ValueError(f"{identifier}: neighboring subspace overlap is singular")
        small_diagnostics = (
            "controlled_gauge_wilson_phase_set_defect",
            "controlled_gauge_projector_maximum_frobenius_defect",
            "pointwise_alignment_frame_maximum_frobenius_defect",
            "pointwise_alignment_operator_maximum_frobenius_defect",
            "controlled_gauge_eigenvalue_maximum_defect",
            "smooth_full_reconstruction_maximum_frobenius_error",
            "rough_full_reconstruction_maximum_frobenius_error",
            "smooth_hopping_hermiticity_maximum_frobenius_residual",
        )
        for key in small_diagnostics:
            if self._real(group[key]) > 1.0e-11:
                raise ValueError(f"{identifier}: diagnostic {key} exceeds tolerance")
        if self._real(group["rough_vs_smooth_unaligned_hopping_l2_defect"]) <= 0.1:
            raise ValueError(f"{identifier}: rough-gauge attack was ineffective")
        direct = self._mapping(group["direct_route"])
        if self._real(direct["coefficient_frobenius_defect"]) > 1.0e-11:
            raise ValueError(f"{identifier}: direct coefficient route disagrees")
        if self._real(direct["training_operator_maximum_frobenius_defect"]) > 1.0e-11:
            raise ValueError(f"{identifier}: direct operator route disagrees")

        hamiltonians = self._complex_array(
            group["represented_reciprocal_hamiltonians"]
        )
        smooth_representatives, smooth_hoppings = self._hoppings(
            group["smooth_hopping_blocks"]
        )
        rough_representatives, rough_hoppings = self._hoppings(
            group["rough_hopping_blocks"]
        )
        if hamiltonians.shape != (mesh_size, 2, 2):
            raise ValueError(f"{identifier}: unexpected Hamiltonian shape")
        expected_representatives = np.arange(-mesh_size // 2, mesh_size // 2)
        if not np.array_equal(smooth_representatives, expected_representatives):
            raise ValueError(f"{identifier}: smooth representative order mismatch")
        if not np.array_equal(rough_representatives, expected_representatives):
            raise ValueError(f"{identifier}: rough representative order mismatch")
        momenta = -0.5 + np.arange(mesh_size, dtype=np.float64) / mesh_size
        transform = np.exp(
            -1j * np.outer(smooth_representatives * period, momenta)
        ) / mesh_size
        recomputed_hoppings = np.einsum(
            "rk,kij->rij", transform, hamiltonians, optimize=True
        )
        if np.max(np.abs(recomputed_hoppings - smooth_hoppings)) > 1.0e-12:
            raise ValueError(f"{identifier}: stored hopping transform mismatch")
        inverse = np.exp(
            1j * np.outer(momenta, smooth_representatives * period)
        )
        reconstructed = np.einsum(
            "kr,rij->kij", inverse, smooth_hoppings, optimize=True
        )
        if np.max(np.abs(reconstructed - hamiltonians)) > 1.0e-11:
            raise ValueError(f"{identifier}: stored inverse transform mismatch")
        identities = self._mapping(group["identities"])
        self._verify_identity(
            hamiltonians,
            self._string(identities["smooth_reciprocal_hamiltonian_sha256"]),
            f"{identifier} reciprocal Hamiltonian",
        )
        self._verify_identity(
            smooth_hoppings,
            self._string(identities["smooth_hopping_sha256"]),
            f"{identifier} smooth hoppings",
        )
        self._verify_identity(
            rough_hoppings,
            self._string(identities["rough_hopping_sha256"]),
            f"{identifier} rough hoppings",
        )
        self._verify_ranges(identifier, self._records(group["range_study"]))

    def _verify_ranges(
        self, identifier: str, records: tuple[dict[str, JsonValue], ...]
    ) -> None:
        ranges = [self._integer(record["hopping_range_cells"]) for record in records]
        if ranges != [0, 1, 2, 3, 4, 6, 8, 12]:
            raise ValueError(f"{identifier}: unexpected hopping hierarchy")
        smooth_omitted = [
            self._real(record["smooth_omitted_block_l2_norm"])
            for record in records
        ]
        smooth_errors = [
            self._real(record["smooth_withheld_eigenvalue_maximum_error"])
            for record in records
        ]
        if any(
            later >= earlier
            for earlier, later in zip(
                smooth_omitted, smooth_omitted[1:], strict=False
            )
        ):
            raise ValueError(f"{identifier}: smooth omitted norm is not decreasing")
        if any(
            later >= earlier
            for earlier, later in zip(smooth_errors, smooth_errors[1:], strict=False)
        ):
            raise ValueError(f"{identifier}: smooth withheld error is not decreasing")
        final = records[-1]
        if self._real(final["rough_omitted_block_l2_norm"]) <= 100.0 * self._real(
            final["smooth_omitted_block_l2_norm"]
        ):
            raise ValueError(f"{identifier}: rough gauge did not degrade locality")
        if self._real(
            final["rough_withheld_eigenvalue_maximum_error"]
        ) <= 5.0 * self._real(final["smooth_withheld_eigenvalue_maximum_error"]):
            raise ValueError(f"{identifier}: rough gauge did not degrade reduction")

    def _hoppings(
        self, value: JsonValue
    ) -> tuple[npt.NDArray[np.int64], ComplexArray3]:
        records = self._records(value)
        representatives = np.asarray(
            [self._integer(record["representative_cells"]) for record in records],
            dtype=np.int64,
        )
        matrices = np.asarray(
            [self._complex_matrix(record["matrix"]) for record in records],
            dtype=np.complex128,
        )
        return representatives, matrices

    def _complex_array(self, value: JsonValue) -> ComplexArray3:
        entries = self._array(value)
        return np.asarray(
            [self._complex_matrix(entry) for entry in entries],
            dtype=np.complex128,
        )

    def _complex_matrix(self, value: JsonValue) -> ComplexMatrix:
        rows = self._array(value)
        matrix: list[list[complex]] = []
        for row_value in rows:
            row = self._array(row_value)
            matrix.append([self._complex(entry) for entry in row])
        return np.asarray(matrix, dtype=np.complex128)

    def _complex(self, value: JsonValue) -> complex:
        pair = self._array(value)
        if len(pair) != 2:
            raise TypeError("complex value must contain real and imaginary parts")
        return complex(self._real(pair[0]), self._real(pair[1]))

    @staticmethod
    def _verify_identity(
        values: npt.NDArray[np.complex128], expected: str, label: str
    ) -> None:
        canonical = np.ascontiguousarray(values, dtype="<c16")
        observed = hashlib.sha256(canonical.tobytes(order="C")).hexdigest()
        if observed != expected:
            raise ValueError(f"{label} identity mismatch")

    @staticmethod
    def _mapping(value: JsonValue) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError("expected JSON object")
        return value

    @staticmethod
    def _records(value: JsonValue) -> tuple[dict[str, JsonValue], ...]:
        if not isinstance(value, list):
            raise TypeError("expected JSON array")
        records: list[dict[str, JsonValue]] = []
        for item in value:
            if not isinstance(item, dict):
                raise TypeError("expected JSON object entry")
            records.append(item)
        return tuple(records)

    @staticmethod
    def _array(value: JsonValue) -> list[JsonValue]:
        if not isinstance(value, list):
            raise TypeError("expected JSON array")
        return value

    @staticmethod
    def _string(value: JsonValue) -> str:
        if not isinstance(value, str):
            raise TypeError("expected string")
        return value

    @staticmethod
    def _real(value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("expected number")
        return float(value)

    @staticmethod
    def _integer(value: JsonValue) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("expected integer")
        return value


class CommandAdapter:
    """Adapt one result path to the independent verifier."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("result", type=Path)
        args = parser.parse_args(argv)
        CompositeResultVerifier().execute(cast(Path, args.result).resolve())
        print("periodic-1d direct composite-band result: PASS")
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
