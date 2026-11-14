"""Typed periodic-2D rank-N aggregate verification orchestration.

Verification composes the independently reconstructed parent/alignment/transport and
direct-sum Fourier/shell/support routes. Passing this software verification does not
establish convergence, material realism, scientific validation, or retained evidence.
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar, Self, final

from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.base import (
    Periodic2DRankNBandEquivalenceHoppingLocalityAction,
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseAction,
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseRequest,
)
from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue
from ksdft2effmass.verification import CompositeVerification

from .fourier_reference import (
    Periodic2DRankNBandEquivalenceHoppingLocalityFourierReferenceAnalyzer,
    Periodic2DRankNBandEquivalenceHoppingLocalityFourierReferenceRequest,
)
from .reference import (
    Periodic2DRankNBandEquivalenceHoppingLocalityReferenceAnalyzer,
    Periodic2DRankNBandEquivalenceHoppingLocalityReferenceRequest,
)
from .request import Periodic2DRankNBandEquivalenceHoppingLocalityRequest
from .result import (
    Periodic2DRankNBandEquivalenceHoppingLocalityAnalysis,
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalysis,
)


def _sha256(value: str, name: str) -> str:
    if type(value) is not str:
        raise TypeError(f"{name} must be a built-in string")
    if len(value) != 64 or value.lower() != value:
        raise ValueError(f"{name} must be one lowercase SHA-256 hexadecimal digest")
    try:
        bytes.fromhex(value)
    except ValueError as error:
        raise ValueError(
            f"{name} must be one lowercase SHA-256 hexadecimal digest"
        ) from error
    return value


@dataclass(frozen=True, slots=True)
class Periodic2DRankNBandEquivalenceHoppingLocalityCaseVerificationRequest(
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseRequest
):
    """Bind one aggregate case to its exact typed study request."""

    study_request: Periodic2DRankNBandEquivalenceHoppingLocalityRequest
    case_analysis: Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalysis

    @property
    def band_subspace_rank(self) -> int:
        """Return the bound case's represented band-subspace rank."""
        return self.case_analysis.retained_rank

    def __post_init__(self) -> None:
        if (
            type(self.study_request)
            is not Periodic2DRankNBandEquivalenceHoppingLocalityRequest
        ):
            raise TypeError("study_request must be the exact periodic-2D request")
        if (
            type(self.case_analysis)
            is not Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalysis
        ):
            raise TypeError("case_analysis must be the exact periodic-2D case analysis")
        case = self.case_analysis
        if (
            case.case_identifier
            not in tuple(item.identifier for item in self.study_request.cases)
            or case.retained_rank not in self.study_request.retained_ranks
            or case.circuit_depth not in self.study_request.circuit_depths
            or case.parent_scale not in self.study_request.parent_scales
            or case.transformation_coefficient
            not in self.study_request.transformation_coefficients
        ):
            raise ValueError("case_analysis must identify one exact request expansion")


