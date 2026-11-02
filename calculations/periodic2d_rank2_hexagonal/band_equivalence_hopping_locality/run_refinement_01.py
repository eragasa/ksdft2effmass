"""Run the first bounded graphene-inspired mesh-refinement point."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from run_nominal_calculation import DEFINITION, construct_artifacts, write_artifacts

REFINEMENT = replace(DEFINITION, construction_size=32, evaluation_size=65)


def main() -> int:
    """Calculate and verify the selected first development refinement."""
    _, result, verification = construct_artifacts(REFINEMENT)
    if not verification.passes:
        raise RuntimeError("independent refinement verification failed")
    replaceable = Path(__file__).resolve().parent / "simulations" / "replaceable"
    output = replaceable / "results" / "refinement" / "N32"
    write_artifacts(output, result, verification)
    print(
        f"family={REFINEMENT.family.to_wire()} lifecycle=development "
        f"construction_size=32 verification=pass output={output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
