from __future__ import annotations

import hashlib
import itertools
import json
import re
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
    "si-accepted-s1-wannier90-localization-lower-energy-frozen-dis2000-20261031T100534Z"
)
PARENT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier90-localization-lower-energy-frozen-20261031T094734Z"
)
SOURCE = PARENT / "prepared-input"
DECISION = Path(
    "/Users/eugene/worktrees/ksdft2effmass-si-right-handed-kpoint/"
    "calculations/Si/bulk/simulations/lower-energy-frozen-disentanglement-extension-decision.md"
)
TOLERANCE_NOTE = Path(
    "/Users/eugene/worktrees/ksdft2effmass-si-right-handed-kpoint/"
    "calculations/Si/bulk/simulations/disentanglement-convergence-tolerance.md"
)
POLICY_DECISION = Path(
    "/Users/eugene/worktrees/ksdft2effmass-si-right-handed-kpoint/"
    "calculations/Si/bulk/simulations/localization-convergence-policy-decision.md"
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
        raise RuntimeError("disentanglement-extension preflight root already exists")
    ROOT.mkdir(parents=True)
    source = ROOT / "source-input"
    source.mkdir()
    for name in ("silicon.nnkp", "silicon.eig", "silicon.amn", "silicon.mmn"):
        shutil.copyfile(SOURCE / name, source / name)
    original = (SOURCE / "silicon.win").read_text(encoding="utf-8")
    marker = "dis_num_iter = 1000\n"
    if (
        original.count(marker) != 1
        or original.count("dis_froz_min = -5.85\n") != 1
        or original.count("dis_froz_max = 8\n") != 1
        or original.count("conv_tol = 2e-9\n") != 1
        or original.count("conv_window = 6\n") != 1
        or original.count("num_cg_steps = 200\n") != 1
        or original.count("num_iter = 4000\n") != 1
        or "trial_step" in original
        or "fixed_step" in original
    ):
        raise RuntimeError("unexpected source construction/control inventory")
    revised = original.replace(marker, "dis_num_iter = 2000\n")
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
            "dis_num_iter_before": 1000,
            "dis_num_iter_after": 2000,
        },
        "change_class": "disentanglement iteration-budget extension",
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
    frozen_mask = (eigenvalues >= -5.85) & (eigenvalues <= 8.0)
    frozen_counts = np.sum(frozen_mask, axis=1)
    frozen_conduction_counts = np.sum(frozen_mask[:, 4:], axis=1)
    if (
        int(np.min(frozen_counts)) != 4
        or int(np.max(frozen_counts)) != 6
        or not np.all(frozen_mask[:, :4])
        or np.any(frozen_mask[:, 6:])
    ):
        raise RuntimeError("lower-energy frozen-window inventory mismatch")
    included = eigenvalues[frozen_mask]
    excluded_above = eigenvalues[eigenvalues > 8.0]
    window_analysis = {
        "schema_version": 1,
        "eigenvalue_artifact": observation(source / "silicon.eig"),
        "energy_unit": "eV",
        "frozen_window_ev": [-5.85, 8.0],
        "kpoint_count": 64,
        "frozen_state_count": int(np.sum(frozen_counts)),
        "minimum_frozen_count_per_kpoint": int(np.min(frozen_counts)),
        "maximum_frozen_count_per_kpoint": int(np.max(frozen_counts)),
        "kpoints_with_at_least_one_frozen_conduction_state": int(
            np.sum(frozen_conduction_counts >= 1)
        ),
        "kpoints_with_two_frozen_conduction_states": int(
            np.sum(frozen_conduction_counts == 2)
        ),
        "maximum_included_energy_ev": float(np.max(included)),
        "minimum_excluded_energy_above_threshold_ev": float(np.min(excluded_above)),
        "threshold_clearance_ev": float(np.min(excluded_above) - np.max(included)),
        "maximum_band_4_ev": float(np.max(eigenvalues[:, 3])),
        "minimum_band_5_ev": float(np.min(eigenvalues[:, 4])),
        "minimum_band_7_ev": float(np.min(eigenvalues[:, 6])),
        "all_four_valence_bands_frozen_at_every_kpoint": True,
        "bands_7_through_12_excluded_from_frozen_window": True,
        "frozen_count_strictly_below_wannier_rank": True,
    }
    window_analysis_path = ROOT / "frozen-window-analysis.json"
    write_json(window_analysis_path, window_analysis)
    parameter_source = Path("/Users/eugene/projects/wannier90-3.1.0/src/parameters.F90")
    previous_wout = PARENT / "run" / "silicon.wout"
    if sha256(parameter_source) != (
        "19db3643a6bda79a656da56fc92c3065dd98b51c73bfdcd8b4325b5d892014a2"
    ):
        raise RuntimeError("Wannier90 parameter-source identity mismatch")
    if "num_cg_steps = 5" not in parameter_source.read_text(encoding="utf-8"):
        raise RuntimeError("Wannier90 source default for num_cg_steps changed")
    if "Number of CG steps before reset           :               200" not in (
        previous_wout.read_text(encoding="utf-8")
    ):
        raise RuntimeError("predecessor did not report num_cg_steps 200")
    cg_verification = {
        "schema_version": 1,
        "wannier90_version": "3.1.0",
        "quantity": "Fletcher-Reeves conjugate-gradient updates before reset",
        "source_default": {
            "value": 5,
            "source": observation(parameter_source),
            "source_line": "num_cg_steps = 5",
        },
        "previous_occurrence": {
            "explicit_num_cg_steps": 200,
            "effective_value_reported_by_wout": 200,
            "win": observation(SOURCE / "silicon.win"),
            "wout": observation(previous_wout),
        },
        "successor_occurrence": {
            "explicit_num_cg_steps": 200,
            "win": observation(preparation.output_directory / "silicon.win"),
        },
        "unchanged_across_successor": True,
    }
    cg_verification_path = ROOT / "cg-reset-default-verification.json"
    write_json(cg_verification_path, cg_verification)
    literature_protocol = {
        "schema_version": 1,
        "source_kind": "current literature-associated high-throughput workflow protocol",
        "repository": "aiidateam/aiida-wannier90-workflows",
        "commit": "1c0115cb7c77541a0bd549bc05005df435d651b6",
        "path": (
            "src/aiida_wannier90_workflows/workflows/protocols/base/wannier90.yaml"
        ),
        "git_blob": "08049bb780e0a9f63276cbcdfecca3c300fc05fb",
        "raw_url": (
            "https://raw.githubusercontent.com/aiidateam/aiida-wannier90-workflows/"
            "1c0115cb7c77541a0bd549bc05005df435d651b6/"
            "src/aiida_wannier90_workflows/workflows/protocols/base/wannier90.yaml"
        ),
        "observed_moderate_parameters": {
            "conv_tol_per_atom_angstrom_squared": 1e-7,
            "conv_window": 3,
            "dis_num_iter": 4000,
            "num_cg_steps": 200,
            "num_iter": 4000,
        },
        "observed_precise_overrides": {
            "conv_tol_per_atom_angstrom_squared": 1e-9,
            "conv_window": 6,
            "dis_num_iter": 40000,
            "num_iter": 40000,
        },
        "adopted_parameters": {
            "num_cg_steps": 200,
            "num_iter": 4000,
            "conv_tol_for_two_atom_cell_angstrom_squared": 2e-9,
            "conv_window": 6,
        },
        "not_adopted": [
            "40000-iteration budgets",
            "precise dis_conv_tol per atom",
            "other protocol settings",
        ],
        "interpretation": (
            "fixed production-practice optimizer coordinates plus the separately "
            "accepted prospective precise Wannierisation policy, not wholesale "
            "protocol adoption"
        ),
    }
    literature_protocol_path = ROOT / "literature-protocol-observation.json"
    write_json(literature_protocol_path, literature_protocol)
    disentanglement_pattern = re.compile(
        r"^\s*(\d+)\s+[-+0-9.Ee]+\s+[-+0-9.Ee]+\s+([-+0-9.Ee]+)"
        r"\s+[-+0-9.Ee]+\s+<-- DIS\s*$"
    )
    fractional_deltas = []
    for line in previous_wout.read_text(encoding="utf-8").splitlines():
        match = disentanglement_pattern.match(line)
        if match is not None:
            fractional_deltas.append((int(match.group(1)), abs(float(match.group(2)))))
    if len(fractional_deltas) != 1000 or fractional_deltas[-1][0] != 1000:
        raise RuntimeError("unexpected predecessor disentanglement trajectory")
    final_two_hundred = [value for _, value in fractional_deltas[-200:]]
    if any(
        current >= previous
        for previous, current in itertools.pairwise(final_two_hundred)
    ):
        raise RuntimeError("predecessor late disentanglement trend is not monotonic")
    trajectory = {
        "schema_version": 1,
        "predecessor_wout": observation(previous_wout),
        "last_iteration": 1000,
        "last_absolute_fractional_delta": fractional_deltas[-1][1],
        "declared_fractional_tolerance": 1e-10,
        "last_delta_to_threshold_ratio": fractional_deltas[-1][1] / 1e-10,
        "iteration_801_absolute_fractional_delta": final_two_hundred[0],
        "iterations_801_through_1000_monotonically_decreasing": True,
        "late_log_linear_extrapolated_crossing_range": [1274, 1285],
        "extrapolation_is_not_completed_convergence": True,
        "interpretation": (
            "the smooth late trend supports one bounded 2000-step test while retaining "
            "the strict fractional criterion"
        ),
    }
    trajectory_path = ROOT / "predecessor-trajectory-summary.json"
    write_json(trajectory_path, trajectory)
    implementation = (
        PROJECTKOIOS
        / "src/python/projectkoios/integrations/wannier90/localization_execution.py"
    )
    blocked_result = PARENT / "campaign-result.json"
    preflight = {
        "schema_version": 1,
        "purpose": "lower-energy frozen-window disentanglement-budget extension",
        "status": "awaiting-explicit-bounded-authorization",
        "execution_performed": False,
        "decision": observation(DECISION),
        "tolerance_interpretation": observation(TOLERANCE_NOTE),
        "prospective_localization_policy": observation(POLICY_DECISION),
        "blocked_parent_result": observation(blocked_result),
        "prepared_input_manifest": observation(preparation.manifest_path),
        "win_transformation": observation(transformation_path),
        "frozen_window_analysis": observation(window_analysis_path),
        "cg_reset_default_verification": observation(cg_verification_path),
        "literature_protocol_observation": observation(literature_protocol_path),
        "predecessor_trajectory_summary": observation(trajectory_path),
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
            "frozen_window_ev": [-5.85, 8.0],
            "frozen_count_per_kpoint_range": [4, 6],
            "frozen_conduction_band_count_per_kpoint_range": [0, 2],
            "frozen_valence_band_count_per_kpoint": 4,
            "precond": True,
            "guiding_centres": False,
            "trial_step": 2.0,
            "trial_step_source": "native-default",
            "fixed_step": None,
            "num_cg_steps": 200,
            "num_iter": 4000,
            "conv_tol_angstrom_squared": 2e-9,
            "conv_window": 6,
            "dis_num_iter": 2000,
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
            "preflight only; no extended-disentanglement localization or operator result"
        ),
    }
    write_json(ROOT / "campaign-preflight.json", preflight)


if __name__ == "__main__":
    main()
