"""Baseline scientific figure for band-equivalence locality."""

from __future__ import annotations

from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from ksdft2effmass.visualizations import BaseFigure

from .data import BandEquivalenceLocalityVisualizationData


@dataclass(frozen=True, slots=True)
class _LocalityRequirementsFigure(BaseFigure):
    data: BandEquivalenceLocalityVisualizationData

    def draw(self) -> Figure:
        figure, axes = plt.subplots(1, 2, figsize=(12.0, 4.6), constrained_layout=True)
        case_names = tuple(dict.fromkeys(self.data.point_case_names))
        for case_name in case_names:
            selected = np.asarray(
                [name == case_name for name in self.data.point_case_names],
                dtype=np.bool_,
            )
            amplitudes = np.asarray(self.data.amplitudes, dtype=np.float64)[selected]
            parent_scales = np.asarray(self.data.parent_scales, dtype=np.float64)[
                selected
            ]
            thresholds = np.asarray(
                self.data.minimum_operator_thresholds, dtype=np.float64
            )[selected]
            joint = np.asarray(self.data.joint_operator_thresholds, dtype=np.float64)[
                selected
            ]
            scatter = axes[0].scatter(
                amplitudes,
                thresholds,
                c=parent_scales,
                label=case_name,
                cmap="viridis",
                edgecolors="none",
            )
            axes[1].scatter(
                thresholds,
                joint,
                c=parent_scales,
                label=case_name,
                cmap="viridis",
                edgecolors="none",
            )
        axes[0].set_xlabel("gauge amplitude")
        axes[0].set_ylabel("minimum operator threshold / E_ref")
        axes[0].set_title("Gauge-amplitude requirement")
        axes[1].set_xlabel("minimum operator threshold / E_ref")
        axes[1].set_ylabel("joint spectrum threshold / E_ref")
        axes[1].set_title("Operator and spectrum requirements")
        for axis in axes:
            axis.grid(True, alpha=0.2)
            axis.legend(frameon=False)
        figure.colorbar(scatter, ax=axes, label="parent scale")
        figure.suptitle(
            "Band equivalence and hopping locality — CALCULATED RESULT — UNSEALED"
        )
        return figure
