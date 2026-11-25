"""Replay the retained window-remedy findings without a calculator or source change.

This calculation-local action authenticates the retained checkpoint and software,
then reuses its byte-bound numerical reference. Original exploratory entrypoints
are archived as evidence, not installed APIs or portable run commands.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import math
from dataclasses import dataclass
from fractions import Fraction
from importlib.metadata import version
from pathlib import Path

import numpy as np
from common_space.verification.gram_rank import _ExactMatrix
from common_space.verification.native_overlap import (
    CommonSpaceNativeOverlapReconstruction,
)
from common_space.verification.native_precision import CommonSpaceMatrixUncertainty
from projectkoios.integrations.wannier90 import (
    Wannier90DisentanglementMatrixParser,
    Wannier90EigenvalueParser,
    Wannier90TrialOrbitalOverlapParser,
)
from projectkoios.physkit.units import PhysicalUnit

type Json = None | bool | int | float | str | list[Json] | dict[str, Json]


def _object(value: Json) -> dict[str, Json]:
    if not isinstance(value, dict):
        raise ValueError("expected a JSON object")
    return value


def _string(value: Json) -> str:
    if type(value) is not str:
        raise ValueError("expected a JSON string")
    return value


def _load(path: Path) -> dict[str, Json]:
    value: Json = json.loads(path.read_bytes())
    return _object(value)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass(frozen=True, slots=True, kw_only=True)
class WindowRemedyReproduction:
    """Reproduce pointwise findings, not a candidate operator or an admission gate.

    All numerical settings are taken from authenticated records. Optional paths
    relocate explicitly named native inputs; their byte identities cannot change.
    No native parser, threshold, source association or missing weight is inferred.
    Scalar output bounds are floating displays of exact rational inequalities;
    they are not machine-readable outward-rounded interval certificates.
    """

    checkpoint: Path
    output_root: Path | None = None
    native_paths: tuple[tuple[str, Path], ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.checkpoint, Path) or (
            self.output_root is not None and not isinstance(self.output_root, Path)
        ):
            raise TypeError("checkpoint/output roots must be pathlib paths")
        if type(self.native_paths) is not tuple or any(
            type(item) is not tuple
            or len(item) != 2
            or type(item[0]) is not str
            or not isinstance(item[1], Path)
            for item in self.native_paths
        ):
            raise TypeError("native paths must be immutable named pathlib pairs")

    @staticmethod
    def _check_energy_membership(
        value: float, lower: Fraction, upper: Fraction
    ) -> None:
        native = Fraction.from_float(value)
        error = Fraction(1, 2 * 10**12) + Fraction.from_float(math.ulp(value)) / 2
        included = lower <= native <= upper
        if included and not (native - error >= lower and native + error <= upper):
            raise RuntimeError("energy-window membership is unresolved")
        if not included and not (native + error < lower or native - error > upper):
            raise RuntimeError("energy-window membership is unresolved")

    def inspect(self) -> dict[str, Json]:
        """Authenticate byte snapshots and their recorded identity relationships."""
        manifest = _load(self.checkpoint / "manifest.json")
        files = manifest["files"]
        if not isinstance(files, list):
            raise ValueError("checkpoint file inventory must be a list")
        seen: set[str] = set()
        for item in files:
            declaration = _object(item)
            name = _string(declaration["path"])
            relative = Path(name)
            if relative.is_absolute() or ".." in relative.parts or name in seen:
                raise ValueError("invalid or duplicate checkpoint path")
            seen.add(name)
            path = self.checkpoint / relative
            data = path.read_bytes()
            if type(declaration["byte_count"]) is not int:
                raise ValueError("checkpoint byte count must be an integer")
            if (
                len(data) != declaration["byte_count"]
                or _sha(path) != declaration["sha256"]
            ):
                raise ValueError(f"checkpoint identity mismatch: {name}")
        scripts = {
            "trial-subspace-diagnostic": "ksd-silicon-trial-subspace-diagnostic.py",
            "trial-whitening": "ksd_silicon_trial_whitening.py",
            "gamma-window": "ksd_silicon_gamma_window.py",
            "gamma-excluded-bands": "ksd_silicon_gamma_excluded_bands.py",
            "window-feasibility": "ksd_silicon_window_feasibility.py",
        }
        required = {
            *(f"results/{name}.json" for name in scripts),
            *(f"original_scripts/{name}" for name in scripts.values()),
            "inputs/request.json",
            "inputs/characterization-result.json",
            "inputs/spatial-truncation-disposition.json",
            "inputs/slater-koster-definition-fit-result.json",
            "inputs/protocol-at-diagnosis.tex",
        }
        if seen != required:
            raise ValueError(
                "checkpoint inventory differs from the fifteen bound artifacts"
            )
        request_path = self.checkpoint / "inputs/request.json"
        request = _load(request_path)
        for name, script in scripts.items():
            record = _load(self.checkpoint / f"results/{name}.json")
            if record["request_sha256"] != _sha(request_path):
                raise ValueError(f"request identity mismatch: {name}")
            if record["script_sha256"] != _sha(
                self.checkpoint / "original_scripts" / script
            ):
                raise ValueError(f"script identity mismatch: {name}")
        inputs = {
            "S30_untruncated_characterization": "characterization-result.json",
            "S105_full_support_disposition": "spatial-truncation-disposition.json",
            "S110_blocked_result": "slater-koster-definition-fit-result.json",
            "hopping_first_protocol": "protocol-at-diagnosis.tex",
        }
        sources = _object(request["sources"])
        for role, name in inputs.items():
            self._authenticate(
                self.checkpoint / "inputs" / name, _object(sources[role])
            )
        return request

    @staticmethod
    def _authenticate(path: Path, declaration: dict[str, Json]) -> bytes:
        payload = path.read_bytes()
        if type(declaration["byte_size"]) is not int:
            raise ValueError("source byte size must be an integer")
        if (
            len(payload) != declaration["byte_size"]
            or hashlib.sha256(payload).hexdigest() != declaration["sha256"]
        ):
            raise ValueError(f"source identity mismatch: {path.name}")
        return payload

    def execute(self) -> Path:
        """Recompute the key scalar findings in an exclusively created output root."""
        if self.output_root is None:
            raise ValueError("an output root is required for numerical replay")
        if self.output_root.exists() or self.output_root.is_symlink():
            raise FileExistsError("output root must not already exist")
        request = self.inspect()
        reference = _load(self.checkpoint / "results/trial-whitening.json")
        provider = _object(request["provider"])
        if version(_string(provider["distribution"])) != provider["version"]:
            raise ValueError("provider distribution version differs")
        for name, expected in _object(reference["module_sha256"]).items():
            module = importlib.import_module(name)
            if module.__file__ is None or _sha(Path(module.__file__)) != expected:
                raise ValueError(f"numerical module identity mismatch: {name}")
        # The archive is an explicit, hash-checked numerical reference, not a
        # replacement provider or a fallback implementation.
        from original_scripts.ksd_silicon_trial_whitening import (
            exact,
            minimum_bounds,
            sanity_checks,
        )

        sanity_checks()
        sources = _object(request["sources"])
        declarations = {
            role: _object(sources[role]) for role in ("AMN", "disentanglement", "gauge")
        }
        window_record = _load(self.checkpoint / "results/gamma-window.json")
        declarations["eig"] = _object(window_record["eig_identity"])
        paths = dict(self.native_paths)
        if len(paths) != len(self.native_paths) or set(paths) - set(declarations):
            raise ValueError("invalid or duplicate native path role")
        payloads = {
            role: self._authenticate(
                paths.get(role, Path(_string(declaration["path"]))), declaration
            )
            for role, declaration in declarations.items()
        }
        amn = Wannier90TrialOrbitalOverlapParser(payload=payloads["AMN"]).parse()
        dis = Wannier90DisentanglementMatrixParser().execute(
            payloads["disentanglement"]
        )
        energies = (
            Wannier90EigenvalueParser()
            .execute(payloads["eig"], PhysicalUnit("eV"))
            .eigenvalues.magnitude
        )
        if (amn.kpoint_count, amn.band_count, amn.trial_orbital_count) != (
            216,
            20,
            10,
        ) or energies.shape != (216, 20):
            raise ValueError("native dimensions differ")
        expected_points = np.asarray(
            [
                (round(i / 6, 10), round(j / 6, 10), round(k / 6, 10))
                for i in range(6)
                for j in range(6)
                for k in range(6)
            ]
        )
        if not np.array_equal(dis.fractional_kpoints.magnitude, expected_points):
            raise ValueError("ordered construction points differ")
        cap_low = float(energies[0, 14])
        cap_high = float(energies[energies > cap_low].min())
        exact_cap = (Fraction.from_float(cap_low) + Fraction.from_float(cap_high)) / 2
        cap = float(exact_cap)
        transform = CommonSpaceNativeOverlapReconstruction._atomic_transform()
        points: list[Json] = []
        gamma: dict[str, Json] = {}
        for index in range(216):
            for energy in energies[index]:
                self._check_energy_membership(float(energy), Fraction(-6), exact_cap)
                self._check_energy_membership(
                    float(energy), Fraction(-117, 20), Fraction(8)
                )
            quantity = amn.matrices[index]
            c = exact(np.asarray(quantity.magnitude)).multiply(transform.adjoint())
            outer = np.flatnonzero((energies[index] >= -6) & (energies[index] <= cap))
            frozen = np.flatnonzero((energies[index] >= -5.85) & (energies[index] <= 8))
            cw = _ExactMatrix(rows=tuple(c.rows[int(i)] for i in outer))
            cf = _ExactMatrix(rows=tuple(c.rows[int(i)] for i in frozen))
            error = CommonSpaceMatrixUncertainty.from_parsed_matrix(
                matrix=quantity, native_component_error=Fraction(1, 2 * 10**12)
            )
            epsilon = error.parsing_error_bound + error.native_error_bound
            lower_trial, _ = minimum_bounds(cw)
            lower_frozen, _ = minimum_bounds(cf.adjoint())
            if len(frozen) > 10 or lower_trial <= epsilon or lower_frozen <= epsilon:
                raise RuntimeError(f"pointwise feasibility not established: {index}")
            qc, _, _ = np.linalg.svd(c.to_numpy(), full_matrices=False)
            qd, _, _ = np.linalg.svd(dis.matrices[index].magnitude, full_matrices=False)
            cosines = np.linalg.svd(qd.conj().T @ qc, compute_uv=False)
            points.append(
                {
                    "ordered_index": index,
                    "trial_minimum_nominal": float(
                        np.linalg.svd(cw.to_numpy(), compute_uv=False)[-1]
                    ),
                    "trial_minimum_lower_display": float(lower_trial - epsilon),
                    "frozen_overlap_minimum_lower_display": float(
                        lower_frozen - epsilon
                    ),
                    "candidate_outer_band_count": len(outer),
                    "frozen_band_count": len(frozen),
                    "original_retained_principal_cosine_minimum_nominal": float(
                        cosines[-1]
                    ),
                }
            )
            if index == 0:
                original = _ExactMatrix(rows=c.rows[:14])
                _, _, vh = np.linalg.svd(original.to_numpy(), full_matrices=False)
                vector = exact(np.asarray(vh[-1].conj()).reshape(-1, 1))
                image = c.multiply(vector)
                response = [
                    z.real**2 + z.imaginary**2 for row in image.rows[14:] for z in row
                ]
                _, window_upper = minimum_bounds(original)
                gamma = {
                    "full_parent_trial_minimum_nominal": float(
                        np.linalg.svd(c.to_numpy(), compute_uv=False)[-1]
                    ),
                    "original_window_trial_minimum_upper_including_input_error_display": float(
                        window_upper + epsilon
                    ),
                    "band15_energy_native_ev": cap_low,
                    "band15_excluded_response_share_nominal": float(
                        response[0] / sum(response, Fraction(0))
                    ),
                }
        result: dict[str, Json] = {
            "scope": "Key-finding replay only; no window selection, operator construction, normalized acceptance criterion or protocol completion.",
            "checkpoint_manifest_sha256": _sha(self.checkpoint / "manifest.json"),
            "reproduction_script_sha256": _sha(Path(__file__)),
            "request_sha256": _sha(self.checkpoint / "inputs/request.json"),
            "test_only_cap_interval_native_ev": [cap_low, cap_high],
            "test_only_cap_representative_native_ev": cap,
            "rounding_model": "Nearest AMN/EIG twelve decimal places; correctly rounded binary64 parsing. Scalar bounds are floating displays, not serialized exact interval certificates.",
            "gamma": gamma,
            "points": points,
            "limitations": "No new localized frame, off-mesh guarantee, symmetry attribution, new overlap-gate result, parent fidelity or production qualification.",
        }
        self.output_root.mkdir(parents=True, exist_ok=False)
        output = self.output_root / "key-findings.json"
        with output.open("x") as stream:
            json.dump(result, stream, indent=2, allow_nan=False)
            stream.write("\n")
        return output


def main() -> None:
    """Expose only checkpoint inspection, explicit input paths and numerical replay."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--checkpoint", type=Path, default=Path(__file__).resolve().parent
    )
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--check-only", action="store_true")
    for role in ("amn", "gauge", "disentanglement", "eig"):
        parser.add_argument(f"--{role}", type=Path)
    args = parser.parse_args()
    paths = tuple(
        ("AMN" if role == "amn" else role, path)
        for role in ("amn", "gauge", "disentanglement", "eig")
        if (path := getattr(args, role)) is not None
    )
    action = WindowRemedyReproduction(
        checkpoint=args.checkpoint, output_root=args.output_root, native_paths=paths
    )
    if args.check_only:
        action.inspect()
        print("Retained checkpoint identities and script/request bindings match.")
    else:
        print(action.execute())


if __name__ == "__main__":
    main()
