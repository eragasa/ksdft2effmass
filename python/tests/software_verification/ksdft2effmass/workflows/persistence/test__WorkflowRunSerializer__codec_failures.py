r"""Software verification of ``WorkflowRunSerializer``.

Bounded artifact scope: returned codec failures, agreement checks and invalid responses.

Evidence profile: claim_bearing

Facet and represented meaning

Immutable typed fault ports exercise both aggregate operations and their counterpart
codec checks. Foreign failure records must remain complete; aggregate-owned failures
must retain phase/input identities and expose no partial run or encoded payload.

Intrinsic and cross-object scope

Faults use a real scalar codec for unaffected operations and deterministic injected
responses for the tested boundary. No store, replay, Task or native process is used.

VVUQ and scientific exclusions

Synthetic software verification only; codec agreement does not establish scientific
meaning, numerical accuracy, historical provenance or authority.
"""

from dataclasses import dataclass, replace
from hashlib import sha256
from pathlib import Path
from typing import Literal

import pytest
from ksdft2effmass import analysis as q
from ksdft2effmass import workflows as w
from ksdft2effmass.petrinet import colored as c
from ksdft2effmass.workflows import WorkflowRunSerializer

type Operation = Literal["encode", "decode"]
type FailureStatus = Literal["incompatible", "invalid", "error"]
type AgreementFault = Literal["encode_identity", "decode_identity", "content"]

pytestmark = pytest.mark.software_verification
SUT = WorkflowRunSerializer


