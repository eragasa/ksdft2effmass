"""Typed reusable sections of represented model-analysis results."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import ClassVar, Self

import numpy as np
from projectkoios.physkit.units import (
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

type ResultSectionFieldType = (
    type[int]
    | type[float]
    | type[str]
    | type[ScalarQuantity]
    | type[VectorQuantity]
    | type[MatrixQuantity]
)


@dataclass(frozen=True, slots=True)
class BaseModelAnalysisResultSection(BaseTypedRecord):
    """Validate one closed mapping of typed model-analysis values.

    Parameters
    ----------
    values
        String-keyed mapping matching the concrete section's exact ``field_types``.

    Raises
    ------
    TypeError
        The root or a field has the wrong type.
    ValueError
        Field names differ from the closed concrete schema.
    """

    values: Mapping[str, SerializableValue]
    field_types: ClassVar[Mapping[str, ResultSectionFieldType]] = MappingProxyType({})

    def __post_init__(self) -> None:
        if not isinstance(self.values, Mapping):
            raise TypeError("section values must be a mapping")
        if set(self.values) != set(self.field_types):
            raise ValueError("section fields do not match the declared contract")
        copied: dict[str, SerializableValue] = {}
        for name, value in self.values.items():
            expected_type = self.field_types[name]
            if expected_type in (int, float, str):
                if type(value) is not expected_type:
                    raise TypeError(f"{name} must be {expected_type.__name__}")
            elif not isinstance(value, expected_type):
                raise TypeError(f"{name} must be {expected_type.__name__}")
            copied[name] = value
        object.__setattr__(self, "values", MappingProxyType(copied))

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return self.values

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        return cls(values=values)

    def matrix(self, name: str) -> MatrixQuantity:
        """Return one declared matrix quantity.

        Parameters
        ----------
        name
            Exact field name in the closed section schema.

        Returns
        -------
        MatrixQuantity
            Immutable represented matrix with its declared unit.

        Raises
        ------
        TypeError
            The name is absent or does not identify a matrix field.
        """
        value = self.values.get(name)
        if not isinstance(value, MatrixQuantity):
            raise TypeError(f"{name} is not a MatrixQuantity field")
        return value

    def vector(self, name: str) -> VectorQuantity:
        """Return one declared vector quantity.

        Parameters
        ----------
        name
            Exact field name in the closed section schema.

        Returns
        -------
        VectorQuantity
            Immutable represented vector with its declared unit.

        Raises
        ------
        TypeError
            The name is absent or does not identify a vector field.
        """
        value = self.values.get(name)
        if not isinstance(value, VectorQuantity):
            raise TypeError(f"{name} is not a VectorQuantity field")
        return value

    def real(self, name: str) -> float:
        """Return one declared built-in floating-point value.

        Parameters
        ----------
        name
            Exact field name in the closed section schema.

        Returns
        -------
        float
            Finite built-in floating-point field.

        Raises
        ------
        TypeError
            The name is absent or does not identify an exact built-in float.
        """
        value = self.values.get(name)
        if type(value) is not float:
            raise TypeError(f"{name} is not a built-in float field")
        return value

    def integer(self, name: str) -> int:
        """Return one declared built-in integer value.

        Parameters
        ----------
        name
            Exact field name in the closed section schema.

        Returns
        -------
        int
            Exact built-in integer field.

        Raises
        ------
        TypeError
            The name is absent or does not identify an exact built-in integer.
        """
        value = self.values.get(name)
        if type(value) is not int:
            raise TypeError(f"{name} is not a built-in integer field")
        return value

    def text(self, name: str) -> str:
        """Return one declared built-in string value.

        Parameters
        ----------
        name
            Exact field name in the closed section schema.

        Returns
        -------
        str
            Exact built-in string field.

        Raises
        ------
        TypeError
            The name is absent or does not identify an exact built-in string.
        """
        value = self.values.get(name)
        if type(value) is not str:
            raise TypeError(f"{name} is not a built-in string field")
        return value

    def scalar(self, name: str) -> ScalarQuantity:
        """Return one declared scalar quantity.

        Parameters
        ----------
        name
            Exact field name in the closed section schema.

        Returns
        -------
        ScalarQuantity
            Finite scalar magnitude with its declared unit.

        Raises
        ------
        TypeError
            The name is absent or does not identify a scalar-quantity field.
        """
        value = self.values.get(name)
        if not isinstance(value, ScalarQuantity):
            raise TypeError(f"{name} is not a ScalarQuantity field")
        return value


class HamiltonianResultSection(BaseModelAnalysisResultSection):
    """Retain parent, reduced, embedded, and boundary Hamiltonian matrices.

    Parameters
    ----------
    values
        Exact five-matrix mapping declared by ``field_types``.

    Raises
    ------
    ValueError
        Units differ or parent, embedded, and reduced shapes violate their spaces.
    """

    field_types = MappingProxyType(
        {
            "parent_hamiltonian": MatrixQuantity,
            "reduced_hamiltonian": MatrixQuantity,
            "embedded_reduced_hamiltonian": MatrixQuantity,
            "cyclic_reference": MatrixQuantity,
            "boundary_realization": MatrixQuantity,
        }
    )

    def __post_init__(self) -> None:
        super().__post_init__()
        matrices = tuple(self.matrix(name) for name in self.field_types)
        if len({matrix.unit for matrix in matrices}) != 1:
            raise ValueError("Hamiltonian matrix units must agree")
        parent = self.matrix("parent_hamiltonian").magnitude
        reduced = self.matrix("reduced_hamiltonian").magnitude
        embedded = self.matrix("embedded_reduced_hamiltonian").magnitude
        if parent.shape[0] != parent.shape[1] or embedded.shape != parent.shape:
            raise ValueError(
                "parent and embedded Hamiltonians must share a square space"
            )
        if reduced.shape[0] != reduced.shape[1] or reduced.shape[0] > parent.shape[0]:
            raise ValueError(
                "reduced Hamiltonian must be square in a retained subspace"
            )


class EigensystemResultSection(BaseModelAnalysisResultSection):
    """Retain represented spectra and Euclidean/quadrature eigenvectors.

    Parameters
    ----------
    values
        Exact three-spectrum and two-eigenvector mapping.

    Raises
    ------
    ValueError
        Spectrum units or shapes differ, or eigenvectors do not span the represented
        space under their declared normalization convention.
    """

    field_types = MappingProxyType(
        {
            "computed_discrete": VectorQuantity,
            "discrete_closed_form": VectorQuantity,
            "continuum_closed_form": VectorQuantity,
            "euclidean": MatrixQuantity,
            "quadrature_normalized": MatrixQuantity,
        }
    )

    def __post_init__(self) -> None:
        super().__post_init__()
        energies = tuple(
            self.vector(name)
            for name in (
                "computed_discrete",
                "discrete_closed_form",
                "continuum_closed_form",
            )
        )
        if len({energy.unit for energy in energies}) != 1:
            raise ValueError("eigensystem energy units must agree")
        if len({energy.magnitude.shape for energy in energies}) != 1:
            raise ValueError("eigensystem spectra must share one shape")
        euclidean = self.matrix("euclidean")
        if not isinstance(euclidean.unit, Unitless):
            raise ValueError("Euclidean eigenvectors must be unitless")
        dimension = energies[0].magnitude.size
        if euclidean.magnitude.shape != (dimension, dimension):
            raise ValueError("Euclidean eigenvectors must span the represented space")
        if self.matrix("quadrature_normalized").magnitude.shape != (
            dimension,
            dimension,
        ):
            raise ValueError("quadrature eigenvectors must span the represented space")


class SpectralReductionResultSection(BaseModelAnalysisResultSection):
    """Retain coordinate maps, orthogonal blocks, and reduction analyses.

    Parameters
    ----------
    values
        Exact mapping of rectangular coordinate maps, square blocks, and full-space
        residual analyses.

    Raises
    ------
    ValueError
        Map, projector, block, or analysis shapes do not identify consistent parent,
        retained, and discarded spaces.
    """

    field_types = MappingProxyType(
        {
            "reduction": MatrixQuantity,
            "embedding": MatrixQuantity,
            "projector": MatrixQuantity,
            "retained": MatrixQuantity,
            "retained_to_discarded": MatrixQuantity,
            "discarded_to_retained": MatrixQuantity,
            "discarded": MatrixQuantity,
            "consistent": MatrixQuantity,
            "unmatched": MatrixQuantity,
            "discarded_sector": MatrixQuantity,
        }
    )

    def __post_init__(self) -> None:
        super().__post_init__()
        reduction = self.matrix("reduction")
        embedding = self.matrix("embedding")
        projector = self.matrix("projector")
        if any(
            not isinstance(value.unit, Unitless)
            for value in (reduction, embedding, projector)
        ):
            raise ValueError("coordinate maps must be unitless")
        retained, parent = reduction.magnitude.shape
        if embedding.magnitude.shape != (parent, retained):
            raise ValueError("embedding and reduction dimensions are incompatible")
        if projector.magnitude.shape != (parent, parent):
            raise ValueError("projector must act on the represented parent space")
        energy_names = tuple(self.field_types)[3:]
        energies = tuple(self.matrix(name) for name in energy_names)
        if len({value.unit for value in energies}) != 1:
            raise ValueError("spectral-reduction energy units must agree")


class QuadratureResultSection(BaseModelAnalysisResultSection):
    """Retain one identified quadrature rule and its represented values.

    Parameters
    ----------
    values
        Exact rule identity, version, name, spacing, interior-weight, weighted-Gram,
        and weighted-projector mapping.

    Raises
    ------
    ValueError
        Dimensions or nondimensional length and projector conventions disagree.
    """

    field_types = MappingProxyType(
        {
            "rule_identifier": str,
            "rule_version": int,
            "rule": str,
            "spacing": ScalarQuantity,
            "interior_weights": VectorQuantity,
            "weighted_gram": MatrixQuantity,
            "weighted_projector": MatrixQuantity,
        }
    )

    def __post_init__(self) -> None:
        super().__post_init__()
        if not self.text("rule_identifier") or not self.text("rule"):
            raise ValueError("quadrature rule identity and name must be nonempty")
        if self.integer("rule_version") <= 0:
            raise ValueError("quadrature rule version must be positive")
        spacing = self.scalar("spacing")
        weights = self.vector("interior_weights")
        if spacing.unit != weights.unit:
            raise ValueError("quadrature spacing and weights must share a length unit")
        if spacing.magnitude <= 0.0 or np.any(weights.magnitude <= 0.0):
            raise ValueError("quadrature spacing and weights must be positive")
        dimension = weights.magnitude.size
        gram = self.matrix("weighted_gram")
        projector = self.matrix("weighted_projector")
        if not isinstance(gram.unit, Unitless) or not isinstance(
            projector.unit, Unitless
        ):
            raise ValueError("weighted Gram matrix and projector must be unitless")
        if gram.magnitude.shape[0] != gram.magnitude.shape[1]:
            raise ValueError("weighted Gram matrix must be square")
        if projector.magnitude.shape != (dimension, dimension):
            raise ValueError("weighted projector must act on the quadrature space")


class AnalyticalSamplingResultSection(BaseModelAnalysisResultSection):
    """Retain analytical sampling coordinates and wavefunctions.

    Parameters
    ----------
    values
        Exact coordinate vector and sampled wavefunction matrix mapping.

    Raises
    ------
    ValueError
        Coordinate samples do not index the wavefunction matrix rows.
    """

    field_types = MappingProxyType(
        {
            "coordinates": VectorQuantity,
            "wavefunctions": MatrixQuantity,
        }
    )

    def __post_init__(self) -> None:
        super().__post_init__()
        coordinates = self.vector("coordinates").magnitude
        wavefunctions = self.matrix("wavefunctions").magnitude
        if coordinates.size < 2 or not np.all(np.diff(coordinates) > 0.0):
            raise ValueError("analytical coordinates must be strictly increasing")
        if wavefunctions.shape[0] != coordinates.size:
            raise ValueError("analytical samples must align with coordinates")
