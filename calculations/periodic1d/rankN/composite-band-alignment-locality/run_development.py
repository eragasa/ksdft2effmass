"""Run the complete bounded schema-free higher-rank D1 development calculation."""

from __future__ import annotations

import json
from pathlib import Path

from workflow import (
    FAMILY_ID,
    PRODUCER_METHOD_ID,
    VERSION_ID,
    HigherRankD1Calculator,
    HigherRankD1ChannelMeshDiagnostics,
    HigherRankD1Definition,
)

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


def _summary() -> dict[str, JsonValue]:
    """Calculate all cases and return an explicitly development-only shape summary."""
    definition = HigherRankD1Definition()
    result = HigherRankD1Calculator().execute(definition)
    cases: list[JsonValue] = []
    for case in result.cases:
        final_channels: list[JsonValue] = []
        for channel in case.meshes[-1].channels:
            channel_summary: dict[str, JsonValue] = {
                "channel": channel.channel,
                "alignment_status": channel.alignment_status,
                "downstream_applicability": channel.downstream_applicability,
            }
            if isinstance(channel, HigherRankD1ChannelMeshDiagnostics):
                support_two = channel.supports[2]
                channel_summary["support_count"] = len(channel.supports)
                channel_summary["pareto_nondominated_supports"] = [
                    point.support
                    for point in channel.pareto_points
                    if point.pareto_efficient
                ]
                channel_summary["support_two_normalized_tail_l2"] = (
                    support_two.tail.normalized_l2_norm
                )
                channel_summary["support_two_normalized_total_operator_error"] = (
                    support_two.total.errors.normalized_matrix_frobenius_maximum
                )
                channel_summary["support_two_normalized_total_spectrum_error"] = (
                    support_two.total.errors.normalized_ordered_spectrum_maximum
                )
            final_channels.append(channel_summary)
        cases.append(
            {
                "case_id": case.case_id,
                "rank": case.rank,
                "depth": case.depth,
                "qualification": case.qualification,
                "failed_gate_paths": list(case.failed_gate_paths),
                "construction_mesh_count": len(case.meshes),
                "refinement_record_count": len(case.refinement),
                "final_mesh_channels": final_channels,
            }
        )
    return {
        "artifact_role": "replaceable-schema-free-development-summary",
        "scientific_evidence": False,
        "family_id": FAMILY_ID,
        "version_id": VERSION_ID,
        "producer_method_id": PRODUCER_METHOD_ID,
        "overall_qualification": result.overall_qualification,
        "case_count": len(result.cases),
        "cases": cases,
    }


def main() -> int:
    """Write one replaceable local summary outside the retained runs tree."""
    output = Path(__file__).resolve().parent / "results"
    output.mkdir(parents=True, exist_ok=True)
    destination = output / "schema-free-development-summary.json"
    payload = _summary()
    destination.write_text(
        json.dumps(payload, allow_nan=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        f"lifecycle=replaceable-schema-free-development "
        f"qualification={payload['overall_qualification']} output={destination}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
