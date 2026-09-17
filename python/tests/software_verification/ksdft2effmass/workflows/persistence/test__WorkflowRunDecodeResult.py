r"""Software verification of ``WorkflowRunDecodeResult``.

Bounded artifact scope: complete run/binding versus decode-failure variants.

Evidence profile: claim_bearing

Facet and represented meaning

Decoded success requires both the complete run and durable binding.

Intrinsic and cross-object scope

Intrinsic record closure only; no wire decoding, replay or structural validation.

VVUQ and scientific exclusions

Software verification of synthetic record inputs, not science or durable presence.
"""

from dataclasses import FrozenInstanceError, replace
from typing import Literal

import pytest
from ksdft2effmass.workflows import (
    WorkflowPersistenceFailure,
    WorkflowRunDecodeResult,
    WorkflowRunSnapshot,
)

pytestmark = pytest.mark.software_verification
SUT = WorkflowRunDecodeResult


class TestWorkflowRunDecodeResult:
    """No partial successful reconstruction."""

    def test_constructor__decoded__retains_complete_pair(
        self, genesis_snapshot: WorkflowRunSnapshot
    ) -> None:
        """Evidence ID: SV-WFR-RUN-DECODE-001

        Requirement: Decoded success retains complete run and durable binding.

        Method: Construct success from a complete genesis and exact binding.

        Oracle: Supplied immutable records, not a serializer round trip.

        Acceptance: Both records retain identity; no failure is present.

        Interpretation: The constructor does not perform decoding or store reads.

        Limitations: Genesis contains no transition history or concrete results.
        """
        value = WorkflowRunDecodeResult(
            status="decoded", run=genesis_snapshot.run, binding=genesis_snapshot.binding
        )
        assert value.run is genesis_snapshot.run
        assert value.binding is genesis_snapshot.binding
        assert value.failure is None

    @pytest.mark.parametrize(
        "status",
        [
            pytest.param("incompatible", id="unsupported_version"),
            pytest.param("corrupt", id="invalid_known_representation"),
            pytest.param("error", id="operational_failure"),
        ],
    )
    def test_constructor__nonsuccess__retains_only_failure(
        self,
        status: Literal["incompatible", "corrupt", "error"],
        record_failure: WorkflowPersistenceFailure,
    ) -> None:
        """Evidence ID: SV-WFR-RUN-DECODE-002

        Requirement: Decode nonsuccess contains no partial run or binding.

        Method: Construct each closed nonsuccess using fixed structured failure.

        Oracle: Reviewed decode vocabulary and exclusive field contract.

        Acceptance: Status/failure persist and run/binding are both None.

        Interpretation: Incompatibility and corruption remain distinct labels.

        Limitations: The serializer owns actual failure classification.
        """
        value = WorkflowRunDecodeResult(status=status, failure=record_failure)
        assert value.status == status
        assert value.failure is record_failure
        assert value.run is None
        assert value.binding is None

    @pytest.mark.parametrize(
        "variant",
        [
            pytest.param("no_run", id="success_without_run"),
            pytest.param("no_binding", id="success_without_binding"),
            pytest.param("with_failure", id="success_with_failure"),
            pytest.param("failed_run", id="failure_with_partial_run"),
            pytest.param("failed_binding", id="failure_with_partial_binding"),
            pytest.param("no_failure", id="failure_without_evidence"),
            pytest.param("unknown", id="unknown_status"),
        ],
    )
    def test_constructor__variant__rejects_partial_or_mixed_values(
        self,
        variant: str,
        genesis_snapshot: WorkflowRunSnapshot,
        record_failure: WorkflowPersistenceFailure,
    ) -> None:
        """Evidence ID: SV-WFR-RUN-DECODE-003

        Requirement: Incomplete, mixed and unknown decode variants are invalid.

        Method: Construct each independently meaningful missing or mixed field case.

        Oracle: Success requires the complete pair and nonsuccess requires failure.

        Acceptance: Each invalid variant raises ValueError.

        Interpretation: A recovered binding alone cannot masquerade as a run.

        Limitations: Constructor rejection does not validate a wire schema.
        """
        with pytest.raises(ValueError):
            if variant == "no_run":
                WorkflowRunDecodeResult(
                    status="decoded", binding=genesis_snapshot.binding
                )
            elif variant == "no_binding":
                WorkflowRunDecodeResult(status="decoded", run=genesis_snapshot.run)
            elif variant == "with_failure":
                WorkflowRunDecodeResult(
                    status="decoded",
                    run=genesis_snapshot.run,
                    binding=genesis_snapshot.binding,
                    failure=record_failure,
                )
            elif variant == "failed_run":
                WorkflowRunDecodeResult(
                    status="corrupt", run=genesis_snapshot.run, failure=record_failure
                )
            elif variant == "failed_binding":
                WorkflowRunDecodeResult(
                    status="error",
                    binding=genesis_snapshot.binding,
                    failure=record_failure,
                )
            elif variant == "no_failure":
                WorkflowRunDecodeResult(status="incompatible")
            else:
                WorkflowRunDecodeResult(status="unknown")  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        "field",
        [
            pytest.param("run", id="identity_without_run"),
            pytest.param("binding", id="text_without_binding"),
            pytest.param("failure", id="text_without_failure"),
            pytest.param("status", id="nonstring_status"),
        ],
    )
    def test_constructor__types__rejects_wrong_fields(
        self, field: str, record_failure: WorkflowPersistenceFailure
    ) -> None:
        """Evidence ID: SV-WFR-RUN-DECODE-004

        Requirement: Record fields cannot be replaced by identity-only stand-ins.

        Method: Replace fields with explicit wrong semantic types.

        Oracle: Concrete run/binding/failure and exact string status contracts.

        Acceptance: Each wrong-type replacement raises TypeError.

        Interpretation: Complete nominal record types are required before closure.

        Limitations: This does not exercise arbitrary ResultObject serialization.
        """
        value = WorkflowRunDecodeResult(status="error", failure=record_failure)
        with pytest.raises(TypeError):
            if field == "run":
                replace(value, run="run")  # type: ignore[arg-type]
            elif field == "binding":
                replace(value, binding="binding")  # type: ignore[arg-type]
            elif field == "failure":
                replace(value, failure="failure")  # type: ignore[arg-type]
            else:
                replace(value, status=False)  # type: ignore[arg-type]

    def test_field__run__is_immutable(
        self, genesis_snapshot: WorkflowRunSnapshot
    ) -> None:
        """Evidence ID: SV-WFR-RUN-DECODE-005

        Requirement: A completed decoded result cannot lose its run in place.

        Method: Attempt assigning None to the successful run field.

        Oracle: Frozen dataclass semantics and complete input run.

        Acceptance: FrozenInstanceError is raised and the original run remains.

        Interpretation: Ordinary mutation cannot create a partial decoded success.

        Limitations: Cross-record domain validity is a separate validator concern.
        """
        value = WorkflowRunDecodeResult(
            status="decoded", run=genesis_snapshot.run, binding=genesis_snapshot.binding
        )
        with pytest.raises(FrozenInstanceError):
            value.run = None  # type: ignore[misc]
        assert value.run is genesis_snapshot.run