class TestWorkflowRunSerializer:
    """Own public codec-port fault injection and complete failure assertions."""

    @dataclass(frozen=True, slots=True)
    class FailureCodec:
        """Return supplied closed failures without counters or mutable call state."""

        encode_failure: w.WorkflowResultValueEncodeResult | None = None
        decode_failure: w.WorkflowResultValueDecodeResult | None = None
        recheck: bool = False

        def encode(self, value: w.ResultObject) -> w.WorkflowResultValueEncodeResult:
            if self.encode_failure is not None and (
                not self.recheck
                or (
                    type(value) is q.ScalarQuantityOfInterestValue
                    and value.value == 3.5
                )
            ):
                return self.encode_failure
            return q.QuantityOfInterestResultValueSerializer().encode(value)

        def decode(
            self, envelope: w.WorkflowEncodedResultValue
        ) -> w.WorkflowResultValueDecodeResult:
            if self.decode_failure is not None:
                return self.decode_failure
            decoded = q.QuantityOfInterestResultValueSerializer().decode(envelope)
            if self.recheck and type(decoded.value) is q.ScalarQuantityOfInterestValue:
                return replace(decoded, value=replace(decoded.value, value=3.5))
            return decoded

    @dataclass(frozen=True, slots=True)
    class AgreementCodec:
        """Substitute a typed identity or value, keeping unaffected mechanics real."""

        fault: AgreementFault

        def encode(self, value: w.ResultObject) -> w.WorkflowResultValueEncodeResult:
            encoded = q.QuantityOfInterestResultValueSerializer().encode(value)
            if self.fault == "encode_identity" and encoded.encoded is not None:
                return replace(
                    encoded,
                    encoded=replace(
                        encoded.encoded,
                        result_identity=w.ResultObjectIdentity("detached"),
                    ),
                )
            return encoded

        def decode(
            self, envelope: w.WorkflowEncodedResultValue
        ) -> w.WorkflowResultValueDecodeResult:
            decoded = q.QuantityOfInterestResultValueSerializer().decode(envelope)
            if type(decoded.value) is q.ScalarQuantityOfInterestValue:
                if self.fault == "decode_identity":
                    return replace(
                        decoded,
                        value=replace(
                            decoded.value, identity=w.ResultObjectIdentity("detached")
                        ),
                    )
                if self.fault == "content":
                    return replace(decoded, value=replace(decoded.value, value=3.5))
            return decoded

    @dataclass(frozen=True, slots=True)
    class WrongResultCodec:
        """Violate the response type only at the explicitly suppressed return site."""

        phase: Operation
        failure: w.WorkflowPersistenceFailure

        def encode(self, value: w.ResultObject) -> w.WorkflowResultValueEncodeResult:
            if self.phase == "encode":
                # Intentional codec protocol violation; the aggregate must reject it.
                return w.WorkflowResultValueDecodeResult(
                    status="error", failure=self.failure
                )  # type: ignore[return-value]
            return q.QuantityOfInterestResultValueSerializer().encode(value)

        def decode(
            self, envelope: w.WorkflowEncodedResultValue
        ) -> w.WorkflowResultValueDecodeResult:
            if self.phase == "decode":
                # Intentional codec protocol violation; the aggregate must reject it.
                return w.WorkflowResultValueEncodeResult(
                    status="error", failure=self.failure
                )  # type: ignore[return-value]
            return q.QuantityOfInterestResultValueSerializer().decode(envelope)

    @dataclass(frozen=True, slots=True)
    class RecursionCodec:
        """Raise a bounded synthetic exception, without allocating recursive state."""

        def encode(self, value: w.ResultObject) -> w.WorkflowResultValueEncodeResult:
            raise RecursionError("synthetic recursion detail must not escape")

        def decode(
            self, envelope: w.WorkflowEncodedResultValue
        ) -> w.WorkflowResultValueDecodeResult:
            raise RecursionError("synthetic recursion detail must not escape")

    @staticmethod
    def wire() -> bytes:
        return (
            Path(__file__)
            .with_name("resources")
            .joinpath("workflow-run-scalar-v1.json")
            .read_bytes()
        )

    @staticmethod
    def make_failure(
        code: w.WorkflowPersistenceFailureCode,
    ) -> w.WorkflowPersistenceFailure:
        return w.WorkflowPersistenceFailure(
            implementation_identity="synthetic-result-codec:1",
            phase="supplied-phase",
            code=code,
            input_identities=("source-b", "source-a"),
            expected="synthetic expected condition",
            observed="synthetic observed condition",
            diagnostic="sanitized supplied diagnostic",
            claim_boundary="software fault fixture only",
        )

    @staticmethod
    def make_run(genesis: w.WorkflowRun) -> w.WorkflowRun:
        evaluator = q.QuantityOfInterestEvaluatorIdentity("synthetic-evaluator:7")
        scalar = q.ScalarQuantityOfInterestValue(
            w.ResultObjectIdentity("synthetic-result"),
            q.ScalarQuantityOfInterestDefinition(
                q.QuantityOfInterestIdentity("synthetic-qoi"),
                q.QuantityOfInterestSubjectIdentity("synthetic-subject"),
                q.QuantityOfInterestStateSpaceIdentity("synthetic-space"),
                q.QuantityOfInterestConventionIdentity("synthetic-convention"),
                evaluator,
                (
                    q.NormalizedObservationRequirementIdentity("second"),
                    q.NormalizedObservationRequirementIdentity("first"),
                ),
                q.QuantityOfInterestCompleteness.COMPLETE,
                "synthetic-unit",
            ),
            w.ResultObjectIdentity("synthetic-observations"),
            evaluator,
            -0.0,
        )
        task = w.TaskInstance(
            w.TaskInstanceIdentity("task"), w.TaskDefinitionIdentity("definition"), None
        )
        return replace(
            genesis,
            task_instances=(task,),
            activations=(
                w.TaskActivation(
                    w.TaskActivationIdentity("activation"),
                    genesis.workflow_identity,
                    genesis.identity,
                    task,
                    w.OperationIdentity("operation"),
                    w.AttemptIdentity("attempt"),
                    (w.TaskInputBinding("scalar", scalar),),
                    w.DirectTaskActivationSelection(
                        c.ColoredPetriNetSelectionResultIdentity("a" * 64)
                    ),
                ),
            ),
        )

    def execute(
        self,
        serializer: WorkflowRunSerializer,
        operation: Operation,
        snapshot: w.WorkflowRunSnapshot,
    ) -> w.WorkflowRunEncodeResult | w.WorkflowRunDecodeResult:
        """Adapt one public operation; assertions remain with the evidence owner."""
        if operation == "encode":
            return serializer.serialize(self.make_run(snapshot.run), snapshot.binding)
        return serializer.deserialize(self.wire())

    @staticmethod
    def assert_no_partial(
        result: w.WorkflowRunEncodeResult | w.WorkflowRunDecodeResult,
    ) -> None:
        if type(result) is w.WorkflowRunEncodeResult:
            assert result.encoded is None
        else:
            assert type(result) is w.WorkflowRunDecodeResult
            assert result.run is None and result.binding is None

    @pytest.mark.parametrize(
        ("operation", "phase", "status", "code"),
        [
            pytest.param(
                "encode",
                "encode",
                "invalid",
                w.WorkflowPersistenceFailureCode.INVARIANT_VIOLATION,
                id="encode_initial_invalid",
            ),
            pytest.param(
                "encode",
                "decode",
                "invalid",
                w.WorkflowPersistenceFailureCode.MALFORMED_REPRESENTATION,
                id="encode_decode_check_corrupt",
            ),
            pytest.param(
                "decode",
                "encode",
                "invalid",
                w.WorkflowPersistenceFailureCode.INVARIANT_VIOLATION,
                id="decode_encode_check_invalid",
            ),
            pytest.param(
                "decode",
                "decode",
                "invalid",
                w.WorkflowPersistenceFailureCode.MALFORMED_REPRESENTATION,
                id="decode_initial_corrupt",
            ),
            pytest.param(
                "encode",
                "encode",
                "incompatible",
                w.WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION,
                id="encode_initial_incompatible",
            ),
            pytest.param(
                "encode",
                "decode",
                "incompatible",
                w.WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION,
                id="encode_decode_check_incompatible",
            ),
            pytest.param(
                "decode",
                "encode",
                "incompatible",
                w.WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION,
                id="decode_encode_check_incompatible",
            ),
            pytest.param(
                "decode",
                "decode",
                "incompatible",
                w.WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION,
                id="decode_initial_incompatible",
            ),
            pytest.param(
                "encode",
                "encode",
                "error",
                w.WorkflowPersistenceFailureCode.CODEC_ERROR,
                id="encode_initial_error",
            ),
            pytest.param(
                "encode",
                "decode",
                "error",
                w.WorkflowPersistenceFailureCode.CODEC_ERROR,
                id="encode_decode_check_error",
            ),
            pytest.param(
                "decode",
                "encode",
                "error",
                w.WorkflowPersistenceFailureCode.CODEC_ERROR,
                id="decode_encode_check_error",
            ),
            pytest.param(
                "decode",
                "decode",
                "error",
                w.WorkflowPersistenceFailureCode.CODEC_ERROR,
                id="decode_initial_error",
            ),
        ],
    )
    def test_method__codec__preserves_returned_foreign_failures(
        self,
        genesis_snapshot: w.WorkflowRunSnapshot,
        operation: Operation,
        phase: Operation,
        status: FailureStatus,
        code: w.WorkflowPersistenceFailureCode,
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-CODEC-FAILURES-001

        Requirement: Initial and counterpart codec failures retain all owning evidence.

        Method: Inject a closed failure into one codec operation, delegating the other.

        Oracle: Independently supplied immutable failure and public status mapping.

        Acceptance: Invalid/corrupt maps to the outer operation; incompatible/error
        remain unchanged. The complete foreign failure is equal and no partial exists.

        Interpretation: Phase and ordered identities remain with the foreign owner.

        Limitations: No exception transport, persistence or scientific claim is tested.
        """
        failure = self.make_failure(code)
        codec = self.FailureCodec(
            encode_failure=w.WorkflowResultValueEncodeResult(
                status=status, failure=failure
            )
            if phase == "encode"
            else None,
            decode_failure=w.WorkflowResultValueDecodeResult(
                status="corrupt" if status == "invalid" else status, failure=failure
            )
            if phase == "decode"
            else None,
        )
        result = self.execute(SUT(result_codec=codec), operation, genesis_snapshot)
        expected = (
            "corrupt" if operation == "decode" and status == "invalid" else status
        )
        assert result.status == expected
        assert result.failure == failure
        self.assert_no_partial(result)

    @pytest.mark.parametrize(
        ("operation", "status", "code"),
        [
            pytest.param(
                "encode",
                "invalid",
                w.WorkflowPersistenceFailureCode.INVARIANT_VIOLATION,
                id="encode_recheck_invalid",
            ),
            pytest.param(
                "decode",
                "invalid",
                w.WorkflowPersistenceFailureCode.INVARIANT_VIOLATION,
                id="decode_recheck_invalid",
            ),
            pytest.param(
                "encode",
                "incompatible",
                w.WorkflowPersistenceFailureCode.UNSUPPORTED_TYPE,
                id="encode_recheck_incompatible",
            ),
            pytest.param(
                "decode",
                "incompatible",
                w.WorkflowPersistenceFailureCode.UNSUPPORTED_TYPE,
                id="decode_recheck_incompatible",
            ),
            pytest.param(
                "encode",
                "error",
                w.WorkflowPersistenceFailureCode.CODEC_ERROR,
                id="encode_recheck_error",
            ),
            pytest.param(
                "decode",
                "error",
                w.WorkflowPersistenceFailureCode.CODEC_ERROR,
                id="decode_recheck_error",
            ),
        ],
    )
    def test_method__codec__preserves_reencoding_failure(
        self,
        genesis_snapshot: w.WorkflowRunSnapshot,
        operation: Operation,
        status: FailureStatus,
        code: w.WorkflowPersistenceFailureCode,
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-CODEC-FAILURES-002

        Requirement: Failure while checking a reconstructed value remains a failure.

        Method: A stateless decoder substitutes a marker value whose encoding returns
        the supplied failure; original-value encoding delegates to the real codec.

        Oracle: Exact supplied failure record and the outer operation's status mapping.

        Acceptance: Complete failure preserved, with no partial run or payload.

        Interpretation: Successful initial encoding/decoding does not bypass rechecking.

        Limitations: The substituted value is a fault, not a valid codec result.
        """
        failure = self.make_failure(code)
        codec = self.FailureCodec(
            encode_failure=w.WorkflowResultValueEncodeResult(
                status=status, failure=failure
            ),
            recheck=True,
        )
        result = self.execute(SUT(result_codec=codec), operation, genesis_snapshot)
        expected = (
            "corrupt" if operation == "decode" and status == "invalid" else status
        )
        assert result.status == expected
        assert result.failure == failure
        self.assert_no_partial(result)

    @pytest.mark.parametrize(
        ("operation", "fault", "code"),
        [
            pytest.param(
                "encode",
                "encode_identity",
                w.WorkflowPersistenceFailureCode.IDENTITY_MISMATCH,
                id="encode_envelope_identity",
            ),
            pytest.param(
                "decode",
                "encode_identity",
                w.WorkflowPersistenceFailureCode.IDENTITY_MISMATCH,
                id="decode_envelope_identity",
            ),
            pytest.param(
                "encode",
                "decode_identity",
                w.WorkflowPersistenceFailureCode.IDENTITY_MISMATCH,
                id="encode_reconstructed_identity",
            ),
            pytest.param(
                "decode",
                "decode_identity",
                w.WorkflowPersistenceFailureCode.IDENTITY_MISMATCH,
                id="decode_reconstructed_identity",
            ),
            pytest.param(
                "encode",
                "content",
                w.WorkflowPersistenceFailureCode.CONTENT_MISMATCH,
                id="encode_changed_value",
            ),
            pytest.param(
                "decode",
                "content",
                w.WorkflowPersistenceFailureCode.CONTENT_MISMATCH,
                id="decode_changed_value",
            ),
        ],
    )
    def test_method__codec__rejects_identity_or_content_disagreement(
        self,
        genesis_snapshot: w.WorkflowRunSnapshot,
        operation: Operation,
        fault: AgreementFault,
        code: w.WorkflowPersistenceFailureCode,
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-CODEC-FAILURES-003

        Requirement: Codec successes must agree on identity and complete content.

        Method: Substitute a typed envelope identity, decoded identity or decoded value.

        Oracle: Public identity/content agreement and aggregate-owned failure context.

        Acceptance: Invalid/corrupt, exact mismatch code, outer phase and input labels,
        and no partial run or payload.

        Interpretation: A reported codec success is insufficient by itself.

        Limitations: No independent mathematical or scientific meaning is established.
        """
        result = self.execute(
            SUT(result_codec=self.AgreementCodec(fault)), operation, genesis_snapshot
        )
        assert result.status == ("invalid" if operation == "encode" else "corrupt")
        assert result.failure is not None and result.failure.code is code
        assert result.failure.phase == operation
        assert (
            result.failure.implementation_identity
            == "ksdft2effmass.workflows.WorkflowRunSerializer:1"
        )
        assert result.failure.input_identities == (
            ("run", "genesis", "genesis-transaction")
            if operation == "encode"
            else ("sha256:" + sha256(self.wire()).hexdigest(),)
        )
        self.assert_no_partial(result)

    @pytest.mark.parametrize(
        ("operation", "phase"),
        [
            pytest.param("encode", "encode", id="encode_wrong_encode_response"),
            pytest.param("encode", "decode", id="encode_wrong_decode_response"),
            pytest.param("decode", "encode", id="decode_wrong_encode_response"),
            pytest.param("decode", "decode", id="decode_wrong_decode_response"),
        ],
    )
    def test_method__codec__rejects_wrong_response_record_type(
        self,
        genesis_snapshot: w.WorkflowRunSnapshot,
        operation: Operation,
        phase: Operation,
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-CODEC-FAILURES-004

        Requirement: Codec responses have exact operation-specific record types.

        Method: Swap encode/decode result-record classes at a narrow fault boundary.

        Oracle: Public exact response contracts and outer malformed/invariant mapping.

        Acceptance: Invalid/corrupt, the aggregate-owned code and no partial result.

        Interpretation: Similar field names cannot substitute for the response contract.

        Limitations: Only the exact typed test return site violates static contracts.
        """
        codec = self.WrongResultCodec(
            phase, self.make_failure(w.WorkflowPersistenceFailureCode.CODEC_ERROR)
        )
        result = self.execute(SUT(result_codec=codec), operation, genesis_snapshot)
        assert result.status == ("invalid" if operation == "encode" else "corrupt")
        assert result.failure is not None
        assert result.failure.code is (
            w.WorkflowPersistenceFailureCode.INVARIANT_VIOLATION
            if operation == "encode"
            else w.WorkflowPersistenceFailureCode.MALFORMED_REPRESENTATION
        )
        self.assert_no_partial(result)

    @pytest.mark.parametrize(
        "operation",
        [
            pytest.param("encode", id="encoding_recursion_limit"),
            pytest.param("decode", id="decoding_recursion_limit"),
        ],
    )
    def test_method__codec__sanitizes_recursion_failure(
        self, genesis_snapshot: w.WorkflowRunSnapshot, operation: Operation
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-CODEC-FAILURES-005

        Requirement: Recursion failure is a sanitized representation-limit error.

        Method: Raise a synthetic RecursionError from the codec without recursive work.

        Oracle: Documented representation-limit classification and diagnostic exclusion.

        Acceptance: Error, representation_limit, outer phase and no detail or partial.

        Interpretation: Resource failure does not become malformed data or success.

        Limitations: This does not measure actual stack, memory or workload limits.
        """
        result = self.execute(
            SUT(result_codec=self.RecursionCodec()), operation, genesis_snapshot
        )
        assert result.status == "error" and result.failure is not None
        assert (
            result.failure.code is w.WorkflowPersistenceFailureCode.REPRESENTATION_LIMIT
        )
        assert result.failure.phase == operation
        assert "synthetic recursion detail" not in result.failure.diagnostic
        self.assert_no_partial(result)
