#!/usr/bin/env python3
"""Verify the prepared local non-DFT native-evidence archive."""

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
    """Verify archive identity, size, format, and declared member roots."""

    __slots__ = ()

    def execute(self, manifest_path: Path) -> None:
        manifest = self._mapping(
            cast(JsonValue, json.loads(manifest_path.read_text(encoding="utf-8")))
        )
        if self._integer(manifest["schema_version"]) != 1:
            raise ValueError("unsupported archive manifest schema")
        archive_path = Path(self._string(manifest["archive_path"]))
        if not archive_path.is_file():
            raise FileNotFoundError(f"local archive is absent: {archive_path}")
        if archive_path.stat().st_size != self._integer(manifest["archive_bytes"]):
            raise AssertionError("archive size mismatch")
        digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
        if digest != self._string(manifest["archive_sha256"]):
            raise AssertionError("archive content identity mismatch")
        with tarfile.open(archive_path, mode="r:gz") as archive:
            roots = {Path(name).parts[0] for name in archive.getnames() if name}
        expected = {
            self._string(value) for value in self._array(manifest["member_roots"])
        }
        if roots != expected:
            raise AssertionError(
                f"archive member roots mismatch: actual={roots}, expected={expected}"
            )

    def _mapping(self, value: JsonValue) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError("expected a mapping")
        return value

    def _array(self, value: JsonValue) -> list[JsonValue]:
        if not isinstance(value, list):
            raise TypeError("expected an array")
        return value

    def _string(self, value: JsonValue) -> str:
        if not isinstance(value, str):
            raise TypeError("expected a string")
        return value

    def _integer(self, value: JsonValue) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("expected an integer")
        return value


def main() -> None:
    """CLI entry point required by the verification-script boundary."""
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    arguments = parser.parse_args()
    NativeEvidenceArchiveVerifier().execute(cast(Path, arguments.manifest).resolve())
    print("periodic_2d_native_evidence_archive_verification=PASS")


if __name__ == "__main__":
    main()
