from __future__ import annotations

import hashlib
import json
import shlex
import tempfile
import unittest
from pathlib import Path

from projectkoios.integrations.wannier90 import (
    Wannier90LocalizationInputPreparer,
    Wannier90LocalizationOutputError,
    Wannier90LocalizationPreparationResult,
    Wannier90LocalizationRunner,
    Wannier90LocalizationRunRequest,
)


class TestWannier90LocalizationRunner(unittest.TestCase):
    def test_preparation_closes_and_correlates_native_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = _write_input_source(root)

            result = Wannier90LocalizationInputPreparer().prepare(
                source_directory=source,
                output_directory=root / "prepared",
                seedname="silicon",
                kpoint_count=1,
                band_count=2,
                wannier_count=1,
                neighbor_count=1,
                parent_preprocessing_sha256="a" * 64,
                parent_converter_sha256="b" * 64,
            )

            self.assertEqual(
                result.manifest.total_byte_count,
                sum(
                    (result.output_directory / value.identity.name).stat().st_size
                    for value in result.manifest.artifacts
                ),
            )
            self.assertEqual(
                json.loads(result.manifest_path.read_text())["seedname"], "silicon"
            )
            self.assertFalse((result.output_directory / "UNK00001.1").exists())

    def test_authorized_runner_stages_once_and_parses_selected_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepared = _prepare(root)
            executable = _write_fake_executable(root, complete=True)
            payload = executable.read_bytes()
            manifest_payload = prepared.manifest_path.read_bytes()

            result = Wannier90LocalizationRunner().run(
                Wannier90LocalizationRunRequest(
                    manifest=prepared.manifest,
                    prepared_input_directory=prepared.output_directory,
                    manifest_path=prepared.manifest_path,
                    manifest_sha256=hashlib.sha256(manifest_payload).hexdigest(),
                    manifest_byte_count=len(manifest_payload),
                    output_directory=root / "run",
                    executable=executable,
                    executable_sha256=hashlib.sha256(payload).hexdigest(),
                    executable_byte_count=len(payload),
                    executable_version="synthetic-1",
                    timeout_seconds=30.0,
                    maximum_retained_bytes=1024 * 1024,
                    execution_authorized=True,
                )
            )

            provider = json.loads(result.provider_result.read_text())
            self.assertEqual(provider["status"], "succeeded")
            self.assertEqual(provider["observations"]["wannier_count"], 1)
            self.assertEqual(
                provider["observations"]["gauge_unitarity_maximum_residual"], 0.0
            )
            execution = json.loads(
                (result.output_directory / "execution.json").read_text()
            )
            self.assertEqual(execution["status"], "succeeded")
            self.assertEqual(execution["command"], [str(executable), "silicon"])

    def test_changed_input_fails_before_output_creation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepared = _prepare(root)
            executable = _write_fake_executable(root, complete=True)
            eig = prepared.output_directory / "silicon.eig"
            eig.write_bytes(eig.read_bytes() + b"changed\n")
            output = root / "changed-run"

            with self.assertRaisesRegex(ValueError, "silicon.eig size mismatch"):
                Wannier90LocalizationRunner().run(
                    _request(prepared, executable, output, authorized=True)
                )

            self.assertFalse(output.exists())

    def test_missing_selected_output_retains_provider_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepared = _prepare(root)
            executable = _write_fake_executable(root, complete=False)
            output = root / "missing-output-run"

            with self.assertRaises(Wannier90LocalizationOutputError):
                Wannier90LocalizationRunner().run(
                    _request(prepared, executable, output, authorized=True)
                )

            retained = json.loads((output / "provider-result.json").read_text())
            self.assertEqual(retained["status"], "output-ineligible")
            self.assertTrue((output / "execution.json").is_file())
            self.assertTrue((output / "artifact-manifest.json").is_file())

    def test_absent_execution_authorization_fails_without_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepared = _prepare(root)
            executable = _write_fake_executable(root, complete=True)
            output = root / "unauthorized-run"

            with self.assertRaises(PermissionError):
                Wannier90LocalizationRunner().run(
                    _request(prepared, executable, output, authorized=False)
                )

            self.assertFalse(output.exists())


def _prepare(root: Path) -> Wannier90LocalizationPreparationResult:
    return Wannier90LocalizationInputPreparer().prepare(
        source_directory=_write_input_source(root),
        output_directory=root / "prepared",
        seedname="silicon",
        kpoint_count=1,
        band_count=2,
        wannier_count=1,
        neighbor_count=1,
        parent_preprocessing_sha256="a" * 64,
        parent_converter_sha256="b" * 64,
    )


