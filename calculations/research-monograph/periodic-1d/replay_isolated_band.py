#!/usr/bin/env python3
"""Replay the frozen isolated-band calculation and retain missing compact artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt
import scipy  # type: ignore[import-untyped]
from run_experiment import (
    ExperimentInput,
    ExperimentInputDeserializer,
    PeriodicReductionExperiment,
)

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type ComplexVector = npt.NDArray[np.complex128]
type ComplexMatrix = npt.NDArray[np.complex128]


class Periodic1DIsolatedBandReplay:
    """Replay one frozen input without replacing its historical result bytes."""

    __slots__ = ()

    def execute(
        self,
        *,
        input_path: Path,
        reference_result_path: Path,
        output_path: Path,
    ) -> bytes:
        """Return deterministic replay artifacts after exact result-byte agreement."""
        input_payload = input_path.read_bytes()
        reference_payload = reference_result_path.read_bytes()
        experiment = ExperimentInputDeserializer().execute(input_payload)
        producer_path = Path(__file__).resolve().with_name("run_experiment.py")
        replayed_payload = PeriodicReductionExperiment().execute(
            experiment,
            input_path,
            producer_path,
        )
        if replayed_payload != reference_payload:
            raise ValueError(
                "replayed result bytes differ from the retained reference result"
            )

        artifacts = self._artifacts(experiment)
        payload: dict[str, JsonValue] = {
            "schema_version": 1,
            "artifact_kind": "periodic-1d-isolated-band-replay-artifacts",
            "experiment_id": experiment.experiment_id,
            "evidence_status": "deterministic replay of illustrative numerical experiment",
            "source_correlation": {
                "input_path": self._repository_path(input_path),
                "input_sha256": hashlib.sha256(input_payload).hexdigest(),
                "reference_result_path": self._repository_path(reference_result_path),
                "reference_result_sha256": hashlib.sha256(
                    reference_payload
                ).hexdigest(),
                "producer_script_path": self._repository_path(producer_path),
                "producer_script_sha256": hashlib.sha256(
                    producer_path.read_bytes()
                ).hexdigest(),
                "replay_script_path": self._repository_path(Path(__file__).resolve()),
                "replay_script_sha256": hashlib.sha256(
                    Path(__file__).read_bytes()
                ).hexdigest(),
                "replayed_result_sha256": hashlib.sha256(replayed_payload).hexdigest(),
                "exact_result_bytes_match": True,
            },
            "runtime": {
                "python_version": platform.python_version(),
                "numpy_version": np.__version__,
                "scipy_version": scipy.__version__,
                "floating_point": "IEEE-754 binary64",
            },
            "retained_space_representation": artifacts[0],
            "effective_model_artifacts": artifacts[1],
            "limitations": [
                (
                    "The retained frame represents the lowest isolated band in the "
                    "finite plane-wave basis; it does not define a different "
                    "scientific subspace under gauge changes."
                ),
                (
                    "The projector-path digest authenticates projectors reconstructed "
                    "from the retained frame; the redundant dense projector path is "
                    "not stored."
                ),
                (
                    "Exact replay agreement establishes reproducibility of this "
                    "illustrative numerical experiment, not semiconductor validation, "
                    "uncertainty quantification, or scientific acceptance."
                ),
            ],
        }
        encoded = (
            json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
        ).encode("utf-8")
        if output_path.exists():
            existing = output_path.read_bytes()
            if existing != encoded:
                raise FileExistsError("replay output exists with different bytes")
            return existing
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(encoded)
        return encoded

    def _artifacts(
        self, experiment: ExperimentInput
    ) -> tuple[dict[str, JsonValue], dict[str, JsonValue]]:
        mesh_size = experiment.reciprocal_mesh_size
        momenta = -0.5 + np.arange(mesh_size, dtype=np.float64) / mesh_size
        cutoff = experiment.plane_wave_cutoffs[-1]
        energies = np.empty(mesh_size, dtype=np.float64)
        states = np.empty((mesh_size, 2 * cutoff + 1), dtype=np.complex128)
        calculation = PeriodicReductionExperiment()
        for index, momentum in enumerate(momenta):
            values, vectors = calculation._pw_eigensystem(
                float(momentum), experiment.potential_strength, cutoff
            )
            energies[index] = values[0]
            states[index] = vectors[:, 0]
        frame, _, _ = calculation._parallel_transport(states)
        projectors = np.einsum("ki,kj->kij", frame, frame.conj(), optimize=True)

        representatives = np.arange(-mesh_size // 2, mesh_size // 2, dtype=np.int64)
        phase = np.exp(
            -1j
            * np.outer(
                representatives * experiment.lattice_period,
                momenta,
            )
        )
        complete = cast(ComplexVector, phase @ energies / mesh_size)
        range_artifacts: list[JsonValue] = []
        for hopping_range in experiment.hopping_ranges:
            retained = np.abs(representatives) <= hopping_range
            retained_representatives = representatives[retained]
            design = np.exp(
                1j
                * np.outer(
                    momenta,
                    retained_representatives * experiment.lattice_period,
                )
            )
            fitted = cast(
                ComplexVector,
                np.linalg.lstsq(design, energies, rcond=None)[0],
            )
            truncated = complete[retained]
            range_artifacts.append(
                {
                    "hopping_range_cells": hopping_range,
                    "representatives_cells": cast(
                        list[JsonValue], retained_representatives.tolist()
                    ),
                    "truncated_coefficients": self._complex_vector(truncated),
                    "truncated_coefficients_content_sha256": self._array_sha256(
                        truncated
                    ),
                    "fitted_coefficients": self._complex_vector(fitted),
                    "fitted_coefficients_content_sha256": self._array_sha256(fitted),
                }
            )

        retained_space: dict[str, JsonValue] = {
            "reciprocal_mesh": cast(list[JsonValue], momenta.tolist()),
            "ambient_plane_wave_indices": cast(
                list[JsonValue], list(range(-cutoff, cutoff + 1))
            ),
            "frame_shape": [mesh_size, 2 * cutoff + 1, 1],
            "frame_encoding": (
                "nested [real, imaginary] IEEE-754 binary64 values in reciprocal-"
                "mesh then increasing-plane-wave-index order"
            ),
            "parallel_transport_frame": [
                self._complex_vector(cast(ComplexVector, row)) for row in frame
            ],
            "frame_content_sha256": self._array_sha256(frame),
            "projector_construction": "P(k) = u(k) u(k)^dagger",
            "projector_path_content_sha256": self._array_sha256(projectors),
            "reciprocal_boundary_sewing": (
                "finite-cutoff upper reciprocal-index shift used by run_experiment.py"
            ),
        }
        effective_models: dict[str, JsonValue] = {
            "complete_representatives_cells": cast(
                list[JsonValue], representatives.tolist()
            ),
            "complete_coefficients": self._complex_vector(complete),
            "complete_coefficients_content_sha256": self._array_sha256(complete),
            "range_artifacts": range_artifacts,
        }
        return retained_space, effective_models

    @staticmethod
    def _array_sha256(values: npt.NDArray[np.generic]) -> str:
        canonical = np.asarray(values, dtype="<c16", order="C")
        return hashlib.sha256(canonical.tobytes(order="C")).hexdigest()

    @staticmethod
    def _complex_vector(values: ComplexVector) -> list[JsonValue]:
        return [
            cast(list[JsonValue], [float(value.real), float(value.imag)])
            for value in values
        ]

    @staticmethod
    def _repository_path(path: Path) -> str:
        repository_root = Path(__file__).resolve().parents[3]
        return path.resolve().relative_to(repository_root).as_posix()


class CommandAdapter:
    """Adapt explicit local paths to one authorized deterministic replay."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("--input", type=Path, required=True)
        parser.add_argument("--reference-result", type=Path, required=True)
        parser.add_argument("--output", type=Path, required=True)
        arguments = parser.parse_args(argv)
        Periodic1DIsolatedBandReplay().execute(
            input_path=cast(Path, arguments.input).resolve(),
            reference_result_path=cast(Path, arguments.reference_result).resolve(),
            output_path=cast(Path, arguments.output).resolve(),
        )
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
