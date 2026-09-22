"""Completion command for the Python architecture inventory-and-policy phase.

The command checks only bounded maintained planning artifacts and deterministic
Harness agreement. It does not inspect manuscript calculations, refactor production
source, establish scientific validity, or provide human acceptance.
"""

from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class PythonArchitectureInventoryCompletionValidator:
    """Validate the phase artifacts and generated Harness agreement."""

    repository_root: Path

    def execute(self) -> int:
        """Return the first failing deterministic check status, otherwise zero."""
        required_artifacts = (
            self.repository_root / "harness/reports/python-architecture-inventory.json",
            self.repository_root / "harness/reports/python-architecture-review.md",
        )
        for artifact in required_artifacts:
            if not artifact.is_file() or not artifact.read_bytes().strip():
                print(f"missing or empty required artifact: {artifact}")
                return 1

        interpreter = self.repository_root / "python/.venv/bin/python"
        generator = (
            self.repository_root
            / ".pi/task-ownership/generate_python_architecture_inventory.py"
        )
        if not generator.is_file():
            print(f"missing inventory generator: {generator}")
            return 1
        with tempfile.TemporaryDirectory(
            prefix="python-architecture-inventory-"
        ) as temporary_directory:
            regenerated = Path(temporary_directory) / "inventory.json"
            generation_command = (
                interpreter,
                generator,
                "--repository-root",
                self.repository_root,
                "--source-root",
                self.repository_root / "python/src/ksdft2effmass",
                "--test-root",
                self.repository_root / "python/tests",
                "--documentation-root",
                self.repository_root / "docs",
                "--task-root",
                self.repository_root / "tasks/software",
                "--output",
                regenerated,
            )
            generated = subprocess.run(
                generation_command,
                cwd=self.repository_root,
                check=False,
            )
            if generated.returncode != 0:
                return generated.returncode
            expected = required_artifacts[0].read_bytes()
            actual = regenerated.read_bytes()
            if actual != expected:
                print(
                    "architecture inventory is stale: "
                    f"expected sha256={hashlib.sha256(expected).hexdigest()} "
                    f"regenerated sha256={hashlib.sha256(actual).hexdigest()}"
                )
                return 1

        commands = (
            (
                interpreter,
                "-m",
                "ksdft2effmass.harness.cli",
                "harness-projection",
                "check",
                "--repository-root",
                str(self.repository_root),
            ),
            (
                interpreter,
                "-m",
                "ksdft2effmass.harness.cli",
                "validate-harness",
                "--repository-root",
                str(self.repository_root),
            ),
            ("git", "diff", "--check"),
        )
        for command in commands:
            completed = subprocess.run(command, cwd=self.repository_root, check=False)
            if completed.returncode != 0:
                return completed.returncode
        return 0


def main() -> int:
    """Adapt the command entry point to its explicit validator owner."""
    repository_root = Path(__file__).resolve().parents[2]
    return PythonArchitectureInventoryCompletionValidator(repository_root).execute()


if __name__ == "__main__":
    sys.exit(main())
