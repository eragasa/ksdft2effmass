"""Root-confined selection of explicit project-local repository inputs."""

from __future__ import annotations

from pathlib import Path


class _RepositoryInputSelector:
    """Select explicit root-confined files and directories for local actions."""

    __slots__ = ()

    @staticmethod
    def _resolved(root: Path, relative: Path, message: str) -> Path:
        resolved_root = root.resolve()
        try:
            resolved = (resolved_root / relative).resolve(strict=True)
            resolved.relative_to(resolved_root)
        except (FileNotFoundError, RuntimeError, ValueError) as exc:
            raise ValueError(f"{message}: {relative}") from exc
        return resolved

    def file(self, root: Path, relative: Path, *, subject: str = "input") -> Path:
        """Return one explicit regular file confined beneath ``root``."""
        resolved = self._resolved(
            root,
            relative,
            f"repository-relative {subject} is not root-confined",
        )
        if not resolved.is_file():
            raise ValueError(
                f"repository-relative {subject} is not a regular file: {relative}"
            )
        return resolved

    def directory(self, root: Path, relative: Path) -> Path:
        """Return one explicit resource root confined beneath ``root``."""
        resolved = self._resolved(
            root,
            relative,
            "repository-relative resource root is not confined",
        )
        if not resolved.is_dir():
            raise ValueError(
                f"repository-relative resource root is not a directory: {relative}"
            )
        return resolved
