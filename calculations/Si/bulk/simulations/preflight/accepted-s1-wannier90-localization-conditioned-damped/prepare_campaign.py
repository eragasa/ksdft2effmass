from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from projectkoios.integrations.wannier90 import Wannier90LocalizationInputPreparer

ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier90-localization-conditioned-damped-20261031T083023Z"
)
PARENT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier90-localization-sp3sstar-20261031T081246Z"
)
SOURCE = PARENT / "prepared-input"
DECISION = Path(
    "/Users/eugene/worktrees/ksdft2effmass-si-right-handed-kpoint/"
    "calculations/Si/bulk/simulations/localization-revision-decision.md"
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
        raise RuntimeError("revised localization preflight root already exists")
    ROOT.mkdir(parents=True)
    source = ROOT / "source-input"
    source.mkdir()
    for name in ("silicon.nnkp", "silicon.eig", "silicon.amn", "silicon.mmn"):
        shutil.copyfile(SOURCE / name, source / name)
    original = (SOURCE / "silicon.win").read_text(encoding="utf-8")
    replacements = {
        "num_iter = 100\n": "num_iter = 500\n",
        "dis_num_iter = 200\n": "dis_num_iter = 1000\n",
        "dis_mix_ratio = 0.5\n": "dis_mix_ratio = 0.2\n",
        "write_u_matrices = .true.\n": (
            "write_u_matrices = .true.\nprecond = .true.\n"
        ),
    }
    revised = original
    for old, new in replacements.items():
        if revised.count(old) != 1:
            raise RuntimeError(f"unexpected WIN control inventory: {old.strip()}")
        revised = revised.replace(old, new)
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
        "changes": {
            "precond": [False, True],
            "num_iter": [100, 500],
            "dis_mix_ratio": [0.5, 0.2],
            "dis_num_iter": [200, 1000],
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
    implementation = (
        PROJECTKOIOS
        / "src/python/projectkoios/integrations/wannier90/localization_execution.py"
    )
    blocked_result = PARENT / "campaign-result.json"
    preflight = {
        "schema_version": 1,
        "purpose": "conditioned and damped rank-10 localization convergence revision",
        "status": "awaiting-explicit-bounded-authorization",
        "execution_performed": False,
        "decision": observation(DECISION),
        "blocked_parent_result": observation(blocked_result),
        "prepared_input_manifest": observation(preparation.manifest_path),
        "win_transformation": observation(transformation_path),
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
            "precond": True,
            "num_iter": 500,
            "conv_tol_angstrom_squared": 1e-10,
            "conv_window": 3,
            "dis_num_iter": 1000,
            "dis_mix_ratio": 0.2,
            "dis_conv_tol_angstrom_squared": 1e-10,
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
            "preflight only; no revised localization or operator result"
        ),
    }
    write_json(ROOT / "campaign-preflight.json", preflight)


if __name__ == "__main__":
    main()
