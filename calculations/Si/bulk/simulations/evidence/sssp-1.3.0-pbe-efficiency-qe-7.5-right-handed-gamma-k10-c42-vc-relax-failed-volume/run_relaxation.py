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
    "si-bulk-vc-relax-gamma-k10-c42-20261031T055443Z"
)
CONFIGURATION = ROOT / "calculation.toml"
EXECUTABLE = Path("/Users/eugene/projects/q-e-qe-7.5/build/bin/pw.x")
PSEUDOPOTENTIAL = Path(
    "/Users/eugene/opt/pseudopotentials/quantum-espresso/sssp/1.3.0/"
    "sets/PBE/efficiency/Si.pbe-n-rrkjus_psl.1.0.0.UPF"
)
TIMEOUT_SECONDS = 1800.0
MAXIMUM_RETAINED_BYTES = 2 * 1024**3


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
    manifest = {
        "schema_version": 1,
        "status": "authorized-not-started",
        "authorization": {
            "operator_message": "go",
            "maximum_invocations": 1,
            "retries": 0,
        },
        "projectkoios_revision": (
            "e146f3722e87ca2de2243421a94448cfa6e27037"
        ),
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
    rendered = (preflight.output_directory / "pw.in").read_text(encoding="ascii")
    required = (
        "calculation = 'vc-relax'",
        "nstep = 200",
        "ecutwfc = 42.0000000000",
        "ecutrho = 336.0000000000",
        "10 10 10 0 0 0",
        "press = 0.0000000000",
        "press_conv_thr = 0.5000000000",
        "cell_dofree = 'volume'",
    )
    if any(value not in rendered for value in required):
        raise RuntimeError("rendered relaxation input failed exact preflight")

    manifest["status"] = "authorized-preflight-passed"
    manifest["preflight_input"] = {
        "byte_size": (preflight.output_directory / "pw.in").stat().st_size,
        "sha256": sha256(preflight.output_directory / "pw.in"),
    }
    write_json(ROOT / "campaign-manifest.json", manifest)

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
    if (result.output_directory / "pw.in").read_bytes() != (
        preflight.output_directory / "pw.in"
    ).read_bytes():
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
    write_json(ROOT / "campaign-manifest.json", manifest)


if __name__ == "__main__":
    main()
