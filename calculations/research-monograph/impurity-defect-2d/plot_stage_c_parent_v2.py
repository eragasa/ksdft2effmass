#!/usr/bin/env python3
"""Version-two CLI adapter for the encapsulated Stage C SVG plotter.

Historical retained SVG provenance remains bound to ``plot_stage_c_parent.py``. This
adapter is the supported wrapper for new rendering operations.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from ksdft2effmass.campaigns.research_monograph import StageCParentSvgPlotter


def main() -> None:
    """Adapt command-line paths into one ``StageCParentSvgPlotter`` call."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    StageCParentSvgPlotter().execute(arguments.result, arguments.output)


if __name__ == "__main__":
    main()
