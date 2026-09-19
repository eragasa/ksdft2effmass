#!/usr/bin/env python3
"""Render a deterministic SVG summary from a retained Stage B result."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import cast

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


class StageBPlotter:
    """Render retained route, bridge, order, and blind data without recalculation."""

    __slots__ = ()

    def execute(self, result_path: Path, output_path: Path) -> None:
        if output_path.exists():
            raise FileExistsError(f"refusing to overwrite {output_path}")
        payload_value = cast(
            JsonValue, json.loads(result_path.read_text(encoding="utf-8"))
        )
        payload = self._mapping(payload_value, "result")
        schedules = self._array(payload["schedules"], "schedules")
        if len(schedules) != 2:
            raise ValueError("Stage B plot requires exactly two schedules")
        width = 1200
        height = 900
        elements = [
            self._rect(0, 0, width, height, "#ffffff"),
            self._text(40, 45, "Stage B multi-route data summary", 26, "#111827"),
            self._text(
                40,
                72,
                "Synthetic finite-matrix evidence; not material validation",
                14,
                "#4b5563",
            ),
        ]
        elements.extend(self._blind_panel(schedules, 40, 110, 540, 310))
        elements.extend(self._bridge_panel(schedules, 620, 110, 540, 310))
        elements.extend(self._adverse_panel(schedules, 40, 470, 540, 310))
        elements.extend(self._order_panel(payload, 620, 470, 540, 310))
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
            f'height="{height}" viewBox="0 0 {width} {height}">\n'
            + "\n".join(elements)
            + "\n</svg>\n"
        )
        output_path.write_text(svg, encoding="utf-8")

    def _blind_panel(
        self,
        schedules: list[JsonValue],
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> list[str]:
        values: list[tuple[str, float]] = []
        first = self._mapping(schedules[0], "schedule")
        routes = self._mapping(first["routes"], "routes")
        for route_id in ("A_centered_uniform", "B_reduced_seam"):
            route = self._mapping(routes[route_id], route_id)
            for case_value in self._array(route["blind_cases"], "blind cases"):
                case = self._mapping(case_value, "blind case")
                case_id = self._string(case["case_id"], "case_id")
                for candidate_value in self._array(case["candidates"], "candidates"):
                    candidate = self._mapping(candidate_value, "candidate")
                    values.append(
                        (
                            f"{route_id}:{case_id}",
                            self._real(candidate["objective"], "objective"),
                        )
                    )
        maximum = max((value for _, value in values), default=1.0)
        maximum = max(maximum, 1.0e-15)
        result = self._panel_frame(x, y, width, height, "Blind objective distributions")
        colors = {
            "A_centered_uniform:blind__gamma": "#2563eb",
            "A_centered_uniform:blind__generic": "#60a5fa",
            "B_reduced_seam:blind__gamma": "#dc2626",
            "B_reduced_seam:blind__generic": "#f87171",
        }
        grouped: dict[str, list[float]] = {}
        for key, value in values:
            grouped.setdefault(key, []).append(value)
        for group_index, (key, group) in enumerate(grouped.items()):
            baseline = y + 65 + group_index * 52
            result.append(self._text(x + 18, baseline, key, 11, colors[key]))
            for index, value in enumerate(group):
                px = x + 210 + int((width - 235) * index / max(len(group) - 1, 1))
                scaled = min(value / maximum, 1.0)
                py = baseline - int(28 * scaled)
                result.append(self._circle(px, py, 1.5, colors[key]))
        result.append(
            self._text(
                x + 18,
                y + height - 18,
                f"retained candidates={len(values)}; first schedule shown",
                11,
                "#4b5563",
            )
        )
        return result

    def _bridge_panel(
        self,
        schedules: list[JsonValue],
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> list[str]:
        result = self._panel_frame(x, y, width, height, "Gauge-bridge residuals")
        colors = ("#7c3aed", "#a78bfa")
        all_values: list[float] = []
        decoded: list[list[float]] = []
        for schedule_value in schedules:
            schedule = self._mapping(schedule_value, "schedule")
            values = [
                self._real(
                    self._mapping(value, "bridge")["canonical_maximum_absolute"],
                    "bridge maximum",
                )
                for value in self._array(schedule["bridges"], "bridges")
            ]
            decoded.append(values)
            all_values.extend(values)
        maximum = max(max(all_values, default=1.0), 1.0e-15)
        for schedule_index, values in enumerate(decoded):
            for index, value in enumerate(values):
                px = x + 28 + int((width - 56) * index / max(len(values) - 1, 1))
                py = y + height - 45 - int((height - 90) * value / maximum)
                result.append(self._circle(px, py, 3.0, colors[schedule_index]))
        result.append(
            self._text(
                x + 18,
                y + height - 18,
                f"maximum={maximum:.3e}; violet shades are execution schedules",
                11,
                "#4b5563",
            )
        )
        return result

    def _adverse_panel(
        self,
        schedules: list[JsonValue],
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> list[str]:
        result = self._panel_frame(x, y, width, height, "Fixed-twist adverse control")
        first = self._mapping(schedules[0], "schedule")
        routes = self._mapping(first["routes"], "routes")
        bars: list[tuple[str, float, str]] = []
        for route_id, color in (
            ("A_centered_uniform", "#059669"),
            ("B_reduced_seam", "#d97706"),
        ):
            route = self._mapping(routes[route_id], route_id)
            adverse = self._mapping(route["adverse_controls"], "adverse")
            fixed = self._mapping(adverse["fixed_twist"], "fixed twist")
            bars.append(
                (
                    route_id,
                    self._real(fixed["adverse_maximum_absolute"], "adverse maximum"),
                    color,
                )
            )
        maximum = max((value for _, value, _ in bars), default=1.0)
        for index, (label, value, color) in enumerate(bars):
            by = y + 85 + index * 95
            bar_width = int((width - 190) * value / max(maximum, 1.0e-30))
            result.append(self._text(x + 18, by, label, 12, "#111827"))
            result.append(self._rect(x + 175, by - 18, bar_width, 24, color))
            result.append(
                self._text(x + 185 + bar_width, by, f"{value:.3e}", 11, color)
            )
        return result

    def _order_panel(
        self,
        payload: dict[str, JsonValue],
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> list[str]:
        result = self._panel_frame(x, y, width, height, "Execution-order comparison")
        comparison = self._mapping(payload["order_comparison"], "order comparison")
        groups = (
            ("known cases", "known_case_comparisons"),
            ("bridges", "bridge_comparisons"),
            ("blind summaries", "blind_comparisons"),
        )
        for index, (label, key) in enumerate(groups):
            count = len(self._array(comparison[key], key))
            py = y + 80 + index * 65
            result.append(self._text(x + 30, py, label, 14, "#111827"))
            result.append(self._text(x + 250, py, str(count), 22, "#1d4ed8"))
        criterion = self._mapping(payload["criterion_evaluation"], "criterion")
        status = self._string(criterion["status"], "criterion status")
        result.append(
            self._text(
                x + 30,
                y + height - 28,
                f"overall retained criterion status: {status}",
                13,
                "#047857" if status == "pass" else "#b91c1c",
            )
        )
        return result

    def _panel_frame(
        self, x: int, y: int, width: int, height: int, title: str
    ) -> list[str]:
        return [
            self._rect(x, y, width, height, "#f9fafb", "#d1d5db"),
            self._text(x + 18, y + 30, title, 17, "#111827"),
        ]

    @staticmethod
    def _mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be an object")
        return value

    @staticmethod
    def _array(value: JsonValue, name: str) -> list[JsonValue]:
        if not isinstance(value, list):
            raise TypeError(f"{name} must be an array")
        return value

    @staticmethod
    def _string(value: JsonValue, name: str) -> str:
        if not isinstance(value, str):
            raise TypeError(f"{name} must be a string")
        return value

    @staticmethod
    def _real(value: JsonValue, name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be numeric")
        return float(value)

    @staticmethod
    def _rect(
        x: int,
        y: int,
        width: int,
        height: int,
        fill: str,
        stroke: str = "none",
    ) -> str:
        return (
            f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
            f'fill="{fill}" stroke="{stroke}"/>'
        )

    @staticmethod
    def _text(x: int, y: int, value: str, size: int, color: str) -> str:
        return (
            f'<text x="{x}" y="{y}" font-family="sans-serif" '
            f'font-size="{size}" fill="{color}">{html.escape(value)}</text>'
        )

    @staticmethod
    def _circle(x: int, y: int, radius: float, fill: str) -> str:
        return f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{fill}"/>'


def main() -> None:
    """Adapt command-line paths to the retained-data SVG plotter."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--result", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()
    StageBPlotter().execute(arguments.result, arguments.output)


if __name__ == "__main__":
    main()
