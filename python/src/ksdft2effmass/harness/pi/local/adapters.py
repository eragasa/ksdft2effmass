"""Strict compatibility adapters for selected live project records."""

from __future__ import annotations

import re

from .. import (
    AgentDescriptorView,
    ArtifactIdentity,
    ChainView,
    CheckpointRecord,
    ChecksumEntry,
    ChecksumManifest,
    DeserializeJsonRecord,
    OwnershipManifestView,
    OwnershipScope,
    ResourcePath,
    SkillDescriptor,
    TaskReference,
    WireRecordKind,
)
from ._parsing import (
    as_bool,
    as_str,
    failure,
    parse_object,
    require_fields,
    strings,
    success,
)
from .models import AdaptationResult, EvidenceOwnershipRelation, LocalIssue


def _invalid(area: str, path: str, exc: Exception) -> AdaptationResult:
    return failure(LocalIssue(f"PIHL.{area}.INVALID", path, str(exc)))


def _options(value: object) -> tuple[tuple[str, str, str | None], ...]:
    if type(value) is not list:
        raise TypeError("options must be an array")
    result = []
    for item in value:
        if type(item) is not dict:
            raise TypeError("option must be an object")
        result.append(
            (
                as_str(item.get("id"), "option id"),
                str(item.get("summary", "")),
                item.get("consequence"),
            )
        )
    return tuple(result)


class AdaptCheckpointRecords:
    """Normalize caller-selected live checkpoint JSON documents."""

    __slots__ = ()

    def execute(
        self, checkpoint_documents: tuple[tuple[ResourcePath, bytes], ...]
    ) -> AdaptationResult:
        """Adapt path/byte pairs into checkpoint records sorted by identity."""
        if type(checkpoint_documents) is not tuple:
            raise TypeError("checkpoint_documents must be a tuple")
        records = []
        for path, payload in checkpoint_documents:
            obj, issue = parse_object(payload, path)
            if issue is not None:
                return failure(issue)
            assert obj is not None
            required = {"checkpoint_id", "status", "options", "record_paths"}
            if (issue := require_fields(obj, required, path)) is not None:
                return failure(issue)
            try:
                records.append(
                    CheckpointRecord(
                        1,
                        as_str(obj["checkpoint_id"], "checkpoint_id"),
                        obj.get("task_id"),
                        obj.get("episode_id"),
                        as_str(obj["status"], "status"),
                        obj.get("decision_class"),
                        obj.get("created_at"),
                        obj.get("question"),
                        _options(obj["options"]),
                        obj.get("human_response"),
                        obj.get("normalized_decision"),
                        obj.get("resolved_at"),
                        obj.get("authorized_scope"),
                        tuple(
                            sorted(
                                path.rstrip("/")
                                for path in strings(obj["record_paths"], "record_paths")
                            )
                        ),
                        (
                            None
                            if obj.get("resumption_status") is None
                            else "resumed"
                            if obj.get("status")
                            in {"resolved", "cancelled", "superseded"}
                            else "blocked"
                        ),
                    )
                )
            except (TypeError, ValueError) as exc:
                return _invalid("CHECKPOINT", path, exc)
        return success(tuple(sorted(records, key=lambda x: x.checkpoint_id)))


class AdaptTaskRecords:
    """Bind selected task Markdown bytes to authoritative chain task entries."""

    __slots__ = ()

    def execute(
        self,
        task_documents: tuple[tuple[ResourcePath, bytes], ...],
        chain_bytes: bytes,
        activation_bytes: bytes,
    ) -> AdaptationResult:
        """Return normalized task references; all paths must have supplied bytes."""
        if type(task_documents) is not tuple:
            raise TypeError("task_documents must be a tuple")
        chain, issue = parse_object(chain_bytes, "chain")
        if issue is not None:
            return failure(issue)
        activation, issue = parse_object(activation_bytes, "activation")
        if issue is not None:
            return failure(issue)
        assert chain is not None and activation is not None
        supplied = {}
        for path, payload in task_documents:
            if type(path) is not str or type(payload) is not bytes:
                raise TypeError("task document entries must be (str, bytes)")
            try:
                text = payload.decode("utf-8")
            except UnicodeDecodeError as exc:
                return _invalid("TASK", path, exc)
            if not text.startswith("# ") or "Status:" not in text:
                return failure(
                    LocalIssue(
                        "PIHL.TASK.INVALID", path, "missing title or Status field"
                    )
                )
            supplied[path] = payload
        try:
            entries = chain["task_sequence"]
            if type(entries) is not list:
                raise TypeError("task_sequence must be an array")
            activated = activation.get(
                "activated_task", activation.get("task", activation.get("task_id"))
            )
            result = []
            ids = {as_str(x.get("id"), "task id") for x in entries if type(x) is dict}
            for item in entries:
                if type(item) is not dict:
                    raise TypeError("task entry must be an object")
                task_id = as_str(item["id"], "task id")
                record = as_str(item["record"], "task record")
                if record not in supplied:
                    raise ValueError(f"missing selected task bytes for {record}")
                task_deps: list[str] = []
                external: list[str] = []
                for dep in item.get("prerequisites", []):
                    name = as_str(dep, "prerequisite").split(":", 1)[0]
                    (task_deps if name in ids else external).append(
                        dep if name not in ids else name
                    )
                result.append(
                    TaskReference(
                        1,
                        task_id,
                        record,
                        tuple(sorted(task_deps)),
                        tuple(sorted(external)),
                        as_str(item["status"], "status"),
                        task_id in {"H1", "H2", "H3", "H4", "H5"},
                    )
                )
            if activated not in {None, *(x.task_id for x in result)}:
                raise ValueError("activation selects an unknown task")
        except (KeyError, TypeError, ValueError) as exc:
            return _invalid("TASK", "chain", exc)
        return success(tuple(sorted(result, key=lambda x: x.task_id)))


