r"""Software verification of ``WorkflowRunSerializer``.

Bounded artifact scope: initial independent aggregate wire and failure evidence.

Evidence profile: claim_bearing

Facet and represented meaning

Fixed genesis and nonempty wires independently specify canonical aggregate bytes,
complete concrete scalar occurrences, nominal fields, multiplicity and signed zero.

Intrinsic and cross-object scope

Serialization and envelope agreement only; no structural validator, repository,
replay or effect entry. Exhaustive seven-family/closed-variant evidence is pending.

VVUQ and scientific exclusions

Software verification using synthetic records, not physical results or authority.
"""

from dataclasses import FrozenInstanceError, dataclass, replace
from pathlib import Path
from typing import Literal

import pytest

from ksdft2effmass.analysis import (
    NormalizedObservationRequirementIdentity,
    QuantityOfInterestCompleteness,
    QuantityOfInterestConventionIdentity,
    QuantityOfInterestEvaluatorIdentity,
    QuantityOfInterestIdentity,
    QuantityOfInterestResultValueSerializer,
    QuantityOfInterestStateSpaceIdentity,
    QuantityOfInterestSubjectIdentity,
    ScalarQuantityOfInterestDefinition,
    ScalarQuantityOfInterestValue,
)
from ksdft2effmass.application import ApplicationResultValueSerializer
from ksdft2effmass.integration.quantum_espresso import (
    QuantumEspressoResultValueSerializer,
)
from ksdft2effmass.petrinet.colored import (
    ColoredPetriNetBinding,
    ColoredPetriNetColorIdentity,
    ColoredPetriNetMarking,
    ColoredPetriNetPlaceIdentity,
    ColoredPetriNetPlaceMarking,
    ColoredPetriNetSelectionResultIdentity,
    ColoredPetriNetToken,
    ColoredPetriNetTokenIdentity,
    ColoredPetriNetTransitionIdentity,
    ColoredPetriNetValue,
    ColoredPetriNetValueKind,
)
from ksdft2effmass.workflows import (
    AnyOfTaskActivationSelection,
    AttemptIdentity,
    ExternalProducerAttemptIdentity,
    ExternalResultProducer,
    ExternalResultProducerIdentity,
    OperationIdentity,
    ResultObject,
    ResultObjectContentIdentity,
    ResultObjectDomainIdentity,
    ResultObjectIdentity,
    ResultObjectReference,
    ResultObjectReferenceIdentity,
    ResultObjectTypeIdentity,
    ResultProducerEvidenceIdentity,
    ResultProducerProvenanceIdentity,
    TaskActivation,
    TaskActivationIdentity,
    TaskDefinitionIdentity,
    TaskGateSelection,
    TaskInputBinding,
    TaskInstance,
    TaskInstanceIdentity,
    TaskStartGate,
    TaskStartGateIdentity,
    TaskStartGateSet,
    TaskStartGateSetIdentity,
    TaskStartGateSetMode,
    WorkflowEncodedResultValue,
    WorkflowPersistenceFailureCode,
    WorkflowResultValueDecodeResult,
    WorkflowResultValueEncodeResult,
    WorkflowResultValueSerializer,
    WorkflowRun,
    WorkflowRunSerializer,
    WorkflowRunSnapshot,
)

pytestmark = pytest.mark.software_verification
SUT = WorkflowRunSerializer


