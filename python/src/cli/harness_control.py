"""Temporary compatibility entry point for :mod:`harness_projection`.

New callers must use ``python/src/cli/harness_projection.py``. This wrapper exists
only during the Architecture v1-to-v2 projection migration and will be removed at
cutover together with the ``HarnessControl*`` compatibility API.
"""

from __future__ import annotations

from collections.abc import Sequence

from harness_projection import cli_main as _projection_main


def cli_main(argv: Sequence[str] | None = None) -> int:
    """Delegate explicit arguments to the maintained projection command."""
    return _projection_main(argv)


main = cli_main


if __name__ == "__main__":
    raise SystemExit(cli_main())
