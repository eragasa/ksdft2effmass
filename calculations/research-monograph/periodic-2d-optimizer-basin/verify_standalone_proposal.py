#!/usr/bin/env python3
"""Verify the proposed standalone-study design without executing it."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type ComplexMatrix = npt.NDArray[np.complex128]


class StandaloneProposalVerifier:
    """Verify configuration, start-design, count, and nonauthorization contracts."""

    __slots__ = ()

    _generators = (
        "x01",
        "y01",
        "x02",
        "y02",
        "x12",
        "y12",
        "diag01",
        "diag012",
    )
    _harmonics = (
        (1, 0),
        (0, 1),
        (1, 1),
        (1, -1),
        (2, 1),
        (1, 2),
        (2, -1),
        (3, 1),
    )
    _bases = ((2, 3, 5, 7), (11, 13, 17, 19), (23, 29, 31, 37))

    def execute(self, proposal_path: Path, starts_path: Path) -> None:
        proposal = self._load(proposal_path)
        starts = self._load(starts_path)
        if proposal["evidence_status"] != "proposed work; not authorized for execution":
            raise AssertionError("proposal must remain explicitly unauthorized")
        configurations = [
            self._mapping(value)
            for value in self._array(proposal["baseline_configurations"])
        ]
        if len(configurations) != 14:
            raise AssertionError("proposal must contain 14 unique interfaces")
        identifiers = [
            self._string(value["configuration_id"]) for value in configurations
        ]
        if len(set(identifiers)) != len(identifiers):
            raise AssertionError("configuration identities must be unique")
        physical = [
            (
                self._integer(value["plane_wave_cutoff"]),
                self._integer(value["reciprocal_mesh_size"]),
                self._real(value["transverse_lattice_length"]),
            )
            for value in configurations
        ]
        if len(set(physical)) != len(physical):
            raise AssertionError("physical interfaces must be unique")
        self._verify_axes(configurations)
        self._verify_counts(proposal)
        expected_proposal = hashlib.sha256(proposal_path.read_bytes()).hexdigest()
        if starts["proposal_sha256"] != expected_proposal:
            raise AssertionError("generated start table does not match proposal")
        records = [self._mapping(value) for value in self._array(starts["starts"])]
        if len(records) != 16 or self._integer(starts["start_count"]) != 16:
            raise AssertionError("start table must contain exactly 16 starts")
        if records[0]["start_id"] != "identity" or records[0]["ordered_terms"] != []:
            raise AssertionError("first start must be identity")
        for index, record in enumerate(records[1:], start=1):
            self._verify_start(index, record)
        defect = self._unitarity_defect(records, 31)
        self._close(
            defect,
            self._real(starts["maximum_unitarity_frobenius_defect"]),
            1.0e-18,
            "maximum unitarity defect",
        )
        if defect > 1.0e-12:
            raise AssertionError("unitarity defect exceeds proposal tolerance")

    def _verify_axes(self, configurations: list[dict[str, JsonValue]]) -> None:
        fixed = sorted(
            self._integer(value["reciprocal_mesh_size"])
            for value in configurations
            if "fixed_embedding_mesh" in self._strings(value["axes"])
        )
        balanced = sorted(
            self._integer(value["reciprocal_mesh_size"])
            for value in configurations
            if "balanced_embedding_mesh" in self._strings(value["axes"])
        )
        cutoff = sorted(
            self._integer(value["plane_wave_cutoff"])
            for value in configurations
            if "cutoff" in self._strings(value["axes"])
            or "cutoff_reference" in self._strings(value["axes"])
        )
        if fixed != [11, 15, 19, 23, 27, 31]:
            raise AssertionError("fixed-embedding mesh sequence disagrees")
        if balanced != [11, 15, 19, 23, 27, 31]:
            raise AssertionError("balanced mesh sequence disagrees")
        if cutoff != [3, 4, 5, 6]:
            raise AssertionError("cutoff sequence disagrees")

    def _verify_counts(self, proposal: dict[str, JsonValue]) -> None:
        counts = self._mapping(proposal["maximum_execution_counts"])
        self._equal(self._integer(counts["unique_interfaces"]), 14, "interfaces")
        self._equal(
            self._integer(counts["baseline_localizations"]), 14 * 16, "baseline"
        )
        self._equal(
            self._integer(counts["optimizer_control_localizations"]),
            2 * 16,
            "controls",
        )
        self._equal(
            self._integer(counts["maximum_conditional_continuations"]),
            14 * 16 + 2 * 16,
            "continuations",
        )
        self._equal(
            self._integer(counts["maximum_localization_stages"]),
            2 * (14 * 16 + 2 * 16),
            "maximum stages",
        )

    def _verify_start(self, index: int, record: dict[str, JsonValue]) -> None:
        if record["start_id"] != f"halton_{index:02d}":
            raise AssertionError("Halton start identity disagrees")
        self._equal(self._integer(record["halton_index"]), index, "Halton index")
        terms = [self._mapping(value) for value in self._array(record["ordered_terms"])]
        if len(terms) != 3:
            raise AssertionError("each Halton start must contain three terms")
        for term_index, (term, bases) in enumerate(
            zip(terms, self._bases, strict=True)
        ):
            coordinates = tuple(self._radical_inverse(index, base) for base in bases)
            if term["generator"] != self._generators[min(int(coordinates[0] * 8), 7)]:
                raise AssertionError("generator category disagrees")
            harmonic = self._integers(term["harmonic"])
            if harmonic != self._harmonics[min(int(coordinates[1] * 8), 7)]:
                raise AssertionError("harmonic category disagrees")
            self._close(
                self._real(term["amplitude"]),
                0.25 + 2.25 * coordinates[2],
                0.0,
                "amplitude",
            )
            self._close(
                self._real(term["phase_radians"]),
                2.0 * math.pi * coordinates[3],
                0.0,
                "phase",
            )
            self._equal(self._integer(term["term_index"]), term_index, "term index")

    def _unitarity_defect(
        self, records: list[dict[str, JsonValue]], mesh_size: int
    ) -> float:
        maximum = 0.0
        for record in records:
            terms = [
                self._mapping(value) for value in self._array(record["ordered_terms"])
            ]
            for ix in range(mesh_size):
                for iy in range(mesh_size):
                    unitary = np.eye(3, dtype=complex)
                    for term in terms:
                        harmonic = self._integers(term["harmonic"])
                        angle = self._real(term["amplitude"]) * math.sin(
                            2.0
                            * math.pi
                            * (
                                harmonic[0] * ix / mesh_size
                                + harmonic[1] * iy / mesh_size
                            )
                            + self._real(term["phase_radians"])
                        )
                        generator = self._generator(self._string(term["generator"]))
                        eigenvalues, eigenvectors = np.linalg.eigh(generator)
                        unitary = (
                            unitary
                            @ (eigenvectors * np.exp(1j * angle * eigenvalues)[None, :])
                            @ eigenvectors.conj().T
                        )
                    maximum = max(
                        maximum,
                        float(np.linalg.norm(unitary.conj().T @ unitary - np.eye(3))),
                    )
        return maximum

    @staticmethod
    def _generator(name: str) -> ComplexMatrix:
        matrix = np.zeros((3, 3), dtype=complex)
        if name in {"x01", "y01", "x02", "y02", "x12", "y12"}:
            first = int(name[1])
            second = int(name[2])
            matrix[first, second] = 1.0 if name[0] == "x" else -1j
            matrix[second, first] = 1.0 if name[0] == "x" else 1j
            return matrix
        if name == "diag01":
            return np.diag([1.0, -1.0, 0.0]).astype(complex) / math.sqrt(2.0)
        if name == "diag012":
            return np.diag([1.0, 1.0, -2.0]).astype(complex) / math.sqrt(6.0)
        raise ValueError(f"unsupported generator {name}")

    @staticmethod
    def _radical_inverse(index: int, base: int) -> float:
        value = 0.0
        factor = 1.0 / base
        current = index
        while current:
            value += factor * (current % base)
            current //= base
            factor /= base
        return value

    @staticmethod
    def _equal(actual: int, expected: int, label: str) -> None:
        if actual != expected:
            raise AssertionError(f"{label}: actual={actual}, expected={expected}")

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

    def _integers(self, value: JsonValue) -> tuple[int, ...]:
        return tuple(self._integer(item) for item in self._array(value))

    def _strings(self, value: JsonValue) -> tuple[str, ...]:
        return tuple(self._string(item) for item in self._array(value))


class CommandAdapter:
    """Adapt proposal and start-table paths to the static verifier."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("--proposal", type=Path, required=True)
        parser.add_argument("--starts", type=Path, required=True)
        arguments = parser.parse_args(argv)
        StandaloneProposalVerifier().execute(
            cast(Path, arguments.proposal).resolve(),
            cast(Path, arguments.starts).resolve(),
        )
        print("periodic_2d_standalone_proposal_verification=PASS")
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
