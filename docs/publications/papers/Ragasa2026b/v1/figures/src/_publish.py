"""Regenerate and stage one Paper 2 figure from its owning experiment."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

SOURCE_DIRECTORY = Path(__file__).resolve().parent
FIGURE_DIRECTORY = SOURCE_DIRECTORY.parent
REPOSITORY = SOURCE_DIRECTORY.parents[6]


def publish(*, generator: str, generated_figure: str) -> None:
    """Run the owning generator and copy its PDF under the caller's mirrored name."""
    arguments = sys.argv[1:]
    if arguments not in ([], ["--reuse-existing"]):
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} [--reuse-existing]")

    generator_path = REPOSITORY / generator
    source_path = REPOSITORY / generated_figure
    if not generator_path.is_file():
        raise FileNotFoundError(f"figure generator does not exist: {generator_path}")

    if not arguments:
        virtual_environment_python = REPOSITORY / "python" / ".venv" / "bin" / "python"
        python = (
            virtual_environment_python
            if virtual_environment_python.is_file()
            else Path(sys.executable)
        )
        environment = os.environ.copy()
        source_root = str(REPOSITORY / "python" / "src")
        previous_python_path = environment.get("PYTHONPATH")
        environment["PYTHONPATH"] = (
            source_root
            if previous_python_path is None
            else f"{source_root}{os.pathsep}{previous_python_path}"
        )
        subprocess.run(
            [str(python), str(generator_path)],
            cwd=generator_path.parent,
            env=environment,
            check=True,
        )

    caller = Path(sys.argv[0]).resolve()
    for suffix in (".pdf", ".png"):
        rendered_source = source_path.with_suffix(suffix)
        if not rendered_source.is_file():
            raise FileNotFoundError(
                f"generated figure does not exist: {rendered_source}"
            )
        target = FIGURE_DIRECTORY / f"{caller.stem}{suffix}"
        temporary_target = target.with_suffix(f"{suffix}.tmp")
        shutil.copyfile(rendered_source, temporary_target)
        temporary_target.replace(target)
        print(target)
