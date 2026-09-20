"""Execution-free correlation of retained Appendix G results with native artifacts."""

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

from .result_documents import Periodic1DRetainedResultKind
from .wannier90_results import (
    Periodic1DWannier90CampaignResult,
    Periodic1DWannier90ResultJsonSerializer,
    Periodic1DWannier90WilsonGroupResult,
)


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90NativeArtifactGroup:
    """Provide one retained group identity and its caller-supplied native bytes."""

    group_id: str
    artifacts: tuple[Wannier90NativeArtifact, ...]

    def __post_init__(self) -> None:
        """Require a stable group identity and a unique nonempty artifact inventory."""
        if type(self.group_id) is not str or not self.group_id:
            raise ValueError("group_id must be a nonempty built-in str")
        if (
            not isinstance(self.artifacts, tuple)
            or not self.artifacts
            or any(type(item) is not Wannier90NativeArtifact for item in self.artifacts)
        ):
            raise TypeError("artifacts must be a nonempty typed tuple")
        names = tuple(artifact.name for artifact in self.artifacts)
        if len(set(names)) != len(names):
            raise ValueError("native artifact names must be unique")


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90NativeArtifactWorkflowRequest:
    """Provide retained result bytes and complete native artifact groups."""

    result_payload: bytes
    result_kind: Periodic1DRetainedResultKind
    artifact_groups: tuple[Periodic1DWannier90NativeArtifactGroup, ...]

    def __post_init__(self) -> None:
        """Require supported result bytes and a unique nonempty group inventory."""
        if type(self.result_payload) is not bytes or not self.result_payload:
            raise ValueError("result_payload must be nonempty built-in bytes")
        if type(self.result_kind) is not Periodic1DRetainedResultKind:
            raise TypeError("result_kind must be Periodic1DRetainedResultKind")
        if self.result_kind not in {
            Periodic1DRetainedResultKind.WANNIER90,
            Periodic1DRetainedResultKind.WANNIER90_PRECONDITIONED,
        }:
            raise ValueError("result_kind must identify a supported Wannier90 result")
        if (
            not isinstance(self.artifact_groups, tuple)
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
    """Retain authenticated identities and parsed scientific files for one group."""

    group_id: str
    correlation: Wannier90NativeArtifactCorrelationResult
    parsed_artifacts: Wannier90ParsedNativeArtifactSet

    def __post_init__(self) -> None:
        """Validate group identity and exact operational ResultObject types."""
        if type(self.group_id) is not str or not self.group_id:
            raise ValueError("group_id must be a nonempty built-in str")
        if type(self.correlation) is not Wannier90NativeArtifactCorrelationResult:
            raise TypeError("correlation uses the wrong ResultObject")
        if type(self.parsed_artifacts) is not Wannier90ParsedNativeArtifactSet:
            raise TypeError("parsed_artifacts uses the wrong ResultObject")


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90NativeArtifactWorkflowResult:
    """Retain a typed result document and every correlated native group."""

    campaign_result: Periodic1DWannier90CampaignResult
    groups: tuple[Periodic1DWannier90NativeArtifactGroupResult, ...]

    def __post_init__(self) -> None:
        """Require exact result types and matching ordered group identifiers."""
        if type(self.campaign_result) is not Periodic1DWannier90CampaignResult:
            raise TypeError("campaign_result must be Periodic1DWannier90CampaignResult")
        if (
            not isinstance(self.groups, tuple)
            or not self.groups
            or any(
                type(group) is not Periodic1DWannier90NativeArtifactGroupResult
                for group in self.groups
            )
        ):
            raise TypeError("groups must be a nonempty typed tuple")
        expected = tuple(group.group_id for group in self.campaign_result.groups)
        observed = tuple(group.group_id for group in self.groups)
        if observed != expected:
            raise ValueError("native result groups must match campaign result order")


class Periodic1DWannier90NativeArtifactWorkflow:
    """Authenticate and parse explicit native bytes without discovery or execution."""

    __slots__ = ()

    correlator = Wannier90NativeArtifactCorrelator()
    parser = Wannier90NativeArtifactSetParser()

    def execute(
        self, request: Periodic1DWannier90NativeArtifactWorkflowRequest
    ) -> Periodic1DWannier90NativeArtifactWorkflowResult:
        """Correlate the exact inventory and parse supported scientific text files."""
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
        return Periodic1DWannier90NativeArtifactWorkflowResult(
            campaign_result,
            tuple(
                self.execute_group(group, supplied[group.group_id])
                for group in campaign_result.groups
            ),
        )

    def execute_group(
        self,
        expected: Periodic1DWannier90WilsonGroupResult,
        supplied: Periodic1DWannier90NativeArtifactGroup,
    ) -> Periodic1DWannier90NativeArtifactGroupResult:
        """Authenticate, parse, and correlate one retained group."""
        correlation = self.correlator.execute(
            expected.artifact_identities, supplied.artifacts
        )
        parsed = self.parser.execute(
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
