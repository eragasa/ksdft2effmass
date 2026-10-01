"""Post hoc synthetic-oracle evaluation for periodic-1D blind alignment."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

import numpy as np

from .construction import BlindAlignmentHiddenTruth
from .records import BlindAlignmentInferenceResult, ComplexMatrix


@dataclass(frozen=True, slots=True)
class BlindAlignmentEvaluationRequest:
    """Request post hoc evaluation of one successful inference.

    Parameters
    ----------
    identifier
        Nonempty campaign case identifier.
    inference
        Successful full or partial inference result.
    hidden_truth
        Construction-only authored map, perturbation, and scalar shift.
    cell_count
        Positive primitive-cell count used to define onsite model blocks.
    eigenvalue_degeneracy_tolerance
        Positive finite absolute tolerance in ``E_G`` for identifying the lowest
        active eigenspace.
    """

    identifier: str
    inference: BlindAlignmentInferenceResult
    hidden_truth: BlindAlignmentHiddenTruth
    cell_count: int
    eigenvalue_degeneracy_tolerance: float

    def __post_init__(self) -> None:
        """Validate exact record types and positive finite evaluation controls."""
        if type(self.identifier) is not str or not self.identifier:
            raise ValueError("identifier must be nonempty")
        if not isinstance(self.inference, BlindAlignmentInferenceResult):
            raise TypeError("inference must be BlindAlignmentInferenceResult")
        if self.inference.status == "stopped":
            raise ValueError("post hoc evaluation requires successful inference")
        if not isinstance(self.hidden_truth, BlindAlignmentHiddenTruth):
            raise TypeError("hidden_truth must be BlindAlignmentHiddenTruth")
        if type(self.cell_count) is not int or self.cell_count < 1:
            raise ValueError("cell_count must be a positive integer")
        if isinstance(self.eigenvalue_degeneracy_tolerance, bool) or not isinstance(
            self.eigenvalue_degeneracy_tolerance, int | float
        ):
            raise TypeError("eigenvalue_degeneracy_tolerance must be real")
        if (
            not np.isfinite(self.eigenvalue_degeneracy_tolerance)
            or self.eigenvalue_degeneracy_tolerance <= 0.0
        ):
            raise ValueError(
                "eigenvalue_degeneracy_tolerance must be positive and finite"
            )


@dataclass(frozen=True, slots=True)
class BlindAlignmentEvaluationResult:
    """Record distinct post hoc map, shift, extraction, model, and spectral errors.

    Parameters
    ----------
    identifier
        Campaign case identifier.
    phase_quotiented_alignment_frobenius_defect
        Frobenius norm of inferred-minus-authored map after one global phase quotient.
    energy_shift_error
        Inferred-minus-authored scalar shift in ``E_G``.
    extraction_frobenius_defect
        Absolute represented extraction error in ``E_G``.
    extraction_relative_frobenius_defect
        Extraction Frobenius defect divided by planted identified-sector norm, or zero
        when that norm is exactly zero.
    planted_onsite_model_class_residual
        Frobenius residual outside the first onsite block for planted truth.
    extracted_onsite_model_class_residual
        Corresponding residual for the inferred extraction.
    active_spectral_maximum_absolute_defect
        Maximum active-sector eigenvalue defect in ``E_G``.
    active_lowest_state_fidelity
        Lowest-state fidelity when the authored lowest eigenspace is one-dimensional;
        otherwise ``None``.
    active_lowest_eigenspace_dimension
        Authored lowest active-eigenspace multiplicity.
    active_lowest_eigenspace_projector_defect
        Frobenius difference of inferred and authored lowest-space projectors.
    alignment_map_sha256
        SHA-256 of canonical little-endian real-imaginary map coordinates.
    extracted_operator_sha256
        SHA-256 of canonical little-endian real-imaginary extraction coordinates.
    """

    identifier: str
    phase_quotiented_alignment_frobenius_defect: float
    energy_shift_error: float
    extraction_frobenius_defect: float
    extraction_relative_frobenius_defect: float
    planted_onsite_model_class_residual: float
    extracted_onsite_model_class_residual: float
    active_spectral_maximum_absolute_defect: float
    active_lowest_state_fidelity: float | None
    active_lowest_eigenspace_dimension: int
    active_lowest_eigenspace_projector_defect: float
    alignment_map_sha256: str
    extracted_operator_sha256: str

    def __post_init__(self) -> None:
        """Require finite diagnostics, valid fidelity, multiplicity, and digests."""
        if type(self.identifier) is not str or not self.identifier:
            raise ValueError("identifier must be nonempty")
        values = (
            self.phase_quotiented_alignment_frobenius_defect,
            self.energy_shift_error,
            self.extraction_frobenius_defect,
            self.extraction_relative_frobenius_defect,
            self.planted_onsite_model_class_residual,
            self.extracted_onsite_model_class_residual,
            self.active_spectral_maximum_absolute_defect,
            self.active_lowest_eigenspace_projector_defect,
        )
        if any(not np.isfinite(value) for value in values):
            raise ValueError("evaluation diagnostics must be finite")
        if self.active_lowest_state_fidelity is not None and (
            not np.isfinite(self.active_lowest_state_fidelity)
            or not 0.0 <= self.active_lowest_state_fidelity <= 1.0
        ):
            raise ValueError("lowest-state fidelity must lie in [0, 1]")
        if (
            type(self.active_lowest_eigenspace_dimension) is not int
            or self.active_lowest_eigenspace_dimension < 1
        ):
            raise ValueError("lowest eigenspace dimension must be a positive integer")
        for digest in (self.alignment_map_sha256, self.extracted_operator_sha256):
            if len(digest) != 64 or any(
                character not in "0123456789abcdef" for character in digest
            ):
                raise ValueError("matrix digests must be lowercase SHA-256 values")


class BlindAlignmentInferenceEvaluator:
    """Evaluate inferred outputs against truth withheld during inference.

    This Actionizer is deliberately separate from
    :class:`BlindAlignmentInferenceActionizer`. Supplying a hidden-truth record here
    does not alter or repeat inference; it computes only declared post hoc synthetic
    errors and canonical matrix identities.
    """

    __slots__ = ()

    def execute(
        self, request: BlindAlignmentEvaluationRequest
    ) -> BlindAlignmentEvaluationResult:
        """Evaluate one successful full or identified-sector result.

        Parameters
        ----------
        request
            Successful inference, separate hidden truth, and explicit evaluation
            controls.

        Returns
        -------
        BlindAlignmentEvaluationResult
            Separate map, shift, extraction, model-class, and spectral diagnostics.

        Raises
        ------
        TypeError
            If ``request`` has the wrong public type.
        ValueError
            If successful represented outputs are absent or dimensionally inconsistent.
        """
        if not isinstance(request, BlindAlignmentEvaluationRequest):
            raise TypeError("request must be BlindAlignmentEvaluationRequest")
        outcome = request.inference
        truth = request.hidden_truth
        alignment = outcome.alignment_map
        projector = outcome.reference_projector
        extracted = outcome.extracted_operator
        shift = outcome.inferred_energy_shift
        if alignment is None or projector is None or extracted is None or shift is None:
            raise ValueError("successful inference outputs are incomplete")
        expected_map = projector @ truth.candidate_to_reference
        phase = np.angle(np.trace(expected_map.conj().T @ alignment))
        map_defect = self._norm(alignment - np.exp(1j * phase) * expected_map)
        target = projector @ truth.planted_defect @ projector
        extraction_defect = self._norm(extracted - target)
        target_norm = self._norm(target)
        if target.shape[0] % request.cell_count != 0:
            raise ValueError("operator dimension must be divisible by cell_count")
        block_size = target.shape[0] // request.cell_count
        extracted_model = np.zeros_like(extracted)
        extracted_model[:block_size, :block_size] = extracted[:block_size, :block_size]
        planted_model = np.zeros_like(target)
        planted_model[:block_size, :block_size] = target[:block_size, :block_size]
        active_values, active_vectors = np.linalg.eigh(projector)
        active_basis = active_vectors[:, active_values > 0.5]
        if active_basis.shape[1] == 0:
            raise ValueError("identified reference sector must be nonempty")
        extracted_active = active_basis.conj().T @ extracted @ active_basis
        target_active = active_basis.conj().T @ target @ active_basis
        extracted_eigenvalues, extracted_vectors = np.linalg.eigh(extracted_active)
        target_eigenvalues, target_vectors = np.linalg.eigh(target_active)
        lowest_mask = (
            np.abs(target_eigenvalues - target_eigenvalues[0])
            <= request.eigenvalue_degeneracy_tolerance
        )
        lowest_dimension = int(np.sum(lowest_mask))
        target_lowest_projector = (
            target_vectors[:, :lowest_dimension]
            @ target_vectors[:, :lowest_dimension].conj().T
        )
        extracted_lowest_projector = (
            extracted_vectors[:, :lowest_dimension]
            @ extracted_vectors[:, :lowest_dimension].conj().T
        )
        fidelity: float | None = None
        if lowest_dimension == 1:
            fidelity = float(
                np.clip(
                    abs(np.vdot(extracted_vectors[:, 0], target_vectors[:, 0])) ** 2,
                    0.0,
                    1.0,
                )
            )
        return BlindAlignmentEvaluationResult(
            identifier=request.identifier,
            phase_quotiented_alignment_frobenius_defect=map_defect,
            energy_shift_error=shift - truth.energy_shift,
            extraction_frobenius_defect=extraction_defect,
            extraction_relative_frobenius_defect=(
                extraction_defect / target_norm if target_norm > 0.0 else 0.0
            ),
            planted_onsite_model_class_residual=self._norm(target - planted_model),
            extracted_onsite_model_class_residual=self._norm(
                extracted - extracted_model
            ),
            active_spectral_maximum_absolute_defect=float(
                np.max(np.abs(extracted_eigenvalues - target_eigenvalues))
            ),
            active_lowest_state_fidelity=fidelity,
            active_lowest_eigenspace_dimension=lowest_dimension,
            active_lowest_eigenspace_projector_defect=self._norm(
                extracted_lowest_projector - target_lowest_projector
            ),
            alignment_map_sha256=self._matrix_sha256(alignment),
            extracted_operator_sha256=self._matrix_sha256(extracted),
        )

    @staticmethod
    def _matrix_sha256(matrix: ComplexMatrix) -> str:
        """Hash canonical little-endian binary64 real-imaginary matrix coordinates."""
        canonical = np.stack((matrix.real, matrix.imag), axis=-1).astype(
            "<f8", copy=True
        )
        canonical[canonical == 0.0] = 0.0
        return hashlib.sha256(canonical.tobytes(order="C")).hexdigest()

    @staticmethod
    def _norm(matrix: ComplexMatrix) -> float:
        """Return the unnormalized matrix Frobenius norm as a Python float."""
        return float(np.linalg.norm(matrix))
