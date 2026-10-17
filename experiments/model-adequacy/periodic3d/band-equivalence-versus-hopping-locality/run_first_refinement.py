"""Run the first bounded simple-cubic mesh-refinement point."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from run_development import DEFINITION, construct_artifacts, write_artifacts

REFINEMENT = replace(DEFINITION, construction_size=16, evaluation_size=33)


def main() -> None:
    """Calculate and verify the prospectively selected first refinement point."""
    result, verification = construct_artifacts(REFINEMENT)
    experiment = Path(__file__).resolve().parent
    output = experiment / "analysis" / "development-refinement" / "N16"
    write_artifacts(output, result, verification)
    print(f"{REFINEMENT.family.value}: N=16 passes={verification.diagnostics.passes}")


if __name__ == "__main__":
    main()
