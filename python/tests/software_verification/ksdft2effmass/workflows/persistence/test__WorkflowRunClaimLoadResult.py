r"""Software verification of ``WorkflowRunClaimLoadResult``.

Bounded artifact scope: historical claim-load failure closure and snapshot exclusion.

Evidence profile: claim_bearing

Facet and represented meaning

Only loaded may contain a snapshot and receipt; failures retain shared read evidence.

Intrinsic and cross-object scope

Intrinsic rejection and retention use complete supported claim records from a real
isolated SQLite lifecycle. Repository tests separately own derivation correctness.

VVUQ and scientific exclusions

Software verification only; supplied genesis is not historical claim evidence.
"""

from dataclasses import FrozenInstanceError, replace
from typing import Literal

import pytest

from ksdft2effmass.persistence import RevisionReadResult, RevisionReadStatus
from ksdft2effmass.workflows import (
    AuthorityReservationOutcomeIdentity,
    WorkflowPersistenceFailure,
    WorkflowRunClaimLoadResult,
    WorkflowRunLoadResult,
)

pytestmark = pytest.mark.software_verification
SUT = WorkflowRunClaimLoadResult


class TestWorkflowRunClaimLoadResult:
    """Closed variant retention with actual historical claim record inputs."""

    def test_constructor__loaded__retains_actual_claim_pair(
        self,
        persisted_claim_load: WorkflowRunClaimLoadResult,
    ) -> None:
        """Evidence ID: SV-WFR-CLAIM-LOAD-006

        Requirement: Loaded retains both complete snapshot and historical receipt.

        Method: Reconstruct the result container from a real confirmed claim load.

        Oracle: Exact immutable input pair and complete retained read observation.

        Acceptance: Snapshot, receipt, request and shared result are retained unchanged.

        Interpretation: The container preserves supplied historical commitment evidence.

        Limitations: Receipt derivation is independently tested by the repository owner.
        """
        original = persisted_claim_load
        value = replace(original)
        assert value.snapshot is original.snapshot and value.receipt is original.receipt
        assert (
            value.request is original.request
            and value.store_result is original.store_result
        )
        assert value.receipt is not None
        assert (
            value.receipt.claimed_reservation_identity
            == value.claimed_reservation_identity
        )
        assert value.failure is None

    @pytest.mark.parametrize(
        "variant",
        [
            pytest.param("no_snapshot", id="receipt_without_snapshot"),
            pytest.param("no_receipt", id="snapshot_without_receipt"),
            pytest.param("failure", id="loaded_with_failure"),
            pytest.param("nonsuccess", id="failure_with_complete_claim_pair"),
        ],
    )
    def test_constructor__loaded__rejects_mixed_actual_claim_evidence(
        self,
        persisted_claim_load: WorkflowRunClaimLoadResult,
        record_failure: WorkflowPersistenceFailure,
        variant: str,
    ) -> None:
        """Evidence ID: SV-WFR-CLAIM-LOAD-007

        Requirement: Successful historical pairs cannot leak into failure variants.

        Method: Remove one required member or add failure to an actual claim result.

        Oracle: Success-only snapshot/receipt and failure exclusion contract.

        Acceptance: Every named invalid container raises ValueError.

        Interpretation: Actual receipt presence cannot convert a failed read to success.

        Limitations: No effect permission is represented by a historical claim receipt.
        """
        with pytest.raises(ValueError):
            if variant == "no_snapshot":
                replace(persisted_claim_load, snapshot=None)
            elif variant == "no_receipt":
                replace(persisted_claim_load, receipt=None)
            elif variant == "failure":
                replace(persisted_claim_load, failure=record_failure)
            else:
                replace(persisted_claim_load, status="error", failure=record_failure)

    @pytest.mark.parametrize(
        "status",
        [
            pytest.param("absent", id="stream_absent"),
            pytest.param("mismatch", id="read_mismatch"),
            pytest.param("incompatible", id="unsupported_representation"),
            pytest.param("corrupt", id="corrupt_read"),
            pytest.param("indeterminate", id="uncertain_read"),
            pytest.param("error", id="operational_failure"),
        ],
    )
    def test_constructor__nonsuccess__preserves_read_evidence(
        self,
        status: Literal[
            "absent", "mismatch", "incompatible", "corrupt", "indeterminate", "error"
        ],
        genesis_load: WorkflowRunLoadResult,
        record_failure: WorkflowPersistenceFailure,
    ) -> None:
        """Evidence ID: SV-WFR-CLAIM-LOAD-001

        Requirement: Every nonsuccess preserves complete available read evidence.

        Method: Construct each named failure with explicit request and evidence.

        Oracle: Closed seven-status vocabulary and no-snapshot nonsuccess contract.

        Acceptance: Request/selector/evidence persist without receipt or snapshot.

        Interpretation: Failure cannot become historical claim permission.

        Limitations: No successful claimed run or repository read is executed.
        """
        request = genesis_load.request
        shared = None
        failure: WorkflowPersistenceFailure | None = record_failure
        if status == "absent":
            shared = RevisionReadResult(
                result_id="absence",
                request_id=request.request_id,
                stream_id=request.stream_id,
                selector=request.selector,
                store_implementation_id="fixture-store",
                store_version_id="fixture:1",
                status=RevisionReadStatus.ABSENT,
                diagnostics=(),
                claim_boundary="supplied synthetic absence record",
                absence_observation="no represented stream",
            )
            failure = None
        claim = AuthorityReservationOutcomeIdentity("selected-claim")
        value = WorkflowRunClaimLoadResult(
            status=status,
            claimed_reservation_identity=claim,
            request=request,
            store_result=shared,
            failure=failure,
        )
        assert value.status == status
        assert value.claimed_reservation_identity == claim
        assert value.request is request
        assert value.store_result is shared
        assert value.failure is failure
        assert value.receipt is None
        assert value.snapshot is None

    def test_constructor__claim_rejection__retains_shared_found_without_snapshot(
        self,
        genesis_load: WorkflowRunLoadResult,
        record_failure: WorkflowPersistenceFailure,
    ) -> None:
        """Evidence ID: SV-WFR-CLAIM-LOAD-002

        Requirement: Rejected claims contain no snapshot but retain read evidence.

        Method: Record claim mismatch after a supplied FOUND genesis observation.

        Oracle: Genesis has no selected claim; failure-only snapshot exclusion.

        Acceptance: Shared observation remains exact but receipt/snapshot are None.

        Interpretation: Reading a run is not successfully recovering a claim.

        Limitations: The repository must independently detect the missing claim.
        """
        value = WorkflowRunClaimLoadResult(
            status="mismatch",
            claimed_reservation_identity=AuthorityReservationOutcomeIdentity(
                "missing-claim"
            ),
            request=genesis_load.request,
            store_result=genesis_load.store_result,
            failure=record_failure,
        )
        assert value.store_result is genesis_load.store_result
        assert value.snapshot is None
        assert value.receipt is None
        assert value.failure is record_failure

    @pytest.mark.parametrize(
        "variant",
        [
            pytest.param("missing_receipt", id="loaded_without_receipt"),
            pytest.param("bare_rejection", id="claim_rejection_without_failure"),
            pytest.param("false_absence", id="absence_from_found_observation"),
            pytest.param("snapshot", id="failure_with_snapshot"),
            pytest.param("unknown", id="unknown_status"),
        ],
    )
    def test_constructor__variant__rejects_incomplete_claim_evidence(
        self,
        variant: str,
        genesis_load: WorkflowRunLoadResult,
        record_failure: WorkflowPersistenceFailure,
    ) -> None:
        """Evidence ID: SV-WFR-CLAIM-LOAD-003

        Requirement: Claim variants require complete and exclusive evidence.

        Method: Omit receipt/failure or attach an unsupported snapshot/status.

        Oracle: Loaded pair and matching-shared-or-domain-failure invariants.

        Acceptance: Every invalid construction raises ValueError.

        Interpretation: A found run alone cannot become a loaded claim.

        Limitations: Valid receipt derivation remains a repository obligation.
        """
        value = WorkflowRunClaimLoadResult(
            status="error",
            claimed_reservation_identity=AuthorityReservationOutcomeIdentity("claim"),
            request=genesis_load.request,
            store_result=genesis_load.store_result,
            failure=record_failure,
        )
        with pytest.raises(ValueError):
            if variant == "missing_receipt":
                replace(
                    value, status="loaded", snapshot=genesis_load.snapshot, failure=None
                )
            elif variant == "bare_rejection":
                replace(value, failure=None)
            elif variant == "false_absence":
                replace(value, status="absent")
            elif variant == "snapshot":
                replace(value, snapshot=genesis_load.snapshot)
            else:
                replace(value, status="unknown")  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        "field",
        [
            pytest.param("claim", id="claim_string_only"),
            pytest.param("request", id="request_string_only"),
            pytest.param("shared", id="shared_result_string_only"),
            pytest.param("snapshot", id="snapshot_string_only"),
            pytest.param("receipt", id="receipt_string_only"),
            pytest.param("failure", id="failure_string_only"),
            pytest.param("status", id="boolean_status"),
        ],
    )
    def test_constructor__types__rejects_wrong_fields(
        self,
        field: str,
        genesis_load: WorkflowRunLoadResult,
        record_failure: WorkflowPersistenceFailure,
    ) -> None:
        """Evidence ID: SV-WFR-CLAIM-LOAD-004

        Requirement: Claim-load fields require exact nominal and record types.

        Method: Replace one field with a closed wrong-type value.

        Oracle: Exact selector, request, result, snapshot, receipt and failure types.

        Acceptance: Every invalid replacement raises TypeError.

        Interpretation: Receipt labels are not complete historical evidence.

        Limitations: Actual receipt correlation belongs to the repository.
        """
        value = WorkflowRunClaimLoadResult(
            status="error",
            claimed_reservation_identity=AuthorityReservationOutcomeIdentity("claim"),
            request=genesis_load.request,
            failure=record_failure,
        )
        with pytest.raises(TypeError):
            if field == "claim":
                replace(value, claimed_reservation_identity="claim")  # type: ignore[arg-type]
            elif field == "request":
                replace(value, request="request")  # type: ignore[arg-type]
            elif field == "shared":
                replace(value, store_result="shared")  # type: ignore[arg-type]
            elif field == "snapshot":
                replace(value, snapshot="snapshot")  # type: ignore[arg-type]
            elif field == "receipt":
                replace(value, receipt="receipt")  # type: ignore[arg-type]
            elif field == "failure":
                replace(value, failure="failure")  # type: ignore[arg-type]
            else:
                replace(value, status=True)  # type: ignore[arg-type]

    def test_field__status__is_immutable(
        self,
        genesis_load: WorkflowRunLoadResult,
        record_failure: WorkflowPersistenceFailure,
    ) -> None:
        """Evidence ID: SV-WFR-CLAIM-LOAD-005

        Requirement: Claim rejection cannot be changed to success in place.

        Method: Attempt direct status assignment on a represented error.

        Oracle: Frozen dataclass semantics and original error label.

        Acceptance: FrozenInstanceError occurs and snapshot remains None.

        Interpretation: Ordinary mutation cannot manufacture historical receipts.

        Limitations: No effect-entry or replay-equality claim is made.
        """
        value = WorkflowRunClaimLoadResult(
            status="error",
            claimed_reservation_identity=AuthorityReservationOutcomeIdentity("claim"),
            request=genesis_load.request,
            failure=record_failure,
        )
        with pytest.raises(FrozenInstanceError):
            value.status = "loaded"  # type: ignore[misc]
        assert value.status == "error"
        assert value.snapshot is None
