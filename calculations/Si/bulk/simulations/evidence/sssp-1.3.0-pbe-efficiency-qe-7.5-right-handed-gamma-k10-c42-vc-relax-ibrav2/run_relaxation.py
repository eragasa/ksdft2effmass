from __future__ import annotations

import hashlib
import json
from pathlib import Path

from projectkoios.integrations.quantumespresso.pw.relaxation.execution import (
    QeRelaxationCalculationRunRequest,
    QeRelaxationCalculationRunner,
)

ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-bulk-vc-relax-ibrav2-gamma-k10-c42-20261031T061128Z"
)
CONFIGURATION = ROOT / "calculation.toml"
EXECUTABLE = Path("/Users/eugene/projects/q-e-qe-7.5/build/bin/pw.x")
PSEUDOPOTENTIAL = Path(
    "/Users/eugene/opt/pseudopotentials/quantum-espresso/sssp/1.3.0/"
    "sets/PBE/efficiency/Si.pbe-n-rrkjus_psl.1.0.0.UPF"
)
TIMEOUT_SECONDS = 1800.0
MAXIMUM_RETAINED_BYTES = 2 * 1024**3
EXPECTED_INPUT_SHA256 = (
    "512d3a35f663db7cf74ef58119942ed0eb8c598fb8fc907b698ed82383c29329"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_size(path: Path) -> int:
    return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())


def write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    patch = ROOT / "projectkoios-fcc-vc-relax.patch"
    manifest: dict[str, object] = {
        "schema_version": 1,
        "status": "authorized-not-started",
        "authorization": {
            "operator_message": "recommendation authorized",
            "maximum_invocations": 1,
            "retries": 0,
        },
        "projectkoios": {
            "base_revision": "e146f3722e87ca2de2243421a94448cfa6e27037",
            "worktree": (
                "/Users/eugene/worktrees/"
                "projectkoios-simulations-qe-fcc-vc-relax"
            ),
            "patch_byte_size": patch.stat().st_size,
            "patch_sha256": sha256(patch),
        },
        "configuration": {
            "path": str(CONFIGURATION),
            "byte_size": CONFIGURATION.stat().st_size,
            "sha256": sha256(CONFIGURATION),
        },
        "resources": {
            "processes": 1,
            "timeout_seconds": TIMEOUT_SECONDS,
            "maximum_retained_bytes": MAXIMUM_RETAINED_BYTES,
        },
        "scientific_disposition": (
            "provisional bulk relaxation; completion is not scientific acceptance"
        ),
        "native_diagnostic_disposition": (
            "QE IEEE flags are retained as native diagnostics and are not an "
            "automatic blocker absent non-finite results, failed convergence, or "
            "corrupted output"
        ),
    }
    write_json(ROOT / "campaign-manifest.json", manifest)

    runner = QeRelaxationCalculationRunner()
    preflight = runner.run(
        QeRelaxationCalculationRunRequest(
            configuration_path=CONFIGURATION,
            output_directory=ROOT / "preflight",
            execute=False,
            timeout_seconds=TIMEOUT_SECONDS,
        )
    )
    input_path = preflight.output_directory / "pw.in"
    rendered = input_path.read_text(encoding="ascii")
    required = (
        "calculation = 'vc-relax'",
        "nstep = 200",
        "ibrav = 2",
        "A = 5.4300000000",
        "ecutwfc = 42.0000000000",
        "ecutrho = 336.0000000000",
        "Si 0.7500000000 0.7500000000 0.7500000000",
        "10 10 10 0 0 0",
        "press = 0.0000000000",
        "press_conv_thr = 0.5000000000",
        "cell_dofree = 'ibrav'",
    )
    forbidden = ("ibrav = 0", "CELL_PARAMETERS", "cell_dofree = 'all'")
    if any(value not in rendered for value in required) or any(
        value in rendered for value in forbidden
    ):
        raise RuntimeError("rendered relaxation input failed exact preflight")
    if sha256(input_path) != EXPECTED_INPUT_SHA256:
        raise RuntimeError("rendered relaxation input identity changed")

    manifest["status"] = "authorized-preflight-passed"
    manifest["preflight_input"] = {
        "byte_size": input_path.stat().st_size,
        "sha256": sha256(input_path),
    }
    write_json(ROOT / "campaign-manifest.json", manifest)

    # This is the sole authorized calculator invocation. There is no retry path.
    result = runner.run(
        QeRelaxationCalculationRunRequest(
            configuration_path=CONFIGURATION,
            output_directory=ROOT / "run",
            execute=True,
            executable=EXECUTABLE,
            pseudopotential=PSEUDOPOTENTIAL,
            timeout_seconds=TIMEOUT_SECONDS,
        )
    )
    if (result.output_directory / "pw.in").read_bytes() != input_path.read_bytes():
        raise RuntimeError("executed input differs from preflight input")
    retained_bytes = tree_size(result.output_directory)
    if retained_bytes > MAXIMUM_RETAINED_BYTES:
        raise RuntimeError("relaxation output exceeded retained-byte bound")
    execution = json.loads(
        (result.output_directory / "execution.json").read_text(encoding="utf-8")
    )
    manifest["status"] = "completed"
    manifest["output_directory"] = str(result.output_directory)
    manifest["retained_bytes"] = retained_bytes
    manifest["execution_status"] = execution["status"]
    manifest["return_code"] = execution["returncode"]
    write_json(ROOT / "campaign-manifest.json", manifest)


if __name__ == "__main__":
    main()
