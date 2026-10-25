"""Typed finite algebraic diagnostics for PIAB1D grid sweeps."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING, Self, cast

import numpy as np
from projectkoios.physkit.units import Unitless, VectorQuantity

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

if TYPE_CHECKING:
    from .grid_sweep import Piab1dGridSweepDefinition


@dataclass(frozen=True, slots=True, eq=False)
class Piab1dFiniteAlgebraicDiagnostics(BaseTypedRecord):
    """Retain grid-indexed spectral and reduction discrepancies.

    Parameters
    ----------
    definition
        Shared PIAB1D grid-sweep declaration.
    discrete_spectrum
        Maximum represented-energy discrepancy from the exact discrete spectrum.
    spectral_reconstruction
        Frobenius discrepancy in ``H = U diag(E) U.T``.
    projector_idempotency
        Frobenius discrepancy in ``P @ P = P``.
    retained_coordinates
        Frobenius discrepancy from the exact retained diagonal spectrum.
    retained_embedding
        Frobenius discrepancy in the retained embedding identity.
    spectral_leakage
        Frobenius norm of retained-to-discarded spectral coupling.

    Raises
    ------
    TypeError
        A field has the wrong typed representation.
    ValueError
        A vector has the wrong grid shape, unit, or sign.

    Notes
    -----
    These observations measure finite algebra and floating-point behavior. They do not
    measure continuum discretization or parent-model error.
    """

    definition: Piab1dGridSweepDefinition
    discrete_spectrum: VectorQuantity
    spectral_reconstruction: VectorQuantity
    projector_idempotency: VectorQuantity
    retained_coordinates: VectorQuantity
    retained_embedding: VectorQuantity
    spectral_leakage: VectorQuantity

    def __post_init__(self) -> None:
        from .grid_sweep import Piab1dGridSweepDefinition

        if not isinstance(self.definition, Piab1dGridSweepDefinition):
            raise TypeError("definition must be Piab1dGridSweepDefinition")
        values = (
            self.discrete_spectrum,
            self.spectral_reconstruction,
            self.projector_idempotency,
            self.retained_coordinates,
            self.retained_embedding,
            self.spectral_leakage,
        )
        if any(not isinstance(value, VectorQuantity) for value in values):
            raise TypeError(
                "finite algebraic diagnostics must be VectorQuantity values"
            )
        shape = (len(self.definition.interior_points),)
        if any(value.magnitude.shape != shape for value in values):
            raise ValueError("finite algebraic diagnostics must cover every grid")
        if any(np.any(value.magnitude < 0.0) for value in values):
            raise ValueError("finite algebraic diagnostics must be nonnegative")
        energy_values = (
            self.discrete_spectrum,
            self.spectral_reconstruction,
            self.retained_coordinates,
            self.retained_embedding,
            self.spectral_leakage,
        )
        if any(not isinstance(value.unit, Unitless) for value in energy_values):
            raise ValueError(
                "energy-valued algebraic diagnostics must use the nondimensional unit"
            )
        if not isinstance(self.projector_idempotency.unit, Unitless):
            raise ValueError("projector idempotency discrepancy must be unitless")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "definition": self.definition,
            "discrete_spectrum": self.discrete_spectrum,
            "spectral_reconstruction": self.spectral_reconstruction,
            "projector_idempotency": self.projector_idempotency,
            "retained_coordinates": self.retained_coordinates,
            "retained_embedding": self.retained_embedding,
            "spectral_leakage": self.spectral_leakage,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        from .grid_sweep import Piab1dGridSweepDefinition

        required = {
            "definition",
            "discrete_spectrum",
            "spectral_reconstruction",
            "projector_idempotency",
            "retained_coordinates",
            "retained_embedding",
            "spectral_leakage",
        }
        if set(values) != required:
            raise ValueError("finite algebraic diagnostic fields do not match")
        definition_value = values["definition"]
        definition = (
            definition_value
            if isinstance(definition_value, Piab1dGridSweepDefinition)
            else Piab1dGridSweepDefinition.from_dict(definition_value)
            if isinstance(definition_value, Mapping)
            else None
        )
        if definition is None:
            raise TypeError("definition must be typed or decode to a mapping")
        names = tuple(required - {"definition"})
        if any(not isinstance(values[name], VectorQuantity) for name in names):
            raise TypeError("algebraic diagnostics must decode to vector quantities")
        return cls(
            definition=definition,
            discrete_spectrum=cast(VectorQuantity, values["discrete_spectrum"]),
            spectral_reconstruction=cast(
                VectorQuantity, values["spectral_reconstruction"]
            ),
            projector_idempotency=cast(VectorQuantity, values["projector_idempotency"]),
            retained_coordinates=cast(VectorQuantity, values["retained_coordinates"]),
            retained_embedding=cast(VectorQuantity, values["retained_embedding"]),
            spectral_leakage=cast(VectorQuantity, values["spectral_leakage"]),
        )
