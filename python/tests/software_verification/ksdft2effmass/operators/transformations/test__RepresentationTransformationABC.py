"""Software verification for :class:`RepresentationTransformationABC`."""

from __future__ import annotations

from typing import cast, final

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
class _SyntheticRequest(RepresentationTransformationRequestABC):
    """Provide one nominal request for skeleton verification."""

    __slots__ = ("_transformation_kind",)

    def __init__(self, transformation_kind: RepresentationTransformationKind) -> None:
        self._transformation_kind = transformation_kind

    @property
    def transformation_kind(self) -> RepresentationTransformationKind:
        """Return the configured enum member."""
        return self._transformation_kind


@final
class _SyntheticResult(RepresentationTransformationResultABC):
    """Provide one nominal result for skeleton verification."""

    __slots__ = ("_transformation_kind",)

    def __init__(self, transformation_kind: RepresentationTransformationKind) -> None:
        self._transformation_kind = transformation_kind

    @property
    def transformation_kind(self) -> RepresentationTransformationKind:
        """Return the configured enum member."""
        return self._transformation_kind


@final
class _SyntheticGaugeConjugation(
    RepresentationTransformationABC[_SyntheticRequest, _SyntheticResult]
):
    """Return one configured result through the nominal skeleton."""

    __slots__ = ("_result_kind",)

    def __init__(self, result_kind: RepresentationTransformationKind) -> None:
        self._result_kind = result_kind

    @property
    def transformation_kind(self) -> RepresentationTransformationKind:
        """Return the operation family implemented by this synthetic Action."""
        return RepresentationTransformationKind.gauge_conjugation

    def transform(self, request: _SyntheticRequest, /) -> _SyntheticResult:
        """Validate kinds and return the configured synthetic result."""
        self._require_compatible_request_kind(request)
        result = _SyntheticResult(self._result_kind)
        return self._require_compatible_result_kind(result)


@final
class _MalformedKindAction(
    RepresentationTransformationABC[_SyntheticRequest, _SyntheticResult]
):
    """Expose a raw string through a deliberately malformed Action property."""

    __slots__ = ()

    @property
    def transformation_kind(self) -> RepresentationTransformationKind:
        """Return an invalid raw string for runtime rejection testing."""
        return cast(RepresentationTransformationKind, "gauge_conjugation")

    def transform(self, request: _SyntheticRequest, /) -> _SyntheticResult:
        """Reject the malformed Action kind before returning a result."""
        self._require_compatible_request_kind(request)
        result = _SyntheticResult(RepresentationTransformationKind.gauge_conjugation)
        return self._require_compatible_result_kind(result)


@final
class _NonNominalResultAction(
    RepresentationTransformationABC[_SyntheticRequest, _SyntheticResult]
):
    """Return a non-nominal value for fail-closed result testing."""

    __slots__ = ()

    @property
    def transformation_kind(self) -> RepresentationTransformationKind:
        """Return the gauge-conjugation enum member."""
        return RepresentationTransformationKind.gauge_conjugation

    def transform(self, request: _SyntheticRequest, /) -> _SyntheticResult:
        """Validate the request and reject a structural result substitute."""
        self._require_compatible_request_kind(request)
        result = cast(_SyntheticResult, "gauge_conjugation")
        return self._require_compatible_result_kind(result)


class TestRepresentationTransformationABC:
    """Establish nominal and enum-stable request-to-result behavior."""

    def test_transform__is_the_abstract_public_override_point(self) -> None:
        """The nominal Action contract requires concrete public transformation."""
        assert "transform" in RepresentationTransformationABC.__abstractmethods__

    def test_transform__returns_same_kind_nominal_result(self) -> None:
        """A same-kind request, Action, and result pass through the skeleton."""
        action = _SyntheticGaugeConjugation(
            RepresentationTransformationKind.gauge_conjugation
        )
        request = _SyntheticRequest(RepresentationTransformationKind.gauge_conjugation)

        result = action.transform(request)

        assert isinstance(result, RepresentationTransformationResultABC)
        assert (
            result.transformation_kind
            is RepresentationTransformationKind.gauge_conjugation
        )

    def test_transform__rejects_request_kind_mismatch(self) -> None:
        """An Action never accepts another transformation family's request."""
        action = _SyntheticGaugeConjugation(
            RepresentationTransformationKind.gauge_conjugation
        )
        request = _SyntheticRequest(RepresentationTransformationKind.alignment)

        with pytest.raises(ValueError, match="request transformation kind"):
            action.transform(request)

    def test_transform__rejects_result_kind_mismatch(self) -> None:
        """An Action never returns another transformation family's result."""
        action = _SyntheticGaugeConjugation(RepresentationTransformationKind.alignment)
        request = _SyntheticRequest(RepresentationTransformationKind.gauge_conjugation)

        with pytest.raises(ValueError, match="result transformation kind"):
            action.transform(request)

    def test_transform__rejects_non_nominal_request(self) -> None:
        """Structural similarity does not replace nominal request membership."""
        action = _SyntheticGaugeConjugation(
            RepresentationTransformationKind.gauge_conjugation
        )

        with pytest.raises(TypeError, match="request must implement"):
            action.transform(cast(_SyntheticRequest, "gauge_conjugation"))

    def test_transform__rejects_non_nominal_result(self) -> None:
        """Structural similarity does not replace nominal result membership."""
        request = _SyntheticRequest(RepresentationTransformationKind.gauge_conjugation)

        with pytest.raises(TypeError, match="result must implement"):
            _NonNominalResultAction().transform(request)

    def test_transform__rejects_raw_string_action_kind(self) -> None:
        """An Action enum property cannot use an unbound textual discriminator."""
        request = _SyntheticRequest(RepresentationTransformationKind.gauge_conjugation)

        with pytest.raises(TypeError, match="Action transformation_kind"):
            _MalformedKindAction().transform(request)

    def test_transform__rejects_raw_string_request_kind(self) -> None:
        """A nominal request still must expose the exact enum type."""
        action = _SyntheticGaugeConjugation(
            RepresentationTransformationKind.gauge_conjugation
        )
        request = _SyntheticRequest(
            cast(RepresentationTransformationKind, "gauge_conjugation")
        )

        with pytest.raises(TypeError, match="request transformation_kind"):
            action.transform(request)

    def test_transform__rejects_raw_string_result_kind(self) -> None:
        """A nominal result still must expose the exact enum type."""
        action = _SyntheticGaugeConjugation(
            cast(RepresentationTransformationKind, "gauge_conjugation")
        )
        request = _SyntheticRequest(RepresentationTransformationKind.gauge_conjugation)

        with pytest.raises(TypeError, match="result transformation_kind"):
            action.transform(request)
