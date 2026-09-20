#!/usr/bin/env python3
"""CLI adapter for the public particle-in-a-box residual-study campaign."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import cast

from ksdft2effmass.campaigns.research_monograph import (
    ParticleInBoxResidualStudyEvaluator,
    ParticleInBoxStudyInputDeserializer,
    ParticleInBoxStudyResultSerializer,
)


def main() -> None:
    """Decode, evaluate, and serialize one explicit residual-study request."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    input_path = cast(Path, args.input).resolve()
    output_path = cast(Path, args.output).resolve()
    script_path = Path(__file__).resolve()
    repository_root = script_path.parents[3]
    definition = ParticleInBoxStudyInputDeserializer().execute(input_path.read_bytes())
    result = ParticleInBoxResidualStudyEvaluator().execute(definition)
    output_path.write_bytes(
        ParticleInBoxStudyResultSerializer().execute(
            result, input_path, script_path, repository_root
        )
    )


if __name__ == "__main__":
    main()
