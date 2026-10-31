from __future__ import annotations

import hashlib
import importlib
import json
import shutil
import tempfile
from collections import Counter
from pathlib import Path

import numpy as np
from projectkoios.physkit import units as _physkit_units

if not hasattr(_physkit_units, "ModelSystemUnitConverter"):
    _physkit_units.ModelSystemUnitConverter = (  # type: ignore[attr-defined]
        _physkit_units.MODEL_SYSTEM_UNIT_CONVERTER
    )
if not hasattr(_physkit_units, "MODEL_SYSTEM_UNIT_CONVERTER"):
    _physkit_units.MODEL_SYSTEM_UNIT_CONVERTER = (  # type: ignore[attr-defined]
        _physkit_units.ModelSystemUnitConverter
    )

from projectkoios.physkit.units import PhysicalUnit  # noqa: E402

from ksdft2effmass.serialization import TypedJsonMappingSerializer  # noqa: E402

_wannier90 = importlib.import_module("projectkoios.integrations.wannier90")
Wannier90EigenvalueParser = _wannier90.Wannier90EigenvalueParser
Wannier90LocalizationInputPreparer = _wannier90.Wannier90LocalizationInputPreparer

ROOT = Path(__file__).resolve().parent
DECISION = ROOT.parents[1] / "c6-t1-full-parent-band-outer-window-decision.md"
PROTOCOL = ROOT.parents[2] / "research-protocol/research-protocol.tex"
SOURCE_PREFLIGHT = ROOT.parent / (
    "accepted-s1-wannier90-localization-c6-lower-energy-frozen-dis4000"
)
SOURCE_INPUT = SOURCE_PREFLIGHT / "prepared/silicon.win"
SOURCE_MANIFEST = SOURCE_PREFLIGHT / "prepared/localization-input-manifest.json"
BLOCKED_ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier90-localization-c6-lower-energy-frozen-dis4000-v1"
)
BLOCKED_CAMPAIGN = BLOCKED_ROOT / "campaign-result.json"
BLOCKED_TRAJECTORY = BLOCKED_ROOT / "trajectory-analysis.json"
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
    "si-accepted-s1-wannier90-localization-c6-t1-full-parent-outer-dis4000-v1"
)
EXPECTED = {
    DECISION: "9162165b70acf163c6af8e495c1714cae0f78bee1a8d96b3571c9268c43c475e",
    PROTOCOL: "d60b773b996e5c24b8333c0e4e919860b2dc8164504d581ac91ccfa208a59cbc",
    SOURCE_INPUT: ("2ddfb1b51cfd476cc6444f8bfec8ae3ef229e882c2e6e5f1ee5bf94addd43e64"),
    SOURCE_MANIFEST: (
        "d285df27cf085c61112bc9c0d79c4056b710708e379359ecb838b793272aee48"
    ),
    BLOCKED_CAMPAIGN: (
        "96065b18d11e7425b3ce6c9737a787d499b45d3822a4f59797df99f588290857"
    ),
    BLOCKED_TRAJECTORY: (
        "bdb9e865a2cbdf81e079cd2b6b9563777e34b0a32d08a5acebba0d996c953d39"
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
_ELECTRON_VOLT = PhysicalUnit("eV")


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
    source = SOURCE_INPUT.read_text(encoding="ascii")
    replacements = {
        "dis_win_min = -5.85\n": "dis_win_min = -6.0\n",
        "dis_win_max = 19.02\n": "dis_win_max = 21.0\n",
    }
    revised = source
    for old, new in replacements.items():
        if revised.count(old) != 1 or new in revised:
            raise RuntimeError(f"outer-window inventory changed: {old.strip()}")
        revised = revised.replace(old, new)
    unchanged = (
        "num_bands = 12",
        "num_wann = 10",
        "num_iter = 4000",
        "conv_tol = 2e-09",
        "conv_window = 6",
        "dis_froz_min = -5.85",
        "dis_froz_max = 8",
        "dis_num_iter = 4000",
        "dis_conv_tol = 1e-10",
        "dis_conv_window = 3",
        "dis_mix_ratio = 0.2",
        "write_hr = .true.",
        "write_u_matrices = .true.",
        "precond = .true.",
        "num_cg_steps = 200",
        "mp_grid = 6 6 6",
    )
    lines = revised.splitlines()
    if any(lines.count(value) != 1 for value in unchanged):
        raise RuntimeError("unchanged target or optimizer inventory changed")
    forbidden = ("trial_step", "fixed_step", "guiding_centres")
    if any(value in revised for value in forbidden):
        raise RuntimeError("unexpected localization control present")
    if len(lines[lines.index("begin kpoints") + 1 : lines.index("end kpoints")]) != 216:
        raise RuntimeError("construction mesh inventory changed")
    return revised.encode("ascii")


def main() -> None:
    if PROPOSED_ROOT.exists():
        raise RuntimeError("proposed C6-T1 occurrence root already exists")
    for path, expected in EXPECTED.items():
        if not path.is_file() or path.is_symlink() or sha256(path) != expected:
            raise RuntimeError(f"identity mismatch: {path}")
    blocked = json.loads(BLOCKED_CAMPAIGN.read_text(encoding="utf-8"))
    if blocked["failure_class"] != "optimizer-wannierisation-convergence-failure":
        raise RuntimeError("blocked predecessor classification changed")
    eigenvalues = (
        Wannier90EigenvalueParser()
        .execute(SOURCE_ARTIFACTS["silicon.eig"].read_bytes(), _ELECTRON_VOLT)
        .eigenvalues.magnitude
    )
    source_outer_counts = np.sum(
        (eigenvalues >= -5.85) & (eigenvalues <= 19.02), axis=1
    )
    revised_outer_counts = np.sum((eigenvalues >= -6.0) & (eigenvalues <= 21.0), axis=1)
    frozen_counts = np.sum((eigenvalues >= -5.85) & (eigenvalues <= 8.0), axis=1)
    if Counter(int(value) for value in source_outer_counts) != Counter(
        {10: 12, 11: 62, 12: 142}
    ):
        raise RuntimeError("source outer-window inventory changed")
    if not np.all(revised_outer_counts == 12):
        raise RuntimeError("C6-T1 outer window does not include all 12 parent bands")
    if Counter(int(value) for value in frozen_counts) != Counter({4: 129, 5: 84, 6: 3}):
        raise RuntimeError("frozen-window inventory changed")
    revised = revised_input()
    prepared_root = ROOT / "prepared"
    if prepared_root.exists():
        shutil.rmtree(prepared_root)
    prepared_root.mkdir()
    with tempfile.TemporaryDirectory(prefix="ksd-c6-t1-") as temporary:
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
        raise RuntimeError("prepared C6-T1 input changed")
    transformation = {
        "schema_version": 1,
        "source_input": identity(SOURCE_INPUT),
        "revised_input": identity(prepared_win),
        "only_change": {
            "coordinate": "outer_window_ev",
            "before": [-5.85, 19.02],
            "after": [-6.0, 21.0],
        },
        "change_class": "target-space outer-envelope redesign",
        "fresh_occurrence": True,
        "checkpoint_consumed": False,
        "failed_outputs_consumed": False,
    }
    transformation_path = ROOT / "input-transformation.json"
    write_mapping(transformation_path, transformation)
    window_analysis = {
        "schema_version": 1,
        "eigenvalue_artifact": identity(SOURCE_ARTIFACTS["silicon.eig"]),
        "energy_unit": "eV",
        "eigenvalue_range_ev": [float(np.min(eigenvalues)), float(np.max(eigenvalues))],
        "source_outer_window_ev": [-5.85, 19.02],
        "source_outer_count_histogram": {
            str(key): value
            for key, value in sorted(Counter(source_outer_counts).items())
        },
        "revised_outer_window_ev": [-6.0, 21.0],
        "revised_outer_count_histogram": {"12": 216},
        "all_twelve_parent_bands_included_at_every_kpoint": True,
        "lower_guard_margin_ev": float(np.min(eigenvalues) - (-6.0)),
        "upper_guard_margin_ev": float(21.0 - np.max(eigenvalues)),
        "frozen_window_ev": [-5.85, 8.0],
        "frozen_count_histogram": {
            str(key): value for key, value in sorted(Counter(frozen_counts).items())
        },
    }
    window_path = ROOT / "target-space-analysis.json"
    write_mapping(window_path, window_analysis)
    campaign = {
        "schema_version": 1,
        "status": "authorization-required",
        "execution_performed": False,
        "purpose": (
            "fresh C6-T1 target-space test changing only the outer window so all 12 "
            "authenticated parent bands are included at every construction point"
        ),
        "decision": identity(DECISION),
        "research_protocol": identity(PROTOCOL),
        "blocked_predecessor": {
            "campaign_result": identity(BLOCKED_CAMPAIGN),
            "trajectory_analysis": identity(BLOCKED_TRAJECTORY),
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
        "target_space_analysis": identity(window_path),
        "source_artifacts": {
            name: identity(path) for name, path in SOURCE_ARTIFACTS.items()
        },
        "candidate": {
            "candidate_id": "C6-T1",
            "seedname": "silicon",
            "kpoint_count": 216,
            "band_count": 12,
            "wannier_count": 10,
            "neighbor_count": 8,
            "outer_window_ev": [-6.0, 21.0],
            "outer_state_count_per_kpoint": 12,
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
            "if C6-T1 fails provider eligibility, no automatic optimizer tuning or "
            "C8 escalation follows"
        ),
        "scientific_disposition": (
            "preflight only; no C6-T1 localized operator or intended-use result"
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
            "one fresh local C6-T1 localization invocation only; no retry, checkpoint "
            "use, optimizer tuning, C8, C12, direct-parent confirmation, component "
            "operator, or Slater-Koster reduction"
        ),
    }
    write_mapping(ROOT / "authorization-request.json", request)


if __name__ == "__main__":
    main()
