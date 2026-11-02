"""Execute the single authorized accepted-S1 parent DFT band-path occurrence."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "input" / "pw.in"
OCCURRENCE = ROOT / "occurrence"
RESULT = ROOT / "result"
EXECUTABLE = Path("/Users/eugene/projects/q-e-qe-7.5/build/bin/pw.x")
SOURCE_RUN = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-parent-scf-gamma-k10-c42-20261031T070321Z/run"
)
EXTERNAL_ROOT = Path(
    "/Users/eugene/projects/ksdft2effmass/"
    "si-accepted-s1-parent-bands-l-gamma-x-gamma-b20-20261102T202436Z"
)
EXPECTED_EXECUTABLE = "87aa72158e2c103c63fce1deca977dc42ff4ba344519a9662aadb96d33eab910"
EXPECTED_INPUT = "a8c1a511949effceae4ef3581ca2a0adc1bbea9330c0dd2fdff65e5f62fda856"
EXPECTED_PSEUDO = "ae3aefd0811f9499dbc4a72f1f9ae02ef4fc7f3568bf6f559b68668719c69e2b"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def identity(path: Path) -> dict[str, str | int]:
    return {"path": str(path), "byte_size": path.stat().st_size, "sha256": sha256(path)}


def main() -> None:
    execution_path = OCCURRENCE / "execution.json"
    if execution_path.exists() or EXTERNAL_ROOT.exists():
        raise RuntimeError("authorized occurrence already exists; retry is forbidden")
    pseudo = SOURCE_RUN / "Si.pbe-n-rrkjus_psl.1.0.0.UPF"
    if sha256(EXECUTABLE) != EXPECTED_EXECUTABLE:
        raise RuntimeError("pw.x identity mismatch")
    if sha256(INPUT) != EXPECTED_INPUT:
        raise RuntimeError("input identity mismatch")
    if sha256(pseudo) != EXPECTED_PSEUDO:
        raise RuntimeError("pseudopotential identity mismatch")
    source_save = SOURCE_RUN / "tmp" / "system.save"
    if not source_save.is_dir() or source_save.is_symlink():
        raise RuntimeError("accepted SCF saved state is unavailable")

    run = EXTERNAL_ROOT / "run"
    run.mkdir(parents=True)
    shutil.copy2(INPUT, run / "pw.in")
    shutil.copy2(pseudo, run / pseudo.name)
    shutil.copytree(SOURCE_RUN / "tmp", run / "tmp", symlinks=False)

    environment = os.environ.copy()
    environment["OMP_NUM_THREADS"] = "1"
    started = time.time()
    with (run / "pw.out").open("wb") as stdout, (run / "pw.err").open("wb") as stderr:
        completed = subprocess.run(
            [str(EXECUTABLE), "-in", "pw.in"],
            cwd=run,
            env=environment,
            stdout=stdout,
            stderr=stderr,
            check=False,
        )
    finished = time.time()
    execution: dict[str, object] = {
        "schema_version": 1,
        "status": "succeeded" if completed.returncode == 0 else "failed",
        "returncode": completed.returncode,
        "invocation_count": 1,
        "retry_count": 0,
        "command": [str(EXECUTABLE), "-in", "pw.in"],
        "working_directory": str(run),
        "started_unix_seconds": started,
        "finished_unix_seconds": finished,
        "wall_seconds": finished - started,
        "openmp_threads": 1,
        "input": identity(run / "pw.in"),
        "pseudopotential": identity(run / pseudo.name),
        "stdout": identity(run / "pw.out"),
        "stderr": identity(run / "pw.err"),
    }
    OCCURRENCE.mkdir(parents=True, exist_ok=True)
    execution_path.write_text(json.dumps(execution, indent=2) + "\n", encoding="utf-8")
    shutil.copy2(run / "pw.in", OCCURRENCE / "pw.in")
    shutil.copy2(run / "pw.out", OCCURRENCE / "pw.out")
    shutil.copy2(run / "pw.err", OCCURRENCE / "pw.err")
    qexsd = run / "tmp" / "system.save" / "data-file-schema.xml"
    if qexsd.is_file():
        shutil.copy2(qexsd, OCCURRENCE / "data-file-schema.xml")
    RESULT.mkdir(parents=True, exist_ok=True)
    (RESULT / "external-root.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "external_root": str(EXTERNAL_ROOT),
                "source_scf_run": str(SOURCE_RUN),
                "qexsd": identity(qexsd) if qexsd.is_file() else None,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    if completed.returncode != 0:
        raise RuntimeError(f"authorized pw.x invocation failed with {completed.returncode}")
    if not qexsd.is_file():
        raise RuntimeError("successful invocation did not produce QEXSD")


if __name__ == "__main__":
    main()