class AdaptChainRecord:
    """Normalize the live chain using already adapted task records."""

    __slots__ = ()

    def execute(
        self,
        chain_bytes: bytes,
        task_records: tuple[TaskReference, ...],
        activation_bytes: bytes,
    ) -> AdaptationResult:
        """Build a generic chain view without reading repository state."""
        chain, issue = parse_object(chain_bytes, "chain")
        if issue is not None:
            return failure(issue)
        activation, issue = parse_object(activation_bytes, "activation")
        if issue is not None:
            return failure(issue)
        assert chain is not None and activation is not None
        try:
            active = chain.get("active_task")
            activated = activation.get(
                "activated_task", activation.get("task", activation.get("task_id"))
            )
            view = ChainView(
                1,
                as_str(chain.get("name"), "chain name"),
                active,
                task_records,
                () if activated is None else (as_str(activated, "activated task"),),
                as_bool(
                    chain["production_execution_authorized"], "production authorization"
                ),
                as_bool(
                    chain["package_publication_authorized"], "publication authorization"
                ),
            )
        except (KeyError, TypeError, ValueError) as exc:
            return _invalid("CHAIN", "chain", exc)
        return success(view)


class AdaptAgentRecords:
    """Extract immutable identities from selected agent front matter."""

    __slots__ = ()

    def execute(
        self, agent_documents: tuple[tuple[ResourcePath, bytes], ...]
    ) -> AdaptationResult:
        """Adapt agent Markdown front matter into sorted generic views."""
        records = []
        for path, payload in agent_documents:
            try:
                text = payload.decode("utf-8")
                name = re.search(r"(?m)^name:\s*(\S+)\s*$", text)
                role = re.search(r"(?m)^acceptanceRole:\s*(\S+)\s*$", text)
                if name is None or role is None:
                    raise ValueError("missing name or acceptanceRole")
                records.append(AgentDescriptorView(1, name.group(1), role.group(1)))
            except (UnicodeDecodeError, TypeError, ValueError) as exc:
                return _invalid("AGENT", path, exc)
        return success(tuple(sorted(records, key=lambda x: x.agent_id)))


