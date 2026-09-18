#!/usr/bin/env python3
"""Verify the local optimizer-basin native-evidence archive."""

from __future__ import annotations

import argparse
import hashlib
import json
import tarfile
from pathlib import Path
from typing import cast

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


class NativeEvidenceArchiveVerifier:
    """Verify archive identity and required retained native members."""

    __slots__ = ()

    def execute(self, manifest_path: Path) -> None:
        manifest = self._mapping(
            cast(JsonValue, json.loads(manifest_path.read_text(encoding="utf-8")))
        )
        if self._integer(manifest["schema_version"]) != 1:
            raise ValueError("unsupported archive manifest schema")
        archive = Path(self._string(manifest["archive_path"]))
        if archive.stat().st_size != self._integer(manifest["archive_bytes"]):
            raise AssertionError("archive byte count mismatch")
        self._identity(archive, manifest["archive_sha256"], "archive")
        execution_name = self._string(manifest["execution_result_relative_path"])
        with tarfile.open(archive, mode="r:gz") as retained:
            files = [member for member in retained.getmembers() if member.isfile()]
            if len(files) != self._integer(manifest["uncompressed_file_count"]):
                raise AssertionError("archive file count mismatch")
            if sum(member.size for member in files) != self._integer(
                manifest["uncompressed_file_bytes"]
            ):
                raise AssertionError("archive uncompressed byte count mismatch")
            member = retained.getmember(execution_name)
            stream = retained.extractfile(member)
            if stream is None:
                raise AssertionError("execution result is absent from archive")
            execution_bytes = stream.read()
            expected_execution = self._string(manifest["execution_result_sha256"])
            if hashlib.sha256(execution_bytes).hexdigest() != expected_execution:
                raise AssertionError("archived execution-result identity mismatch")
            names = {value.name for value in files}
        root = self._string(manifest["contained_root"])
        required = {
            f"{root}/execution-result.json",
            f"{root}/mesh_n23_p4_c23/rough_smooth/low_triple/low_triple.wout",
            f"{root}/mesh_n23_p4_c23/rough_smooth/analysis-result.json",
            f"{root}/cutoff_p5_n19_c19/rough_smooth/low_triple/low_triple_hr.dat",
            f"{root}/embedding_c15_p4_n19/y02_soft/low_triple/low_triple_u.mat",
        }
        missing = required - names
        if missing:
            raise AssertionError(f"archive lacks required members: {sorted(missing)}")

    @staticmethod
    def _identity(path: Path, expected: JsonValue, label: str) -> None:
        if not isinstance(expected, str):
            raise TypeError("expected digest must be a string")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise AssertionError(
                f"{label} identity mismatch: actual={actual}, expected={expected}"
            )

    @staticmethod
    def _mapping(value: JsonValue) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError("expected an object")
        return value

    @staticmethod
    def _string(value: JsonValue) -> str:
        if not isinstance(value, str):
            raise TypeError("expected a string")
        return value

    @staticmethod
    def _integer(value: JsonValue) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("expected an integer")
        return value


class CommandAdapter:
    """Adapt the CLI manifest path to the archive verifier."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("manifest", type=Path)
        arguments = parser.parse_args(argv)
        NativeEvidenceArchiveVerifier().execute(
            cast(Path, arguments.manifest).resolve()
        )
        print("periodic_2d_optimizer_basin_archive_verification=PASS")
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