def _request(
    prepared: Wannier90LocalizationPreparationResult,
    executable: Path,
    output: Path,
    *,
    authorized: bool,
) -> Wannier90LocalizationRunRequest:
    manifest_payload = prepared.manifest_path.read_bytes()
    executable_payload = executable.read_bytes()
    return Wannier90LocalizationRunRequest(
        manifest=prepared.manifest,
        prepared_input_directory=prepared.output_directory,
        manifest_path=prepared.manifest_path,
        manifest_sha256=hashlib.sha256(manifest_payload).hexdigest(),
        manifest_byte_count=len(manifest_payload),
        output_directory=output,
        executable=executable,
        executable_sha256=hashlib.sha256(executable_payload).hexdigest(),
        executable_byte_count=len(executable_payload),
        executable_version="synthetic-1",
        timeout_seconds=30.0,
        maximum_retained_bytes=1024 * 1024,
        execution_authorized=authorized,
    )


def _write_input_source(root: Path) -> Path:
    source = root / "source"
    source.mkdir()
    payloads = {
        "silicon.win": b"num_bands = 2\nnum_wann = 1\nwrite_hr = true\n",
        "silicon.eig": b"1 1 0.5\n2 1 1.5\n",
        "silicon.amn": (b"synthetic amn\n2 1 1\n1 1 1 1.0 0.0\n2 1 1 0.0 0.0\n"),
        "silicon.mmn": (
            b"synthetic mmn\n2 1 1\n1 1 0 0 0\n1.0 0.0\n0.0 0.0\n0.0 0.0\n1.0 0.0\n"
        ),
        "silicon.nnkp": b"""synthetic nnkp
calc_only_A : F
begin real_lattice
1.0 0.0 0.0
0.0 1.0 0.0
0.0 0.0 1.0
end real_lattice
begin recip_lattice
6.0 0.0 0.0
0.0 6.0 0.0
0.0 0.0 6.0
end recip_lattice
begin kpoints
1
0.0 0.0 0.0
end kpoints
begin projections
1
0.0 0.0 0.0 0 1 1
0.0 0.0 1.0 1.0 0.0 0.0 1.0
end projections
begin nnkpts
1
1 1 0 0 0
end nnkpts
begin exclude_bands
0
end exclude_bands
""",
    }
    for name, payload in payloads.items():
        (source / name).write_bytes(payload)
    return source


def _write_fake_executable(root: Path, *, complete: bool) -> Path:
    fixtures = root / ("complete-outputs" if complete else "incomplete-outputs")
    fixtures.mkdir()
    outputs = {
        "silicon.wout": b""" |  Length Unit : Ang  |
Cycle: 1
 WF centre and spread    1  ( 0.0, 0.0, 0.0 )  0.20
  1  -1.0  0.0 <-- CONV
 <<< Disentanglement convergence criteria satisfied >>>
 <<< Wannierisation convergence criteria satisfied >>>
Final State
 WF centre and spread    1  ( 0.0, 0.0, 0.0 )  0.20
 Omega I = 0.10
 Omega D = 0.02
 Omega OD = 0.03
 Omega Total = 0.15
 All done: wannier90 exiting
""",
        "silicon_u.mat": b"synthetic u\n1 1 1\n0.0 0.0 0.0\n1.0 0.0\n",
        "silicon_u_dis.mat": (
            b"synthetic udis\n1 1 2\n0.0 0.0 0.0\n1.0 0.0\n0.0 0.0\n"
        ),
        "silicon_hr.dat": b"synthetic hr\n1\n1\n1\n0 0 0 1 1 0.5 0.0\n",
    }
    if not complete:
        del outputs["silicon_hr.dat"]
    for name, payload in outputs.items():
        (fixtures / name).write_bytes(payload)
    executable = root / (
        "wannier90-complete.x" if complete else "wannier90-incomplete.x"
    )
    copy_commands = "".join(
        f"cp {shlex.quote(str(fixtures / name))} {shlex.quote(name)}\n"
        for name in outputs
    )
    executable.write_text("#!/bin/sh\nset -eu\n" + copy_commands, encoding="ascii")
    executable.chmod(0o755)
    return executable


if __name__ == "__main__":
    unittest.main()
