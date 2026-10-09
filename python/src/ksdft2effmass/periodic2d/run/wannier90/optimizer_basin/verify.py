"""Repository-portable verification of the optimizer-basin study."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from ksdft2effmass.serialization.json import JsonValue, StrictJsonDecoder

from .encoded_documents import Periodic2DOptimizerBasinEncodedDocuments

_CONFIGURATION_COUNT = 9
_INITIAL_GAUGE_COUNT = 8
_STUDY_EVIDENCE_STATUS = "authorized synthetic non-DFT study input"
_RESULT_EVIDENCE_STATUS = "calculated synthetic non-DFT numerical verification"
_NEGATIVE_DISPOSITION = (
    "does not support the frozen finite-parameter convergence criteria"
)


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerBasinCampaignVerificationRequest:
    """Request portable verification of one retained optimizer-basin study.

    Parameters
    ----------
    encoded_documents
        Exact retained input and result wires owned by the optimizer-basin campaign.
    repository_root
        Absolute repository root used only to authenticate directly declared compact
        source files. The verifier does not search for or access the external native-run
        directory.

    Raises
    ------
    TypeError
        If either argument has the wrong exact contract type.
    ValueError
        If ``repository_root`` is not absolute.
    """

    encoded_documents: Periodic2DOptimizerBasinEncodedDocuments
    repository_root: Path

    def __post_init__(self) -> None:
        """Validate exact document ownership and an absolute repository root."""
        if type(self.encoded_documents) is not Periodic2DOptimizerBasinEncodedDocuments:
            raise TypeError(
                "encoded_documents must be Periodic2DOptimizerBasinEncodedDocuments"
            )
        if not isinstance(self.repository_root, Path):
            raise TypeError("repository_root must be pathlib.Path")
        if not self.repository_root.is_absolute():
            raise ValueError("repository_root must be absolute")


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerBasinCampaignVerificationResult:
    """Report bounded compact-source and structural reconstruction outcomes.

    Parameters
    ----------
    source_authentication_passed
        Exact Boolean result of directly declared compact-source authentication.
    structural_reconstruction_passed
        Exact Boolean result of endpoint, basin, count, and negative-gate checks.
    configuration_count
        Nonnegative exact built-in integer number of correlated configurations.
    converged_count
        Nonnegative exact built-in integer number of native-converged endpoints.
    nonconverged_count
        Nonnegative exact built-in integer number of retained nonconverged endpoints.
    retained_result_sha256
        Lowercase SHA-256 identity of the exact encoded result wire.

    Raises
    ------
    TypeError
        If a flag is not an exact built-in Boolean, a count is not an exact built-in
        integer, or the digest is not a string.
    ValueError
        If a count is negative or the digest is not lowercase SHA-256 hexadecimal.

    Notes
    -----
    A passing Action-produced result establishes authenticated compact-source identity
    and internal consistency of counts, basin partitions, and retained negative
    occupancy gates. Constructing this DataObject directly validates intrinsic state but
    does not prove that the verifier Action executed. The result does not authenticate
    the external native tree, rerun Wannier90, prove a global optimum, establish
    numerical convergence, or record scientific acceptance.
    """

    source_authentication_passed: bool
    structural_reconstruction_passed: bool
    configuration_count: int
    converged_count: int
    nonconverged_count: int
    retained_result_sha256: str

    def __post_init__(self) -> None:
        """Validate exact intrinsic result representations and value ranges."""
        self._check_args_flags()
        self._check_args_counts()
        self._check_args_digest()

    def _check_args_flags(self) -> None:
        """Require exact built-in Boolean pass indicators."""
        for name, value in (
            ("source_authentication_passed", self.source_authentication_passed),
            ("structural_reconstruction_passed", self.structural_reconstruction_passed),
        ):
            if type(value) is not bool:
                raise TypeError(f"{name} must be a built-in bool")

    def _check_args_counts(self) -> None:
        """Require nonnegative exact built-in endpoint and configuration counts."""
        for name, value in (
            ("configuration_count", self.configuration_count),
            ("converged_count", self.converged_count),
            ("nonconverged_count", self.nonconverged_count),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be an integer")
            if value < 0:
                raise ValueError(f"{name} must be nonnegative")

    def _check_args_digest(self) -> None:
        """Require one exact lowercase SHA-256 wire identity."""
        StrictJsonDecoder().sha256(
            self.retained_result_sha256, "retained_result_sha256"
        )

    @property
    def passes(self) -> bool:
        """Return the conjunction of the two bounded pass indicators."""
        return (
            self.source_authentication_passed and self.structural_reconstruction_passed
        )


class Periodic2DOptimizerBasinCampaignVerifier:
    """Reconstruct compact endpoint, basin, count, and negative-gate evidence.

    The verifier correlates declared configurations and deterministic gauge identities,
    partitions encoded native-converged endpoints into the retained observed basins,
    reconstructs aggregate counts and best-observed endpoints, and fails closed if the
    retained negative convergence disposition is promoted. It performs no optimization,
    native-file discovery, global-minimum search, uncertainty analysis, or scientific
    acceptance decision.
    """

    __slots__ = ("_decoder",)

    def __init__(self) -> None:
        """Create one verifier with a private strict JSON wire decoder."""
        self._decoder = StrictJsonDecoder()

    def execute(
        self, request: Periodic2DOptimizerBasinCampaignVerificationRequest
    ) -> Periodic2DOptimizerBasinCampaignVerificationResult:
        """Authenticate compact sources and reconstruct retained structural evidence.

        Parameters
        ----------
        request
            Exact encoded documents and an absolute repository root.

        Returns
        -------
        Periodic2DOptimizerBasinCampaignVerificationResult
            Counts and bounded pass indicators after all checks succeed.

        Raises
        ------
        TypeError
            If decoded values have representations inconsistent with the retained
            schema.
        ValueError
            If either document is invalid strict UTF-8 JSON, repeats an object key,
            contains a nonstandard nonfinite constant or nonfinite decoded real, or
            declares a compact source resolving outside ``repository_root``.
        OverflowError
            If a required integer real lies outside the binary64 range.
        KeyError
            If a required retained-schema field is absent.
        OSError
            If a confined, directly declared compact repository source cannot be read.
        MemoryError
            If Python cannot allocate a decoded document representation.
        RecursionError
            If a document exceeds parser or validator recursion depth.
        AssertionError
            If identities, declarations, counts, basin partitions, best endpoints, or
            frozen negative dispositions disagree.

        Notes
        -----
        The method reconstructs compact-document consistency only. Native Wannier90
        output and historical process execution remain outside this portable route.
        """
        # Strict shared decoding rejects ambiguous duplicate keys and nonstandard
        # constants before any campaign field can influence verification.
        study = self._decoder.document(request.encoded_documents.input_payload)
        result = self._decoder.document(request.encoded_documents.result_payload)
        self._equal(self._integer(study["schema_version"]), 1, "study schema")
        self._equal(self._integer(result["schema_version"]), 1, "result schema")
        self._verify_campaign_metadata(study, result)
        self._authenticate_sources(request, result)
        declared, gauge_ids = self._study_declarations(study)
        configurations, by_id, converged_total, nonconverged_total = (
            self._verify_configurations(result, declared, gauge_ids)
        )
        self._verify_execution_summary(
            result, len(configurations), converged_total, nonconverged_total
        )
        self._verify_negative_disposition(result, by_id, study, declared)
        return Periodic2DOptimizerBasinCampaignVerificationResult(
            True,
            True,
            len(configurations),
            converged_total,
            nonconverged_total,
            hashlib.sha256(request.encoded_documents.result_payload).hexdigest(),
        )

    def _verify_campaign_metadata(
        self,
        study: dict[str, JsonValue],
        result: dict[str, JsonValue],
    ) -> None:
        """Correlate identity/claim metadata and preserve distinct evidence roles."""
        for key in ("experiment_id", "authorization_checkpoint", "claim_boundary"):
            if self._string(result[key]) != self._string(study[key]):
                raise AssertionError(f"campaign {key} disagrees")
        expected_statuses = (_STUDY_EVIDENCE_STATUS, _RESULT_EVIDENCE_STATUS)
        actual_statuses = (
            self._string(study["evidence_status"]),
            self._string(result["evidence_status"]),
        )
        if actual_statuses != expected_statuses:
            raise AssertionError("campaign evidence statuses disagree")

    def _authenticate_sources(
        self,
        request: Periodic2DOptimizerBasinCampaignVerificationRequest,
        result: dict[str, JsonValue],
    ) -> None:
        """Authenticate the input wire and directly declared compact sources."""
        provenance = self._mapping(result["provenance"])
        self._content_identity(
            request.encoded_documents.input_payload,
            self._sha256(provenance["study_input_sha256"]),
            "study input",
        )
        for path_key, digest_key in (
            ("extractor_path", "extractor_sha256"),
            ("base_extractor_path", "base_extractor_sha256"),
        ):
            path = self._repository_source(
                request.repository_root,
                self._string(provenance[path_key]),
                path_key,
            )
            expected_digest = self._sha256(provenance[digest_key])
            self._content_identity(path.read_bytes(), expected_digest, path_key)

    def _study_declarations(
        self, study: dict[str, JsonValue]
    ) -> tuple[dict[str, dict[str, JsonValue]], tuple[str, ...]]:
        """Return exact unique configuration and initial-gauge declarations."""
        configurations = self._records(study["configurations"])
        configuration_ids = tuple(
            self._string(item["configuration_id"]) for item in configurations
        )
        if len(configurations) != _CONFIGURATION_COUNT or len(configuration_ids) != len(
            set(configuration_ids)
        ):
            raise AssertionError("expected nine unique declared configurations")
        declared = dict(zip(configuration_ids, configurations, strict=True))
        gauge_ids = tuple(
            self._string(item["gauge_id"])
            for item in self._records(study["initial_gauges"])
        )
        if len(gauge_ids) != _INITIAL_GAUGE_COUNT or len(set(gauge_ids)) != len(
            gauge_ids
        ):
            raise AssertionError("expected eight unique deterministic gauges")
        return declared, gauge_ids

    def _verify_configurations(
        self,
        result: dict[str, JsonValue],
        declared: dict[str, dict[str, JsonValue]],
        gauge_ids: tuple[str, ...],
    ) -> tuple[list[dict[str, JsonValue]], dict[str, dict[str, JsonValue]], int, int]:
        """Verify unique result configurations and accumulate endpoint counts."""
        configurations = self._records(result["configurations"])
        configuration_ids = tuple(
            self._string(item["configuration_id"]) for item in configurations
        )
        if len(configurations) != _CONFIGURATION_COUNT or len(configuration_ids) != len(
            set(configuration_ids)
        ):
            raise AssertionError("expected nine unique result configurations")
        if set(declared) != set(configuration_ids):
            raise AssertionError("configuration identities disagree")
        by_id = dict(zip(configuration_ids, configurations, strict=True))
        converged_total = 0
        nonconverged_total = 0
        for identifier, configuration in by_id.items():
            converged_count, nonconverged_count = self._verify_configuration(
                configuration, declared[identifier], gauge_ids, identifier
            )
            converged_total += converged_count
            nonconverged_total += nonconverged_count
        return configurations, by_id, converged_total, nonconverged_total

    def _verify_configuration(
        self,
        configuration: dict[str, JsonValue],
        expected: dict[str, JsonValue],
        gauge_ids: tuple[str, ...],
        identifier: str,
    ) -> tuple[int, int]:
        """Verify one configuration and return converged/nonconverged counts."""
        if not self._same_json_value(
            configuration["study_axes"], expected["study_axes"]
        ):
            raise AssertionError(f"{identifier}: study axes disagree")
        for key in ("plane_wave_cutoff", "reciprocal_mesh_size"):
            self._equal(
                self._integer(configuration[key]),
                self._integer(expected[key]),
                f"{identifier}:{key}",
            )
        self._close(
            self._real(configuration["transverse_lattice_length"]),
            self._real(expected["transverse_lattice_length"]),
            0.0,
            f"{identifier}:embedding",
        )
        starts = self._records(configuration["starts"])
        start_ids = tuple(self._string(item["gauge_id"]) for item in starts)
        if len(starts) != len(gauge_ids):
            raise AssertionError(f"{identifier}: expected exactly eight starts")
        if len(start_ids) != len(set(start_ids)):
            raise AssertionError(f"{identifier}: duplicate start gauge identity")
        if set(start_ids) != set(gauge_ids):
            raise AssertionError(f"{identifier}: gauge identities disagree")
        if not all(self._boolean(item["completed"]) for item in starts):
            raise AssertionError(f"{identifier}: incomplete endpoint")
        # Process completion and native localization convergence are distinct.
        converged = [
            item
            for item in starts
            if self._boolean(item["convergence_criterion_satisfied"])
        ]
        nonconverged = [
            item
            for item in starts
            if not self._boolean(item["convergence_criterion_satisfied"])
        ]
        if not converged:
            raise AssertionError(f"{identifier}: no converged endpoint")
        self._equal(
            self._integer(configuration["converged_start_count"]),
            len(converged),
            f"{identifier}:converged count",
        )
        retained_nonconverged = tuple(
            self._string(value)
            for value in self._array(configuration["nonconverged_gauge_ids"])
        )
        if len(retained_nonconverged) != len(set(retained_nonconverged)):
            raise AssertionError(f"{identifier}: duplicate nonconverged gauge identity")
        if set(retained_nonconverged) != {
            self._string(item["gauge_id"]) for item in nonconverged
        }:
            raise AssertionError(f"{identifier}: nonconverged identities disagree")
        self._verify_basins(configuration, converged, identifier)
        if not self._boolean(configuration["best_is_observed_not_proven_global"]):
            raise AssertionError(f"{identifier}: global-optimum claim boundary changed")
        # "Best" is restricted to declared, native-converged starts; it is not a
        # claim of global optimality over all possible gauges.
        best = min(
            converged,
            key=lambda item: self._real(item["native_total_spread_cell_squared"]),
        )
        retained_best = self._mapping(configuration["best_observed_converged"])
        if not self._same_json_value(retained_best, best):
            raise AssertionError(f"{identifier}: best observed endpoint disagrees")
        return len(converged), len(nonconverged)

    def _verify_execution_summary(
        self,
        result: dict[str, JsonValue],
        configuration_count: int,
        converged_count: int,
        nonconverged_count: int,
    ) -> None:
        """Correlate aggregate retained counts with reconstructed endpoint counts."""
        summary = self._mapping(result["execution_summary"])
        if not self._boolean(summary["all_localization_processes_completed"]):
            raise AssertionError("aggregate process-completion disposition disagrees")
        self._equal(
            self._integer(summary["configuration_count"]),
            configuration_count,
            "configuration count",
        )
        self._equal(
            self._integer(summary["localization_count"]),
            converged_count + nonconverged_count,
            "localization count",
        )
        self._equal(
            self._integer(summary["converged_localization_count"]),
            converged_count,
            "converged count",
        )
        self._equal(
            self._integer(summary["nonconverged_localization_count"]),
            nonconverged_count,
            "nonconverged count",
        )

    def _verify_basins(
        self,
        configuration: dict[str, JsonValue],
        converged: list[dict[str, JsonValue]],
        identifier: str,
    ) -> None:
        """Verify that retained observed basins partition converged starts exactly.

        Basin membership is accepted only for encoded native-converged endpoints. The
        routine checks occupancy arithmetic, representative membership, uniqueness,
        completeness, and the retained basin count. It does not independently recompute
        spread or periodic-center distances and does not prove distinct stationary
        points.
        """
        basins = self._records(configuration["observed_converged_basins"])
        members: list[str] = []
        for basin in basins:
            gauge_ids = [
                self._string(value) for value in self._array(basin["gauge_ids"])
            ]
            self._equal(
                self._integer(basin["occupancy"]),
                len(gauge_ids),
                f"{identifier}:basin occupancy",
            )
            if self._string(basin["representative_gauge_id"]) not in gauge_ids:
                raise AssertionError(f"{identifier}: basin representative absent")
            members.extend(gauge_ids)
        expected = sorted(self._string(item["gauge_id"]) for item in converged)
        if sorted(members) != expected or len(members) != len(set(members)):
            raise AssertionError(f"{identifier}: basin partition disagrees")
        self._equal(
            self._integer(configuration["observed_converged_basin_count"]),
            len(basins),
            f"{identifier}:basin count",
        )

    def _verify_negative_disposition(
        self,
        result: dict[str, JsonValue],
        by_id: dict[str, dict[str, JsonValue]],
        study: dict[str, JsonValue],
        declared: dict[str, dict[str, JsonValue]],
    ) -> None:
        """Preserve and reconstruct the frozen negative occupancy dispositions.

        The method recomputes best-basin occupancy for the declared finest mesh and
        cutoff pairs and rejects any promotion to supporting convergence. Other frozen
        numerical gates remain encoded evidence owned by the broader retained verifier.
        """
        assessment = self._mapping(result["convergence_assessment"])
        if not self._boolean(assessment["not_a_global_or_general_claim"]):
            raise AssertionError("global/general claim boundary changed")
        if self._boolean(assessment["supports_declared_convergence"]):
            raise AssertionError("retained negative convergence disposition changed")
        if self._string(assessment["disposition"]) != _NEGATIVE_DISPOSITION:
            raise AssertionError("retained negative disposition text changed")
        method = self._mapping(study["convergence_method"])
        if not self._boolean(method["require_both_best_and_median_stability"]):
            raise AssertionError("best-and-median stability requirement changed")
        required = self._integer(method["minimum_repeated_best_basin_occupancy"])
        pair_definitions = (
            ("mesh_finest_pair", "mesh", "reciprocal_mesh_size"),
            ("cutoff_finest_pair", "cutoff", "plane_wave_cutoff"),
        )
        for key, axis, control_key in pair_definitions:
            pair = self._mapping(assessment[key])
            expected_ids = self._declared_pair_ids(
                method, declared, key, axis, control_key
            )
            actual_ids = (
                self._string(pair["lower_configuration_id"]),
                self._string(pair["upper_configuration_id"]),
            )
            if actual_ids != expected_ids:
                raise AssertionError(f"{key}: configuration identities disagree")
            lower = by_id[actual_ids[0]]
            upper = by_id[actual_ids[1]]
            occupancy = min(
                self._best_basin_occupancy(lower), self._best_basin_occupancy(upper)
            )
            self._equal(
                self._integer(pair["minimum_endpoint_best_basin_occupancy"]),
                occupancy,
                f"{key}:occupancy",
            )
            if self._boolean(pair["occupancy_pass"]) != (occupancy >= required):
                raise AssertionError(f"{key}: occupancy disposition disagrees")
            if self._boolean(pair["supporting"]):
                raise AssertionError(f"{key}: unsupported convergence promotion")
        self._verify_embedding_sensitivity(assessment, by_id, declared)

    def _declared_pair_ids(
        self,
        method: dict[str, JsonValue],
        declared: dict[str, dict[str, JsonValue]],
        pair_key: str,
        axis: str,
        control_key: str,
    ) -> tuple[str, str]:
        """Resolve one declared ordered finest pair from axes and exact controls."""
        controls = self._decoder.integers(method[pair_key], pair_key)
        if len(controls) != 2 or len(set(controls)) != 2:
            raise AssertionError(f"{pair_key}: expected two unique controls")
        identifiers: list[str] = []
        for control in controls:
            matches = [
                identifier
                for identifier, configuration in declared.items()
                if axis
                in {
                    self._string(value)
                    for value in self._array(configuration["study_axes"])
                }
                and self._integer(configuration[control_key]) == control
            ]
            if len(matches) != 1:
                raise AssertionError(f"{pair_key}: control identity is not unique")
            identifiers.append(matches[0])
        return identifiers[0], identifiers[1]

    def _verify_embedding_sensitivity(
        self,
        assessment: dict[str, JsonValue],
        by_id: dict[str, dict[str, JsonValue]],
        declared: dict[str, dict[str, JsonValue]],
    ) -> None:
        """Correlate retained embedding summaries with their configuration records."""
        expected_ids = {
            identifier
            for identifier, configuration in declared.items()
            if {
                self._string(value)
                for value in self._array(configuration["study_axes"])
            }
            & {"embedding", "embedding_reference"}
        }
        summaries = self._records(assessment["embedding_sensitivity"])
        summary_ids = tuple(
            self._string(summary["configuration_id"]) for summary in summaries
        )
        if (
            len(summary_ids) != len(set(summary_ids))
            or set(summary_ids) != expected_ids
        ):
            raise AssertionError("embedding sensitivity identities disagree")
        for summary in summaries:
            identifier = self._string(summary["configuration_id"])
            configuration = by_id[identifier]
            for key in (
                "best_observed_converged",
                "median_across_converged_starts",
                "observed_converged_basin_count",
                "transverse_lattice_length",
            ):
                if not self._same_json_value(summary[key], configuration[key]):
                    raise AssertionError(
                        f"{identifier}: embedding sensitivity {key} disagrees"
                    )

    def _best_basin_occupancy(self, configuration: dict[str, JsonValue]) -> int:
        """Return occupancy of the basin containing the best observed endpoint.

        Raises
        ------
        AssertionError
            If the retained best endpoint appears in no observed basin.
        """
        best_id = self._string(
            self._mapping(configuration["best_observed_converged"])["gauge_id"]
        )
        for basin in self._records(configuration["observed_converged_basins"]):
            ids = tuple(
                self._string(value) for value in self._array(basin["gauge_ids"])
            )
            if best_id in ids:
                return self._integer(basin["occupancy"])
        raise AssertionError("best endpoint has no basin")

    @staticmethod
    def _repository_source(root: Path, declared: str, label: str) -> Path:
        """Resolve one declared source while confining it to ``root``.

        Resolution permits retained paths containing internal ``..`` components when
        their normalized target remains inside the repository. Absolute paths and
        symlink traversals are likewise accepted only when their resolved target is
        beneath the resolved repository root.

        Raises
        ------
        ValueError
            If the resolved source lies outside the repository root.
        """
        resolved_root = root.resolve()
        candidate = (resolved_root / Path(declared)).resolve()
        if not candidate.is_relative_to(resolved_root):
            raise ValueError(f"{label} must resolve within repository_root")
        return candidate

    @staticmethod
    def _content_identity(payload: bytes, expected: str, label: str) -> None:
        """Require one byte payload to match its declared SHA-256 identity."""
        actual = hashlib.sha256(payload).hexdigest()
        if actual != expected:
            raise AssertionError(f"{label} identity mismatch")

    @classmethod
    def _same_json_value(cls, actual: JsonValue, expected: JsonValue) -> bool:
        """Compare closed JSON trees without Python's Boolean/numeric equivalence."""
        if type(actual) is not type(expected):
            return False
        if type(actual) is list and type(expected) is list:
            return len(actual) == len(expected) and all(
                cls._same_json_value(left, right)
                for left, right in zip(actual, expected, strict=True)
            )
        if type(actual) is dict and type(expected) is dict:
            return actual.keys() == expected.keys() and all(
                cls._same_json_value(actual[key], expected[key]) for key in actual
            )
        return actual == expected

    def _records(self, value: JsonValue) -> list[dict[str, JsonValue]]:
        return [self._mapping(item) for item in self._array(value)]

    @staticmethod
    def _mapping(value: JsonValue) -> dict[str, JsonValue]:
        """Return one already-decoded exact object at a schema boundary."""
        if type(value) is not dict:
            raise TypeError("expected mapping")
        return value

    @staticmethod
    def _array(value: JsonValue) -> list[JsonValue]:
        """Return one already-decoded exact array at a schema boundary."""
        if type(value) is not list:
            raise TypeError("expected array")
        return value

    def _string(self, value: JsonValue) -> str:
        """Return one exact string through the shared strict decoder contract."""
        return self._decoder.string(value, "value")

    def _integer(self, value: JsonValue) -> int:
        """Return one exact integer while rejecting Boolean substitution."""
        return self._decoder.integer(value, "value")

    def _real(self, value: JsonValue) -> float:
        """Return one finite binary64 real through the shared decoder contract."""
        return self._decoder.real(value, "value")

    def _boolean(self, value: JsonValue) -> bool:
        """Return one exact built-in Boolean through the shared decoder contract."""
        return self._decoder.boolean(value, "value")

    def _sha256(self, value: JsonValue) -> str:
        """Return one exact lowercase SHA-256 through the shared decoder contract."""
        return self._decoder.sha256(value, "value")

    @staticmethod
    def _equal(actual: int, expected: int, label: str) -> None:
        if actual != expected:
            raise AssertionError(f"{label}: {actual} != {expected}")

    @staticmethod
    def _close(actual: float, expected: float, tolerance: float, label: str) -> None:
        if abs(actual - expected) > tolerance:
            raise AssertionError(f"{label}: {actual} != {expected}")
