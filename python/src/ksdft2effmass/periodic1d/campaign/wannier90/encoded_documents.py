"""Exact encoded-document ownership for the periodic-1D Wannier90 campaign.

This immutable boundary separates retained wire bytes and an explicit schema
identity from native artifact bytes, decoded observations, represented operators,
provenance interpretation, verification policy, and protected execution.
"""

from dataclasses import dataclass

from ksdft2effmass.periodic1d.campaign.result_documents import (
    Periodic1DEncodedResultKind,
)


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90EncodedDocuments:
    """Store exact composite input and Wannier90 result document bytes.

    Parameters
    ----------
    composite_input_payload
        Nonempty exact built-in :class:`bytes` for the version-one composite campaign
        input document shared by the supported Wannier90 result variants.
    result_payload
        Nonempty exact built-in :class:`bytes` for one retained Wannier90 result
        document.
    result_kind
        Exact encoded-result discriminator for ``result_payload``. Only
        :attr:`Periodic1DEncodedResultKind.WANNIER90` and
        :attr:`Periodic1DEncodedResultKind.WANNIER90_PRECONDITIONED` are supported.

    Raises
    ------
    TypeError
        If either payload is not exact built-in :class:`bytes`, or if ``result_kind``
        is not exactly :class:`Periodic1DEncodedResultKind`.
    ValueError
        If either payload is empty or ``result_kind`` identifies another campaign
        result family.

    Notes
    -----
    This frozen DataObject owns encoded documents and their exact wire-variant identity
    only. It preserves caller-supplied byte objects without decoding, normalization,
    re-encoding, coercion, or copying. It is not a scientific model, retained space,
    retained or represented operator, decoded campaign result, or acceptance record.

    Native Wannier90 artifacts remain explicit
    ``Periodic1DWannier90NativeArtifactGroup`` values owned outside this record.
    Keeping those files separate prevents presence, path, rank, or filename from being
    inferred from an encoded result document. Correlation, native-file authentication,
    parsing, numerical verification, source provenance, and scientific interpretation
    belong to separate operations. A payload or SHA-256 digest establishes content
    identity only, not execution provenance, localization convergence, physical
    validity, uncertainty quantification, or acceptance.
    """

    composite_input_payload: bytes
    result_payload: bytes
    result_kind: Periodic1DEncodedResultKind

    def __post_init__(self) -> None:
        """Validate exact payload representations and wire-variant ownership.

        Raises
        ------
        TypeError
            If a payload or result-kind representation has the wrong exact type.
        ValueError
            If a payload is empty or the exact enum member is outside the two
            Wannier90 result variants.
        """
        self._check_args_payload_representations()
        self._check_args_result_kind()

    def _check_args_payload_representations(self) -> None:
        """Require two nonempty exact built-in byte representations.

        Raises
        ------
        TypeError
            If either encoded document is not exact built-in :class:`bytes`.
        ValueError
            If either exact byte representation is empty.
        """
        if type(self.composite_input_payload) is not bytes:
            raise TypeError("composite_input_payload must be built-in bytes")
        if not self.composite_input_payload:
            raise ValueError("composite_input_payload must be nonempty")
        if type(self.result_payload) is not bytes:
            raise TypeError("result_payload must be built-in bytes")
        if not self.result_payload:
            raise ValueError("result_payload must be nonempty")

    def _check_args_result_kind(self) -> None:
        """Require an exact discriminator for one supported Wannier90 wire variant.

        Raises
        ------
        TypeError
            If ``result_kind`` is not exactly
            :class:`Periodic1DEncodedResultKind`.
        ValueError
            If the enum member belongs to another encoded campaign result family.
        """
        if type(self.result_kind) is not Periodic1DEncodedResultKind:
            raise TypeError("result_kind must be Periodic1DEncodedResultKind")
        # The discriminator selects an exact result decoder; document content or a
        # filename must never be used to infer this wire-level identity.
        if self.result_kind not in {
            Periodic1DEncodedResultKind.WANNIER90,
            Periodic1DEncodedResultKind.WANNIER90_PRECONDITIONED,
        }:
            raise ValueError("result_kind must identify a supported Wannier90 result")
