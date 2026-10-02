#!/usr/bin/env python3
"""Verify reconstructable channels of the retained periodic-1D composite result."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import cast

from ksdft2effmass.campaigns.research_monograph import (
    Periodic1DCompositeCampaign,
    Periodic1DCompositeEncodedDocuments,
)
from ksdft2effmass.operators import ScalarQuantity, Unitless


class CommandAdapter:
    """Adapt one retained result path to the supported verified Workflow."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        """Correlate retained bytes and run independent numerical reconstruction."""
        parser = argparse.ArgumentParser()
        parser.add_argument("result", type=Path)
        arguments = parser.parse_args(argv)
        result_path = cast(Path, arguments.result).resolve()
        input_path = Path(__file__).resolve().with_name("composite-input.json")
        campaign = Periodic1DCompositeCampaign(
            Periodic1DCompositeEncodedDocuments(
                input_path.read_bytes(),
                result_path.read_bytes(),
            )
        )
        outcome = campaign.verify(
            absolute_tolerance=ScalarQuantity(1.0e-11, Unitless())
        )
        if not outcome.passes:
            raise ValueError("periodic-1d composite independent verification failed")
        print("periodic-1d direct composite-band result: PASS")
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
