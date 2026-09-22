"""Explicit-root resource path observation and resolution."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import TYPE_CHECKING

from ..identity import (
    ArtifactIdentity,
    HarnessInternalError,
    Identifier,
    _require_identifier,
)
from ..validation import ResourceResolutionResult, ValidationIssue, _issue, _result
from .manifests import ResourceManifestValidator, _manifest_maps
from .records import ResourceManifest, ResourceReference

if TYPE_CHECKING:
    from ..profiles import ProjectProfile


def _confined_file(root: Path, path: str) -> tuple[Path | None, ValidationIssue | None]:
    if (
        not isinstance(root, Path)
        or not root.is_absolute()
        or not root.exists()
        or not root.is_dir()
    ):
        return None, _issue(
            "PIH.PATH.ROOT_INVALID",
            "Explicit root must be an existing absolute directory.",
            path=path,
        )
    resolved_root = root.resolve()
    current = root
    for segment in path.split("/"):
        try:
            names = os.listdir(current)
        except OSError:
            return None, _issue(
                "PIH.PATH.MISSING", "Resource component is missing.", path=path
            )
        if segment not in names:
            if any(n.casefold() == segment.casefold() for n in names):
                return None, _issue(
                    "PIH.PATH.CASE_MISMATCH",
                    "Resource component case differs.",
                    path=path,
                )
            return None, _issue("PIH.PATH.MISSING", "Resource is missing.", path=path)
        current = current / segment
        if current.is_symlink():
            return None, _issue(
                "PIH.PATH.SYMLINK", "Symlink components are prohibited.", path=path
            )
    try:
        resolved = current.resolve()
        resolved.relative_to(resolved_root)
    except OSError, ValueError:
        return None, _issue(
            "PIH.PATH.ESCAPE", "Resolved path escapes its root.", path=path
        )
    if not current.is_file():
        return None, _issue(
            "PIH.PATH.NOT_FILE", "Resource is not a regular file.", path=path
        )
    return current, None


class ResourceResolver:
    """Resolve and hash one resource beneath explicit roots."""

    __slots__ = ()

    def execute(
        self,
        resource_id: Identifier,
        generic_root: Path,
        generic_manifest: ResourceManifest,
        generic_manifest_identity: ArtifactIdentity,
        local_root: Path | None,
        local_manifest: ResourceManifest | None,
        local_manifest_identity: ArtifactIdentity | None,
        profile: ProjectProfile,
    ) -> ResourceResolutionResult:
        _require_identifier(resource_id, "resource_id")
        if not isinstance(generic_root, Path) or (
            local_root is not None and not isinstance(local_root, Path)
        ):
            raise TypeError("roots must be pathlib.Path")
        validation = ResourceManifestValidator().execute(
            generic_manifest,
            generic_manifest_identity,
            local_manifest,
            local_manifest_identity,
            profile,
        )
        if validation.status == "FAIL":
            return ResourceResolutionResult(None, None, validation)
        expects_local = profile.local_manifest_id is not None
        root_presence_matches = (expects_local and local_root is not None) or (
            not expects_local and local_root is None
        )
        if not root_presence_matches:
            validation = _result(
                validation.issues
                + (
                    _issue(
                        "PIH.RESOURCE.MANIFEST_MISMATCH",
                        "Local root presence does not match profile.",
                    ),
                )
            )
        if validation.status == "FAIL":
            return ResourceResolutionResult(None, None, validation)
        gm, lm = _manifest_maps(generic_manifest, local_manifest)
        matches: list[tuple[Path | None, ResourceReference]] = (
            [(generic_root, gm[resource_id])] if resource_id in gm else []
        )
        if resource_id in lm:
            matches.append((local_root, lm[resource_id]))
        if not matches:
            return ResourceResolutionResult(
                None,
                None,
                _result(
                    (
                        _issue(
                            "PIH.RESOURCE.NOT_FOUND",
                            "Resource ID was not found.",
                            resource_id,
                        ),
                    )
                ),
            )
        if len(matches) != 1:
            return ResourceResolutionResult(
                None,
                None,
                _result(
                    (
                        _issue(
                            "PIH.RESOURCE.AMBIGUOUS_SELECTION",
                            "Resource ID is ambiguous.",
                            resource_id,
                        ),
                    )
                ),
            )
        root, ref = matches[0]
        if root is None:
            return ResourceResolutionResult(
                None,
                None,
                _result(
                    (
                        _issue(
                            "PIH.PATH.ROOT_INVALID",
                            "Selected layer has no root.",
                            resource_id,
                            ref.path,
                        ),
                    )
                ),
            )
        path, problem = _confined_file(root, ref.path)
        if problem is not None:
            return ResourceResolutionResult(None, None, _result((problem,)))
        if path is None:
            raise AssertionError("successful confinement must return a path")
        try:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError as exc:
            raise HarnessInternalError("ResourceResolver", str(exc)) from exc
        if digest != ref.content_identity.digest:
            return ResourceResolutionResult(
                None,
                None,
                _result(
                    (
                        _issue(
                            "PIH.ARTIFACT.HASH_MISMATCH",
                            "Resource bytes differ from identity.",
                            resource_id,
                            ref.path,
                        ),
                    )
                ),
            )
        return ResourceResolutionResult(path, ref, _result())
