#!/usr/bin/env python3
"""Acquire or generate the explicit current-fact supplement."""

from __future__ import annotations

import subprocess
import sys

from public_import_current_fact_supplement.command import (
    CurrentFactSupplementCommand,
    SupplementCommandArguments,
)


def main() -> int:
    """Adapt the process entry point to the typed command owner."""
    try:
        CurrentFactSupplementCommand().execute(
            SupplementCommandArguments.parse(tuple(sys.argv[1:]))
        )
    except (OSError, ValueError, TypeError, subprocess.SubprocessError) as exc:
        print(f"current-fact supplement generation failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
