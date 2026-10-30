"""Run the first bounded silicon-inspired mesh-refinement point."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from run_development import DEFINITION, construct_artifacts, write_artifacts

REFINEMENT = replace(DEFINITION, construction_size=16, evaluation_size=33)


def main() -> int:
    """Calculate and verify the selected first development refinement."""
    _, result, verification = construct_artifacts(REFINEMENT)
    if not verification.passes:
        raise RuntimeError("independent refinement verification failed")
    development = Path(__file__).resolve().parent / "simulations" / "development"
    output = development / "results" / "refinement" / "N16"
    write_artifacts(output, result, verification)
    print(
        f"family={REFINEMENT.family.to_wire()} lifecycle=development "
        f"construction_size=16 verification=pass output={output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
