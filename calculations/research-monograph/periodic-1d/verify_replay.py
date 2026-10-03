#!/usr/bin/env python3
"""Verify retained periodic-1D replay artifacts without rerunning the producer."""

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
type ComplexVector = npt.NDArray[np.complex128]
type ComplexMatrix = npt.NDArray[np.complex128]


class Periodic1DIsolatedBandReplayVerifier:
    """Authenticate and verify one retained replay-artifact document."""

    __slots__ = ()

    def execute(
        self,
        *,
        input_path: Path,
        reference_result_path: Path,
        artifact_path: Path,
    ) -> None:
        """Raise when source correlation or reconstructable artifact checks fail."""
        input_payload = input_path.read_bytes()
        result_payload = reference_result_path.read_bytes()
        artifact = self._mapping(
            cast(JsonValue, json.loads(artifact_path.read_text())), "artifact"
        )
        if self._integer(artifact["schema_version"], "schema_version") != 1:
            raise ValueError("unsupported replay-artifact schema version")
        if artifact["artifact_kind"] != ("periodic-1d-isolated-band-replay-artifacts"):
            raise ValueError("unsupported replay-artifact kind")

        source = self._mapping(artifact["source_correlation"], "source_correlation")
        self._require_hash(
            input_payload, source["input_sha256"], "input source correlation"
        )
        self._require_hash(
            result_payload,
            source["reference_result_sha256"],
            "result source correlation",
        )
        if source["replayed_result_sha256"] != source["reference_result_sha256"]:
            raise ValueError("replayed and reference result identities differ")
        if source["exact_result_bytes_match"] is not True:
            raise ValueError("artifact does not claim exact replay-result agreement")
        repository_root = artifact_path.resolve().parents[5]
        for path_name, digest_name in (
            ("producer_script_path", "producer_script_sha256"),
            ("replay_script_path", "replay_script_sha256"),
        ):
            correlated_path = repository_root / self._string(
                source[path_name], path_name
            )
            self._require_hash(
                correlated_path.read_bytes(), source[digest_name], path_name
            )

        result = self._mapping(
            cast(JsonValue, json.loads(result_payload.decode("utf-8"))), "result"
        )
        if artifact["experiment_id"] != result["experiment_id"]:
            raise ValueError("artifact and result experiment identities differ")
        reduction = self._mapping(
            result["isolated_band_reduction"], "isolated_band_reduction"
        )
        convention = self._mapping(
            result["dimensionless_convention"], "dimensionless_convention"
        )
        retained = self._mapping(
            artifact["retained_space_representation"],
            "retained_space_representation",
        )
        effective = self._mapping(
            artifact["effective_model_artifacts"], "effective_model_artifacts"
        )
        self._verify_frame(retained)
        self._verify_effective_models(reduction, convention, effective)

    def _verify_frame(self, retained: dict[str, JsonValue]) -> None:
        shape = self._integers(retained["frame_shape"], "frame_shape")
        if len(shape) != 3 or shape[2] != 1:
            raise ValueError("frame_shape must identify a scalar band-frame path")
        rows = self._array(retained["parallel_transport_frame"], "frame")
        if len(rows) != shape[0]:
            raise ValueError("frame row count does not match frame_shape")
        frame = np.asarray(
            [self._complex_vector(row, "frame row") for row in rows],
            dtype=np.complex128,
        )
        if frame.shape != (shape[0], shape[1]):
            raise ValueError("retained frame values do not match frame_shape")
        norms = np.sum(np.square(np.abs(frame)), axis=1)
        orthonormality_absolute_tolerance = float(
            np.finfo(np.float64).eps * frame.shape[1]
        )
        if float(np.max(np.abs(norms - 1.0))) > orthonormality_absolute_tolerance:
            raise ValueError("retained frame exceeds the binary64 roundoff bound")
        self._require_array_hash(frame, retained["frame_content_sha256"], "frame")
        projectors = np.einsum("ki,kj->kij", frame, frame.conj(), optimize=True)
        self._require_array_hash(
            projectors,
            retained["projector_path_content_sha256"],
            "projector path",
        )

    def _verify_effective_models(
        self,
        reduction: dict[str, JsonValue],
        convention: dict[str, JsonValue],
        effective: dict[str, JsonValue],
    ) -> None:
        representatives = np.asarray(
            self._integers(
                effective["complete_representatives_cells"],
                "complete_representatives_cells",
            ),
            dtype=np.int64,
        )
        complete = self._complex_vector(
            effective["complete_coefficients"], "complete_coefficients"
        )
        self._require_array_hash(
            complete,
            effective["complete_coefficients_content_sha256"],
            "complete coefficients",
        )
        retained_complete = self._complex_vector(
            reduction["hopping_coefficients"], "retained hopping_coefficients"
        )
        if not np.array_equal(complete, retained_complete):
            raise ValueError("complete replay coefficients differ from retained result")
        retained_representatives = np.asarray(
            self._integers(
                reduction["hopping_representatives_cells"],
                "hopping_representatives_cells",
            ),
            dtype=np.int64,
        )
        if not np.array_equal(representatives, retained_representatives):
            raise ValueError("complete representatives differ from retained result")

        momenta = np.asarray(
            self._reals(reduction["reciprocal_mesh"], "reciprocal_mesh")
        )
        energies = np.asarray(
            self._reals(reduction["lowest_band_energies"], "lowest_band_energies")
        )
        period = self._real(convention["lattice_period"], "lattice_period")
        complete_design = np.exp(1j * np.outer(momenta, representatives * period))
        reconstructed = complete_design @ complete
        maximum_error = float(np.max(np.abs(reconstructed.real - energies)))
        if maximum_error != self._real(
            reduction["full_mesh_reconstruction_maximum_absolute_error"],
            "full_mesh_reconstruction_maximum_absolute_error",
        ):
            raise ValueError("complete reconstruction diagnostic differs")

        diagnostics = {
            self._integer(item["hopping_range_cells"], "hopping_range_cells"): item
            for item in self._objects(
                reduction["hopping_range_study"], "hopping_range_study"
            )
        }
        artifacts = self._objects(effective["range_artifacts"], "range_artifacts")
        if len(artifacts) != len(diagnostics):
            raise ValueError("effective-model range inventory differs")
        for value in artifacts:
            hopping_range = self._integer(
                value["hopping_range_cells"], "hopping_range_cells"
            )
            diagnostic = diagnostics.get(hopping_range)
            if diagnostic is None:
                raise ValueError("effective-model range has no retained diagnostic")
            range_representatives = np.asarray(
                self._integers(value["representatives_cells"], "representatives_cells"),
                dtype=np.int64,
            )
            expected_representatives = representatives[
                np.abs(representatives) <= hopping_range
            ]
            if not np.array_equal(range_representatives, expected_representatives):
                raise ValueError("range representatives do not match truncation")
            truncated = self._complex_vector(
                value["truncated_coefficients"], "truncated_coefficients"
            )
            fitted = self._complex_vector(
                value["fitted_coefficients"], "fitted_coefficients"
            )
            self._require_array_hash(
                truncated,
                value["truncated_coefficients_content_sha256"],
                "truncated coefficients",
            )
            self._require_array_hash(
                fitted,
                value["fitted_coefficients_content_sha256"],
                "fitted coefficients",
            )
            expected_truncated = complete[np.abs(representatives) <= hopping_range]
            if not np.array_equal(truncated, expected_truncated):
                raise ValueError("truncated coefficients differ from complete source")
            design = np.exp(1j * np.outer(momenta, range_representatives * period))
            independently_fitted = cast(
                ComplexVector, np.linalg.lstsq(design, energies, rcond=None)[0]
            )
            if not np.array_equal(fitted, independently_fitted):
                raise ValueError("fitted coefficients differ from independent fit")
            coefficient_defect = float(np.linalg.norm(fitted - truncated))
            if coefficient_defect != self._real(
                diagnostic["direct_mediated_coefficient_l2_defect"],
                "direct_mediated_coefficient_l2_defect",
            ):
                raise ValueError("direct/mediated coefficient diagnostic differs")

    @staticmethod
    def _require_hash(payload: bytes, claimed: JsonValue, owner: str) -> None:
        if claimed != hashlib.sha256(payload).hexdigest():
            raise ValueError(f"{owner} SHA-256 differs")

    @staticmethod
    def _require_array_hash(
        values: npt.NDArray[np.generic], claimed: JsonValue, owner: str
    ) -> None:
        canonical = np.asarray(values, dtype="<c16", order="C")
        digest = hashlib.sha256(canonical.tobytes(order="C")).hexdigest()
        if claimed != digest:
            raise ValueError(f"{owner} content SHA-256 differs")

    @staticmethod
    def _mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be a JSON object")
        return value

    def _objects(self, value: JsonValue, name: str) -> tuple[dict[str, JsonValue], ...]:
        return tuple(self._mapping(item, name) for item in self._array(value, name))

    @staticmethod
    def _array(value: JsonValue, name: str) -> list[JsonValue]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return value

    def _complex_vector(self, value: JsonValue, name: str) -> ComplexVector:
        rows = self._array(value, name)
        pairs = tuple(self._reals(row, name) for row in rows)
        if any(len(pair) != 2 for pair in pairs):
            raise ValueError(f"{name} values must contain real/imaginary pairs")
        return np.asarray(
            [complex(pair[0], pair[1]) for pair in pairs], dtype=np.complex128
        )

    def _reals(self, value: JsonValue, name: str) -> tuple[float, ...]:
        return tuple(self._real(item, name) for item in self._array(value, name))

    def _integers(self, value: JsonValue, name: str) -> tuple[int, ...]:
        return tuple(self._integer(item, name) for item in self._array(value, name))

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


class CommandAdapter:
    """Adapt explicit local paths to replay-artifact verification."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("--input", type=Path, required=True)
        parser.add_argument("--reference-result", type=Path, required=True)
        parser.add_argument("--artifact", type=Path, required=True)
        arguments = parser.parse_args(argv)
        Periodic1DIsolatedBandReplayVerifier().execute(
            input_path=cast(Path, arguments.input).resolve(),
            reference_result_path=cast(Path, arguments.reference_result).resolve(),
            artifact_path=cast(Path, arguments.artifact).resolve(),
        )
        print("periodic-1d isolated-band replay artifacts: PASS")
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
