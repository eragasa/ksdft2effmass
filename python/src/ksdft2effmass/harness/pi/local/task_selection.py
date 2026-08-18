"""Minimal project-local development Task selection state.

``DevelopmentTaskSelection`` owns only current selection and activation-reference
facts. Task identity, hierarchy, prerequisites, lifecycle, scope, and sequence
remain in canonical ``HarnessTask`` records. The serializer and deserializer own
the strict version-1 JSON representation. This module performs no repository
discovery, Task activation, authority interpretation, persistence, scientific
workflow control, or automatic successor selection.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from ..identity import (
    Identifier,
    _require_sorted_unique,
    _require_tuple,
    _require_version,
)
from .task_model import _require_local_identifier


@dataclass(frozen=True, slots=True)
class DevelopmentTaskSelection:
    """Represent minimal selection facts without Task topology.

    Parameters
    ----------
    schema_version
        Selection-state schema version, fixed to ``1``.
    active_task_id
        Exact currently selected Task identity, or ``None`` when no Task is
        selected. The value grants no authority or permission.
    explicit_activation_receipt_ids
        Sorted unique references to explicit activation receipts applicable to the
        represented selection state. Receipts are referenced, not embedded or
        interpreted.
    automatic_successor_activation
        Explicit policy flag. Version 1 accepts only ``False``; graph eligibility
        never activates a Task automatically.

    Raises
    ------
    TypeError
        If a field has the wrong semantic built-in type.
    ValueError
        If a version, identifier, ordering, uniqueness, or disabled-policy
        invariant fails.

    Notes
    -----
    Protected execution, publication authority, Task lifecycle, development
    decisions, and scientific CPN or Workflow state are outside this record.
    """

    schema_version: int
    active_task_id: Identifier | None
    explicit_activation_receipt_ids: tuple[Identifier, ...]
    automatic_successor_activation: bool

    def __post_init__(self) -> None:
        if _require_version(self.schema_version, "schema_version") != 1:
            raise ValueError("schema_version must equal 1")
        if self.active_task_id is not None:
            _require_local_identifier(self.active_task_id, "active_task_id")
        _require_tuple(
            self.explicit_activation_receipt_ids,
            "explicit_activation_receipt_ids",
        )
        for receipt_id in self.explicit_activation_receipt_ids:
            _require_local_identifier(receipt_id, "explicit_activation_receipt_id")
        _require_sorted_unique(
            self.explicit_activation_receipt_ids,
            "explicit_activation_receipt_ids",
        )
        if type(self.automatic_successor_activation) is not bool:
            raise TypeError("automatic_successor_activation must be bool")
        if self.automatic_successor_activation:
            raise ValueError("automatic_successor_activation must be false")


class DevelopmentTaskSelectionSerializer:
    """Serialize :class:`DevelopmentTaskSelection` to canonical JSON bytes."""

    __slots__ = ()

    def execute(self, selection: DevelopmentTaskSelection) -> bytes:
        """Return the canonical version-1 selection-state representation.

        Parameters
        ----------
        selection
            Exact immutable selection state.

        Returns
        -------
        bytes
            UTF-8 JSON with constructor field order, two-space indentation, literal
            Unicode, and exactly one final LF.

        Raises
        ------
        TypeError
            If ``selection`` is not exactly :class:`DevelopmentTaskSelection`.
        """
        if type(selection) is not DevelopmentTaskSelection:
            raise TypeError("selection must be DevelopmentTaskSelection")
        value = {
            "schema_version": selection.schema_version,
            "active_task_id": selection.active_task_id,
            "explicit_activation_receipt_ids": list(
                selection.explicit_activation_receipt_ids
            ),
            "automatic_successor_activation": (
                selection.automatic_successor_activation
            ),
        }
        return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


class DevelopmentTaskSelectionDeserializer:
    """Strictly deserialize version-1 development Task selection JSON."""

    __slots__ = ()

    def execute(self, payload: bytes) -> DevelopmentTaskSelection:
        """Return the immutable selection state represented by ``payload``.

        Parameters
        ----------
        payload
            Exact built-in bytes containing one UTF-8 JSON object.

        Returns
        -------
        DevelopmentTaskSelection
            Strictly decoded and intrinsically validated state.

        Raises
        ------
        TypeError
            If bytes or represented fields have wrong semantic types.
        ValueError
            If UTF-8, JSON, key closure, version, or value invariants fail.
        """
        if type(payload) is not bytes:
            raise TypeError("payload must be bytes")
        if payload.startswith(b"\xef\xbb\xbf"):
            raise ValueError("payload must not contain a UTF-8 BOM")

        def object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
            result: dict[str, Any] = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError(f"duplicate JSON key {key}")
                result[key] = value
            return result

        try:
            value = json.loads(payload.decode("utf-8"), object_pairs_hook=object_pairs)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("payload must be one UTF-8 JSON value") from exc
        if type(value) is not dict:
            raise TypeError("payload must represent a JSON object")
        expected = {
            "schema_version",
            "active_task_id",
            "explicit_activation_receipt_ids",
            "automatic_successor_activation",
        }
        missing = expected - set(value)
        unknown = set(value) - expected
        if missing:
            raise ValueError(f"missing field {sorted(missing)[0]}")
        if unknown:
            raise ValueError(f"unknown field {sorted(unknown)[0]}")
        receipts = value["explicit_activation_receipt_ids"]
        if type(receipts) is not list:
            raise TypeError("explicit_activation_receipt_ids must be a JSON array")
        return DevelopmentTaskSelection(
            value["schema_version"],
            value["active_task_id"],
            tuple(receipts),
            value["automatic_successor_activation"],
        )
