"""Explicit project-local harness context composition."""

from __future__ import annotations

import hashlib
from pathlib import Path

from .. import (
    ArtifactIdentity,
    JsonRecordDeserializer,
    ProjectProfileLoader,
    ResourceManifest,
    ResourceManifestValidator,
    WireRecordKind,
)
from ._parsing import failure, success
from .models import AdaptationResult, LocalHarnessContext, LocalIssue, RepositoryRoots


class LocalHarnessContextLoader:
    """Load and validate explicit profile and manifest bytes.

    Notes
    -----
    This action performs no current-directory, environment, or Git discovery.
    The caller owns all roots and represented bytes.
    """

    __slots__ = ()

    def execute(
        self,
        roots: RepositoryRoots,
        profile_bytes: bytes,
        generic_manifest_bytes: bytes,
        local_manifest_bytes: bytes,
    ) -> AdaptationResult:
        """Return a validated local composition.

        Parameters
        ----------
        roots
            Explicit repository and resource roots.
        profile_bytes, generic_manifest_bytes, local_manifest_bytes
            Exact JSON bytes selected by the caller.

        Returns
        -------
        AdaptationResult
            A `LocalHarnessContext` on success; local diagnostics otherwise.
        """
        if type(roots) is not RepositoryRoots:
            raise TypeError("roots must be RepositoryRoots")
        resolved_roots: dict[str, Path] = {}
        for name in (
            "repository_root",
            "generic_resource_root",
            "local_resource_root",
        ):
            root = getattr(roots, name)
            try:
                resolved = root.resolve(strict=True)
            except OSError:
                resolved = None
            if resolved is None or resolved != root or not root.is_dir():
                return failure(
                    LocalIssue(
                        "PIHL.CONTEXT.ROOT_INVALID",
                        str(root),
                        f"{name} must be an existing resolved nonsymlink directory",
                    )
                )
            resolved_roots[name] = resolved
        repository_root = resolved_roots["repository_root"]
        if any(
            not resolved_roots[name].is_relative_to(repository_root)
            for name in ("generic_resource_root", "local_resource_root")
        ):
            return failure(
                LocalIssue(
                    "PIHL.CONTEXT.ROOT_INVALID",
                    None,
                    "resource roots must resolve below repository_root",
                )
            )
        for value, name in (
            (profile_bytes, "profile"),
            (generic_manifest_bytes, "generic manifest"),
            (local_manifest_bytes, "local manifest"),
        ):
            if type(value) is not bytes:
                raise TypeError(f"{name} bytes must be bytes")
        profile_result = ProjectProfileLoader().execute(profile_bytes, None, (1,), (1,))
        if profile_result.profile is None:
            return failure(
                LocalIssue(
                    "PIHL.CONTEXT.PROFILE_INVALID",
                    None,
                    profile_result.validation.status,
                )
            )
        decoded = []
        for payload, label in (
            (generic_manifest_bytes, "generic"),
            (local_manifest_bytes, "local"),
        ):
            result = JsonRecordDeserializer().execute(
                WireRecordKind.ResourceManifest, payload
            )
            if type(result.record) is not ResourceManifest:
                return failure(
                    LocalIssue(
                        "PIHL.CONTEXT.MANIFEST_INVALID", label, result.validation.status
                    )
                )
            decoded.append(result.record)
        generic, local = decoded
        validation = ResourceManifestValidator().execute(
            generic,
            ArtifactIdentity(
                1, "sha256", hashlib.sha256(generic_manifest_bytes).hexdigest()
            ),
            local,
            ArtifactIdentity(
                1, "sha256", hashlib.sha256(local_manifest_bytes).hexdigest()
            ),
            profile_result.profile,
        )
        if validation.status == "FAIL":
            return failure(
                LocalIssue(
                    "PIHL.CONTEXT.COMPOSITION_INVALID",
                    None,
                    ",".join(x.code for x in validation.issues),
                )
            )
        return success(
            LocalHarnessContext(
                roots,
                profile_result.profile,
                generic,
                ArtifactIdentity(
                    1, "sha256", hashlib.sha256(generic_manifest_bytes).hexdigest()
                ),
                local,
                ArtifactIdentity(
                    1, "sha256", hashlib.sha256(local_manifest_bytes).hexdigest()
                ),
            )
        )
