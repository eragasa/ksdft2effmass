"""Immutable canonical resource inputs for project-local control construction."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ... import (
    ArtifactIdentity,
    JsonRecordDeserializer,
    ProjectProfile,
    ResourceManifest,
    ResourceManifestValidator,
    ResourceReference,
    ResourceResolver,
    WireRecordKind,
)
from .encoding import _ControlEncoding
from .input_files import _ControlInputFileSelector


@dataclass(frozen=True, slots=True)
class _ControlResourceInput:
    """One validated manifest entry and its repository-relative source path."""

    reference: ResourceReference
    layer: str
    source_path: str


@dataclass(frozen=True, slots=True)
class _ControlResourceCorpus:
    """Validated manifest metadata and observed resource identities."""

    generic_manifest: ResourceManifest
    local_manifest: ResourceManifest
    resources: tuple[_ControlResourceInput, ...]


class _ControlResourceCorpusBuilder:
    """Build canonical resource inputs without repository discovery."""

    __slots__ = ()

    @staticmethod
    def _decode(kind: WireRecordKind, payload: bytes, expected: type[object]) -> object:
        result = JsonRecordDeserializer().execute(kind, payload)
        if type(result.record) is not expected:
            codes = ", ".join(issue.code for issue in result.validation.issues)
            raise ValueError(f"canonical resource input is nonconforming: {codes}")
        return result.record

    def execute(
        self,
        repository_root: Path,
        profile_path: Path,
        generic_manifest_path: Path,
        generic_root_path: Path,
        local_manifest_path: Path,
        local_root_path: Path,
    ) -> _ControlResourceCorpus:
        """Validate and observe one explicit generic/local resource corpus."""
        root = repository_root.resolve()
        selector = _ControlInputFileSelector()
        profile_file = selector.file(root, profile_path, subject="resource input")
        generic_file = selector.file(
            root, generic_manifest_path, subject="resource input"
        )
        local_file = selector.file(root, local_manifest_path, subject="resource input")
        generic_root = selector.directory(root, generic_root_path)
        local_root = selector.directory(root, local_root_path)
        profile_payload = profile_file.read_bytes()
        generic_payload = generic_file.read_bytes()
        local_payload = local_file.read_bytes()
        profile = self._decode(
            WireRecordKind.ProjectProfile, profile_payload, ProjectProfile
        )
        generic = self._decode(
            WireRecordKind.ResourceManifest, generic_payload, ResourceManifest
        )
        local = self._decode(
            WireRecordKind.ResourceManifest, local_payload, ResourceManifest
        )
        assert isinstance(profile, ProjectProfile)
        assert isinstance(generic, ResourceManifest)
        assert isinstance(local, ResourceManifest)
        generic_identity = ArtifactIdentity(
            1, "sha256", _ControlEncoding.sha256(generic_payload)
        )
        local_identity = ArtifactIdentity(
            1, "sha256", _ControlEncoding.sha256(local_payload)
        )
        validation = ResourceManifestValidator().execute(
            generic,
            generic_identity,
            local,
            local_identity,
            profile,
        )
        if validation.status != "PASS":
            codes = ", ".join(issue.code for issue in validation.issues)
            raise ValueError(f"canonical resource inputs are nonconforming: {codes}")
        resources: list[_ControlResourceInput] = []
        by_layer = (
            ("generic", generic),
            ("project_local", local),
        )
        resolver = ResourceResolver()
        for layer, manifest in by_layer:
            for reference in manifest.resources:
                resolved = resolver.execute(
                    reference.resource_id,
                    generic_root,
                    generic,
                    generic_identity,
                    local_root,
                    local,
                    local_identity,
                    profile,
                )
                if (
                    resolved.validation.status != "PASS"
                    or resolved.resolved_path is None
                ):
                    codes = ", ".join(
                        issue.code for issue in resolved.validation.issues
                    )
                    raise ValueError(
                        f"canonical resource source is nonconforming: {codes}"
                    )
                selected_root = generic_root if layer == "generic" else local_root
                source_path = (
                    Path(generic_root_path if layer == "generic" else local_root_path)
                    / resolved.resolved_path.relative_to(selected_root)
                ).as_posix()
                resources.append(_ControlResourceInput(reference, layer, source_path))
        return _ControlResourceCorpus(generic, local, tuple(resources))
