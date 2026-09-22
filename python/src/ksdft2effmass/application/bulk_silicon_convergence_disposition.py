"""Explicit file adapter for the bulk-silicon convergence disposition compiler."""

from __future__ import annotations

import sys
from pathlib import Path

from ksdft2effmass.campaigns._bulk_silicon_convergence_disposition import (
    BULK_SILICON_SEQUENTIAL_SCAN_CONFIGURATION,
    BulkSiliconConvergenceDispositionJsonSerializer,
    BulkSiliconConvergenceDispositionPlanner,
    BulkSiliconFiniteSettingAnalysisJsonDecoder,
)


class BulkSiliconConvergenceDispositionApplication:
    """Read one exact retained analysis and write one generated decision packet."""

    __slots__ = ()

    def execute(self, source: Path, destination: Path, source_reference: str) -> None:
        """Compile ``source`` to ``destination`` without running scientific software."""
        if not isinstance(source, Path) or not isinstance(destination, Path):
            raise TypeError("source and destination must be pathlib.Path values")
        if type(source_reference) is not str or not source_reference:
            raise ValueError("source_reference must be a nonempty built-in str")
        evidence = BulkSiliconFiniteSettingAnalysisJsonDecoder().execute(
            source_reference, source.read_bytes()
        )
        packet = BulkSiliconConvergenceDispositionPlanner(
            BULK_SILICON_SEQUENTIAL_SCAN_CONFIGURATION
        ).execute(evidence)
        destination.write_bytes(
            BulkSiliconConvergenceDispositionJsonSerializer().execute(packet)
        )


class BulkSiliconConvergenceDispositionCli:
    """Own the command-line adaptation for the explicit file application."""

    __slots__ = ()

    def execute(self, arguments: tuple[str, ...]) -> None:
        """Validate explicit path arguments and invoke the application once."""
        if type(arguments) is not tuple or any(
            type(value) is not str for value in arguments
        ):
            raise TypeError("arguments must be a tuple of built-in str values")
        if len(arguments) != 4 or arguments[2] != "--source-reference":
            raise ValueError(
                "usage: SOURCE DESTINATION --source-reference REPOSITORY_PATH"
            )
        BulkSiliconConvergenceDispositionApplication().execute(
            Path(arguments[0]), Path(arguments[1]), arguments[3]
        )


if __name__ == "__main__":
    BulkSiliconConvergenceDispositionCli().execute(tuple(sys.argv[1:]))
