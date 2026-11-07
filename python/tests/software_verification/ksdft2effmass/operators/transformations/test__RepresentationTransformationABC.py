"""Software verification for :class:`RepresentationTransformationABC`."""

from __future__ import annotations

from dataclasses import dataclass
from typing import assert_type, final

import pytest

from ksdft2effmass.operators.transformations.base import (
    RepresentationTransformationABC,
    RepresentationTransformationRequestABC,
    RepresentationTransformationResultABC,
)
from ksdft2effmass.operators.transformations.identities import (
    RepresentationTransformationKind,
)

pytestmark = pytest.mark.software_verification


@final
@dataclass(frozen=True, slots=True)
class _SyntheticGaugeConjugationRequest(RepresentationTransformationRequestABC):
    """Provide the exact request type for one synthetic transformation."""

    @property
    def transformation_kind(self) -> RepresentationTransformationKind:
        """Return the class-owned transformation kind."""
        return RepresentationTransformationKind.gauge_conjugation


@final
@dataclass(frozen=True, slots=True)
class _ForeignGaugeConjugationRequest(RepresentationTransformationRequestABC):
    """Provide a foreign exact request carrying the same enum member."""

    @property
    def transformation_kind(self) -> RepresentationTransformationKind:
        """Return the same kind as the intended synthetic request."""
        return RepresentationTransformationKind.gauge_conjugation


@final
@dataclass(frozen=True, slots=True)
class _SyntheticAlignmentRequest(RepresentationTransformationRequestABC):
    """Provide a nominal request carrying another enum member."""

    @property
    def transformation_kind(self) -> RepresentationTransformationKind:
        """Return the alignment transformation kind."""
        return RepresentationTransformationKind.alignment


@final
@dataclass(frozen=True, slots=True)
class _SyntheticGaugeConjugationResult(RepresentationTransformationResultABC):
    """Provide the exact result type for one synthetic transformation."""

    @property
    def transformation_kind(self) -> RepresentationTransformationKind:
        """Return the class-owned transformation kind."""
        return RepresentationTransformationKind.gauge_conjugation


@final
@dataclass(frozen=True, slots=True)
class _ForeignGaugeConjugationResult(RepresentationTransformationResultABC):
    """Provide a foreign exact result carrying the same enum member."""

    @property
    def transformation_kind(self) -> RepresentationTransformationKind:
        """Return the same kind as the intended synthetic result."""
        return RepresentationTransformationKind.gauge_conjugation


@final
@dataclass(frozen=True, slots=True)
class _SyntheticAlignmentResult(RepresentationTransformationResultABC):
    """Provide a nominal result carrying another enum member."""

    @property
    def transformation_kind(self) -> RepresentationTransformationKind:
        """Return the alignment transformation kind."""
        return RepresentationTransformationKind.alignment


@final
@dataclass(frozen=True, slots=True)
class _SyntheticGaugeConjugation(RepresentationTransformationABC):
    """Bind one exact request and directly construct one exact result."""

    _request: _SyntheticGaugeConjugationRequest

    def __post_init__(self) -> None:
        """Validate the exact request type and class-owned enum agreement."""
        self._require_exact_request(self._request)
        self._require_compatible_request_kind(self._request)

    @property
    def transformation_kind(self) -> RepresentationTransformationKind:
        """Return the class-owned transformation kind."""
        return RepresentationTransformationKind.gauge_conjugation

    @staticmethod
    def _require_exact_request(
        request: RepresentationTransformationRequestABC,
        /,
    ) -> None:
        """Reject a request outside this concrete transformation triple."""
        if type(request) is not _SyntheticGaugeConjugationRequest:
            raise TypeError(
                "request must be an exact _SyntheticGaugeConjugationRequest"
            )

    @staticmethod
    def _require_exact_result(
        result: RepresentationTransformationResultABC,
        /,
    ) -> None:
        """Reject a result outside this concrete transformation triple."""
        if type(result) is not _SyntheticGaugeConjugationResult:
            raise TypeError("result must be an exact _SyntheticGaugeConjugationResult")

    def transform(self) -> _SyntheticGaugeConjugationResult:
        """Directly construct, validate, and return the exact concrete result."""
        result: _SyntheticGaugeConjugationResult = _SyntheticGaugeConjugationResult()
        self._require_exact_result(result)
        self._require_compatible_result_kind(result)
        return result


class TestRepresentationTransformationABC:
    """Establish the non-generic nominal transformation contract."""

    def test_transform__is_the_abstract_public_override_point(self) -> None:
        """The nominal Action root requires a concrete public transformation."""
        assert "transform" in RepresentationTransformationABC.__abstractmethods__

    def test_concrete_triple__has_one_exact_kind_and_result_type(self) -> None:
        """One concrete request, transformation, and result share one enum member."""
        request = _SyntheticGaugeConjugationRequest()
        transformation = _SyntheticGaugeConjugation(request)

        result = transformation.transform()

        assert_type(result, _SyntheticGaugeConjugationResult)
        assert type(transformation._request) is _SyntheticGaugeConjugationRequest
        assert type(result) is _SyntheticGaugeConjugationResult
        assert (
            request.transformation_kind
            is transformation.transformation_kind
            is result.transformation_kind
            is RepresentationTransformationKind.gauge_conjugation
        )

    def test_exact_request_validator__rejects_foreign_same_kind_request(self) -> None:
        """Enum agreement does not admit another concrete request type."""
        foreign = _ForeignGaugeConjugationRequest()

        with pytest.raises(TypeError, match="exact _SyntheticGaugeConjugationRequest"):
            _SyntheticGaugeConjugation._require_exact_request(foreign)

    def test_exact_result_validator__rejects_foreign_same_kind_result(self) -> None:
        """Enum agreement does not admit another concrete result type."""
        foreign = _ForeignGaugeConjugationResult()

        with pytest.raises(TypeError, match="exact _SyntheticGaugeConjugationResult"):
            _SyntheticGaugeConjugation._require_exact_result(foreign)

    def test_request_kind_validator__rejects_other_kind(self) -> None:
        """The shared helper rejects another nominal request kind."""
        transformation = _SyntheticGaugeConjugation(_SyntheticGaugeConjugationRequest())

        with pytest.raises(ValueError, match="request transformation kind"):
            transformation._require_compatible_request_kind(
                _SyntheticAlignmentRequest()
            )

    def test_result_kind_validator__rejects_other_kind(self) -> None:
        """The shared helper rejects another nominal result kind."""
        transformation = _SyntheticGaugeConjugation(_SyntheticGaugeConjugationRequest())

        with pytest.raises(ValueError, match="result transformation kind"):
            transformation._require_compatible_result_kind(_SyntheticAlignmentResult())
