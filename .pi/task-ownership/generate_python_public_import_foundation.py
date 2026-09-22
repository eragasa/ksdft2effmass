#!/usr/bin/env python3
"""Generate the explicit-input public-import fact foundation."""

from __future__ import annotations

import subprocess
import sys

from public_import_foundation.command import (
    FoundationCommandArguments,
    PublicImportFoundationCommand,
)


def main() -> int:
    """Adapt the process entry point to the command ActionObject."""
    try:
        arguments = FoundationCommandArguments.parse(tuple(sys.argv[1:]))
        PublicImportFoundationCommand().execute(arguments)
    except (OSError, ValueError, TypeError, subprocess.SubprocessError) as exc:
        print(f"public-import foundation generation failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
