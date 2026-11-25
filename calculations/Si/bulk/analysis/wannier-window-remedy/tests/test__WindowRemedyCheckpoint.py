"""Retention integrity and fail-closed replay storage, not scientific validation."""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


class TestWindowRemedyCheckpoint:
    """Keep original observations intact and require fresh replay output."""

    @pytest.fixture
    def repository_root(self) -> Path:
        return Path(__file__).resolve().parents[6]

    @staticmethod
    def _root(repository_root: Path) -> Path:
        return repository_root / "calculations/Si/bulk/analysis/wannier-window-remedy"

    @classmethod
    def _run(
        cls, repository_root: Path, *arguments: str
    ) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["PYTHONPATH"] = os.pathsep.join(
            (
                str(repository_root / "calculations/Si/bulk"),
                str(repository_root / "python/src"),
            )
        )
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [
                sys.executable,
                str(cls._root(repository_root) / "reproduce.py"),
                *arguments,
            ],
            cwd=repository_root,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_check_only__does_not_open_native_inputs(
        self, repository_root: Path, tmp_path: Path
    ) -> None:
        missing = str(tmp_path / "missing-native-file")
        result = self._run(
            repository_root,
            "--check-only",
            "--amn",
            missing,
            "--eig",
            missing,
            "--gauge",
            missing,
            "--disentanglement",
            missing,
        )
        assert result.returncode == 0, result.stderr
        assert "Retained checkpoint identities" in result.stdout
        assert not (tmp_path / "missing-native-file").exists()

    def test_changed_observation__fails_before_output(
        self, repository_root: Path, tmp_path: Path
    ) -> None:
        copied = tmp_path / "checkpoint"
        shutil.copytree(self._root(repository_root), copied)
        result_path = copied / "results/gamma-window.json"
        result_path.write_bytes(result_path.read_bytes() + b"\n")
        output = tmp_path / "replay"
        result = self._run(
            repository_root, "--checkpoint", str(copied), "--output-root", str(output)
        )
        assert result.returncode != 0
        assert (
            "checkpoint identity mismatch: results/gamma-window.json" in result.stderr
        )
        assert not output.exists()

    def test_changed_request__cannot_reuse_old_result_binding(
        self, repository_root: Path, tmp_path: Path
    ) -> None:
        copied = tmp_path / "checkpoint"
        shutil.copytree(self._root(repository_root), copied)
        request = copied / "inputs/request.json"
        original = request.read_bytes()
        changed = original.replace(b"CSD0-CSD1-c6", b"DSD0-CSD1-c6", 1)
        assert changed != original and len(changed) == len(original)
        request.write_bytes(changed)
        manifest = copied / "manifest.json"
        original_sha = hashlib.sha256(original).hexdigest()
        manifest_text = manifest.read_text()
        assert manifest_text.count(original_sha) == 1
        manifest.write_text(
            manifest_text.replace(original_sha, hashlib.sha256(changed).hexdigest())
        )
        result = self._run(repository_root, "--checkpoint", str(copied), "--check-only")
        assert result.returncode != 0
        assert "request identity mismatch" in result.stderr

    def test_existing_output__is_not_overwritten(
        self, repository_root: Path, tmp_path: Path
    ) -> None:
        output = tmp_path / "replay"
        output.mkdir()
        sentinel = output / "sentinel.txt"
        sentinel.write_bytes(b"preserve")
        result = self._run(repository_root, "--output-root", str(output))
        assert result.returncode != 0
        assert "output root must not already exist" in result.stderr
        assert sentinel.read_bytes() == b"preserve"
        assert sorted(p.name for p in output.iterdir()) == ["sentinel.txt"]

    def test_dangling_output_symlink__is_not_followed(
        self, repository_root: Path, tmp_path: Path
    ) -> None:
        output = tmp_path / "replay"
        target = tmp_path / "missing-target"
        output.symlink_to(target, target_is_directory=True)
        result = self._run(repository_root, "--output-root", str(output))
        assert result.returncode != 0
        assert "output root must not already exist" in result.stderr
        assert output.is_symlink()
        assert not target.exists()