@dataclass(frozen=True, slots=True)
class Periodic2DRankNBandEquivalenceHoppingLocalityCaseVerification(BaseTypedRecord):
    """Retain both independent verification routes for one aggregate case."""

    WIRE_IDENTITY: ClassVar[str] = (
        "ksdft2effmass.periodic2d-rankN-band-equivalence-hopping-locality-case-verification.v1"
    )

    model_identity: str
    parent_alignment_transport: CompositeVerification
    fourier_shell_support: CompositeVerification

    def __post_init__(self) -> None:
        if type(self.model_identity) is not str or not self.model_identity:
            raise TypeError("model_identity must be a nonempty built-in string")
        if type(self.parent_alignment_transport) is not CompositeVerification:
            raise TypeError("parent_alignment_transport must be CompositeVerification")
        if type(self.fourier_shell_support) is not CompositeVerification:
            raise TypeError("fourier_shell_support must be CompositeVerification")

    @property
    def passed(self) -> bool:
        """Return whether both independent case routes passed."""
        return (
            self.parent_alignment_transport.passed and self.fourier_shell_support.passed
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "wire_identity": self.WIRE_IDENTITY,
            "model_identity": self.model_identity,
            "parent_alignment_transport": self.parent_alignment_transport.to_dict(),
            "fourier_shell_support": self.fourier_shell_support.to_dict(),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "wire_identity",
            "model_identity",
            "parent_alignment_transport",
            "fourier_shell_support",
        }
        if set(values) != required:
            raise ValueError("periodic-2D case-verification fields do not match")
        if values["wire_identity"] != cls.WIRE_IDENTITY:
            raise ValueError("case-verification wire identity does not match")
        model_identity = values["model_identity"]
        parent = values["parent_alignment_transport"]
        fourier = values["fourier_shell_support"]
        if type(model_identity) is not str:
            raise TypeError("model_identity must decode to a built-in string")
        if not isinstance(parent, Mapping) or not isinstance(fourier, Mapping):
            raise TypeError("case-verification routes must decode to mappings")
        return cls(
            model_identity=model_identity,
            parent_alignment_transport=CompositeVerification.from_dict(parent),
            fourier_shell_support=CompositeVerification.from_dict(fourier),
        )


@dataclass(frozen=True, slots=True)
class Periodic2DRankNBandEquivalenceHoppingLocalityVerification(
    BaseTypedRecord,
):
    """Retain authenticated aggregate software-verification observations."""

    WIRE_IDENTITY: ClassVar[str] = (
        "ksdft2effmass.periodic2d-rankN-band-equivalence-hopping-locality-verification.v1"
    )

    request_sha256: str
    analysis_sha256: str
    cases: tuple[Periodic2DRankNBandEquivalenceHoppingLocalityCaseVerification, ...]

    def __post_init__(self) -> None:
        _sha256(self.request_sha256, "request_sha256")
        _sha256(self.analysis_sha256, "analysis_sha256")
        if (
            type(self.cases) is not tuple
            or not self.cases
            or any(
                type(case)
                is not Periodic2DRankNBandEquivalenceHoppingLocalityCaseVerification
                for case in self.cases
            )
        ):
            raise TypeError("cases must contain exact periodic-2D case verifications")
        identities = tuple(case.model_identity for case in self.cases)
        if len(set(identities)) != len(identities):
            raise ValueError("case-verification model identities must be unique")

    @property
    def passed(self) -> bool:
        """Return whether every case passed every independent route."""
        return all(case.passed for case in self.cases)

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "wire_identity": self.WIRE_IDENTITY,
            "request_sha256": self.request_sha256,
            "analysis_sha256": self.analysis_sha256,
            "cases": tuple(case.to_dict() for case in self.cases),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "wire_identity",
            "request_sha256",
            "analysis_sha256",
            "cases",
        }
        if set(values) != required:
            raise ValueError("periodic-2D aggregate-verification fields do not match")
        if values["wire_identity"] != cls.WIRE_IDENTITY:
            raise ValueError("aggregate-verification wire identity does not match")
        request_sha256 = values["request_sha256"]
        analysis_sha256 = values["analysis_sha256"]
        cases = values["cases"]
        if type(request_sha256) is not str or type(analysis_sha256) is not str:
            raise TypeError("verification identity fields must decode to strings")
        if type(cases) is not tuple or any(
            not isinstance(case, Mapping) for case in cases
        ):
            raise TypeError("verification cases must decode to mappings")
        return cls(
            request_sha256=request_sha256,
            analysis_sha256=analysis_sha256,
            cases=tuple(
                Periodic2DRankNBandEquivalenceHoppingLocalityCaseVerification.from_dict(
                    case
                )
                for case in cases
            ),
        )


