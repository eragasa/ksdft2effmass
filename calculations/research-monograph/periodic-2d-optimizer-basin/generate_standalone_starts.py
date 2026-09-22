#!/usr/bin/env python3
"""Generate the exact deterministic starts for the proposed standalone study."""

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


class StandaloneStartDesign:
    """Generate identity plus fifteen exact Halton-designed unitary fields."""

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

    def execute(self, proposal_path: Path, output_path: Path) -> dict[str, JsonValue]:
        proposal = cast(
            JsonValue, json.loads(proposal_path.read_text(encoding="utf-8"))
        )
        if not isinstance(proposal, dict):
            raise TypeError("proposal root must be an object")
        starts: list[JsonValue] = [
            {"start_id": "identity", "halton_index": 0, "ordered_terms": []}
        ]
        for index in range(1, 16):
            terms: list[JsonValue] = []
            for term_index, bases in enumerate(self._bases):
                generator_coordinate = self._radical_inverse(index, bases[0])
                harmonic_coordinate = self._radical_inverse(index, bases[1])
                amplitude_coordinate = self._radical_inverse(index, bases[2])
                phase_coordinate = self._radical_inverse(index, bases[3])
                terms.append(
                    {
                        "term_index": term_index,
                        "generator": self._generators[
                            min(int(generator_coordinate * 8), 7)
                        ],
                        "harmonic": list(
                            self._harmonics[min(int(harmonic_coordinate * 8), 7)]
                        ),
                        "amplitude": 0.25 + 2.25 * amplitude_coordinate,
                        "phase_radians": 2.0 * math.pi * phase_coordinate,
                        "halton_coordinates": {
                            "generator": generator_coordinate,
                            "harmonic": harmonic_coordinate,
                            "amplitude": amplitude_coordinate,
                            "phase": phase_coordinate,
                        },
                    }
                )
            starts.append(
                {
                    "start_id": f"halton_{index:02d}",
                    "halton_index": index,
                    "ordered_terms": terms,
                }
            )
        maximum_defect = self._maximum_unitarity_defect(starts, 31)
        if maximum_defect > 1.0e-12:
            raise AssertionError("generated start unitary defect exceeds tolerance")
        result: dict[str, JsonValue] = {
            "schema_version": 1,
            "design_id": "periodic-2d-standalone-halton-starts-v1",
            "evidence_status": "proposed deterministic initialization table",
            "proposal_path": proposal_path.name,
            "proposal_sha256": hashlib.sha256(proposal_path.read_bytes()).hexdigest(),
            "start_count": len(starts),
            "mesh_used_for_unitarity_check": 31,
            "maximum_unitarity_frobenius_defect": maximum_defect,
            "starts": starts,
            "claim_boundary": (
                "This deterministic low-discrepancy construction improves coverage "
                "but is not a probability distribution and does not establish "
                "exhaustive optimizer-basin discovery."
            ),
        }
        output_path.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        return result

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

    def _maximum_unitarity_defect(
        self, starts: list[JsonValue], mesh_size: int
    ) -> float:
        maximum = 0.0
        for start_value in starts:
            if not isinstance(start_value, dict):
                raise TypeError("start must be an object")
            terms = start_value["ordered_terms"]
            if not isinstance(terms, list):
                raise TypeError("ordered terms must be an array")
            for ix in range(mesh_size):
                for iy in range(mesh_size):
                    unitary = np.eye(3, dtype=complex)
                    for term_value in terms:
                        if not isinstance(term_value, dict):
                            raise TypeError("term must be an object")
                        harmonic = term_value["harmonic"]
                        if not isinstance(harmonic, list) or len(harmonic) != 2:
                            raise TypeError("harmonic must contain two integers")
                        mx = self._integer(harmonic[0])
                        my = self._integer(harmonic[1])
                        angle = self._real(term_value["amplitude"]) * math.sin(
                            2.0 * math.pi * (mx * ix / mesh_size + my * iy / mesh_size)
                            + self._real(term_value["phase_radians"])
                        )
                        generator = self._generator(
                            self._string(term_value["generator"])
                        )
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
    def _integer(value: JsonValue) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("expected an integer")
        return value

    @staticmethod
    def _real(value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("expected a real number")
        return float(value)

    @staticmethod
    def _string(value: JsonValue) -> str:
        if not isinstance(value, str):
            raise TypeError("expected a string")
        return value


class CommandAdapter:
    """Adapt proposal and output paths to the start-design action."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("--proposal", type=Path, required=True)
        parser.add_argument("--output", type=Path, required=True)
        arguments = parser.parse_args(argv)
        result = StandaloneStartDesign().execute(
            cast(Path, arguments.proposal).resolve(),
            cast(Path, arguments.output).resolve(),
        )
        print(
            json.dumps(
                {
                    "start_count": result["start_count"],
                    "maximum_unitarity_frobenius_defect": result[
                        "maximum_unitarity_frobenius_defect"
                    ],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