class TestWorkflowRunSerializer:
    """Initial complete-wire and adversarial representation checks."""

    @dataclass(frozen=True)
    class FaultCodec:
        """Typed operation-failure injection only; never returns placeholder values."""

        fault: Literal["memory", "runtime"]

        def encode(self, value: ResultObject) -> WorkflowResultValueEncodeResult:
            if self.fault == "memory":
                raise MemoryError("not copied to diagnostics")
            raise RuntimeError("not copied to diagnostics")

        def decode(
            self, value: WorkflowEncodedResultValue
        ) -> WorkflowResultValueDecodeResult:
            if self.fault == "memory":
                raise MemoryError("not copied to diagnostics")
            raise RuntimeError("not copied to diagnostics")

    @staticmethod
    def make_serializer() -> WorkflowRunSerializer:
        qe = QuantumEspressoResultValueSerializer()
        return WorkflowRunSerializer(
            result_codec=ApplicationResultValueSerializer(
                workflow_codec=WorkflowResultValueSerializer(source_codec=qe),
                quantum_espresso_codec=qe,
                quantity_of_interest_codec=QuantityOfInterestResultValueSerializer(),
            )
        )

    @staticmethod
    def wire(nonempty: bool = False) -> bytes:
        name = (
            "workflow-run-nonempty-v1.json"
            if nonempty
            else "genesis-record-envelope.json"
        )
        return (Path(__file__).parent / "resources" / name).read_bytes()

    @staticmethod
    def make_scalar() -> ScalarQuantityOfInterestValue:
        evaluator = QuantityOfInterestEvaluatorIdentity("synthetic-evaluator:7")
        return ScalarQuantityOfInterestValue(
            ResultObjectIdentity("synthetic-result"),
            ScalarQuantityOfInterestDefinition(
                QuantityOfInterestIdentity("synthetic-qoi"),
                QuantityOfInterestSubjectIdentity("synthetic-subject"),
                QuantityOfInterestStateSpaceIdentity("synthetic-space"),
                QuantityOfInterestConventionIdentity("synthetic-convention"),
                evaluator,
                (
                    NormalizedObservationRequirementIdentity("second"),
                    NormalizedObservationRequirementIdentity("first"),
                ),
                QuantityOfInterestCompleteness.COMPLETE,
                "synthetic-unit",
            ),
            ResultObjectIdentity("synthetic-observations"),
            evaluator,
            -0.0,
        )

    @classmethod
    def make_nonempty(cls, genesis: WorkflowRun) -> WorkflowRun:
        transition = ColoredPetriNetTransitionIdentity("transition")
        task = TaskInstance(
            TaskInstanceIdentity("task"),
            TaskDefinitionIdentity("task-definition"),
            TaskStartGateSet(
                TaskStartGateSetIdentity("gate-set"),
                TaskStartGateSetMode.ANY_OF,
                (TaskStartGate(TaskStartGateIdentity("gate"), 1 << 80, transition),),
            ),
        )
        scalar = cls.make_scalar()
        activation = TaskActivation(
            TaskActivationIdentity("activation"),
            genesis.workflow_identity,
            genesis.identity,
            task,
            OperationIdentity("operation"),
            AttemptIdentity("attempt"),
            (TaskInputBinding("scalar", scalar),),
            AnyOfTaskActivationSelection(
                TaskStartGateSetIdentity("gate-set"),
                TaskGateSelection(
                    TaskStartGateIdentity("gate"),
                    ColoredPetriNetBinding(transition, ()),
                ),
                ColoredPetriNetSelectionResultIdentity("a" * 64),
            ),
        )
        reference = ResultObjectReference(
            identity=ResultObjectReferenceIdentity("reference"),
            result=scalar,
            concrete_type_identity=ResultObjectTypeIdentity(
                "ksdft2effmass.analysis.ScalarQuantityOfInterestValue:1"
            ),
            owning_domain_identity=ResultObjectDomainIdentity("ksdft2effmass.analysis"),
            content_identity=ResultObjectContentIdentity(
                "qoi-result-value:1:sha256:82f1cc1a48c83ff5e3e8a112ef556608a1f181403302bfffa3731cd4be3a98ab"
            ),
            producer_provenance=ExternalResultProducer(
                identity=ResultProducerProvenanceIdentity("producer"),
                external_producer_identity=ExternalResultProducerIdentity("external"),
                producer_attempt_identity=ExternalProducerAttemptIdentity(
                    "external-attempt"
                ),
                evidence_identities=(ResultProducerEvidenceIdentity("evidence"),),
                limitations=("synthetic software fixture",),
            ),
        )
        zero = ColoredPetriNetToken(
            ColoredPetriNetColorIdentity("color"),
            ColoredPetriNetValue(ColoredPetriNetValueKind.REAL, -0.0),
        )
        text = ColoredPetriNetToken(
            ColoredPetriNetColorIdentity("color"),
            ColoredPetriNetValue(ColoredPetriNetValueKind.STRING, "μ \n"),
            ColoredPetriNetTokenIdentity("identified"),
        )
        marking = ColoredPetriNetMarking(
            genesis.initial_marking.identity,
            genesis.initial_marking.definition_identity,
            (
                ColoredPetriNetPlaceMarking(
                    ColoredPetriNetPlaceIdentity("place"), (zero, zero, text)
                ),
            ),
        )
        return replace(
            genesis,
            task_instances=(task,),
            activations=(activation,),
            result_references=(reference,),
            initial_marking=marking,
            current_marking=marking,
        )

    @pytest.mark.parametrize(
        "nonempty,digest",
        [
            pytest.param(
                False,
                "760cd93744b80ecdefd7fccb0bf0b3145dcc7cd794113154411c626fcd77f456",
                id="complete_genesis",
            ),
            pytest.param(
                True,
                "1fa2eac859f9f030f30a7904fa605d2c4a881bd6b0000116a9007b32e5b8562a",
                id="gates_marking_and_concrete_results",
            ),
        ],
    )
    def test_method__serialize__matches_independent_complete_wire(
        self, genesis_snapshot: WorkflowRunSnapshot, nonempty: bool, digest: str
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-001

        Requirement: Serialize complete records and binding without field loss.

        Method: Encode independently constructed runs and compare fixed wire bytes.

        Oracle: Hand-authored JSON resources and separately fixed SHA-256 digests.

        Acceptance: Exact bytes, schema and content identity match independent literals.

        Interpretation: Repeated concrete results remain complete envelopes.

        Limitations: Exhaustive seven-family/history/authority fixtures are pending.
        """
        run = (
            self.make_nonempty(genesis_snapshot.run)
            if nonempty
            else genesis_snapshot.run
        )
        result = self.make_serializer().serialize(run, genesis_snapshot.binding)
        assert result.status == "encoded", result.failure
        assert result.encoded is not None
        assert result.encoded.payload == self.wire(nonempty)
        assert result.encoded.schema_identity == "ksdft2effmass.workflow-run:1"
        assert (
            result.encoded.content_identity
            == "ksdft2effmass.workflow-run:1:sha256:" + digest
        )

    @pytest.mark.parametrize(
        "nonempty",
        [
            pytest.param(False, id="complete_genesis"),
            pytest.param(True, id="nonempty_concrete_run"),
        ],
    )
    def test_method__deserialize__reconstructs_independent_fields(
        self, genesis_snapshot: WorkflowRunSnapshot, nonempty: bool
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-002

        Requirement: Decode complete nominal records, binding and exact numeric state.

        Method: Decode fixed independent bytes and compare separately built records.

        Oracle: Direct public constructors, complete expected run and fixed binding.

        Acceptance: Full records agree and signed-zero hex/multiplicity are preserved.

        Interpretation: The expected records are not produced by the serializer.

        Limitations: No structural-history or replay-equality claim is made.
        """
        expected = (
            self.make_nonempty(genesis_snapshot.run)
            if nonempty
            else genesis_snapshot.run
        )
        result = self.make_serializer().deserialize(self.wire(nonempty))
        assert result.status == "decoded", result.failure
        assert result.run == expected
        assert result.binding == genesis_snapshot.binding
        if nonempty:
            assert result.run is not None
            tokens = result.run.current_marking.places[0].tokens
            assert tokens[0] == tokens[1]
            assert tokens[0].token_identity is None
            number = tokens[0].value.value
            assert type(number) is float and number.hex() == "-0x0.0p+0"
            scalar = result.run.activations[0].inputs[0].result
            assert type(scalar) is ScalarQuantityOfInterestValue
            assert scalar.value.hex() == "-0x0.0p+0"
            assert scalar.quantity.unit == "synthetic-unit"

    @pytest.mark.parametrize(
        "old,new",
        [
            pytest.param(
                b'"schema":"ksdft2effmass.workflow-run:1"',
                b'"schema":"ksdft2effmass.workflow-run:2"',
                id="aggregate_schema",
            ),
            pytest.param(
                b"WorkflowRunAtomicRepository:1",
                b"WorkflowRunAtomicRepository:2",
                id="historical_writer",
            ),
            pytest.param(
                b'"schema_version":{"fields":{"value":"0x1"}',
                b'"schema_version":{"fields":{"value":"0x2"}',
                id="run_contract",
            ),
            pytest.param(
                b'"type":"TaskInstance"',
                b'"type":"TaskInstance:2"',
                id="nested_record_type",
            ),
            pytest.param(
                b'"schema_identity":"qoi-result-value:1"',
                b'"schema_identity":"qoi-result-value:2"',
                id="concrete_result_schema",
            ),
        ],
    )
    def test_method__deserialize__rejects_unsupported_versions(
        self, old: bytes, new: bytes
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-003

        Requirement: Unknown root, writer, record and value versions are incompatible.

        Method: Change one literal version/type in an otherwise fixed nonempty wire.

        Oracle: Explicit version-one support without dynamic reconstruction.

        Acceptance: Incompatible has failure evidence and no run or binding.

        Interpretation: Unsupported versions are never interpreted as legacy success.

        Limitations: This is initial version evidence, not an exhaustive family matrix.
        """
        wire = self.wire(True)
        assert old in wire
        result = self.make_serializer().deserialize(wire.replace(old, new, 1))
        assert result.status == "incompatible", result.failure
        assert result.run is None and result.binding is None
        assert result.failure is not None

    @pytest.mark.parametrize(
        "mutation",
        [
            pytest.param("newline", id="trailing_newline"),
            pytest.param("duplicate", id="duplicate_root_member"),
            pytest.param("missing", id="missing_commit_binding"),
            pytest.param("extra", id="extra_root_member"),
            pytest.param("integer", id="noncanonical_hex_integer"),
            pytest.param("float", id="noncanonical_float_hex"),
            pytest.param("number", id="raw_numeric_token"),
            pytest.param("nominal", id="wrong_known_nominal_tag"),
            pytest.param("unicode", id="nonascii_wire"),
            pytest.param("base64", id="malformed_concrete_payload"),
        ],
    )
    def test_method__deserialize__rejects_malformed_known_wire(
        self, mutation: str
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-004

        Requirement: Known malformed/noncanonical bytes are corrupt, never success.

        Method: Apply literal grammar/field mutations to fixed complete bytes.

        Oracle: Reviewed ASCII/member/tag/numeric/base64 canonical wire contract.

        Acceptance: Corrupt retains failure evidence and no run or binding.

        Interpretation: JSON parse success alone is insufficient for reconstruction.

        Limitations: Exhaustive nested record corruption matrices remain pending.
        """
        wire = self.wire(True)
        if mutation == "newline":
            wire += b"\n"
        elif mutation == "duplicate":
            wire = b'{"schema":"ksdft2effmass.workflow-run:1",' + wire[1:]
        elif mutation == "missing":
            wire = wire.replace(b'"commit_binding":', b'"missing_binding":', 1)
        elif mutation == "extra":
            wire = b'{"additional":null,' + wire[1:]
        elif mutation == "integer":
            wire = wire.replace(b'"value":"0x1"', b'"value":"0x01"', 1)
        elif mutation == "float":
            wire = wire.replace(b'"value":"-0x0.0p+0"', b'"value":"-0x0.00p+0"', 1)
        elif mutation == "number":
            wire = wire.replace(
                b'"schema_version":{"fields":{"value":"0x1"},"type":"int"}',
                b'"schema_version":1',
                1,
            )
        elif mutation == "nominal":
            wire = wire.replace(
                b'"type":"WorkflowRunIdentity"', b'"type":"WorkflowIdentity"', 1
            )
        elif mutation == "unicode":
            wire = wire.replace(b"\\u03bc", "μ".encode(), 1)
        else:
            wire = wire.replace(
                b'"payload":{"fields":{"value":"', b'"payload":{"fields":{"value":"!', 1
            )
        result = self.make_serializer().deserialize(wire)
        assert result.status == "corrupt", result.failure
        assert result.run is None and result.binding is None
        assert result.failure is not None

    @pytest.mark.parametrize(
        "target",
        [
            pytest.param("occurrence", id="same_result_identity_different_signed_zero"),
            pytest.param("reference", id="detached_reference_content"),
        ],
    )
    def test_method__serialize__rejects_conflicting_result_content(
        self, genesis_snapshot: WorkflowRunSnapshot, target: str
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-005

        Requirement: Repeated result identity and reference metadata must agree exactly.

        Method: Change one scalar occurrence or one reference content label only.

        Oracle: Fixed identical complete envelopes and owning content metadata.

        Acceptance: Invalid content mismatch returns no encoded aggregate.

        Interpretation: Identity equality does not establish exact content equality.

        Limitations: Nested observation-set conflict cases belong to further evidence.
        """
        run = self.make_nonempty(genesis_snapshot.run)
        if target == "occurrence":
            activation = replace(
                run.activations[0],
                inputs=(
                    TaskInputBinding("scalar", replace(self.make_scalar(), value=0.0)),
                ),
            )
            run = replace(run, activations=(activation,))
        else:
            run = replace(
                run,
                result_references=(
                    replace(
                        run.result_references[0],
                        content_identity=ResultObjectContentIdentity("detached"),
                    ),
                ),
            )
        result = self.make_serializer().serialize(run, genesis_snapshot.binding)
        assert result.status == "invalid"
        assert result.encoded is None
        assert result.failure is not None
        assert result.failure.code is WorkflowPersistenceFailureCode.CONTENT_MISMATCH

    def test_method__serialize__binds_transaction_label(
        self, genesis_snapshot: WorkflowRunSnapshot
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-006

        Requirement: The durable transaction label participates in payload content.

        Method: Encode the fixed run with a changed transaction label only.

        Oracle: Independent literal substitution in the fixed genesis root binding.

        Acceptance: New exact bytes contain that substitution and content changes.

        Interpretation: Transaction identity is recoverable from durable run bytes.

        Limitations: No store commit or receipt derivation is performed.
        """
        binding = replace(genesis_snapshot.binding, transaction_identity="changed")
        result = self.make_serializer().serialize(genesis_snapshot.run, binding)
        assert result.encoded is not None
        assert result.encoded.payload == self.wire().replace(
            b'"genesis-transaction"', b'"changed"'
        )
        assert result.encoded.content_identity != genesis_snapshot.revision.content_id

    @pytest.mark.parametrize(
        "value",
        [
            pytest.param("{}", id="text_not_bytes"),
            pytest.param(bytearray(b"{}"), id="mutable_payload"),
            pytest.param(False, id="boolean_payload"),
        ],
    )
    def test_method__deserialize__rejects_wrong_direct_types(
        self, value: str | bytearray | bool
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-007

        Requirement: Direct encoded inputs must be exact immutable bytes.

        Method: Pass closed wrong semantic types at the intentional invalid call.

        Oracle: Exact bytes API contract, distinct from known-wire corruption.

        Acceptance: Each call raises TypeError rather than coercing or decoding.

        Interpretation: Public Python inputs do not inherit wire conversion permissions.

        Limitations: These partitions do not enumerate every Python object.
        """
        with pytest.raises(TypeError):
            self.make_serializer().deserialize(value)  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        "fault,code",
        [
            pytest.param(
                "memory",
                WorkflowPersistenceFailureCode.REPRESENTATION_LIMIT,
                id="allocation_failure",
            ),
            pytest.param(
                "runtime",
                WorkflowPersistenceFailureCode.CODEC_ERROR,
                id="codec_operation_failure",
            ),
        ],
    )
    def test_method__serialize__represents_operational_errors(
        self,
        genesis_snapshot: WorkflowRunSnapshot,
        fault: Literal["memory", "runtime"],
        code: WorkflowPersistenceFailureCode,
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-009

        Requirement: Codec exceptions produce sanitized errors without partial bytes.

        Method: Inject a typed failing codec while traversing a concrete-result run.

        Oracle: Closed allocation/operational error codes and explicit input identities.

        Acceptance: Error has the expected code, bound inputs and no exception text.

        Interpretation: Operational failure is neither invalid science nor success.

        Limitations: No process failure, store I/O or native executable is involved.
        """
        serializer = WorkflowRunSerializer(result_codec=self.FaultCodec(fault))
        result = serializer.serialize(
            self.make_nonempty(genesis_snapshot.run), genesis_snapshot.binding
        )
        assert result.status == "error" and result.encoded is None
        assert result.failure is not None and result.failure.code is code
        assert result.failure.input_identities == (
            "run",
            "genesis",
            "genesis-transaction",
        )
        assert "not copied" not in result.failure.diagnostic

    @pytest.mark.parametrize(
        "fault,code",
        [
            pytest.param(
                "memory",
                WorkflowPersistenceFailureCode.REPRESENTATION_LIMIT,
                id="allocation_failure",
            ),
            pytest.param(
                "runtime",
                WorkflowPersistenceFailureCode.CODEC_ERROR,
                id="codec_operation_failure",
            ),
        ],
    )
    def test_method__deserialize__represents_operational_errors(
        self, fault: Literal["memory", "runtime"], code: WorkflowPersistenceFailureCode
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-010

        Requirement: Decode exceptions produce sanitized errors without partial runs.

        Method: Inject a typed failing codec while decoding independent fixed bytes.

        Oracle: Closed error codes and fixed input payload SHA-256 identity.

        Acceptance: Error retains the code/input digest and no run or binding.

        Interpretation: Error does not imply corruption, absence or recovered state.

        Limitations: No store read or historical receipt operation is exercised.
        """
        result = WorkflowRunSerializer(result_codec=self.FaultCodec(fault)).deserialize(
            self.wire(True)
        )
        assert (
            result.status == "error" and result.run is None and result.binding is None
        )
        assert result.failure is not None and result.failure.code is code
        assert result.failure.input_identities == (
            "sha256:1fa2eac859f9f030f30a7904fa605d2c4a881bd6b0000116a9007b32e5b8562a",
        )
        assert "not copied" not in result.failure.diagnostic

    @pytest.mark.parametrize(
        "target",
        [
            pytest.param("run", id="unknown_run_version"),
            pytest.param("writer", id="unknown_writer_version"),
        ],
    )
    def test_method__serialize__rejects_unsupported_versions(
        self, genesis_snapshot: WorkflowRunSnapshot, target: str
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-011

        Requirement: Encoding recognizes only run and historical writer version one.

        Method: Change one supported record's version label before encoding.

        Oracle: Explicit supported run/writer contract, not an inferred legacy mode.

        Acceptance: Incompatible carries version failure and no encoded payload.

        Interpretation: The supplied historical writer is not replaced by this reader.

        Limitations: No store or scientific version selection is exercised.
        """
        run = genesis_snapshot.run
        binding = genesis_snapshot.binding
        if target == "run":
            run = replace(run, schema_version=2)
        else:
            binding = replace(
                binding, persistence_implementation_identity="future-writer:2"
            )
        result = self.make_serializer().serialize(run, binding)
        assert result.status == "incompatible" and result.encoded is None
        assert result.failure is not None
        assert result.failure.code is WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION

    @pytest.mark.parametrize(
        "target",
        [
            pytest.param("run", id="run_identity_only"),
            pytest.param("binding", id="binding_label_only"),
            pytest.param("codec", id="codec_label_only"),
        ],
    )
    def test_method__serialize__rejects_wrong_direct_types(
        self, genesis_snapshot: WorkflowRunSnapshot, target: str
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-012

        Requirement: Direct run, binding and codec inputs have exact semantic types.

        Method: Supply an identifying string rather than the complete input or port.

        Oracle: Explicit serializer API and injected-codec protocol contracts.

        Acceptance: Each wrong semantic type raises TypeError before traversal.

        Interpretation: Labels do not replace complete immutable input records.

        Limitations: This is not arbitrary implementation support evidence.
        """
        with pytest.raises(TypeError):
            if target == "run":
                self.make_serializer().serialize("run", genesis_snapshot.binding)  # type: ignore[arg-type]
            elif target == "binding":
                self.make_serializer().serialize(genesis_snapshot.run, "binding")  # type: ignore[arg-type]
            else:
                WorkflowRunSerializer(result_codec="codec")  # type: ignore[arg-type]

    def test_field__result_codec__is_immutable(self) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-008

        Requirement: The serializer retains an immutable explicit codec dependency.

        Method: Attempt reassigning its configured port.

        Oracle: Frozen dataclass semantics, with no ambient registry or cache.

        Acceptance: Assignment raises FrozenInstanceError.

        Interpretation: Callers cannot silently replace codec behavior in place.

        Limitations: The injected implementation itself must obey its port contract.
        """
        serializer = self.make_serializer()
        with pytest.raises(FrozenInstanceError):
            serializer.result_codec = serializer.result_codec  # type: ignore[misc]
