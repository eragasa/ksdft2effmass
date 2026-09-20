"""Command and atomic-output boundaries for foundation generation."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from tempfile import NamedTemporaryFile

from python_public_import_foundation_model import (
    ClosedFoundationSerializer,
    FoundationJsonCodec,
)

from public_import_foundation.foundation_assembly import (
    PublicImportFactFoundationBuilder,
)
from public_import_foundation.input_snapshot import (
    FoundationFormatError,
    FoundationInputManifestPreparer,
    FoundationInputManifestSerializer,
    FoundationInputSelectionParser,
    FoundationPathPolicy,
)


@dataclass(frozen=True, slots=True)
class FoundationCommandArguments:
    """Represent one exact command invocation."""

    operation: str
    repository_root: Path
    selection: Path | None
    manifest: Path | None
    accepted_inventory: Path | None
    output: Path
    python_executable: Path | None

    @classmethod
    def parse(cls, arguments: tuple[str, ...]) -> FoundationCommandArguments:
        """Parse one closed prepare or generate invocation."""
        if not arguments or arguments[0] not in {"prepare", "generate"}:
            raise ValueError("first argument must be prepare or generate")
        operation = arguments[0]
        values: dict[str, Path] = {}
        remaining = arguments[1:]
        if len(remaining) % 2 != 0:
            raise ValueError("every command flag requires one path value")
        for index in range(0, len(remaining), 2):
            flag = remaining[index]
            if flag in values:
                raise ValueError(f"repeated argument: {flag}")
            values[flag] = Path(remaining[index + 1]).resolve()
        expected = (
            {"--repository-root", "--selection", "--output"}
            if operation == "prepare"
            else {
                "--repository-root",
                "--manifest",
                "--accepted-inventory",
                "--output",
                "--python-executable",
            }
        )
        if set(values) != expected:
            raise ValueError(
                f"{operation} requires exactly: " + " ".join(sorted(expected))
            )
        return cls(
            operation=operation,
            repository_root=values["--repository-root"],
            selection=values.get("--selection"),
            manifest=values.get("--manifest"),
            accepted_inventory=values.get("--accepted-inventory"),
            output=values["--output"],
            python_executable=values.get("--python-executable"),
        )


class FoundationAtomicWriter:
    """Own same-directory atomic replacement for one completed artifact."""

    __slots__ = ()

    def execute(self, output: Path, payload: bytes) -> None:
        """Atomically replace output only after complete payload construction."""
        output.parent.mkdir(parents=True, exist_ok=True)
        temporary_path: Path | None = None
        try:
            with NamedTemporaryFile(
                mode="wb", dir=output.parent, prefix=f".{output.name}.", delete=False
            ) as stream:
                stream.write(payload)
                stream.flush()
                os.fsync(stream.fileno())
                temporary_path = Path(stream.name)
            os.replace(temporary_path, output)
        finally:
            if temporary_path is not None and temporary_path.exists():
                temporary_path.unlink()


@dataclass(frozen=True, slots=True)
class PublicImportFoundationCommand:
    """Execute the exact prepare or generate command boundary."""

    def execute(self, arguments: FoundationCommandArguments) -> None:
        """Write the requested canonical artifact."""
        if arguments.operation == "prepare":
            if arguments.selection is None:
                raise AssertionError("prepare requires selection")
            selections = FoundationInputSelectionParser().execute(
                arguments.selection.read_bytes()
            )
            output = arguments.output.resolve()
            collision_paths = {
                FoundationPathPolicy.resolve(arguments.repository_root, selection.path)
                for selection in selections
            } | {arguments.selection.resolve()}
            if output in collision_paths:
                raise FoundationFormatError(
                    "output path aliases a selected prepare input"
                )
            manifest = FoundationInputManifestPreparer(
                arguments.repository_root
            ).execute(selections)
            FoundationAtomicWriter().execute(
                arguments.output,
                FoundationInputManifestSerializer().encode(manifest),
            )
            return
        if (
            arguments.manifest is None
            or arguments.accepted_inventory is None
            or arguments.python_executable is None
        ):
            raise AssertionError(
                "generate requires manifest, inventory, and interpreter"
            )
        manifest = FoundationInputManifestSerializer().decode(
            arguments.manifest.read_bytes()
        )
        output_path = arguments.output.resolve()
        collision_paths = {
            FoundationPathPolicy.resolve(arguments.repository_root, entry.path)
            for entry in manifest.entries
        } | {
            arguments.manifest.resolve(),
            arguments.accepted_inventory.resolve(),
            arguments.python_executable.resolve(),
        }
        if output_path in collision_paths:
            raise FoundationFormatError("output path aliases a generate input")
        inventory_relative = PurePosixPath(
            arguments.accepted_inventory.resolve()
            .relative_to(arguments.repository_root.resolve())
            .as_posix()
        )
        report = PublicImportFactFoundationBuilder(
            repository_root=arguments.repository_root,
            python_executable=arguments.python_executable,
        ).execute(manifest, inventory_relative)
        output_payload = FoundationJsonCodec().encode(
            ClosedFoundationSerializer().execute(report)
        )
        FoundationAtomicWriter().execute(arguments.output, output_payload)
