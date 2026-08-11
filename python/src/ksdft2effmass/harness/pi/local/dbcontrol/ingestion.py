"""Repository-specific catalog ingestion for control construction."""

from __future__ import annotations

import json
import sqlite3
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from ...evidence.python_conformance.evidence import _PythonEvidenceFactExtractor
from ...evidence.python_conformance.model import PythonTestModuleModel
from ...evidence.python_conformance.nodes import _PythonTestNodeProjector
from .constants import _EVIDENCE_CLASSES, _IDENTIFIER
from .encoding import _ControlEncoding
from .resources import _ControlResourceCorpus


class _RepositoryControlIngestor:
    """Ingest one explicit repository corpus into an initialized database."""

    __slots__ = (
        "connection",
        "root",
        "unresolved",
        "module_inventory",
        "evidence_profiles",
        "evidence_models",
        "evidence_predecessors",
        "resource_corpus",
    )

    def __init__(
        self,
        connection: sqlite3.Connection,
        root: Path,
        unresolved: list[str],
        module_inventory: tuple[Mapping[str, Any], ...] = (),
        evidence_models: tuple[PythonTestModuleModel, ...] = (),
        evidence_predecessors: tuple[tuple[str, str], ...] = (),
        resource_corpus: _ControlResourceCorpus | None = None,
    ) -> None:
        self.connection = connection
        self.root = root
        self.unresolved = unresolved
        self.module_inventory = module_inventory
        self.evidence_profiles: dict[str, str] = {}
        self.evidence_models = {model.path: model for model in evidence_models}
        self.evidence_predecessors = dict(evidence_predecessors)
        self.resource_corpus = resource_corpus

    def execute(self) -> None:
        """Ingest the complete repository control corpus in dependency order."""
        self._migrate_tasks()
        self._migrate_evidence()
        self._migrate_collected_nodes()
        self._migrate_agents_and_skills()
        self._migrate_resources()
        self._migrate_decisions()

    def _module_inventory(self) -> list[Mapping[str, Any]]:
        """Return the explicit source-derived corpus; projections are never read."""
        return list(self.module_inventory)

    def _canonical_evidence_id(
        self, module: Mapping[str, Any], function_name: str
    ) -> str:
        path = Path(module["path"])
        parts = list(path.parts)
        try:
            start = parts.index("ksdft2effmass")
            domain = [_ControlEncoding.slug(item) for item in parts[start + 1 : -1]]
        except ValueError:
            domain = ["repository"]
        subject = _ControlEncoding.slug(path.stem.removeprefix("test__"))
        claim = ".".join(
            _ControlEncoding.slug(item)
            for item in function_name.removeprefix("test_").split("__")
        )
        prefix = _EVIDENCE_CLASSES[module["evidence_class"]]
        return ".".join((prefix, *(domain or ["root"]), subject, claim))

    def _frontmatter(self, text: str) -> dict[str, str]:
        if not text.startswith("---\n"):
            return {}
        end = text.find("\n---\n", 4)
        if end < 0:
            return {}
        result = {}
        for line in text[4:end].splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                result[key.strip()] = value.strip()
        return result

    def _migrate_tasks(self) -> None:
        connection = self.connection
        root = self.root
        task_paths = sorted(
            (root / "harness/tasks").glob("*.json"), key=lambda item: item.name
        )
        tasks: dict[str, dict[str, Any]] = {}
        for path in task_paths:
            task = json.loads(path.read_text())
            task_id = task["task_id"]
            if type(task_id) is not str or task_id != path.stem:
                raise ValueError(
                    "authoritative Task identity must equal its source filename: "
                    f"{path.name}"
                )
            tasks[task_id] = task
        extraction_id = "harness.extraction"
        legacy_extraction = tasks.pop("H5", None)
        if legacy_extraction is not None:
            legacy_extraction["task_id"] = extraction_id
            legacy_extraction["title"] = (
                "Harness extraction — Standalone extraction readiness"
            )
            legacy_extraction["status_detail"] = (
                "optional; blocked by accepted H4 and separate explicit "
                "harness.extraction activation; inactive"
            )
            for field in ("authorized_scope", "completion_criteria", "exclusions"):
                legacy_extraction[field] = [
                    value.replace("H5", extraction_id)
                    for value in legacy_extraction[field]
                ]
            tasks[extraction_id] = legacy_extraction
        for task in tasks.values():
            if task.get("parent_task_id") == "H5":
                task["parent_task_id"] = extraction_id
            for field in ("task_prerequisite_ids", "superseded_by_task_ids"):
                if field in task:
                    task[field] = [
                        extraction_id if value == "H5" else value
                        for value in task[field]
                    ]
        migration_id = "harness.simplification.round-2.sqlite-hybrid-cutover"
        tasks[migration_id] = {
            "schema_version": 3,
            "task_id": migration_id,
            "title": "Implement the complete SQLite-hybrid harness control cutover",
            "status": "completed",
            "status_detail": "bounded migration completed; no successor activated",
            "parent_task_id": None,
            "task_prerequisite_ids": ["harness.simplification.evidence.naming"],
            "external_prerequisite_ids": [],
            "superseded_by_task_ids": [],
            "explicit_activation_required": False,
            "objective": (
                "Consolidate structured harness control information in one tracked "
                "authoritative SQLite database while retaining executable code and "
                "human-authored content in ordinary files."
            ),
            "authority_reference_paths": ["AGENTS.md"],
            "authorized_scope": [
                "Migrate Tasks, evidence, tests, agents, skills, resources, "
                "decisions, and generated projection identities into the "
                "SQLite-hybrid control model."
            ],
            "completion_criteria": [
                "The deterministic database, SQL recovery representation, "
                "projections, reader cutover, and bounded validation agree."
            ],
            "exclusions": [
                "Runtime observations, telemetry, scientific calculations, protected "
                "execution, release actions, and successor activation remain excluded."
            ],
            "intake_path": None,
            "archived_source": None,
        }
        ids = set(tasks)
        for task_id, task in sorted(tasks.items()):
            archived = task.get("archived_source") or {}
            connection.execute(
                "INSERT INTO task_definition VALUES (?,?,?,?,?,?,?,?,?,?)",
                (
                    task_id,
                    task["schema_version"],
                    task["title"],
                    task["objective"],
                    f"harness/tasks/{task_id}.json",
                    task.get("status_detail"),
                    int(task["explicit_activation_required"]),
                    task.get("intake_path"),
                    archived.get("path"),
                    archived.get("sha256"),
                ),
            )
            status = task["status"]
            connection.execute(
                "INSERT INTO task_state VALUES (?,?,?,?)",
                (task_id, status, int(status == "active"), 0),
            )
            event_kind = (
                "superseded"
                if "superseded" in status
                else "deferred"
                if "deferred" in status or status == "inactive"
                else "completed"
                if status != "active"
                else "activated"
            )
            connection.execute(
                "INSERT INTO task_state_event VALUES (?,?,?,?,?)",
                (
                    f"task-state.{_ControlEncoding.slug(task_id)}.imported",
                    task_id,
                    0,
                    status,
                    event_kind,
                ),
            )
            for kind, field in (
                ("authority_reference", "authority_reference_paths"),
                ("authorized_scope", "authorized_scope"),
                ("completion_criterion", "completion_criteria"),
                ("exclusion", "exclusions"),
            ):
                for index, value in enumerate(task[field]):
                    connection.execute(
                        "INSERT INTO task_text VALUES (?,?,?,?)",
                        (task_id, kind, index, value),
                    )
        if extraction_id in ids:
            connection.execute(
                "INSERT INTO task_alias VALUES (?,?,?)",
                ("H5", extraction_id, "historical"),
            )
        for task_id, task in sorted(tasks.items()):
            if task.get("parent_task_id") in ids:
                connection.execute(
                    "INSERT INTO task_relationship VALUES (?,?,?)",
                    (task_id, task["parent_task_id"], "child_of"),
                )
            for dependency in task["task_prerequisite_ids"]:
                if dependency in ids:
                    connection.execute(
                        "INSERT INTO task_relationship VALUES (?,?,?)",
                        (task_id, dependency, "depends_on"),
                    )
            for index, dependency in enumerate(task["external_prerequisite_ids"]):
                connection.execute(
                    "INSERT INTO task_external_prerequisite VALUES (?,?,?)",
                    (task_id, dependency, index),
                )
            for replacement in task.get("superseded_by_task_ids", []):
                if replacement in ids:
                    connection.execute(
                        "INSERT INTO task_relationship VALUES (?,?,?)",
                        (task_id, replacement, "superseded_by"),
                    )

    def _migrate_evidence(self) -> None:
        connection = self.connection
        root = self.root
        unresolved = self.unresolved
        for module in self._module_inventory():
            path = root / module["path"]
            model = self.evidence_models.get(str(module["path"]))
            if model is None:
                unresolved.append(f"unresolved test module: {module['path']}")
                continue
            self.evidence_profiles[str(module["path"])] = model.evidence_profile
            module_id = "test-module." + _ControlEncoding.slug(
                path.relative_to(root / "python/tests").with_suffix("").as_posix()
            ).replace("-", ".")
            subject = (
                module.get("sut")
                or module.get("artifact")
                or path.stem.removeprefix("test__")
            )
            connection.execute(
                "INSERT INTO test_module VALUES (?,?,?,?,?,?,?)",
                (
                    module_id,
                    module["path"],
                    model.source_sha256,
                    module["mode"],
                    subject,
                    _EVIDENCE_CLASSES[module["evidence_class"]],
                    module["evidence_profile"],
                ),
            )
            for function_name, extracted_id in _PythonEvidenceFactExtractor().execute(
                model
            ):
                owner_node = f"{module['path']}::{function_name}"
                old_id = extracted_id or None
                canonical = (
                    old_id
                    if old_id is not None
                    and _IDENTIFIER.fullmatch(old_id)
                    and old_id.split(".", 1)[0] in _EVIDENCE_CLASSES.values()
                    else self._canonical_evidence_id(module, function_name)
                )
                naming = "semantic"
                claim_summary = (
                    function_name.removeprefix("test_")
                    .replace("__", ": ")
                    .replace("_", " ")
                )
                try:
                    connection.execute(
                        "INSERT INTO evidence_claim VALUES (?,?,?,?)",
                        (
                            canonical,
                            _EVIDENCE_CLASSES[module["evidence_class"]],
                            claim_summary,
                            naming,
                        ),
                    )
                    connection.execute(
                        "INSERT INTO evidence_owner VALUES (?,?,?,?)",
                        (
                            canonical,
                            module_id,
                            owner_node,
                            "test_function"
                            if module["mode"] == "class_owned"
                            else "artifact_test",
                        ),
                    )
                    predecessor = self.evidence_predecessors.get(owner_node)
                    if predecessor is not None:
                        connection.execute(
                            "INSERT INTO evidence_predecessor VALUES (?,?)",
                            (canonical, predecessor),
                        )
                except sqlite3.IntegrityError as exc:
                    unresolved.append(
                        f"duplicate evidence identity or owner: {canonical} ({exc})"
                    )
                    continue
                if old_id is not None and old_id != canonical:
                    try:
                        connection.execute(
                            "INSERT INTO evidence_alias VALUES (?,?,?)",
                            (old_id, canonical, "historical"),
                        )
                    except sqlite3.IntegrityError:
                        unresolved.append(f"duplicate historical alias: {old_id}")

    def _migrate_collected_nodes(self) -> None:
        """Project canonical node identities from the parsed evidence corpus."""
        connection = self.connection
        unresolved = self.unresolved
        modules = {
            path: module_id
            for module_id, path in connection.execute(
                "SELECT module_id,source_path FROM test_module"
            )
        }
        owners = {
            (module_id, node_id.rsplit("::", 1)[-1]): evidence_id
            for evidence_id, module_id, node_id in connection.execute(
                "SELECT evidence_id,module_id,owner_node_id FROM evidence_owner"
            )
        }
        models = tuple(
            self.evidence_models[path] for path in sorted(self.evidence_models)
        )
        for fact in _PythonTestNodeProjector().execute(models):
            module_id = modules.get(fact.module_path)
            if module_id is None:
                unresolved.append(
                    f"unresolved collected test module: {fact.module_path}"
                )
                continue
            evidence_id = owners.get((module_id, fact.function_name))
            if evidence_id is None:
                unresolved.append(
                    f"missing evidence owner for collected node: {fact.node_id}"
                )
                continue
            connection.execute(
                "INSERT INTO test_node VALUES (?,?,?,?)",
                (fact.node_id, module_id, evidence_id, fact.parameter_id),
            )

    def _migrate_agents_and_skills(self) -> None:
        connection = self.connection
        root = self.root
        skill_paths = sorted(
            (
                *root.glob(".pi/skills/*/SKILL.md"),
                *root.glob(".agents/skills/*/SKILL.md"),
            ),
            key=lambda item: item.as_posix(),
        )
        skill_ids: set[str] = set()
        for path in skill_paths:
            relative = path.relative_to(root).as_posix()
            meta = self._frontmatter(path.read_text())
            skill_id = _ControlEncoding.slug(
                meta.get("name", path.parent.name)
            ).replace("-", ".")
            if skill_id in skill_ids:
                skill_id = "project." + skill_id
            skill_ids.add(skill_id)
            canonical = root / "harness/pi/skills" / path.parent.name / "SKILL.md"
            descriptor = (
                root / "harness/pi/skills" / path.parent.name / "descriptor.json"
            )
            connection.execute(
                "INSERT INTO skill_definition VALUES (?,?,?,?,?,?)",
                (
                    skill_id,
                    canonical.relative_to(root).as_posix()
                    if canonical.exists()
                    else relative,
                    relative,
                    descriptor.relative_to(root).as_posix()
                    if descriptor.exists()
                    else None,
                    _ControlEncoding.sha256(path.read_bytes()),
                    1,
                ),
            )
        by_name = {
            row[0].replace(".", "-"): row[0]
            for row in connection.execute("SELECT skill_id FROM skill_definition")
        }
        for path in sorted(root.glob(".pi/agents/*.md"), key=lambda item: item.name):
            meta = self._frontmatter(path.read_text())
            agent_id = _ControlEncoding.slug(meta.get("name", path.stem)).replace(
                "-", "."
            )
            access = "writer" if meta.get("acceptanceRole") == "writer" else "read_only"
            connection.execute(
                "INSERT INTO agent_definition VALUES (?,?,?,?,?,?)",
                (
                    agent_id,
                    path.relative_to(root).as_posix(),
                    _ControlEncoding.sha256(path.read_bytes()),
                    "durable",
                    access,
                    1,
                ),
            )
            for name in (
                item.strip()
                for item in meta.get("skills", "").split(",")
                if item.strip()
            ):
                routed_skill_id = by_name.get(name)
                if routed_skill_id is not None:
                    connection.execute(
                        "INSERT OR IGNORE INTO agent_skill_route VALUES (?,?)",
                        (agent_id, routed_skill_id),
                    )

    def _migrate_resources(self) -> None:
        corpus = self.resource_corpus
        if corpus is None:
            return
        connection = self.connection
        ids = {item.reference.resource_id for item in corpus.resources}
        for item in corpus.resources:
            resource = item.reference
            connection.execute(
                "INSERT INTO resource_definition VALUES (?,?,?,?,?,?,?)",
                (
                    resource.resource_id,
                    item.layer,
                    resource.resource_kind,
                    item.source_path,
                    resource.content_identity.digest,
                    resource.format_version,
                    resource.schema_version,
                ),
            )
        for item in corpus.resources:
            resource = item.reference
            for dependency in resource.dependency_ids:
                if dependency in ids:
                    connection.execute(
                        "INSERT INTO resource_dependency VALUES (?,?)",
                        (resource.resource_id, dependency),
                    )
            if resource.resource_kind == "profile":
                for index, dependency in enumerate(resource.dependency_ids):
                    if dependency in ids:
                        connection.execute(
                            "INSERT OR IGNORE INTO resource_profile_membership "
                            "VALUES (?,?,?)",
                            (resource.resource_id, dependency, index),
                        )

    def _migrate_decisions(self) -> None:
        connection = self.connection
        root = self.root
        for path in sorted(
            (root / ".pi/checkpoints").glob("*.json"), key=lambda item: item.name
        ):
            if path.name.endswith("schema.json"):
                continue
            document = json.loads(path.read_text())
            decision_id = document.get("checkpoint_id") or path.stem
            status = str(document.get("status", "unresolved"))
            resolved = (
                status in {"resolved", "accepted", "cancelled", "superseded"}
                or document.get("resolved_at") is not None
            )
            disposition = document.get("normalized_decision")
            if disposition is not None and type(disposition) is not str:
                disposition = json.dumps(
                    disposition,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                )
            task_id = document.get("task_id")
            if (
                task_id is not None
                and connection.execute(
                    "SELECT 1 FROM task_definition WHERE task_id=?", (task_id,)
                ).fetchone()
                is None
            ):
                task_id = None
            connection.execute(
                "INSERT INTO decision_reference VALUES (?,?,?,?,?,?)",
                (
                    decision_id,
                    path.relative_to(root).as_posix(),
                    _ControlEncoding.sha256(path.read_bytes()),
                    task_id,
                    disposition,
                    "resolved" if resolved else "unresolved",
                ),
            )
