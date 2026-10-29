"""Authenticated rank-two composite-alignment projection."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

import numpy as np
from projectkoios.physkit.units import MatrixQuantity, Unitless, VectorQuantity

from ksdft2effmass.serialization import SerializableValue
from ksdft2effmass.visualizations import BaseVisualizationData


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DCompositeBandAlignmentVisualizationData(BaseVisualizationData):
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
        maximum_ranges_value = values["maximum_ranges"]
        if not isinstance(maximum_ranges_value, tuple):
            raise TypeError("maximum_ranges must decode to a tuple")
        ranges_list: list[int] = []
        for entry in maximum_ranges_value:
            if type(entry) is not int:
                raise TypeError("maximum_ranges must decode to integers")
            ranges_list.append(entry)
        ranges = tuple(ranges_list)

        representatives_value = values["transform_representatives"]
        if not isinstance(representatives_value, tuple):
            raise TypeError("transform_representatives must decode to a tuple")
        representatives_list: list[int] = []
        for entry in representatives_value:
            if type(entry) is not int:
                raise TypeError("transform_representatives must decode to integers")
            representatives_list.append(entry)
        representatives = tuple(representatives_list)

        channel_names_value = values["channel_names"]
        if not isinstance(channel_names_value, tuple):
            raise TypeError("channel_names must decode to a tuple")
        channels_list: list[str] = []
        for entry in channel_names_value:
            if type(entry) is not str:
                raise TypeError("channel_names must decode to strings")
            channels_list.append(entry)
        channels = tuple(channels_list)

        diagnostic_names_value = values["diagnostic_names"]
        if not isinstance(diagnostic_names_value, tuple):
            raise TypeError("diagnostic_names must decode to a tuple")
        diagnostic_names_list: list[str] = []
        for entry in diagnostic_names_value:
            if type(entry) is not str:
                raise TypeError("diagnostic_names must decode to strings")
            diagnostic_names_list.append(entry)
        diagnostic_names = tuple(diagnostic_names_list)
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
