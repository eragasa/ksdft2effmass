"""Software verification of the authenticated visualization base action."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from typing import Self

import matplotlib.pyplot as plt
import pytest
from matplotlib.figure import Figure

from ksdft2effmass.serialization import SerializableValue
from ksdft2effmass.verification import VisualizationVerification
from ksdft2effmass.visualizations import (
    BaseFigure,
    BaseVisualizationData,
    BaseVisualizer,
    PngFigureRenderer,
    PngVisualization,
)

pytestmark = pytest.mark.software_verification


class _Plot(Enum):
    line = "line.png"
    second = "second.png"


class _OtherPlot(Enum):
    line = "other-line.png"


@dataclass(frozen=True, slots=True)
class _Data(BaseVisualizationData):
    label: str

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {"label": self.label}

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {"label"}:
            raise ValueError("data fields do not match")
        label = values["label"]
        if type(label) is not str:
            raise TypeError("label must decode to a built-in string")
        return cls(label=label)


@dataclass(frozen=True, slots=True)
class _Verification(VisualizationVerification):
    accepted: bool
    projection_sha256: str

    @property
    def passed(self) -> bool:
        return self.accepted

    def authenticated_visualization_data_sha256(self) -> str:
        return self.projection_sha256

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "accepted": self.accepted,
            "projection_sha256": self.projection_sha256,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {"accepted", "projection_sha256"}:
            raise ValueError("verification fields do not match")
        accepted = values["accepted"]
        projection_sha256 = values["projection_sha256"]
        if type(accepted) is not bool or type(projection_sha256) is not str:
            raise TypeError("verification fields have invalid types")
        return cls(accepted=accepted, projection_sha256=projection_sha256)


@dataclass(frozen=True, slots=True)
class _DuckVerification:
    passed: bool
    projection_sha256: str

    def authenticated_visualization_data_sha256(self) -> str:
        return self.projection_sha256


@dataclass(frozen=True, slots=True)
class _Figure(BaseFigure):
    def draw(self) -> Figure:
        figure, axis = plt.subplots(figsize=(2.0, 1.0))
        axis.plot((0.0, 1.0), (0.0, 1.0))
        return figure


class _Visualizer(BaseVisualizer[_Data, _Verification, _Plot]):
    __slots__ = ("_duplicate", "_emit")

    def __init__(
        self,
        *,
        data: _Data,
        verification: _Verification,
        plots: tuple[_Plot, ...] = (_Plot.line,),
        emit: bool = True,
        duplicate: bool = False,
    ) -> None:
        super().__init__(data=data, verification=verification, plots=plots)
        self._emit = emit
        self._duplicate = duplicate

    def _render(self) -> frozenset[PngVisualization[_Plot]]:
        if not self._emit:
            return frozenset()
        first = PngFigureRenderer(
            plot=_Plot.line,
            figure=_Figure(),
            dpi=80,
        ).visualize()
        if not self._duplicate:
            return frozenset({first})
        second = PngFigureRenderer(
            plot=_Plot.line,
            figure=_Figure(),
            dpi=81,
        ).visualize()
        return frozenset({first, second})


class TestBaseVisualizer:
    """Establish constructor authentication and final inventory enforcement."""

    def test_visualize__authenticated_request__returns_exact_inventory(self) -> None:
        data = _Data(label="authenticated")
        verification = _Verification(
            accepted=True,
            projection_sha256=hashlib.sha256(data.to_json()).hexdigest(),
        )
        visualizer = _Visualizer(data=data, verification=verification)

        rendered = visualizer.visualize()

        assert visualizer.data is data
        assert visualizer.verification is verification
        assert visualizer.plots == (_Plot.line,)
        assert {value.plot for value in rendered} == {_Plot.line}
        with pytest.raises(AttributeError):
            visualizer.data = _Data(label="replacement")  # type: ignore[misc]
        with pytest.raises(AttributeError):
            visualizer.verification = verification  # type: ignore[misc]
        with pytest.raises(AttributeError):
            visualizer.plots = (_Plot.second,)  # type: ignore[misc]

    def test_init__failed_different_or_duck_verification__rejects(self) -> None:
        data = _Data(label="authenticated")
        digest = hashlib.sha256(data.to_json()).hexdigest()
        with pytest.raises(TypeError, match="VisualizationVerification"):
            _Visualizer(
                data=data,
                verification=_DuckVerification(  # type: ignore[arg-type]
                    passed=True,
                    projection_sha256=digest,
                ),
            )
        with pytest.raises(ValueError, match="passing verification"):
            _Visualizer(
                data=data,
                verification=_Verification(
                    accepted=False,
                    projection_sha256=digest,
                ),
            )
        with pytest.raises(ValueError, match="digests differ"):
            _Visualizer(
                data=data,
                verification=_Verification(
                    accepted=True,
                    projection_sha256="0" * 64,
                ),
            )

    def test_init__invalid_closed_inventory__rejects(self) -> None:
        data = _Data(label="authenticated")
        verification = _Verification(
            accepted=True,
            projection_sha256=hashlib.sha256(data.to_json()).hexdigest(),
        )
        with pytest.raises(ValueError, match="must not be empty"):
            _Visualizer(data=data, verification=verification, plots=())
        with pytest.raises(ValueError, match="unique Enum members"):
            _Visualizer(
                data=data,
                verification=verification,
                plots=(_Plot.line, _Plot.line),
            )
        with pytest.raises(TypeError, match="one Enum type"):
            _Visualizer(
                data=data,
                verification=verification,
                plots=(_Plot.line, _OtherPlot.line),  # type: ignore[arg-type]
            )

    def test_visualize__invalid_rendered_inventory__rejects(self) -> None:
        data = _Data(label="authenticated")
        verification = _Verification(
            accepted=True,
            projection_sha256=hashlib.sha256(data.to_json()).hexdigest(),
        )
        visualizer = _Visualizer(
            data=data,
            verification=verification,
            emit=False,
        )

        with pytest.raises(RuntimeError, match="inventory differs"):
            visualizer.visualize()

        duplicate_visualizer = _Visualizer(
            data=data,
            verification=verification,
            plots=(_Plot.line, _Plot.second),
            duplicate=True,
        )
        with pytest.raises(RuntimeError, match="inventory differs"):
            duplicate_visualizer.visualize()
