"""Thin repository CLI adapter over one internal reusable command owner."""

from __future__ import annotations

from collections.abc import Sequence

from ksdft2effmass.harness.pi.local._commands import (
    validate_python_conformance as _owner,
)


def cli_main(argv: Sequence[str] | None = None) -> int:
    """Delegate explicit arguments to the internal reusable owner."""
    return _owner.run(argv)


main = cli_main


if __name__ == "__main__":
    raise SystemExit(cli_main())
