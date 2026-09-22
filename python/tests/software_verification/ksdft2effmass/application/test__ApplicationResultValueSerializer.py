r"""Software verification of ``ApplicationResultValueSerializer``.

Bounded artifact scope: explicit immutable seven-family codec composition.

Evidence profile: claim_bearing

Facet and represented meaning

Seven fixed literal wires establish outward routing and complete nested agreement.

Intrinsic and cross-object scope

This codec binds three exact owners and routes concrete types without discovery.
Owning codecs retain complete field, precision and invariant evidence separately.

VVUQ and scientific exclusions

Software verification only; no composition root, aggregate repository, scientific
execution, numerical validation, authority or human acceptance is established.
"""

import base64
import hashlib
import json
from dataclasses import FrozenInstanceError, dataclass, replace
from pathlib import Path
from typing import cast
from unittest.mock import patch

import pytest

from ksdft2effmass.analysis import (
    QuantityOfInterestResultValueSerializer,
    ScalarQuantityOfInterestEvaluationFailure,
    ScalarQuantityOfInterestValue,
)
from ksdft2effmass.application import ApplicationResultValueSerializer
from ksdft2effmass.integration.quantum_espresso import (
    QuantumEspressoBandsResult,
    QuantumEspressoExtractedObservationResult,
    QuantumEspressoPwResult,
    QuantumEspressoResultValueSerializer,
)
from ksdft2effmass.workflows import (
    NormalizedObservationSet,
    ResultObjectContentIdentity,
    ResultObjectDomainIdentity,
    ResultObjectIdentity,
    ResultObjectTypeIdentity,
    ScientificDecisionResolution,
    WorkflowEncodedResultValue,
    WorkflowPersistenceFailure,
    WorkflowPersistenceFailureCode,
    WorkflowResultValueCodec,
    WorkflowResultValueDecodeResult,
    WorkflowResultValueSerializer,
)

pytestmark = pytest.mark.software_verification
SUT = ApplicationResultValueSerializer
type SupportedValue = (
    ScientificDecisionResolution
    | NormalizedObservationSet
    | QuantumEspressoPwResult
    | QuantumEspressoBandsResult
    | QuantumEspressoExtractedObservationResult
    | ScalarQuantityOfInterestValue
    | ScalarQuantityOfInterestEvaluationFailure
)
type JsonValue = None | bool | str | list[JsonValue] | dict[str, JsonValue]


