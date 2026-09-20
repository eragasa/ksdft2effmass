"""Matplotlib rendering for retained defect-2D Stage C parent results.

The represented input is a retained JSON result document. The plotting ActionObjects
render scalar criteria and adverse-control diagnostics on caller-supplied Matplotlib
axes or create new axes when none are supplied. The SVG Workflow composes those plots
without loading matrix artifacts, performing accepted-parent calculations,
establishing scientific validity, or quantifying uncertainty.
"""

from __future__ import annotations

import io
import json
import math
import os
from dataclasses import dataclass
from pathlib import Path

from matplotlib import pyplot as plt
from matplotlib.axes import Axes

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type RawJsonValue = (
    JsonScalar | list[RawJsonValue] | tuple[tuple[str, RawJsonValue], ...]
)


@dataclass(frozen=True, slots=True)
class AdoptedCriterionPlotRecord:
    """Represent one retained adopted-criterion plotting row.

    Parameters
    ----------
    identifier
        Nonempty criterion identifier displayed on the vertical axis.
    value
        Finite retained criterion value.
    comparison
        Displayed comparison operator. Supported values are ``<=``, ``==``, ``>=``,
        ``<``, and ``>``.
    threshold
        Finite retained acceptance threshold.
    passed
        Exact retained software-criterion disposition.
    """

    identifier: str
    value: float
    comparison: str
    threshold: float
    passed: bool

    def __post_init__(self) -> None:
        """Enforce the closed plotting-record contract."""

        if type(self.identifier) is not str or not self.identifier:
            raise TypeError("identifier must be a nonempty string")
        if type(self.value) is not float:
            raise TypeError("value must be a float")
        if not math.isfinite(self.value):
            raise ValueError("value must be finite")
        if type(self.comparison) is not str:
            raise TypeError("comparison must be a string")
        if self.comparison not in {"<=", "==", ">=", "<", ">"}:
            raise ValueError("comparison is not supported")
        if type(self.threshold) is not float:
            raise TypeError("threshold must be a float")
        if not math.isfinite(self.threshold):
            raise ValueError("threshold must be finite")
        if type(self.passed) is not bool:
            raise TypeError("passed must be a bool")


@dataclass(frozen=True, slots=True)
class AdverseControlPlotRecord:
    """Represent one retained adverse-control plotting row.

    Parameters
    ----------
    identifier
        Nonempty adverse-control identifier displayed on the vertical axis.
    status
        Nonempty retained status text.
    value
        Finite nonnegative diagnostic value, or ``None`` when the control reports
        status only.
    """

    identifier: str
    status: str
    value: float | None

    def __post_init__(self) -> None:
        """Enforce the closed adverse-control plotting contract."""

        if type(self.identifier) is not str or not self.identifier:
            raise TypeError("identifier must be a nonempty string")
        if type(self.status) is not str or not self.status:
            raise TypeError("status must be a nonempty string")
        if self.value is not None:
            if type(self.value) is not float:
                raise TypeError("value must be a float or None")
            if not math.isfinite(self.value):
                raise ValueError("value must be finite")
            if self.value < 0.0:
                raise ValueError("value must be nonnegative")


