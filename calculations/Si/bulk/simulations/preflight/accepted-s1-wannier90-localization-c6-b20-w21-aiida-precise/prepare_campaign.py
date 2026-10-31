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
SIMULATIONS = ROOT.parents[1]
PROTOCOL = ROOT.parents[2] / "research-protocol/research-protocol.tex"
TARGET_DECISION = SIMULATIONS / "c6-b20-w21-outer-window-decision.md"
CONVERGENCE_DECISION = SIMULATIONS / "aiida-precise-convergence-adaptation-decision.md"
PREPROCESSING_ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier90-preprocess-c6-b20-w21-aiida-precise-v1"
)
PREPROCESSING_INPUT = PREPROCESSING_ROOT / "input/silicon.win"
PREPROCESSING_RESULT = PREPROCESSING_ROOT / "preprocessing-result.json"
CONVERTER_ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-pw2wannier90-c6-b20-w21-aiida-precise-v1"
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
    "si-accepted-s1-wannier90-localization-c6-b20-w21-aiida-precise-v1"
)
PREPARED_ROOT = ROOT / "prepared"
EXPECTED = {
    PROTOCOL: "230aa0cebb37cf28a2e2e7cdcf1186d5ded98971217be3bbb8beadc2879d9dad",
    TARGET_DECISION: (
        "526b0a265b306c13f9ae54ce34c57030277f15704a4a571295da43330005db59"
    ),
    CONVERGENCE_DECISION: (
        "9d2e8269d1f2351d1c3b3228c24f4b2baad6505c1c1039da8889412b3cba6238"
    ),
    PREPROCESSING_INPUT: (
        "b48069e4f8ecd7209a318c47c77691de063bd0575658eb88a1e662a359d3dcc8"
    ),
    PREPROCESSING_RESULT: (
        "ca73c8e0384e5f8b3bccffbe1ab1b2e58d636876f802b380a06eec74f8c50e93"
    ),
    CONVERTER_RESULT: (
        "b8cc1b5df05fdda09fbbad13374635aed08aa630d11b16d554010f12ed8ed37a"
    ),
    SOURCE_ARTIFACTS["silicon.nnkp"]: (
        "608b8e0aacb8adddcfc2b8e0090ce48f5b916aec0d321bb69aabf01af9462575"
    ),
    SOURCE_ARTIFACTS["silicon.eig"]: (
        "a54f31f8f72cd32b63ad78e47378cd0a8ce97474ad223606f88d48c97c890dd2"
    ),
    SOURCE_ARTIFACTS["silicon.amn"]: (
        "9186cd5b8802bede18f81b96188f0a2035eb97565c2f811f5ca7769f2ebefece"
    ),
    SOURCE_ARTIFACTS["silicon.mmn"]: (
        "f81833fe7476426c15b690774214b4d07acaa2ffa93b1facb8ceb78c44ab6074"
    ),
    EXECUTABLE: "c826f817f807cf069e16d6e529a52ddc15d2f677101065908bcb2030d7f7d1dd",
    PROVIDER_IMPLEMENTATION: (
        "3080b663b8801968ebaea75b9cc55ab9bfb7ea17150f3e35dc47387ee8dbaaaa"
    ),
}
TIMEOUT_SECONDS = 14_400.0
MAXIMUM_BYTES = 128 * 1024**2
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


def localization_input() -> bytes:
    source = PREPROCESSING_INPUT.read_text(encoding="ascii")
    marker = "write_hr = .true.\n"
    additions = (
        "write_hr = .true.\n"
        "write_u_matrices = .true.\n"
        "precond = .true.\n"
        "num_cg_steps = 200\n"
    )
    if source.count(marker) != 1:
        raise RuntimeError("preprocessing write_hr inventory changed")
    forbidden_existing = (
        "write_u_matrices",
        "precond",
        "num_cg_steps",
        "trial_step",
        "fixed_step",
        "guiding_centres",
    )
    if any(value in source for value in forbidden_existing):
        raise RuntimeError("preprocessing input contains localization-only controls")
    prepared = source.replace(marker, additions)
    required = (
        "num_bands = 20",
        "num_wann = 10",
        "num_iter = 40000",
        "conv_tol = 2e-09",
        "conv_window = 6",
        "dis_win_min = -6",
        "dis_win_max = 21",
        "dis_froz_min = -5.85",
        "dis_froz_max = 8",
        "dis_num_iter = 40000",
        "dis_conv_tol = 2e-09",
        "dis_conv_window = 3",
        "dis_mix_ratio = 0.2",
        "write_hr = .true.",
        "write_u_matrices = .true.",
        "precond = .true.",
        "num_cg_steps = 200",
        "mp_grid = 6 6 6",
    )
    lines = prepared.splitlines()
    if any(lines.count(value) != 1 for value in required):
        raise RuntimeError("precise localization control inventory changed")
    return prepared.encode("ascii")


