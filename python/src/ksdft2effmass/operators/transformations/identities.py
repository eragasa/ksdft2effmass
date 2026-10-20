"""Immutable identities for directed representation-transformation edges."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import final

from ksdft2effmass.operators.representations.identities import (
    BlochSpaceRole,
    CellHoppingRepresentationRole,
    RepresentationIdentity,
)


class RepresentationTransformationKind(Enum):
    """Enumerate derivation-edge kinds between representation nodes.

    Attributes
    ----------
    frame_compression
        Frame compression ``F† H F`` from an ambient to a retained space.
    gauge_conjugation
        Internal-coordinate conjugation on a retained Bloch representation.
    alignment
        Corrective alignment under a separately declared admissible family.
    finite_fourier_conversion
        Conversion from a retained Bloch field to complete cell-hopping blocks.
    support_truncation
        Restriction of a complete coefficient inventory to declared support.
    fourier_reconstruction
        Construction of a retained Bloch field from cell-hopping coefficients.

    Notes
    -----
    These members classify directed edges, not node roles. The integer ``.value``
    is an internal discriminant; serializers must map members explicitly.
    """

    frame_compression = 1
    gauge_conjugation = 2
    alignment = 3
    finite_fourier_conversion = 4
    support_truncation = 5
    fourier_reconstruction = 6


def _require_nonempty_exact_string(value: str, name: str, /) -> str:
    """Validate one exact nonempty built-in string without normalization."""
    if type(value) is not str:
        raise TypeError(f"{name} must be an exact built-in string")
    if value == "":
        raise ValueError(f"{name} must not be empty")
    return value


def _require_compatible_role_transition(
    kind: RepresentationTransformationKind,
    source: RepresentationIdentity,
    target: RepresentationIdentity,
) -> None:
    """Reject a source/target role transition incompatible with ``kind``."""
    source_role = source.role
    target_role = target.role
    valid = False
    if kind is RepresentationTransformationKind.frame_compression:
        valid = (
            source_role is BlochSpaceRole.ambient
            and target_role is BlochSpaceRole.retained
        )
    elif kind in (
        RepresentationTransformationKind.gauge_conjugation,
        RepresentationTransformationKind.alignment,
    ):
        valid = (
            source_role is BlochSpaceRole.retained
            and target_role is BlochSpaceRole.retained
        )
    elif kind is RepresentationTransformationKind.finite_fourier_conversion:
        valid = (
            source_role is BlochSpaceRole.retained
            and target_role is CellHoppingRepresentationRole.complete_declared_inventory
        )
    elif kind is RepresentationTransformationKind.support_truncation:
        valid = (
            source_role is CellHoppingRepresentationRole.complete_declared_inventory
            and target_role is CellHoppingRepresentationRole.support_truncated
        )
    elif kind is RepresentationTransformationKind.fourier_reconstruction:
        valid = (
            type(source_role) is CellHoppingRepresentationRole
            and target_role is BlochSpaceRole.retained
        )
    if not valid:
        raise ValueError(
            "source and target roles are incompatible with transformation kind"
        )


@final
@dataclass(frozen=True, slots=True)
class TransformationIdentity:
    """Identify one directed derivation edge between representation nodes.

    Parameters
    ----------
    transformation_id
        Exact nonempty identity of this edge.
    kind
        Explicit derivation-kind enum member.
    method_id
        Exact nonempty identity of the construction or solver method.
    orientation
        Exact nonempty convention for source/target and adjoint orientation.
    source_identity
        Exact source representation-node identity.
    target_identity
        Exact target representation-node identity.

    Raises
    ------
    TypeError
        If the kind, an endpoint, or a textual field violates its exact nominal
        type.
    ValueError
        If text is empty or the source/target roles are incompatible with ``kind``.

    Notes
    -----
    The edge identity performs no numerical transformation and is not a witness,
    qualification result, evidence record, or formal proof.
    """

    transformation_id: str
    kind: RepresentationTransformationKind
    method_id: str
    orientation: str
    source_identity: RepresentationIdentity
    target_identity: RepresentationIdentity

    def __post_init__(self) -> None:
        """Validate exact edge metadata, endpoints, and enum-compatible roles."""
        _require_nonempty_exact_string(
            self.transformation_id,
            "transformation identity",
        )
        if type(self.kind) is not RepresentationTransformationKind:
            raise TypeError("kind must be a RepresentationTransformationKind")
        _require_nonempty_exact_string(self.method_id, "method identity")
        _require_nonempty_exact_string(self.orientation, "transformation orientation")
        if type(self.source_identity) is not RepresentationIdentity:
            raise TypeError("source_identity must be an exact RepresentationIdentity")
        if type(self.target_identity) is not RepresentationIdentity:
            raise TypeError("target_identity must be an exact RepresentationIdentity")
        _require_compatible_role_transition(
            self.kind,
            self.source_identity,
            self.target_identity,
        )


@final
class TransformationIdentityFactory:
    """Construct carrier-compatible representation-transformation identities.

    The explicit enum argument keeps the edge kind visible in domain code. The
    factory creates identity metadata only and does not apply an operation.
    """

    __slots__ = ()

    def create(
        self,
        *,
        transformation_id: str,
        kind: RepresentationTransformationKind,
        method_id: str,
        orientation: str,
        source_identity: RepresentationIdentity,
        target_identity: RepresentationIdentity,
    ) -> TransformationIdentity:
        """Construct one validated directed transformation identity.

        Parameters
        ----------
        transformation_id
            Exact nonempty edge identity.
        kind
            Explicit transformation-kind enum member.
        method_id
            Exact nonempty method identity.
        orientation
            Exact nonempty source/target and adjoint convention.
        source_identity
            Exact source representation identity.
        target_identity
            Exact target representation identity.

        Returns
        -------
        TransformationIdentity
            Immutable edge identity with a carrier-compatible role transition.
        """
        if type(kind) is not RepresentationTransformationKind:
            raise TypeError("kind must be a RepresentationTransformationKind")
        if type(source_identity) is not RepresentationIdentity:
            raise TypeError("source_identity must be an exact RepresentationIdentity")
        if type(target_identity) is not RepresentationIdentity:
            raise TypeError("target_identity must be an exact RepresentationIdentity")
        return TransformationIdentity(
            transformation_id=transformation_id,
            kind=kind,
            method_id=method_id,
            orientation=orientation,
            source_identity=source_identity,
            target_identity=target_identity,
        )


__all__ = [
    "RepresentationTransformationKind",
    "TransformationIdentity",
    "TransformationIdentityFactory",
]
