"""Canonical version-one encoding and identity correlation for blind alignment."""

from __future__ import annotations

import hashlib
import json

from .result_records import (
    BlindAlignmentCampaignResult,
    BlindAlignmentEnergyAnchorDiagnosticResult,
    BlindAlignmentResultCorrelation,
    BlindAlignmentResultCorrelationRequest,
    BlindAlignmentStoppedCaseResult,
    BlindAlignmentSuccessfulCaseResult,
    DiagnosticOutcome,
)
from .result_serialization import BlindAlignmentResultDeserializer
from .serialization import JsonValue


class BlindAlignmentResultSerializer:
    """Encode a typed result as canonical version-one UTF-8 JSON bytes."""

    __slots__ = ()

    def serialize(self, result: BlindAlignmentCampaignResult) -> bytes:
        """Serialize one complete typed result with sorted keys and trailing newline.

        Parameters
        ----------
        result
            Complete immutable campaign result.

        Returns
        -------
        bytes
            Canonical UTF-8 JSON using two-space indentation, sorted object keys, and a
            single trailing newline.

        Raises
        ------
        TypeError
            If ``result`` is not the exact public result type.
        """
        if not isinstance(result, BlindAlignmentCampaignResult):
            raise TypeError("result must be BlindAlignmentCampaignResult")
        return (
            json.dumps(
                self._document(result), indent=2, sort_keys=True, allow_nan=False
            )
            + "\n"
        ).encode("utf-8")

    def _document(self, result: BlindAlignmentCampaignResult) -> dict[str, JsonValue]:
        """Build the closed version-one document representation."""
        boundary = result.information_boundary
        contract = boundary.observation_contract
        policy = result.policy
        diagnostics = result.debugging_diagnostics
        rank = diagnostics.rank_reconciliation
        spin = diagnostics.spin_reconciliation
        gauge = result.gauge_equivalent_case
        provenance = result.provenance
        return {
            "calculation_status": "calculated synthetic numerical-verification result",
            "debugging_diagnostics": {
                "conditioning_boundary": [
                    {
                        **self._outcome(item.outcome),
                        "additive_anchor_noise_spectral_norm": (
                            item.additive_anchor_noise_spectral_norm
                        ),
                        "requested_minimum_anchor_singular_value": (
                            item.requested_minimum_anchor_singular_value
                        ),
                    }
                    for item in diagnostics.conditioning_boundary
                ],
                "energy_anchor_boundary": [
                    self._energy_anchor(item)
                    for item in diagnostics.energy_anchor_boundary
                ],
                "interpretation": diagnostics.interpretation,
                "principal_angle_boundary": [
                    {
                        **self._outcome(item.outcome),
                        "diagnostic_reference_basis_indices": list(
                            item.diagnostic_reference_basis_indices
                        ),
                        "minimum_subspace_overlap_singular_value": (
                            item.minimum_subspace_overlap_singular_value
                        ),
                        "requested_principal_angle_radians": (
                            item.requested_principal_angle_radians
                        ),
                    }
                    for item in diagnostics.principal_angle_boundary
                ],
                "rank_reconciliation": {
                    **self._successful(rank.case),
                    "candidate_dimension": rank.candidate_dimension,
                    "direct_comparison_issue_code": rank.direct_comparison_issue_code,
                    "dropped_dimension": rank.dropped_dimension,
                    "reference_dimension": rank.reference_dimension,
                    "resolution": rank.resolution,
                },
                "spin_reconciliation": {
                    "direct_comparison_issue_code": spin.direct_comparison_issue_code,
                    "direct_comparison_status": "stopped",
                    "lifted_alignment": self._successful(spin.lifted_alignment),
                    "lossless_spin_restriction_available": (
                        spin.lossless_spin_restriction_available
                    ),
                    "resolution": spin.resolution,
                    "spin_independent_restriction_residual": (
                        spin.spin_independent_restriction_residual
                    ),
                },
            },
            "error_accounting": dict(result.error_accounting),
            "evidence_status": "synthetic test data",
            "exact_full_rank_cases": [
                self._successful(case) for case in result.exact_full_rank_cases
            ],
            "experiment_id": result.experiment_id,
            "gauge_equivalent_case": {
                **self._successful(gauge.case),
                "compressed_completion_extraction_disagreement": (
                    gauge.compressed_completion_extraction_disagreement
                ),
                "full_completion_extraction_disagreement": (
                    gauge.full_completion_extraction_disagreement
                ),
                "identified_dimension": gauge.identified_dimension,
                "partial_map_agreement_between_completions": (
                    gauge.partial_map_agreement_between_completions
                ),
                "unidentified_complement_dimension": (
                    gauge.unidentified_complement_dimension
                ),
            },
            "information_boundary": {
                "declared_observation_contract": {
                    "anchor_cross_covariance": contract.anchor_cross_covariance,
                    "energy_reference": contract.energy_reference,
                    "orbital_labels": contract.orbital_labels,
                    "site_anchor_labels": contract.site_anchor_labels,
                    "spin_frame": contract.spin_frame,
                },
                "inference_inputs": list(boundary.inference_inputs),
                "oracle_use": boundary.oracle_use,
                "withheld_from_inference": list(boundary.withheld_from_inference),
            },
            "limitations": list(result.limitations),
            "noise_sweep": [
                {
                    **self._successful(item.case),
                    "unitary_noise_radians": item.unitary_noise_radians,
                }
                for item in result.noise_sweep
            ],
            "policy": {
                "anchor_rank_tolerance": policy.anchor_rank_tolerance,
                "core_radius_cells": result.core_radius_cells,
                "maximum_anchor_condition_number": (
                    policy.maximum_anchor_condition_number
                ),
                "maximum_principal_angle_radians": (
                    policy.maximum_principal_angle_radians
                ),
                "minimum_energy_anchor_rank": policy.minimum_energy_anchor_rank,
            },
            "provenance": {
                "input_path": provenance.input_path,
                "input_sha256": provenance.input_sha256,
                "numpy_version": provenance.numpy_version,
                "python_version": provenance.python_version,
                "script_path": provenance.script_path,
                "script_sha256": provenance.script_sha256,
            },
            "schema_version": 1,
            "source_identities": [
                {"path": identity.path, "sha256": identity.sha256}
                for identity in result.source_identities
            ],
            "stopping_cases": [
                {**self._stopped(item.outcome), "kind": item.kind}
                for item in result.stopping_cases
            ],
        }

    @staticmethod
    def _successful(case: BlindAlignmentSuccessfulCaseResult) -> dict[str, JsonValue]:
        """Flatten one successful inference and evaluation into wire fields."""
        evaluation = case.evaluation
        return {
            "active_lowest_eigenspace_dimension": (
                evaluation.active_lowest_eigenspace_dimension
            ),
            "active_lowest_eigenspace_projector_defect": (
                evaluation.active_lowest_eigenspace_projector_defect
            ),
            "active_lowest_state_fidelity": evaluation.active_lowest_state_fidelity,
            "active_spectral_maximum_absolute_defect": (
                evaluation.active_spectral_maximum_absolute_defect
            ),
            "alignment_map_sha256": evaluation.alignment_map_sha256,
            "anchor_condition_number": case.anchor_condition_number,
            "anchor_rank": case.anchor_rank,
            "dimension": case.dimension,
            "energy_anchor_rank": case.energy_anchor_rank,
            "energy_shift_error": evaluation.energy_shift_error,
            "extracted_onsite_model_class_residual": (
                evaluation.extracted_onsite_model_class_residual
            ),
            "extracted_operator_sha256": evaluation.extracted_operator_sha256,
            "extraction_frobenius_defect": evaluation.extraction_frobenius_defect,
            "extraction_relative_frobenius_defect": (
                evaluation.extraction_relative_frobenius_defect
            ),
            "id": case.identifier,
            "inferred_energy_shift": case.inferred_energy_shift,
            "issue_codes": [],
            "maximum_principal_angle_radians": case.maximum_principal_angle_radians,
            "minimum_anchor_singular_value": case.minimum_anchor_singular_value,
            "phase_quotiented_alignment_frobenius_defect": (
                evaluation.phase_quotiented_alignment_frobenius_defect
            ),
            "planted_onsite_model_class_residual": (
                evaluation.planted_onsite_model_class_residual
            ),
            "status": case.status,
        }

    @staticmethod
    def _stopped(case: BlindAlignmentStoppedCaseResult) -> dict[str, JsonValue]:
        """Flatten one structured stop with explicit null output fields."""
        return {
            "alignment_map": None,
            "anchor_condition_number": case.anchor_condition_number,
            "anchor_rank": case.anchor_rank,
            "energy_anchor_rank": case.energy_anchor_rank,
            "extracted_operator": None,
            "id": case.identifier,
            "inferred_energy_shift": None,
            "issue_codes": list(case.issue_codes),
            "maximum_principal_angle_radians": case.maximum_principal_angle_radians,
            "minimum_anchor_singular_value": case.minimum_anchor_singular_value,
            "status": "stopped",
        }

    def _outcome(self, outcome: DiagnosticOutcome) -> dict[str, JsonValue]:
        """Flatten either a successful or stopped diagnostic outcome."""
        if isinstance(outcome, BlindAlignmentSuccessfulCaseResult):
            return self._successful(outcome)
        return self._stopped(outcome)

    def _energy_anchor(
        self, item: BlindAlignmentEnergyAnchorDiagnosticResult
    ) -> dict[str, JsonValue]:
        """Flatten one exterior-rank diagnostic and its requested rank."""
        return {
            **self._outcome(item.outcome),
            "requested_energy_anchor_rank": item.requested_energy_anchor_rank,
        }


