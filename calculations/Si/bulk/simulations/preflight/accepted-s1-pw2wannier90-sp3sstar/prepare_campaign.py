from __future__ import annotations

import hashlib
import importlib
import json
from pathlib import Path

from projectkoios.integrations.quantumespresso.saved_state import (
    QeSavedStateCalculation,
    QeSavedStateManifestJsonCodec,
    QeSavedStateManifestVerifier,
)
from projectkoios.physkit import units as _physkit_units

if not hasattr(_physkit_units, "ModelSystemUnitConverter"):
    _physkit_units.ModelSystemUnitConverter = _physkit_units.MODEL_SYSTEM_UNIT_CONVERTER

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

ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-pw2wannier90-sp3sstar-20261031T074802Z"
)
KSD_ROOT = Path("/Users/eugene/worktrees/ksdft2effmass-si-right-handed-kpoint")
DECISION = KSD_ROOT / "calculations/Si/bulk/simulations/wannier-interface-decision.md"
NSCF_ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier-nscf-4x4x4-b12-david-20261031T072258Z"
)
NSCF_MANIFEST = NSCF_ROOT / "run/nscf-saved-state-manifest.json"
NSCF_SAVED_STATE_ROOT = NSCF_ROOT / "run/tmp"
PREPROCESSING_ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier90-preprocess-sp3sstar-20261031T073157Z"
)
NNKP = PREPROCESSING_ROOT / "run/silicon.nnkp"
PREPROCESSING_RESULT = PREPROCESSING_ROOT / "preprocessing-result.json"
EXECUTABLE = Path("/Users/eugene/projects/q-e-qe-7.5/build/bin/pw2wannier90.x")
PREFLIGHT_OUTPUT = ROOT / "preflight-output"
DECISION_SHA256 = "76b53356bb8aff1bfc7915900a7e8a3b4bab5bb724bb4a43bbb34e85dd01a152"
NSCF_MANIFEST_SHA256 = (
    "cab588c939b3b9bdea95496458be414f465f38fb036d1ade62405f8d602bf4ce"
)
NNKP_SHA256 = "4dd17877e0f3bc0b19a0f74ce539a91bd8ceb1c66a18d3f733f08e5d8ce07014"
EXECUTABLE_SHA256 = "61c8255b0745df2a5dec3c55e600b1f8b87039b564004997ac45cfee42cf2c8c"
TIMEOUT_SECONDS = 300.0
MAXIMUM_BYTES = 256 * 1024**2


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def observation(path: Path) -> dict[str, object]:
    return {"path": str(path), "byte_size": path.stat().st_size, "sha256": sha256(path)}


def write_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, allow_nan=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def configuration() -> QePw2Wannier90InputConfiguration:
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
        nnkp_sha256=NNKP_SHA256,
        nnkp_byte_size=NNKP.stat().st_size,
        parent_nscf_saved_state_manifest_sha256=NSCF_MANIFEST_SHA256,
    )


def main() -> None:
    if any(path.name != "prepare_campaign.py" for path in ROOT.iterdir()):
        raise RuntimeError("preflight root must contain only prepare_campaign.py")
    for path, expected, label in (
        (DECISION, DECISION_SHA256, "interface decision"),
        (NSCF_MANIFEST, NSCF_MANIFEST_SHA256, "NSCF manifest"),
        (NNKP, NNKP_SHA256, "NNKP"),
        (EXECUTABLE, EXECUTABLE_SHA256, "converter executable"),
    ):
        if not path.is_file() or path.is_symlink() or sha256(path) != expected:
            raise RuntimeError(f"{label} identity mismatch")
    manifest = QeSavedStateManifestJsonCodec().loads(NSCF_MANIFEST.read_bytes())
    if manifest.calculation is not QeSavedStateCalculation.nscf:
        raise RuntimeError("converter parent is not an NSCF saved state")
    saved_state_paths = QeSavedStateManifestVerifier().verify(
        manifest, NSCF_SAVED_STATE_ROOT
    )
    parsed_nnkp = Wannier90NnkpParser().execute(NNKP.read_bytes())
    if (
        parsed_nnkp.kpoint_count != 64
        or len(parsed_nnkp.projections) != 10
        or parsed_nnkp.excluded_bands
    ):
        raise RuntimeError("NNKP does not satisfy the converter declaration")
    preprocessing = json.loads(PREPROCESSING_RESULT.read_text(encoding="utf-8"))
    if preprocessing["scientific_disposition"].startswith("Eligible NNKP") is False:
        raise RuntimeError("preprocessing result is not an eligible candidate handoff")
    projection = QePw2Wannier90InputProjector().project(configuration())
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
    write_json(
        ROOT / "campaign-preflight.json",
        {
            "schema_version": 1,
            "status": "awaiting-explicit-bounded-authorization",
            "execution_performed": False,
            "authorization_request": {
                "maximum_invocations": 1,
                "retries": 0,
                "stop_on_failure": True,
            },
            "purpose": "first rank-10 AMN/MMN/EIG interface conversion qualification",
            "scientific_disposition": (
                "preflight only; no converter, localization, interpolation, or "
                "operator-adequacy result"
            ),
            "projectkoios_revision": "e146f3722e87ca2de2243421a94448cfa6e27037",
            "planned_command": [str(EXECUTABLE), "-in", "pw2wannier90.in"],
            "executable": observation(EXECUTABLE),
            "decision": observation(DECISION),
            "parent_nscf": {
                "manifest": observation(NSCF_MANIFEST),
                "saved_state_root": str(NSCF_SAVED_STATE_ROOT),
                "verified_file_count": len(saved_state_paths),
                "verified_total_bytes": sum(
                    path.stat().st_size for path in saved_state_paths
                ),
            },
            "parent_preprocessing": {
                "nnkp": observation(NNKP),
                "result": observation(PREPROCESSING_RESULT),
                "kpoint_count": parsed_nnkp.kpoint_count,
                "projection_count": len(parsed_nnkp.projections),
                "neighbor_count_per_kpoint": parsed_nnkp.neighbor_count,
            },
            "input": observation(rendered_input),
            "input_manifest": observation(dry_run.input_manifest),
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
                "coefficient_evidence": (
                    "authenticated native QE wavefunction inventory retained in the "
                    "Davidson NSCF saved state"
                ),
            },
            "acceptance": {
                "required_return_code": 0,
                "required_native_completion": "JOB DONE",
                "required_outputs": list(projection.required_output_filenames),
                "required_mechanical_checks": [
                    "regular nonempty AMN/MMN/EIG artifacts",
                    "AMN rank and 64-point shape",
                    "MMN rank, 64-point shape, and NNKP neighbor correlation",
                    "EIG 12-band by 64-point shape",
                    "finite numeric payloads",
                ],
            },
            "resource_bounds": {
                "processes": 1,
                "timeout_seconds": TIMEOUT_SECONDS,
                "maximum_retained_bytes": MAXIMUM_BYTES,
            },
        },
    )


if __name__ == "__main__":
    main()
