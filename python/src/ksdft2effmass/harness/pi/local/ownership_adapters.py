"""Compatibility adapters for selected ownership and agent records."""

from __future__ import annotations

from .. import OwnershipManifestView, OwnershipScope
from ._parsing import as_str, failure, parse_object, success
from .models import AdaptationResult, LocalIssue


def _invalid(area: str, path: str, exc: Exception) -> AdaptationResult:
    return failure(LocalIssue(f"PIHL.{area}.INVALID", path, str(exc)))


class OwnershipManifestAdapter:
    """Normalize live version-2 and retained version-1 ownership manifests.

    Version 1 is a bounded compatibility input, including its local
    ``boundary_owned`` spelling. The ActionObject does not validate launch
    authority or assign work.
    """

    __slots__ = ()

    def execute(self, manifest_bytes: bytes) -> AdaptationResult:
        """Adapt one explicit ownership-manifest representation.

        Parameters
        ----------
        manifest_bytes
            Exact version-1 or version-2 ownership JSON bytes.

        Returns
        -------
        AdaptationResult
            A generic ownership-manifest view on success, or deterministic local
            diagnostics for malformed or unsupported input.
        """
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
                        tuple(
                            sorted(
                                scopes, key=lambda value: (value.path, value.scope_kind)
                            )
                        ),
                    )
                )
            reviewers = tuple(
                sorted(
                    (
                        as_str(value.get("role", value["agent"]), "reviewer role"),
                        as_str(value["agent"], "reviewer agent"),
                    )
                    for value in reviewers_raw
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