class BlindAlignmentRetainedResultCorrelator:
    """Correlate typed and retained identity without numerical verification."""

    __slots__ = ()

    def execute(
        self, request: BlindAlignmentResultCorrelationRequest
    ) -> BlindAlignmentResultCorrelation:
        """Compare semantic records and canonical bytes against retained bytes.

        Parameters
        ----------
        request
            Newly calculated result and retained version-one payload.

        Returns
        -------
        BlindAlignmentResultCorrelation
            Separate semantic, canonical-byte, and digest identity channels.

        Raises
        ------
        TypeError
            If ``request`` has the wrong public type.
        ValueError
            If the retained payload is not a valid version-one result.
        """
        if not isinstance(request, BlindAlignmentResultCorrelationRequest):
            raise TypeError("request must be BlindAlignmentResultCorrelationRequest")
        calculated = BlindAlignmentResultSerializer().serialize(
            request.calculated_result
        )
        retained = BlindAlignmentResultDeserializer().deserialize(
            request.retained_payload
        )
        return BlindAlignmentResultCorrelation(
            semantic_equal=request.calculated_result == retained,
            canonical_bytes_equal=calculated == request.retained_payload,
            calculated_sha256=hashlib.sha256(calculated).hexdigest(),
            retained_sha256=hashlib.sha256(request.retained_payload).hexdigest(),
        )
