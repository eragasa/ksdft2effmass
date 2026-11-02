from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path
from types import ModuleType

import numpy as np
from numpy.typing import NDArray

RealArray = NDArray[np.float64]
type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]

ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[4]
REQUEST = ROOT / "request.json"
OUTPUT = ROOT / "result.json"
STATUS = (
    "post-hoc-producer-checked-development-exploration-not-independently-verified"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def identity(path: Path) -> JsonObject:
    return {
        "path": str(path),
        "byte_size": path.stat().st_size,
        "sha256": sha256(path),
    }


def mapping(value: JsonValue, name: str) -> JsonObject:
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be a mapping")
    return value


def values(value: JsonValue, name: str) -> list[JsonValue]:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be a list")
    return value


def numeric(value: JsonValue, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be numeric")
    return float(value)


def string(value: JsonValue, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise TypeError(f"{name} must be a nonempty string")
    return value


def source_path(declaration: JsonObject, name: str) -> Path:
    path = Path(string(declaration["path"], f"{name} path"))
    return path if path.is_absolute() else REPOSITORY / path


def authenticate_sources(request: JsonObject) -> JsonObject:
    authenticated: JsonObject = {}
    for label, declaration_value in mapping(request["sources"], "sources").items():
        declaration = mapping(declaration_value, label)
        path = source_path(declaration, label)
        if not path.is_file() or path.is_symlink():
            raise RuntimeError(f"source absent or symlinked: {path}")
        observed = identity(path)
        expected_size = int(numeric(declaration["byte_size"], f"{label} size"))
        expected_digest = string(declaration["sha256"], f"{label} digest")
        if observed["byte_size"] != expected_size or observed["sha256"] != expected_digest:
            raise RuntimeError(f"source identity mismatch: {path}")
        authenticated[label] = observed
    return authenticated


def load_adapter(path: Path) -> ModuleType:
    specification = importlib.util.spec_from_file_location(
        "c6_b20_w21_tau_map_adapter", path
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("cannot load the authenticated native-HR adapter")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def point_inventory(path: Path) -> RealArray:
    manifest_value: JsonValue = json.loads(path.read_text(encoding="utf-8"))
    manifest = mapping(manifest_value, "point manifest")
    points = values(manifest["points"], "manifest points")
    coordinates = np.asarray(
        [
            [
                numeric(component, "fractional coordinate")
                for component in values(
                    mapping(point, "point")["fractional_reciprocal_coordinates"],
                    "point coordinates",
                )
            ]
            for point in points
        ],
        dtype=np.float64,
    )
    if coordinates.shape != (408, 3):
        raise RuntimeError("development point inventory must have shape (408, 3)")
    return coordinates


def pareto_membership(
    candidates: list[JsonObject], spectral_key: str, operator_key: str
) -> tuple[str, ...]:
    members: list[str] = []
    for candidate in candidates:
        candidate_spectral = numeric(candidate[spectral_key], spectral_key)
        candidate_operator = numeric(candidate[operator_key], operator_key)
        dominated = False
        for other in candidates:
            if other is candidate:
                continue
            other_spectral = numeric(other[spectral_key], spectral_key)
            other_operator = numeric(other[operator_key], operator_key)
            if (
                other_spectral <= candidate_spectral
                and other_operator <= candidate_operator
                and (
                    other_spectral < candidate_spectral
                    or other_operator < candidate_operator
                )
            ):
                dominated = True
                break
        if not dominated:
            members.append(string(candidate["shell_id"], "shell id"))
    return tuple(members)


def main() -> None:
    if OUTPUT.exists():
        raise FileExistsError(f"refusing to overwrite retained result: {OUTPUT}")
    start = time.perf_counter()
    request_value: JsonValue = json.loads(REQUEST.read_text(encoding="utf-8"))
    request = mapping(request_value, "request")
    authenticated = authenticate_sources(request)
    sources = mapping(request["sources"], "sources")
    adapter_path = source_path(
        mapping(sources["authenticated_adapter"], "adapter"), "adapter"
    )
    adapter = load_adapter(adapter_path)
    native = adapter.parse_hr(
        source_path(mapping(sources["hamiltonian"], "hamiltonian"), "Hamiltonian")
    )
    operator = adapter.FiniteWannierOperator.from_native(
        native,
        source_path(mapping(sources["ws_vectors"], "WS vectors"), "WS vectors"),
    )
    design_value: JsonValue = json.loads(
        source_path(
            mapping(sources["truncation_design"], "truncation design"),
            "truncation design",
        ).read_text(encoding="utf-8")
    )
    design = mapping(design_value, "truncation design")
    fixed_source = mapping(design["fixed_reduction_source"], "fixed source")
    direct_basis = np.asarray(
        values(fixed_source["direct_basis_columns_angstrom"], "direct basis"),
        dtype=np.float64,
    )
    if direct_basis.shape != (3, 3):
        raise RuntimeError("direct basis must have shape (3, 3)")
    family = mapping(design["truncation_family"], "truncation family")
    shells = [mapping(item, "shell") for item in values(family["shells"], "shells")]
    if len(shells) != 18:
        raise RuntimeError("frozen native shell family must contain 18 candidates")
    coordinates = point_inventory(
        source_path(mapping(sources["point_manifest"], "point manifest"), "point manifest")
    )
    full_matrices = operator.matrices(coordinates)
    full_spectrum = np.linalg.eigvalsh(full_matrices)
    cartesian = np.asarray(operator.representatives, dtype=np.float64) @ direct_basis.T
    rounded_radii = np.round(np.linalg.norm(cartesian, axis=1), decimals=9)
    rank = 10
    root_rank = float(np.sqrt(rank))
    candidate_records: list[JsonObject] = []
    for shell in shells:
        radius = numeric(shell["display_radius_angstrom"], "shell radius")
        mask = rounded_radii <= radius
        included_count = int(np.count_nonzero(mask))
        expected_count = int(
            numeric(shell["included_representative_count"], "included count")
        )
        if included_count != expected_count:
            raise RuntimeError(
                f"native mask count mismatch for {string(shell['shell_id'], 'shell id')}"
            )
        subset = adapter.FiniteWannierOperator(
            representatives=operator.representatives[mask],
            blocks_ev=operator.blocks_ev[mask],
            native_representative_count=operator.native_representative_count,
        )
        candidate_matrices = subset.matrices(coordinates)
        matrix_difference = candidate_matrices - full_matrices
        frobenius = np.linalg.norm(matrix_difference, axis=(-2, -1))
        candidate_spectrum = np.linalg.eigvalsh(candidate_matrices)
        spectrum_difference = candidate_spectrum - full_spectrum
        record: JsonObject = {
            "shell_id": string(shell["shell_id"], "shell id"),
            "shell_index_zero_based": int(
                numeric(shell["shell_index_zero_based"], "shell index")
            ),
            "radius_angstrom": radius,
            "included_representative_count": included_count,
            "proper_reduced_candidate": not bool(shell["full_support_control"]),
            "tau_1_spectral_rms": float(
                np.sqrt(np.mean(np.square(spectrum_difference)))
            ),
            "tau_2_operator_rms_per_state": float(
                np.sqrt(np.mean(np.square(frobenius)) / rank)
            ),
            "spectral_maximum": float(np.max(np.abs(spectrum_difference))),
            "operator_maximum_per_state": float(np.max(frobenius) / root_rank),
            "maximum_matrix_hermiticity_defect_ev": float(
                np.max(
                    np.linalg.norm(
                        candidate_matrices
                        - candidate_matrices.conj().swapaxes(-1, -2),
                        axis=(-2, -1),
                    )
                )
            ),
        }
        candidate_records.append(record)
    proper_candidates = [
        candidate
        for candidate in candidate_records
        if candidate["proper_reduced_candidate"] is True
    ]
    rms_pareto = pareto_membership(
        proper_candidates,
        "tau_1_spectral_rms",
        "tau_2_operator_rms_per_state",
    )
    maximum_pareto = pareto_membership(
        proper_candidates,
        "spectral_maximum",
        "operator_maximum_per_state",
    )
    full_control = candidate_records[-1]
    for key in (
        "tau_1_spectral_rms",
        "tau_2_operator_rms_per_state",
        "spectral_maximum",
        "operator_maximum_per_state",
    ):
        if numeric(full_control[key], key) != 0.0:
            raise RuntimeError("full-support control must have exact zero loss")
    result: JsonObject = {
        "schema_version": 1,
        "status": STATUS,
        "calculator_invocations": 0,
        "independent_reconstruction_performed": False,
        "post_hoc": True,
        "request": identity(REQUEST),
        "producer": identity(Path(__file__)),
        "authenticated_sources": authenticated,
        "hypothesis": {
            "tau_1": "uniform-408-point RMS ordered-spectrum error / 1 eV",
            "tau_2": (
                "uniform-408-point RMS Hamiltonian Frobenius error per retained "
                "state / 1 eV"
            ),
            "feasible_pair_rule": (
                "a threshold pair is feasible exactly when at least one proper reduced "
                "candidate has tau_1 requirement no greater than the supplied tau_1 "
                "and tau_2 requirement no greater than the supplied tau_2"
            ),
            "minimum_support_witness_rule": (
                "among feasible proper reduced candidates select the smallest exact "
                "included-representative count"
            ),
            "threshold_acceptance_claim": False,
        },
        "evaluation": {
            "point_count": len(coordinates),
            "weights": "uniform 1/408",
            "basis": "fixed authenticated rank-10 Wannier basis",
            "alignment": "identity",
            "energy_scale_ev": 1.0,
            "parent_values_consumed": False,
            "confirmation_402_geometry_consumed": False,
        },
        "candidate_family": {
            "native_effective_representative_count": len(operator.representatives),
            "proper_reduced_candidate_count": len(proper_candidates),
            "full_support_control_shell_id": string(
                full_control["shell_id"], "full control id"
            ),
            "full_support_excluded_from_feasibility": True,
            "reason": (
                "including the exact full source would make every nonnegative threshold "
                "pair trivially feasible"
            ),
        },
        "candidates": candidate_records,
        "rms_loss_pair_pareto_shells": list(rms_pareto),
        "maximum_loss_pair_pareto_shells": list(maximum_pareto),
        "execution": {
            "elapsed_seconds": float(time.perf_counter() - start),
            "output_path": str(OUTPUT),
        },
        "limitations": [
            "This is a post-hoc threshold-map exploration, not a prospective acceptance test.",
            "The finite family consists only of literal native Wigner-Seitz shell truncations; no block coefficients are refitted.",
            "The result tests internal compressibility of the represented Wannier Hamiltonian, not agreement with the DFT parent or experiment.",
            "The exact full-support source is excluded from reduced-family feasibility and retained only as a zero-loss control.",
            "No Slater-Koster orbital semantics, parameterization, or model-class expressivity claim is made.",
        ],
    }
    OUTPUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
