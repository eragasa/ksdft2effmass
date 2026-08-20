"""Complete explicit-input operation for local Harness resource composition."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ksdft2effmass.harness.pi import ResourceResolver, ValidationIssue

from .context import LocalHarnessContextLoader
from .models import LocalHarnessContext, LocalIssue, RepositoryRoots


@dataclass(frozen=True, slots=True)
class _LocalHarnessResourceValidationRequest:
    """Exact roots and selected resource records for one validation operation."""

    repository_root: Path
    generic_resource_root: Path
    local_resource_root: Path
    profile_path: Path
    generic_manifest_path: Path
    local_manifest_path: Path


@dataclass(frozen=True, slots=True)
class _LocalHarnessResourceIssue:
    """Immutable normalized issue for command-independent resource validation."""

    code: str
    detail: str
    path: str | None


@dataclass(frozen=True, slots=True)
class _LocalHarnessResourceResult:
    """One immutable nested resource-validation outcome."""

    resource_id: str
    status: str
    issues: tuple[_LocalHarnessResourceIssue, ...]


@dataclass(frozen=True, slots=True)
class _LocalHarnessResourceValidationResult:
    """Immutable aggregate resource-composition outcome."""

    status: str
    stage: str
    issues: tuple[_LocalHarnessResourceIssue, ...]
    resources: tuple[_LocalHarnessResourceResult, ...]


def _issue(issue: LocalIssue | ValidationIssue) -> _LocalHarnessResourceIssue:
    detail = issue.detail if isinstance(issue, LocalIssue) else issue.message
    return _LocalHarnessResourceIssue(
        issue.code,
        detail,
        str(issue.path) if issue.path is not None else None,
    )


def _read_file(path: Path, root: Path, label: str) -> bytes:
    if not path.is_absolute():
        raise ValueError(f"{label} path must be absolute")
    if ".." in path.parts:
        raise ValueError(f"{label} path must not contain parent traversal")
    try:
        resolved_root = root.resolve(strict=True)
        resolved_path = path.resolve(strict=True)
        resolved_path.relative_to(resolved_root)
    except (OSError, ValueError) as exc:
        raise ValueError(
            f"{label} path must resolve below its explicit resource root"
        ) from exc
    if resolved_path != path or not path.is_file() or path.is_symlink():
        raise ValueError(f"{label} path must select a nonsymlink regular file")
    return path.read_bytes()


class _LocalHarnessResourceCompositionValidator:
    """Validate one explicit current generic/local Harness resource composition."""

    __slots__ = ()

    def execute(
        self, request: _LocalHarnessResourceValidationRequest
    ) -> _LocalHarnessResourceValidationResult:
        """Return aggregate validation without command rendering or exit policy."""
        for value, label in (
            (request.repository_root, "repository root"),
            (request.generic_resource_root, "generic resource root"),
            (request.local_resource_root, "local resource root"),
        ):
            if not value.is_absolute():
                raise ValueError(f"{label} must be an absolute path")
            if ".." in value.parts or value.resolve(strict=True) != value:
                raise ValueError(f"{label} must be a resolved nonsymlink path")
        roots = RepositoryRoots(
            request.repository_root,
            request.generic_resource_root,
            request.local_resource_root,
        )
        profile_bytes = _read_file(
            request.profile_path, roots.local_resource_root, "profile"
        )
        generic_bytes = _read_file(
            request.generic_manifest_path,
            roots.generic_resource_root,
            "generic manifest",
        )
        local_bytes = _read_file(
            request.local_manifest_path,
            roots.local_resource_root,
            "local manifest",
        )
        adapted = LocalHarnessContextLoader().execute(
            roots, profile_bytes, generic_bytes, local_bytes
        )
        if type(adapted.value) is not LocalHarnessContext:
            return _LocalHarnessResourceValidationResult(
                "FAIL",
                "context",
                tuple(_issue(issue) for issue in adapted.validation.issues),
                (),
            )
        context = adapted.value
        resource_ids = tuple(
            sorted(
                resource.resource_id
                for manifest in (context.generic_manifest, context.local_manifest)
                for resource in manifest.resources
            )
        )
        resources = []
        for resource_id in resource_ids:
            result = ResourceResolver().execute(
                resource_id,
                roots.generic_resource_root,
                context.generic_manifest,
                context.generic_manifest_identity,
                roots.local_resource_root,
                context.local_manifest,
                context.local_manifest_identity,
                context.profile,
            )
            resources.append(
                _LocalHarnessResourceResult(
                    resource_id,
                    result.validation.status,
                    tuple(_issue(issue) for issue in result.validation.issues),
                )
            )
        failed = any(resource.status == "FAIL" for resource in resources)
        return _LocalHarnessResourceValidationResult(
            "FAIL" if failed else "PASS",
            "resources",
            (),
            tuple(resources),
        )
