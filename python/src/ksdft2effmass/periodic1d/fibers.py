"""Parent-qualified requests for one-dimensional represented Bloch fibers.

The shared request in this module binds a finite fiber construction to an exact
scientific parent model and to stable mathematical-operator and finite-state-space
identities.  Representation-specific modules own the plane-wave and coordinate-grid
numerics.  This separation prevents dimensions, spectra, paths, or descriptive names
from being used as substitutes for scientific identity.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.periodic import PeriodicOperatorReference

from .model import Periodic1DFourierHamiltonianToyModel


@dataclass(frozen=True, slots=True)
class Periodic1DFiberHamiltonianRequest:
    """Bind one finite Bloch-fiber request to its scientific parent identities.

    Parameters
    ----------
    representation_id
        Stable nonempty identity of the finite numerical representation used for
        this request.  It identifies neither the untruncated parent operator nor
        the finite state space by itself.
    parent_model
        Exact complete one-dimensional Fourier Hamiltonian parent model.
    represented_operator
        Stable reference carrying the parent-model, represented-operator, and
        finite-state-space identities.  Its model identity must equal
        ``parent_model.model_id`` and its state-space identity must differ from
        the untruncated parent state-space identity.
    reduced_momentum
        Dimensionless reduced reciprocal coordinate in the closed primitive
        interval ``[-0.5, 0.5]``.
    provenance_id
        Stable nonempty identity of the provenance record describing why and how
        this request was authored.

    Raises
    ------
    TypeError
        If an identity is not an exact built-in string, a component has the
        wrong exact domain type, or ``reduced_momentum`` is not an exact built-in
        float.  Booleans and numeric strings are rejected.
    ValueError
        If an identity is empty; momentum is nonfinite or outside the primitive
        interval; the operator is not one-dimensional; the parent-model
        identities disagree; or finite and untruncated state spaces are
        conflated.

    Notes
    -----
    The request supplies identity and correlation metadata only.  It performs no
    matrix construction, basis selection, discretization convergence study,
    scientific validation, or uncertainty quantification.  SHA-256 values, file
    names, matrix dimensions, and spectra are not accepted as identity proxies.
    """

    representation_id: str
    parent_model: Periodic1DFourierHamiltonianToyModel
    represented_operator: PeriodicOperatorReference
    reduced_momentum: float
    provenance_id: str

    def __post_init__(self) -> None:
        """Validate exact fields and the parent/operator/state-space binding."""
        self._check_args_identities_and_momentum()
        self._check_args_parent_binding()

    def _check_args_identities_and_momentum(self) -> None:
        """Require exact nonempty identities and finite primitive-zone momentum."""
        for name, value in (
            ("representation_id", self.representation_id),
            ("provenance_id", self.provenance_id),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if value == "":
                raise ValueError(f"{name} must be nonempty")
        if type(self.reduced_momentum) is not float:
            raise TypeError("reduced_momentum must be a built-in float")
        if not np.isfinite(self.reduced_momentum):
            raise ValueError("reduced_momentum must be finite")
        if not -0.5 <= self.reduced_momentum <= 0.5:
            raise ValueError("reduced_momentum must lie in [-0.5, 0.5]")

    def _check_args_parent_binding(self) -> None:
        """Require exact parent types and stable correlated scientific identities."""
        if type(self.parent_model) is not Periodic1DFourierHamiltonianToyModel:
            raise TypeError("parent_model must be Periodic1DFourierHamiltonianToyModel")
        if type(self.represented_operator) is not PeriodicOperatorReference:
            raise TypeError("represented_operator must be PeriodicOperatorReference")
        if self.represented_operator.model_id != self.parent_model.model_id:
            raise ValueError("represented operator must identify the parent model")
        if self.represented_operator.spatial_dimension != 1:
            raise ValueError("represented operator must be one-dimensional")
        if self.represented_operator.state_space_id == self.parent_model.state_space_id:
            raise ValueError(
                "finite and untruncated parent state spaces must remain distinct"
            )

    @property
    def model_id(self) -> str:
        """Return the exact stable parent-model identity."""
        return self.parent_model.model_id

    @property
    def operator_id(self) -> str:
        """Return the exact stable finite represented-operator identity."""
        return self.represented_operator.operator_id

    @property
    def state_space_id(self) -> str:
        """Return the exact stable finite represented-state-space identity."""
        return self.represented_operator.state_space_id


__all__ = ["Periodic1DFiberHamiltonianRequest"]
