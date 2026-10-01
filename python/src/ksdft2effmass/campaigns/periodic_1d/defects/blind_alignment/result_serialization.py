"""Strict version-one JSON decoding for retained blind-alignment results."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence

from .evaluation import BlindAlignmentEvaluationResult
from .input_records import (
    BlindAlignmentObservationInformationContract,
    BlindAlignmentSourceIdentity,
    BlindAlignmentStopKind,
)
from .records import BlindAlignmentInferencePolicy
from .result_records import (
    BlindAlignmentCampaignResult,
    BlindAlignmentConditioningDiagnosticResult,
    BlindAlignmentDiagnosticSuiteResult,
    BlindAlignmentEnergyAnchorDiagnosticResult,
    BlindAlignmentGaugeCaseResult,
    BlindAlignmentInformationBoundary,
    BlindAlignmentNoiseCaseResult,
    BlindAlignmentPrincipalAngleDiagnosticResult,
    BlindAlignmentProvenance,
    BlindAlignmentRankReconciliationResult,
    BlindAlignmentSpinReconciliationResult,
    BlindAlignmentStoppedCaseResult,
    BlindAlignmentStoppingControlResult,
    BlindAlignmentSuccessfulCaseResult,
    DiagnosticOutcome,
    SuccessfulStatus,
)
from .serialization import JsonValue


class BlindAlignmentResultDeserializer:
    """Decode only the closed semantic version-one result contract.

    The decoder accepts UTF-8 JSON bytes, rejects duplicate object keys and non-finite
    JSON constants, enforces exact object keys, validates fixed evidence/status
    declarations, and returns immutable typed records. Decoding and correlation do not
    numerically verify the retained calculation.
    """

    __slots__ = ()

    def deserialize(self, payload: bytes) -> BlindAlignmentCampaignResult:
        """Decode one canonical-compatible version-one result document.

        Parameters
        ----------
        payload
            UTF-8 JSON bytes.

        Returns
        -------
        BlindAlignmentCampaignResult
            Complete immutable semantic result.

        Raises
        ------
        TypeError
            If ``payload`` is not exact ``bytes``.
        ValueError
            If JSON syntax, keys, scalar types, fixed declarations, or invariants are
            invalid.
        """
        if type(payload) is not bytes:
            raise TypeError("payload must be exact bytes")
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValueError("payload must be UTF-8") from error
        try:
            decoded = json.loads(
                text,
                object_pairs_hook=self._unique_object,
                parse_constant=self._reject_constant,
            )
        except (json.JSONDecodeError, TypeError) as error:
            raise ValueError("payload must be valid strict JSON") from error
        root = self._mapping(
            decoded,
            (
                "calculation_status",
                "debugging_diagnostics",
                "error_accounting",
                "evidence_status",
                "exact_full_rank_cases",
                "experiment_id",
                "gauge_equivalent_case",
                "information_boundary",
                "limitations",
                "noise_sweep",
                "policy",
                "provenance",
                "schema_version",
                "source_identities",
                "stopping_cases",
            ),
            "result",
        )
        if self._integer(root["schema_version"], "schema_version") != 1:
            raise ValueError("unsupported blind-alignment result schema version")
        self._fixed(
            root["calculation_status"],
            "calculated synthetic numerical-verification result",
            "calculation_status",
        )
        self._fixed(root["evidence_status"], "synthetic test data", "evidence_status")
        policy_mapping = self._mapping(
            root["policy"],
            (
                "anchor_rank_tolerance",
                "core_radius_cells",
                "maximum_anchor_condition_number",
                "maximum_principal_angle_radians",
                "minimum_energy_anchor_rank",
            ),
            "policy",
        )
        policy = BlindAlignmentInferencePolicy(
            anchor_rank_tolerance=self._real(
                policy_mapping["anchor_rank_tolerance"], "anchor_rank_tolerance"
            ),
            maximum_anchor_condition_number=self._real(
                policy_mapping["maximum_anchor_condition_number"],
                "maximum_anchor_condition_number",
            ),
            maximum_principal_angle_radians=self._real(
                policy_mapping["maximum_principal_angle_radians"],
                "maximum_principal_angle_radians",
            ),
            minimum_energy_anchor_rank=self._integer(
                policy_mapping["minimum_energy_anchor_rank"],
                "minimum_energy_anchor_rank",
            ),
        )
        return BlindAlignmentCampaignResult(
            experiment_id=self._string(root["experiment_id"], "experiment_id"),
            information_boundary=self._information_boundary(
                root["information_boundary"]
            ),
            policy=policy,
            core_radius_cells=self._integer(
                policy_mapping["core_radius_cells"], "core_radius_cells"
            ),
            exact_full_rank_cases=tuple(
                self._successful(value)
                for value in self._sequence(
                    root["exact_full_rank_cases"], "exact_full_rank_cases"
                )
            ),
            noise_sweep=tuple(
                self._noise(value)
                for value in self._sequence(root["noise_sweep"], "noise_sweep")
            ),
            gauge_equivalent_case=self._gauge(root["gauge_equivalent_case"]),
            stopping_cases=tuple(
                self._stopping_control(value)
                for value in self._sequence(root["stopping_cases"], "stopping_cases")
            ),
            debugging_diagnostics=self._diagnostics(root["debugging_diagnostics"]),
            source_identities=tuple(
                self._source_identity(value)
                for value in self._sequence(
                    root["source_identities"], "source_identities"
                )
            ),
            error_accounting=self._string_mapping_entries(
                root["error_accounting"], "error_accounting"
            ),
            limitations=self._string_tuple(root["limitations"], "limitations"),
            provenance=self._provenance(root["provenance"]),
        )

    def _successful(self, value: JsonValue) -> BlindAlignmentSuccessfulCaseResult:
        """Decode one exact flattened successful outcome."""
        item = self._mapping(
            value,
            (
                "active_lowest_eigenspace_dimension",
                "active_lowest_eigenspace_projector_defect",
                "active_lowest_state_fidelity",
                "active_spectral_maximum_absolute_defect",
                "alignment_map_sha256",
                "anchor_condition_number",
                "anchor_rank",
                "dimension",
                "energy_anchor_rank",
                "energy_shift_error",
                "extracted_onsite_model_class_residual",
                "extracted_operator_sha256",
                "extraction_frobenius_defect",
                "extraction_relative_frobenius_defect",
                "id",
                "inferred_energy_shift",
                "issue_codes",
                "maximum_principal_angle_radians",
                "minimum_anchor_singular_value",
                "phase_quotiented_alignment_frobenius_defect",
                "planted_onsite_model_class_residual",
                "status",
            ),
            "successful case",
        )
        if self._sequence(item["issue_codes"], "issue_codes"):
            raise ValueError("successful case issue_codes must be empty")
        identifier = self._string(item["id"], "id")
        status = self._string(item["status"], "status")
        successful_status: SuccessfulStatus
        if status == "aligned_full":
            successful_status = "aligned_full"
        elif status == "aligned_partial":
            successful_status = "aligned_partial"
        else:
            raise ValueError("successful case has unsupported status")
        fidelity_value = item["active_lowest_state_fidelity"]
        fidelity = (
            None
            if fidelity_value is None
            else self._real(fidelity_value, "active_lowest_state_fidelity")
        )
        evaluation = BlindAlignmentEvaluationResult(
            identifier=identifier,
            phase_quotiented_alignment_frobenius_defect=self._real(
                item["phase_quotiented_alignment_frobenius_defect"],
                "phase_quotiented_alignment_frobenius_defect",
            ),
            energy_shift_error=self._real(
                item["energy_shift_error"], "energy_shift_error"
            ),
            extraction_frobenius_defect=self._real(
                item["extraction_frobenius_defect"], "extraction_frobenius_defect"
            ),
            extraction_relative_frobenius_defect=self._real(
                item["extraction_relative_frobenius_defect"],
                "extraction_relative_frobenius_defect",
            ),
            planted_onsite_model_class_residual=self._real(
                item["planted_onsite_model_class_residual"],
                "planted_onsite_model_class_residual",
            ),
            extracted_onsite_model_class_residual=self._real(
                item["extracted_onsite_model_class_residual"],
                "extracted_onsite_model_class_residual",
            ),
            active_spectral_maximum_absolute_defect=self._real(
                item["active_spectral_maximum_absolute_defect"],
                "active_spectral_maximum_absolute_defect",
            ),
            active_lowest_state_fidelity=fidelity,
            active_lowest_eigenspace_dimension=self._integer(
                item["active_lowest_eigenspace_dimension"],
                "active_lowest_eigenspace_dimension",
            ),
            active_lowest_eigenspace_projector_defect=self._real(
                item["active_lowest_eigenspace_projector_defect"],
                "active_lowest_eigenspace_projector_defect",
            ),
            alignment_map_sha256=self._string(
                item["alignment_map_sha256"], "alignment_map_sha256"
            ),
            extracted_operator_sha256=self._string(
                item["extracted_operator_sha256"], "extracted_operator_sha256"
            ),
        )
        return BlindAlignmentSuccessfulCaseResult(
            identifier=identifier,
            status=successful_status,
            dimension=self._integer(item["dimension"], "dimension"),
            anchor_rank=self._integer(item["anchor_rank"], "anchor_rank"),
            anchor_condition_number=self._real(
                item["anchor_condition_number"], "anchor_condition_number"
            ),
            minimum_anchor_singular_value=self._real(
                item["minimum_anchor_singular_value"],
                "minimum_anchor_singular_value",
            ),
            maximum_principal_angle_radians=self._real(
                item["maximum_principal_angle_radians"],
                "maximum_principal_angle_radians",
            ),
            energy_anchor_rank=self._real(
                item["energy_anchor_rank"], "energy_anchor_rank"
            ),
            inferred_energy_shift=self._real(
                item["inferred_energy_shift"], "inferred_energy_shift"
            ),
            evaluation=evaluation,
        )

    def _stopped(
        self, value: JsonValue, extra_keys: tuple[str, ...] = ()
    ) -> BlindAlignmentStoppedCaseResult:
        """Decode one flattened stopped outcome with optional wrapper keys."""
        item = self._mapping(
            value,
            (
                "alignment_map",
                "anchor_condition_number",
                "anchor_rank",
                "energy_anchor_rank",
                "extracted_operator",
                "id",
                "inferred_energy_shift",
                "issue_codes",
                "maximum_principal_angle_radians",
                "minimum_anchor_singular_value",
                "status",
                *extra_keys,
            ),
            "stopped case",
        )
        self._fixed(item["status"], "stopped", "stopped status")
        for key in ("alignment_map", "extracted_operator", "inferred_energy_shift"):
            if item[key] is not None:
                raise ValueError(f"stopped case {key} must be null")
        return BlindAlignmentStoppedCaseResult(
            identifier=self._string(item["id"], "id"),
            issue_codes=self._string_tuple(item["issue_codes"], "issue_codes"),
            anchor_rank=self._integer(item["anchor_rank"], "anchor_rank"),
            anchor_condition_number=self._optional_real(
                item["anchor_condition_number"], "anchor_condition_number"
            ),
            minimum_anchor_singular_value=self._optional_real(
                item["minimum_anchor_singular_value"],
                "minimum_anchor_singular_value",
            ),
            maximum_principal_angle_radians=self._optional_real(
                item["maximum_principal_angle_radians"],
                "maximum_principal_angle_radians",
            ),
            energy_anchor_rank=self._optional_real(
                item["energy_anchor_rank"], "energy_anchor_rank"
            ),
        )

    def _noise(self, value: JsonValue) -> BlindAlignmentNoiseCaseResult:
        """Decode a successful case carrying one unitary-noise control."""
        item = self._mapping(
            value, (*self._successful_keys(), "unitary_noise_radians"), "noise case"
        )
        return BlindAlignmentNoiseCaseResult(
            case=self._successful(self._without(item, ("unitary_noise_radians",))),
            unitary_noise_radians=self._real(
                item["unitary_noise_radians"], "unitary_noise_radians"
            ),
        )

    def _gauge(self, value: JsonValue) -> BlindAlignmentGaugeCaseResult:
        """Decode the identified-sector completion-nonuniqueness control."""
        extras = (
            "compressed_completion_extraction_disagreement",
            "full_completion_extraction_disagreement",
            "identified_dimension",
            "partial_map_agreement_between_completions",
            "unidentified_complement_dimension",
        )
        item = self._mapping(value, (*self._successful_keys(), *extras), "gauge case")
        return BlindAlignmentGaugeCaseResult(
            case=self._successful(self._without(item, extras)),
            identified_dimension=self._integer(
                item["identified_dimension"], "identified_dimension"
            ),
            unidentified_complement_dimension=self._integer(
                item["unidentified_complement_dimension"],
                "unidentified_complement_dimension",
            ),
            full_completion_extraction_disagreement=self._real(
                item["full_completion_extraction_disagreement"],
                "full_completion_extraction_disagreement",
            ),
            compressed_completion_extraction_disagreement=self._real(
                item["compressed_completion_extraction_disagreement"],
                "compressed_completion_extraction_disagreement",
            ),
            partial_map_agreement_between_completions=self._real(
                item["partial_map_agreement_between_completions"],
                "partial_map_agreement_between_completions",
            ),
        )

    def _stopping_control(
        self, value: JsonValue
    ) -> BlindAlignmentStoppingControlResult:
        """Decode one authored negative control and structured stop."""
        item = self._mapping(value, (*self._stopped_keys(), "kind"), "stopping control")
        kind_value = self._string(item["kind"], "kind")
        kind: BlindAlignmentStopKind
        if kind_value == "anchor-condition":
            kind = "anchor-condition"
        elif kind_value == "principal-angle":
            kind = "principal-angle"
        elif kind_value == "rank-mismatch":
            kind = "rank-mismatch"
        elif kind_value == "spin-mismatch":
            kind = "spin-mismatch"
        elif kind_value == "energy-anchor":
            kind = "energy-anchor"
        else:
            raise ValueError("unsupported stopping-control kind")
        return BlindAlignmentStoppingControlResult(
            kind=kind,
            outcome=self._stopped(item, ("kind",)),
        )

    def _diagnostics(self, value: JsonValue) -> BlindAlignmentDiagnosticSuiteResult:
        """Decode all neighboring stopping-boundary diagnostics."""
        item = self._mapping(
            value,
            (
                "conditioning_boundary",
                "energy_anchor_boundary",
                "interpretation",
                "principal_angle_boundary",
                "rank_reconciliation",
                "spin_reconciliation",
            ),
            "debugging_diagnostics",
        )
        return BlindAlignmentDiagnosticSuiteResult(
            conditioning_boundary=tuple(
                self._conditioning(value)
                for value in self._sequence(
                    item["conditioning_boundary"], "conditioning_boundary"
                )
            ),
            principal_angle_boundary=tuple(
                self._principal_angle(value)
                for value in self._sequence(
                    item["principal_angle_boundary"], "principal_angle_boundary"
                )
            ),
            rank_reconciliation=self._rank(item["rank_reconciliation"]),
            spin_reconciliation=self._spin(item["spin_reconciliation"]),
            energy_anchor_boundary=tuple(
                self._energy_anchor(value)
                for value in self._sequence(
                    item["energy_anchor_boundary"], "energy_anchor_boundary"
                )
            ),
            interpretation=self._string(item["interpretation"], "interpretation"),
        )

    def _conditioning(
        self, value: JsonValue
    ) -> BlindAlignmentConditioningDiagnosticResult:
        """Decode one conditioning-boundary diagnostic."""
        extras = (
            "additive_anchor_noise_spectral_norm",
            "requested_minimum_anchor_singular_value",
        )
        item = self._diagnostic_mapping(value, extras, "conditioning diagnostic")
        return BlindAlignmentConditioningDiagnosticResult(
            outcome=self._outcome(self._without(item, extras)),
            requested_minimum_anchor_singular_value=self._real(
                item["requested_minimum_anchor_singular_value"],
                "requested_minimum_anchor_singular_value",
            ),
            additive_anchor_noise_spectral_norm=self._real(
                item["additive_anchor_noise_spectral_norm"],
                "additive_anchor_noise_spectral_norm",
            ),
        )

    def _principal_angle(
        self, value: JsonValue
    ) -> BlindAlignmentPrincipalAngleDiagnosticResult:
        """Decode one principal-angle boundary diagnostic."""
        extras = (
            "diagnostic_reference_basis_indices",
            "minimum_subspace_overlap_singular_value",
            "requested_principal_angle_radians",
        )
        item = self._diagnostic_mapping(value, extras, "principal-angle diagnostic")
        return BlindAlignmentPrincipalAngleDiagnosticResult(
            outcome=self._outcome(self._without(item, extras)),
            requested_principal_angle_radians=self._real(
                item["requested_principal_angle_radians"],
                "requested_principal_angle_radians",
            ),
            minimum_subspace_overlap_singular_value=self._real(
                item["minimum_subspace_overlap_singular_value"],
                "minimum_subspace_overlap_singular_value",
            ),
            diagnostic_reference_basis_indices=tuple(
                self._integer(entry, "diagnostic_reference_basis_indices entry")
                for entry in self._sequence(
                    item["diagnostic_reference_basis_indices"],
                    "diagnostic_reference_basis_indices",
                )
            ),
        )

    def _energy_anchor(
        self, value: JsonValue
    ) -> BlindAlignmentEnergyAnchorDiagnosticResult:
        """Decode one exterior energy-anchor boundary diagnostic."""
        extras = ("requested_energy_anchor_rank",)
        item = self._diagnostic_mapping(value, extras, "energy-anchor diagnostic")
        return BlindAlignmentEnergyAnchorDiagnosticResult(
            outcome=self._outcome(self._without(item, extras)),
            requested_energy_anchor_rank=self._integer(
                item["requested_energy_anchor_rank"], "requested_energy_anchor_rank"
            ),
        )

    def _rank(self, value: JsonValue) -> BlindAlignmentRankReconciliationResult:
        """Decode explicit unequal-rank rectangular reconciliation."""
        extras = (
            "candidate_dimension",
            "direct_comparison_issue_code",
            "dropped_dimension",
            "reference_dimension",
            "resolution",
        )
        item = self._mapping(
            value, (*self._successful_keys(), *extras), "rank reconciliation"
        )
        return BlindAlignmentRankReconciliationResult(
            case=self._successful(self._without(item, extras)),
            direct_comparison_issue_code=self._string(
                item["direct_comparison_issue_code"], "direct_comparison_issue_code"
            ),
            reference_dimension=self._integer(
                item["reference_dimension"], "reference_dimension"
            ),
            candidate_dimension=self._integer(
                item["candidate_dimension"], "candidate_dimension"
            ),
            dropped_dimension=self._integer(
                item["dropped_dimension"], "dropped_dimension"
            ),
            resolution=self._string(item["resolution"], "resolution"),
        )

    def _spin(self, value: JsonValue) -> BlindAlignmentSpinReconciliationResult:
        """Decode direct spin mismatch and explicit spin-lift reconciliation."""
        item = self._mapping(
            value,
            (
                "direct_comparison_issue_code",
                "direct_comparison_status",
                "lifted_alignment",
                "lossless_spin_restriction_available",
                "resolution",
                "spin_independent_restriction_residual",
            ),
            "spin reconciliation",
        )
        self._fixed(
            item["direct_comparison_status"], "stopped", "direct comparison status"
        )
        return BlindAlignmentSpinReconciliationResult(
            direct_comparison_issue_code=self._string(
                item["direct_comparison_issue_code"], "direct_comparison_issue_code"
            ),
            resolution=self._string(item["resolution"], "resolution"),
            spin_independent_restriction_residual=self._real(
                item["spin_independent_restriction_residual"],
                "spin_independent_restriction_residual",
            ),
            lossless_spin_restriction_available=self._boolean(
                item["lossless_spin_restriction_available"],
                "lossless_spin_restriction_available",
            ),
            lifted_alignment=self._successful(item["lifted_alignment"]),
        )

    def _information_boundary(
        self, value: JsonValue
    ) -> BlindAlignmentInformationBoundary:
        """Decode the declared inference and oracle-use information boundary."""
        item = self._mapping(
            value,
            (
                "declared_observation_contract",
                "inference_inputs",
                "oracle_use",
                "withheld_from_inference",
            ),
            "information_boundary",
        )
        contract = self._mapping(
            item["declared_observation_contract"],
            (
                "anchor_cross_covariance",
                "energy_reference",
                "orbital_labels",
                "site_anchor_labels",
                "spin_frame",
            ),
            "declared_observation_contract",
        )
        return BlindAlignmentInformationBoundary(
            observation_contract=BlindAlignmentObservationInformationContract(
                orbital_labels=self._string(
                    contract["orbital_labels"], "orbital_labels"
                ),
                site_anchor_labels=self._string(
                    contract["site_anchor_labels"], "site_anchor_labels"
                ),
                anchor_cross_covariance=self._string(
                    contract["anchor_cross_covariance"], "anchor_cross_covariance"
                ),
                energy_reference=self._string(
                    contract["energy_reference"], "energy_reference"
                ),
                spin_frame=self._string(contract["spin_frame"], "spin_frame"),
            ),
            inference_inputs=self._string_tuple(
                item["inference_inputs"], "inference_inputs"
            ),
            withheld_from_inference=self._string_tuple(
                item["withheld_from_inference"], "withheld_from_inference"
            ),
            oracle_use=self._string(item["oracle_use"], "oracle_use"),
        )

    def _source_identity(self, value: JsonValue) -> BlindAlignmentSourceIdentity:
        """Decode one authenticated source path and digest."""
        item = self._mapping(value, ("path", "sha256"), "source identity")
        return BlindAlignmentSourceIdentity(
            path=self._string(item["path"], "path"),
            sha256=self._string(item["sha256"], "sha256"),
        )

    def _provenance(self, value: JsonValue) -> BlindAlignmentProvenance:
        """Decode the retained execution-provenance record."""
        item = self._mapping(
            value,
            (
                "input_path",
                "input_sha256",
                "numpy_version",
                "python_version",
                "script_path",
                "script_sha256",
            ),
            "provenance",
        )
        return BlindAlignmentProvenance(
            input_path=self._string(item["input_path"], "input_path"),
            input_sha256=self._string(item["input_sha256"], "input_sha256"),
            script_path=self._string(item["script_path"], "script_path"),
            script_sha256=self._string(item["script_sha256"], "script_sha256"),
            python_version=self._string(item["python_version"], "python_version"),
            numpy_version=self._string(item["numpy_version"], "numpy_version"),
        )

    def _outcome(self, value: JsonValue) -> DiagnosticOutcome:
        """Decode a successful or stopped flattened diagnostic outcome."""
        item = self._unrestricted_mapping(value, "diagnostic outcome")
        status = self._string(item.get("status"), "status")
        if status == "stopped":
            return self._stopped(item)
        return self._successful(item)

    def _diagnostic_mapping(
        self, value: JsonValue, extras: tuple[str, ...], context: str
    ) -> dict[str, JsonValue]:
        """Require keys for one successful-or-stopped diagnostic plus extras."""
        item = self._unrestricted_mapping(value, context)
        status = self._string(item.get("status"), "status")
        base = self._stopped_keys() if status == "stopped" else self._successful_keys()
        return self._mapping(item, (*base, *extras), context)

    @staticmethod
    def _successful_keys() -> tuple[str, ...]:
        """Return exact flattened successful-case wire keys."""
        return (
            "active_lowest_eigenspace_dimension",
            "active_lowest_eigenspace_projector_defect",
            "active_lowest_state_fidelity",
            "active_spectral_maximum_absolute_defect",
            "alignment_map_sha256",
            "anchor_condition_number",
            "anchor_rank",
            "dimension",
            "energy_anchor_rank",
            "energy_shift_error",
            "extracted_onsite_model_class_residual",
            "extracted_operator_sha256",
            "extraction_frobenius_defect",
            "extraction_relative_frobenius_defect",
            "id",
            "inferred_energy_shift",
            "issue_codes",
            "maximum_principal_angle_radians",
            "minimum_anchor_singular_value",
            "phase_quotiented_alignment_frobenius_defect",
            "planted_onsite_model_class_residual",
            "status",
        )

    @staticmethod
    def _stopped_keys() -> tuple[str, ...]:
        """Return exact flattened stopped-case wire keys."""
        return (
            "alignment_map",
            "anchor_condition_number",
            "anchor_rank",
            "energy_anchor_rank",
            "extracted_operator",
            "id",
            "inferred_energy_shift",
            "issue_codes",
            "maximum_principal_angle_radians",
            "minimum_anchor_singular_value",
            "status",
        )

    @staticmethod
    def _without(
        mapping: Mapping[str, JsonValue], excluded: tuple[str, ...]
    ) -> dict[str, JsonValue]:
        """Return a shallow object without wrapper-only fields."""
        return {key: value for key, value in mapping.items() if key not in excluded}

    @staticmethod
    def _unique_object(pairs: list[tuple[str, JsonValue]]) -> dict[str, JsonValue]:
        """Construct one object while rejecting duplicate JSON member names."""
        result: dict[str, JsonValue] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    @staticmethod
    def _reject_constant(token: str) -> JsonValue:
        """Reject non-finite JSON constants unsupported by the contract."""
        raise ValueError(f"non-finite JSON constant is invalid: {token}")

    def _mapping(
        self, value: JsonValue, required: tuple[str, ...], context: str
    ) -> dict[str, JsonValue]:
        """Require a string-key mapping with exactly the declared keys."""
        mapping = self._unrestricted_mapping(value, context)
        if set(mapping) != set(required):
            raise ValueError(f"{context} keys must be exactly {sorted(required)}")
        return mapping

    @staticmethod
    def _unrestricted_mapping(value: JsonValue, context: str) -> dict[str, JsonValue]:
        """Require a string-key JSON object without imposing a key set."""
        if not isinstance(value, Mapping):
            raise TypeError(f"{context} must be an object")
        result: dict[str, JsonValue] = {}
        for key, item in value.items():
            if type(key) is not str:
                raise TypeError(f"{context} keys must be strings")
            result[key] = item
        return result

    @staticmethod
    def _sequence(value: JsonValue, context: str) -> tuple[JsonValue, ...]:
        """Require a JSON array rather than text or an object."""
        if not isinstance(value, Sequence) or isinstance(value, str | bytes):
            raise TypeError(f"{context} must be an array")
        return tuple(value)

    def _string_tuple(self, value: JsonValue, context: str) -> tuple[str, ...]:
        """Decode a JSON array of exact strings."""
        return tuple(
            self._string(entry, f"{context} entry")
            for entry in self._sequence(value, context)
        )

    def _string_mapping_entries(
        self, value: JsonValue, context: str
    ) -> tuple[tuple[str, str], ...]:
        """Decode an object as deterministically key-sorted text entries."""
        mapping = self._unrestricted_mapping(value, context)
        return tuple(
            (key, self._string(mapping[key], f"{context}.{key}"))
            for key in sorted(mapping)
        )

    @staticmethod
    def _string(value: JsonValue | None, context: str) -> str:
        """Require one exact nonempty string."""
        if type(value) is not str or not value:
            raise TypeError(f"{context} must be a nonempty string")
        return value

    @staticmethod
    def _integer(value: JsonValue, context: str) -> int:
        """Require one exact JSON integer and reject Boolean values."""
        if type(value) is not int:
            raise TypeError(f"{context} must be an integer")
        return value

    @staticmethod
    def _real(value: JsonValue, context: str) -> float:
        """Require one JSON integer or real and reject Boolean values."""
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{context} must be real")
        return float(value)

    def _optional_real(self, value: JsonValue, context: str) -> float | None:
        """Decode a nullable finite real scalar."""
        return None if value is None else self._real(value, context)

    @staticmethod
    def _boolean(value: JsonValue, context: str) -> bool:
        """Require one exact JSON Boolean."""
        if type(value) is not bool:
            raise TypeError(f"{context} must be Boolean")
        return value

    def _fixed(self, value: JsonValue, expected: str, context: str) -> None:
        """Require one exact fixed string declaration."""
        if self._string(value, context) != expected:
            raise ValueError(f"{context} must be {expected!r}")
