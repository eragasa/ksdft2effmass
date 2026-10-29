"""Authenticated constrained-admissible-set visualization projection."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

import numpy as np
from projectkoios.physkit.units import MatrixQuantity, Unitless, VectorQuantity

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue
from ksdft2effmass.visualizations import BaseVisualizationData

from ..definition import Periodic1DAdmissibleSetThresholds
from ..results import (
    Periodic1DAdmissibleSetDisposition,
    Periodic1DAdmissibleSetParameterEvaluation,
)


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DAdmissibleSetProofPointVisualizationData(BaseTypedRecord):
    """Pair one typed proof-point evaluation with its authenticated case context."""

    thresholds: Periodic1DAdmissibleSetThresholds
    disposition: Periodic1DAdmissibleSetDisposition
    separation_bounds: VectorQuantity
    evaluation: Periodic1DAdmissibleSetParameterEvaluation

    def __post_init__(self) -> None:
        if type(self.thresholds) is not Periodic1DAdmissibleSetThresholds:
            raise TypeError("thresholds has the wrong exact type")
        if type(self.disposition) is not Periodic1DAdmissibleSetDisposition:
            raise TypeError("disposition has the wrong exact type")
        if type(self.separation_bounds) is not VectorQuantity:
            raise TypeError("separation_bounds must be VectorQuantity")
        if (
            not isinstance(self.separation_bounds.unit, Unitless)
            or self.separation_bounds.magnitude.shape != (2,)
            or np.any(self.separation_bounds.magnitude < 0.0)
        ):
            raise ValueError(
                "separation_bounds must be a nonnegative unitless length-two vector"
            )
        if self.separation_bounds.magnitude[0] > self.separation_bounds.magnitude[1]:
            raise ValueError("separation_bounds must be ordered")
        if type(self.evaluation) is not Periodic1DAdmissibleSetParameterEvaluation:
            raise TypeError("evaluation has the wrong exact type")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "thresholds": self.thresholds.to_dict(),
            "disposition": self.disposition.value,
            "separation_bounds": self.separation_bounds,
            "evaluation": self.evaluation.to_dict(),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "thresholds",
            "disposition",
            "separation_bounds",
            "evaluation",
        }:
            raise ValueError("proof-point visualization fields do not match")
        thresholds = values["thresholds"]
        disposition = values["disposition"]
        bounds = values["separation_bounds"]
        evaluation = values["evaluation"]
        if not isinstance(thresholds, Mapping):
            raise TypeError("thresholds must decode to a mapping")
        if type(disposition) is not str:
            raise TypeError("disposition must decode to a string")
        if type(bounds) is not VectorQuantity:
            raise TypeError("separation_bounds must decode to VectorQuantity")
        if not isinstance(evaluation, Mapping):
            raise TypeError("evaluation must decode to a mapping")
        return cls(
            Periodic1DAdmissibleSetThresholds.from_dict(thresholds),
            Periodic1DAdmissibleSetDisposition(disposition),
            bounds,
            Periodic1DAdmissibleSetParameterEvaluation.from_dict(evaluation),
        )


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DConstrainedAdmissibleSetVisualizationData(BaseVisualizationData):
    """Retain the complete verifier-authenticated two-figure projection."""

    parameter_names: tuple[str, str]
    parameter_bounds: MatrixQuantity
    loss_channel_names: tuple[str, str]
    locality_channel_names: tuple[str, str, str]
    proof_points: tuple[
        Periodic1DAdmissibleSetProofPointVisualizationData,
        Periodic1DAdmissibleSetProofPointVisualizationData,
        Periodic1DAdmissibleSetProofPointVisualizationData,
    ]

    def __post_init__(self) -> None:
        if self.parameter_names != ("energy_shift_ratio", "splitting_scale"):
            raise ValueError("parameter_names must match the closed parameter order")
        if type(self.parameter_bounds) is not MatrixQuantity:
            raise TypeError("parameter_bounds must be MatrixQuantity")
        if (
            not isinstance(self.parameter_bounds.unit, Unitless)
            or self.parameter_bounds.magnitude.shape != (2, 2)
            or np.any(
                self.parameter_bounds.magnitude[:, 0]
                >= self.parameter_bounds.magnitude[:, 1]
            )
        ):
            raise ValueError(
                "parameter_bounds must contain two increasing unitless pairs"
            )
        if self.loss_channel_names != ("spectral", "operator"):
            raise ValueError("loss_channel_names must match the closed channel order")
        if self.locality_channel_names != ("reference", "attacked", "candidate"):
            raise ValueError(
                "locality_channel_names must match the closed channel order"
            )
        if not isinstance(self.proof_points, tuple) or len(self.proof_points) != 3:
            raise TypeError(
                "proof_points must contain the closed three-point inventory"
            )
        if any(
            type(value) is not Periodic1DAdmissibleSetProofPointVisualizationData
            for value in self.proof_points
        ):
            raise TypeError("proof_points contain a value of the wrong exact type")
        if tuple(value.evaluation.role for value in self.proof_points) != (
            "compatible-common-witness",
            "separated-spectral-boundary",
            "separated-operator-boundary",
        ):
            raise ValueError("proof_points must match the closed role inventory")
        ranges = tuple(
            item.maximum_range for item in self.proof_points[0].evaluation.locality
        )
        if any(
            tuple(item.maximum_range for item in value.evaluation.locality) != ranges
            for value in self.proof_points
        ):
            raise ValueError("proof points must share one locality-range inventory")
        lower = self.parameter_bounds.magnitude[:, 0]
        upper = self.parameter_bounds.magnitude[:, 1]
        if any(
            np.any(np.asarray(value.evaluation.parameter) < lower)
            or np.any(np.asarray(value.evaluation.parameter) > upper)
            for value in self.proof_points
        ):
            raise ValueError(
                "proof-point parameters must lie in the declared rectangle"
            )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "parameter_names": self.parameter_names,
            "parameter_bounds": self.parameter_bounds,
            "loss_channel_names": self.loss_channel_names,
            "locality_channel_names": self.locality_channel_names,
            "proof_points": tuple(value.to_dict() for value in self.proof_points),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "parameter_names",
            "parameter_bounds",
            "loss_channel_names",
            "locality_channel_names",
            "proof_points",
        }:
            raise ValueError("admissible-set visualization fields do not match")
        parameter_names = values["parameter_names"]
        bounds = values["parameter_bounds"]
        loss_names = values["loss_channel_names"]
        locality_names = values["locality_channel_names"]
        proof_points = values["proof_points"]
        if (
            not isinstance(parameter_names, tuple)
            or len(parameter_names) != 2
            or any(type(value) is not str for value in parameter_names)
        ):
            raise TypeError("parameter_names must decode to two strings")
        if type(bounds) is not MatrixQuantity:
            raise TypeError("parameter_bounds must decode to MatrixQuantity")
        if (
            not isinstance(loss_names, tuple)
            or len(loss_names) != 2
            or any(type(value) is not str for value in loss_names)
        ):
            raise TypeError("loss_channel_names must decode to two strings")
        if (
            not isinstance(locality_names, tuple)
            or len(locality_names) != 3
            or any(type(value) is not str for value in locality_names)
        ):
            raise TypeError("locality_channel_names must decode to three strings")
        if not isinstance(proof_points, tuple) or len(proof_points) != 3:
            raise TypeError("proof_points must decode to three mappings")
        decoded: list[Periodic1DAdmissibleSetProofPointVisualizationData] = []
        for value in proof_points:
            if not isinstance(value, Mapping):
                raise TypeError("proof points must decode to mappings")
            decoded.append(
                Periodic1DAdmissibleSetProofPointVisualizationData.from_dict(value)
            )
        return cls(
            parameter_names,
            bounds,
            loss_names,
            locality_names,
            (decoded[0], decoded[1], decoded[2]),
        )


__all__ = [
    "Periodic1DAdmissibleSetProofPointVisualizationData",
    "Periodic1DConstrainedAdmissibleSetVisualizationData",
]
