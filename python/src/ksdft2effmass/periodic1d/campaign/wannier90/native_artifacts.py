"""Execution-free authentication and parsing of explicit native artifact bytes.

Campaign-owned group inventories are correlated with artifact identities retained by a
strictly decoded result. Generic Wannier90 correlation and parsing Actions are composed
in two passes: every group's explicit names, byte counts, and SHA-256 identities must
agree before any scientific payload is parsed. No filesystem
root is accepted or discovered and no executable is invoked.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.integration.wannier90 import (
    Wannier90NativeArtifact,
    Wannier90NativeArtifactCorrelationResult,
    Wannier90NativeArtifactCorrelator,
    Wannier90NativeArtifactSetParser,
    Wannier90ParsedNativeArtifactSet,
)
from ksdft2effmass.operators import PhysicalUnit
from ksdft2effmass.periodic1d.campaign.result_documents import (
    Periodic1DEncodedResultKind,
)

from .results import (
    Periodic1DWannier90CampaignResult,
    Periodic1DWannier90ResultJsonSerializer,
    Periodic1DWannier90WilsonGroupResult,
)


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90NativeArtifactGroup:
    """Store one native band-group identity and explicit artifact bytes.

    Parameters
    ----------
    group_id
        Nonempty exact built-in :class:`str` identifying one retained Wannier90 band
        group. The value is an explicit correlation key, not an inferred band-space or
        gauge identity.
    artifacts
        Nonempty immutable tuple of exact :class:`Wannier90NativeArtifact` records in
        caller-supplied order. Logical artifact names must be unique within the group.

    Raises
    ------
    ValueError
        If ``group_id`` is not a nonempty exact built-in string or if artifact names
        are duplicated.
    TypeError
        If ``artifacts`` is not a nonempty tuple of exact
        :class:`Wannier90NativeArtifact` values.

    Notes
    -----
    This DataObject owns explicit native file bytes separately from
    ``Periodic1DWannier90EncodedDocuments``. It does not own a filesystem root,
    perform path discovery, infer missing files, execute Wannier90, parse scientific
    content, or establish that the group matches an encoded result. Dedicated Actions
    authenticate, parse, and correlate the supplied inventory against explicit retained
    identities. The record preserves caller order; correlation later binds by unique
    logical name and emits the explicit expected result order. A file payload may be
    empty where the lower-level native-artifact contract permits it.

    A group name and artifact digest identify supplied content only. They do not by
    themselves establish source provenance, convergence, physical validity, uncertainty
    quantification, or acceptance.
    """

    group_id: str
    artifacts: tuple[Wannier90NativeArtifact, ...]

    def __post_init__(self) -> None:
        """Validate explicit group identity and immutable artifact inventory.

        Raises
        ------
        ValueError
            If the group identity is invalid or artifact names are duplicated.
        TypeError
            If the artifact inventory has the wrong representation or member types.
        """
        self._check_args_group_identity()
        self._check_args_artifact_inventory()

    def _check_args_group_identity(self) -> None:
        """Require a nonempty exact built-in group-correlation key.

        Raises
        ------
        ValueError
            If ``group_id`` is not a nonempty exact built-in :class:`str`.
        """
        if type(self.group_id) is not str or not self.group_id:
            raise ValueError("group_id must be a nonempty built-in str")

    def _check_args_artifact_inventory(self) -> None:
        """Require a nonempty typed inventory with unique logical names.

        Raises
        ------
        TypeError
            If ``artifacts`` is not a nonempty tuple of exact
            :class:`Wannier90NativeArtifact` values.
        ValueError
            If more than one artifact has the same logical name.
        """
        if (
            type(self.artifacts) is not tuple
            or not self.artifacts
            or any(type(item) is not Wannier90NativeArtifact for item in self.artifacts)
        ):
            raise TypeError("artifacts must be a nonempty typed tuple")
        names = tuple(artifact.name for artifact in self.artifacts)
        # Names are correlation keys. A duplicate would make expected-to-observed
        # binding ambiguous even when the two payloads happen to be byte-identical.
        if len(set(names)) != len(names):
            raise ValueError("native artifact names must be unique")


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90NativeArtifactWorkflowRequest:
    """Provide retained result bytes and complete native artifact groups.

    Parameters
    ----------
    result_payload
        Nonempty exact retained JSON bytes.
    result_kind
        Explicit supported result-wire discriminator.
    artifact_groups
        Nonempty exact tuple of uniquely identified native groups.

    Raises
    ------
    TypeError
        If bytes, kind, tuple, or members have wrong exact representations.
    ValueError
        If bytes are empty, the kind is unsupported, or group identities repeat.
    """

    result_payload: bytes
    result_kind: Periodic1DEncodedResultKind
    artifact_groups: tuple[Periodic1DWannier90NativeArtifactGroup, ...]

    def __post_init__(self) -> None:
        """Validate exact result-wire input and native group inventory."""
        self._check_args_result_wire()
        self._check_args_artifact_groups()

    def _check_args_result_wire(self) -> None:
        """Require nonempty exact bytes and a supported explicit wire kind."""
        if type(self.result_payload) is not bytes:
            raise TypeError("result_payload must be built-in bytes")
        if not self.result_payload:
            raise ValueError("result_payload must be nonempty")
        if type(self.result_kind) is not Periodic1DEncodedResultKind:
            raise TypeError("result_kind must be Periodic1DEncodedResultKind")
        if self.result_kind not in {
            Periodic1DEncodedResultKind.WANNIER90,
            Periodic1DEncodedResultKind.WANNIER90_PRECONDITIONED,
        }:
            raise ValueError("result_kind must identify a supported Wannier90 result")

    def _check_args_artifact_groups(self) -> None:
        """Require a nonempty exact group tuple with unique explicit identities."""
        if (
            type(self.artifact_groups) is not tuple
            or not self.artifact_groups
            or any(
                type(group) is not Periodic1DWannier90NativeArtifactGroup
                for group in self.artifact_groups
            )
        ):
            raise TypeError("artifact_groups must be a nonempty typed tuple")
        group_ids = tuple(group.group_id for group in self.artifact_groups)
        if len(set(group_ids)) != len(group_ids):
            raise ValueError("native artifact group identifiers must be unique")


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90NativeArtifactGroupResult:
    """Retain authenticated identities and parsed scientific files for one group.

    Parameters
    ----------
    group_id
        Explicit nonempty group-correlation identity.
    correlation
        Generic Result authenticating expected and observed native artifact identities.
    parsed_artifacts
        Generic Result containing the supported parsed native records.

    Raises
    ------
    TypeError
        If either nested Result has the wrong exact semantic type.
    ValueError
        If ``group_id`` is not a nonempty exact built-in string.
    """

    group_id: str
    correlation: Wannier90NativeArtifactCorrelationResult
    parsed_artifacts: Wannier90ParsedNativeArtifactSet

    def __post_init__(self) -> None:
        """Validate group identity and exact operational AbstractResultObject types."""
        if type(self.group_id) is not str or not self.group_id:
            raise ValueError("group_id must be a nonempty built-in str")
        if type(self.correlation) is not Wannier90NativeArtifactCorrelationResult:
            raise TypeError("correlation uses the wrong AbstractResultObject")
        if type(self.parsed_artifacts) is not Wannier90ParsedNativeArtifactSet:
            raise TypeError("parsed_artifacts uses the wrong AbstractResultObject")


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90NativeArtifactWorkflowResult:
    """Retain a typed result document and every correlated native group.

    Parameters
    ----------
    campaign_result
        Typed retained Wannier90 result and complete immutable source document.
    groups
        Nonempty native group Results in exact retained campaign order.

    Raises
    ------
    TypeError
        If aggregate or group Results have wrong exact semantic types.
    ValueError
        If native group identities differ from retained campaign order.
    """

    campaign_result: Periodic1DWannier90CampaignResult
    groups: tuple[Periodic1DWannier90NativeArtifactGroupResult, ...]

    def __post_init__(self) -> None:
        """Validate exact result types and ordered group correlation."""
        self._check_args_result_types()
        self._check_args_group_correlation()

    def _check_args_result_types(self) -> None:
        """Require exact campaign and native-group Result records."""
        if type(self.campaign_result) is not Periodic1DWannier90CampaignResult:
            raise TypeError("campaign_result must be Periodic1DWannier90CampaignResult")
        if (
            type(self.groups) is not tuple
            or not self.groups
            or any(
                type(group) is not Periodic1DWannier90NativeArtifactGroupResult
                for group in self.groups
            )
        ):
            raise TypeError("groups must be a nonempty typed tuple")

    def _check_args_group_correlation(self) -> None:
        """Require native groups to match retained campaign order exactly."""
        expected = tuple(group.group_id for group in self.campaign_result.groups)
        observed = tuple(group.group_id for group in self.groups)
        if observed != expected:
            raise ValueError("native result groups must match campaign result order")


class Periodic1DWannier90NativeArtifactWorkflow:
    """Authenticate and parse explicit native bytes without discovery or execution.

    A whole-request identity-authentication pass precedes all scientific parsing.
    Generic integration owners perform digest correlation and native format adaptation;
    this campaign Workflow
    adds exact retained group rank and center correlation. Logical names and hashes are
    not promoted into physical-model, state-space, gauge, or provenance identities.
    """

    __slots__ = ()

    def execute(
        self, request: Periodic1DWannier90NativeArtifactWorkflowRequest
    ) -> Periodic1DWannier90NativeArtifactWorkflowResult:
        """Authenticate the complete inventory and parse supported native text.

        Parameters
        ----------
        request
            Exact retained result bytes, explicit result kind, and caller-supplied
            native artifact groups.

        Returns
        -------
        Periodic1DWannier90NativeArtifactWorkflowResult
            Typed retained observations plus authenticated and parsed native groups.

        Raises
        ------
        TypeError
            If request or nested records have wrong exact representations.
        ValueError
            If schema decoding, inventory correlation, digest authentication, native
            parsing, dimensional checks, or center correlation fails.
        UnicodeDecodeError
            If retained JSON is not valid UTF-8. Native scientific-text decoders report
            invalid UTF-8 as ``ValueError`` at their parser boundaries.
        OverflowError
            If a required native or retained numeric value is not representable in its
            documented binary64/complex128 representation.
        MemoryError
            If a decoded tree or dense native matrix cannot be allocated.
        RecursionError
            If retained JSON exceeds parser recursion limits.
        """
        if type(request) is not Periodic1DWannier90NativeArtifactWorkflowRequest:
            raise TypeError(
                "request must be Periodic1DWannier90NativeArtifactWorkflowRequest"
            )
        campaign_result = Periodic1DWannier90ResultJsonSerializer(
            request.result_kind
        ).deserialize(request.result_payload)
        supplied = {group.group_id: group for group in request.artifact_groups}
        expected_ids = tuple(group.group_id for group in campaign_result.groups)
        if set(supplied) != set(expected_ids):
            raise ValueError("native artifact group inventory does not agree")
        # Complete the byte-identity barrier for the whole request before any group
        # can expose scientific text to a parser or allocate dense parsed matrices.
        correlations = tuple(
            self._authenticate_group(group, supplied[group.group_id])
            for group in campaign_result.groups
        )
        return Periodic1DWannier90NativeArtifactWorkflowResult(
            campaign_result,
            tuple(
                self._parse_group(
                    group,
                    supplied[group.group_id],
                    correlation,
                )
                for group, correlation in zip(
                    campaign_result.groups, correlations, strict=True
                )
            ),
        )

    def _authenticate_group(
        self,
        expected: Periodic1DWannier90WilsonGroupResult,
        supplied: Periodic1DWannier90NativeArtifactGroup,
    ) -> Wannier90NativeArtifactCorrelationResult:
        """Authenticate one complete named byte inventory without parsing it."""
        return Wannier90NativeArtifactCorrelator().execute(
            expected.artifact_identities, supplied.artifacts
        )

    def _parse_group(
        self,
        expected: Periodic1DWannier90WilsonGroupResult,
        supplied: Periodic1DWannier90NativeArtifactGroup,
        correlation: Wannier90NativeArtifactCorrelationResult,
    ) -> Periodic1DWannier90NativeArtifactGroupResult:
        """Parse and correlate one group after the whole-request identity barrier."""
        parsed = Wannier90NativeArtifactSetParser().execute(
            expected.group_id,
            supplied.artifacts,
            PhysicalUnit("eV"),
            PhysicalUnit("angstrom"),
        )
        if parsed.localization.wannier_count != expected.direct_spectrum.rank:
            raise ValueError("native Wannier count does not match Wilson spectrum rank")
        if not np.array_equal(
            parsed.localization.centers.magnitude,
            np.asarray(expected.wannier90_centers_cell_coordinates, dtype=np.float64),
        ):
            raise ValueError("parsed native centers do not match retained centers")
        return Periodic1DWannier90NativeArtifactGroupResult(
            expected.group_id, correlation, parsed
        )
