"""Observation-only inference for periodic-1D blind alignment."""

from __future__ import annotations

from typing import Literal

import numpy as np

from .records import (
    BlindAlignmentInferenceRequest,
    BlindAlignmentInferenceResult,
    ComplexMatrix,
)


class BlindAlignmentInferenceActionizer:
    """Infer a candidate-to-reference partial isometry and scalar energy shift.

    The Actionizer receives only the observation and numerical policy carried by a
    :class:`BlindAlignmentInferenceRequest`.  It does not receive or discover an
    authored alignment map, scalar shift, planted perturbation, retained result, or
    post hoc oracle error.

    Full-rank execution requires equal represented dimensions.  Explicit rectangular
    reconciliation is available through :meth:`execute_reconciled_partial` only when
    the request declares partial alignment and the candidate is lower-dimensional.
    Both routes use an SVD polar factor of the authored anchor cross-covariance.
    """

    __slots__ = ()

    def execute(
        self, request: BlindAlignmentInferenceRequest
    ) -> BlindAlignmentInferenceResult:
        """Infer a full or identified-sector square alignment.

        Parameters
        ----------
        request
            Immutable observation and inference policy.

        Returns
        -------
        BlindAlignmentInferenceResult
            Successful represented outputs or one structured stopping code.

        Raises
        ------
        TypeError
            If ``request`` is not a :class:`BlindAlignmentInferenceRequest`.
        ValueError
            If matrix shapes or comparison-critical units, geometry, or reduced
            momentum are internally inconsistent.
        """
        if not isinstance(request, BlindAlignmentInferenceRequest):
            raise TypeError("request must be a BlindAlignmentInferenceRequest")
        observation = request.observation
        policy = request.policy
        reference_dimension, candidate_dimension = self._validate_observation(request)
        if reference_dimension != candidate_dimension:
            return self._stopped("BLIND_ALIGNMENT.RANK_MISMATCH")
        if (
            observation.reference_operator.basis.spin_count
            != observation.candidate_operator.basis.spin_count
        ):
            return self._stopped("BLIND_ALIGNMENT.SPIN_MISMATCH")
        maximum_angle = self._maximum_principal_angle(
            observation.retained_subspace_overlap
        )
        if maximum_angle > policy.maximum_principal_angle_radians:
            return self._stopped(
                "BLIND_ALIGNMENT.SUBSPACE_ANGLE_EXCEEDED",
                maximum_principal_angle=maximum_angle,
            )
        left, singular, right_adjoint = np.linalg.svd(
            observation.anchor_cross_covariance, full_matrices=False
        )
        active = singular > policy.anchor_rank_tolerance
        rank = int(np.sum(active))
        if rank == 0:
            return self._stopped(
                "BLIND_ALIGNMENT.ANCHOR_RANK_ZERO",
                maximum_principal_angle=maximum_angle,
            )
        minimum_active = float(np.min(singular[active]))
        condition = float(np.max(singular[active]) / minimum_active)
        if condition > policy.maximum_anchor_condition_number:
            return self._stopped(
                "BLIND_ALIGNMENT.ANCHOR_ILL_CONDITIONED",
                rank=rank,
                condition=condition,
                minimum_singular=minimum_active,
                maximum_principal_angle=maximum_angle,
            )
        if rank < reference_dimension and not observation.allow_partial_alignment:
            return self._stopped(
                "BLIND_ALIGNMENT.ANCHOR_RANK_DEFICIENT",
                rank=rank,
                condition=condition,
                minimum_singular=minimum_active,
                maximum_principal_angle=maximum_angle,
            )
        alignment = left[:, active] @ right_adjoint[active, :]
        return self._extract(
            request,
            alignment,
            rank,
            condition,
            minimum_active,
            maximum_angle,
            "aligned_full" if rank == reference_dimension else "aligned_partial",
        )

    def execute_reconciled_partial(
        self, request: BlindAlignmentInferenceRequest
    ) -> BlindAlignmentInferenceResult:
        """Infer a declared rectangular partial isometry.

        Parameters
        ----------
        request
            Observation with a larger reference space than candidate space and
            ``allow_partial_alignment=True``.

        Returns
        -------
        BlindAlignmentInferenceResult
            An identified-sector result or one structured stopping code.

        Raises
        ------
        TypeError
            If ``request`` has the wrong type.
        ValueError
            If the observation is not an explicitly declared rectangular
            reconciliation or its comparison-critical metadata is inconsistent.
        """
        if not isinstance(request, BlindAlignmentInferenceRequest):
            raise TypeError("request must be a BlindAlignmentInferenceRequest")
        observation = request.observation
        policy = request.policy
        reference_dimension, candidate_dimension = self._validate_observation(request)
        if (
            reference_dimension <= candidate_dimension
            or not observation.allow_partial_alignment
        ):
            raise ValueError("rectangular reconciliation contract is invalid")
        if (
            observation.reference_operator.basis.spin_count
            != observation.candidate_operator.basis.spin_count
        ):
            return self._stopped("BLIND_ALIGNMENT.SPIN_MISMATCH")
        maximum_angle = self._maximum_principal_angle(
            observation.retained_subspace_overlap
        )
        if maximum_angle > policy.maximum_principal_angle_radians:
            return self._stopped(
                "BLIND_ALIGNMENT.SUBSPACE_ANGLE_EXCEEDED",
                maximum_principal_angle=maximum_angle,
            )
        left, singular, right_adjoint = np.linalg.svd(
            observation.anchor_cross_covariance, full_matrices=False
        )
        active = singular > policy.anchor_rank_tolerance
        rank = int(np.sum(active))
        if rank != candidate_dimension:
            return self._stopped(
                "BLIND_ALIGNMENT.ANCHOR_RANK_DEFICIENT",
                rank=rank,
                maximum_principal_angle=maximum_angle,
            )
        minimum_active = float(np.min(singular[active]))
        condition = float(np.max(singular[active]) / minimum_active)
        if condition > policy.maximum_anchor_condition_number:
            return self._stopped(
                "BLIND_ALIGNMENT.ANCHOR_ILL_CONDITIONED",
                rank=rank,
                condition=condition,
                minimum_singular=minimum_active,
                maximum_principal_angle=maximum_angle,
            )
        alignment = left[:, active] @ right_adjoint[active, :]
        return self._extract(
            request,
            alignment,
            rank,
            condition,
            minimum_active,
            maximum_angle,
            "aligned_partial",
        )

    @staticmethod
    def _validate_observation(
        request: BlindAlignmentInferenceRequest,
    ) -> tuple[int, int]:
        """Validate represented dimensions and comparison-critical metadata."""
        observation = request.observation
        reference = observation.reference_operator
        candidate = observation.candidate_operator
        reference_dimension = reference.basis.dimension
        candidate_dimension = candidate.basis.dimension
        if reference.matrix.shape != (reference_dimension, reference_dimension):
            raise ValueError("reference operator dimension is inconsistent")
        if candidate.matrix.shape != (candidate_dimension, candidate_dimension):
            raise ValueError("candidate operator dimension is inconsistent")
        rectangular_shape = (reference_dimension, candidate_dimension)
        if observation.anchor_cross_covariance.shape != rectangular_shape:
            raise ValueError("anchor cross-covariance shape is inconsistent")
        if observation.retained_subspace_overlap.shape != rectangular_shape:
            raise ValueError("retained-subspace overlap shape is inconsistent")
        if observation.exterior_energy_anchor.shape != (
            reference_dimension,
            reference_dimension,
        ):
            raise ValueError("exterior energy-anchor shape is inconsistent")
        reference_basis = reference.basis
        candidate_basis = candidate.basis
        if reference_basis.energy_unit != candidate_basis.energy_unit:
            raise ValueError("blind alignment requires a common energy unit")
        if reference_basis.geometry_id != candidate_basis.geometry_id:
            raise ValueError("blind alignment requires a common geometry")
        if reference_basis.subspace_id != candidate_basis.subspace_id:
            raise ValueError("blind alignment requires a declared common subspace")
        if not np.isclose(
            reference_basis.reduced_momentum,
            candidate_basis.reduced_momentum,
            rtol=0.0,
            atol=0.0,
        ):
            raise ValueError("blind alignment requires equal reduced momentum")
        return reference_dimension, candidate_dimension

    @staticmethod
    def _maximum_principal_angle(overlap: ComplexMatrix) -> float:
        """Return the largest principal angle encoded by overlap singular values."""
        singular = np.linalg.svd(overlap, compute_uv=False)
        if singular.size == 0:
            raise ValueError("retained-subspace overlap must have nonzero dimension")
        minimum = float(np.min(np.clip(singular, 0.0, 1.0)))
        return float(np.arccos(minimum))

    def _extract(
        self,
        request: BlindAlignmentInferenceRequest,
        alignment: ComplexMatrix,
        rank: int,
        condition: float,
        minimum_singular: float,
        maximum_principal_angle: float,
        status: Literal["aligned_full", "aligned_partial"],
    ) -> BlindAlignmentInferenceResult:
        """Estimate the scalar shift and extract the identified-sector operator."""
        observation = request.observation
        policy = request.policy
        projector = alignment @ alignment.conj().T
        energy_anchor = projector @ observation.exterior_energy_anchor @ projector
        energy_rank = int(
            np.sum(
                np.linalg.svd(energy_anchor, compute_uv=False)
                > policy.anchor_rank_tolerance
            )
        )
        if energy_rank < policy.minimum_energy_anchor_rank:
            return self._stopped(
                "BLIND_ALIGNMENT.ENERGY_ANCHOR_INSUFFICIENT",
                rank=rank,
                condition=condition,
                minimum_singular=minimum_singular,
                maximum_principal_angle=maximum_principal_angle,
                energy_rank=energy_rank,
            )
        energy_weight = float(np.trace(energy_anchor).real)
        if (
            not np.isfinite(energy_weight)
            or abs(energy_weight) <= policy.anchor_rank_tolerance
        ):
            return self._stopped(
                "BLIND_ALIGNMENT.ENERGY_ANCHOR_ZERO_WEIGHT",
                rank=rank,
                condition=condition,
                minimum_singular=minimum_singular,
                maximum_principal_angle=maximum_principal_angle,
                energy_rank=energy_rank,
            )
        aligned_candidate = (
            alignment @ observation.candidate_operator.matrix @ alignment.conj().T
        )
        reference_compressed = (
            projector @ observation.reference_operator.matrix @ projector
        )
        shift = float(
            np.trace(
                energy_anchor
                @ (aligned_candidate - reference_compressed)
                @ energy_anchor
            ).real
            / energy_weight
        )
        extracted = aligned_candidate - shift * projector - reference_compressed
        return BlindAlignmentInferenceResult(
            status=status,
            issue_codes=(),
            alignment_map=alignment,
            reference_projector=projector,
            extracted_operator=extracted,
            inferred_energy_shift=shift,
            anchor_rank=rank,
            anchor_condition_number=condition,
            minimum_anchor_singular_value=minimum_singular,
            maximum_principal_angle_radians=maximum_principal_angle,
            energy_anchor_rank=energy_rank,
        )

    @staticmethod
    def _stopped(
        issue: str,
        *,
        rank: int = 0,
        condition: float | None = None,
        minimum_singular: float | None = None,
        maximum_principal_angle: float | None = None,
        energy_rank: int | None = None,
    ) -> BlindAlignmentInferenceResult:
        """Construct one coherent structured stop without represented outputs."""
        return BlindAlignmentInferenceResult(
            status="stopped",
            issue_codes=(issue,),
            alignment_map=None,
            reference_projector=None,
            extracted_operator=None,
            inferred_energy_shift=None,
            anchor_rank=rank,
            anchor_condition_number=condition,
            minimum_anchor_singular_value=minimum_singular,
            maximum_principal_angle_radians=maximum_principal_angle,
            energy_anchor_rank=energy_rank,
        )
