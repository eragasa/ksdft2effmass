"""Immutable records for periodic-1D blind alignment.

The records distinguish represented observations from the inference policy and its
structured outcome.  They contain no retained-artifact paths, hidden authored map,
planted perturbation, or post hoc acceptance decision.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
import numpy.typing as npt

from ksdft2effmass.periodic1d.campaign.extraction.matched.records import (
    RepresentedOperator,
)

type ComplexMatrix = npt.NDArray[np.complex128]
type BlindAlignmentStatus = Literal["aligned_full", "aligned_partial", "stopped"]


@dataclass(frozen=True, slots=True)
class BlindAlignmentInferencePolicy:
    r"""Store numerical policy for one blind-alignment inference.

    Parameters
    ----------
    anchor_rank_tolerance
        Exclusive singular-value threshold used to identify anchor and energy-anchor
        rank.  Built-in Python ``int`` and ``float`` values are accepted; the value is
        dimensionless and must be positive and finite.
    maximum_anchor_condition_number
        Inclusive upper bound on the active anchor condition number.  The value is
        dimensionless and must be at least one and finite.
    maximum_principal_angle_radians
        Inclusive upper bound on the largest retained-subspace principal angle, in
        radians.  It must lie in the closed interval from zero to :math:`\pi/2`.
    minimum_energy_anchor_rank
        Minimum identified exterior-sector rank.  Python ``int`` values of at least
        one are accepted; booleans are rejected.
    """

    anchor_rank_tolerance: float
    maximum_anchor_condition_number: float
    maximum_principal_angle_radians: float
    minimum_energy_anchor_rank: int

    def __post_init__(self) -> None:
        """Reject invalid scalar types, ranges, and nonfinite policy values."""
        reals = (
            self.anchor_rank_tolerance,
            self.maximum_anchor_condition_number,
            self.maximum_principal_angle_radians,
        )
        if any(
            isinstance(value, bool) or not isinstance(value, int | float)
            for value in reals
        ):
            raise TypeError("blind-alignment policy values must be real numbers")
        if (
            not np.isfinite(self.anchor_rank_tolerance)
            or self.anchor_rank_tolerance <= 0.0
        ):
            raise ValueError("anchor_rank_tolerance must be positive and finite")
        if (
            not np.isfinite(self.maximum_anchor_condition_number)
            or self.maximum_anchor_condition_number < 1.0
        ):
            raise ValueError(
                "maximum_anchor_condition_number must be finite and at least one"
            )
        if (
            not np.isfinite(self.maximum_principal_angle_radians)
            or not 0.0 <= self.maximum_principal_angle_radians <= np.pi / 2.0
        ):
            raise ValueError("maximum_principal_angle_radians must lie in [0, pi/2]")
        if type(self.minimum_energy_anchor_rank) is not int:
            raise TypeError("minimum_energy_anchor_rank must be an integer")
        if self.minimum_energy_anchor_rank < 1:
            raise ValueError("minimum_energy_anchor_rank must be positive")


@dataclass(frozen=True, slots=True)
class BlindAlignmentObservation:
    """Represent only information visible to blind alignment.

    Parameters
    ----------
    identifier
        Nonempty observation identifier.
    reference_operator
        Reference represented Hamiltonian.  Its matrix is expressed in reference
        coordinates and its energy reference identifies the target convention.
    candidate_operator
        Candidate represented Hamiltonian before coordinate and scalar-energy
        alignment.
    anchor_cross_covariance
        Complex matrix from candidate coordinates to reference coordinates, with
        shape ``(reference dimension, candidate dimension)``.
    retained_subspace_overlap
        Complex matrix whose singular values define retained-subspace principal
        angles.  It has the same rectangular shape as the anchor covariance.
    exterior_energy_anchor
        Complex square matrix on the reference space used only to estimate the scalar
        energy shift after coordinate alignment.
    allow_partial_alignment
        Whether rank-deficient identified-sector alignment is explicitly admissible.
        This must be a Python ``bool``.

    Notes
    -----
    The observation deliberately excludes the authored alignment map, scalar shift,
    planted defect, and post hoc oracle errors.  Array fields are copied into
    read-only ``complex128`` storage.  Numeric strings and Boolean arrays are not
    accepted.
    """

    identifier: str
    reference_operator: RepresentedOperator
    candidate_operator: RepresentedOperator
    anchor_cross_covariance: ComplexMatrix
    retained_subspace_overlap: ComplexMatrix
    exterior_energy_anchor: ComplexMatrix
    allow_partial_alignment: bool

    def __post_init__(self) -> None:
        """Validate metadata and retain read-only observation matrices."""
        if not isinstance(self.identifier, str):
            raise TypeError("identifier must be a string")
        if not self.identifier:
            raise ValueError("identifier must be nonempty")
        if not isinstance(self.reference_operator, RepresentedOperator):
            raise TypeError("reference_operator must be a RepresentedOperator")
        if not isinstance(self.candidate_operator, RepresentedOperator):
            raise TypeError("candidate_operator must be a RepresentedOperator")
        if type(self.allow_partial_alignment) is not bool:
            raise TypeError("allow_partial_alignment must be Boolean")
        for name in (
            "anchor_cross_covariance",
            "retained_subspace_overlap",
            "exterior_energy_anchor",
        ):
            source = getattr(self, name)
            if not isinstance(source, np.ndarray):
                raise TypeError(f"{name} must be a NumPy array")
            if not np.issubdtype(source.dtype, np.number) or np.issubdtype(
                source.dtype, np.bool_
            ):
                raise TypeError(f"{name} must contain numeric non-Boolean values")
            value = np.asarray(source, dtype=np.complex128)
            if value.ndim != 2:
                raise ValueError(f"{name} must be two-dimensional")
            if not np.all(np.isfinite(value)):
                raise ValueError(f"{name} must be finite")
            immutable = np.frombuffer(
                value.tobytes(order="C"), dtype=np.complex128
            ).reshape(value.shape)
            object.__setattr__(self, name, immutable)


@dataclass(frozen=True, slots=True)
class BlindAlignmentInferenceRequest:
    """Bind one observation to the explicit inference policy applied to it.

    Parameters
    ----------
    observation
        Observation containing only inference-visible represented data.
    policy
        Numerical rank, conditioning, principal-angle, and energy-anchor policy.
    """

    observation: BlindAlignmentObservation
    policy: BlindAlignmentInferencePolicy

    def __post_init__(self) -> None:
        """Require the exact public observation and policy record types."""
        if not isinstance(self.observation, BlindAlignmentObservation):
            raise TypeError("observation must be a BlindAlignmentObservation")
        if not isinstance(self.policy, BlindAlignmentInferencePolicy):
            raise TypeError("policy must be a BlindAlignmentInferencePolicy")


@dataclass(frozen=True, slots=True)
class BlindAlignmentInferenceResult:
    """Record a full, partial, or stopped blind-alignment outcome.

    Parameters
    ----------
    status
        ``"aligned_full"``, ``"aligned_partial"``, or ``"stopped"``.
    issue_codes
        Sorted unique structured stop codes.  Successful outcomes have no codes.
    alignment_map
        Inferred partial isometry from candidate to reference coordinates, or
        ``None`` after a stop.
    reference_projector
        Projector onto the identified reference sector, or ``None`` after a stop.
    extracted_operator
        Candidate-minus-reference operator after inferred coordinate and scalar
        energy alignment, compressed to the identified sector, or ``None`` after a
        stop.
    inferred_energy_shift
        Estimated candidate-minus-reference scalar energy shift, in the operators'
        common energy unit, or ``None`` after a stop.
    anchor_rank
        Numerical anchor rank under the request policy.
    anchor_condition_number
        Active anchor condition number when available.
    minimum_anchor_singular_value
        Smallest active dimensionless anchor singular value when available.
    maximum_principal_angle_radians
        Largest inferred retained-subspace principal angle when available.
    energy_anchor_rank
        Numerical exterior energy-anchor rank when evaluated.

    Notes
    -----
    A successful result is numerical evidence about the declared finite matrices.  It
    does not establish physical equivalence, material validity, or a unique extension
    outside a partially identified sector.
    """

    status: BlindAlignmentStatus
    issue_codes: tuple[str, ...]
    alignment_map: ComplexMatrix | None
    reference_projector: ComplexMatrix | None
    extracted_operator: ComplexMatrix | None
    inferred_energy_shift: float | None
    anchor_rank: int
    anchor_condition_number: float | None
    minimum_anchor_singular_value: float | None
    maximum_principal_angle_radians: float | None
    energy_anchor_rank: int | None

    def __post_init__(self) -> None:
        """Enforce status coherence and immutable finite represented outputs."""
        if self.status not in ("aligned_full", "aligned_partial", "stopped"):
            raise ValueError("unsupported blind-alignment status")
        if type(self.anchor_rank) is not int:
            raise TypeError("anchor_rank must be an integer")
        if self.anchor_rank < 0:
            raise ValueError("anchor_rank must be nonnegative")
        if type(self.issue_codes) is not tuple or any(
            type(value) is not str or not value for value in self.issue_codes
        ):
            raise TypeError("issue_codes must contain nonempty strings")
        if self.issue_codes != tuple(sorted(set(self.issue_codes))):
            raise ValueError("issue_codes must be sorted and unique")
        stopped = self.status == "stopped"
        arrays = (
            self.alignment_map,
            self.reference_projector,
            self.extracted_operator,
        )
        if stopped != bool(self.issue_codes):
            raise ValueError("stopped status must agree with issue_codes")
        if stopped and any(value is not None for value in arrays):
            raise ValueError("stopped inference must not return represented outputs")
        if not stopped and any(value is None for value in arrays):
            raise ValueError("successful inference must return represented outputs")
        if stopped and self.inferred_energy_shift is not None:
            raise ValueError("stopped inference must not return an energy shift")
        if not stopped and self.inferred_energy_shift is None:
            raise ValueError("successful inference must return an energy shift")
        optional_reals = (
            self.anchor_condition_number,
            self.minimum_anchor_singular_value,
            self.maximum_principal_angle_radians,
            self.inferred_energy_shift,
        )
        if any(
            value is not None
            and (isinstance(value, bool) or not isinstance(value, int | float))
            for value in optional_reals
        ):
            raise TypeError("blind-alignment scalar diagnostics must be real numbers")
        if any(
            value is not None and not np.isfinite(value) for value in optional_reals
        ):
            raise ValueError("blind-alignment scalar diagnostics must be finite")
        if self.energy_anchor_rank is not None:
            if type(self.energy_anchor_rank) is not int:
                raise TypeError("energy_anchor_rank must be an integer")
            if self.energy_anchor_rank < 0:
                raise ValueError("energy_anchor_rank must be nonnegative")
        for name in ("alignment_map", "reference_projector", "extracted_operator"):
            source = getattr(self, name)
            if source is None:
                continue
            if not isinstance(source, np.ndarray):
                raise TypeError(f"{name} must be a NumPy array")
            if not np.issubdtype(source.dtype, np.number) or np.issubdtype(
                source.dtype, np.bool_
            ):
                raise TypeError(f"{name} must contain numeric non-Boolean values")
            value = np.asarray(source, dtype=np.complex128)
            if value.ndim != 2 or not np.all(np.isfinite(value)):
                raise ValueError(f"{name} must be a finite matrix")
            immutable = np.frombuffer(
                value.tobytes(order="C"), dtype=np.complex128
            ).reshape(value.shape)
            object.__setattr__(self, name, immutable)
