"""Compatibility adapters and selectors for selected evidence records."""

from __future__ import annotations

from .. import ResourcePath
from ._parsing import as_str, failure, parse_object, success
from .models import AdaptationResult, EvidenceOwnershipRelation, LocalIssue


def _invalid(area: str, path: str, exc: Exception) -> AdaptationResult:
    return failure(LocalIssue(f"PIHL.{area}.INVALID", path, str(exc)))


class EvidenceOwnershipManifestAdapter:
    """Normalize the retained P1 evidence-ownership manifest.

    The action consumes only caller-supplied bytes. It maps the historical
    ``boundary_owned`` spelling to accepted ``artifact_owned`` evidence plus
    explicit agreement metadata; it does not add a generic ownership kind,
    discover evidence, or change maintained evidence ownership.
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


class EvidenceModuleSelector:
    """Confine caller-selected evidence module bytes to profile scopes.

    The generic project profile owns the scope rules. This ActionObject selects
    explicit bytes only and performs no discovery, parsing, or evidence
    validation.
    """

    __slots__ = ()

    def execute(
        self, module_payloads: tuple[tuple[ResourcePath, bytes], ...], profile: object
    ) -> AdaptationResult:
        """Return sorted explicit modules accepted by a project profile.

        Parameters
        ----------
        module_payloads
            Exact ``(resource_path, Python_source_bytes)`` pairs selected by the
            caller.
        profile
            Exact generic `ProjectProfile` whose evidence scope rules constrain
            every path.

        Returns
        -------
        AdaptationResult
            The path-sorted input pairs on success, or a deterministic outside-
            scope diagnostic.

        Raises
        ------
        TypeError
            If the profile, collection, path, or payload has the wrong semantic
            type.
        """
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
