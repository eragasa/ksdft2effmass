from __future__ import annotations

import hashlib
import importlib
import json
import shutil
import tempfile
from pathlib import Path

from projectkoios.physkit import units as _physkit_units

if not hasattr(_physkit_units, "ModelSystemUnitConverter"):
    _physkit_units.ModelSystemUnitConverter = (  # type: ignore[attr-defined]
        _physkit_units.MODEL_SYSTEM_UNIT_CONVERTER
    )
if not hasattr(_physkit_units, "MODEL_SYSTEM_UNIT_CONVERTER"):
    _physkit_units.MODEL_SYSTEM_UNIT_CONVERTER = (  # type: ignore[attr-defined]
        _physkit_units.ModelSystemUnitConverter
    )

from ksdft2effmass.serialization import TypedJsonMappingSerializer  # noqa: E402

_wannier90 = importlib.import_module("projectkoios.integrations.wannier90")
Wannier90LocalizationInputPreparer = _wannier90.Wannier90LocalizationInputPreparer

ROOT = Path(__file__).resolve().parent
DECISION = ROOT.parents[1] / "c6-disentanglement-budget-extension-decision.md"
PROTOCOL = ROOT.parents[2] / "research-protocol/research-protocol.tex"
PREDECESSOR = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier90-localization-c6-lower-energy-frozen-dis2000-v1"
)
PREDECESSOR_INPUT = PREDECESSOR / "prepared-input/silicon.win"
PREDECESSOR_CAMPAIGN = PREDECESSOR / "campaign-result.json"
PREDECESSOR_TRAJECTORY = PREDECESSOR / "trajectory-analysis.json"
PREDECESSOR_WOUT = PREDECESSOR / "run/silicon.wout"
CONVERTER_ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-pw2wannier90-c6-lower-energy-frozen-v1"
)
PREPROCESSING_RESULT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier90-preprocess-c6-lower-energy-frozen-v1/"
    "preprocessing-result.json"
)
CONVERTER_RESULT = CONVERTER_ROOT / "converter-result.json"
SOURCE_ARTIFACTS = {
    "silicon.nnkp": CONVERTER_ROOT / "run/silicon.nnkp",
    "silicon.eig": CONVERTER_ROOT / "run/silicon.eig",
    "silicon.amn": CONVERTER_ROOT / "run/silicon.amn",
    "silicon.mmn": CONVERTER_ROOT / "run/silicon.mmn",
}
EXECUTABLE = Path("/Users/eugene/projects/wannier90-3.1.0/wannier90.x")
PROVIDER_IMPLEMENTATION = Path(
    "/Users/eugene/worktrees/"
    "projectkoios-simulations-pw-dft-wannierization-tranche-1/"
    "src/python/projectkoios/integrations/wannier90/localization_execution.py"
)
PROPOSED_ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier90-localization-c6-lower-energy-frozen-dis4000-v1"
)
EXPECTED = {
    DECISION: "c0dc41bce705c9637e88bbf607f6db8599cbae564bbc8d46182dbf8277b8c181",
    PROTOCOL: "36ac947bb316af52675a038f0950a6bdacd7a9d13dbb5770812b4cc499df33eb",
    PREDECESSOR_INPUT: (
        "0d5b693972309245f0ce04fca42e8806a8c33017af7d0e184424dec0b429694c"
    ),
    PREDECESSOR_CAMPAIGN: (
        "afbdf5c5cdb2afa602e4235372c01d53cf03b0b4f1174ec37549a0bfe098615a"
    ),
    PREDECESSOR_TRAJECTORY: (
        "971249965dc13b6c3aee779f7196068493ceedd46f45056ce43a998ed19fb4dd"
    ),
    PREDECESSOR_WOUT: (
        "dd8599308ae3bef123a15bbc980ece0c7d668ee92392f738aa8b4a9021413998"
    ),
    PREPROCESSING_RESULT: (
        "8306f8b7340e1673a79342a8725b4ad2bd63e96ea078929b423f6d72145538a4"
    ),
    CONVERTER_RESULT: (
        "ebb9352aa1184be665ef8021bf26feea466ef1f0ce701d071546a19e934f7769"
    ),
    SOURCE_ARTIFACTS["silicon.nnkp"]: (
        "f367195dcc42a72244104e8149bbc75b4ce623c67a6acc1d169c68b33aeffead"
    ),
    SOURCE_ARTIFACTS["silicon.eig"]: (
        "94d759c2906c041a14adc12bd6d740f1f5499c7c85aeea20b06752536f25c463"
    ),
    SOURCE_ARTIFACTS["silicon.amn"]: (
        "efda4f7d101eb5ed5c7d871c3b5a9c14a2343bc09e86188dbf48dca5731355eb"
    ),
    SOURCE_ARTIFACTS["silicon.mmn"]: (
        "f2db3539f36fb2a5c8174c503326e56726553593ec0609f96e66186db488e1a1"
    ),
    EXECUTABLE: ("c826f817f807cf069e16d6e529a52ddc15d2f677101065908bcb2030d7f7d1dd"),
}
TIMEOUT_SECONDS = 600.0
MAXIMUM_BYTES = 64 * 1024**2
SERIALIZER = TypedJsonMappingSerializer()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(path: Path) -> dict[str, object]:
    return {
        "path": str(path),
        "byte_size": path.stat().st_size,
        "sha256": sha256(path),
    }


