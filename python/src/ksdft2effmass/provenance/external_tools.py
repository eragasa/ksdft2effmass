"""Immutable declarations for externally supplied tool capabilities.

This module owns the declaration layer of the external-tool lifecycle: stable
family identity, requested installation metadata, and declared capabilities.
Each frozen, slotted DataObject stores only its constructor fields and validates
its intrinsic invariants directly in ``__post_init__``.  No shared validator,
canonicalization service, or derived mutable state is used.

The dependency direction is outward from these declarations: observation,
execution, actions, and serialization layers may import them, while this module
imports none of those layers.  The records do not discover, import, probe, or
execute tools; interpret version precedence; grant authorization; or establish
availability, numerical correctness, scientific validation, or uncertainty
quantification.  Wrong semantic Python types raise :class:`TypeError`; values
of the correct type that violate the documented lexical invariants raise
:class:`ValueError`.  Construction performs no input/output.

Examples
--------
Construct declarations through the supported package API::

    from ksdft2effmass.provenance import ExternalToolIdentity

    identity = ExternalToolIdentity("qe", "quantum-espresso")
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from enum import StrEnum

# Exact version-1 portable identifier and opaque-version lexical grammars.
_ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
_VERSION_PATTERN = re.compile(r"[0-9A-Za-z][0-9A-Za-z._+-]{0,63}\Z")


class CapabilityKind(StrEnum):
    """Closed version-1 categories of externally provided behavior.

    Attributes
    ----------
    EXECUTE
        Capability to request external activity.
    PARSE
        Capability to parse an externally defined representation.
    RENDER
        Capability to render an externally defined representation.
    TRANSFER
        Capability to transfer an artifact across an external boundary.

    Notes
    -----
    Declaration order and string values are versioned wire vocabulary.  A kind
    classifies a declared interface only; it does not prove that an installation
    exists or that the behavior is scientifically suitable.
    """

    EXECUTE = "execute"
    PARSE = "parse"
    RENDER = "render"
    TRANSFER = "transfer"


@dataclass(frozen=True, slots=True)
class ExternalToolIdentity:
    """Stable identity of an external tool family.

    Parameters
    ----------
    tool_id
        Stable project identity matching
        ``[A-Za-z0-9][A-Za-z0-9._:-]{0,127}``.
    implementation_family
        Portable implementation-family identifier under the same grammar.  It
        is not a dynamic import name or plugin registration key.

    Raises
    ------
    TypeError
        If either field is not a built-in :class:`str`.
    ValueError
        If either field is empty, contains Unicode surrogates, is not Unicode
        NFC, or violates the portable identifier grammar.

    Notes
    -----
    Both fields are stored unchanged.  The record has no derived state and does
    not locate an executable, package, installation, or runtime client.
    """

    tool_id: str
    implementation_family: str

    def __post_init__(self) -> None:
        """Validate the two directly owned portable identifiers."""
        for value, name in (
            (self.tool_id, "tool_id"),
            (self.implementation_family, "implementation_family"),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not value:
                raise ValueError(f"{name} must not be empty")
            if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
                raise ValueError(f"{name} must not contain Unicode surrogates")
            if unicodedata.normalize("NFC", value) != value:
                raise ValueError(f"{name} must be Unicode NFC")
            if _ID_PATTERN.fullmatch(value) is None:
                raise ValueError(f"{name} is not a portable identifier")


@dataclass(frozen=True, slots=True)
class ExternalToolSpecification:
    """Immutable requested external-tool installation specification.

    Parameters
    ----------
    specification_id
        Stable declaration identity under the portable identifier grammar.
    tool_id
        Identity of the declared external-tool family under that grammar.
    requested_version
        Opaque portable lexical version text matching
        ``[0-9A-Za-z][0-9A-Za-z._+-]{0,63}``.
    executable_or_package_id
        Declared executable or package identifier, never a runtime handle.

    Raises
    ------
    TypeError
        If a field is not a built-in :class:`str`.
    ValueError
        If text is empty, contains a Unicode surrogate, is not NFC, or violates
        its identifier or version grammar.

    Notes
    -----
    Fields are stored unchanged; version text is not parsed, ordered, resolved,
    or compared.  This declaration neither discovers nor verifies software.
    """

    specification_id: str
    tool_id: str
    requested_version: str
    executable_or_package_id: str

    def __post_init__(self) -> None:
        """Validate directly owned identifier and opaque-version fields."""
        for value, name, pattern, grammar_message in (
            (
                self.specification_id,
                "specification_id",
                _ID_PATTERN,
                "is not a portable identifier",
            ),
            (self.tool_id, "tool_id", _ID_PATTERN, "is not a portable identifier"),
            (
                self.requested_version,
                "requested_version",
                _VERSION_PATTERN,
                "is not portable lexical version text",
            ),
            (
                self.executable_or_package_id,
                "executable_or_package_id",
                _ID_PATTERN,
                "is not a portable identifier",
            ),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not value:
                raise ValueError(f"{name} must not be empty")
            if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
                raise ValueError(f"{name} must not contain Unicode surrogates")
            if unicodedata.normalize("NFC", value) != value:
                raise ValueError(f"{name} must be Unicode NFC")
            if pattern.fullmatch(value) is None:
                raise ValueError(f"{name} {grammar_message}")


@dataclass(frozen=True, slots=True)
class DeclaredCapability:
    """One immutable capability requested from an external tool.

    Parameters
    ----------
    capability_id
        Stable declaration identity under the portable identifier grammar.
    tool_id
        Declared provider tool identity under the same grammar.
    kind
        Exact version-1 :class:`CapabilityKind` category.
    name
        Narrow capability name under the portable identifier grammar.
    specification_version
        Identifier-form version of the project-owned capability contract.

    Raises
    ------
    TypeError
        If a textual field is not a built-in :class:`str` or ``kind`` is not a
        :class:`CapabilityKind`.
    ValueError
        If textual state is empty, contains a Unicode surrogate, is not NFC, or
        violates the portable identifier grammar.

    Notes
    -----
    All state is stored unchanged and no capability is invoked or verified.
    The declaration makes no availability or scientific-validity claim.
    """

    capability_id: str
    tool_id: str
    kind: CapabilityKind
    name: str
    specification_version: str

    def __post_init__(self) -> None:
        """Validate this declaration's identifiers and exact enum member."""
        for value, field_name in (
            (self.capability_id, "capability_id"),
            (self.tool_id, "tool_id"),
        ):
            if type(value) is not str:
                raise TypeError(f"{field_name} must be a built-in str")
            if not value:
                raise ValueError(f"{field_name} must not be empty")
            if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
                raise ValueError(f"{field_name} must not contain Unicode surrogates")
            if unicodedata.normalize("NFC", value) != value:
                raise ValueError(f"{field_name} must be Unicode NFC")
            if _ID_PATTERN.fullmatch(value) is None:
                raise ValueError(f"{field_name} is not a portable identifier")
        if not isinstance(self.kind, CapabilityKind):
            raise TypeError("kind must be a CapabilityKind")
        for value, field_name in (
            (self.name, "name"),
            (self.specification_version, "specification_version"),
        ):
            if type(value) is not str:
                raise TypeError(f"{field_name} must be a built-in str")
            if not value:
                raise ValueError(f"{field_name} must not be empty")
            if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
                raise ValueError(f"{field_name} must not contain Unicode surrogates")
            if unicodedata.normalize("NFC", value) != value:
                raise ValueError(f"{field_name} must be Unicode NFC")
            if _ID_PATTERN.fullmatch(value) is None:
                raise ValueError(f"{field_name} is not a portable identifier")
