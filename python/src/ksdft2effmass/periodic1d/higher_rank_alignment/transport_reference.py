"""Producer-independent transport reference for the constant analytic frame.

The protocol's analytic retained frame and endpoint sewing map are constant identities.
This bounded reference therefore reconstructs the exact closed route directly, without
invoking the PhysKit transporter or producer analysis actions.  It is evidence for the
constant-frame transport control, not complete protocol verification.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import final

import numpy as np
from projectkoios.physkit.numerics.typing.numpy.arrays import RealArray
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.verification import MaximumAbsoluteErrorComparison

from .calculation_result import Periodic1DRankNAlignmentCalculationResult
from .result import Periodic1DRankNAlignmentTransportOwnerResult

_REFERENCE_SCALAR_ABSOLUTE_TOLERANCE = 1.0e-11
_REFERENCE_ARRAY_ABSOLUTE_TOLERANCE = 1.0e-10


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRankNTransportReferenceRequest:
    """Bind one exact producer result to the bounded transport reference action."""

    calculation_result: Periodic1DRankNAlignmentCalculationResult

    def __post_init__(self) -> None:
        if (
            type(self.calculation_result)
            is not Periodic1DRankNAlignmentCalculationResult
        ):
            raise TypeError("calculation_result must be the exact calculation result")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRankNTransportReference:
    """Store immutable constant-frame closed-route comparisons."""

    comparisons: Mapping[str, MaximumAbsoluteErrorComparison]

    def __post_init__(self) -> None:
        if not isinstance(self.comparisons, Mapping) or not self.comparisons:
            raise TypeError("comparisons must be a nonempty mapping")
        if any(
            type(key) is not str
            or not key
            or type(value) is not MaximumAbsoluteErrorComparison
            for key, value in self.comparisons.items()
        ):
            raise TypeError("comparison inventory contains an invalid entry")
        object.__setattr__(
            self,
            "comparisons",
            MappingProxyType(dict(self.comparisons)),
        )


@final
class Periodic1DRankNTransportReferenceAnalyzer:
    """Reconstruct constant-frame transport without the producer transporter."""

    __slots__ = ("_request",)

    def __init__(self, request: Periodic1DRankNTransportReferenceRequest) -> None:
        if type(request) is not Periodic1DRankNTransportReferenceRequest:
            raise TypeError("request must be the exact transport reference request")
        self._request = request

    @property
    def request(self) -> Periodic1DRankNTransportReferenceRequest:
        """Return the exact immutable request bound to this action."""
        return self._request

    def execute(self) -> Periodic1DRankNTransportReference:
        """Return direct constant-frame transport comparisons on all meshes."""
        calculation = self._request.calculation_result
        configuration = calculation.request.configuration
        rank = calculation.request.retained_rank
        identity = np.eye(rank, dtype=np.complex128)
        comparisons: dict[str, MaximumAbsoluteErrorComparison] = {}

        cutoff = max(
            configuration.rank_absolute_tolerance,
            configuration.rank_relative_tolerance,
        )
        for mesh in calculation.meshes:
            size = mesh.construction_mesh_size
            transport = mesh.transport
            if type(transport) is not Periodic1DRankNAlignmentTransportOwnerResult:
                raise ValueError(
                    "bounded transport reference requires a completed transport result"
                )
            prefix = f"mesh[{size}].transport"
            singular_values, cutoffs, margins, ranks, unitary_defects = _link_arrays(
                transport
            )
            for name, reference_array, observed_array in (
                (
                    "link_singular_values",
                    MatrixQuantity(np.ones((size, rank), dtype=np.float64), Unitless()),
                    MatrixQuantity(singular_values, Unitless()),
                ),
                (
                    "link_rank_cutoffs",
                    VectorQuantity(np.full(size, cutoff, dtype=np.float64), Unitless()),
                    VectorQuantity(cutoffs, Unitless()),
                ),
                (
                    "link_rank_margins",
                    VectorQuantity(
                        np.full(size, 1.0 - cutoff, dtype=np.float64), Unitless()
                    ),
                    VectorQuantity(margins, Unitless()),
                ),
                (
                    "link_numerical_ranks",
                    VectorQuantity(np.full(size, rank, dtype=np.float64), Unitless()),
                    VectorQuantity(ranks, Unitless()),
                ),
                (
                    "link_unitarity_defects",
                    VectorQuantity(np.zeros(size, dtype=np.float64), Unitless()),
                    VectorQuantity(unitary_defects, Unitless()),
                ),
            ):
                comparisons[f"{prefix}.{name}"] = _comparison(
                    observed_array,
                    reference_array,
                    _REFERENCE_ARRAY_ABSOLUTE_TOLERANCE,
                )

            phases = transport.ordered_closure_endpoint_mismatch_phases
            primitive_to_sewn = transport.primitive_last_to_sewn_first_right_unitary
            sewn_to_primitive = transport.sewn_first_to_primitive_last_right_unitary
            correction_step = (
                transport.distributed_closure_correction_right_unitary_step
            )
            if (
                phases is None
                or primitive_to_sewn is None
                or sewn_to_primitive is None
                or correction_step is None
            ):
                raise ValueError(
                    "bounded transport reference requires complete closure evidence"
                )
            comparisons[f"{prefix}.closure_phases"] = _comparison(
                VectorQuantity(np.asarray(phases, dtype=np.float64), Unitless()),
                VectorQuantity(np.zeros(rank, dtype=np.float64), Unitless()),
                _REFERENCE_ARRAY_ABSOLUTE_TOLERANCE,
            )
            for name, observed_matrix in (
                ("primitive_last_to_sewn_first", primitive_to_sewn),
                ("sewn_first_to_primitive_last", sewn_to_primitive),
                ("distributed_correction_step", correction_step),
            ):
                comparisons[f"{prefix}.{name}"] = _comparison(
                    observed_matrix,
                    ComplexMatrixQuantity(identity, Unitless()),
                    _REFERENCE_ARRAY_ABSOLUTE_TOLERANCE,
                )

            closure_residual = (
                transport.maximum_absolute_entry_closure_alignment_residual
            )
            closure_unitarity = (
                transport.maximum_absolute_entry_closure_alignment_unitarity_defect
            )
            if (
                closure_residual is None
                or closure_unitarity is None
                or mesh.endpoint_closure_defect is None
                or mesh.primitive_closure_defect is None
            ):
                raise ValueError(
                    "bounded transport reference requires complete closure diagnostics"
                )
            for name, observed_scalar in (
                ("closure_alignment_residual", closure_residual),
                ("closure_alignment_unitarity_defect", closure_unitarity),
                ("endpoint_closure_defect", mesh.endpoint_closure_defect),
                ("primitive_closure_defect", mesh.primitive_closure_defect),
                (
                    "deficient_link_count",
                    float(len(transport.deficient_link_indices)),
                ),
                (
                    "unattempted_link_count",
                    float(len(transport.unattempted_link_indices)),
                ),
            ):
                comparisons[f"{prefix}.{name}"] = _comparison(
                    ScalarQuantity(observed_scalar, Unitless()),
                    ScalarQuantity(0.0, Unitless()),
                    _REFERENCE_SCALAR_ABSOLUTE_TOLERANCE,
                )

        return Periodic1DRankNTransportReference(comparisons=comparisons)


def _link_arrays(
    transport: Periodic1DRankNAlignmentTransportOwnerResult,
) -> tuple[RealArray, RealArray, RealArray, RealArray, RealArray]:
    singular_values: list[tuple[float, ...]] = []
    cutoffs: list[float] = []
    margins: list[float] = []
    ranks: list[float] = []
    unitary_defects: list[float] = []
    for link in transport.link_results:
        if (
            link.singular_values is None
            or link.applied_rank_cutoff is None
            or link.rank_margin is None
            or link.numerical_rank is None
            or link.maximum_absolute_entry_unitarity_defect is None
        ):
            raise ValueError(
                "bounded transport reference requires qualified link diagnostics"
            )
        singular_values.append(link.singular_values)
        cutoffs.append(link.applied_rank_cutoff)
        margins.append(link.rank_margin)
        ranks.append(float(link.numerical_rank))
        unitary_defects.append(link.maximum_absolute_entry_unitarity_defect)
    return (
        np.asarray(singular_values, dtype=np.float64),
        np.asarray(cutoffs, dtype=np.float64),
        np.asarray(margins, dtype=np.float64),
        np.asarray(ranks, dtype=np.float64),
        np.asarray(unitary_defects, dtype=np.float64),
    )


def _comparison(
    observed: (
        ScalarQuantity | VectorQuantity | MatrixQuantity | ComplexMatrixQuantity
    ),
    reference: ScalarQuantity | VectorQuantity | MatrixQuantity | ComplexMatrixQuantity,
    tolerance: float,
) -> MaximumAbsoluteErrorComparison:
    return MaximumAbsoluteErrorComparison(
        observed=observed,
        reference=reference,
        tolerance=ScalarQuantity(tolerance, observed.unit),
    )


__all__ = [
    "Periodic1DRankNTransportReference",
    "Periodic1DRankNTransportReferenceAnalyzer",
    "Periodic1DRankNTransportReferenceRequest",
]
