#!/usr/bin/env python3
"""CLI adapter for independent continuum-refinement verification."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import cast

from continuum_refinement_calculation.verify_result import (
    ContinuumRefinementVerificationWorkflow,
)


def main() -> None:
    """Adapt one result path to the independent verification Workflow."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--result", type=Path, required=True)
    arguments = parser.parse_args()
    ContinuumRefinementVerificationWorkflow().execute(
        cast(Path, arguments.result).resolve()
    )


if __name__ == "__main__":
    main()
