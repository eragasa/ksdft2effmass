"""Fourier-series projection into a PhysKit block-hopping representation."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from projectkoios.numerics.finite_periodic.numpy.matrix_series import (
    NumpyFiniteFourierMatrixSeries,
)
from projectkoios.physkit.periodic.lattice.finite_domain import (
    LatticeDimension,
    LatticeDisplacement,
)
from projectkoios.physkit.periodic.lattice.hopping import (
    DenseBlockHoppingModel,
    DenseBlockHoppingTerm,
)
from projectkoios.physkit.units import ComplexMatrixQuantity, Unitless


@dataclass(frozen=True, slots=True)
class FourierSeriesBlockHoppingRepresentationRequest:
    """Bind one Fourier series to explicit provider-representation identities.

    Parameters
    ----------
    identifier
        Nonempty identity for the resulting provider representation.
    energy_reference
        Nonempty identity for the represented common energy zero.
    basis_identifier
        Nonempty identity for the ordered retained primitive-cell basis.
    series
        Exact finite Fourier matrix series in two or three periodic dimensions.

    """

    identifier: str
    energy_reference: str
    basis_identifier: str
    series: NumpyFiniteFourierMatrixSeries

    def __post_init__(self) -> None:
        """Validate exact identities and Fourier-series ownership.

        Raises
        ------
        TypeError
            If an identity is not a built-in string or ``series`` lacks its exact
            numerical owner.
        ValueError
            If an identity is empty or the series dimension is not two or three.

        """
        # Exact nominal checks prevent strings, arrays, or compatible-looking
        # third-party values from becoming representation identities implicitly.
        for value, name in (
            (self.identifier, "identifier"),
            (self.energy_reference, "energy_reference"),
            (self.basis_identifier, "basis_identifier"),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in string")
            if not value:
                raise ValueError(f"{name} must be nonempty")
        if type(self.series) is not NumpyFiniteFourierMatrixSeries:
            raise TypeError("series must be NumpyFiniteFourierMatrixSeries")
        if self.series.dimension not in (2, 3):
            raise ValueError("series dimension must be two or three")


class FourierSeriesBlockHoppingRepresentation:
    """Construct one immutable ordinary-lattice provider representation.

    The operation changes representation only. It does not assign KSD scientific-model
    identity, infer physical geometry, select support, or analyze locality.
    """

    __slots__ = ("_request",)

    def __init__(
        self,
        *,
        request: FourierSeriesBlockHoppingRepresentationRequest,
    ) -> None:
        """Bind one exact immutable representation request.

        Parameters
        ----------
        request
            Exact representation request owned by this operation.

        Raises
        ------
        TypeError
            If ``request`` lacks its exact nominal owner.

        """
        if type(request) is not FourierSeriesBlockHoppingRepresentationRequest:
            raise TypeError(
                "request must be FourierSeriesBlockHoppingRepresentationRequest"
            )
        self._request = request

    @property
    def request(self) -> FourierSeriesBlockHoppingRepresentationRequest:
        """Return the exact immutable request bound to this operation.

        Returns
        -------
        FourierSeriesBlockHoppingRepresentationRequest
            Request retained by identity for the lifetime of the operation.

        """
        return self._request

    def result(self) -> DenseBlockHoppingModel:
        """Return the sorted unitless PhysKit block-hopping representation.

        Returns
        -------
        DenseBlockHoppingModel
            Immutable ordinary-lattice representation whose displacement order is
            lexicographic and whose blocks preserve the Fourier coefficients exactly.

        """
        series = self._request.series
        # Close the numerical library's integer dimension onto PhysKit's exact
        # ordinary-lattice enum before constructing any displacement values.
        dimension = (
            LatticeDimension.TWO
            if series.dimension == 2
            else LatticeDimension.THREE
        )
        entries: list[tuple[LatticeDisplacement, ComplexMatrixQuantity]] = []
        for mode, coefficient in zip(
            series.integer_modes,
            series.matrix_coefficients,
            strict=True,
        ):
            if dimension is LatticeDimension.TWO:
                displacement = LatticeDisplacement(
                    dimension,
                    (int(mode[0]), int(mode[1])),
                )
            else:
                displacement = LatticeDisplacement(
                    dimension,
                    (int(mode[0]), int(mode[1]), int(mode[2])),
                )
            entries.append(
                (
                    displacement,
                    # Copy each coefficient so the provider value cannot retain a
                    # writable view into the numerical Fourier-series storage.
                    ComplexMatrixQuantity(
                        np.array(coefficient, dtype=np.complex128, copy=True),
                        Unitless(),
                    ),
                )
            )
        # Provider term order is made deterministic independently of the transform's
        # mode enumeration; callers correlate shells through displacement identity.
        entries.sort(key=lambda entry: entry[0].components)
        return DenseBlockHoppingModel(
            identifier=self._request.identifier,
            dimension=dimension,
            terms=tuple(
                DenseBlockHoppingTerm(
                    displacement=displacement,
                    coefficient=coefficient,
                )
                for displacement, coefficient in entries
            ),
            energy_unit=Unitless(),
            energy_reference=self._request.energy_reference,
            basis_identifier=self._request.basis_identifier,
        )


__all__ = [
    "FourierSeriesBlockHoppingRepresentation",
    "FourierSeriesBlockHoppingRepresentationRequest",
]
