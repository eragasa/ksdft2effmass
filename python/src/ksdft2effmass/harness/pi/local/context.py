"""Explicit project-local harness context composition."""

from __future__ import annotations

import hashlib

from .. import (
    ArtifactIdentity,
    DeserializeJsonRecord,
    LoadProjectProfile,
    ResourceManifest,
    ValidateResourceManifest,
    WireRecordKind,
)
from ._parsing import failure, success
from .models import AdaptationResult, LocalHarnessContext, LocalIssue, RepositoryRoots


class LoadLocalHarnessContext:
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
        for name in (
            "repository_root",
            "generic_resource_root",
            "local_resource_root",
        ):
            root = getattr(roots, name)
            if not root.exists() or not root.is_dir():
                return failure(
                    LocalIssue(
                        "PIHL.CONTEXT.ROOT_INVALID",
                        str(root),
                        f"{name} must be an existing directory",
                    )
                )
        for value, name in (
            (profile_bytes, "profile"),
            (generic_manifest_bytes, "generic manifest"),
            (local_manifest_bytes, "local manifest"),
        ):
            if type(value) is not bytes:
                raise TypeError(f"{name} bytes must be bytes")
        profile_result = LoadProjectProfile().execute(profile_bytes, None, (1,), (1,))
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
            result = DeserializeJsonRecord().execute(
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
        validation = ValidateResourceManifest().execute(
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
