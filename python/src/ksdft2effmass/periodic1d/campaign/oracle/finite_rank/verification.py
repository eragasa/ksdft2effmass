"""Independently verify the finite-rank analytical-oracle result."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from ksdft2effmass.periodic1d.campaign.serialization import (
    Periodic1DCampaignJsonDecoder,
)
from ksdft2effmass.serialization.json import JsonValue

from .encoded_documents import FiniteRankOracleEncodedDocuments
from .independent_reconstruction import (
    FiniteRankOracleIndependentReconstructor,
)

LEGACY_RUNNER_SHA256 = (
    "0f0ffde200456882981cc8b89bc3622af4dd00696ce0c17a0ad106ed957ffc06"
)


@dataclass(frozen=True, slots=True)
class FiniteRankOracleVerificationRequest:
    """Request finite-rank-oracle verification from explicit documents and location.

    Parameters
    ----------
    encoded_documents
        Exact finite-rank-oracle input and retained-result bytes.
    repository_root
        Absolute filesystem base for repository-relative authenticated sources.

    Raises
    ------
    TypeError
        If documents or repository root use unsupported public types.
    ValueError
        If ``repository_root`` is relative.

    Notes
    -----
    Construction checks intrinsic type and lexical location contracts only. It does
    not resolve the root, require it to exist, read files, decode JSON, authenticate
    identities, reconstruct resolvent roots or eigenspaces, or qualify an oracle.
    The verifier later authenticates the retained input identity, accepts only the
    frozen historical runner digest for a legacy result or checks explicit script
    and implementation identities for a newer result, and authenticates
    source-result identities declared by the input. It does not recursively follow
    provenance links in those source results. Neither the path nor successful
    authentication establishes material provenance, scientific validation, UQ, or
    acceptance.
    """

    encoded_documents: FiniteRankOracleEncodedDocuments
    repository_root: Path

    def __post_init__(self) -> None:
        """Require exact documents and an absolute repository root.

        Raises
        ------
        TypeError
            If documents or repository root use unsupported public types.
        ValueError
            If the repository root is relative.
        """
        if type(self.encoded_documents) is not FiniteRankOracleEncodedDocuments:
            raise TypeError(
                "encoded_documents must be FiniteRankOracleEncodedDocuments"
            )
        if not isinstance(self.repository_root, Path):
            raise TypeError("repository_root must be pathlib.Path")
        if not self.repository_root.is_absolute():
            raise ValueError("repository_root must be absolute")


@dataclass(frozen=True, slots=True)
class FiniteRankOracleVerificationResult:
    """Report separate source, structure, numerical, and aggregate channels.

    Parameters
    ----------
    source_authentication_passed
        Whether every declared compact source matched its exact content identity.
    structural_contract_passed
        Whether every closed-schema and intrinsic structural check passed.
    numerical_reconstruction_passed
        Whether every independent numerical reconstruction comparison passed.
    verified_record_count
        Number of retained result records reconstructed and compared.
    source_identity_count
        Number of distinct authenticated source identities checked.
    retained_result_sha256
        Lowercase SHA-256 identity of the exact retained-result bytes.

    Raises
    ------
    TypeError
        An argument does not have the required exact public type.
    ValueError
        An argument violates a schema, domain, identity, or correlation invariant.
    """

    source_authentication_passed: bool
    structural_contract_passed: bool
    numerical_reconstruction_passed: bool
    verified_record_count: int
    source_identity_count: int
    retained_result_sha256: str

    def __post_init__(self) -> None:
        """Validate channels, counts, and retained SHA-256 identity."""
        channels = (
            self.source_authentication_passed,
            self.structural_contract_passed,
            self.numerical_reconstruction_passed,
        )
        if any(type(value) is not bool for value in channels):
            raise TypeError("verification channels must be Boolean")
        if (
            type(self.verified_record_count) is not int
            or self.verified_record_count < 1
        ):
            raise ValueError("verified_record_count must be positive")
        if (
            type(self.source_identity_count) is not int
            or self.source_identity_count < 1
        ):
            raise ValueError("source_identity_count must be positive")
        if len(self.retained_result_sha256) != 64 or any(
            character not in "0123456789abcdef"
            for character in self.retained_result_sha256
        ):
            raise ValueError("retained_result_sha256 must be lowercase SHA-256")

    @property
    def passed(self) -> bool:
        """Return the aggregate disposition across all channels.

        Returns
        -------
        bool
            ``True`` only when every retained verification channel passes.
        """
        return (
            self.source_authentication_passed
            and self.structural_contract_passed
            and self.numerical_reconstruction_passed
        )


class FiniteRankOracleCampaignVerifier:
    """Reconstruct both routes without importing the maintained Workflow.

    Decoding, finite-operator construction, resolvent reconstruction, comparisons, and
    identity checks are owned by this independent verifier instance rather than by
    static namespace utilities.
    """

    __slots__ = ("_decoder", "_reconstructor")

    def __init__(self) -> None:
        """Bind strict JSON mechanics and the independent numerical route."""
        self._decoder = Periodic1DCampaignJsonDecoder()
        self._reconstructor = FiniteRankOracleIndependentReconstructor()

    def execute(
        self, request: FiniteRankOracleVerificationRequest
    ) -> FiniteRankOracleVerificationResult:
        """Authenticate and independently reconstruct the retained oracle result.

        Parameters
        ----------
        request
            Typed request carrying all inputs required by the operation.

        Returns
        -------
        FiniteRankOracleVerificationResult
            Authentication, structural, and independent finite reconstruction channels.

        Raises
        ------
        TypeError
            An argument does not have the required exact public type.
        ValueError
            An argument violates a schema, domain, identity, or correlation invariant.
        """
        if not isinstance(request, FiniteRankOracleVerificationRequest):
            raise TypeError("request must be FiniteRankOracleVerificationRequest")
        repository_root = request.repository_root
        retained = self._decoder.document(
            request.encoded_documents.retained_result_document
        )
        if self._decoder.integer(retained["schema_version"], "schema version") != 1:
            raise ValueError("unsupported result schema")
        if retained["evidence_status"] != "synthetic test data":
            raise ValueError("evidence status mismatch")
        provenance = self._decoder.mapping(retained["provenance"], "provenance")
        input_path = repository_root / self._decoder.nonempty_string(
            provenance["input_path"], "input path"
        )
        script_path = repository_root / self._decoder.nonempty_string(
            provenance["script_path"], "script path"
        )
        self._assert_text(
            self._sha256(input_path), provenance["input_sha256"], "input sha256"
        )
        self._assert_text(
            hashlib.sha256(request.encoded_documents.input_document).hexdigest(),
            provenance["input_sha256"],
            "encapsulated input sha256",
        )
        recorded_script_sha256 = self._decoder.nonempty_string(
            provenance["script_sha256"], "script sha256"
        )
        implementation_path_value = provenance.get("implementation_path")
        implementation_sha256_value = provenance.get("implementation_sha256")
        if implementation_path_value is None and implementation_sha256_value is None:
            self._assert_text(
                LEGACY_RUNNER_SHA256,
                recorded_script_sha256,
                "historical script sha256",
            )
        else:
            self._assert_text(
                self._sha256(script_path),
                recorded_script_sha256,
                "script sha256",
            )
            implementation_path = repository_root / self._decoder.nonempty_string(
                implementation_path_value, "implementation path"
            )
            self._assert_text(
                self._sha256(implementation_path),
                implementation_sha256_value,
                "implementation sha256",
            )
        source = self._decoder.document(request.encoded_documents.input_document)
        source_records = self._records(source["source_identities"], "sources")
        retained_sources = self._records(
            retained["source_identities"], "retained sources"
        )
        if source_records != retained_sources:
            raise ValueError("retained source identities differ from input")
        for record in source_records:
            path_text = self._decoder.nonempty_string(record["path"], "source path")
            digest = self._decoder.nonempty_string(record["sha256"], "source sha256")
            if self._sha256(repository_root / path_text) != digest:
                raise ValueError(f"source identity mismatch: {path_text}")
        composite = self._load(
            repository_root
            / self._decoder.nonempty_string(source_records[0]["path"], "parent path")
        )
        parent_contract = self._decoder.mapping(source["parent_contract"], "parent")
        group_id = self._decoder.nonempty_string(
            parent_contract["composite_group_id"], "group id"
        )
        hopping_range = self._decoder.integer(
            parent_contract["hopping_range_cells"], "hopping range"
        )
        momentum = self._decoder.real(parent_contract["supercell_momentum"], "momentum")
        hoppings = self._reconstructor.hoppings(composite, group_id, hopping_range)
        rank_one = self._decoder.mapping(source["rank_one_contract"], "rank one")
        cell_counts = self._decoder.integers(rank_one["supercell_sizes"], "cell counts")
        magnitudes = self._decoder.reals(
            rank_one["attractive_magnitudes"], "magnitudes"
        )
        angle = self._decoder.real(rank_one["orbital_angle_radians"], "angle")
        phase = self._decoder.real(rank_one["orbital_relative_phase_radians"], "phase")
        orbital = np.asarray(
            [np.cos(angle), np.exp(1j * phase) * np.sin(angle)],
            dtype=np.complex128,
        )
        site = self._decoder.integer(rank_one["defect_site"], "defect site")
        tolerances = self._decoder.mapping(source["tolerances"], "tolerances")
        root_tolerance = self._decoder.real(
            tolerances["root_interval"], "root tolerance"
        )
        edge_margin = self._decoder.real(
            tolerances["bound_state_edge_margin"], "edge margin"
        )
        expected_sweep: list[JsonValue] = []
        for cell_count in cell_counts:
            for magnitude in magnitudes:
                expected_sweep.append(
                    self._reconstructor.rank_one_record(
                        hoppings,
                        cell_count,
                        momentum,
                        orbital,
                        site,
                        magnitude,
                        root_tolerance,
                        edge_margin,
                    )
                )
        self._assert_json(retained["rank_one_sweep"], expected_sweep, "rank one sweep")
        special = self._decoder.mapping(source["special_controls"], "special")
        expected_special = self._reconstructor.special_records(
            hoppings,
            momentum,
            orbital,
            site,
            special,
            root_tolerance,
            edge_margin,
        )
        self._assert_json(
            retained["special_controls"], expected_special, "special controls"
        )
        records = tuple(
            self._decoder.mapping(item, "sweep record") for item in expected_sweep
        )
        expected_summary: dict[str, JsonValue] = {
            "case_count": len(records),
            "maximum_energy_absolute_discrepancy": max(
                self._decoder.real(item["energy_absolute_discrepancy"], "energy error")
                for item in records
            ),
            "maximum_projector_frobenius_defect": max(
                self._decoder.real(
                    item["projector_frobenius_defect"], "projector error"
                )
                for item in records
            ),
            "maximum_oracle_secular_residual": max(
                self._decoder.real(item["oracle_secular_residual"], "secular residual")
                for item in records
            ),
            "all_attractive_bound_state_counts": [1],
        }
        self._assert_json(retained["summary"], expected_summary, "summary")
        contract = self._decoder.mapping(retained["oracle_contract"], "oracle contract")
        independence = self._decoder.nonempty_string(
            contract["independence_boundary"], "independence boundary"
        )
        if "does not diagonalize the full defect Hamiltonian" not in independence:
            raise ValueError("oracle independence boundary is missing")
        limitations = retained["limitations"]
        if not isinstance(limitations, list) or len(limitations) != 4:
            raise ValueError("four limitations are required")
        return FiniteRankOracleVerificationResult(
            source_authentication_passed=True,
            structural_contract_passed=True,
            numerical_reconstruction_passed=True,
            verified_record_count=len(expected_sweep) + len(expected_special),
            source_identity_count=len(source_records),
            retained_result_sha256=hashlib.sha256(
                request.encoded_documents.retained_result_document
            ).hexdigest(),
        )

    def _assert_json(self, actual: JsonValue, expected: JsonValue, path: str) -> None:
        """Implement the owner-local assert json operation."""
        if isinstance(expected, dict):
            if not isinstance(actual, dict) or set(actual) != set(expected):
                raise ValueError(f"field mismatch at {path}")
            for key, value in expected.items():
                self._assert_json(actual[key], value, f"{path}.{key}")
            return
        if isinstance(expected, list):
            if not isinstance(actual, list) or len(actual) != len(expected):
                raise ValueError(f"array mismatch at {path}")
            for index, (actual_item, expected_item) in enumerate(
                zip(actual, expected, strict=True)
            ):
                self._assert_json(actual_item, expected_item, f"{path}[{index}]")
            return
        if isinstance(expected, float):
            try:
                np.testing.assert_allclose(
                    self._decoder.real(actual, path),
                    expected,
                    rtol=5.0e-12,
                    atol=5.0e-14,
                )
            except AssertionError as error:
                raise ValueError(f"value mismatch at {path}") from error
            return
        if actual != expected:
            raise ValueError(f"value mismatch at {path}")

    def _load(self, path: Path) -> dict[str, JsonValue]:
        """Strictly decode one authenticated JSON source artifact."""
        return self._decoder.document(path.read_bytes())

    def _records(self, value: JsonValue, name: str) -> tuple[dict[str, JsonValue], ...]:
        """Adapt one decoded array to verifier-owned records."""
        return tuple(
            self._decoder.mapping(item, name)
            for item in self._decoder.array(value, name)
        )

    def _assert_text(self, expected: str, actual: JsonValue, name: str) -> None:
        """Implement the owner-local assert text operation."""
        if self._decoder.nonempty_string(actual, name) != expected:
            raise ValueError(f"{name} mismatch")

    def _sha256(self, path: Path) -> str:
        """Implement the owner-local sha256 operation."""
        return hashlib.sha256(path.read_bytes()).hexdigest()
