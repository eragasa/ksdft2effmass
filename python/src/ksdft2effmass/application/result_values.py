"""Explicit seven-family result codec composition, not an application root.

Three named immutable dependencies own their concrete wires. This module only routes
exact supported classes and type labels; it performs no discovery, registration,
configuration resolution, database selection, native I/O, effects or scientific work.
Unknown result families and versions cannot be reconstructed as protocol stand-ins.
"""

from dataclasses import dataclass

from ksdft2effmass.analysis import (
    QuantityOfInterestResultValueSerializer,
    ScalarQuantityOfInterestEvaluationFailure,
    ScalarQuantityOfInterestValue,
)
from ksdft2effmass.integration.quantum_espresso import (
    QuantumEspressoBandsResult,
    QuantumEspressoExtractedObservationResult,
    QuantumEspressoPwResult,
    QuantumEspressoResultValueSerializer,
)
from ksdft2effmass.workflows import (
    NormalizedObservationSet,
    ResultObject,
    ResultObjectIdentity,
    ScientificDecisionResolution,
    WorkflowEncodedResultValue,
    WorkflowPersistenceFailure,
    WorkflowPersistenceFailureCode,
    WorkflowResultValueDecodeResult,
    WorkflowResultValueEncodeResult,
    WorkflowResultValueSerializer,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class ApplicationResultValueSerializer:
    """Compose seven exact concrete result families through three named codecs.

    Parameters
    ----------
    workflow_codec
        Exact frozen Workflow serializer. Its source dependency must be an exact
        ``QuantumEspressoResultValueSerializer``, preventing arbitrary nested source
        implementations. Independently constructed instances of this stateless
        immutable codec are equivalent; object identity is not a wire contract.
    quantum_espresso_codec
        Exact frozen QE serializer for PW, bands and extracted observations.
    quantity_of_interest_codec
        Exact frozen scalar success/failure serializer.

    Raises
    ------
    TypeError
        A dependency, including the Workflow source codec, is not the exact
        supported concrete immutable serializer.

    Notes
    -----
    Explicit branches preserve owning wire/schema/content labels and closed failure
    results without wrapping successful values or replacing diagnostics. No registry,
    mutable cache, ambient configuration or automatic implementation discovery exists.
    Complete repeated-identity agreement across a run belongs to the aggregate codec;
    each occurrence here remains a complete envelope, including nested observations.
    This class does not build the separately planned application composition root.
    """

    workflow_codec: WorkflowResultValueSerializer
    quantum_espresso_codec: QuantumEspressoResultValueSerializer
    quantity_of_interest_codec: QuantityOfInterestResultValueSerializer

    def __post_init__(self) -> None:
        """Require the three exact immutable owners and the selected source family."""
        if type(self.workflow_codec) is not WorkflowResultValueSerializer:
            raise TypeError("workflow_codec must be WorkflowResultValueSerializer")
        if (
            type(self.quantum_espresso_codec)
            is not QuantumEspressoResultValueSerializer
        ):
            raise TypeError(
                "quantum_espresso_codec must be QuantumEspressoResultValueSerializer"
            )
        if (
            type(self.quantity_of_interest_codec)
            is not QuantityOfInterestResultValueSerializer
        ):
            raise TypeError(
                "quantity_of_interest_codec must be "
                "QuantityOfInterestResultValueSerializer"
            )
        if (
            type(self.workflow_codec.source_codec)
            is not QuantumEspressoResultValueSerializer
        ):
            raise TypeError(
                "Workflow source codec must be QuantumEspressoResultValueSerializer"
            )

    def encode(self, value: ResultObject) -> WorkflowResultValueEncodeResult:
        """Delegate one exact supported result to its owning codec.

        Parameters
        ----------
        value
            Workflow-facing result, not a promise of serialization support.

        Returns
        -------
        WorkflowResultValueEncodeResult
            Owning complete envelope or closed failure; unsupported exact types and
            subclasses return incompatible without discovery or coercion.

        Raises
        ------
        TypeError
            Input does not expose an exact nominal ResultObject identity.
        """
        if (
            not isinstance(value, ResultObject)
            or type(value.identity) is not ResultObjectIdentity
        ):
            raise TypeError("value must expose an exact ResultObjectIdentity")
        if (
            type(value) is ScientificDecisionResolution
            or type(value) is NormalizedObservationSet
        ):
            return self.workflow_codec.encode(value)
        if (
            type(value) is QuantumEspressoPwResult
            or type(value) is QuantumEspressoBandsResult
            or type(value) is QuantumEspressoExtractedObservationResult
        ):
            return self.quantum_espresso_codec.encode(value)
        if (
            type(value) is ScalarQuantityOfInterestValue
            or type(value) is ScalarQuantityOfInterestEvaluationFailure
        ):
            return self.quantity_of_interest_codec.encode(value)
        return WorkflowResultValueEncodeResult(
            status="incompatible",
            failure=self._failure("encode", (value.identity.value,)),
        )

    def decode(
        self, value: WorkflowEncodedResultValue
    ) -> WorkflowResultValueDecodeResult:
        """Delegate only explicitly supported concrete type labels.

        Parameters
        ----------
        value
            Complete exact byte-bound envelope, including owning schema and domain.

        Returns
        -------
        WorkflowResultValueDecodeResult
            Complete concrete value or owning incompatible/corrupt/error evidence.
            Unknown type labels are incompatible; selected owners validate schemas,
            domain/content binding and complete nested reconstruction.

        Raises
        ------
        TypeError
            Input is not an exact WorkflowEncodedResultValue.
        """
        if type(value) is not WorkflowEncodedResultValue:
            raise TypeError("value must be WorkflowEncodedResultValue")
        label = value.concrete_type_identity.value
        if label in (
            "ksdft2effmass.workflows.ScientificDecisionResolution:1",
            "ksdft2effmass.workflows.NormalizedObservationSet:1",
        ):
            return self.workflow_codec.decode(value)
        if label in (
            "ksdft2effmass.integration.quantum_espresso.QuantumEspressoPwResult:1",
            "ksdft2effmass.integration.quantum_espresso.QuantumEspressoBandsResult:1",
            "ksdft2effmass.integration.quantum_espresso.QuantumEspressoExtractedObservationResult:1",
        ):
            return self.quantum_espresso_codec.decode(value)
        if label in (
            "ksdft2effmass.analysis.ScalarQuantityOfInterestValue:1",
            "ksdft2effmass.analysis.ScalarQuantityOfInterestEvaluationFailure:1",
        ):
            return self.quantity_of_interest_codec.decode(value)
        return WorkflowResultValueDecodeResult(
            status="incompatible",
            failure=self._failure(
                "decode", (value.result_identity.value, value.schema_identity, label)
            ),
        )

    @staticmethod
    def _failure(phase: str, identities: tuple[str, ...]) -> WorkflowPersistenceFailure:
        return WorkflowPersistenceFailure(
            implementation_identity="ksdft2effmass.application.ApplicationResultValueSerializer:1",
            phase=phase,
            code=WorkflowPersistenceFailureCode.UNSUPPORTED_TYPE,
            input_identities=identities,
            expected="one of seven explicitly supported exact concrete result families",
            observed="unsupported_type",
            diagnostic="application result codec has no selected concrete branch",
            claim_boundary="software representation only; no discovery or science",
        )