class TestApplicationResultValueSerializer:
    """Actual domain codecs, not stand-ins for the selected seven families."""

    @staticmethod
    def make_codec() -> ApplicationResultValueSerializer:
        qe = QuantumEspressoResultValueSerializer()
        return ApplicationResultValueSerializer(
            workflow_codec=WorkflowResultValueSerializer(source_codec=qe),
            quantum_espresso_codec=qe,
            quantity_of_interest_codec=QuantityOfInterestResultValueSerializer(),
        )

    @staticmethod
    def fixture_envelope(family: str) -> WorkflowEncodedResultValue:
        root = Path(__file__).parents[1]
        manifest = cast(
            dict[str, dict[str, str]],
            json.loads(
                Path(__file__)
                .with_name("resources")
                .joinpath("result-values-v1.json")
                .read_bytes()
            ),
        )
        entry = manifest[family]
        payload = root.joinpath(entry["path"]).read_bytes()
        assert hashlib.sha256(payload).hexdigest() == entry["payload_digest"]
        return WorkflowEncodedResultValue(
            result_identity=ResultObjectIdentity(entry["result_identity"]),
            concrete_type_identity=ResultObjectTypeIdentity(
                entry["concrete_type_identity"]
            ),
            owning_domain_identity=ResultObjectDomainIdentity(
                entry["owning_domain_identity"]
            ),
            schema_identity=entry["schema_identity"],
            content_identity=ResultObjectContentIdentity(entry["content_identity"]),
            payload=payload,
            payload_digest=entry["payload_digest"],
        )

    @pytest.mark.parametrize(
        "family,expected_type",
        [
            pytest.param(
                "decision", ScientificDecisionResolution, id="scientific_decision"
            ),
            pytest.param("set", NormalizedObservationSet, id="normalized_set"),
            pytest.param("pw", QuantumEspressoPwResult, id="qe_pw"),
            pytest.param("bands", QuantumEspressoBandsResult, id="qe_bands"),
            pytest.param(
                "observation",
                QuantumEspressoExtractedObservationResult,
                id="qe_observation",
            ),
            pytest.param("scalar", ScalarQuantityOfInterestValue, id="scalar_success"),
            pytest.param(
                "failure",
                ScalarQuantityOfInterestEvaluationFailure,
                id="scalar_failure",
            ),
        ],
    )
    def test_method__codec__routes_seven_independent_literal_families(
        self, family: str, expected_type: type[SupportedValue]
    ) -> None:
        """Evidence ID: SV-APPLICATION-RESULT-CODEC-001

        Requirement: Exactly seven concrete families route to their actual owners.

        Method: Decode each independently fixed wire and encode its concrete result.

        Oracle: Literal payloads and fixed metadata manifest, not generated round trips.

        Acceptance: Exact concrete type, result identity and complete envelope agree.

        Interpretation: Both routes retain complete owning envelopes unchanged.

        Limitations: Domain codec tests own independent complete-field reconstruction.
        """
        envelope = self.fixture_envelope(family)
        codec = self.make_codec()
        decoded = codec.decode(envelope)
        assert decoded.status == "decoded"
        assert type(decoded.value) is expected_type
        assert decoded.value is not None
        assert decoded.value.identity == envelope.result_identity
        encoded = codec.encode(decoded.value)
        assert encoded.status == "encoded"
        assert encoded.encoded == envelope

    def test_method__codec__retains_nested_and_standalone_identity_agreement(
        self,
    ) -> None:
        """Evidence ID: SV-APPLICATION-RESULT-CODEC-002

        Requirement: Repeated source occurrences retain identical complete envelopes.

        Method: Encode a set's source standalone and compare its literal nested
        envelope.

        Oracle: Fixed source-z metadata and exact decoded base64 in the set fixture.

        Acceptance: Every standalone envelope field equals its nested occurrence.

        Interpretation: Composition does not replace repeated values with identities.

        Limitations: Future aggregate traversal owns rejection across run occurrences.
        """
        codec = self.make_codec()
        envelope = self.fixture_envelope("set")
        decoded = codec.decode(envelope)
        assert type(decoded.value) is NormalizedObservationSet
        source = decoded.value.sources[0]
        encoded = codec.encode(source).encoded
        assert encoded is not None
        wire = cast(dict[str, JsonValue], json.loads(envelope.payload))
        fields = wire["fields"]
        assert isinstance(fields, dict)
        sources = fields["sources"]
        assert isinstance(sources, list)
        first = sources[0]
        assert isinstance(first, dict)
        nested = first["fields"]
        assert isinstance(nested, dict)
        payload_record = nested["payload"]
        assert isinstance(payload_record, dict)
        payload_fields = payload_record["fields"]
        assert isinstance(payload_fields, dict)
        text = payload_fields["value"]
        assert isinstance(text, str)
        payload = base64.b64decode(text, validate=True)
        digest = hashlib.sha256(payload).hexdigest()
        assert encoded == WorkflowEncodedResultValue(
            result_identity=ResultObjectIdentity("source-z"),
            concrete_type_identity=ResultObjectTypeIdentity(
                "ksdft2effmass.integration.quantum_espresso.QuantumEspressoExtractedObservationResult:1"
            ),
            owning_domain_identity=ResultObjectDomainIdentity(
                "ksdft2effmass.integration.quantum_espresso"
            ),
            schema_identity="qe-result-value:1",
            content_identity=ResultObjectContentIdentity(
                f"qe-result-value:1:sha256:{digest}"
            ),
            payload=payload,
            payload_digest=digest,
        )
        repeated = codec.decode(encoded)
        assert repeated.status == "decoded"
        assert repeated.value is not None
        assert codec.encode(repeated.value).encoded == encoded

    def test_method__encode__distinguishes_equal_identity_changed_content(self) -> None:
        """Evidence ID: SV-APPLICATION-RESULT-CODEC-003

        Requirement: Equal identities with different content must remain
        distinguishable.

        Method: Encode negative and positive zero under the same scalar identity.

        Oracle: Fixed scalar literal contains negative-zero hexadecimal representation.

        Acceptance: Identity agrees but exact payload, digest and content
        identity differ.

        Interpretation: No identity cache or lossy identity substitution hides
        differences.

        Limitations: This codec has no multi-occurrence run context to reject a pair.
        """
        codec = self.make_codec()
        envelope = self.fixture_envelope("scalar")
        decoded = codec.decode(envelope)
        assert type(decoded.value) is ScalarQuantityOfInterestValue
        assert decoded.value.value.hex() == "-0x0.0p+0"
        changed = codec.encode(replace(decoded.value, value=0.0)).encoded
        assert changed is not None
        assert changed.result_identity == envelope.result_identity
        assert changed.payload == envelope.payload.replace(b"-0x0.0p+0", b"0x0.0p+0")
        assert changed.payload_digest != envelope.payload_digest
        assert changed.content_identity != envelope.content_identity

    @pytest.mark.parametrize(
        "family",
        [
            pytest.param("decision", id="workflow_owner"),
            pytest.param("pw", id="qe_owner"),
            pytest.param("scalar", id="analysis_owner"),
        ],
    )
    def test_method__decode__preserves_unknown_schema_incompatibility(
        self, family: str
    ) -> None:
        """Evidence ID: SV-APPLICATION-RESULT-CODEC-004

        Requirement: Outward owners retain their unknown-schema incompatibility.

        Method: Route each owning domain's valid envelope with an unsupported schema.

        Oracle: Only the three declared version-one schemas have selected
        implementations.

        Acceptance: Incompatible with unsupported-version evidence and no value.

        Interpretation: Application does not mask or reinterpret owning failures.

        Limitations: Future schema support requires explicit owner implementation.
        """
        decoded = self.make_codec().decode(
            replace(self.fixture_envelope(family), schema_identity="future:2")
        )
        assert decoded.status == "incompatible"
        assert decoded.value is None
        assert decoded.failure is not None
        assert (
            decoded.failure.code == WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION
        )

    def test_method__decode__rejects_unknown_concrete_type(self) -> None:
        """Evidence ID: SV-APPLICATION-RESULT-CODEC-005

        Requirement: Unknown type versions have no dynamically discovered fallback.

        Method: Route a valid payload under an unimplemented concrete version label.

        Oracle: The application uses seven explicit version-one type labels only.

        Acceptance: Incompatible application failure and no value.

        Interpretation: Owning payload plausibility cannot create version support.

        Limitations: This does not define a future migration policy.
        """
        decoded = self.make_codec().decode(
            replace(
                self.fixture_envelope("decision"),
                concrete_type_identity=ResultObjectTypeIdentity(
                    "ksdft2effmass.workflows.ScientificDecisionResolution:2"
                ),
            )
        )
        assert decoded.status == "incompatible"
        assert decoded.value is None
        assert decoded.failure is not None
        assert (
            decoded.failure.implementation_identity
            == "ksdft2effmass.application.ApplicationResultValueSerializer:1"
        )

    def test_method__encode__rejects_arbitrary_protocol_values(self) -> None:
        """Evidence ID: SV-APPLICATION-RESULT-CODEC-006

        Requirement: ResultObject identity conformance alone cannot select a branch.

        Method: Encode a local immutable identity-only protocol implementation.

        Oracle: Selected exact concrete families exclude anonymous result substitutes.

        Acceptance: Incompatible outcome contains no envelope.

        Interpretation: No registry or reflection extends the selected coverage.

        Limitations: This tests software support, not scientific result admissibility.
        """

        @dataclass(frozen=True)
        class IdentityOnly:
            identity: ResultObjectIdentity

        result = self.make_codec().encode(
            IdentityOnly(ResultObjectIdentity("synthetic-result"))
        )
        assert result.status == "incompatible"
        assert result.encoded is None

    def test_field__dependencies__are_named_immutable_and_correlated(self) -> None:
        """Evidence ID: SV-APPLICATION-RESULT-CODEC-007

        Requirement: Three named immutable dependencies bind the exact QE source owner.

        Method: Inspect bindings, reject reassignment and substitute a wrong source.

        Oracle: Frozen fields and exact Workflow-source/QE concrete-family contract.

        Acceptance: Reassignment and wrong source reject; equivalent QE instances work.

        Interpretation: No ambient configuration, registry or mutable cache is required.

        Limitations: This is minimal codec composition, not an application root.
        """
        codec = self.make_codec()
        assert isinstance(codec, WorkflowResultValueCodec)
        assert codec.workflow_codec.source_codec is codec.quantum_espresso_codec
        with pytest.raises(FrozenInstanceError):
            codec.quantum_espresso_codec = QuantumEspressoResultValueSerializer()  # type: ignore[misc]
        equivalent = replace(
            codec, quantum_espresso_codec=QuantumEspressoResultValueSerializer()
        )
        assert equivalent.decode(self.fixture_envelope("set")).status == "decoded"
        with pytest.raises(TypeError, match="Workflow source codec"):
            replace(
                codec,
                workflow_codec=WorkflowResultValueSerializer(
                    source_codec=QuantityOfInterestResultValueSerializer()
                ),
            )

    @pytest.mark.parametrize(
        "invalid",
        [
            pytest.param(None, id="null"),
            pytest.param("codec", id="text"),
            pytest.param(True, id="boolean"),
        ],
    )
    def test_method__codec__rejects_wrong_direct_types(
        self, invalid: None | str | bool
    ) -> None:
        """Evidence ID: SV-APPLICATION-RESULT-CODEC-008

        Requirement: Direct semantic type violations raise TypeError without coercion.

        Method: Supply closed invalid inputs to both operations and each dependency.

        Oracle: Exact immutable dependency, result identity and envelope contracts.

        Acceptance: Every invalid direct call raises TypeError.

        Interpretation: Untyped representations never become domain values implicitly.

        Limitations: Intentional static violations are isolated at exact call sites.
        """
        codec = self.make_codec()
        with pytest.raises(TypeError):
            codec.encode(invalid)  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            codec.decode(invalid)  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            replace(codec, workflow_codec=invalid)  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            replace(codec, quantum_espresso_codec=invalid)  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            replace(codec, quantity_of_interest_codec=invalid)  # type: ignore[arg-type]

    def test_method__decode__preserves_complete_owning_failure(self) -> None:
        """Evidence ID: SV-APPLICATION-RESULT-CODEC-009

        Requirement: Application routing preserves the exact owning failure result.

        Method: Inject a closed QE operational failure and decode through application.

        Oracle: Independently constructed status and complete diagnostic record.

        Acceptance: The same failure result is returned without a partial value.

        Interpretation: Composition neither sanitizes away nor invents owner evidence.

        Limitations: This controlled fault is not a scientific or resource-limit result.
        """
        failure = WorkflowPersistenceFailure(
            implementation_identity="qe-test:1",
            phase="decode",
            code=WorkflowPersistenceFailureCode.CODEC_ERROR,
            input_identities=("synthetic-result",),
            expected="complete result",
            observed="operation failed",
            diagnostic="sanitized",
            claim_boundary="software only",
        )
        expected = WorkflowResultValueDecodeResult(status="error", failure=failure)
        with patch.object(
            QuantumEspressoResultValueSerializer, "decode", return_value=expected
        ):
            result = self.make_codec().decode(self.fixture_envelope("pw"))
        assert result is expected
        assert result.value is None

    def test_public_api__package__exports_only_minimal_codec(self) -> None:
        """Evidence ID: SV-APPLICATION-RESULT-CODEC-010

        Requirement: The new application package exposes only its minimal codec.

        Method: Inspect the supported public package inventory and concrete export.

        Oracle: Exactly ApplicationResultValueSerializer, not a root or registry.

        Acceptance: Exact export inventory and imported class agree.

        Interpretation: This chunk does not claim application composition completion.

        Limitations: No dependency-direction claim is inferred from export presence.
        """
        import ksdft2effmass.application as application

        assert application.__all__ == ["ApplicationResultValueSerializer"]
        assert (
            application.ApplicationResultValueSerializer
            is ApplicationResultValueSerializer
        )
