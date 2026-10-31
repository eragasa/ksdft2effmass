from __future__ import annotations

import hashlib
import json
from pathlib import Path

from projectkoios.integrations.wannier90 import (
    Wannier90LocalizationInputArtifact,
    Wannier90LocalizationInputManifest,
    Wannier90LocalizationInputRole,
    Wannier90LocalizationRunner,
    Wannier90LocalizationRunRequest,
    Wannier90NativeArtifactIdentity,
)

ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-wannier90-localization-sp3sstar-20261031T081246Z"
)
PREPARED = ROOT / "prepared-input"
MANIFEST_PATH = PREPARED / "localization-input-manifest.json"
PREFLIGHT = ROOT / "campaign-preflight.json"
AUTHORIZATION = ROOT / "authorization.json"
OUTPUT = ROOT / "run"
EXECUTABLE = Path("/Users/eugene/projects/wannier90-3.1.0/wannier90.x")
PREFLIGHT_SHA256 = "e2e47329bfb028cb930cc79c7a7227fdfd6475f7d21d2755e5ea97931c9a61d1"
MANIFEST_SHA256 = "3066ec192ace13bd5daee88d3c14367eef5d1c2d27021ce7335332dd5776387a"
EXECUTABLE_SHA256 = "c826f817f807cf069e16d6e529a52ddc15d2f677101065908bcb2030d7f7d1dd"
PREPROCESSING_SHA256 = (
    "d68e18bc9ee1138ca2e392198ab15b80e43ebf3ce319fb5ff0d7b772172191ee"
)
CONVERTER_SHA256 = "3e68cd8fd3b9b5438772bc73fbcae9d835ffd819ca6155aa9989703a28def823"
AUTHORIZATION_TEXT = (
    "Authorize exactly one Wannier90 localization invocation described in "
    "campaign-preflight.json, with zero retries and stop on failure."
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def identity(name: str) -> Wannier90NativeArtifactIdentity:
    path = PREPARED / name
    return Wannier90NativeArtifactIdentity(name, path.stat().st_size, sha256(path))


def main() -> None:
    if OUTPUT.exists():
        raise RuntimeError("localization output already exists; no retry is permitted")
    if sha256(PREFLIGHT) != PREFLIGHT_SHA256:
        raise RuntimeError("campaign preflight identity mismatch")
    if sha256(MANIFEST_PATH) != MANIFEST_SHA256:
        raise RuntimeError("prepared-input manifest identity mismatch")
    if sha256(EXECUTABLE) != EXECUTABLE_SHA256 or EXECUTABLE.stat().st_size != 891048:
        raise RuntimeError("wannier90.x identity mismatch")
    if not AUTHORIZATION.is_file() or AUTHORIZATION.is_symlink():
        raise PermissionError("bounded authorization record is absent")
    authorization = json.loads(AUTHORIZATION.read_text(encoding="utf-8"))
    required_authorization = {
        "authorization": AUTHORIZATION_TEXT,
        "campaign_preflight_sha256": PREFLIGHT_SHA256,
        "maximum_invocations": 1,
        "retries_authorized": 0,
        "stop_on_failure": True,
    }
    if authorization != required_authorization:
        raise PermissionError("authorization record does not match the bounded request")
    manifest = Wannier90LocalizationInputManifest(
        schema_version=1,
        seedname="silicon",
        kpoint_count=64,
        band_count=12,
        wannier_count=10,
        neighbor_count=8,
        parent_preprocessing_sha256=PREPROCESSING_SHA256,
        parent_converter_sha256=CONVERTER_SHA256,
        artifacts=(
            Wannier90LocalizationInputArtifact(
                Wannier90LocalizationInputRole.construction_input,
                identity("silicon.win"),
            ),
            Wannier90LocalizationInputArtifact(
                Wannier90LocalizationInputRole.preprocessing_topology,
                identity("silicon.nnkp"),
            ),
            Wannier90LocalizationInputArtifact(
                Wannier90LocalizationInputRole.eigenvalues,
                identity("silicon.eig"),
            ),
            Wannier90LocalizationInputArtifact(
                Wannier90LocalizationInputRole.projections,
                identity("silicon.amn"),
            ),
            Wannier90LocalizationInputArtifact(
                Wannier90LocalizationInputRole.neighbor_overlaps,
                identity("silicon.mmn"),
            ),
        ),
    )
    if manifest.to_json_bytes() != MANIFEST_PATH.read_bytes():
        raise RuntimeError("reconstructed manifest disagrees with prepared evidence")
    result = Wannier90LocalizationRunner().run(
        Wannier90LocalizationRunRequest(
            manifest=manifest,
            prepared_input_directory=PREPARED,
            manifest_path=MANIFEST_PATH,
            manifest_sha256=MANIFEST_SHA256,
            manifest_byte_count=MANIFEST_PATH.stat().st_size,
            output_directory=OUTPUT,
            executable=EXECUTABLE,
            executable_sha256=EXECUTABLE_SHA256,
            executable_byte_count=EXECUTABLE.stat().st_size,
            executable_version="3.1.0",
            timeout_seconds=300.0,
            maximum_retained_bytes=67108864,
            execution_authorized=True,
            kpoint_tolerance=1.0e-10,
            isometry_tolerance=1.0e-8,
            hamiltonian_hermiticity_tolerance=1.0e-8,
        )
    )
    campaign_result = {
        "schema_version": 1,
        "invocation_count": 1,
        "retry_count": 0,
        "execution_record": str(result.output_directory / "execution.json"),
        "artifact_manifest": str(result.artifact_manifest),
        "provider_result": str(result.provider_result),
        "scientific_disposition": (
            "provider-eligible localization output only; scientific interpolation "
            "and component-operator acceptance remain separate"
        ),
    }
    (ROOT / "campaign-result.json").write_text(
        json.dumps(campaign_result, allow_nan=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
