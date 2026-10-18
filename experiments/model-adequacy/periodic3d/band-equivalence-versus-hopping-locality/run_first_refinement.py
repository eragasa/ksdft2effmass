"""Run the first bounded simple-cubic mesh-refinement point."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from run_development import DEFINITION, construct_artifacts, write_artifacts

REFINEMENT = replace(DEFINITION, construction_size=16, evaluation_size=33)


def main() -> int:
    """Calculate and verify the selected first development refinement."""
    result, verification = construct_artifacts(REFINEMENT)
    if not verification.diagnostics.passes:
        raise RuntimeError("independent refinement verification failed")
    experiment = Path(__file__).resolve().parent
    output = experiment / "analysis" / "development-refinement" / "N16"
    write_artifacts(output, result, verification)
    print(
        f"family={REFINEMENT.family.value} lifecycle=development "
        f"construction_size=16 verification=pass output={output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
