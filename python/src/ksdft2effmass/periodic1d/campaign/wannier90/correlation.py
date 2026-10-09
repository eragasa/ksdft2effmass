"""Authenticate and correlate retained periodic-1D Wannier90 campaign documents.

The Workflow binds one exact composite campaign input to one retained Wannier90 result.
It authenticates the still-opaque input bytes against the SHA-256 declared by the
strictly decoded result *before* deserializing input-owned scientific controls. It then
checks the ordered retained-band inventory. No native file is inferred, discovered, or
parsed here, and no calculator is executed.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from ksdft2effmass.periodic1d.campaign.composite import (
    Periodic1DCompositeCampaignDefinition,
    Periodic1DCompositeCampaignJsonSerializer,
)
from ksdft2effmass.periodic1d.campaign.result_documents import (
    Periodic1DEncodedResultJsonSerializer,
    Periodic1DEncodedResultKind,
)
from ksdft2effmass.periodic1d.campaign.serialization import (
    Periodic1DCampaignJsonDecoder,
)

from .results import (
    Periodic1DWannier90CampaignResult,
    Periodic1DWannier90ResultJsonSerializer,
)

_SUPPORTED_RESULT_KINDS = frozenset(
    {
        Periodic1DEncodedResultKind.WANNIER90,
        Periodic1DEncodedResultKind.WANNIER90_PRECONDITIONED,
    }
)


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90CampaignWorkflowRequest:
    """Provide exact retained wires and an explicit result-wire discriminator.

    Parameters
    ----------
    composite_input_payload
        Nonempty exact built-in bytes for the version-one composite campaign input.
    result_payload
        Nonempty exact built-in bytes for one retained Wannier90 campaign result.
    result_kind
        Explicit wire identity. Only ``WANNIER90`` and
        ``WANNIER90_PRECONDITIONED`` are supported; content and filenames are never
        used to infer this value.

    Raises
    ------
    TypeError
        If either payload or ``result_kind`` has the wrong exact representation.
    ValueError
        If a payload is empty or the result kind belongs to another campaign family.

    Notes
    -----
    This request carries persistence representations, not a physical model, native
    artifact inventory, provenance proof, convergence decision, or execution authority.
    """

    composite_input_payload: bytes
    result_payload: bytes
    result_kind: Periodic1DEncodedResultKind

    def __post_init__(self) -> None:
        """Validate exact payload representations and supported wire identity."""
        self._check_args_payloads()
        self._check_args_result_kind()

    def _check_args_payloads(self) -> None:
        """Require nonempty exact built-in bytes for both retained documents.

        Raises
        ------
        TypeError
            If either payload is not exact built-in :class:`bytes`.
        ValueError
            If either exact byte payload is empty.
        """
        for name, payload in (
            ("composite_input_payload", self.composite_input_payload),
            ("result_payload", self.result_payload),
        ):
            if type(payload) is not bytes:
                raise TypeError(f"{name} must be built-in bytes")
            if not payload:
                raise ValueError(f"{name} must be nonempty")

    def _check_args_result_kind(self) -> None:
        """Require one exact supported Wannier90 result-wire discriminator.

        Raises
        ------
        TypeError
            If ``result_kind`` is not exactly :class:`Periodic1DEncodedResultKind`.
        ValueError
            If it identifies a non-Wannier90 campaign wire.
        """
        if type(self.result_kind) is not Periodic1DEncodedResultKind:
            raise TypeError("result_kind must be Periodic1DEncodedResultKind")
        if self.result_kind not in _SUPPORTED_RESULT_KINDS:
            raise ValueError("result_kind must identify a supported Wannier90 result")


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90CampaignWorkflowResult:
    """Retain authenticated controls, typed observations, and exact wire identities.

    Parameters
    ----------
    composite_definition
        Strictly decoded composite campaign controls authenticated by
        ``composite_input_sha256``.
    campaign_result
        Typed Wilson-center observations adapted from the retained result wire.
    composite_input_sha256, result_sha256
        Lowercase SHA-256 content identities of the exact input and result bytes.

    Raises
    ------
    TypeError
        If either semantic record has the wrong exact type.
    ValueError
        If a digest is malformed or ``result_sha256`` disagrees with the exact source
        identity retained by ``campaign_result``.

    Notes
    -----
    The Result preserves campaign evidence; it is not a represented operator,
    effective model, provenance attestation, scientific validation, uncertainty
    statement, or acceptance record.
    """

    composite_definition: Periodic1DCompositeCampaignDefinition
    campaign_result: Periodic1DWannier90CampaignResult
    composite_input_sha256: str
    result_sha256: str

    def __post_init__(self) -> None:
        """Validate exact record ownership and correlated wire identities."""
        self._check_args_record_types()
        self._check_args_wire_identities()

    def _check_args_record_types(self) -> None:
        """Require exact composite-definition and campaign-result records.

        Raises
        ------
        TypeError
            If either value is a substitute semantic type.
        """
        if type(self.composite_definition) is not Periodic1DCompositeCampaignDefinition:
            raise TypeError("composite_definition uses the wrong record type")
        if type(self.campaign_result) is not Periodic1DWannier90CampaignResult:
            raise TypeError("campaign_result uses the wrong result type")

    def _check_args_wire_identities(self) -> None:
        """Require canonical digests and exact result-source correlation.

        Raises
        ------
        ValueError
            If either SHA-256 is malformed or the result digest disagrees with its
            retained source document.
        """
        decoder = Periodic1DCampaignJsonDecoder()
        decoder.sha256(self.composite_input_sha256, "composite_input_sha256")
        decoder.sha256(self.result_sha256, "result_sha256")
        if self.result_sha256 != self.campaign_result.source_document.source_sha256:
            raise ValueError("result SHA-256 must match the retained source identity")


class Periodic1DWannier90CampaignWorkflow:
    """Authenticate and correlate retained Wannier90 observations with controls.

    Result-first authentication is deliberate. The result declares the expected
    composite-input digest, so the Workflow hashes the input while it remains opaque
    and rejects disagreement before parsing or using input-owned bands, meshes, or
    model controls. SHA-256 establishes exact content identity only; it does not prove
    authorship, historical execution, or scientific correctness.
    """

    __slots__ = ()

    def execute(
        self, request: Periodic1DWannier90CampaignWorkflowRequest
    ) -> Periodic1DWannier90CampaignWorkflowResult:
        """Authenticate both wires and correlate their ordered retained groups.

        Parameters
        ----------
        request
            Exact composite/result bytes and the explicit result-wire identity.

        Returns
        -------
        Periodic1DWannier90CampaignWorkflowResult
            Strictly decoded records and exact SHA-256 content identities.

        Raises
        ------
        TypeError
            If ``request`` has the wrong exact semantic type or decoded values have
            wrong primitive representations.
        ValueError
            If strict decoding, result schema adaptation, input authentication, or
            ordered retained-group correlation fails.
        UnicodeDecodeError
            If either retained payload is not valid UTF-8 after crossing its applicable
            authentication boundary.
        OverflowError
            If a decoded finite diagnostic cannot be represented through required
            binary64 phase conversion.
        MemoryError
            If strict decoding or dense retained-matrix adaptation cannot allocate its
            required storage.
        RecursionError
            If a retained JSON document exceeds parser recursion limits.
        """
        if type(request) is not Periodic1DWannier90CampaignWorkflowRequest:
            raise TypeError(
                "request must be Periodic1DWannier90CampaignWorkflowRequest"
            )
        campaign_result = Periodic1DWannier90ResultJsonSerializer(
            request.result_kind
        ).deserialize(request.result_payload)
        input_sha256 = hashlib.sha256(request.composite_input_payload).hexdigest()
        declared_input_sha256 = self._declared_composite_input_sha256(campaign_result)
        # Input-owned scientific controls remain opaque until their exact bytes have
        # been authenticated against the result's provenance declaration.
        if declared_input_sha256 != input_sha256:
            raise ValueError("Wannier90 composite input SHA-256 does not agree")
        definition = Periodic1DCompositeCampaignJsonSerializer().deserialize(
            request.composite_input_payload
        )
        self._check_ordered_group_correlation(definition, campaign_result)
        return Periodic1DWannier90CampaignWorkflowResult(
            definition,
            campaign_result,
            input_sha256,
            hashlib.sha256(request.result_payload).hexdigest(),
        )

    def _declared_composite_input_sha256(
        self, campaign_result: Periodic1DWannier90CampaignResult
    ) -> str:
        """Read the required input digest from the strictly decoded result.

        Parameters
        ----------
        campaign_result
            Typed result retaining its complete immutable decoded JSON tree.

        Returns
        -------
        str
            Lowercase SHA-256 declared for the composite input bytes.

        Raises
        ------
        TypeError
            If the provenance object or digest has the wrong representation.
        ValueError
            If the provenance object or digest is missing or malformed.
        """
        retained = Periodic1DEncodedResultJsonSerializer(
            campaign_result.source_document.kind
        )
        provenance = retained.object_field(
            campaign_result.source_document.root, "provenance"
        )
        return Periodic1DCampaignJsonDecoder().sha256(
            retained.string_field(provenance, "composite_input_sha256"),
            "provenance.composite_input_sha256",
        )

    def _check_ordered_group_correlation(
        self,
        definition: Periodic1DCompositeCampaignDefinition,
        campaign_result: Periodic1DWannier90CampaignResult,
    ) -> None:
        """Require exact group identifiers and ordered selected-band inventories.

        Parameters
        ----------
        definition
            Authenticated composite campaign definition.
        campaign_result
            Typed retained Wannier90 observations.

        Raises
        ------
        ValueError
            If result groups differ from the definition in identity, order, or selected
            zero-based band indices.
        """
        expected_groups = tuple(
            (
                group.identifier,
                tuple(range(group.lower_index, group.upper_index + 1)),
            )
            for group in definition.retained_band_groups
        )
        observed_groups = tuple(
            (group.group_id, group.band_indices) for group in campaign_result.groups
        )
        if observed_groups != expected_groups:
            raise ValueError("Wannier90 retained band groups do not agree")
