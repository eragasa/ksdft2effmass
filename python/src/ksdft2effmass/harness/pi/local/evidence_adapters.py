"""Compatibility adapters and selectors for selected evidence records."""

from __future__ import annotations

from .. import ResourcePath
from ._parsing import failure, success
from .models import AdaptationResult, LocalIssue


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
