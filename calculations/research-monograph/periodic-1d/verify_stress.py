"""Verify reconstructable channels of the periodic-1D reduction challenge."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import cast

from ksdft2effmass.operators import ScalarQuantity, Unitless
from ksdft2effmass.periodic1d.campaign.reduction_challenge import (
    Periodic1DReductionChallengeCampaign,
    Periodic1DReductionChallengeEncodedDocuments,
)


class CommandAdapter:
    """Adapt one retained result path to the reduction-challenge campaign."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        """Correlate retained bytes and reconstruct challenge diagnostics."""
        parser = argparse.ArgumentParser()
        parser.add_argument("result", type=Path)
        arguments = parser.parse_args(argv)
        result_path = cast(Path, arguments.result).resolve()
        input_path = Path(__file__).resolve().with_name("stress-input.json")
        campaign = Periodic1DReductionChallengeCampaign(
            Periodic1DReductionChallengeEncodedDocuments(
                input_path.read_bytes(),
                result_path.read_bytes(),
            )
        )
        outcome = campaign.verify(
            absolute_tolerance=ScalarQuantity(1.0e-10, Unitless())
        )
        if not outcome.passes:
            raise ValueError(
                "periodic-1d reduction-challenge independent verification failed"
            )
        print("periodic-1d reduction-challenge result: PASS")
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
