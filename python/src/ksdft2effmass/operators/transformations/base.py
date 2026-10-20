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


class RepresentationTransformationABC[
    RequestT: RepresentationTransformationRequestABC,
    ResultT: RepresentationTransformationResultABC,
](ABC):
    """Transform one nominal request into one same-kind nominal result.

    Concrete Actions expose one fixed :attr:`transformation_kind` and implement the
    public :meth:`transform` operation. Implementations must reject a request or result
    whose exact enum member differs from the Action. The protected final validation
    methods provide shared fail-closed checks without replacing the selected abstract
    public override point. Kind agreement does not infer correctness or qualification.
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
    def transform(self, request: RequestT, /) -> ResultT:
        """Transform one operation-specific request into one nominal result.

        Concrete Actions implement this public method and must apply the fail-closed
        request and result kind checks, either through the protected validation methods
        below or through an equally strict operation-specific refinement.

        Parameters
        ----------
        request
            Nominal operation-specific request.

        Returns
        -------
        ResultT
            Operation-specific result carrying the same enum member.
        """

    @final
    def _require_compatible_request_kind(self, request: RequestT, /) -> None:
        """Reject a non-nominal request or request/Action kind disagreement.

        Parameters
        ----------
        request
            Operation-specific request to validate before numerical work.

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
    def _require_compatible_result_kind(self, result: ResultT, /) -> ResultT:
        """Return a nominal result after rejecting result/Action kind disagreement.

        Parameters
        ----------
        result
            Operation-specific result to validate before returning it.

        Returns
        -------
        ResultT
            The unchanged same-kind nominal result.

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
        return result


__all__ = [
    "RepresentationTransformationABC",
    "RepresentationTransformationRequestABC",
    "RepresentationTransformationResultABC",
]