def write_mapping(path: Path, value: dict[str, object]) -> None:
    path.write_bytes(SERIALIZER.serialize(value))


def revised_input() -> bytes:
    source = PREDECESSOR_INPUT.read_text(encoding="ascii")
    marker = "dis_num_iter = 2000\n"
    if source.count(marker) != 1 or "dis_num_iter = 4000\n" in source:
        raise RuntimeError("predecessor iteration-budget inventory changed")
    revised = source.replace(marker, "dis_num_iter = 4000\n")
    unchanged = (
        "num_bands = 12\n",
        "num_wann = 10\n",
        "num_iter = 4000\n",
        "conv_tol = 2e-09\n",
        "conv_window = 6\n",
        "dis_win_min = -5.85\n",
        "dis_win_max = 19.02\n",
        "dis_froz_min = -5.85\n",
        "dis_froz_max = 8\n",
        "dis_conv_tol = 1e-10\n",
        "dis_conv_window = 3\n",
        "dis_mix_ratio = 0.2\n",
        "write_hr = .true.\n",
        "write_u_matrices = .true.\n",
        "precond = .true.\n",
        "num_cg_steps = 200\n",
        "mp_grid = 6 6 6\n",
    )
    revised_lines = revised.splitlines()
    if any(revised_lines.count(value.rstrip("\n")) != 1 for value in unchanged):
        raise RuntimeError("unchanged localization control inventory changed")
    if revised_lines.count("dis_num_iter = 4000") != 1:
        raise RuntimeError("revised iteration budget is absent")
    forbidden = ("trial_step", "fixed_step", "guiding_centres")
    if any(value in revised for value in forbidden):
        raise RuntimeError("unexpected localization control present")
    if len(revised) != len(source):
        raise RuntimeError("iteration-budget substitution changed input length")
    return revised.encode("ascii")


