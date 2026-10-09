"""Version-one wire adaptation for periodic-1D blind alignment."""

from __future__ import annotations

from typing import cast

import numpy as np

from ksdft2effmass.periodic1d.campaign.serialization import (
    Periodic1DCampaignJsonDecoder,
)
from ksdft2effmass.serialization.json import JsonValue

from .input_records import (
    BlindAlignmentCampaignInput,
    BlindAlignmentDiagnosticControls,
    BlindAlignmentExactCase,
    BlindAlignmentGaugeCase,
    BlindAlignmentNoiseSweep,
    BlindAlignmentObservationInformationContract,
    BlindAlignmentSourceIdentity,
    BlindAlignmentStopKind,
    BlindAlignmentStoppingCase,
)
from .records import BlindAlignmentInferencePolicy


class BlindAlignmentInputDeserializer:
    """Deserialize the exact closed version-one campaign input.

    ``execute`` accepts UTF-8 JSON bytes and rejects unsupported versions, missing or
    additional fields, booleans in numeric positions, numeric strings, nonfinite
    values, and invalid cross-field records.  Successful decoding establishes only
    the wire and intrinsic input contract; it does not authenticate referenced files
    or establish numerical or scientific correctness.
    """

    __slots__ = ("_decoder",)

    def __init__(self) -> None:
        """Bind the maintained strict campaign JSON decoder."""
        self._decoder = Periodic1DCampaignJsonDecoder()

    def execute(self, payload: bytes) -> BlindAlignmentCampaignInput:
        """Decode one version-one campaign input.

        Parameters
        ----------
        payload
            UTF-8 JSON bytes.

        Returns
        -------
        BlindAlignmentCampaignInput
            Immutable typed campaign controls.

        Raises
        ------
        TypeError
            If a represented field has the wrong semantic type.
        ValueError
            If JSON, schema version, field inventory, finiteness, or an intrinsic
            invariant is invalid.
        """
        if type(payload) is not bytes:
            raise TypeError("payload must be bytes")
        root = self._mapping(self._decoder.document(payload), "input")
        self._fields(
            root,
            (
                "schema_version",
                "experiment_id",
                "evidence_status",
                "baseline_sources",
                "observation_information_contract",
                "inference_policy",
                "exact_cases",
                "noise_sweep",
                "gauge_equivalent_case",
                "debugging_diagnostics",
                "stopping_cases",
                "algebraic_tolerance",
            ),
            "input",
        )
        if self._integer(root["schema_version"], "schema_version") != 1:
            raise ValueError("unsupported input schema version")
        if self._string(root["evidence_status"], "evidence_status") != (
            "synthetic test data"
        ):
            raise ValueError("evidence_status must identify synthetic test data")
        sources = self._mapping(root["baseline_sources"], "baseline_sources")
        self._fields(
            sources,
            ("input_path", "input_sha256", "result_path", "result_sha256"),
            "baseline_sources",
        )
        information = self._mapping(
            root["observation_information_contract"],
            "observation_information_contract",
        )
        self._fields(
            information,
            (
                "anchor_cross_covariance",
                "site_anchor_labels",
                "orbital_labels",
                "spin_frame",
                "energy_reference",
            ),
            "observation_information_contract",
        )
        policy = self._mapping(root["inference_policy"], "inference_policy")
        self._fields(
            policy,
            (
                "anchor_rank_tolerance",
                "maximum_anchor_condition_number",
                "maximum_principal_angle_radians",
                "minimum_energy_anchor_rank",
                "core_radius_cells",
            ),
            "inference_policy",
        )
        exact_cases = tuple(
            self._exact_case(item)
            for item in self._records(root["exact_cases"], "exact_cases")
        )
        noise = self._noise_sweep(root["noise_sweep"])
        gauge = self._gauge_case(root["gauge_equivalent_case"])
        diagnostics = self._diagnostics(root["debugging_diagnostics"])
        stopping_cases = tuple(
            self._stopping_case(item)
            for item in self._records(root["stopping_cases"], "stopping_cases")
        )
        return BlindAlignmentCampaignInput(
            experiment_id=self._string(root["experiment_id"], "experiment_id"),
            baseline_input=BlindAlignmentSourceIdentity(
                self._string(sources["input_path"], "baseline input path"),
                self._string(sources["input_sha256"], "baseline input SHA-256"),
            ),
            baseline_result=BlindAlignmentSourceIdentity(
                self._string(sources["result_path"], "baseline result path"),
                self._string(sources["result_sha256"], "baseline result SHA-256"),
            ),
            observation_information=BlindAlignmentObservationInformationContract(
                self._string(
                    information["anchor_cross_covariance"],
                    "anchor cross-covariance information",
                ),
                self._string(
                    information["site_anchor_labels"], "site-anchor information"
                ),
                self._string(information["orbital_labels"], "orbital information"),
                self._string(information["spin_frame"], "spin-frame information"),
                self._string(
                    information["energy_reference"], "energy-reference information"
                ),
            ),
            policy=BlindAlignmentInferencePolicy(
                self._real(policy["anchor_rank_tolerance"], "anchor rank tolerance"),
                self._real(
                    policy["maximum_anchor_condition_number"],
                    "maximum anchor condition number",
                ),
                self._real(
                    policy["maximum_principal_angle_radians"],
                    "maximum principal angle",
                ),
                self._integer(
                    policy["minimum_energy_anchor_rank"],
                    "minimum energy-anchor rank",
                ),
            ),
            core_radius_cells=self._integer(policy["core_radius_cells"], "core radius"),
            exact_cases=exact_cases,
            noise_sweep=noise,
            gauge_case=gauge,
            stopping_cases=stopping_cases,
            diagnostics=diagnostics,
            algebraic_tolerance=self._real(
                root["algebraic_tolerance"], "algebraic tolerance"
            ),
        )

    def _exact_case(self, value: JsonValue) -> BlindAlignmentExactCase:
        """Decode one closed exact full-rank case record."""
        record = self._mapping(value, "exact case")
        self._fields(
            record,
            ("id", "defect_id", "spin_count", "minimum_anchor_singular_value"),
            "exact case",
        )
        return BlindAlignmentExactCase(
            self._string(record["id"], "exact case id"),
            self._string(record["defect_id"], "exact defect id"),
            self._integer(record["spin_count"], "exact spin count"),
            self._real(
                record["minimum_anchor_singular_value"],
                "exact minimum anchor singular value",
            ),
        )

    def _noise_sweep(self, value: JsonValue) -> BlindAlignmentNoiseSweep:
        """Decode the closed deterministic anchor-noise sequence."""
        record = self._mapping(value, "noise_sweep")
        self._fields(
            record,
            (
                "id",
                "defect_id",
                "spin_count",
                "minimum_anchor_singular_value",
                "unitary_noise_radians",
                "generator_seed",
            ),
            "noise_sweep",
        )
        return BlindAlignmentNoiseSweep(
            self._string(record["id"], "noise id"),
            self._string(record["defect_id"], "noise defect id"),
            self._integer(record["spin_count"], "noise spin count"),
            self._real(
                record["minimum_anchor_singular_value"],
                "noise minimum anchor singular value",
            ),
            self._reals(record["unitary_noise_radians"], "unitary noise radians"),
            self._integer(record["generator_seed"], "noise generator seed"),
        )

    def _gauge_case(self, value: JsonValue) -> BlindAlignmentGaugeCase:
        """Decode the closed undercomplete gauge-equivalent case."""
        record = self._mapping(value, "gauge_equivalent_case")
        self._fields(
            record,
            (
                "id",
                "defect_id",
                "spin_count",
                "identified_site_count",
                "minimum_nonzero_anchor_singular_value",
                "complement_rotation_radians",
                "generator_seed",
            ),
            "gauge_equivalent_case",
        )
        return BlindAlignmentGaugeCase(
            self._string(record["id"], "gauge id"),
            self._string(record["defect_id"], "gauge defect id"),
            self._integer(record["spin_count"], "gauge spin count"),
            self._integer(record["identified_site_count"], "identified site count"),
            self._real(
                record["minimum_nonzero_anchor_singular_value"],
                "minimum nonzero anchor singular value",
            ),
            self._real(record["complement_rotation_radians"], "complement rotation"),
            self._integer(record["generator_seed"], "gauge generator seed"),
        )

    def _diagnostics(self, value: JsonValue) -> BlindAlignmentDiagnosticControls:
        """Decode all neighboring stopping-boundary probe controls."""
        record = self._mapping(value, "debugging_diagnostics")
        self._fields(
            record,
            (
                "conditioning_minimum_singular_values",
                "conditioning_additive_anchor_noise",
                "conditioning_noise_seed",
                "principal_angle_radians",
                "rank_drop",
                "energy_anchor_ranks",
            ),
            "debugging_diagnostics",
        )
        return BlindAlignmentDiagnosticControls(
            self._reals(
                record["conditioning_minimum_singular_values"],
                "conditioning minimum singular values",
            ),
            self._real(
                record["conditioning_additive_anchor_noise"],
                "conditioning additive anchor noise",
            ),
            self._integer(record["conditioning_noise_seed"], "conditioning noise seed"),
            self._reals(record["principal_angle_radians"], "principal angles"),
            self._integer(record["rank_drop"], "rank drop"),
            self._integers(record["energy_anchor_ranks"], "energy-anchor ranks"),
        )

    def _stopping_case(self, value: JsonValue) -> BlindAlignmentStoppingCase:
        """Decode one kind-specific structured-stop case."""
        record = self._mapping(value, "stopping case")
        common = {"id", "kind"}
        kind = self._string(record["kind"], "stopping kind")
        key_by_kind = {
            "anchor-condition": "minimum_anchor_singular_value",
            "principal-angle": "maximum_principal_angle_radians",
            "rank-mismatch": "candidate_dimension_delta",
            "spin-mismatch": "candidate_spin_count",
            "energy-anchor": None,
        }
        if kind not in key_by_kind:
            raise ValueError("unsupported stopping-case kind")
        numeric_key = key_by_kind[kind]
        expected = common if numeric_key is None else common | {numeric_key}
        self._fields(record, tuple(sorted(expected)), "stopping case")
        numeric: float | int | None = None
        if numeric_key is not None:
            numeric = (
                self._integer(record[numeric_key], numeric_key)
                if kind in ("rank-mismatch", "spin-mismatch")
                else self._real(record[numeric_key], numeric_key)
            )
        return BlindAlignmentStoppingCase(
            self._string(record["id"], "stopping id"),
            cast(BlindAlignmentStopKind, kind),
            numeric,
        )

    @staticmethod
    def _fields(
        record: dict[str, JsonValue], expected: tuple[str, ...], name: str
    ) -> None:
        """Require an exact closed JSON-object field inventory."""
        actual = set(record)
        required = set(expected)
        if actual != required:
            missing = ", ".join(sorted(required - actual)) or "none"
            additional = ", ".join(sorted(actual - required)) or "none"
            message = (
                f"{name} fields are invalid; missing: {missing}; "
                f"additional: {additional}"
            )
            raise ValueError(message)

    @staticmethod
    def _mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        """Require one JSON object with built-in string keys."""
        if not isinstance(value, dict) or any(type(key) is not str for key in value):
            raise TypeError(f"{name} must be a JSON object with string keys")
        return value

    def _records(self, value: JsonValue, name: str) -> tuple[dict[str, JsonValue], ...]:
        """Require one JSON array containing only object records."""
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return tuple(self._mapping(item, name) for item in value)

    @staticmethod
    def _string(value: JsonValue, name: str) -> str:
        """Require one nonempty built-in string."""
        if type(value) is not str:
            raise TypeError(f"{name} must be a string")
        if not value:
            raise ValueError(f"{name} must be nonempty")
        return value

    @staticmethod
    def _integer(value: JsonValue, name: str) -> int:
        """Require one built-in integer while rejecting booleans."""
        if type(value) is not int:
            raise TypeError(f"{name} must be an integer")
        return value

    @staticmethod
    def _real(value: JsonValue, name: str) -> float:
        """Convert one finite JSON number to binary64 while rejecting booleans."""
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be a real number")
        converted = float(value)
        if not np.isfinite(converted):
            raise ValueError(f"{name} must be finite")
        return converted

    def _reals(self, value: JsonValue, name: str) -> tuple[float, ...]:
        """Decode one JSON array of finite binary64 values."""
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return tuple(self._real(item, name) for item in value)

    def _integers(self, value: JsonValue, name: str) -> tuple[int, ...]:
        """Decode one JSON array of built-in integers."""
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return tuple(self._integer(item, name) for item in value)
