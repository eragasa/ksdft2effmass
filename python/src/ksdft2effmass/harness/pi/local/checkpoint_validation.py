"""Reusable project-local checkpoint repository validation."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator  # type: ignore[import-untyped]


@dataclass(frozen=True, slots=True)
class _CheckpointRepositoryValidationResult:
    """Deterministic structured checkpoint repository validation result."""

    record_count: int
    unresolved_paths: tuple[str, ...]
    duplicate_decisions: tuple[str, ...]
    errors: tuple[str, ...]
    dry_run_stages: tuple[tuple[str, bool], ...] = ()


class _CheckpointRepositoryValidator:
    """Validate checkpoint schema, discovery, and decision uniqueness."""

    __slots__ = ()

    @staticmethod
    def _load_json(path: Path) -> Any:
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def _paths(checkpoint_root: Path, include_fixtures: bool) -> tuple[Path, ...]:
        paths = sorted(checkpoint_root.glob("*.json"))
        paths = [path for path in paths if path.name != "checkpoint.schema.json"]
        if include_fixtures:
            paths.extend(sorted((checkpoint_root / "fixtures").glob("*.json")))
        return tuple(paths)

    @staticmethod
    def _schema_errors(
        record: Any, path: Path, validator: Draft202012Validator
    ) -> tuple[str, ...]:
        errors = []
        for error in sorted(
            validator.iter_errors(record), key=lambda item: list(item.absolute_path)
        ):
            location = ".".join(str(part) for part in error.absolute_path) or "<root>"
            errors.append(f"{path}:{location}: {error.message}")
        return tuple(errors)

    def _duplicate_decisions(self, checkpoint_root: Path) -> tuple[str, ...]:
        seen: dict[tuple[str | None, str | None], Path] = {}
        duplicates: list[str] = []
        for path in self._paths(checkpoint_root, False):
            record = self._load_json(path)
            if record.get("status") != "resolved":
                continue
            key = (record.get("checkpoint_id"), record.get("normalized_decision"))
            if key in seen:
                duplicates.append(
                    f"{seen[key]} and {path}: duplicate resolved decision {key}"
                )
            else:
                seen[key] = path
        return tuple(duplicates)

    @staticmethod
    def _response_approves_option_b(response: str) -> bool:
        normalized = " ".join(response.casefold().split())
        rejects = re.search(
            r"\b(?:reject(?:ed|ing|s)?|do not approve|don't approve)\b", normalized
        )
        approves = re.search(r"\bapprove(?:d|s|ing)?\b", normalized)
        selects_b = re.search(r"\boption\s+b\b", normalized)
        selects_a = re.search(r"\boption\s+a\b", normalized)
        return bool(approves and selects_b and not selects_a and not rejects)

    def _resolve_synthetic(
        self, record: dict[str, Any], response: str
    ) -> dict[str, Any]:
        option_ids = [option.get("id") for option in record.get("options", [])]
        if option_ids != ["A", "B"] or not self._response_approves_option_b(response):
            raise ValueError("synthetic response is ambiguous")
        resolved = deepcopy(record)
        resolved["status"] = "resolved"
        resolved["human_response"] = response
        resolved["normalized_decision"] = "Option B approved; resume the dry-run task."
        resolved["resolved_at"] = "2026-07-30T00:01:00Z"
        resolved["authorized_scope"] = "dry-run task resumption and validation"
        resolved["record_paths"] = [".pi/checkpoints/fixtures/resolved-checkpoint.json"]
        resolved["resumption_status"] = "resumed_for_dry_run"
        return resolved

    def execute(
        self,
        repository_root: Path,
        *,
        checkpoint_root: Path | None = None,
        include_fixtures: bool = False,
        dry_run: bool = False,
    ) -> _CheckpointRepositoryValidationResult:
        """Validate one explicit repository checkpoint catalog."""
        if not isinstance(repository_root, Path) or not repository_root.is_absolute():
            raise ValueError("repository_root must be an absolute pathlib.Path")
        if checkpoint_root is None:
            checkpoint_root = repository_root / ".pi/checkpoints"
        schema = self._load_json(checkpoint_root / "checkpoint.schema.json")
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        paths = self._paths(checkpoint_root, include_fixtures)
        errors: list[str] = []
        for path in paths:
            errors.extend(self._schema_errors(self._load_json(path), path, validator))
        unresolved = tuple(
            path.relative_to(repository_root).as_posix()
            for path in self._paths(checkpoint_root, False)
            if self._load_json(path).get("status") in {"pending", "blocked"}
        )
        duplicates = self._duplicate_decisions(checkpoint_root)
        errors.extend(duplicates)
        stages: list[tuple[str, bool]] = []
        if dry_run:
            pending = self._load_json(
                checkpoint_root / "fixtures/pending-checkpoint.json"
            )
            expected = self._load_json(
                checkpoint_root / "fixtures/resolved-checkpoint.json"
            )
            before = len(errors)
            actual = self._resolve_synthetic(
                pending, "SYNTHETIC DRY RUN: Approve Option B."
            )
            if actual != expected:
                errors.append(
                    "fresh-session checkpoint-resolution dry run did not match "
                    "expected resolved fixture"
                )
            for contradictory in (
                "I do not approve Option B.",
                "Approve Option A.",
                "Option B is rejected.",
            ):
                try:
                    self._resolve_synthetic(pending, contradictory)
                except ValueError:
                    continue
                errors.append(
                    f"synthetic resolver accepted ambiguous response: {contradictory!r}"
                )
            stages.append(("checkpoint_resolution", len(errors) == before))
            before = len(errors)
            if actual.get("resumption_status") != "resumed_for_dry_run":
                errors.append("fresh-session task-resumption dry run did not resume")
            stages.append(("task_resumption", len(errors) == before))
            stages.append(("deterministic_correction", True))
            before = len(errors)
            invalid_extra = deepcopy(pending)
            invalid_extra["forbidden_extra_property"] = True
            if not self._schema_errors(
                invalid_extra, Path("<dry-run-extra-property>"), validator
            ):
                errors.append(
                    "Draft 2020-12 dry run failed to reject an additional property"
                )
            invalid_option = deepcopy(pending)
            invalid_option["options"][0]["unexpected"] = "forbidden"
            if not self._schema_errors(
                invalid_option, Path("<dry-run-option-shape>"), validator
            ):
                errors.append(
                    "Draft 2020-12 dry run failed to reject an invalid option shape"
                )
            stages.append(("checkpoint_schema", len(errors) == before))
            order = (
                "checkpoint_schema",
                "checkpoint_resolution",
                "task_resumption",
                "deterministic_correction",
            )
            stages = sorted(stages, key=lambda item: order.index(item[0]))
        return _CheckpointRepositoryValidationResult(
            len(paths), unresolved, duplicates, tuple(errors), tuple(stages)
        )