class AdaptOwnershipManifest:
    """Normalize live version-2 and retained version-1 ownership manifests."""

    __slots__ = ()

    def execute(self, manifest_bytes: bytes) -> AdaptationResult:
        """Adapt ownership JSON; version 1 `boundary_owned` remains local-only input."""
        obj, issue = parse_object(manifest_bytes, "ownership")
        if issue is not None:
            return failure(issue)
        assert obj is not None
        try:
            version = obj.get("schema_version")
            owners = obj.get("owners", obj)
            if version == 1 and "writers" not in owners:
                writer_items = tuple(
                    (role, value)
                    for role, value in owners.items()
                    if role != "reviewers" and type(value) is dict
                )
                writers_raw = tuple(
                    {
                        "role": role,
                        "agent": value["agent"],
                        "owned_paths": value.get("owned_paths", ()),
                    }
                    for role, value in writer_items
                )
            else:
                writers_raw = owners["writers"]
            reviewers_raw = owners["reviewers"]
            writers: list[tuple[str, str, tuple[OwnershipScope, ...]]] = []
            for writer in writers_raw:
                scopes: list[OwnershipScope] = []
                for raw in writer.get("owned_scopes", writer.get("owned_paths", [])):
                    if type(raw) is str:
                        path, kind = raw.rstrip("/"), "directory_tree"
                    elif type(raw) is dict:
                        path = as_str(raw.get("path"), "scope path").rstrip("/")
                        kind = raw.get("scope_kind", "directory_tree")
                        if kind == "boundary_owned":
                            kind = "file"
                    else:
                        raise TypeError("invalid ownership scope")
                    scopes.append(OwnershipScope(1, path, kind))
                writers.append(
                    (
                        as_str(writer["role"], "writer role"),
                        as_str(writer["agent"], "writer agent"),
                        tuple(sorted(scopes, key=lambda x: (x.path, x.scope_kind))),
                    )
                )
            reviewers = tuple(
                sorted(
                    (
                        as_str(x.get("role", x["agent"]), "reviewer role"),
                        as_str(x["agent"], "reviewer agent"),
                    )
                    for x in reviewers_raw
                )
            )
            completion = obj.get("completion_validator", {})
            if version == 1 and not completion:
                completion = obj.get("test_ownership", {}).get(
                    "completion_validator", {}
                )
            task_record = obj.get("task_record", obj.get("task_record_path"))
            completion_path = as_str(
                completion.get("path", obj.get("completion_validator_path")),
                "completion path",
            ).rstrip("/")
            if version == 1:
                normalized_writers: list[
                    tuple[str, str, tuple[OwnershipScope, ...]]
                ] = []
                for role, agent, owned_scopes in writers:
                    normalized_scopes = owned_scopes
                    if role == "tests":
                        normalized_scopes = tuple(
                            sorted(
                                (
                                    *owned_scopes,
                                    OwnershipScope(1, completion_path, "file"),
                                ),
                                key=lambda scope: (scope.path, scope.scope_kind),
                            )
                        )
                    normalized_writers.append((role, agent, normalized_scopes))
                writers = normalized_writers
            raw_command = completion.get("command", obj.get("completion_command", []))
            command = (
                tuple(raw_command.split())
                if type(raw_command) is str
                else tuple(raw_command)
            )
            view = OwnershipManifestView(
                1,
                as_str(obj["task_id"], "task_id"),
                as_str(task_record, "task record"),
                tuple(sorted(writers)),
                reviewers,
                completion_path,
                command,
                obj.get("orchestration_profile_id"),
            )
            if version not in {1, 2}:
                raise ValueError("unsupported ownership schema version")
        except (KeyError, TypeError, ValueError) as exc:
            return _invalid("OWNERSHIP", "ownership", exc)
        return success(view)


class AdaptChecksumCatalog:
    """Normalize retained sha256sum-style catalog bytes."""

    __slots__ = ()

    def execute(self, catalog_bytes: bytes) -> AdaptationResult:
        """Return a generic checksum manifest from exact catalog bytes."""
        if type(catalog_bytes) is not bytes:
            raise TypeError("catalog_bytes must be bytes")
        try:
            entries = []
            for line in catalog_bytes.decode("utf-8").splitlines():
                if not line:
                    continue
                digest, marker, path = line.partition("  ")
                if not marker:
                    raise ValueError("catalog line must use two-space separator")
                entries.append(
                    ChecksumEntry(1, path, ArtifactIdentity(1, "sha256", digest))
                )
            return success(
                ChecksumManifest(1, tuple(sorted(entries, key=lambda x: x.path)))
            )
        except (UnicodeDecodeError, TypeError, ValueError) as exc:
            return _invalid("CHECKSUM", "catalog", exc)


class AdaptSkillInventory:
    """Select canonical skills and decode their generic descriptor bytes."""

    __slots__ = ()

    def execute(
        self,
        inventory_bytes: bytes,
        descriptor_bytes: tuple[tuple[ResourcePath, bytes], ...],
    ) -> AdaptationResult:
        """Return descriptors whose IDs match the explicit live inventory."""
        inventory, issue = parse_object(inventory_bytes, "skill inventory")
        if issue is not None:
            return failure(issue)
        assert inventory is not None
        try:
            skills = inventory["skills"]
            names = {as_str(item["skill_name"], "skill_name") for item in skills}
            descriptors = []
            for path, payload in descriptor_bytes:
                decoded = DeserializeJsonRecord().execute(
                    WireRecordKind.SkillDescriptor, payload
                )
                if type(decoded.record) is not SkillDescriptor:
                    raise ValueError(f"invalid descriptor {path}")
                if decoded.record.skill_id not in names:
                    raise ValueError(f"descriptor {path} is absent from inventory")
                descriptors.append(decoded.record)
            descriptor_ids = [x.skill_id for x in descriptors]
            if not descriptor_ids or len(descriptor_ids) != len(set(descriptor_ids)):
                raise ValueError("descriptor selection must be nonempty and unique")
        except (KeyError, TypeError, ValueError) as exc:
            return _invalid("SKILL", "skill inventory", exc)
        return success(tuple(sorted(descriptors, key=lambda x: x.skill_id)))


