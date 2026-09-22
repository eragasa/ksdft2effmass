#!/usr/bin/env python3
"""Verify the local standalone-study native-evidence archive."""

from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import tarfile
from pathlib import Path
from typing import BinaryIO, cast

from execute_study import JsonValue


class StandaloneArchiveVerifier:
    """Verify archive identity, inventory, links, and control-record members."""

    __slots__ = ()

    def execute(self, manifest_path: Path) -> None:
        manifest = self._load(manifest_path)
        archive = Path(self._string(manifest["archive_path"]))
        self._equal(
            archive.stat().st_size,
            self._integer(manifest["archive_bytes"]),
            "archive bytes",
        )
        self._identity(archive, self._string(manifest["archive_sha256"]), "archive")
        root = self._string(manifest["contained_root"])
        with tarfile.open(archive, "r:gz") as handle:
            members = handle.getmembers()
            files = [member for member in members if member.isfile()]
            links = [member for member in members if member.issym()]
            directories = [member for member in members if member.isdir()]
            self._equal(
                len(members),
                self._integer(manifest["archive_member_count"]),
                "member count",
            )
            self._equal(
                len(files), self._integer(manifest["regular_file_count"]), "file count"
            )
            self._equal(
                sum(member.size for member in files),
                self._integer(manifest["regular_file_bytes"]),
                "file bytes",
            )
            self._equal(
                len(links), self._integer(manifest["symbolic_link_count"]), "link count"
            )
            self._equal(
                len(directories),
                self._integer(manifest["directory_count"]),
                "directory count",
            )
            for member in members:
                if member.name.startswith("/") or ".." in Path(member.name).parts:
                    raise AssertionError(f"unsafe archive member {member.name}")
                if member.name != root and not member.name.startswith(f"{root}/"):
                    raise AssertionError(f"member outside contained root {member.name}")
            for member in links:
                normalized = posixpath.normpath(
                    posixpath.join(posixpath.dirname(member.name), member.linkname)
                )
                if normalized != root and not normalized.startswith(f"{root}/"):
                    raise AssertionError(f"symlink escapes archive root: {member.name}")
            self._member_identity(
                handle,
                self._string(manifest["execution_result_relative_path"]),
                self._string(manifest["execution_result_sha256"]),
            )
            self._member_identity(
                handle,
                self._string(manifest["pre_resume_snapshot_relative_path"]),
                self._string(manifest["pre_resume_snapshot_sha256"]),
            )
            required = (
                f"{root}/fixed_c31_p4_n31/baseline_preconditioned/halton_15/low_triple/low_triple.wout",
                f"{root}/fixed_c31_p4_n31/baseline_preconditioned/halton_02/continuation/low_triple/low_triple.wout",
                f"{root}/balanced_p4_n23_c23/control_preconditioner_off/halton_13/continuation/low_triple/low_triple.chk",
                f"{root}/fixed_c31_p6_n23/interface/low_triple/low_triple.mmn",
            )
            names = {member.name for member in members}
            for name in required:
                if name not in names:
                    raise AssertionError(f"required archive member missing: {name}")

    def _member_identity(
        self, archive: tarfile.TarFile, name: str, expected: str
    ) -> None:
        stream = archive.extractfile(name)
        if stream is None:
            raise AssertionError(f"archive member is not a file: {name}")
        actual = self._stream_sha256(stream)
        if actual != expected:
            raise AssertionError(
                f"archive member identity mismatch: {name}: "
                f"actual={actual}, expected={expected}"
            )

    @staticmethod
    def _stream_sha256(stream: BinaryIO) -> str:
        digest = hashlib.sha256()
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
        return digest.hexdigest()

    @staticmethod
    def _identity(path: Path, expected: str, label: str) -> None:
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            while chunk := stream.read(1024 * 1024):
                digest.update(chunk)
        actual = digest.hexdigest()
        if actual != expected:
            raise AssertionError(
                f"{label} identity mismatch: actual={actual}, expected={expected}"
            )

    @staticmethod
    def _equal(actual: int, expected: int, label: str) -> None:
        if actual != expected:
            raise AssertionError(f"{label}: actual={actual}, expected={expected}")

    def _load(self, path: Path) -> dict[str, JsonValue]:
        return self._mapping(
            cast(JsonValue, json.loads(path.read_text(encoding="utf-8")))
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
    """Adapt the archive-manifest path to archive verification."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("manifest", type=Path)
        arguments = parser.parse_args(argv)
        StandaloneArchiveVerifier().execute(cast(Path, arguments.manifest).resolve())
        print("periodic_2d_standalone_archive_verification=PASS")
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
