from __future__ import annotations

import hashlib
import importlib
import json
import shutil
from pathlib import Path

from projectkoios.integrations.quantumespresso.saved_state import (
    QeSavedStateCalculation,
    QeSavedStateManifestJsonCodec,
    QeSavedStateManifestVerifier,
)
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

_configuration = importlib.import_module(
    "projectkoios.integrations.quantumespresso.pw2wannier90.configuration"
)
_execution = importlib.import_module(
    "projectkoios.integrations.quantumespresso.pw2wannier90.execution"
)
_projection = importlib.import_module(
    "projectkoios.integrations.quantumespresso.pw2wannier90.projection"
)
_nnkp = importlib.import_module("projectkoios.integrations.wannier90.nnkp")
QePw2Wannier90InputConfiguration = _configuration.QePw2Wannier90InputConfiguration
QePw2Wannier90Mode = _configuration.QePw2Wannier90Mode
QePw2Wannier90SpinComponent = _configuration.QePw2Wannier90SpinComponent
QePw2Wannier90RunRequest = _execution.QePw2Wannier90RunRequest
QePw2Wannier90Runner = _execution.QePw2Wannier90Runner
QePw2Wannier90InputProjector = _projection.QePw2Wannier90InputProjector
Wannier90NnkpParser = _nnkp.Wannier90NnkpParser

ROOT = Path(__file__).resolve().parent
DECISION = ROOT.parents[1] / "wannier-interface-decision.md"
NSCF_ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier-nscf-6x6x6-b12-david-c6-v1"
)
NSCF_MANIFEST = NSCF_ROOT / "run/nscf-saved-state-manifest.json"
NSCF_SAVED_STATE_ROOT = NSCF_ROOT / "run/tmp"
PREPROCESSING_ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier90-preprocess-c6-lower-energy-frozen-v1"
)
NNKP = PREPROCESSING_ROOT / "run/silicon.nnkp"
PREPROCESSING_RESULT = PREPROCESSING_ROOT / "preprocessing-result.json"
EXECUTABLE = Path("/Users/eugene/projects/q-e-qe-7.5/build/bin/pw2wannier90.x")
PREFLIGHT_OUTPUT = ROOT / "rendered"
PROPOSED_ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-pw2wannier90-c6-lower-energy-frozen-v1"
)
EXPECTED = {
    DECISION: "d8e2730f5d857639a49dc2fd2eb3c2a9a291386f808e5525435a0602233fff56",
    NSCF_MANIFEST: ("28df04c1bf314371d6138bfe41b564147354253c6d609b465c7ebd4778c617b8"),
    NNKP: "f367195dcc42a72244104e8149bbc75b4ce623c67a6acc1d169c68b33aeffead",
    PREPROCESSING_RESULT: (
        "8306f8b7340e1673a79342a8725b4ad2bd63e96ea078929b423f6d72145538a4"
    ),
    EXECUTABLE: ("61c8255b0745df2a5dec3c55e600b1f8b87039b564004997ac45cfee42cf2c8c"),
}
TIMEOUT_SECONDS = 300.0
MAXIMUM_BYTES = 256 * 1024**2
SERIALIZER = TypedJsonMappingSerializer()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(path: Path) -> dict[str, object]:
    return {
        "path": str(path),
        "byte_size": path.stat().st_size,
        "sha256": sha256(path),
    }


def write_mapping(path: Path, payload: dict[str, object]) -> None:
    path.write_bytes(SERIALIZER.serialize(payload))


def configuration() -> object:
    return QePw2Wannier90InputConfiguration(
        prefix="system",
        outdir="./tmp/",
        seedname="silicon",
        spin_component=QePw2Wannier90SpinComponent.none,
        mode=QePw2Wannier90Mode.standalone,
        write_amn=True,
        write_mmn=True,
        write_unk=False,
        write_spn=False,
        input_filename="pw2wannier90.in",
        nnkp_filename="silicon.nnkp",
        nnkp_sha256=EXPECTED[NNKP],
        nnkp_byte_size=NNKP.stat().st_size,
        parent_nscf_saved_state_manifest_sha256=EXPECTED[NSCF_MANIFEST],
    )