def main() -> None:
    if PROPOSED_ROOT.exists():
        raise RuntimeError("proposed localization occurrence root already exists")
    for path, expected in EXPECTED.items():
        if not path.is_file() or path.is_symlink() or sha256(path) != expected:
            raise RuntimeError(f"identity mismatch: {path}")
    preprocessing = json.loads(PREPROCESSING_RESULT.read_text(encoding="utf-8"))
    converter = json.loads(CONVERTER_RESULT.read_text(encoding="utf-8"))
    if not preprocessing["scientific_disposition"].startswith(
        "eligible C6-B20-W21 AiiDA-precise NNKP"
    ):
        raise RuntimeError("preprocessing result is not eligible")
    if not converter["scientific_disposition"].startswith(
        "eligible C6-B20-W21 20-band AMN/MMN/EIG"
    ):
        raise RuntimeError("converter result is not eligible")

    prepared_input = localization_input()
    if PREPARED_ROOT.exists():
        shutil.rmtree(PREPARED_ROOT)
    PREPARED_ROOT.mkdir()
    with tempfile.TemporaryDirectory(
        prefix="ksd-c6-b20-w21-localization-"
    ) as temporary:
        temporary_root = Path(temporary)
        source = temporary_root / "source"
        output = temporary_root / "output"
        source.mkdir()
        (source / "silicon.win").write_bytes(prepared_input)
        for name, path in SOURCE_ARTIFACTS.items():
            shutil.copyfile(path, source / name)
        preparation = Wannier90LocalizationInputPreparer().prepare(
            source_directory=source,
            output_directory=output,
            seedname="silicon",
            kpoint_count=216,
            band_count=20,
            wannier_count=10,
            neighbor_count=8,
            parent_preprocessing_sha256=EXPECTED[PREPROCESSING_RESULT],
            parent_converter_sha256=EXPECTED[CONVERTER_RESULT],
        )
        shutil.copyfile(output / "silicon.win", PREPARED_ROOT / "silicon.win")
        shutil.copyfile(
            preparation.manifest_path,
            PREPARED_ROOT / "localization-input-manifest.json",
        )

    prepared_win = PREPARED_ROOT / "silicon.win"
    prepared_manifest = PREPARED_ROOT / "localization-input-manifest.json"
    if prepared_win.read_bytes() != prepared_input:
        raise RuntimeError("prepared localization input changed")

    transformation = {
        "schema_version": 1,
        "source_preprocessing_input": identity(PREPROCESSING_INPUT),
        "prepared_localization_input": identity(prepared_win),
        "added_localization_only_controls": {
            "write_u_matrices": True,
            "precond": True,
            "num_cg_steps": 200,
        },
        "unchanged_precise_convergence_controls": {
            "num_iter": 40000,
            "conv_tol_angstrom_squared": 2e-9,
            "conv_window": 6,
            "dis_num_iter": 40000,
            "dis_conv_tol_dimensionless": 2e-9,
        },
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
            "one fresh C6-B20-W21 localization eligibility occurrence using the "
            "pinned AiiDA precise convergence-derived tuple"
        ),
        "research_protocol": identity(PROTOCOL),
        "target_space_decision": identity(TARGET_DECISION),
        "convergence_adaptation_decision": identity(CONVERGENCE_DECISION),
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
            "candidate_id": "C6-B20-W21",
            "convergence_profile": "pinned-aiida-precise-two-atom-adaptation",
            "seedname": "silicon",
            "kpoint_count": 216,
            "band_count": 20,
            "wannier_count": 10,
            "neighbor_count": 8,
            "outer_window_ev": [-6.0, 21.0],
            "frozen_window_ev": [-5.85, 8.0],
            "projections": ["Si:sp3", "Si:l=0:r=2"],
            "precond": True,
            "guiding_centres": False,
            "trial_step": 2.0,
            "trial_step_source": "native-default",
            "fixed_step": None,
            "num_cg_steps": 200,
            "num_iter": 40000,
            "conv_tol_angstrom_squared": 2e-9,
            "conv_window": 6,
            "dis_num_iter": 40000,
            "dis_mix_ratio": 0.2,
            "dis_conv_tol_dimensionless": 2e-9,
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
            "basis": (
                "the blocked 12-band 4000+4000-step C6 occurrence required 359.302 "
                "seconds; scaling its measured per-iteration cost by (20/12)^2 and "
                "both precise 40000-step ceilings gives a conservative four-hour "
                "single-process bound"
            ),
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
            "if this occurrence fails provider eligibility, no automatic retry, "
            "budget extension, C6-B30, C8, or C12 follows"
        ),
        "scientific_disposition": (
            "preflight only; no localized operator, optimizer result, or "
            "intended-use result"
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
            "checkpoint_consumed": False,
            "failed_outputs_consumed": False,
        },
        "campaign_preflight": identity(campaign_path),
        "authorization_scope": (
            "one fresh local C6-B20-W21 precise-profile localization invocation only; "
            "no retry, checkpoint use, failed-output use, further budget extension, "
            "C6-B30, C8, C12, confirmation, component operator, or Slater-Koster "
            "reduction"
        ),
    }
    write_mapping(ROOT / "authorization-request.json", request)


if __name__ == "__main__":
    main()