class AdaptEvidenceOwnershipManifest:
    """Normalize the retained P1 evidence-ownership manifest.

    The action consumes only caller-supplied bytes. It maps the historical
    ``boundary_owned`` spelling to accepted ``artifact_owned`` evidence plus
    explicit agreement metadata; it does not add a generic ownership kind.
    """

    __slots__ = ()

    def execute(self, manifest_bytes: bytes) -> AdaptationResult:
        """Adapt retained class, artifact, and boundary evidence ownership.

        Parameters
        ----------
        manifest_bytes
            Exact bytes of the retained P1 ``test-ownership-manifest.json``.

        Returns
        -------
        AdaptationResult
            A module-path-sorted tuple of `EvidenceOwnershipRelation` records,
            or deterministic local diagnostics when the input is invalid.
        """
        manifest, issue = parse_object(manifest_bytes, "evidence ownership")
        if issue is not None:
            return failure(issue)
        assert manifest is not None
        try:
            if manifest.get("manifest_version") != 3:
                raise ValueError("unsupported evidence ownership manifest version")
            relations: list[EvidenceOwnershipRelation] = []
            modules = manifest.get("modules")
            artifacts = manifest.get("artifact_modules")
            if type(modules) is not list or type(artifacts) is not list:
                raise TypeError("modules and artifact_modules must be arrays")
            for item in modules:
                if type(item) is not dict:
                    raise TypeError("class-owned module must be an object")
                relations.append(
                    EvidenceOwnershipRelation(
                        as_str(item.get("module"), "module"),
                        _evidence_ids(item.get("evidence")),
                        "class_owned",
                        as_str(item.get("public_class"), "public_class"),
                    )
                )
            for item in artifacts:
                if type(item) is not dict:
                    raise TypeError("artifact-owned module must be an object")
                ownership_type = item.get("ownership_type")
                common = (
                    as_str(item.get("module"), "module"),
                    _evidence_ids(item.get("evidence")),
                    "artifact_owned",
                )
                if ownership_type == "boundary_owned":
                    relations.append(
                        EvidenceOwnershipRelation(
                            *common,
                            as_str(item.get("boundary_owner"), "boundary_owner"),
                            "agreement",
                            "workflow-cpn-v1-python-runtime",
                            "workflow-cpn-v1-json-schema-wire-contract",
                            "none",
                        )
                    )
                elif ownership_type == "artifact_owned_integration":
                    relations.append(
                        EvidenceOwnershipRelation(
                            *common,
                            as_str(item.get("artifact_owner"), "artifact_owner"),
                        )
                    )
                else:
                    raise ValueError("unsupported retained evidence ownership type")
            ordered = tuple(sorted(relations, key=lambda value: value.module_path))
            paths = tuple(value.module_path for value in ordered)
            if len(paths) != len(set(paths)):
                raise ValueError("evidence module paths must be unique")
        except (TypeError, ValueError) as exc:
            return _invalid("EVIDENCE_OWNERSHIP", "evidence ownership", exc)
        return success(ordered)


def _evidence_ids(value: object) -> tuple[str, ...]:
    """Return sorted retained evidence IDs from one module entry."""
    if type(value) is not list or not value:
        raise TypeError("evidence must be a nonempty array")
    identifiers = []
    for item in value:
        if type(item) is not dict:
            raise TypeError("evidence entry must be an object")
        identifiers.append(as_str(item.get("evidence_id"), "evidence_id"))
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("module evidence IDs must be unique")
    return tuple(sorted(identifiers))


class SelectEvidenceModules:
    """Confine caller-selected evidence module bytes to profile scopes."""

    __slots__ = ()

    def execute(
        self, module_payloads: tuple[tuple[ResourcePath, bytes], ...], profile: object
    ) -> AdaptationResult:
        """Return sorted explicit modules accepted by a generic project profile."""
        from .. import ProjectProfile

        if type(profile) is not ProjectProfile or type(module_payloads) is not tuple:
            raise TypeError("invalid evidence selection arguments")
        selected = []
        for path, payload in module_payloads:
            if type(path) is not str or type(payload) is not bytes:
                raise TypeError("module entries must be (str, bytes)")
            if not any(
                scope.contains(path)
                for scope, _marker, _prefixes in profile.evidence_scope_rules
            ):
                return failure(
                    LocalIssue(
                        "PIHL.EVIDENCE.OUTSIDE_SCOPE",
                        path,
                        "module is outside declared evidence scopes",
                    )
                )
            selected.append((path, payload))
        return success(tuple(sorted(selected)))
