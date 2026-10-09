"""Schema-specific decoding for the standalone optimizer-study documents."""

from __future__ import annotations

import json
import math
from typing import cast

from ksdft2effmass.serialization.json import JsonValue, StrictJsonDecoder

from .encoded_documents import Periodic2DOptimizerStandaloneEncodedDocuments
from .records import (
    OptimizerStandaloneBasin,
    OptimizerStandaloneControlObservation,
    OptimizerStandaloneControls,
    OptimizerStandaloneDecodedDocuments,
    OptimizerStandaloneEndpoint,
    OptimizerStandaloneExecutionSummary,
    OptimizerStandaloneGaugeDesign,
    OptimizerStandaloneGroup,
    OptimizerStandaloneMemberEquivalence,
    OptimizerStandaloneNativeCenter,
    OptimizerStandaloneNativeEndpoint,
    OptimizerStandaloneProposal,
    OptimizerStandaloneProvenance,
    OptimizerStandaloneRejectedEquivalence,
    OptimizerStandaloneResult,
    OptimizerStandaloneSensitivity,
)

_SCHEMA_VERSION = 1

type LegacyStandaloneJsonValue = (
    None
    | bool
    | int
    | float
    | str
    | list[LegacyStandaloneJsonValue]
    | dict[str, LegacyStandaloneJsonValue]
)
type JsonPathPart = str | int


class OptimizerStandaloneLegacyResultDecoder:
    """Decode one historical result wire with a bounded ``Infinity`` extension.

    The retained result uses bare ``Infinity`` only for two extended-real fields in
    rejected basin-equivalence candidates. Duplicate keys, ``NaN``, ``-Infinity``, and
    nonfinite values at every other location fail closed. Mutable parse containers never
    leave this decoder.
    """

    __slots__ = ()

    def execute(self, payload: bytes) -> dict[str, LegacyStandaloneJsonValue]:
        """Decode and validate the historical standalone-result object.

        Parameters
        ----------
        payload
            Exact retained result bytes.

        Returns
        -------
        dict[str, LegacyStandaloneJsonValue]
            Temporary duplicate-free historical parse tree.

        Raises
        ------
        TypeError
            If ``payload`` is not exact bytes or the root/value representation is wrong.
        ValueError
            If UTF-8/JSON is malformed, keys repeat, or a nonfinite token is outside the
            two declared rejected-equivalence fields.
        MemoryError
            If parsing cannot allocate the tree.
        RecursionError
            If the wire exceeds parser or validation recursion depth.
        """
        if type(payload) is not bytes:
            raise TypeError("payload must be exact bytes")
        try:
            raw = cast(
                LegacyStandaloneJsonValue,
                json.loads(
                    payload.decode("utf-8"),
                    object_pairs_hook=self._object_from_pairs,
                    parse_constant=self._nonfinite_constant,
                ),
            )
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError("payload must be valid UTF-8 historical JSON") from error
        if type(raw) is not dict:
            raise TypeError("result root must be a JSON object")
        self._check_value(raw, ())
        return raw

    def _object_from_pairs(
        self, pairs: list[tuple[str, LegacyStandaloneJsonValue]]
    ) -> dict[str, LegacyStandaloneJsonValue]:
        """Construct an object while rejecting duplicate keys."""
        result: dict[str, LegacyStandaloneJsonValue] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    def _nonfinite_constant(self, value: str) -> float:
        """Recognize only the historical positive-infinity token."""
        if value == "Infinity":
            return math.inf
        raise ValueError(f"unsupported historical constant: {value}")

    def _check_value(
        self, value: LegacyStandaloneJsonValue, path: tuple[JsonPathPart, ...]
    ) -> None:
        """Require closed JSON values and confine positive infinity by exact path."""
        if value is None or type(value) in {bool, int, str}:
            return
        if type(value) is float:
            if math.isfinite(value):
                return
            if value != math.inf or not self._is_extended_real_path(path):
                raise ValueError("nonfinite value lies outside the historical contract")
            return
        if type(value) is list:
            for index, item in enumerate(value):
                self._check_value(item, (*path, index))
            return
        if type(value) is dict:
            for key, item in value.items():
                if type(key) is not str:
                    raise TypeError("historical JSON object keys must be strings")
                self._check_value(item, (*path, key))
            return
        raise TypeError("historical result contains an unsupported representation")

    def _is_extended_real_path(self, path: tuple[JsonPathPart, ...]) -> bool:
        """Return whether ``path`` exactly names a declared extended-real field."""
        return (
            len(path) == 7
            and path[0] == "groups"
            and type(path[1]) is int
            and path[2] == "observed_density_d4_basins"
            and type(path[3]) is int
            and path[4] == "rejected_equivalence_candidates"
            and type(path[5]) is int
            and path[6]
            in {
                "center_set_periodic_distance",
                "maximum_density_l2_mismatch",
            }
        )


