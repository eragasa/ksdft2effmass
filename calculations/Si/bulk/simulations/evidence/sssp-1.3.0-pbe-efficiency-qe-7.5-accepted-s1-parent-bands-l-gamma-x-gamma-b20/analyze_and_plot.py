"""Parse the retained QE stdout and render the parent band-path diagram."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
from types import ModuleType

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

ROOT = Path(__file__).resolve().parent
PATH_MANIFEST = ROOT / "input" / "path.json"
STDOUT = ROOT / "occurrence" / "pw.out"
OUTPUT = ROOT / "result" / "band-data.json"
FIGURES = ROOT / "figures"
GAUGE_SCRIPT = ROOT.parents[2] / "analysis/c6-b20-w21-gauge-alignment-locality/run_analysis.py"
GAUGE_REQUEST = ROOT.parents[2] / "analysis/c6-b20-w21-gauge-alignment-locality/request.json"
EXPECTED_STDOUT = "ac291059569886db84a3723b2c6c8da9489987aa8a57769e1e5a2d5f48ffe138"
EXPECTED_PATH = "05d1abb15cf4e9067f761ba74942d692b0b12af46ab4e8db362c22aa903a7ca7"
EXPECTED_POINT_COUNT = 241
EXPECTED_BAND_COUNT = 20
K_HEADER = re.compile(r"^\s*k\s*=.*bands \(ev\):\s*$")
FLOAT = re.compile(r"[-+]?\d+\.\d+(?:[Ee][-+]?\d+)?")
RealArray = NDArray[np.float64]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_stdout() -> RealArray:
    if sha256(STDOUT) != EXPECTED_STDOUT:
        raise RuntimeError("retained pw.out identity mismatch")
    text = STDOUT.read_text(encoding="utf-8")
    if "JOB DONE." not in text:
        raise RuntimeError("retained QE occurrence did not complete")
    lines = text.splitlines()
    spectra: list[list[float]] = []
    index = 0
    while index < len(lines):
        if K_HEADER.match(lines[index]) is None:
            index += 1
            continue
        values: list[float] = []
        index += 1
        while index < len(lines) and len(values) < EXPECTED_BAND_COUNT:
            values.extend(float(value) for value in FLOAT.findall(lines[index]))
            index += 1
        if len(values) != EXPECTED_BAND_COUNT:
            raise RuntimeError("invalid eigenvalue block in retained pw.out")
        spectra.append(values)
    result = np.asarray(spectra, dtype=np.float64)
    if result.shape != (EXPECTED_POINT_COUNT, EXPECTED_BAND_COUNT):
        raise RuntimeError(f"unexpected parent spectrum shape: {result.shape}")
    if not np.all(np.isfinite(result)):
        raise RuntimeError("parent spectrum contains nonfinite values")
    return result


def load_path() -> tuple[dict[str, object], RealArray]:
    if sha256(PATH_MANIFEST) != EXPECTED_PATH:
        raise RuntimeError("path manifest identity mismatch")
    manifest = json.loads(PATH_MANIFEST.read_text(encoding="utf-8"))
    points = np.asarray(
        [point["fractional_reciprocal_coordinates"] for point in manifest["points"]],
        dtype=np.float64,
    )
    if points.shape != (EXPECTED_POINT_COUNT, 3):
        raise RuntimeError("invalid path coordinate shape")
    return manifest, points


def load_wannier(points: RealArray) -> tuple[RealArray, dict[str, object]]:
    specification = importlib.util.spec_from_file_location("c6_b20_w21_gauge_source", GAUGE_SCRIPT)
    if specification is None or specification.loader is None:
        raise RuntimeError("cannot load authenticated Wannier parser")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    request = json.loads(GAUGE_REQUEST.read_text(encoding="utf-8"))
    sources = request["sources"]
    native = module.parse_hr(Path(sources["hamiltonian"]["path"]))
    operator = module.FiniteWannierOperator.from_native(
        native, Path(sources["ws_vectors"]["path"])
    )
    matrices = np.asarray(operator.matrices(points), dtype=np.complex128)
    eigenvalues = np.linalg.eigvalsh(matrices)
    if eigenvalues.shape != (EXPECTED_POINT_COUNT, 10):
        raise RuntimeError("unexpected Wannier spectrum shape")
    return eigenvalues, {
        "hamiltonian": sources["hamiltonian"],
        "ws_vectors": sources["ws_vectors"],
        "energy_reference": "native Wannier90/QE energy reference; no fitted shift",
    }


def path_distance(points: RealArray) -> RealArray:
    reciprocal = np.asarray(
        [
            [1.1488345422775257, -1.1488345422775257, 1.1488345422775257],
            [1.1488345422775257, 1.1488345422775257, -1.1488345422775257],
            [-1.1488345422775257, 1.1488345422775257, 1.1488345422775257],
        ],
        dtype=np.float64,
    )
    cartesian = points @ reciprocal.T
    distance = np.zeros(len(points), dtype=np.float64)
    distance[1:] = np.cumsum(np.linalg.norm(np.diff(cartesian, axis=0), axis=1))
    return distance


def render(
    distance: RealArray,
    parent: RealArray,
    wannier: RealArray,
    vertex_indices: list[int],
    vertex_labels: list[str],
    reference: float,
) -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(7.4, 5.2), constrained_layout=True)
    for band in range(12):
        axis.plot(
            distance,
            parent[:, band] - reference,
            color="0.25",
            linewidth=1.05,
            label="DFT parent" if band == 0 else None,
            zorder=2,
        )
    for band in range(10):
        axis.plot(
            distance,
            wannier[:, band] - reference,
            color="#2878b5",
            linewidth=0.85,
            linestyle="--",
            alpha=0.9,
            label="C6-B20-W21 source" if band == 0 else None,
            zorder=3,
        )
    for index in vertex_indices:
        axis.axvline(distance[index], color="0.75", linewidth=0.8, zorder=1)
    axis.axhline(0.0, color="0.1", linewidth=0.8, linestyle=":")
    axis.set_xticks([distance[index] for index in vertex_indices], vertex_labels)
    axis.set_xlim(float(distance[0]), float(distance[-1]))
    axis.set_ylim(-11.0, 8.0)
    axis.set_ylabel(r"Energy relative to parent path VBM (eV)")
    axis.set_title("Accepted-S1 PBE parent band path")
    axis.legend(loc="upper right", frameon=False)
    axis.text(
        0.015,
        0.02,
        "QE 7.5 · SSSP 1.3.0 PBE efficiency · 42/336 Ry",
        transform=axis.transAxes,
        fontsize=8,
        color="0.35",
    )
    figure.savefig(FIGURES / "parent-dft-band-diagram.pdf")
    figure.savefig(FIGURES / "parent-dft-band-diagram.png", dpi=240)
    plt.close(figure)


def main() -> None:
    if OUTPUT.exists():
        raise RuntimeError("refusing to overwrite retained band data")
    manifest, points = load_path()
    parent = parse_stdout()
    wannier, wannier_sources = load_wannier(points)
    distance = path_distance(points)
    segments = manifest["segments"]
    vertex_indices = [int(segments[0]["start_point_index_zero_based"])] + [
        int(segment["end_point_index_zero_based"]) for segment in segments
    ]
    vertex_labels = [r"$L$", r"$\Gamma$", r"$X$", r"$\Gamma$"]
    parent_vbm = float(np.max(parent[:, 3]))
    parent_cbm = float(np.min(parent[:, 4]))
    wannier_vbm = float(np.max(wannier[:, 3]))
    wannier_cbm = float(np.min(wannier[:, 4]))
    render(distance, parent, wannier, vertex_indices, vertex_labels, parent_vbm)
    result: dict[str, object] = {
        "schema_version": 1,
        "status": "producer-checked-band-path-postprocessing",
        "calculator_invocations_in_postprocessing": 0,
        "path": manifest,
        "distance_inverse_angstrom": distance.tolist(),
        "parent_eigenvalues_ev_native_reference": parent.tolist(),
        "wannier_eigenvalues_ev_native_reference": wannier.tolist(),
        "energy_reference": {
            "plot_zero": "maximum parent band index 3 on the retained path",
            "parent_path_vbm_ev_native_reference": parent_vbm,
            "wannier_path_vbm_ev_native_reference": wannier_vbm,
            "no_fitted_energy_shift": True,
        },
        "path_diagnostics": {
            "parent_path_cbm_ev_native_reference": parent_cbm,
            "parent_path_indirect_gap_ev": parent_cbm - parent_vbm,
            "wannier_path_cbm_ev_native_reference": wannier_cbm,
            "wannier_path_indirect_gap_ev": wannier_cbm - wannier_vbm,
            "scope": "sampled L-Gamma-X-Gamma path only; not a global Brillouin-zone extremum proof",
        },
        "sources": {
            "qe_stdout": {
                "path": str(STDOUT),
                "byte_size": STDOUT.stat().st_size,
                "sha256": sha256(STDOUT),
            },
            "path_manifest": {
                "path": str(PATH_MANIFEST),
                "byte_size": PATH_MANIFEST.stat().st_size,
                "sha256": sha256(PATH_MANIFEST),
            },
            "wannier": wannier_sources,
        },
        "figure": {
            "displayed_parent_bands": 12,
            "computed_parent_bands": 20,
            "displayed_wannier_bands": 10,
            "common_reference": "parent path VBM; source uses native common energy reference without fitted shift",
        },
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
