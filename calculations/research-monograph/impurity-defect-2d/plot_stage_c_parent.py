#!/usr/bin/env python3
"""Render deterministic SVG diagnostics for a retained Stage C parent result."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import cast

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]


class StageCParentResultReader:
    """Decode only the retained scalar diagnostics needed for plotting."""

    __slots__ = ()

    @staticmethod
    def mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be an object")
        return value

    @staticmethod
    def array(value: JsonValue, name: str) -> list[JsonValue]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be an array")
        return value

    @staticmethod
    def text(value: JsonValue, name: str) -> str:
        if not isinstance(value, str):
            raise TypeError(f"{name} must be a string")
        return value

    @staticmethod
    def real(value: JsonValue, name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be real")
        return float(value)


class StageCParentSvgPlotter:
    """Render deterministic criteria and adverse-control bars without matrices."""

    __slots__ = ("_json",)

    def __init__(self) -> None:
        self._json = StageCParentResultReader()

    def execute(self, result_path: Path, output_path: Path) -> None:
        if output_path.exists():
            raise FileExistsError(f"refusing to overwrite {output_path}")
        result = self._json.mapping(
            cast(JsonValue, json.loads(result_path.read_bytes())), "result"
        )
        if result.get("accepted_parent_read") is not False:
            raise ValueError("plotter accepts only the execution-free record")
        criteria = [
            self._json.mapping(value, "criterion")
            for value in self._json.array(result["criteria"], "criteria")
        ]
        schedules = self._json.array(result["schedules"], "schedules")
        first_schedule = self._json.mapping(schedules[0], "schedule")
        adverse = [
            self._json.mapping(value, "adverse")
            for value in self._json.array(
                first_schedule["adverse_controls"], "adverse controls"
            )
        ]
        svg = self._render(criteria, adverse)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(svg)

    def _render(
        self,
        criteria: list[dict[str, JsonValue]],
        adverse: list[dict[str, JsonValue]],
    ) -> str:
        width = 1240
        height = 1080
        parts = [
            '<svg xmlns="http://www.w3.org/2000/svg" width="1240" '
            'height="1080" viewBox="0 0 1240 1080">',
            '<rect width="1240" height="1080" fill="#f8fafc"/>',
            '<text x="60" y="52" font-family="sans-serif" font-size="25" '
            'font-weight="700" fill="#172554">Stage C accepted-parent contract: '
            "authored-fixture behavior</text>",
            '<text x="60" y="78" font-family="sans-serif" font-size="14" '
            'fill="#475569">Synthetic software verification only; no accepted-parent '
            "read or result</text>",
            '<text x="60" y="118" font-family="sans-serif" font-size="18" '
            'font-weight="700" fill="#172554">Adopted criteria</text>',
        ]
        for index, criterion in enumerate(criteria):
            y = 146 + index * 27
            passed = criterion.get("passed") is True
            color = "#15803d" if passed else "#b91c1c"
            identifier = html.escape(
                self._json.text(criterion["criterion"], "criterion")
            )
            value = self._json.real(criterion["value"], "value")
            threshold = self._json.real(criterion["threshold"], "threshold")
            comparison = html.escape(
                self._json.text(criterion["comparison"], "comparison")
            )
            parts.extend(
                [
                    f'<rect x="60" y="{y - 15}" width="14" height="14" '
                    f'rx="2" fill="{color}"/>',
                    f'<text x="84" y="{y - 3}" font-family="monospace" '
                    f'font-size="12" fill="#0f172a">{identifier}</text>',
                    f'<text x="800" y="{y - 3}" font-family="monospace" '
                    f'font-size="12" fill="#334155">{value:.3e} {comparison} '
                    f"{threshold:.3e}</text>",
                ]
            )
        adverse_y = 146 + len(criteria) * 27 + 25
        parts.append(
            f'<text x="60" y="{adverse_y}" font-family="sans-serif" '
            'font-size="18" font-weight="700" fill="#172554">Adverse controls</text>'
        )
        numerical = [record for record in adverse if record["value"] is not None]
        maximum = max(
            self._json.real(record["value"], "adverse value") for record in numerical
        )
        for index, record in enumerate(adverse):
            y = adverse_y + 31 + index * 31
            identifier = html.escape(
                self._json.text(record["control_id"], "control id")
            )
            raw_value = record["value"]
            if raw_value is None:
                width_value = 270.0
                label = html.escape(self._json.text(record["status"], "status"))
                color = "#7c3aed"
            else:
                value = self._json.real(raw_value, "adverse value")
                width_value = max(4.0, 480.0 * value / maximum)
                label = f"{value:.3e}"
                color = "#c2410c"
            parts.extend(
                [
                    f'<text x="60" y="{y}" font-family="monospace" '
                    f'font-size="11" fill="#0f172a">{identifier}</text>',
                    f'<rect x="510" y="{y - 13}" width="{width_value:.3f}" '
                    f'height="16" rx="2" fill="{color}"/>',
                    f'<text x="{520.0 + width_value:.3f}" y="{y}" '
                    f'font-family="monospace" font-size="11" fill="#334155">'
                    f"{label}</text>",
                ]
            )
        parts.extend(
            [
                f'<line x1="60" y1="{height - 55}" x2="{width - 60}" '
                f'y2="{height - 55}" stroke="#cbd5e1"/>',
                f'<text x="60" y="{height - 28}" font-family="sans-serif" '
                'font-size="12" fill="#475569">208 route evaluations · 104 '
                "bridges · 1,040 model fits · 104 schedule comparisons</text>",
                "</svg>",
            ]
        )
        return "\n".join(parts) + "\n"


def main() -> None:
    """Adapt argparse paths into the deterministic SVG plotter."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    StageCParentSvgPlotter().execute(arguments.result, arguments.output)


if __name__ == "__main__":
    main()