@dataclass(frozen=True, slots=True)
class StageCParentPlotData:
    """Retain the scalar Stage C data required by the plotting composition.

    Parameters
    ----------
    accepted_parent_read
        Whether the source result records an accepted-parent read.
    criteria
        Ordered adopted-criterion plotting rows.
    adverse_controls
        Ordered adverse-control plotting rows from the first retained schedule.
    route_evaluations
        Nonnegative retained route-evaluation count.
    bridge_records
        Nonnegative retained bridge-record count.
    model_fit_records
        Nonnegative retained model-fit count.
    schedule_comparisons
        Nonnegative retained schedule-comparison count.
    """

    accepted_parent_read: bool
    criteria: tuple[AdoptedCriterionPlotRecord, ...]
    adverse_controls: tuple[AdverseControlPlotRecord, ...]
    route_evaluations: int
    bridge_records: int
    model_fit_records: int
    schedule_comparisons: int

    def __post_init__(self) -> None:
        """Require typed nonempty channels and nonnegative inventory counts."""

        if type(self.accepted_parent_read) is not bool:
            raise TypeError("accepted_parent_read must be a bool")
        if type(self.criteria) is not tuple or not self.criteria:
            raise TypeError("criteria must be a nonempty tuple")
        if not all(
            type(record) is AdoptedCriterionPlotRecord for record in self.criteria
        ):
            raise TypeError("criteria must contain AdoptedCriterionPlotRecord values")
        if type(self.adverse_controls) is not tuple or not self.adverse_controls:
            raise TypeError("adverse_controls must be a nonempty tuple")
        if not all(
            type(record) is AdverseControlPlotRecord for record in self.adverse_controls
        ):
            raise TypeError(
                "adverse_controls must contain AdverseControlPlotRecord values"
            )
        for name, value in (
            ("route_evaluations", self.route_evaluations),
            ("bridge_records", self.bridge_records),
            ("model_fit_records", self.model_fit_records),
            ("schedule_comparisons", self.schedule_comparisons),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be an int")
            if value < 0:
                raise ValueError(f"{name} must be nonnegative")


class StageCParentResultReader:
    """Decode the retained scalar diagnostics required by the plotters."""

    __slots__ = ()

    def execute(self, result_path: Path) -> StageCParentPlotData:
        """Decode one retained Stage C JSON result into immutable plotting data.

        Parameters
        ----------
        result_path
            Existing UTF-8 JSON result path.

        Returns
        -------
        StageCParentPlotData
            Immutable scalar diagnostics and inventory counts.

        Raises
        ------
        TypeError
            If a required field has the wrong semantic type.
        KeyError
            If a required field is absent.
        ValueError
            If the source is not valid UTF-8 JSON or violates a plotting invariant.
        """

        if not isinstance(result_path, Path):
            raise TypeError("result_path must be a Path")
        try:
            decoded: RawJsonValue = json.loads(
                result_path.read_bytes(), object_pairs_hook=self.object_pairs
            )
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError("result must be valid UTF-8 JSON") from error
        result = self.mapping(self.normalize(decoded), "result")
        schedules = self.array(result["schedules"], "schedules")
        if not schedules:
            raise ValueError("schedules must be nonempty")
        first_schedule = self.mapping(schedules[0], "schedule")
        inventory = self.mapping(result["inventory"], "inventory")
        criteria = tuple(
            self.criterion(self.mapping(value, "criterion"))
            for value in self.array(result["criteria"], "criteria")
        )
        adverse_controls = tuple(
            self.adverse_control(self.mapping(value, "adverse control"))
            for value in self.array(
                first_schedule["adverse_controls"], "adverse controls"
            )
        )
        return StageCParentPlotData(
            accepted_parent_read=self.boolean(
                result["accepted_parent_read"], "accepted_parent_read"
            ),
            criteria=criteria,
            adverse_controls=adverse_controls,
            route_evaluations=self.integer(
                inventory["route_evaluations"], "route_evaluations"
            ),
            bridge_records=self.integer(inventory["bridge_records"], "bridge_records"),
            model_fit_records=self.integer(
                inventory["model_fit_records"], "model_fit_records"
            ),
            schedule_comparisons=self.integer(
                inventory["schedule_comparisons"], "schedule_comparisons"
            ),
        )

    def criterion(self, value: dict[str, JsonValue]) -> AdoptedCriterionPlotRecord:
        """Decode one adopted-criterion plotting row."""

        return AdoptedCriterionPlotRecord(
            identifier=self.text(value["criterion"], "criterion"),
            value=self.real(value["value"], "value"),
            comparison=self.text(value["comparison"], "comparison"),
            threshold=self.real(value["threshold"], "threshold"),
            passed=self.boolean(value["passed"], "passed"),
        )

    def adverse_control(self, value: dict[str, JsonValue]) -> AdverseControlPlotRecord:
        """Decode one adverse-control plotting row."""

        raw_value = value["value"]
        numerical_value = (
            None if raw_value is None else self.real(raw_value, "adverse value")
        )
        return AdverseControlPlotRecord(
            identifier=self.text(value["control_id"], "control_id"),
            status=self.text(value["status"], "status"),
            value=numerical_value,
        )

    @classmethod
    def normalize(cls, value: RawJsonValue) -> JsonValue:
        """Convert decoded JSON into the closed recursive representation."""

        if value is None or isinstance(value, bool | int | float | str):
            return value
        if isinstance(value, list):
            return [cls.normalize(item) for item in value]
        result: dict[str, JsonValue] = {}
        for key, item in value:
            if key in result:
                raise ValueError(f"duplicate JSON object name: {key}")
            result[key] = cls.normalize(item)
        return result

    @staticmethod
    def object_pairs(
        pairs: list[tuple[str, RawJsonValue]],
    ) -> tuple[tuple[str, RawJsonValue], ...]:
        """Preserve object pairs so duplicate JSON names can be rejected."""

        return tuple(pairs)

    @staticmethod
    def mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        """Return one JSON object or raise ``TypeError``."""

        if type(value) is not dict:
            raise TypeError(f"{name} must be an object")
        return value

    @staticmethod
    def array(value: JsonValue, name: str) -> list[JsonValue]:
        """Return one JSON array or raise ``TypeError``."""

        if type(value) is not list:
            raise TypeError(f"{name} must be an array")
        return value

    @staticmethod
    def text(value: JsonValue, name: str) -> str:
        """Return one nonempty JSON string or raise ``TypeError``."""

        if type(value) is not str or not value:
            raise TypeError(f"{name} must be a nonempty string")
        return value

    @staticmethod
    def real(value: JsonValue, name: str) -> float:
        """Return one finite JSON real without admitting Boolean values."""

        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be real")
        result = float(value)
        if not math.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result

    @staticmethod
    def integer(value: JsonValue, name: str) -> int:
        """Return one JSON integer without admitting Boolean values."""

        if type(value) is not int:
            raise TypeError(f"{name} must be an integer")
        return value

    @staticmethod
    def boolean(value: JsonValue, name: str) -> bool:
        """Return one JSON Boolean."""

        if type(value) is not bool:
            raise TypeError(f"{name} must be boolean")
        return value


class AdoptedCriteriaPlot:
    """Render adopted Stage C criteria on supplied or newly created axes.

    Parameters
    ----------
    axes
        Matplotlib axes to clear and populate. If ``None``, :meth:`execute` creates
        and returns axes in a new figure.
    """

    __slots__ = ("_axes",)

    def __init__(self, axes: Axes | None = None) -> None:
        if axes is not None and not isinstance(axes, Axes):
            raise TypeError("axes must be a matplotlib.axes.Axes or None")
        self._axes = axes

    def execute(self, criteria: tuple[AdoptedCriterionPlotRecord, ...]) -> Axes:
        """Render ordered criterion rows and return the populated axes.

        Parameters
        ----------
        criteria
            Nonempty immutable sequence of adopted-criterion rows.

        Returns
        -------
        matplotlib.axes.Axes
            The supplied axes, or newly created axes when none were supplied.

        Raises
        ------
        TypeError
            If *criteria* is not a tuple of ``AdoptedCriterionPlotRecord`` values.
        ValueError
            If *criteria* is empty.
        """

        if type(criteria) is not tuple or not all(
            type(record) is AdoptedCriterionPlotRecord for record in criteria
        ):
            raise TypeError(
                "criteria must be a tuple of AdoptedCriterionPlotRecord values"
            )
        if not criteria:
            raise ValueError("criteria must be nonempty")
        axes = self._axes if self._axes is not None else self.new_axes()
        axes.clear()
        positions = tuple(range(len(criteria)))
        colors = tuple("#15803d" if record.passed else "#b91c1c" for record in criteria)
        axes.scatter(
            [0.0] * len(criteria),
            positions,
            marker="s",
            s=70.0,
            c=colors,
            clip_on=False,
        )
        for position, record in zip(positions, criteria, strict=True):
            axes.text(
                0.04,
                position,
                record.identifier,
                ha="left",
                va="center",
                fontsize=8,
                family="monospace",
                color="#0f172a",
            )
            axes.text(
                0.99,
                position,
                f"{record.value:.3e} {record.comparison} {record.threshold:.3e}",
                ha="right",
                va="center",
                fontsize=8,
                family="monospace",
                color="#334155",
            )
        axes.set_xlim(-0.02, 1.02)
        axes.set_ylim(len(criteria) - 0.5, -0.5)
        axes.set_title("Adopted criteria", loc="left", fontsize=12, weight="bold")
        axes.set_axis_off()
        return axes

    @staticmethod
    def new_axes() -> Axes:
        """Create standalone Matplotlib axes for one criteria plot."""

        figure = plt.figure(figsize=(12.4, 7.0), layout="constrained")
        return figure.add_subplot(1, 1, 1)


class AdverseControlBarPlot:
    """Render adverse-control diagnostics on supplied or newly created axes.

    Parameters
    ----------
    axes
        Matplotlib axes to clear and populate. If ``None``, :meth:`execute` creates
        and returns axes in a new figure.
    """

    __slots__ = ("_axes",)

    def __init__(self, axes: Axes | None = None) -> None:
        if axes is not None and not isinstance(axes, Axes):
            raise TypeError("axes must be a matplotlib.axes.Axes or None")
        self._axes = axes

    def execute(self, controls: tuple[AdverseControlPlotRecord, ...]) -> Axes:
        """Render normalized adverse-control bars and return the populated axes.

        Numerical bars are normalized by the largest retained numerical value.
        Status-only controls use a fixed 0.55 display width and are colored purple.
        The normalization is a display convention, not a physical comparison.

        Parameters
        ----------
        controls
            Nonempty immutable sequence of adverse-control rows.

        Returns
        -------
        matplotlib.axes.Axes
            The supplied axes, or newly created axes when none were supplied.

        Raises
        ------
        TypeError
            If *controls* is not a tuple of ``AdverseControlPlotRecord`` values.
        ValueError
            If *controls* is empty or contains no numerical control.
        """

        if type(controls) is not tuple or not all(
            type(record) is AdverseControlPlotRecord for record in controls
        ):
            raise TypeError(
                "controls must be a tuple of AdverseControlPlotRecord values"
            )
        if not controls:
            raise ValueError("controls must be nonempty")
        numerical = tuple(
            record.value for record in controls if record.value is not None
        )
        if not numerical:
            raise ValueError("controls must contain at least one numerical value")
        maximum = max(numerical)
        scale = maximum if maximum > 0.0 else 1.0
        widths = tuple(
            0.55 if record.value is None else record.value / scale
            for record in controls
        )
        colors = tuple(
            "#7c3aed" if record.value is None else "#c2410c" for record in controls
        )
        positions = tuple(range(len(controls)))
        axes = self._axes if self._axes is not None else self.new_axes()
        axes.clear()
        axes.barh(positions, widths, color=colors, height=0.62)
        axes.set_yticks(
            positions, labels=tuple(record.identifier for record in controls)
        )
        axes.invert_yaxis()
        axes.set_xlim(0.0, 1.22)
        axes.set_xlabel("relative to maximum numerical adverse value")
        axes.set_title("Adverse controls", loc="left", fontsize=12, weight="bold")
        axes.tick_params(axis="y", labelsize=8)
        axes.tick_params(axis="x", labelsize=8)
        axes.grid(axis="x", color="#cbd5e1", linewidth=0.6, alpha=0.7)
        axes.set_axisbelow(True)
        for position, width, record in zip(positions, widths, controls, strict=True):
            label = record.status if record.value is None else f"{record.value:.3e}"
            axes.text(
                min(width + 0.015, 1.03),
                position,
                label,
                ha="left",
                va="center",
                fontsize=8,
                family="monospace",
                color="#334155",
            )
        return axes

    @staticmethod
    def new_axes() -> Axes:
        """Create standalone Matplotlib axes for one adverse-control plot."""

        figure = plt.figure(figsize=(12.4, 5.0), layout="constrained")
        return figure.add_subplot(1, 1, 1)


class StageCParentSvgPlotter:
    """Compose retained criteria and adverse-control plots into one SVG."""

    __slots__ = ("_reader",)

    def __init__(self) -> None:
        self._reader = StageCParentResultReader()

    def execute(self, result_path: Path, output_path: Path) -> None:
        """Render one retained Stage C JSON result to a new deterministic SVG.

        Parameters
        ----------
        result_path
            Existing UTF-8 JSON result containing criteria, schedule diagnostics,
            and inventory counts.
        output_path
            New SVG path. Parent directories are created when necessary.

        Raises
        ------
        FileExistsError
            If *output_path* already exists.
        TypeError
            If a required retained field has the wrong semantic type.
        KeyError
            If a required retained field is absent.
        ValueError
            If the input is invalid JSON or violates a plotting invariant.

        Notes
        -----
        Matplotlib SVG IDs use a fixed salt and volatile date metadata is omitted.
        Determinism is bounded to the same Matplotlib and font environment. Rendering
        is software behavior and does not establish scientific validation or UQ.
        """

        if not isinstance(result_path, Path):
            raise TypeError("result_path must be a Path")
        if not isinstance(output_path, Path):
            raise TypeError("output_path must be a Path")
        data = self._reader.execute(result_path)
        with plt.rc_context(
            {
                "font.family": "DejaVu Sans",
                "svg.fonttype": "none",
                "svg.hashsalt": "ksdft2effmass-stage-c-parent-v2",
            }
        ):
            figure = plt.figure(figsize=(12.4, 10.8), layout="constrained")
            grid = figure.add_gridspec(2, 1, height_ratios=(1.7, 1.0))
            criteria_axes = figure.add_subplot(grid[0, 0])
            adverse_axes = figure.add_subplot(grid[1, 0])
            AdoptedCriteriaPlot(criteria_axes).execute(data.criteria)
            AdverseControlBarPlot(adverse_axes).execute(data.adverse_controls)
            title = (
                "Stage C retained-result diagnostics"
                if data.accepted_parent_read
                else "Stage C accepted-parent contract: authored-fixture behavior"
            )
            subtitle = (
                "Caller-supplied retained fields; evidence status is not authenticated"
                if data.accepted_parent_read
                else (
                    "Synthetic software verification only; no accepted-parent read "
                    "or result"
                )
            )
            figure.suptitle(title, fontsize=17, weight="bold", color="#172554")
            figure.text(
                0.5,
                0.965,
                subtitle,
                ha="center",
                va="top",
                fontsize=10,
                color="#475569",
            )
            figure.text(
                0.5,
                0.006,
                (
                    f"{data.route_evaluations} route evaluations · "
                    f"{data.bridge_records} bridges · "
                    f"{data.model_fit_records:,} model fits · "
                    f"{data.schedule_comparisons} schedule comparisons"
                ),
                ha="center",
                va="bottom",
                fontsize=9,
                color="#475569",
            )
            buffer = io.BytesIO()
            try:
                figure.savefig(
                    buffer,
                    format="svg",
                    metadata={"Date": None, "Creator": "ksdft2effmass"},
                    facecolor="#f8fafc",
                )
            finally:
                plt.close(figure)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("xb") as stream:
            stream.write(buffer.getvalue())
            stream.flush()
            os.fsync(stream.fileno())
