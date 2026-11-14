"""Cross-wire correlation for the rank-one first-passing certification.

Validation in this module is structural. It authenticates canonical bytes and their
cross-record bindings, then reports the exact endpoint disposition already checked by
the result record. It does not establish outward interval containment or admit a runtime
certification as evidence.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from hashlib import sha256
from typing import Self

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from .records import (
    CONTRACT_ID,
    SUPPORT_INVENTORY,
    FirstPassingSupportDisposition,
    FirstPassingSupportRequest,
    FirstPassingSupportResult,
)

_SHA256_PATTERN = re.compile(r"[0-9a-f]{64}\Z")
_IDENTIFIER_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")


@dataclass(frozen=True, slots=True)
class FirstPassingSupportWireValidation(BaseTypedRecord):
    """Retain structural validation of one canonical request/result wire pair.

    Parameters
    ----------
    certificate_id
        Portable certification identity shared by the correlated records.
    request_sha256
        SHA-256 digest of the exact canonical request bytes.
    result_sha256
        SHA-256 digest of the exact canonical result bytes.
    selected_support
        Dimensionless support correlated between request and result.
    disposition
        Exact endpoint disposition reported by the validated result.

    Raises
    ------
    TypeError
        A field has the wrong exact type; booleans are not support integers.
    ValueError
        An identity, digest, or support violates its closed contract.

    Notes
    -----
    This record reports structural correlation only. It does not report verified
    outward containment.
    """

    certificate_id: str
    request_sha256: str
    result_sha256: str
    selected_support: int
    disposition: FirstPassingSupportDisposition

    def __post_init__(self) -> None:
        if type(self.certificate_id) is not str:
            raise TypeError("certificate_id must be a built-in str")
        if _IDENTIFIER_PATTERN.fullmatch(self.certificate_id) is None:
            raise ValueError("certificate_id must be a portable identifier")
        for name, value in (
            ("request_sha256", self.request_sha256),
            ("result_sha256", self.result_sha256),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if _SHA256_PATTERN.fullmatch(value) is None:
                raise ValueError(
                    f"{name} must be a 64-character lowercase SHA-256 digest"
                )
        if type(self.selected_support) is not int:
            raise TypeError("selected_support must be a built-in int excluding bool")
        if self.selected_support not in SUPPORT_INVENTORY:
            raise ValueError(
                "selected_support is outside the complete support inventory"
            )
        if not isinstance(self.disposition, FirstPassingSupportDisposition):
            raise TypeError("disposition must be FirstPassingSupportDisposition")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "certificate_id": self.certificate_id,
            "request_sha256": self.request_sha256,
            "result_sha256": self.result_sha256,
            "selected_support": self.selected_support,
            "disposition": self.disposition.to_wire(),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        expected = {
            "certificate_id",
            "request_sha256",
            "result_sha256",
            "selected_support",
            "disposition",
        }
        if set(values) != expected:
            raise ValueError("wire-validation fields do not match the contract")
        certificate_id = values["certificate_id"]
        request_sha256 = values["request_sha256"]
        result_sha256 = values["result_sha256"]
        selected_support = values["selected_support"]
        disposition = values["disposition"]
        if type(certificate_id) is not str:
            raise TypeError("certificate_id must decode to a built-in str")
        if type(request_sha256) is not str or type(result_sha256) is not str:
            raise TypeError("wire digests must decode to built-in strings")
        if type(selected_support) is not int:
            raise TypeError("selected_support must decode to a built-in int")
        if type(disposition) is not str:
            raise TypeError("disposition must decode to a built-in str")
        return cls(
            certificate_id=certificate_id,
            request_sha256=request_sha256,
            result_sha256=result_sha256,
            selected_support=selected_support,
            disposition=FirstPassingSupportDisposition.from_wire(disposition),
        )


class FirstPassingSupportWireValidator:
    """Validate canonical certification bytes and their cross-record bindings.

    Notes
    -----
    The action has no mutable state and performs no filesystem access. Successful
    validation establishes canonical decoding, exact byte digests, certification
    identity correlation, support correlation, and endpoint classification only.
    """

    __slots__ = ()

    CONTRACT_ID = CONTRACT_ID

    def validate(
        self,
        request_wire: bytes,
        result_wire: bytes,
    ) -> FirstPassingSupportWireValidation:
        """Validate one canonical pair without asserting interval containment.

        Parameters
        ----------
        request_wire
            Canonical UTF-8 JSON bytes produced by
            :meth:`FirstPassingSupportRequest.to_json`.
        result_wire
            Canonical UTF-8 JSON bytes produced by
            :meth:`FirstPassingSupportResult.to_json`.

        Returns
        -------
        FirstPassingSupportWireValidation
            Immutable byte identities, correlated support, and endpoint disposition.

        Raises
        ------
        TypeError
            A wire or decoded field has the wrong exact type.
        ValueError
            Decoding, canonical-byte admission, request-digest binding, certificate
            identity correlation, or support correlation fails.

        Notes
        -----
        No enclosure computation or independent containment replay is performed.
        """
        request = FirstPassingSupportRequest.from_json(request_wire)
        result = FirstPassingSupportResult.from_json(result_wire)
        # Re-serialization admits only the package's one canonical byte representation.
        if request.to_json() != request_wire:
            raise ValueError("request bytes are not the canonical representation")
        if result.to_json() != result_wire:
            raise ValueError("result bytes are not the canonical representation")
        # Correlate the result to the admitted request bytes, not merely decoded values.
        request_digest = sha256(request_wire).hexdigest()
        if result.request_sha256 != request_digest:
            raise ValueError(
                "certification result request_sha256 does not match request"
            )
        self._validate_identity_correlation(request, result)
        return FirstPassingSupportWireValidation(
            certificate_id=request.certificate_id,
            request_sha256=request_digest,
            result_sha256=sha256(result_wire).hexdigest(),
            selected_support=request.selected_support,
            disposition=result.disposition,
        )

    @staticmethod
    def _validate_identity_correlation(
        request: FirstPassingSupportRequest,
        result: FirstPassingSupportResult,
    ) -> None:
        if result.certificate_id != request.certificate_id:
            raise ValueError("certificate_id differs between request and result")
        if result.selected_support != request.selected_support:
            raise ValueError("selected_support differs between request and result")


__all__ = [
    "FirstPassingSupportWireValidation",
    "FirstPassingSupportWireValidator",
]
