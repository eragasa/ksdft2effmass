#!/usr/bin/env python3
"""CLI adapter for the Appendix E finite harmonic-oscillator comparison."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import cast

from ksdft2effmass.campaigns.research_monograph import (
    HarmonicOscillatorStudyEvaluator,
    HarmonicOscillatorStudyInputDeserializer,
    HarmonicOscillatorStudyResultSerializer,
)


def main() -> None:
    """Adapt command-line paths to the owned experiment Workflow."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    input_path = cast(Path, args.input).resolve()
    output_path = cast(Path, args.output).resolve()
    script_path = Path(__file__).resolve()
    repository_root = script_path.parents[3]
    definition = HarmonicOscillatorStudyInputDeserializer().execute(
        input_path.read_bytes()
    )
    result = HarmonicOscillatorStudyEvaluator().execute(definition)
    payload = HarmonicOscillatorStudyResultSerializer().execute(
        result,
        input_path,
        script_path,
        repository_root,
    )
    output_path.write_bytes(payload)


if __name__ == "__main__":
    main()
