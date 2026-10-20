"""Independently verify the replaceable QHO1D development result."""

from __future__ import annotations

from pathlib import Path

from ksdft2effmass.model_systems.qho1d import QHO1DResultVerifier

EXPERIMENT_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = EXPERIMENT_ROOT.parents[1]
OUTPUT_PATH = EXPERIMENT_ROOT / "analysis" / "development" / "qho1d-result.json"


def main() -> int:
    """Verify the fixed development output path and report its disposition."""
    QHO1DResultVerifier().execute(OUTPUT_PATH, REPOSITORY_ROOT)
    print(
        f"experiment=qho1d lifecycle=development verification=pass output={OUTPUT_PATH}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
