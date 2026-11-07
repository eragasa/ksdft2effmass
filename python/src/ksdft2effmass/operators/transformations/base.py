"""Nominal computational skeleton for representation transformations.

The interfaces in this module own operational request-to-result typing. They do not
supply a universal enum-dispatched factory, numerical implementation, evidence, wire
format, or formal proof contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from .identities import RepresentationTransformationKind


class RepresentationTransformationRequestABC(ABC):
    """Identify a nominal request for one representation-transformation family.

    Notes
    -----
    Concrete requests own operation-specific payloads. The shared enum property is a
    visible computational discriminator, not a raw string or serialization token.
    """

    __slots__ = ()

    @property
    @abstractmethod
    def transformation_kind(self) -> RepresentationTransformationKind:
        """Return the exact representation-transformation enum member.

        Returns
        -------
        RepresentationTransformationKind
            Operation family requested by this nominal request.
        """


class RepresentationTransformationResultABC(ABC):
    """Identify a nominal result for one representation-transformation family.

    Notes
    -----
    Concrete results own operation-specific success, failure, target, witness, and
    evidence payloads. Enum agreement alone establishes none of those properties.
    """

    __slots__ = ()

    @property
    @abstractmethod
    def transformation_kind(self) -> RepresentationTransformationKind:
        """Return the exact representation-transformation enum member.

        Returns
        -------
        RepresentationTransformationKind
            Operation family represented by this nominal result.
        """


class RepresentationTransformationABC(ABC):
    """Nominal root for one concrete request-bound transformation.

    A final concrete transformation owns one exact request type, one exact result type,
    and one fixed :class:`RepresentationTransformationKind`. Its constructor binds and
    validates the request. Its public :meth:`transform` override narrows the nominal
    result return type to the exact concrete result type.

    This non-generic base cannot express or enforce each concrete request type. The
    protected final methods validate nominal membership and exact enum agreement only.
    Every concrete transformation remains responsible for its exact request check,
    invoking both kind validators, and directly constructing its exact result. These
    obligations require explicit verification for every concrete transformation triple.
    Kind agreement does not infer numerical correctness or scientific qualification.
    """

    __slots__ = ()

    @property
    @abstractmethod
    def transformation_kind(self) -> RepresentationTransformationKind:
        """Return the fixed transformation-kind enum member owned by this Action.

        Returns
        -------
        RepresentationTransformationKind
            Exact operation family implemented by the Action.
        """

    @abstractmethod
    def transform(self) -> RepresentationTransformationResultABC:
        """Execute the request bound to this transformation.

        Concrete final transformations override this method with their exact concrete
        result return type. They directly construct that result, validate its kind, and
        return it without a configurable result-constructor seam.

        Returns
        -------
        RepresentationTransformationResultABC
            Nominal result refined covariantly by each concrete transformation.
        """

    @final
    def _require_compatible_request_kind(
        self,
        request: RepresentationTransformationRequestABC,
        /,
    ) -> None:
        """Reject a non-nominal request or request/Action kind disagreement.

        This helper does not establish the operation-specific concrete request type.
        The concrete transformation must perform that exact type check first.

        Parameters
        ----------
        request
            Concrete request already checked against the transformation's exact type.

        Raises
        ------
        TypeError
            If request membership or either enum type is invalid.
        ValueError
            If the request and Action enum members differ.
        """
        if not isinstance(request, RepresentationTransformationRequestABC):
            raise TypeError(
                "request must implement RepresentationTransformationRequestABC"
            )
        action_kind = self.transformation_kind
        if type(action_kind) is not RepresentationTransformationKind:
            raise TypeError(
                "Action transformation_kind must be a RepresentationTransformationKind"
            )
        request_kind = request.transformation_kind
        if type(request_kind) is not RepresentationTransformationKind:
            raise TypeError(
                "request transformation_kind must be a RepresentationTransformationKind"
            )
        if request_kind is not action_kind:
            raise ValueError("request transformation kind does not match Action kind")

    @final
    def _require_compatible_result_kind(
        self,
        result: RepresentationTransformationResultABC,
        /,
    ) -> None:
        """Reject a non-nominal result or result/Action kind disagreement.

        This helper does not establish the operation-specific concrete result type.
        The concrete transformation must construct and check that exact type first.

        Parameters
        ----------
        result
            Concrete result already checked against the transformation's exact type.

        Raises
        ------
        TypeError
            If result membership or either enum type is invalid.
        ValueError
            If the result and Action enum members differ.
        """
        if not isinstance(result, RepresentationTransformationResultABC):
            raise TypeError(
                "result must implement RepresentationTransformationResultABC"
            )
        action_kind = self.transformation_kind
        if type(action_kind) is not RepresentationTransformationKind:
            raise TypeError(
                "Action transformation_kind must be a RepresentationTransformationKind"
            )
        result_kind = result.transformation_kind
        if type(result_kind) is not RepresentationTransformationKind:
            raise TypeError(
                "result transformation_kind must be a RepresentationTransformationKind"
            )
        if result_kind is not action_kind:
            raise ValueError("result transformation kind does not match Action kind")


__all__ = [
    "RepresentationTransformationABC",
    "RepresentationTransformationRequestABC",
    "RepresentationTransformationResultABC",
]
