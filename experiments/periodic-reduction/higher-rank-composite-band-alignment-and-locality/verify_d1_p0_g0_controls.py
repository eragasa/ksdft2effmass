#!/usr/bin/env python3
"""Sample the selected D1 P0/G0 control formulas.

This development utility checks the analytic formulas on a finite grid. Its output is a
sanity check, not a proof of the exterior-isolation energy, a convergence result, or
retained scientific evidence. The mesh-independent certificate is derived in the
protocol.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

RANKS: tuple[int, ...] = (3, 4, 8, 16)
DEPTHS: tuple[int, ...] = (1, 2, 4, 8)
DEFAULT_SAMPLE_INTERVALS = 20_000


@dataclass(frozen=True, slots=True)
class SampledControlSummary:
    """Finite-grid summary for one retained rank."""

    rank: int
    sampled_isolation_energy: float
    sampled_max_angle: float


def _rank_coordinate(rank: int, index: int) -> float:
    return (2.0 * index - rank - 1.0) / (rank - 1.0)


def _pair_coordinate(rank: int, pair_index: int) -> float:
    return (2.0 * pair_index - rank) / (rank - 1.0)


def _even_harmonic(momentum: float) -> float:
    return 0.75 * math.cos(momentum) + 0.25 * math.cos(2.0 * momentum)


def _layer_harmonic(momentum: float, layer: int) -> float:
    return 0.75 * math.sin(momentum) + 0.25 * (-1.0) ** layer * math.sin(2.0 * momentum)


def _retained_energy(rank: int, index: int, harmonic: float) -> float:
    coordinate = _rank_coordinate(rank, index)
    return 0.40 * coordinate + 0.25 * (1.0 + 0.20 * coordinate) * harmonic


def _exterior_energy(rank: int, index: int, harmonic: float) -> float:
    coordinate = _rank_coordinate(rank, index)
    return 3.00 + 0.30 * coordinate + 0.10 * harmonic


def _givens_angle(
    rank: int,
    layer: int,
    pair_index: int,
    layer_harmonic: float,
) -> float:
    coordinate = _pair_coordinate(rank, pair_index)
    return (
        0.35
        * (-1.0) ** (layer + pair_index)
        * (1.0 + 0.15 * coordinate)
        * layer_harmonic
    )


def sample_control(rank: int, sample_intervals: int) -> SampledControlSummary:
    """Sample the isolation energy and attack-angle magnitude for one declared rank.

    Energies are returned in units of ``E_ref`` and angles in radians. The grid contains
    ``sample_intervals + 1`` points including both endpoints of ``[-pi, pi]``.
    """

    if isinstance(rank, bool) or not isinstance(rank, int) or rank < 2:
        raise ValueError("rank must be an integer greater than or equal to two")
    if (
        isinstance(sample_intervals, bool)
        or not isinstance(sample_intervals, int)
        or sample_intervals <= 0
        or sample_intervals % 2 != 0
    ):
        raise ValueError("sample_intervals must be a positive even integer")

    minimum_isolation_energy = math.inf
    maximum_angle = 0.0
    maximum_layer = max(DEPTHS)

    for sample_index in range(sample_intervals + 1):
        momentum = -math.pi + 2.0 * math.pi * sample_index / sample_intervals
        harmonic = _even_harmonic(momentum)
        retained = tuple(
            _retained_energy(rank, index, harmonic) for index in range(1, rank + 1)
        )
        exterior = tuple(
            _exterior_energy(rank, index, harmonic) for index in range(1, rank + 1)
        )
        minimum_isolation_energy = min(
            minimum_isolation_energy,
            min(exterior) - max(retained),
        )

        for layer in range(1, maximum_layer + 1):
            layer_harmonic = _layer_harmonic(momentum, layer)
            for pair_index in range(1, rank):
                angle = _givens_angle(
                    rank,
                    layer,
                    pair_index,
                    layer_harmonic,
                )
                maximum_angle = max(maximum_angle, abs(angle))

    return SampledControlSummary(
        rank=rank,
        sampled_isolation_energy=minimum_isolation_energy,
        sampled_max_angle=maximum_angle,
    )


def main() -> int:
    """Run the finite-grid development sanity check and return success."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sample-intervals",
        type=int,
        default=DEFAULT_SAMPLE_INTERVALS,
        help="positive even number of intervals on [-pi, pi] (default: 20000)",
    )
    arguments = parser.parse_args()

    for rank in RANKS:
        summary = sample_control(rank, arguments.sample_intervals)
        print(
            f"rank={summary.rank} "
            f"sampled_isolation_energy_E_ref={summary.sampled_isolation_energy:.12f} "
            f"sampled_maximum_angle_rad={summary.sampled_max_angle:.12f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
