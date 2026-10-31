from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import numpy as np
from projectkoios.integrations.wannier90 import (
    Wannier90EigenvalueParser,
    Wannier90LocalizationInputPreparer,
)
from projectkoios.physkit.units import PhysicalUnit

ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier90-localization-conduction-frozen-fixed-step1-20261031T091916Z"
)
PARENT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier90-localization-conduction-frozen-iter1000-20261031T085113Z"
)
SOURCE = PARENT / "prepared-input"
DECISION = Path(
    "/Users/eugene/worktrees/ksdft2effmass-si-right-handed-kpoint/"
    "calculations/Si/bulk/simulations/conduction-frozen-fixed-step-decision.md"
)
TOLERANCE_NOTE = Path(
    "/Users/eugene/worktrees/ksdft2effmass-si-right-handed-kpoint/"
    "calculations/Si/bulk/simulations/disentanglement-convergence-tolerance.md"
)
PROJECTKOIOS = Path(
    "/Users/eugene/worktrees/projectkoios-simulations-pw-dft-wannierization-tranche-1"
)
EXECUTABLE = Path("/Users/eugene/projects/wannier90-3.1.0/wannier90.x")
PREPROCESSING_SHA256 = (
    "d68e18bc9ee1138ca2e392198ab15b80e43ebf3ce319fb5ff0d7b772172191ee"
)
CONVERTER_SHA256 = "3e68cd8fd3b9b5438772bc73fbcae9d835ffd819ca6155aa9989703a28def823"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def observation(path: Path) -> dict[str, object]:
    return {"path": str(path), "byte_size": path.stat().st_size, "sha256": sha256(path)}


