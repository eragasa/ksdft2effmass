"""Independently verify the replaceable QHO1D development result."""

from __future__ import annotations

from pathlib import Path

from ksdft2effmass.model_systems.qho1d import Qho1dResultVerifier

CALCULATION_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = CALCULATION_ROOT.parents[1]
OUTPUT_PATH = CALCULATION_ROOT / "analysis" / "development" / "qho1d-result.json"


def main() -> int:
    """Verify the fixed development output path and report its disposition."""
    Qho1dResultVerifier().execute(OUTPUT_PATH, REPOSITORY_ROOT)
    print(
        "calculation=qho1d lifecycle=development verification=pass "
        f"output={OUTPUT_PATH}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
