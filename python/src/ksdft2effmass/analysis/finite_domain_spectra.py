"""Host-edge and below-edge diagnostics for retained complex Hermitian eigenpairs."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

import numpy as np

from ksdft2effmass.operators import (
    ComplexHermitianEigenpairResidualResult,
    ComplexHermitianEigenpairResult,
    ScalarQuantity,
    VectorQuantity,
)


class BoundStateSelectionStatus(StrEnum):
    """Whether the retained lowest-eigenpair window completes below-edge counting."""

    COMPLETE_BELOW_EDGE = "complete_below_edge"
    INCOMPLETE_SELECTED_WINDOW = "incomplete_selected_window"


@dataclass(frozen=True, slots=True)
class HostEdgeReference:
    """Identify one host spectral edge in an explicit energy unit."""

    identifier: str
    energy: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate nonempty identity and exact scalar energy."""
        if type(self.identifier) is not str:
            raise TypeError("identifier must be a string")
        if not self.identifier:
            raise ValueError("identifier must be nonempty")
        if type(self.energy) is not ScalarQuantity:
            raise TypeError("energy must be ScalarQuantity")


@dataclass(frozen=True, slots=True)
class HostEdgeBoundStateResult:
    """Retain selected below-edge states and explicit counting completeness."""

    eigenpair_residuals: ComplexHermitianEigenpairResidualResult
    host_edge: HostEdgeReference
    threshold: ScalarQuantity
    selected_indices: tuple[int, ...]
    binding_energies: VectorQuantity
    selection_status: BoundStateSelectionStatus

    def __post_init__(self) -> None:
        """Validate units, threshold criterion, indices, energies, and completeness."""
        if (
            type(self.eigenpair_residuals)
            is not ComplexHermitianEigenpairResidualResult
        ):
            raise TypeError(
                "eigenpair_residuals must be ComplexHermitianEigenpairResidualResult"
            )
        if not self.eigenpair_residuals.passes:
            raise ValueError(
                "eigenpair residuals must pass before bound-state analysis"
            )
        if type(self.host_edge) is not HostEdgeReference:
            raise TypeError("host_edge must be HostEdgeReference")
        if type(self.threshold) is not ScalarQuantity:
            raise TypeError("threshold must be ScalarQuantity")
        if self.host_edge.energy.unit != self.eigenpairs.eigenvalues.unit:
            raise ValueError("host edge and eigenvalue units must agree")
        if self.threshold.unit != self.host_edge.energy.unit:
            raise ValueError("bound-state threshold and host-edge units must agree")
        if self.threshold.magnitude < 0.0:
            raise ValueError("bound-state threshold must be nonnegative")
        if type(self.selected_indices) is not tuple or any(
            type(index) is not int for index in self.selected_indices
        ):
            raise TypeError("selected_indices must be a tuple of built-in ints")
        cutoff = self.host_edge.energy.magnitude - self.threshold.magnitude
        expected_indices = tuple(
            int(index)
            for index in np.flatnonzero(self.eigenpairs.eigenvalues.magnitude < cutoff)
        )
        if self.selected_indices != expected_indices:
            raise ValueError("selected_indices must equal the below-edge prefix")
        if type(self.binding_energies) is not VectorQuantity:
            raise TypeError("binding_energies must be VectorQuantity")
        if self.binding_energies.unit != self.host_edge.energy.unit:
            raise ValueError("binding energy and host-edge units must agree")
        expected_binding = (
            self.host_edge.energy.magnitude
            - self.eigenpairs.eigenvalues.magnitude[
                np.asarray(self.selected_indices, dtype=np.int64)
            ]
        )
        if not np.array_equal(self.binding_energies.magnitude, expected_binding):
            raise ValueError("binding energies must be host-edge referenced")
        if type(self.selection_status) is not BoundStateSelectionStatus:
            raise TypeError("selection_status must be BoundStateSelectionStatus")
        complete = (
            self.eigenpairs.selected_count == self.eigenpairs.full_dimension
            or len(self.selected_indices) < self.eigenpairs.selected_count
        )
        expected_status = (
            BoundStateSelectionStatus.COMPLETE_BELOW_EDGE
            if complete
            else BoundStateSelectionStatus.INCOMPLETE_SELECTED_WINDOW
        )
        if self.selection_status is not expected_status:
            raise ValueError(
                "selection_status must agree with retained spectral coverage"
            )

    @property
    def eigenpairs(self) -> ComplexHermitianEigenpairResult:
        """Return the exact eigenpair record covered by algebraic residuals."""
        return self.eigenpair_residuals.eigenpairs

    @property
    def below_edge_state_count(self) -> int:
        """Return retained count, exact only when spectral coverage is complete."""
        return len(self.selected_indices)

    @property
    def count_is_complete(self) -> bool:
        """Return whether the retained window completes below-edge counting."""
        return self.selection_status is BoundStateSelectionStatus.COMPLETE_BELOW_EDGE

    @property
    def no_bound_state(self) -> bool:
        """Return a no-bound-state outcome only for a complete empty selection."""
        return self.count_is_complete and not self.selected_indices


class HostEdgeBoundStateAnalyzer:
    """Classify retained lowest eigenvalues relative to one explicit host edge."""

    __slots__ = ()

    def execute(
        self,
        eigenpair_residuals: ComplexHermitianEigenpairResidualResult,
        host_edge: HostEdgeReference,
        threshold: ScalarQuantity,
    ) -> HostEdgeBoundStateResult:
        """Return below-edge states and selected-window completeness."""
        if type(eigenpair_residuals) is not ComplexHermitianEigenpairResidualResult:
            raise TypeError(
                "eigenpair_residuals must be ComplexHermitianEigenpairResidualResult"
            )
        if not eigenpair_residuals.passes:
            raise ValueError(
                "eigenpair residuals must pass before bound-state analysis"
            )
        eigenpairs = eigenpair_residuals.eigenpairs
        if type(host_edge) is not HostEdgeReference:
            raise TypeError("host_edge must be HostEdgeReference")
        if type(threshold) is not ScalarQuantity:
            raise TypeError("threshold must be ScalarQuantity")
        if host_edge.energy.unit != eigenpairs.eigenvalues.unit:
            raise ValueError("host edge and eigenvalue units must agree")
        if threshold.unit != host_edge.energy.unit:
            raise ValueError("bound-state threshold and host-edge units must agree")
        if threshold.magnitude < 0.0:
            raise ValueError("bound-state threshold must be nonnegative")
        cutoff = host_edge.energy.magnitude - threshold.magnitude
        selected_indices = tuple(
            int(index)
            for index in np.flatnonzero(eigenpairs.eigenvalues.magnitude < cutoff)
        )
        binding = (
            host_edge.energy.magnitude
            - eigenpairs.eigenvalues.magnitude[
                np.asarray(selected_indices, dtype=np.int64)
            ]
        )
        complete = (
            eigenpairs.selected_count == eigenpairs.full_dimension
            or len(selected_indices) < eigenpairs.selected_count
        )
        status = (
            BoundStateSelectionStatus.COMPLETE_BELOW_EDGE
            if complete
            else BoundStateSelectionStatus.INCOMPLETE_SELECTED_WINDOW
        )
        return HostEdgeBoundStateResult(
            eigenpair_residuals,
            host_edge,
            threshold,
            selected_indices,
            VectorQuantity(binding, host_edge.energy.unit),
            status,
        )