def main() -> None:
    if PROPOSED_ROOT.exists():
        raise RuntimeError("proposed converter occurrence root already exists")
    for path, expected in EXPECTED.items():
        if not path.is_file() or path.is_symlink() or sha256(path) != expected:
            raise RuntimeError(f"identity mismatch: {path}")
    manifest = QeSavedStateManifestJsonCodec().loads(NSCF_MANIFEST.read_bytes())
    if manifest.calculation is not QeSavedStateCalculation.nscf:
        raise RuntimeError("converter parent is not an NSCF saved state")
    saved_state_paths = QeSavedStateManifestVerifier().verify(
        manifest, NSCF_SAVED_STATE_ROOT
    )
    parsed_nnkp = Wannier90NnkpParser().execute(NNKP.read_bytes())
    if (
        parsed_nnkp.kpoint_count != 216
        or parsed_nnkp.neighbor_count != 8
        or len(parsed_nnkp.neighbors) != 1728
        or len(parsed_nnkp.projections) != 10
        or parsed_nnkp.excluded_bands
    ):
        raise RuntimeError("NNKP does not satisfy the C6 converter declaration")
    preprocessing = json.loads(PREPROCESSING_RESULT.read_text(encoding="utf-8"))
    if not preprocessing["scientific_disposition"].startswith("eligible C6 NNKP"):
        raise RuntimeError("preprocessing result is not an eligible C6 handoff")
    projection = QePw2Wannier90InputProjector().project(configuration())
    if PREFLIGHT_OUTPUT.exists():
        shutil.rmtree(PREFLIGHT_OUTPUT)
    dry_run = QePw2Wannier90Runner().run(
        QePw2Wannier90RunRequest(
            projection=projection,
            output_directory=PREFLIGHT_OUTPUT,
            execute=False,
            timeout_seconds=TIMEOUT_SECONDS,
        )
    )
    rendered_input = dry_run.output_directory / projection.rendered_input.filename
    if rendered_input.read_text(encoding="ascii") != projection.rendered_input.text:
        raise RuntimeError("dry-run input differs from deterministic projection")
    campaign = {
        "schema_version": 1,
        "status": "authorization-required",
        "execution_performed": False,
        "purpose": (
            "C6 rank-10 AMN/MMN/EIG interface conversion with fixed spectral settings"
        ),
        "proposed_occurrence_root": str(PROPOSED_ROOT),
        "planned_command": [str(EXECUTABLE), "-in", "pw2wannier90.in"],
        "executable": identity(EXECUTABLE),
        "decision": identity(DECISION),
        "parent_nscf": {
            "manifest": identity(NSCF_MANIFEST),
            "saved_state_root": str(NSCF_SAVED_STATE_ROOT),
            "verified_file_count": len(saved_state_paths),
            "verified_total_bytes": sum(
                path.stat().st_size for path in saved_state_paths
            ),
        },
        "parent_preprocessing": {
            "nnkp": identity(NNKP),
            "result": identity(PREPROCESSING_RESULT),
            "kpoint_count": parsed_nnkp.kpoint_count,
            "projection_count": len(parsed_nnkp.projections),
            "neighbor_count_per_kpoint": parsed_nnkp.neighbor_count,
            "neighbor_record_count": len(parsed_nnkp.neighbors),
        },
        "input": identity(rendered_input),
        "input_manifest": identity(dry_run.input_manifest),
        "candidate": {
            "prefix": projection.prefix,
            "outdir": projection.outdir,
            "seedname": projection.seedname,
            "spin_component": "none",
            "mode": "standalone",
            "write_amn": True,
            "write_mmn": True,
            "write_unk": False,
            "write_spn": False,
            "required_outputs": list(projection.required_output_filenames),
        },
        "acceptance": {
            "required_return_code": 0,
            "required_native_completion": "JOB DONE",
            "required_outputs": list(projection.required_output_filenames),
            "required_mechanical_checks": [
                "regular nonempty AMN/MMN/EIG artifacts",
                "AMN rank and 216-point shape",
                "MMN rank, 216-point shape, and NNKP neighbor correlation",
                "EIG 12-band by 216-point shape",
                "finite numeric payloads",
            ],
        },
        "resource_bounds": {
            "processes": 1,
            "timeout_seconds": TIMEOUT_SECONDS,
            "maximum_retained_bytes": MAXIMUM_BYTES,
            "maximum_invocations": 1,
            "retries": 0,
        },
        "scientific_disposition": (
            "preflight only; no converter, localization, interpolation, or "
            "operator-adequacy result"
        ),
    }
    campaign_path = ROOT / "campaign-preflight.json"
    write_mapping(campaign_path, campaign)
    request = {
        "schema_version": 1,
        "status": "authorization-required",
        "authorization_granted": False,
        "requested_occurrence": {
            "calculator": "Quantum ESPRESSO 7.5 pw2wannier90.x",
            "command": [str(EXECUTABLE), "-in", "pw2wannier90.in"],
            "executable_sha256": EXPECTED[EXECUTABLE],
            "input": identity(rendered_input),
            "parent_nscf_manifest_sha256": EXPECTED[NSCF_MANIFEST],
            "nnkp_sha256": EXPECTED[NNKP],
            "processes": 1,
            "timeout_seconds": TIMEOUT_SECONDS,
            "maximum_retained_bytes": MAXIMUM_BYTES,
            "maximum_invocations": 1,
            "retries": 0,
            "stop_on_failure": True,
        },
        "campaign_preflight": identity(campaign_path),
        "authorization_scope": (
            "one local converter invocation only; no retry, localization, C8, C12, "
            "or confirmation-parent evaluation"
        ),
    }
    write_mapping(ROOT / "authorization-request.json", request)


if __name__ == "__main__":
    main()
