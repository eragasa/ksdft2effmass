"""Construction of contained LaTeX manuscript source graphs."""

import re
from pathlib import Path

from ksdft2effmass.publications.audit_records import (
    LatexManuscriptAuditIssue,
    LatexManuscriptAuditIssueCode,
    LatexManuscriptAuditRequest,
    LatexSource,
    LatexSourceGraph,
    LatexSourceGraphConstructionResult,
)


class LatexSourceGraphConstructor:
    """Construct one manuscript composition and bibliography source graph."""

    __slots__ = ()

    _bibliography_pattern = re.compile(
        r"\\addbibresource(?:\s*\[[^\]]*\])?\{([^{}]+)\}"
    )
    _include_pattern = re.compile(r"\\(?:include|input)\{([^{}]+)\}")

    def execute(
        self, request: LatexManuscriptAuditRequest
    ) -> LatexSourceGraphConstructionResult:
        """Load one recursively composed source graph without executing TeX."""
        if type(request) is not LatexManuscriptAuditRequest:
            raise TypeError("request must be LatexManuscriptAuditRequest")

        issues: list[LatexManuscriptAuditIssue] = []
        source_texts: dict[Path, str] = {}
        self._load_composition_source(
            request,
            request.composition_path,
            (),
            source_texts,
            issues,
        )
        composition_sources = tuple(
            LatexSource(path, source_texts[path]) for path in sorted(source_texts)
        )
        bibliography_sources = self._load_bibliographies(
            request,
            composition_sources,
            issues,
        )
        return LatexSourceGraphConstructionResult(
            LatexSourceGraph(composition_sources, bibliography_sources),
            tuple(issues),
        )

    def _load_composition_source(
        self,
        request: LatexManuscriptAuditRequest,
        path: Path,
        ancestors: tuple[Path, ...],
        source_texts: dict[Path, str],
        issues: list[LatexManuscriptAuditIssue],
    ) -> None:
        """Load one source and recursively follow its composition edges."""
        if path in ancestors:
            parent = ancestors[-1] if ancestors else request.composition_path
            issues.append(
                LatexManuscriptAuditIssue(
                    LatexManuscriptAuditIssueCode.INCLUDE_CYCLE,
                    parent,
                    1,
                    str(path.relative_to(request.source_root)),
                )
            )
            return
        if path in source_texts:
            return
        if not path.is_file():
            issues.append(
                LatexManuscriptAuditIssue(
                    LatexManuscriptAuditIssueCode.MISSING_SOURCE,
                    path,
                    1,
                    str(path),
                )
            )
            return

        source = LatexSource(path, path.read_text(encoding="utf-8"))
        source_texts[path] = source.text
        for match in self._include_pattern.finditer(source.visible_text):
            target = self._include_path(request.source_root, match.group(1))
            line = source.line_number(match.start())
            if target is None:
                issues.append(
                    LatexManuscriptAuditIssue(
                        LatexManuscriptAuditIssueCode.INCLUDE_PATH_ESCAPE,
                        path,
                        line,
                        match.group(1),
                    )
                )
                continue
            if not target.is_file():
                issues.append(
                    LatexManuscriptAuditIssue(
                        LatexManuscriptAuditIssueCode.MISSING_INCLUDE,
                        path,
                        line,
                        match.group(1),
                    )
                )
                continue
            self._load_composition_source(
                request,
                target,
                (*ancestors, path),
                source_texts,
                issues,
            )

    def _load_bibliographies(
        self,
        request: LatexManuscriptAuditRequest,
        composition_sources: tuple[LatexSource, ...],
        issues: list[LatexManuscriptAuditIssue],
    ) -> tuple[LatexSource, ...]:
        """Load contained BibLaTeX resources declared by composition sources."""
        bibliography_texts: dict[Path, str] = {}
        for source in composition_sources:
            for match in self._bibliography_pattern.finditer(source.visible_text):
                target_text = match.group(1).strip()
                target = self._bibliography_path(request.source_root, target_text)
                line = source.line_number(match.start())
                if target is None:
                    issues.append(
                        LatexManuscriptAuditIssue(
                            LatexManuscriptAuditIssueCode.BIBLIOGRAPHY_PATH_ESCAPE,
                            source.path,
                            line,
                            target_text,
                        )
                    )
                    continue
                if not target.is_file():
                    issues.append(
                        LatexManuscriptAuditIssue(
                            LatexManuscriptAuditIssueCode.MISSING_BIBLIOGRAPHY,
                            source.path,
                            line,
                            target_text,
                        )
                    )
                    continue
                if target not in bibliography_texts:
                    bibliography_texts[target] = target.read_text(encoding="utf-8")
        return tuple(
            LatexSource(path, bibliography_texts[path])
            for path in sorted(bibliography_texts)
        )

    @staticmethod
    def _bibliography_path(source_root: Path, target_text: str) -> Path | None:
        """Resolve one extension-optional bibliography beneath the source root."""
        target = Path(target_text)
        if target.suffix == "":
            target = target.with_suffix(".bib")
        resolved = source_root / target
        try:
            resolved.relative_to(source_root)
        except ValueError:
            return None
        if ".." in target.parts:
            return None
        return resolved

    @staticmethod
    def _include_path(source_root: Path, target_text: str) -> Path | None:
        """Resolve one extension-optional include path beneath the source root."""
        target = Path(target_text)
        if target.suffix == "":
            target = target.with_suffix(".tex")
        resolved = source_root / target
        try:
            resolved.relative_to(source_root)
        except ValueError:
            return None
        if ".." in target.parts:
            return None
        return resolved
