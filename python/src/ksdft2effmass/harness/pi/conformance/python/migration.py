"""Independent evidence migration and projection-debt rule owner."""

from __future__ import annotations

import json
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class _PythonEvidenceMigrationRuleResult:
    """Immutable migration findings, predecessor pairs, and legacy owner debt."""

    findings: tuple[tuple[str, str, str, int | None], ...]
    pairs: tuple[tuple[str, str], ...]
    legacy_test_owner_paths: tuple[str, ...] | None

    def activated_legacy_test_owner_paths(
        self, source_paths: tuple[str, ...]
    ) -> tuple[str, ...]:
        """Resolve schema-v1 whole-corpus compatibility or schema-v2 path debt."""
        if self.legacy_test_owner_paths is None:
            return tuple(sorted(set(source_paths)))
        return self.legacy_test_owner_paths


class _PythonEvidenceMigrationRule:
    """Own predecessor relations and bounded test-owner projection migration."""

    __slots__ = ()

    def execute(
        self, path: str, payload: bytes | None, read_error: str | None
    ) -> _PythonEvidenceMigrationRuleResult:
        """Validate one migration resource and expose only conforming state."""
        findings = self._validate(path, payload, read_error)
        if findings or payload is None:
            return _PythonEvidenceMigrationRuleResult(findings, (), None)
        value = json.loads(payload.decode("utf-8"))
        pairs = tuple(
            (item["new_node_id"], item["old_node_id"]) for item in value["mappings"]
        )
        legacy_paths = (
            tuple(value["legacy_test_owner_paths"])
            if value["schema_version"] == 2
            else None
        )
        return _PythonEvidenceMigrationRuleResult(findings, pairs, legacy_paths)

    @classmethod
    def _validate(
        cls, path: str, payload: bytes | None, read_error: str | None
    ) -> tuple[tuple[str, str, str, int | None], ...]:
        """Validate a closed predecessor relation and explicit legacy path set."""
        if read_error is not None:
            return (("TE.MIGRATION_INPUT", path, read_error, None),)
        assert payload is not None
        try:
            value = json.loads(payload.decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError) as exc:
            return (("TE.MIGRATION_INPUT", path, str(exc), None),)
        base_keys = {
            "schema_version",
            "expected_old_node_ids",
            "expected_new_node_ids",
            "mappings",
        }
        version = value.get("schema_version") if type(value) is dict else None
        required = (
            base_keys if version == 1 else base_keys | {"legacy_test_owner_paths"}
        )
        if type(value) is not dict or version not in {1, 2} or set(value) != required:
            return (
                (
                    "TE.MIGRATION_INPUT",
                    path,
                    "migration input must have exact schema-version-1 or -2 keys",
                    None,
                ),
            )
        findings: list[tuple[str, str, str, int | None]] = []
        old = value.get("expected_old_node_ids")
        new = value.get("expected_new_node_ids")
        mappings = value.get("mappings")
        legacy_paths = value.get("legacy_test_owner_paths", [])
        if (
            type(legacy_paths) is not list
            or any(
                type(item) is not str
                or not item.endswith(".py")
                or item.startswith("/")
                or ".." in item.split("/")
                or "::" in item
                for item in legacy_paths
            )
            or legacy_paths != sorted(set(legacy_paths))
        ):
            findings.append(
                (
                    "TE.MIGRATION_LEGACY_OWNER_PATHS",
                    path,
                    "legacy test-owner paths must be sorted unique relative Python "
                    "module paths",
                    None,
                )
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
                        f"expected {label} inventory must contain unique nonempty "
                        "strings",
                        None,
                    )
                )
        if type(mappings) is not list:
            findings.append(
                ("TE.MIGRATION_INPUT", path, "mappings must be a list", None)
            )
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
                (
                    "TE.MIGRATION_ONE_TO_ONE",
                    path,
                    "mapping sides must both be unique",
                    None,
                )
            )
        if (
            type(old) is list
            and type(new) is list
            and not cls._has_complete_predecessor_pairs(
                tuple(old), tuple(new), tuple(pairs)
            )
        ):
            findings.append(
                (
                    "TE.MIGRATION_INCOMPLETE",
                    path,
                    "mapping must exactly cover both expected node inventories",
                    None,
                )
            )
        if type(legacy_paths) is list:
            owner_migration_paths = {
                new_node.split("::", maxsplit=1)[0]
                for _, new_node in pairs
                if "::Test" in new_node
            }
            contradictory = sorted(owner_migration_paths & set(legacy_paths))
            if contradictory:
                findings.append(
                    (
                        "TE.MIGRATION_OWNER_MODE",
                        path,
                        "class-qualified predecessors conflict with legacy owner path "
                        f"{contradictory[0]}",
                        None,
                    )
                )
        return tuple(findings)

    @staticmethod
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
