"""Deprecated public compatibility for historical shadow comparison.

No maintained repository replay route consumes these records or actions. They remain
importable because R2.7 does not authorize breaking public API removal.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .. import ArtifactIdentity
from .models import LocalHarnessContext, LocalIssue, LocalValidationResult

_CLASSIFICATIONS = {"equivalent", "intentional", "defect", "deferred"}
_DIFFERENCE_KEYS = {
    "exit_status",
    "inventory",
    "issue_facts",
    "report_identity",
    "state_facts",
    "status",
}


@dataclass(frozen=True, slots=True)
class LegacyInvocation:
    """Retained legacy command identity without execution authority."""

    pair_id: str
    argv: tuple[str, ...]
    input_paths: tuple[str, ...]
    expected_report_path: str | None

    def __post_init__(self) -> None:
        if type(self.pair_id) is not str or not self.pair_id:
            raise TypeError("pair_id must be a nonempty str")
        for name in ("argv", "input_paths"):
            values = getattr(self, name)
            if type(values) is not tuple or any(type(x) is not str for x in values):
                raise TypeError(f"{name} must be a tuple of str")
        if not self.argv:
            raise ValueError("argv must be nonempty")
        if (
            self.expected_report_path is not None
            and type(self.expected_report_path) is not str
        ):
            raise TypeError("expected_report_path must be str or None")


@dataclass(frozen=True, slots=True)
class ShadowObservation:
    """Normalized machine facts from one externally collected implementation run."""

    implementation_id: str
    status: str
    issue_facts: tuple[tuple[str, str, str | None, str | None, tuple[str, ...]], ...]
    state_facts: tuple[tuple[str, tuple[str, ...]], ...]
    inventory: tuple[str, ...]
    exit_status: int
    report_identity: ArtifactIdentity | None

    def __post_init__(self) -> None:
        if type(self.implementation_id) is not str or not self.implementation_id:
            raise TypeError("implementation_id must be a nonempty str")
        if type(self.status) is not str or self.status not in {"PASS", "WARN", "FAIL"}:
            raise ValueError("status must be a built-in PASS, WARN, or FAIL str")
        if type(self.issue_facts) is not tuple:
            raise TypeError("issue_facts must be a tuple")
        for fact in self.issue_facts:
            if type(fact) is not tuple or len(fact) != 5:
                raise TypeError("issue facts must be 5-tuples")
            code, severity, subject_id, path, related_ids = fact
            if type(code) is not str or type(severity) is not str:
                raise TypeError("issue code and severity must be str")
            if subject_id is not None and type(subject_id) is not str:
                raise TypeError("issue subject identity must be str or None")
            if path is not None and type(path) is not str:
                raise TypeError("issue path must be str or None")
            if type(related_ids) is not tuple or any(
                type(identity) is not str for identity in related_ids
            ):
                raise TypeError("related identities must be a tuple of str")
            if related_ids != tuple(sorted(set(related_ids))):
                raise ValueError("related identities must be unique and sorted")
        issue_key = lambda fact: (  # noqa: E731
            fact[0],
            fact[1],
            fact[2] or "",
            fact[3] or "",
            fact[4],
        )
        if self.issue_facts != tuple(sorted(set(self.issue_facts), key=issue_key)):
            raise ValueError("issue_facts must be unique and sorted")
        if type(self.state_facts) is not tuple:
            raise TypeError("state_facts must be a tuple")
        for state_fact in self.state_facts:
            if type(state_fact) is not tuple or len(state_fact) != 2:
                raise TypeError("state facts must be pairs")
            name, identities = state_fact
            if type(name) is not str:
                raise TypeError("state fact name must be str")
            if type(identities) is not tuple or any(
                type(identity) is not str for identity in identities
            ):
                raise TypeError("state identities must be a tuple of str")
            if identities != tuple(sorted(set(identities))):
                raise ValueError("state identities must be unique and sorted")
        if self.state_facts != tuple(sorted(set(self.state_facts))):
            raise ValueError("state_facts must be unique and sorted")
        if type(self.inventory) is not tuple or any(
            type(identity) is not str for identity in self.inventory
        ):
            raise TypeError("inventory must be a tuple of str")
        if self.inventory != tuple(sorted(set(self.inventory))):
            raise ValueError("inventory must be unique and sorted")
        if type(self.exit_status) is not int:
            raise TypeError("exit_status must be int excluding bool")
        if (
            self.report_identity is not None
            and type(self.report_identity) is not ArtifactIdentity
        ):
            raise TypeError("report_identity has wrong type")


@dataclass(frozen=True, slots=True)
class ShadowPairResult:
    """Comparison of legacy and local observations for identical declared input."""

    pair_id: str
    legacy: ShadowObservation
    local: ShadowObservation
    classification: str
    differences: tuple[str, ...]
    rationale: str
    authority_citations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if type(self.pair_id) is not str or not self.pair_id:
            raise TypeError("pair_id must be a nonempty str")
        if (
            type(self.legacy) is not ShadowObservation
            or type(self.local) is not ShadowObservation
        ):
            raise TypeError("legacy and local must be ShadowObservation")
        if type(self.classification) is not str or self.classification not in (
            _CLASSIFICATIONS
        ):
            raise ValueError("invalid shadow classification")
        if type(self.differences) is not tuple or any(
            type(value) is not str or value not in _DIFFERENCE_KEYS
            for value in self.differences
        ):
            raise TypeError("differences must contain supported string keys")
        if self.differences != tuple(sorted(set(self.differences))):
            raise ValueError("differences must be unique and sorted")
        actual_differences = tuple(
            sorted(
                name
                for name in _DIFFERENCE_KEYS
                if getattr(self.legacy, name) != getattr(self.local, name)
            )
        )
        if self.differences != actual_differences:
            raise ValueError("differences must exactly describe both observations")
        if type(self.rationale) is not str or not self.rationale:
            raise TypeError("rationale must be a nonempty str")
        if type(self.authority_citations) is not tuple or any(
            type(value) is not str or not value for value in self.authority_citations
        ):
            raise TypeError("authority_citations must be nonempty strings")
        if self.authority_citations != tuple(sorted(set(self.authority_citations))):
            raise ValueError("authority_citations must be unique and sorted")
        if self.classification == "equivalent":
            if self.differences or self.authority_citations:
                raise ValueError("equivalent pairs have no differences or citations")
        elif not self.differences:
            raise ValueError("nonequivalent pairs must identify differences")
        if self.classification in {"intentional", "deferred"}:
            if not self.authority_citations:
                raise ValueError(
                    "intentional/deferred pairs require authority citations"
                )
        elif self.authority_citations:
            raise ValueError("equivalent/defect pairs cannot cite waiver authority")


@dataclass(frozen=True, slots=True)
class ShadowReplayResult:
    """Deterministic aggregate of externally collected shadow pairs."""

    pairs: tuple[ShadowPairResult, ...]
    validation: LocalValidationResult
    authoritative_clean_revision: str

    def __post_init__(self) -> None:
        if type(self.pairs) is not tuple or self.pairs != tuple(
            sorted(self.pairs, key=lambda x: x.pair_id)
        ):
            raise ValueError("pairs must be pair-ID sorted")
        if type(self.validation) is not LocalValidationResult:
            raise TypeError("validation has wrong type")
        if (
            type(self.authoritative_clean_revision) is not str
            or not self.authoritative_clean_revision
        ):
            raise TypeError("authoritative_clean_revision must be nonempty str")


class ShadowPairComparator:
    """Compare normalized fields and apply explicit accepted difference rules."""

    __slots__ = ()

    def execute(
        self,
        pair_id: str,
        legacy_observation: ShadowObservation,
        local_observation: ShadowObservation,
        approved_difference_rules: tuple[tuple[str, str, str], ...] = (),
    ) -> ShadowPairResult:
        """Classify a pair as equivalent, intentional, defect, or deferred.

        Rules are ``(difference_key, classification, authority_citation)`` triples.
        Only `intentional` and `deferred` are valid rule classifications, and
        every observed difference must have the same explicit classification.
        """
        if type(pair_id) is not str or not pair_id:
            raise TypeError("pair_id must be nonempty str")
        if (
            type(legacy_observation) is not ShadowObservation
            or type(local_observation) is not ShadowObservation
        ):
            raise TypeError("observations have wrong type")
        if type(approved_difference_rules) is not tuple:
            raise TypeError("approved_difference_rules must be a tuple")
        fields = (
            "status",
            "issue_facts",
            "state_facts",
            "inventory",
            "exit_status",
            "report_identity",
        )
        differences = tuple(
            sorted(
                name
                for name in fields
                if getattr(legacy_observation, name) != getattr(local_observation, name)
            )
        )
        if not differences:
            return ShadowPairResult(
                pair_id,
                legacy_observation,
                local_observation,
                "equivalent",
                (),
                "exact normalized parity",
            )
        rules = {}
        for rule in approved_difference_rules:
            if type(rule) is not tuple or len(rule) != 3:
                raise TypeError("difference rules must be triples")
            key, classification, citation = rule
            if (
                type(key) is not str
                or key not in _DIFFERENCE_KEYS
                or type(classification) is not str
                or classification not in {"intentional", "deferred"}
                or type(citation) is not str
                or not citation
            ):
                raise ValueError(
                    "difference rules require a supported key, "
                    "intentional/deferred classification, and citation"
                )
            if key in rules:
                raise ValueError("difference rule keys must be unique")
            rules[key] = (classification, citation)
        matched = [rules.get(key) for key in differences]
        if (
            all(rule is not None for rule in matched)
            and len({rule[0] for rule in matched if rule is not None}) == 1
        ):
            classification = matched[0][0]  # type: ignore[index]
            citations = tuple(sorted({rule[1] for rule in matched if rule is not None}))
            rationale = "; ".join(citations)
        else:
            classification, rationale, citations = (
                "defect",
                "unapproved normalized behavior difference",
                (),
            )
        return ShadowPairResult(
            pair_id,
            legacy_observation,
            local_observation,
            classification,
            differences,
            rationale,
            citations,
        )


class ShadowSuiteReplayer:
    """Aggregate externally executed pairs against one explicit clean root.

    This action intentionally does not launch commands. Collection remains an
    evidence-layer responsibility; this local action checks root/context
    ownership and deterministically assesses already structured comparisons.
    """

    __slots__ = ()

    def execute(
        self,
        pairs: tuple[ShadowPairResult, ...],
        explicit_revision_root: Path,
        context: LocalHarnessContext,
        authoritative_clean_revision: str,
    ) -> ShadowReplayResult:
        """Return sorted pair results and fail on defects or deferred behavior."""
        if type(pairs) is not tuple or any(
            type(x) is not ShadowPairResult for x in pairs
        ):
            raise TypeError("pairs must contain ShadowPairResult")
        if (
            not isinstance(explicit_revision_root, Path)
            or not explicit_revision_root.is_absolute()
            or not explicit_revision_root.is_dir()
        ):
            raise ValueError(
                "explicit_revision_root must be an absolute existing directory"
            )
        if type(context) is not LocalHarnessContext:
            raise TypeError("context must be LocalHarnessContext")
        if (
            type(authoritative_clean_revision) is not str
            or not authoritative_clean_revision
        ):
            raise TypeError("authoritative_clean_revision must be nonempty str")
        ordered = tuple(sorted(pairs, key=lambda x: x.pair_id))
        issues = tuple(
            LocalIssue(
                f"PIHL.SHADOW.{x.classification.upper()}", x.pair_id, x.rationale
            )
            for x in ordered
            if x.classification in {"defect", "deferred"}
        )
        validation = LocalValidationResult(
            "FAIL" if issues else "PASS",
            tuple(sorted(issues, key=lambda x: (x.code, x.path or "", x.detail))),
        )
        return ShadowReplayResult(ordered, validation, authoritative_clean_revision)
