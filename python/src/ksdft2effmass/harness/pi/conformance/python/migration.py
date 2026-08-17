"""Independent evidence predecessor and migration-map rule owner."""

from __future__ import annotations

import json
from dataclasses import dataclass


def _has_complete_predecessor_pairs(
    old_ids: tuple[str, ...],
    new_ids: tuple[str, ...],
    pairs: tuple[tuple[str, str], ...],
) -> bool:
    """Return whether one-to-one pairs exactly cover both inventories."""
    return (
        len(pairs) == len(old_ids) == len(new_ids)
        and len({old for old, _ in pairs}) == len(pairs)
        and len({new for _, new in pairs}) == len(pairs)
        and {old for old, _ in pairs} == set(old_ids)
        and {new for _, new in pairs} == set(new_ids)
    )


def _validate_migration(
    path: str, payload: bytes | None, read_error: str | None
) -> tuple[tuple[str, str, str, int | None], ...]:
    """Validate a closed complete one-to-one predecessor relation."""
    if read_error is not None:
        return (("TE.MIGRATION_INPUT", path, read_error, None),)
    assert payload is not None
    try:
        value = json.loads(payload.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        return (("TE.MIGRATION_INPUT", path, str(exc), None),)
    required = {
        "schema_version",
        "expected_old_node_ids",
        "expected_new_node_ids",
        "mappings",
    }
    if (
        type(value) is not dict
        or set(value) != required
        or value.get("schema_version") != 1
    ):
        return (
            (
                "TE.MIGRATION_INPUT",
                path,
                "migration input must have the exact schema-version-1 keys",
                None,
            ),
        )
    findings: list[tuple[str, str, str, int | None]] = []
    old, new, mappings = (
        value.get("expected_old_node_ids"),
        value.get("expected_new_node_ids"),
        value.get("mappings"),
    )
    for label, inventory in (("old", old), ("new", new)):
        if (
            type(inventory) is not list
            or any(type(item) is not str or not item for item in inventory)
            or len(inventory) != len(set(inventory))
        ):
            findings.append(
                (
                    "TE.MIGRATION_INVENTORY",
                    path,
                    f"expected {label} inventory must contain unique nonempty strings",
                    None,
                )
            )
    if type(mappings) is not list:
        findings.append(("TE.MIGRATION_INPUT", path, "mappings must be a list", None))
        return tuple(findings)
    pairs: list[tuple[str, str]] = []
    for index, item in enumerate(mappings):
        if (
            type(item) is not dict
            or set(item) != {"old_node_id", "new_node_id"}
            or type(item.get("old_node_id")) is not str
            or not item.get("old_node_id")
            or type(item.get("new_node_id")) is not str
            or not item.get("new_node_id")
        ):
            findings.append(
                (
                    "TE.MIGRATION_ENTRY",
                    path,
                    f"mappings[{index}] must be one exact nonempty old/new pair",
                    None,
                )
            )
        else:
            pairs.append((item["old_node_id"], item["new_node_id"]))
    if len({item[0] for item in pairs}) != len(pairs) or len(
        {item[1] for item in pairs}
    ) != len(pairs):
        findings.append(
            ("TE.MIGRATION_ONE_TO_ONE", path, "mapping sides must both be unique", None)
        )
    if (
        type(old) is list
        and type(new) is list
        and not _has_complete_predecessor_pairs(tuple(old), tuple(new), tuple(pairs))
    ):
        findings.append(
            (
                "TE.MIGRATION_INCOMPLETE",
                path,
                "mapping must exactly cover both expected node inventories",
                None,
            )
        )
    return tuple(findings)


def _predecessor_pairs(payload: bytes) -> tuple[tuple[str, str], ...]:
    """Extract immutable ``(new node, old node)`` predecessor pairs."""
    value = json.loads(payload.decode("utf-8"))
    return tuple(
        (item["new_node_id"], item["old_node_id"]) for item in value["mappings"]
    )


@dataclass(frozen=True, slots=True)
class _PythonEvidencePredecessorRuleResult:
    """Immutable predecessor-map findings and validated pairs."""

    findings: tuple[tuple[str, str, str, int | None], ...]
    pairs: tuple[tuple[str, str], ...]


class _PythonEvidencePredecessorRule:
    """Own complete one-to-one evidence predecessor policy."""

    __slots__ = ()

    def execute(
        self, path: str, payload: bytes | None, read_error: str | None
    ) -> _PythonEvidencePredecessorRuleResult:
        """Validate one map and expose pairs only when it is conforming."""
        findings = _validate_migration(path, payload, read_error)
        pairs = (
            _predecessor_pairs(payload) if not findings and payload is not None else ()
        )
        return _PythonEvidencePredecessorRuleResult(findings, pairs)
