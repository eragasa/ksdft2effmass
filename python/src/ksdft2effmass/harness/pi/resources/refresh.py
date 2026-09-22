"""Explicit selected resource identity refresh."""

from __future__ import annotations

import hashlib
from pathlib import Path

from ..identity import ArtifactIdentity, HarnessInternalError
from ..validation import ValidationIssue, _issue, _result
from .records import (
    ResourceManifest,
    ResourceManifestRefreshRequest,
    ResourceManifestRefreshResult,
    ResourceReference,
)
from .resolution import _confined_file


class ResourceManifestRefresher:
    """Refresh selected content identities beneath one explicit root.

    The stateless action resolves only paths already declared by the supplied
    manifest, reuses the same exact-case, nonsymlink, root-confined regular-file
    observation as :class:`ResourceResolver`, and computes SHA-256 from observed
    bytes. It returns a new manifest without discovering resources or writing a
    file.
    """

    __slots__ = ()

    def execute(
        self, request: ResourceManifestRefreshRequest
    ) -> ResourceManifestRefreshResult:
        """Return a canonical manifest proposal for the explicit selection.

        Parameters
        ----------
        request
            Existing manifest, explicit absolute root, and selected resource IDs.

        Returns
        -------
        ResourceManifestRefreshResult
            Proposed immutable manifest, changed identities, and deterministic
            findings. A failed result contains no partial manifest.

        Raises
        ------
        TypeError
            If ``request`` is not exactly ``ResourceManifestRefreshRequest``.
        HarnessInternalError
            If bytes cannot be read after successful path observation.
        """
        if type(request) is not ResourceManifestRefreshRequest:
            raise TypeError("request must be ResourceManifestRefreshRequest")

        by_id: dict[str, list[ResourceReference]] = {}
        for resource in request.manifest.resources:
            by_id.setdefault(resource.resource_id, []).append(resource)

        selected: dict[str, tuple[ResourceReference, Path]] = {}
        issues: list[ValidationIssue] = []
        for resource_id in request.resource_ids:
            matches = by_id.get(resource_id, [])
            if not matches:
                issues.append(
                    _issue(
                        "PIH.RESOURCE.NOT_FOUND",
                        "Resource ID was not found.",
                        resource_id,
                    )
                )
                continue
            if len(matches) != 1:
                issues.append(
                    _issue(
                        "PIH.RESOURCE.AMBIGUOUS_SELECTION",
                        "Resource ID is ambiguous.",
                        resource_id,
                    )
                )
                continue
            reference = matches[0]
            path, problem = _confined_file(request.root, reference.path)
            if problem is not None:
                issues.append(problem)
                continue
            if path is None:
                raise AssertionError("successful confinement must return a path")
            selected[resource_id] = (reference, path)

        validation = _result(tuple(issues))
        if validation.status == "FAIL":
            return ResourceManifestRefreshResult(None, (), validation)

        identities: dict[str, ArtifactIdentity] = {}
        changed_ids: list[str] = []
        for resource_id in request.resource_ids:
            reference, path = selected[resource_id]
            try:
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
            except OSError as exc:
                raise HarnessInternalError(
                    "ResourceManifestRefresher", str(exc)
                ) from exc
            identity = ArtifactIdentity(1, "sha256", digest)
            identities[resource_id] = identity
            if identity != reference.content_identity:
                changed_ids.append(resource_id)

        refreshed_resources = tuple(
            ResourceReference(
                resource.schema_version,
                resource.resource_id,
                resource.resource_kind,
                resource.format_version,
                resource.path,
                identities[resource.resource_id],
                resource.dependency_ids,
            )
            if resource.resource_id in identities
            and identities[resource.resource_id] != resource.content_identity
            else resource
            for resource in request.manifest.resources
        )
        refreshed_manifest = ResourceManifest(
            request.manifest.schema_version,
            request.manifest.manifest_id,
            request.manifest.manifest_version,
            request.manifest.layer,
            request.manifest.extends_manifest_id,
            refreshed_resources,
        )
        return ResourceManifestRefreshResult(
            refreshed_manifest, tuple(changed_ids), validation
        )