def write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, allow_nan=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    if ROOT.exists():
        raise RuntimeError("fixed-step preflight root already exists")
    ROOT.mkdir(parents=True)
    source = ROOT / "source-input"
    source.mkdir()
    for name in ("silicon.nnkp", "silicon.eig", "silicon.amn", "silicon.mmn"):
        shutil.copyfile(SOURCE / name, source / name)
    original = (SOURCE / "silicon.win").read_text(encoding="utf-8")
    marker = "precond = .true.\n"
    if (
        original.count(marker) != 1
        or "trial_step" in original
        or "fixed_step" in original
    ):
        raise RuntimeError("unexpected source line-search control inventory")
    revised = original.replace(marker, marker + "fixed_step = 1\n")
    (source / "silicon.win").write_text(revised, encoding="utf-8")
    preparation = Wannier90LocalizationInputPreparer().prepare(
        source_directory=source,
        output_directory=ROOT / "prepared-input",
        seedname="silicon",
        kpoint_count=64,
        band_count=12,
        wannier_count=10,
        neighbor_count=8,
        parent_preprocessing_sha256=PREPROCESSING_SHA256,
        parent_converter_sha256=CONVERTER_SHA256,
    )
    transformation = {
        "schema_version": 1,
        "source_win": observation(SOURCE / "silicon.win"),
        "revised_win": observation(preparation.output_directory / "silicon.win"),
        "only_change": {
            "line_search_before": "parabolic with native trial_step 2.0",
            "line_search_after": "disabled; dimensionless fixed_step 1.0",
        },
        "unchanged_interface_artifacts": [
            "silicon.nnkp",
            "silicon.eig",
            "silicon.amn",
            "silicon.mmn",
        ],
        "fresh_occurrence": True,
        "checkpoint_consumed": False,
    }
    transformation_path = ROOT / "win-transformation.json"
    write_json(transformation_path, transformation)
    eigenvalues = (
        Wannier90EigenvalueParser()
        .execute((source / "silicon.eig").read_bytes(), PhysicalUnit("eV"))
        .eigenvalues.magnitude
    )
    frozen_counts = np.sum((eigenvalues >= 6.0) & (eigenvalues <= 19.02), axis=1)
    below_counts = np.sum(eigenvalues < 6.0, axis=1)
    if not np.all(frozen_counts == 8) or not np.all(below_counts == 4):
        raise RuntimeError(
            "frozen window does not select exactly eight conduction bands"
        )
    window_analysis = {
        "schema_version": 1,
        "eigenvalue_artifact": observation(source / "silicon.eig"),
        "energy_unit": "eV",
        "frozen_window_ev": [6.0, 19.02],
        "kpoint_count": 64,
        "minimum_frozen_count_per_kpoint": int(np.min(frozen_counts)),
        "maximum_frozen_count_per_kpoint": int(np.max(frozen_counts)),
        "minimum_below_window_count_per_kpoint": int(np.min(below_counts)),
        "maximum_below_window_count_per_kpoint": int(np.max(below_counts)),
        "maximum_band_4_ev": float(np.max(eigenvalues[:, 3])),
        "minimum_band_5_ev": float(np.min(eigenvalues[:, 4])),
        "maximum_band_12_ev": float(np.max(eigenvalues[:, 11])),
        "exactly_eight_conduction_bands_frozen_at_every_kpoint": True,
    }
    window_analysis_path = ROOT / "frozen-window-analysis.json"
    write_json(window_analysis_path, window_analysis)
    implementation = (
        PROJECTKOIOS
        / "src/python/projectkoios/integrations/wannier90/localization_execution.py"
    )
    blocked_result = PARENT / "campaign-result.json"
    preflight = {
        "schema_version": 1,
        "purpose": "conduction-frozen fixed-step Wannierisation test",
        "status": "awaiting-explicit-bounded-authorization",
        "execution_performed": False,
        "decision": observation(DECISION),
        "tolerance_interpretation": observation(TOLERANCE_NOTE),
        "blocked_parent_result": observation(blocked_result),
        "prepared_input_manifest": observation(preparation.manifest_path),
        "win_transformation": observation(transformation_path),
        "frozen_window_analysis": observation(window_analysis_path),
        "projectkoios_provider": {
            "base_revision": "e146f3722e87ca2de2243421a94448cfa6e27037",
            "implementation": observation(implementation),
        },
        "candidate": {
            "seedname": "silicon",
            "kpoint_count": 64,
            "band_count": 12,
            "wannier_count": 10,
            "neighbor_count": 8,
            "outer_window_ev": [-5.85, 19.02],
            "frozen_window_ev": [6.0, 19.02],
            "frozen_conduction_band_count_per_kpoint": 8,
            "frozen_valence_band_count_per_kpoint": 0,
            "precond": True,
            "guiding_centres": False,
            "trial_step": None,
            "fixed_step": 1.0,
            "fixed_step_unit": "dimensionless",
            "num_iter": 1000,
            "conv_tol_angstrom_squared": 1e-10,
            "conv_window": 3,
            "dis_num_iter": 1000,
            "dis_mix_ratio": 0.2,
            "dis_conv_tol_fractional": 1e-10,
            "dis_conv_window": 3,
            "fresh_occurrence": True,
            "checkpoint_consumed": False,
        },
        "executable": {"version": "3.1.0", **observation(EXECUTABLE)},
        "planned_command": [str(EXECUTABLE), "silicon"],
        "resource_bounds": {
            "processes": 1,
            "timeout_seconds": 300.0,
            "maximum_retained_bytes": 67108864,
            "retries": 0,
            "stop_on_failure": True,
        },
        "required_outputs": [
            "silicon.wout",
            "silicon_hr.dat",
            "silicon_u.mat",
            "silicon_u_dis.mat",
        ],
        "eligibility_policy": {
            "required_return_code": 0,
            "disentanglement_convergence_phrase_required": True,
            "wannierisation_convergence_phrase_required": True,
            "native_completion_phrase_required": True,
            "maximum_iteration_warning_forbidden": True,
            "unitary_isometry_tolerance": 1e-8,
            "kpoint_fractional_tolerance": 1e-10,
            "hamiltonian_hermiticity_tolerance_ev": 1e-8,
        },
        "authorization_request": {
            "maximum_invocations": 1,
            "retries": 0,
            "stop_on_failure": True,
        },
        "scientific_disposition": (
            "preflight only; no fixed-step localization or operator result"
        ),
    }
    write_json(ROOT / "campaign-preflight.json", preflight)


if __name__ == "__main__":
    main()