class Periodic2DOptimizerStandaloneDocumentDecoder:
    """Adapt three exact wires to closed immutable row-055 records."""

    __slots__ = ("decoder", "result_decoder")

    def __init__(self) -> None:
        """Create strict proposal/gauge and bounded historical-result decoders."""
        self.decoder = StrictJsonDecoder()
        self.result_decoder = OptimizerStandaloneLegacyResultDecoder()

    def execute(
        self, documents: Periodic2DOptimizerStandaloneEncodedDocuments
    ) -> OptimizerStandaloneDecodedDocuments:
        """Decode verifier-owned fields without assigning scientific validity.

        Parameters
        ----------
        documents
            Exact proposal, initial-gauge, and standalone-result wires.

        Returns
        -------
        OptimizerStandaloneDecodedDocuments
            Closed immutable verifier-owned records.

        Raises
        ------
        TypeError
            If a wire or field has an incompatible exact representation.
        ValueError
            If JSON, a digest, or a numeric value violates its wire contract.
        OverflowError
            If integer-to-binary64 conversion is unrepresentable.
        KeyError
            If a required verifier-owned field is absent.
        AssertionError
            If a schema version is unsupported.
        MemoryError
            If decoding or record adaptation cannot allocate required state.
        RecursionError
            If a document exceeds parser or validation recursion depth.
        """
        if type(documents) is not Periodic2DOptimizerStandaloneEncodedDocuments:
            raise TypeError(
                "documents must be Periodic2DOptimizerStandaloneEncodedDocuments"
            )
        proposal_root = self.decoder.document(documents.proposal_payload)
        gauge_root = self.decoder.document(documents.initial_gauges_payload)
        result_root = self.result_decoder.execute(documents.result_payload)
        return OptimizerStandaloneDecodedDocuments(
            proposal=self._proposal(proposal_root),
            gauge_design=self._gauge_design(gauge_root),
            result=self._result(result_root),
        )

    def _proposal(self, root: dict[str, JsonValue]) -> OptimizerStandaloneProposal:
        """Adapt schema and basin-threshold fields from the proposal."""
        schema = self.decoder.integer(root["schema_version"], "proposal.schema_version")
        self._require_schema(schema, "proposal")
        method = self._mapping(root["basin_method"], "proposal.basin_method")
        return OptimizerStandaloneProposal(
            schema_version=schema,
            spread_tolerance=self.decoder.real(
                method["spread_absolute_tolerance_cell_squared"],
                "proposal.basin_method.spread_absolute_tolerance_cell_squared",
            ),
            center_tolerance=self.decoder.real(
                method["center_set_periodic_tolerance_cell"],
                "proposal.basin_method.center_set_periodic_tolerance_cell",
            ),
            density_tolerance=self.decoder.real(
                method["maximum_matched_density_l2_mismatch"],
                "proposal.basin_method.maximum_matched_density_l2_mismatch",
            ),
            best_basin_minimum_occupancy=self.decoder.integer(
                method["best_basin_minimum_occupancy"],
                "proposal.basin_method.best_basin_minimum_occupancy",
            ),
        )

    def _gauge_design(
        self, root: dict[str, JsonValue]
    ) -> OptimizerStandaloneGaugeDesign:
        """Adapt schema, proposal identity, and ordered deterministic starts."""
        schema = self.decoder.integer(root["schema_version"], "gauges.schema_version")
        self._require_schema(schema, "gauges")
        values = self._array(root["starts"], "gauges.starts")
        start_ids: list[str] = []
        for index, value in enumerate(values):
            item = self._mapping(value, f"gauges.starts[{index}]")
            start_ids.append(
                self.decoder.nonempty_string(
                    item["start_id"], f"gauges.starts[{index}].start_id"
                )
            )
        return OptimizerStandaloneGaugeDesign(
            schema_version=schema,
            proposal_sha256=self.decoder.sha256(
                root["proposal_sha256"], "gauges.proposal_sha256"
            ),
            declared_start_count=self.decoder.integer(
                root["start_count"], "gauges.start_count"
            ),
            start_ids=tuple(start_ids),
        )

    def _result(
        self, root: dict[str, LegacyStandaloneJsonValue]
    ) -> OptimizerStandaloneResult:
        """Adapt all verifier-owned fields from the historical result."""
        schema = self.decoder.integer(root["schema_version"], "result.schema_version")
        self._require_schema(schema, "result")
        provenance_value = self._legacy_mapping(root["provenance"], "result.provenance")
        provenance = OptimizerStandaloneProvenance(
            proposal_sha256=self.decoder.sha256(
                provenance_value["proposal_sha256"],
                "result.provenance.proposal_sha256",
            ),
            extractor_path=self.decoder.nonempty_string(
                provenance_value["extractor_path"],
                "result.provenance.extractor_path",
            ),
            extractor_sha256=self.decoder.sha256(
                provenance_value["extractor_sha256"],
                "result.provenance.extractor_sha256",
            ),
        )
        endpoint_values = self._legacy_array(root["endpoints"], "result.endpoints")
        endpoints = tuple(
            self._endpoint(value, index) for index, value in enumerate(endpoint_values)
        )
        summary = self._summary(root["execution_summary"])
        group_values = self._legacy_array(root["groups"], "result.groups")
        groups = tuple(
            self._group(value, index) for index, value in enumerate(group_values)
        )
        contract = self._legacy_mapping(
            root["analysis_contract"], "result.analysis_contract"
        )
        assessment = self._legacy_mapping(
            root["convergence_assessment"], "result.convergence_assessment"
        )
        return OptimizerStandaloneResult(
            schema_version=schema,
            provenance=provenance,
            endpoints=endpoints,
            summary=summary,
            groups=groups,
            basin_tolerance_control_status=self.decoder.nonempty_string(
                contract["basin_tolerance_control_status"],
                "result.analysis_contract.basin_tolerance_control_status",
            ),
            supports_declared_convergence=self.decoder.boolean(
                assessment["supports_declared_convergence"],
                "result.convergence_assessment.supports_declared_convergence",
            ),
            not_global_optimizer_convergence=self.decoder.boolean(
                assessment["not_global_optimizer_convergence"],
                "result.convergence_assessment.not_global_optimizer_convergence",
            ),
            not_general_wannier_convergence=self.decoder.boolean(
                assessment["not_general_wannier_convergence"],
                "result.convergence_assessment.not_general_wannier_convergence",
            ),
            convergence_disposition=self.decoder.nonempty_string(
                assessment["disposition"],
                "result.convergence_assessment.disposition",
            ),
        )

    def _endpoint(
        self, value: LegacyStandaloneJsonValue, index: int
    ) -> OptimizerStandaloneEndpoint:
        """Adapt one initial/continuation endpoint transition."""
        label = f"result.endpoints[{index}]"
        item = self._legacy_mapping(value, label)
        continuation_value = item["continuation_native_endpoint"]
        continuation = (
            None
            if continuation_value is None
            else self._native_endpoint(continuation_value, f"{label}.continuation")
        )
        continuation_converged_value = item["continuation_native_converged"]
        continuation_converged = (
            None
            if continuation_converged_value is None
            else self.decoder.boolean(
                continuation_converged_value,
                f"{label}.continuation_native_converged",
            )
        )
        return OptimizerStandaloneEndpoint(
            configuration_id=self.decoder.nonempty_string(
                item["configuration_id"], f"{label}.configuration_id"
            ),
            arm=self.decoder.nonempty_string(item["arm"], f"{label}.arm"),
            start_id=self.decoder.nonempty_string(
                item["start_id"], f"{label}.start_id"
            ),
            start_index=self.decoder.integer(
                item["start_index"], f"{label}.start_index"
            ),
            initial_process_completed=self.decoder.boolean(
                item["initial_process_completed"],
                f"{label}.initial_process_completed",
            ),
            initial_native_converged=self.decoder.boolean(
                item["initial_native_converged"],
                f"{label}.initial_native_converged",
            ),
            continuation_applied=self.decoder.boolean(
                item["continuation_applied"], f"{label}.continuation_applied"
            ),
            continuation_native_converged=continuation_converged,
            initial_native_endpoint=self._native_endpoint(
                item["initial_native_endpoint"], f"{label}.initial"
            ),
            continuation_native_endpoint=continuation,
            effective_native_converged=self.decoder.boolean(
                item["effective_native_converged"],
                f"{label}.effective_native_converged",
            ),
            effective_native_endpoint=self._native_endpoint(
                item["effective_native_endpoint"], f"{label}.effective"
            ),
            effective_total_iterations=self.decoder.integer(
                item["effective_total_iterations"],
                f"{label}.effective_total_iterations",
            ),
        )

    def _native_endpoint(
        self, value: LegacyStandaloneJsonValue, label: str
    ) -> OptimizerStandaloneNativeEndpoint:
        """Adapt every field in one retained native endpoint object."""
        item = self._legacy_mapping(value, label)
        center_values = self._legacy_array(item["centers"], f"{label}.centers")
        if len(center_values) != 3:
            raise ValueError(f"{label}.centers must contain three orbitals")
        centers: list[OptimizerStandaloneNativeCenter] = []
        for index, center_value in enumerate(center_values):
            center_label = f"{label}.centers[{index}]"
            center = self._legacy_mapping(center_value, center_label)
            centers.append(
                OptimizerStandaloneNativeCenter(
                    active_fractional=self._pair(
                        center["active_fractional"],
                        f"{center_label}.active_fractional",
                    ),
                    active_fractional_modulo_cell=self._pair(
                        center["active_fractional_modulo_cell"],
                        f"{center_label}.active_fractional_modulo_cell",
                    ),
                    orbital=self.decoder.integer(
                        center["orbital"], f"{center_label}.orbital"
                    ),
                )
            )
        if tuple(center.orbital for center in centers) != (0, 1, 2):
            raise ValueError(f"{label}.centers must retain orbital order 0, 1, 2")
        orbital_spreads = tuple(
            self.decoder.real(item_value, f"{label}.orbital_spreads_cell_squared")
            for item_value in self._legacy_array(
                item["orbital_spreads_cell_squared"],
                f"{label}.orbital_spreads_cell_squared",
            )
        )
        if len(orbital_spreads) != 3:
            raise ValueError(
                f"{label}.orbital_spreads_cell_squared must contain three values"
            )
        return OptimizerStandaloneNativeEndpoint(
            centers=tuple(centers),
            classification_status=self.decoder.nonempty_string(
                item["classification_status"], f"{label}.classification_status"
            ),
            diagnostic_classification=self.decoder.nonempty_string(
                item["diagnostic_classification"],
                f"{label}.diagnostic_classification",
            ),
            iterations=self.decoder.integer(item["iterations"], f"{label}.iterations"),
            omega_d_cell_squared=self.decoder.real(
                item["omega_d_cell_squared"], f"{label}.omega_d_cell_squared"
            ),
            omega_i_cell_squared=self.decoder.real(
                item["omega_i_cell_squared"], f"{label}.omega_i_cell_squared"
            ),
            omega_od_cell_squared=self.decoder.real(
                item["omega_od_cell_squared"], f"{label}.omega_od_cell_squared"
            ),
            omega_tilde_cell_squared=self.decoder.real(
                item["omega_tilde_cell_squared"],
                f"{label}.omega_tilde_cell_squared",
            ),
            omega_total_cell_squared=self.decoder.real(
                item["omega_total_cell_squared"],
                f"{label}.omega_total_cell_squared",
            ),
            orbital_spreads_cell_squared=orbital_spreads,
            terminal_detrended_spread_rms=self.decoder.real(
                item["terminal_detrended_spread_rms"],
                f"{label}.terminal_detrended_spread_rms",
            ),
            terminal_maximum_spread_cell_squared=self.decoder.real(
                item["terminal_maximum_spread_cell_squared"],
                f"{label}.terminal_maximum_spread_cell_squared",
            ),
            terminal_median_absolute_delta_spread=self.decoder.real(
                item["terminal_median_absolute_delta_spread"],
                f"{label}.terminal_median_absolute_delta_spread",
            ),
            terminal_median_rms_gradient=self.decoder.real(
                item["terminal_median_rms_gradient"],
                f"{label}.terminal_median_rms_gradient",
            ),
            terminal_minimum_spread_cell_squared=self.decoder.real(
                item["terminal_minimum_spread_cell_squared"],
                f"{label}.terminal_minimum_spread_cell_squared",
            ),
            terminal_spread_slope_per_iteration=self.decoder.real(
                item["terminal_spread_slope_per_iteration"],
                f"{label}.terminal_spread_slope_per_iteration",
            ),
            terminal_window_point_count=self.decoder.integer(
                item["terminal_window_point_count"],
                f"{label}.terminal_window_point_count",
            ),
            trace_point_count=self.decoder.integer(
                item["trace_point_count"], f"{label}.trace_point_count"
            ),
        )

    def _summary(
        self, value: LegacyStandaloneJsonValue
    ) -> OptimizerStandaloneExecutionSummary:
        """Adapt retained aggregate counts and diagnostic counts."""
        item = self._legacy_mapping(value, "result.execution_summary")
        diagnostics = self._legacy_mapping(
            item["effective_nonconvergence_diagnostic_counts"],
            "result.execution_summary.effective_nonconvergence_diagnostic_counts",
        )
        return OptimizerStandaloneExecutionSummary(
            initial_localization_count=self.decoder.integer(
                item["initial_localization_count"], "summary.initial_localization_count"
            ),
            initial_process_completion_count=self.decoder.integer(
                item["initial_process_completion_count"],
                "summary.initial_process_completion_count",
            ),
            initial_native_converged_count=self.decoder.integer(
                item["initial_native_converged_count"],
                "summary.initial_native_converged_count",
            ),
            continuation_count=self.decoder.integer(
                item["continuation_count"], "summary.continuation_count"
            ),
            continuation_native_converged_count=self.decoder.integer(
                item["continuation_native_converged_count"],
                "summary.continuation_native_converged_count",
            ),
            effective_native_converged_count=self.decoder.integer(
                item["effective_native_converged_count"],
                "summary.effective_native_converged_count",
            ),
            effective_native_nonconverged_count=self.decoder.integer(
                item["effective_native_nonconverged_count"],
                "summary.effective_native_nonconverged_count",
            ),
            diagnostic_counts=tuple(
                (
                    key,
                    self.decoder.integer(value_item, f"summary.diagnostics.{key}"),
                )
                for key, value_item in diagnostics.items()
            ),
        )

    def _group(
        self, value: LegacyStandaloneJsonValue, index: int
    ) -> OptimizerStandaloneGroup:
        """Adapt one retained group and its basin diagnostics."""
        label = f"result.groups[{index}]"
        item = self._legacy_mapping(value, label)
        best = self._legacy_mapping(
            item["best_observed_converged"], f"{label}.best_observed_converged"
        )
        basin_values = self._legacy_array(
            item["observed_density_d4_basins"],
            f"{label}.observed_density_d4_basins",
        )
        sensitivity_values = self._legacy_array(
            item["density_tolerance_sensitivity"],
            f"{label}.density_tolerance_sensitivity",
        )
        return OptimizerStandaloneGroup(
            configuration_id=self.decoder.nonempty_string(
                item["configuration_id"], f"{label}.configuration_id"
            ),
            arm=self.decoder.nonempty_string(item["arm"], f"{label}.arm"),
            initial_native_converged_count=self.decoder.integer(
                item["initial_native_converged_count"],
                f"{label}.initial_native_converged_count",
            ),
            effective_native_converged_count=self.decoder.integer(
                item["effective_native_converged_count"],
                f"{label}.effective_native_converged_count",
            ),
            effective_native_converged_fraction=self.decoder.real(
                item["effective_native_converged_fraction"],
                f"{label}.effective_native_converged_fraction",
            ),
            effective_nonconverged_start_ids=tuple(
                self.decoder.nonempty_string(start_id, f"{label}.nonconverged")
                for start_id in self._legacy_array(
                    item["effective_nonconverged_start_ids"],
                    f"{label}.effective_nonconverged_start_ids",
                )
            ),
            best_observed_start_id=self.decoder.nonempty_string(
                best["start_id"], f"{label}.best_observed_converged.start_id"
            ),
            declared_basin_count=self.decoder.integer(
                item["observed_density_d4_basin_count"],
                f"{label}.observed_density_d4_basin_count",
            ),
            basins=tuple(
                self._basin(basin, label, basin_index)
                for basin_index, basin in enumerate(basin_values)
            ),
            best_basin_criterion_pass=self.decoder.boolean(
                item["best_basin_criterion_pass"],
                f"{label}.best_basin_criterion_pass",
            ),
            sensitivity=tuple(
                self._sensitivity(record, label, record_index)
                for record_index, record in enumerate(sensitivity_values)
            ),
            controls=self._controls(item["basin_post_hoc_numerical_controls"], label),
        )

    def _basin(
        self, value: LegacyStandaloneJsonValue, group_label: str, index: int
    ) -> OptimizerStandaloneBasin:
        """Adapt one basin membership and rejected-candidate sequence."""
        label = f"{group_label}.basins[{index}]"
        item = self._legacy_mapping(value, label)
        member_values = self._legacy_array(
            item["member_equivalence_diagnostics"],
            f"{label}.member_equivalence_diagnostics",
        )
        members: list[OptimizerStandaloneMemberEquivalence] = []
        for member_index, member_value in enumerate(member_values):
            member_label = f"{label}.members[{member_index}]"
            member = self._legacy_mapping(member_value, member_label)
            members.append(
                OptimizerStandaloneMemberEquivalence(
                    start_id=self.decoder.nonempty_string(
                        member["start_id"], f"{member_label}.start_id"
                    ),
                    center_set_periodic_distance=self.decoder.real(
                        member["center_set_periodic_distance"],
                        f"{member_label}.center_set_periodic_distance",
                    ),
                    maximum_density_l2_mismatch=self.decoder.real(
                        member["maximum_density_l2_mismatch"],
                        f"{member_label}.maximum_density_l2_mismatch",
                    ),
                )
            )
        rejected_values = self._legacy_array(
            item["rejected_equivalence_candidates"],
            f"{label}.rejected_equivalence_candidates",
        )
        rejected: list[OptimizerStandaloneRejectedEquivalence] = []
        for rejected_index, rejected_value in enumerate(rejected_values):
            rejected_label = f"{label}.rejected[{rejected_index}]"
            candidate = self._legacy_mapping(rejected_value, rejected_label)
            rejected.append(
                OptimizerStandaloneRejectedEquivalence(
                    center_set_periodic_distance=self._nonnegative_extended_real(
                        candidate["center_set_periodic_distance"],
                        f"{rejected_label}.center_set_periodic_distance",
                    ),
                    maximum_density_l2_mismatch=self._nonnegative_extended_real(
                        candidate["maximum_density_l2_mismatch"],
                        f"{rejected_label}.maximum_density_l2_mismatch",
                    ),
                    representative_start_id=self.decoder.nonempty_string(
                        candidate["representative_start_id"],
                        f"{rejected_label}.representative_start_id",
                    ),
                )
            )
        return OptimizerStandaloneBasin(
            basin_id=self.decoder.nonempty_string(
                item["basin_id"], f"{label}.basin_id"
            ),
            representative_start_id=self.decoder.nonempty_string(
                item["representative_start_id"],
                f"{label}.representative_start_id",
            ),
            representative_omega_tilde_cell_squared=self.decoder.real(
                item["representative_omega_tilde_cell_squared"],
                f"{label}.representative_omega_tilde_cell_squared",
            ),
            start_ids=tuple(
                self.decoder.nonempty_string(start_id, f"{label}.start_ids")
                for start_id in self._legacy_array(
                    item["start_ids"], f"{label}.start_ids"
                )
            ),
            occupancy=self.decoder.integer(item["occupancy"], f"{label}.occupancy"),
            start_blocks_present=tuple(
                self.decoder.integer(block, f"{label}.start_blocks_present")
                for block in self._legacy_array(
                    item["start_blocks_present"], f"{label}.start_blocks_present"
                )
            ),
            appears_in_both_start_blocks=self.decoder.boolean(
                item["appears_in_both_start_blocks"],
                f"{label}.appears_in_both_start_blocks",
            ),
            member_equivalence_diagnostics=tuple(members),
            rejected_equivalence_candidates=tuple(rejected),
        )

    def _sensitivity(
        self, value: LegacyStandaloneJsonValue, group_label: str, index: int
    ) -> OptimizerStandaloneSensitivity:
        """Adapt one density-threshold sensitivity record."""
        label = f"{group_label}.sensitivity[{index}]"
        item = self._legacy_mapping(value, label)
        return OptimizerStandaloneSensitivity(
            density_l2_tolerance=self.decoder.real(
                item["density_l2_tolerance"], f"{label}.density_l2_tolerance"
            ),
            direct_matching_pair_count=self.decoder.integer(
                item["direct_matching_pair_count"],
                f"{label}.direct_matching_pair_count",
            ),
            best_endpoint_direct_match_start_ids=tuple(
                self.decoder.nonempty_string(start_id, f"{label}.match_start_ids")
                for start_id in self._legacy_array(
                    item["best_endpoint_direct_match_start_ids"],
                    f"{label}.best_endpoint_direct_match_start_ids",
                )
            ),
            best_endpoint_direct_occupancy=self.decoder.integer(
                item["best_endpoint_direct_occupancy"],
                f"{label}.best_endpoint_direct_occupancy",
            ),
        )

    def _controls(
        self, value: LegacyStandaloneJsonValue, group_label: str
    ) -> OptimizerStandaloneControls:
        """Adapt post-hoc numerical control records and declared maxima."""
        label = f"{group_label}.controls"
        item = self._legacy_mapping(value, label)
        record_values = self._legacy_array(item["records"], f"{label}.records")
        observations: list[OptimizerStandaloneControlObservation] = []
        for index, record_value in enumerate(record_values):
            record_label = f"{label}.records[{index}]"
            record = self._legacy_mapping(record_value, record_label)
            observations.append(
                OptimizerStandaloneControlObservation(
                    center_set_periodic_distance=self.decoder.real(
                        record["center_set_periodic_distance"],
                        f"{record_label}.center_set_periodic_distance",
                    ),
                    maximum_density_l2_mismatch=self.decoder.real(
                        record["maximum_density_l2_mismatch"],
                        f"{record_label}.maximum_density_l2_mismatch",
                    ),
                )
            )
        return OptimizerStandaloneControls(
            declared_count=self.decoder.integer(
                item["control_count"], f"{label}.control_count"
            ),
            maximum_center_distance=self.decoder.real(
                item["maximum_center_set_periodic_distance_cell"],
                f"{label}.maximum_center_set_periodic_distance_cell",
            ),
            maximum_density_mismatch=self.decoder.real(
                item["maximum_density_l2_mismatch"],
                f"{label}.maximum_density_l2_mismatch",
            ),
            passes_center_tolerance=self.decoder.boolean(
                item["passes_frozen_center_tolerance"],
                f"{label}.passes_frozen_center_tolerance",
            ),
            passes_density_tolerance=self.decoder.boolean(
                item["passes_frozen_density_tolerance"],
                f"{label}.passes_frozen_density_tolerance",
            ),
            observations=tuple(observations),
        )

    def _pair(
        self, value: LegacyStandaloneJsonValue, label: str
    ) -> tuple[float, float]:
        """Adapt one exact two-coordinate finite binary64 vector."""
        values = self._legacy_array(value, label)
        coordinates = tuple(self.decoder.real(item, label) for item in values)
        if len(coordinates) != 2:
            raise ValueError(f"{label} must contain two coordinates")
        return coordinates[0], coordinates[1]

    def _nonnegative_extended_real(
        self, value: LegacyStandaloneJsonValue, label: str
    ) -> float:
        """Adapt one nonnegative finite or positive-infinite binary64 value."""
        if type(value) is int:
            result = float(value)
        elif type(value) is float:
            result = value
        else:
            raise TypeError(f"{label} must be an extended real")
        if math.isnan(result) or result < 0.0:
            raise ValueError(f"{label} must be nonnegative and not NaN")
        return result

    def _mapping(self, value: JsonValue, label: str) -> dict[str, JsonValue]:
        """Require one strict-decoded object without copying it again."""
        if type(value) is not dict:
            raise TypeError(f"{label} must be a JSON object")
        return value

    def _array(self, value: JsonValue, label: str) -> list[JsonValue]:
        """Require one strict-decoded array without copying it again."""
        if type(value) is not list:
            raise TypeError(f"{label} must be a JSON array")
        return value

    def _legacy_mapping(
        self, value: LegacyStandaloneJsonValue, label: str
    ) -> dict[str, LegacyStandaloneJsonValue]:
        """Require one historical object during bounded adaptation."""
        if type(value) is not dict:
            raise TypeError(f"{label} must be a JSON object")
        return value

    def _legacy_array(
        self, value: LegacyStandaloneJsonValue, label: str
    ) -> list[LegacyStandaloneJsonValue]:
        """Require one historical array during bounded adaptation."""
        if type(value) is not list:
            raise TypeError(f"{label} must be a JSON array")
        return value

    def _require_schema(self, schema: int, label: str) -> None:
        """Require the sole retained schema version before adaptation."""
        if schema != _SCHEMA_VERSION:
            raise AssertionError(f"{label} schema changed")