@final
class Periodic2DRankNBandEquivalenceHoppingLocalityCaseVerifier(
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseAction
):
    """Execute both independent routes for one constructor-bound case."""

    __slots__ = ("_request",)

    def __init__(
        self,
        *,
        request: Periodic2DRankNBandEquivalenceHoppingLocalityCaseVerificationRequest,
    ) -> None:
        if (
            type(request)
            is not Periodic2DRankNBandEquivalenceHoppingLocalityCaseVerificationRequest
        ):
            raise TypeError("request must be the exact periodic-2D case verification")
        self._request = request

    @property
    def request(
        self,
    ) -> Periodic2DRankNBandEquivalenceHoppingLocalityCaseVerificationRequest:
        """Return the immutable case-verification request."""
        return self._request

    @property
    def band_subspace_rank(self) -> int:
        """Return the verified case's represented band-subspace rank."""
        return self.request.band_subspace_rank

    def execute(self) -> Periodic2DRankNBandEquivalenceHoppingLocalityCaseVerification:
        """Return typed observations from both independent reference routes."""
        request = self._request
        parent_reference = (
            Periodic2DRankNBandEquivalenceHoppingLocalityReferenceAnalyzer(
                request=Periodic2DRankNBandEquivalenceHoppingLocalityReferenceRequest(
                    study_request=request.study_request,
                    case_analysis=request.case_analysis,
                )
            ).execute()
        )
        fourier_reference = Periodic2DRankNBandEquivalenceHoppingLocalityFourierReferenceAnalyzer(  # noqa: E501
            request=Periodic2DRankNBandEquivalenceHoppingLocalityFourierReferenceRequest(
                study_request=request.study_request,
                case_analysis=request.case_analysis,
            )
        ).execute()
        return Periodic2DRankNBandEquivalenceHoppingLocalityCaseVerification(
            model_identity=request.case_analysis.model_identity,
            parent_alignment_transport=CompositeVerification.evaluate(
                parent_reference.comparisons
            ),
            fourier_shell_support=CompositeVerification.evaluate(
                fourier_reference.comparisons
            ),
        )


@final
class Periodic2DRankNBandEquivalenceHoppingLocalityVerifier(
    Periodic2DRankNBandEquivalenceHoppingLocalityAction
):
    """Sequence per-case verification for one complete immutable analysis."""

    __slots__ = ("_analysis",)

    def __init__(
        self,
        *,
        analysis: Periodic2DRankNBandEquivalenceHoppingLocalityAnalysis,
    ) -> None:
        if type(analysis) is not Periodic2DRankNBandEquivalenceHoppingLocalityAnalysis:
            raise TypeError("analysis must be the exact periodic-2D rank-N analysis")
        self._analysis = analysis

    @property
    def analysis(self) -> Periodic2DRankNBandEquivalenceHoppingLocalityAnalysis:
        """Return the immutable aggregate analysis bound to this verifier."""
        return self._analysis

    @property
    def band_subspace_ranks(self) -> tuple[int, ...]:
        """Return the verified band-subspace rank inventory."""
        return self.analysis.band_subspace_ranks

    def execute(self) -> Periodic2DRankNBandEquivalenceHoppingLocalityVerification:
        """Verify every aggregate case without retained side effects."""
        analysis = self._analysis
        cases = tuple(
            Periodic2DRankNBandEquivalenceHoppingLocalityCaseVerifier(
                request=Periodic2DRankNBandEquivalenceHoppingLocalityCaseVerificationRequest(
                    study_request=analysis.request,
                    case_analysis=case,
                )
            ).execute()
            for case in analysis.cases
        )
        request_sha256 = hashlib.sha256(analysis.request.to_json()).hexdigest()
        analysis_sha256 = hashlib.sha256(analysis.to_json()).hexdigest()
        return Periodic2DRankNBandEquivalenceHoppingLocalityVerification(
            request_sha256=request_sha256,
            analysis_sha256=analysis_sha256,
            cases=cases,
        )


__all__ = [
    "Periodic2DRankNBandEquivalenceHoppingLocalityCaseVerification",
    "Periodic2DRankNBandEquivalenceHoppingLocalityCaseVerificationRequest",
    "Periodic2DRankNBandEquivalenceHoppingLocalityCaseVerifier",
    "Periodic2DRankNBandEquivalenceHoppingLocalityVerification",
    "Periodic2DRankNBandEquivalenceHoppingLocalityVerifier",
]