def main() -> None:
    if PROPOSED_ROOT.exists():
        raise RuntimeError("proposed localization occurrence root already exists")
    for path, expected in EXPECTED.items():
        if not path.is_file() or path.is_symlink() or sha256(path) != expected:
            raise RuntimeError(f"identity mismatch: {path}")
    predecessor = json.loads(PREDECESSOR_CAMPAIGN.read_text(encoding="utf-8"))
    if (
        predecessor["provider_status"] != "output-ineligible"
        or predecessor["failure_class"]
        != "optimizer-disentanglement-convergence-failure"
    ):
        raise RuntimeError("predecessor is not the declared optimizer failure")
    trajectory = json.loads(PREDECESSOR_TRAJECTORY.read_text(encoding="utf-8"))
    disentanglement = trajectory["disentanglement"]
    if (
        disentanglement["final_iteration"] != 2000
        or disentanglement["final_absolute_fractional_delta"] != 4.679e-8
        or not disentanglement["iterations_1800_through_2000_monotonically_decreasing"]
    ):
        raise RuntimeError("predecessor trajectory no longer supports the amendment")
    revised = revised_input()
    prepared_root = ROOT / "prepared"
    if prepared_root.exists():
        shutil.rmtree(prepared_root)
    prepared_root.mkdir()
    with tempfile.TemporaryDirectory(prefix="ksd-c6-dis4000-") as temporary:
        source = Path(temporary) / "source"
        output = Path(temporary) / "output"
        source.mkdir()
        (source / "silicon.win").write_bytes(revised)
        for name, path in SOURCE_ARTIFACTS.items():
            shutil.copyfile(path, source / name)
        preparation = Wannier90LocalizationInputPreparer().prepare(
            source_directory=source,
            output_directory=output,
            seedname="silicon",
            kpoint_count=216,
            band_count=12,
            wannier_count=10,
            neighbor_count=8,
            parent_preprocessing_sha256=EXPECTED[PREPROCESSING_RESULT],
            parent_converter_sha256=EXPECTED[CONVERTER_RESULT],
        )
        shutil.copyfile(output / "silicon.win", prepared_root / "silicon.win")
        shutil.copyfile(
            preparation.manifest_path,
            prepared_root / "localization-input-manifest.json",
        )
    prepared_win = prepared_root / "silicon.win"
    prepared_manifest = prepared_root / "localization-input-manifest.json"
    if prepared_win.read_bytes() != revised:
        raise RuntimeError("prepared localization input changed")
    transformation = {
        "schema_version": 1,
        "source_input": identity(PREDECESSOR_INPUT),
        "revised_input": identity(prepared_win),
        "only_change": {
            "parameter": "dis_num_iter",
            "before": 2000,
            "after": 4000,
        },
        "change_class": "optimizer-eligibility iteration-budget extension",
        "fresh_occurrence": True,
        "checkpoint_consumed": False,
        "failed_outputs_consumed": False,
    }
    transformation_path = ROOT / "input-transformation.json"
    write_mapping(transformation_path, transformation)
    campaign = {
        "schema_version": 1,
        "status": "authorization-required",
        "execution_performed": False,
        "purpose": (
            "one fresh C6 optimizer-eligibility test changing only dis_num_iter "
            "from 2000 to 4000"
        ),
        "decision": identity(DECISION),
        "research_protocol": identity(PROTOCOL),
        "blocked_predecessor": {
            "campaign_result": identity(PREDECESSOR_CAMPAIGN),
            "trajectory_analysis": identity(PREDECESSOR_TRAJECTORY),
            "wout": identity(PREDECESSOR_WOUT),
        },
        "proposed_occurrence_root": str(PROPOSED_ROOT),
        "planned_command": [str(EXECUTABLE), "silicon"],
        "executable": {"version": "3.1.0", **identity(EXECUTABLE)},
        "projectkoios_provider": {
            "base_revision": "e146f3722e87ca2de2243421a94448cfa6e27037",
            "implementation": identity(PROVIDER_IMPLEMENTATION),
        },
        "parent_preprocessing_result": identity(PREPROCESSING_RESULT),
        "parent_converter_result": identity(CONVERTER_RESULT),
        "prepared_input": identity(prepared_win),
        "prepared_input_manifest": identity(prepared_manifest),
        "input_transformation": identity(transformation_path),
        "source_artifacts": {
            name: identity(path) for name, path in SOURCE_ARTIFACTS.items()
        },
        "candidate": {
            "seedname": "silicon",
            "kpoint_count": 216,
            "band_count": 12,
            "wannier_count": 10,
            "neighbor_count": 8,
            "outer_window_ev": [-5.85, 19.02],
            "frozen_window_ev": [-5.85, 8.0],
            "projections": ["Si:sp3", "Si:l=0:r=2"],
            "precond": True,
            "guiding_centres": False,
            "trial_step": 2.0,
            "trial_step_source": "native-default",
            "fixed_step": None,
            "num_cg_steps": 200,
            "num_iter": 4000,
            "conv_tol_angstrom_squared": 2e-9,
            "conv_window": 6,
            "dis_num_iter": 4000,
            "dis_mix_ratio": 0.2,
            "dis_conv_tol_fractional": 1e-10,
            "dis_conv_window": 3,
            "write_hr": True,
            "write_u_matrices": True,
            "fresh_occurrence": True,
            "checkpoint_consumed": False,
            "failed_outputs_consumed": False,
        },
        "resource_bounds": {
            "processes": 1,
            "timeout_seconds": TIMEOUT_SECONDS,
            "maximum_retained_bytes": MAXIMUM_BYTES,
            "maximum_invocations": 1,
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
        "stop_policy": (
            "if this 4000-step occurrence fails, no automatic budget extension or "
            "C8 escalation follows"
        ),
        "scientific_disposition": (
            "preflight only; no C6 localized operator or intended-use result"
        ),
    }
    campaign_path = ROOT / "campaign-preflight.json"
    write_mapping(campaign_path, campaign)
    request = {
        "schema_version": 1,
        "status": "authorization-required",
        "authorization_granted": False,
        "requested_occurrence": {
            "calculator": "Wannier90 3.1.0",
            "command": [str(EXECUTABLE), "silicon"],
            "executable_sha256": EXPECTED[EXECUTABLE],
            "input": identity(prepared_win),
            "input_manifest": identity(prepared_manifest),
            "source_artifacts": {
                name: identity(path) for name, path in SOURCE_ARTIFACTS.items()
            },
            "processes": 1,
            "timeout_seconds": TIMEOUT_SECONDS,
            "maximum_retained_bytes": MAXIMUM_BYTES,
            "maximum_invocations": 1,
            "retries": 0,
            "stop_on_failure": True,
        },
        "campaign_preflight": identity(campaign_path),
        "authorization_scope": (
            "one fresh local dis_num_iter=4000 localization invocation only; no retry, "
            "checkpoint use, further budget extension, C8, C12, direct-parent "
            "confirmation, component operator, or Slater-Koster reduction"
        ),
    }
    write_mapping(ROOT / "authorization-request.json", request)


if __name__ == "__main__":
    main()
