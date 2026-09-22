r"""Software verification of ``WorkflowRunLoadResult``.

Bounded artifact scope: closed domain load variants and complete shared evidence.

Evidence profile: claim_bearing

Facet and represented meaning

Only loaded retains a snapshot; absence requires explicit shared absence evidence.

Intrinsic and cross-object scope

Record closure, not request correlation, wire reconstruction or repository behavior.

VVUQ and scientific exclusions

Software verification of supplied synthetic evidence, not a real read or science.
"""

from dataclasses import FrozenInstanceError, replace
from typing import Literal

import pytest

from ksdft2effmass.persistence import (
    RevisionReadResult,
    RevisionReadStatus,
    RevisionSelector,
)
from ksdft2effmass.workflows import WorkflowPersistenceFailure, WorkflowRunLoadResult

pytestmark = pytest.mark.software_verification
SUT = WorkflowRunLoadResult


class TestWorkflowRunLoadResult:
    """Closed load evidence without inferring presence from errors."""

    @staticmethod
    def make_absent() -> RevisionReadResult:
        return RevisionReadResult(
            result_id="absent-result",
            request_id="read",
            stream_id="run",
            selector=RevisionSelector.LATEST,
            store_implementation_id="fixture-store",
            store_version_id="fixture:1",
            status=RevisionReadStatus.ABSENT,
            diagnostics=("explicit absence",),
            claim_boundary="synthetic observation",
            absence_observation="stream absent in the supplied store observation",
        )

    def test_constructor__loaded__retains_all_shared_evidence(
        self, genesis_load: WorkflowRunLoadResult
    ) -> None:
        """Evidence ID: SV-WFR-LOAD-001

        Requirement: Loaded preserves complete request, shared result and snapshot.

        Method: Construct a second result from explicit existing input records.

        Oracle: Exact supplied object identities, including shared evidence fields.

        Acceptance: Request/result/snapshot retain identity and no failure is added.

        Interpretation: No store observation is fabricated by copying record state.

        Limitations: The future repository must correlate independently valid records.
        """
        value = WorkflowRunLoadResult(
            status="loaded",
            request=genesis_load.request,
            store_result=genesis_load.store_result,
            snapshot=genesis_load.snapshot,
        )
        assert value.request is genesis_load.request
        assert value.store_result is genesis_load.store_result
        assert value.snapshot is genesis_load.snapshot
        assert value.failure is None

    def test_constructor__absent__retains_explicit_observation(
        self, genesis_load: WorkflowRunLoadResult
    ) -> None:
        """Evidence ID: SV-WFR-LOAD-002

        Requirement: Absence retains its explicit complete shared observation.

        Method: Construct absent from a fixed shared ABSENT result.

        Oracle: Supplied absence, result, request, store and diagnostic records.

        Acceptance: Full shared result persists and no snapshot/failure is created.

        Interpretation: Absence is represented evidence, not an error inference.

        Limitations: The fixture does not execute a shared-store read.
        """
        observation = self.make_absent()
        value = WorkflowRunLoadResult(
            status="absent", request=genesis_load.request, store_result=observation
        )
        assert value.store_result is observation
        assert value.snapshot is None
        assert value.failure is None

    @pytest.mark.parametrize(
        "status",
        [
            pytest.param("mismatch", id="identity_mismatch"),
            pytest.param("incompatible", id="unsupported_version"),
            pytest.param("corrupt", id="corrupt_representation"),
            pytest.param("indeterminate", id="uncertain_observation"),
            pytest.param("error", id="operational_failure"),
        ],
    )
    def test_constructor__domain_rejection__retains_full_failure(
        self,
        genesis_load: WorkflowRunLoadResult,
        record_failure: WorkflowPersistenceFailure,
        status: Literal[
            "mismatch", "incompatible", "corrupt", "indeterminate", "error"
        ],
    ) -> None:
        """Evidence ID: SV-WFR-LOAD-003

        Requirement: Each domain rejection retains complete failure and no snapshot.

        Method: Construct the named closed status with supplied domain evidence.

        Oracle: Reviewed load vocabulary and exclusive snapshot contract.

        Acceptance: Status/failure persist with no invented store result or snapshot.

        Interpretation: Pre-read rejection need not fabricate shared result evidence.

        Limitations: Status classification by the repository is not exercised.
        """
        value = WorkflowRunLoadResult(
            status=status, request=genesis_load.request, failure=record_failure
        )
        assert value.status == status
        assert value.failure is record_failure
        assert value.store_result is None
        assert value.snapshot is None

    @pytest.mark.parametrize(
        "variant",
        [
            pytest.param("no_snapshot", id="loaded_without_snapshot"),
            pytest.param("no_found", id="loaded_without_found_evidence"),
            pytest.param("mixed", id="loaded_with_failure"),
            pytest.param("failure_snapshot", id="nonsuccess_with_snapshot"),
            pytest.param("bare_absent", id="absence_without_shared_observation"),
            pytest.param("bare_error", id="error_without_evidence"),
            pytest.param("unknown", id="unknown_status"),
        ],
    )
    def test_constructor__variant__rejects_invalid_evidence(
        self,
        variant: str,
        genesis_load: WorkflowRunLoadResult,
        record_failure: WorkflowPersistenceFailure,
    ) -> None:
        """Evidence ID: SV-WFR-LOAD-004

        Requirement: Incomplete, mixed and unknown load variants are rejected.

        Method: Independently remove evidence or mix success and failure fields.

        Oracle: Closed success, absence and nonsuccess evidence invariants.

        Acceptance: Every invalid variant raises ValueError.

        Interpretation: An operational failure cannot by itself establish absence.

        Limitations: Shared request/address/envelope binding is repository-owned.
        """
        with pytest.raises(ValueError):
            if variant == "no_snapshot":
                replace(genesis_load, snapshot=None)
            elif variant == "no_found":
                replace(genesis_load, store_result=None)
            elif variant == "mixed":
                replace(genesis_load, failure=record_failure)
            elif variant == "failure_snapshot":
                replace(genesis_load, status="corrupt", failure=record_failure)
            elif variant == "bare_absent":
                WorkflowRunLoadResult(
                    status="absent",
                    request=genesis_load.request,
                    failure=record_failure,
                )
            elif variant == "bare_error":
                WorkflowRunLoadResult(status="error", request=genesis_load.request)
            else:
                replace(genesis_load, status="unknown")  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        "field",
        [
            pytest.param("request", id="request_label_only"),
            pytest.param("store_result", id="store_label_only"),
            pytest.param("snapshot", id="snapshot_label_only"),
            pytest.param("failure", id="failure_text_only"),
            pytest.param("status", id="boolean_status"),
        ],
    )
    def test_constructor__types__rejects_wrong_fields(
        self, genesis_load: WorkflowRunLoadResult, field: str
    ) -> None:
        """Evidence ID: SV-WFR-LOAD-005

        Requirement: Load evidence has exact concrete field types.

        Method: Replace one field with an explicit closed wrong semantic type.

        Oracle: Exact request, shared result, snapshot, failure and status contracts.

        Acceptance: All replacements raise TypeError.

        Interpretation: Bare labels cannot stand in for complete read evidence.

        Limitations: No wire parser is involved in these constructor cases.
        """
        with pytest.raises(TypeError):
            if field == "request":
                replace(genesis_load, request="request")  # type: ignore[arg-type]
            elif field == "store_result":
                replace(genesis_load, store_result="result")  # type: ignore[arg-type]
            elif field == "snapshot":
                replace(genesis_load, snapshot="snapshot")  # type: ignore[arg-type]
            elif field == "failure":
                replace(genesis_load, failure="failure")  # type: ignore[arg-type]
            else:
                replace(genesis_load, status=True)  # type: ignore[arg-type]

    def test_field__snapshot__is_immutable(
        self, genesis_load: WorkflowRunLoadResult
    ) -> None:
        """Evidence ID: SV-WFR-LOAD-006

        Requirement: A loaded result cannot lose its snapshot through assignment.

        Method: Attempt direct mutation of a complete loaded record.

        Oracle: Frozen dataclass semantics and original complete snapshot.

        Acceptance: FrozenInstanceError occurs and snapshot remains present.

        Interpretation: Ordinary callers cannot mutate success into partial success.

        Limitations: This does not authorize advancing the retained run.
        """
        with pytest.raises(FrozenInstanceError):
            genesis_load.snapshot = None  # type: ignore[misc]
        assert genesis_load.snapshot is not None
