"""Authenticated figures for rank-two composite-band alignment and locality."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Self

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from projectkoios.physkit.units import MatrixQuantity, Unitless, VectorQuantity

from ksdft2effmass.model_systems.visualization import (
    BaseModelAnalysisFigure,
    BaseModelAnalysisVisualizationData,
    BaseModelAnalysisVisualizer,
    ModelAnalysisPngFigureRenderer,
    ModelAnalysisPngVisualization,
)
from ksdft2effmass.serialization import SerializableValue

if TYPE_CHECKING:
    from .verification import Periodic1DCompositeBandAlignmentVerification


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DCompositeBandAlignmentVisualizationData(
    BaseModelAnalysisVisualizationData
):
    """Retain exactly the verifier-authenticated values drawn by all figures."""

    evaluation_reduced_momenta: VectorQuantity
    evaluation_parent_spectrum: MatrixQuantity
    maximum_ranges: tuple[int, ...]
    channel_names: tuple[str, ...]
    cyclic_conversion_powers: VectorQuantity
    ordinary_omitted_block_l2_norms: MatrixQuantity
    construction_total_spectral_maximum_errors: MatrixQuantity
    evaluation_interpolation_hamiltonian_maximum_errors: VectorQuantity
    evaluation_truncation_hamiltonian_maximum_errors: MatrixQuantity
    evaluation_total_hamiltonian_maximum_errors: MatrixQuantity
    evaluation_interpolation_spectral_maximum_errors: VectorQuantity
    evaluation_truncation_spectral_maximum_errors: MatrixQuantity
    evaluation_total_spectral_maximum_errors: MatrixQuantity
    transform_representatives: tuple[int, ...]
    hopping_block_frobenius_norms: MatrixQuantity
    diagnostic_names: tuple[str, ...]
    diagnostic_values: VectorQuantity

    def __post_init__(self) -> None:
        if type(self.evaluation_reduced_momenta) is not VectorQuantity:
            raise TypeError("evaluation_reduced_momenta must be VectorQuantity")
        if type(self.evaluation_parent_spectrum) is not MatrixQuantity:
            raise TypeError("evaluation_parent_spectrum must be MatrixQuantity")
        if not isinstance(
            self.evaluation_reduced_momenta.unit, Unitless
        ) or not isinstance(self.evaluation_parent_spectrum.unit, Unitless):
            raise ValueError("evaluation values must be unitless")
        size = self.evaluation_reduced_momenta.magnitude.size
        if size <= 0 or self.evaluation_parent_spectrum.magnitude.shape != (size, 2):
            raise ValueError(
                "evaluation spectrum must align with the coordinate vector"
            )
        if not (
            isinstance(self.maximum_ranges, tuple)
            and self.maximum_ranges
            and all(type(value) is int for value in self.maximum_ranges)
        ):
            raise TypeError("maximum_ranges must contain built-in integers")
        if self.maximum_ranges != tuple(sorted(set(self.maximum_ranges))):
            raise ValueError("maximum_ranges must be strictly increasing")
        if self.channel_names != ("reference", "attacked", "pointwise"):
            raise ValueError("channel_names must match the closed channel inventory")
        channel_shape = (len(self.channel_names),)
        for vector, name in (
            (self.cyclic_conversion_powers, "cyclic_conversion_powers"),
            (
                self.evaluation_interpolation_hamiltonian_maximum_errors,
                "evaluation_interpolation_hamiltonian_maximum_errors",
            ),
            (
                self.evaluation_interpolation_spectral_maximum_errors,
                "evaluation_interpolation_spectral_maximum_errors",
            ),
        ):
            if type(vector) is not VectorQuantity:
                raise TypeError(f"{name} must be VectorQuantity")
            if (
                not isinstance(vector.unit, Unitless)
                or vector.magnitude.shape != channel_shape
            ):
                raise ValueError(f"{name} must be a unitless channel vector")
            if np.any(vector.magnitude < 0.0):
                raise ValueError(f"{name} must be nonnegative")
        range_shape = (len(self.maximum_ranges), len(self.channel_names))
        for matrix, name in (
            (
                self.ordinary_omitted_block_l2_norms,
                "ordinary_omitted_block_l2_norms",
            ),
            (
                self.construction_total_spectral_maximum_errors,
                "construction_total_spectral_maximum_errors",
            ),
            (
                self.evaluation_truncation_hamiltonian_maximum_errors,
                "evaluation_truncation_hamiltonian_maximum_errors",
            ),
            (
                self.evaluation_total_hamiltonian_maximum_errors,
                "evaluation_total_hamiltonian_maximum_errors",
            ),
            (
                self.evaluation_truncation_spectral_maximum_errors,
                "evaluation_truncation_spectral_maximum_errors",
            ),
            (
                self.evaluation_total_spectral_maximum_errors,
                "evaluation_total_spectral_maximum_errors",
            ),
        ):
            if type(matrix) is not MatrixQuantity:
                raise TypeError(f"{name} must be MatrixQuantity")
            if (
                not isinstance(matrix.unit, Unitless)
                or matrix.magnitude.shape != range_shape
            ):
                raise ValueError(f"{name} must be a unitless range-by-channel matrix")
            if np.any(matrix.magnitude < 0.0):
                raise ValueError(f"{name} must be nonnegative")
        if not (
            isinstance(self.transform_representatives, tuple)
            and self.transform_representatives
            and all(type(value) is int for value in self.transform_representatives)
        ):
            raise TypeError("transform_representatives must contain integers")
        if self.transform_representatives != tuple(
            sorted(set(self.transform_representatives))
        ):
            raise ValueError("transform_representatives must be sorted and unique")
        if type(self.hopping_block_frobenius_norms) is not MatrixQuantity:
            raise TypeError("hopping_block_frobenius_norms must be MatrixQuantity")
        if not isinstance(self.hopping_block_frobenius_norms.unit, Unitless) or (
            self.hopping_block_frobenius_norms.magnitude.shape
            != (len(self.channel_names), len(self.transform_representatives))
        ):
            raise ValueError("hopping block norms must align with channels and support")
        if np.any(self.hopping_block_frobenius_norms.magnitude < 0.0):
            raise ValueError("hopping block norms must be nonnegative")
        if not (
            isinstance(self.diagnostic_names, tuple)
            and self.diagnostic_names
            and all(type(value) is str and value for value in self.diagnostic_names)
        ):
            raise TypeError("diagnostic_names must contain nonempty strings")
        if len(set(self.diagnostic_names)) != len(self.diagnostic_names):
            raise ValueError("diagnostic_names must be unique")
        if type(self.diagnostic_values) is not VectorQuantity:
            raise TypeError("diagnostic_values must be VectorQuantity")
        if not isinstance(self.diagnostic_values.unit, Unitless) or (
            self.diagnostic_values.magnitude.shape != (len(self.diagnostic_names),)
        ):
            raise ValueError("diagnostic values must align with their names")
        if np.any(self.diagnostic_values.magnitude < 0.0):
            raise ValueError("diagnostic values must be nonnegative")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "evaluation_reduced_momenta": self.evaluation_reduced_momenta,
            "evaluation_parent_spectrum": self.evaluation_parent_spectrum,
            "maximum_ranges": self.maximum_ranges,
            "channel_names": self.channel_names,
            "cyclic_conversion_powers": self.cyclic_conversion_powers,
            "ordinary_omitted_block_l2_norms": (self.ordinary_omitted_block_l2_norms),
            "construction_total_spectral_maximum_errors": (
                self.construction_total_spectral_maximum_errors
            ),
            "evaluation_interpolation_hamiltonian_maximum_errors": (
                self.evaluation_interpolation_hamiltonian_maximum_errors
            ),
            "evaluation_truncation_hamiltonian_maximum_errors": (
                self.evaluation_truncation_hamiltonian_maximum_errors
            ),
            "evaluation_total_hamiltonian_maximum_errors": (
                self.evaluation_total_hamiltonian_maximum_errors
            ),
            "evaluation_interpolation_spectral_maximum_errors": (
                self.evaluation_interpolation_spectral_maximum_errors
            ),
            "evaluation_truncation_spectral_maximum_errors": (
                self.evaluation_truncation_spectral_maximum_errors
            ),
            "evaluation_total_spectral_maximum_errors": (
                self.evaluation_total_spectral_maximum_errors
            ),
            "transform_representatives": self.transform_representatives,
            "hopping_block_frobenius_norms": self.hopping_block_frobenius_norms,
            "diagnostic_names": self.diagnostic_names,
            "diagnostic_values": self.diagnostic_values,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "evaluation_reduced_momenta",
            "evaluation_parent_spectrum",
            "maximum_ranges",
            "channel_names",
            "cyclic_conversion_powers",
            "ordinary_omitted_block_l2_norms",
            "construction_total_spectral_maximum_errors",
            "evaluation_interpolation_hamiltonian_maximum_errors",
            "evaluation_truncation_hamiltonian_maximum_errors",
            "evaluation_total_hamiltonian_maximum_errors",
            "evaluation_interpolation_spectral_maximum_errors",
            "evaluation_truncation_spectral_maximum_errors",
            "evaluation_total_spectral_maximum_errors",
            "transform_representatives",
            "hopping_block_frobenius_norms",
            "diagnostic_names",
            "diagnostic_values",
        }
        if set(values) != required:
            raise ValueError("composite visualization fields do not match")
        coordinates = values["evaluation_reduced_momenta"]
        spectrum = values["evaluation_parent_spectrum"]
        conversion_powers = values["cyclic_conversion_powers"]
        ordinary_omitted = values["ordinary_omitted_block_l2_norms"]
        construction_total = values["construction_total_spectral_maximum_errors"]
        interpolation_hamiltonian = values[
            "evaluation_interpolation_hamiltonian_maximum_errors"
        ]
        truncation_hamiltonian = values[
            "evaluation_truncation_hamiltonian_maximum_errors"
        ]
        total_hamiltonian = values["evaluation_total_hamiltonian_maximum_errors"]
        interpolation_spectral = values[
            "evaluation_interpolation_spectral_maximum_errors"
        ]
        truncation_spectral = values["evaluation_truncation_spectral_maximum_errors"]
        total_spectral = values["evaluation_total_spectral_maximum_errors"]
        hopping_norms = values["hopping_block_frobenius_norms"]
        diagnostic_values = values["diagnostic_values"]
        if type(coordinates) is not VectorQuantity:
            raise TypeError("evaluation_reduced_momenta must decode to VectorQuantity")
        if type(spectrum) is not MatrixQuantity:
            raise TypeError("evaluation_parent_spectrum must decode to MatrixQuantity")
        if type(conversion_powers) is not VectorQuantity:
            raise TypeError("cyclic_conversion_powers must decode to VectorQuantity")
        if type(interpolation_hamiltonian) is not VectorQuantity:
            raise TypeError(
                "evaluation_interpolation_hamiltonian_maximum_errors must decode "
                "to VectorQuantity"
            )
        if type(interpolation_spectral) is not VectorQuantity:
            raise TypeError(
                "evaluation_interpolation_spectral_maximum_errors must decode "
                "to VectorQuantity"
            )
        if type(ordinary_omitted) is not MatrixQuantity:
            raise TypeError(
                "ordinary_omitted_block_l2_norms must decode to MatrixQuantity"
            )
        if type(construction_total) is not MatrixQuantity:
            raise TypeError(
                "construction_total_spectral_maximum_errors must decode to "
                "MatrixQuantity"
            )
        if type(truncation_hamiltonian) is not MatrixQuantity:
            raise TypeError(
                "evaluation_truncation_hamiltonian_maximum_errors must decode "
                "to MatrixQuantity"
            )
        if type(total_hamiltonian) is not MatrixQuantity:
            raise TypeError(
                "evaluation_total_hamiltonian_maximum_errors must decode to "
                "MatrixQuantity"
            )
        if type(truncation_spectral) is not MatrixQuantity:
            raise TypeError(
                "evaluation_truncation_spectral_maximum_errors must decode to "
                "MatrixQuantity"
            )
        if type(total_spectral) is not MatrixQuantity:
            raise TypeError(
                "evaluation_total_spectral_maximum_errors must decode to MatrixQuantity"
            )
        if type(hopping_norms) is not MatrixQuantity:
            raise TypeError(
                "hopping_block_frobenius_norms must decode to MatrixQuantity"
            )
        if type(diagnostic_values) is not VectorQuantity:
            raise TypeError("diagnostic_values must decode to VectorQuantity")
        ranges = cls._integer_tuple(values["maximum_ranges"], "maximum_ranges")
        representatives = cls._integer_tuple(
            values["transform_representatives"], "transform_representatives"
        )
        channels = cls._string_tuple(values["channel_names"], "channel_names")
        diagnostic_names = cls._string_tuple(
            values["diagnostic_names"], "diagnostic_names"
        )
        return cls(
            evaluation_reduced_momenta=coordinates,
            evaluation_parent_spectrum=spectrum,
            maximum_ranges=ranges,
            channel_names=channels,
            cyclic_conversion_powers=conversion_powers,
            ordinary_omitted_block_l2_norms=ordinary_omitted,
            construction_total_spectral_maximum_errors=construction_total,
            evaluation_interpolation_hamiltonian_maximum_errors=(
                interpolation_hamiltonian
            ),
            evaluation_truncation_hamiltonian_maximum_errors=(truncation_hamiltonian),
            evaluation_total_hamiltonian_maximum_errors=total_hamiltonian,
            evaluation_interpolation_spectral_maximum_errors=(interpolation_spectral),
            evaluation_truncation_spectral_maximum_errors=truncation_spectral,
            evaluation_total_spectral_maximum_errors=total_spectral,
            transform_representatives=representatives,
            hopping_block_frobenius_norms=hopping_norms,
            diagnostic_names=diagnostic_names,
            diagnostic_values=diagnostic_values,
        )

    @staticmethod
    def _integer_tuple(value: SerializableValue, name: str) -> tuple[int, ...]:
        if not isinstance(value, tuple):
            raise TypeError(f"{name} must decode to a tuple")
        result: list[int] = []
        for entry in value:
            if type(entry) is not int:
                raise TypeError(f"{name} must decode to integers")
            result.append(entry)
        return tuple(result)

    @staticmethod
    def _string_tuple(value: SerializableValue, name: str) -> tuple[str, ...]:
        if not isinstance(value, tuple):
            raise TypeError(f"{name} must decode to a tuple")
        result: list[str] = []
        for entry in value:
            if type(entry) is not str:
                raise TypeError(f"{name} must decode to strings")
            result.append(entry)
        return tuple(result)


class Periodic1DCompositeBandAlignmentVisualizationPlotEnum(Enum):
    """Declare the closed three-figure output inventory."""

    ALIGNMENT = "rank2-composite-alignment.png"
    LOCALITY = "rank2-composite-locality.png"
    ERROR_CHANNELS = "rank2-composite-error-channels.png"


@dataclass(frozen=True, slots=True)
class _AlignmentFigure(BaseModelAnalysisFigure):
    data: Periodic1DCompositeBandAlignmentVisualizationData

    def draw(self) -> Figure:
        figure, axes = plt.subplots(1, 2, figsize=(12.0, 4.6), constrained_layout=True)
        coordinates = self.data.evaluation_reduced_momenta.magnitude
        spectrum = self.data.evaluation_parent_spectrum.magnitude
        axes[0].plot(coordinates, spectrum[:, 0], label="retained band 1")
        axes[0].plot(coordinates, spectrum[:, 1], label="retained band 2")
        axes[0].set_xlabel("reduced momentum")
        axes[0].set_ylabel("energy / E_ref")
        axes[0].set_title("Parent retained spectrum")
        axes[0].legend()
        positions = np.arange(len(self.data.diagnostic_names), dtype=np.float64)
        axes[1].bar(positions, self.data.diagnostic_values.magnitude)
        axes[1].set_xticks(
            positions, self.data.diagnostic_names, rotation=25, ha="right"
        )
        axes[1].set_yscale("log")
        axes[1].set_ylabel("dimensionless defect")
        axes[1].set_title("Alignment diagnostics")
        figure.suptitle("Rank-two composite-band alignment")
        return figure


@dataclass(frozen=True, slots=True)
class _LocalityFigure(BaseModelAnalysisFigure):
    data: Periodic1DCompositeBandAlignmentVisualizationData

    def draw(self) -> Figure:
        figure, axes = plt.subplots(1, 2, figsize=(12.0, 4.6), constrained_layout=True)
        ranges = np.asarray(self.data.maximum_ranges, dtype=np.int64)
        for index, channel in enumerate(self.data.channel_names):
            axes[0].semilogy(
                ranges,
                self.data.evaluation_total_spectral_maximum_errors.magnitude[:, index],
                marker="o",
                label=channel,
            )
            axes[1].semilogy(
                self.data.transform_representatives,
                self.data.hopping_block_frobenius_norms.magnitude[index],
                marker=".",
                label=channel,
            )
        axes[0].set_xlabel("maximum hopping range")
        axes[0].set_ylabel("evaluation spectral maximum error / E_ref")
        axes[0].set_title("Finite-range spectral errors")
        axes[0].legend()
        axes[1].set_xlabel("lattice representative")
        axes[1].set_ylabel("block Frobenius norm / E_ref")
        axes[1].set_title("Complete block-hopping decay")
        axes[1].legend()
        figure.suptitle("Rank-two composite-band block locality")
        return figure


@dataclass(frozen=True, slots=True)
class _ErrorChannelFigure(BaseModelAnalysisFigure):
    data: Periodic1DCompositeBandAlignmentVisualizationData

    def draw(self) -> Figure:
        figure, axes = plt.subplots(1, 3, figsize=(15.0, 4.6), constrained_layout=True)
        ranges = np.asarray(self.data.maximum_ranges, dtype=np.int64)
        attacked_index = self.data.channel_names.index("attacked")
        positions = np.arange(len(self.data.channel_names), dtype=np.float64)
        axes[0].bar(positions, self.data.cyclic_conversion_powers.magnitude)
        axes[0].set_xticks(positions, self.data.channel_names, rotation=20, ha="right")
        axes[0].set_yscale("log")
        axes[0].set_ylabel("conversion power / E_ref²")
        axes[0].set_title("Cyclic Nyquist conversion")
        interpolation_hamiltonian = (
            self.data.evaluation_interpolation_hamiltonian_maximum_errors.magnitude[
                attacked_index
            ]
        )
        axes[1].semilogy(
            ranges,
            np.full(ranges.shape, interpolation_hamiltonian),
            marker="o",
            label="interpolation",
        )
        axes[1].semilogy(
            ranges,
            self.data.evaluation_truncation_hamiltonian_maximum_errors.magnitude[
                :, attacked_index
            ],
            marker="o",
            label="truncation",
        )
        axes[1].semilogy(
            ranges,
            self.data.evaluation_total_hamiltonian_maximum_errors.magnitude[
                :, attacked_index
            ],
            marker="o",
            label="total",
        )
        axes[1].set_xlabel("maximum hopping range")
        axes[1].set_ylabel("normalized maximum Frobenius error")
        axes[1].set_title("Attacked Hamiltonian channels")
        axes[1].legend()
        interpolation_spectral = (
            self.data.evaluation_interpolation_spectral_maximum_errors.magnitude[
                attacked_index
            ]
        )
        axes[2].semilogy(
            ranges,
            np.full(ranges.shape, interpolation_spectral),
            marker="o",
            label="interpolation",
        )
        axes[2].semilogy(
            ranges,
            self.data.evaluation_truncation_spectral_maximum_errors.magnitude[
                :, attacked_index
            ],
            marker="o",
            label="truncation",
        )
        axes[2].semilogy(
            ranges,
            self.data.evaluation_total_spectral_maximum_errors.magnitude[
                :, attacked_index
            ],
            marker="o",
            label="total",
        )
        axes[2].set_xlabel("maximum hopping range")
        axes[2].set_ylabel("maximum sorted-band error / E_ref")
        axes[2].set_title("Attacked spectral channels")
        axes[2].legend()
        figure.suptitle("Rank-two composite-band error-channel decomposition")
        return figure


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeBandAlignmentVisualizer(BaseModelAnalysisVisualizer):
    """Authenticate one projection and render the closed three-figure inventory."""

    data: Periodic1DCompositeBandAlignmentVisualizationData
    verification: Periodic1DCompositeBandAlignmentVerification
    dpi: int = 180

    def __post_init__(self) -> None:
        self._authenticate(self.data, self.verification)
        if type(self.dpi) is not int:
            raise TypeError("dpi must be a built-in int")
        if self.dpi <= 0:
            raise ValueError("dpi must be positive")

    def visualize(
        self,
    ) -> frozenset[
        ModelAnalysisPngVisualization[
            Periodic1DCompositeBandAlignmentVisualizationPlotEnum
        ]
    ]:
        visualizations = frozenset(
            {
                ModelAnalysisPngFigureRenderer(
                    Periodic1DCompositeBandAlignmentVisualizationPlotEnum.ALIGNMENT,
                    _AlignmentFigure(self.data),
                    self.dpi,
                ).visualize(),
                ModelAnalysisPngFigureRenderer(
                    Periodic1DCompositeBandAlignmentVisualizationPlotEnum.LOCALITY,
                    _LocalityFigure(self.data),
                    self.dpi,
                ).visualize(),
                ModelAnalysisPngFigureRenderer(
                    Periodic1DCompositeBandAlignmentVisualizationPlotEnum.ERROR_CHANNELS,
                    _ErrorChannelFigure(self.data),
                    self.dpi,
                ).visualize(),
            }
        )
        self._require_complete_inventory(
            visualizations,
            frozenset(Periodic1DCompositeBandAlignmentVisualizationPlotEnum),
        )
        return visualizations


__all__ = [
    "Periodic1DCompositeBandAlignmentVisualizationData",
    "Periodic1DCompositeBandAlignmentVisualizationPlotEnum",
    "Periodic1DCompositeBandAlignmentVisualizer",
]
