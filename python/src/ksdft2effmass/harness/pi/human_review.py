"""Pure explicit-input records and packet preparation for bounded human review.

The module represents deterministic harness observations about an explicitly
identified review target. It performs no repository discovery, filesystem or Git
access, subprocess execution, clock access, networking, database persistence,
human-decision recording, acceptance, correction, or successor activation.
Software observations remain distinct from human judgment and from numerical or
scientific evidence.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .identity import (
    _require_builtin_str,
    _require_identifier,
    _require_path,
    _require_tuple,
)

_EVIDENCE_CLASSES = {
    "software_verification",
    "numerical_verification",
    "scientific_validation",
    "uncertainty_quantification",
    "not_applicable",
}
_OBSERVATION_STATUSES = {"passed", "failed", "indeterminate", "not_run"}
_FINDING_SEVERITIES = {"blocker", "high", "medium", "low", "advisory"}
_PACKET_STATUSES = {"ready_for_human_review", "blocked_by_invalid_observation"}
_GIT_REVISION = re.compile(r"[0-9a-f]{40}\Z", re.ASCII)


@dataclass(frozen=True, slots=True)
class HumanReviewTarget:
    """Identify exactly one bounded subject for deterministic review preparation.

    Parameters
    ----------
    review_id
        Stable version-1 harness identifier for the review.
    revision
        Exact lowercase 40-character Git object name supplied by the caller.
    represented_subject
        Nonempty human-readable name of the represented public subject.
    paths
        Nonempty ordered tuple of unique normalized root-relative POSIX paths.
    evidence_class
        One member of ``software_verification``, ``numerical_verification``,
        ``scientific_validation``, ``uncertainty_quantification``, or
        ``not_applicable``.
    contract_references
        Ordered tuple of unique normalized root-relative POSIX paths identifying
        applicable contracts or maintained documentation.

    Notes
    -----
    Construction validates lexical values only. It does not inspect Git, resolve
    paths, or infer whether any supplied path exists.
    """

    review_id: str
    revision: str
    represented_subject: str
    paths: tuple[str, ...]
    evidence_class: str
    contract_references: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_identifier(self.review_id, "review_id")
        _require_builtin_str(self.revision, "revision")
        if _GIT_REVISION.fullmatch(self.revision) is None:
            raise ValueError(
                "revision must contain 40 lowercase hexadecimal characters"
            )
        _require_builtin_str(self.represented_subject, "represented_subject")
        if not self.represented_subject.strip():
            raise ValueError("represented_subject must contain non-whitespace text")
        _require_tuple(self.paths, "paths")
        paths = tuple(path for path in self.paths)
        if not paths:
            raise ValueError("paths must be nonempty")
        for path in paths:
            _require_path(path, "paths item")
        if len(set(paths)) != len(paths):
            raise ValueError("paths must contain unique paths")
        object.__setattr__(self, "paths", paths)
        _require_builtin_str(self.evidence_class, "evidence_class")
        if self.evidence_class not in _EVIDENCE_CLASSES:
            raise ValueError("unsupported evidence_class")
        _require_tuple(self.contract_references, "contract_references")
        contract_references = tuple(path for path in self.contract_references)
        for path in contract_references:
            _require_path(path, "contract_references item")
        if len(set(contract_references)) != len(contract_references):
            raise ValueError("contract_references must contain unique paths")
        object.__setattr__(self, "contract_references", contract_references)


@dataclass(frozen=True, slots=True)
class HumanReviewObservation:
    """Record one deterministic observation without making a human judgment.

    Parameters
    ----------
    observation_id
        Stable version-1 harness identifier for this observation.
    check_name
        Nonempty exact name of the check or observation method.
    status
        One of ``passed``, ``failed``, ``indeterminate``, or ``not_run``.
    summary
        Concise substantive text describing what occurred.
    path
        Optional normalized root-relative POSIX path associated with the observation.
    detail
        Optional nonempty supporting detail preserved exactly.

    Notes
    -----
    An observation does not establish human acceptance, numerical correctness,
    scientific validity, or uncertainty-quantification adequacy.
    """

    observation_id: str
    check_name: str
    status: str
    summary: str
    path: str | None = None
    detail: str | None = None

    def __post_init__(self) -> None:
        _require_identifier(self.observation_id, "observation_id")
        _require_builtin_str(self.check_name, "check_name")
        if not self.check_name.strip():
            raise ValueError("check_name must contain non-whitespace text")
        _require_builtin_str(self.status, "status")
        if self.status not in _OBSERVATION_STATUSES:
            raise ValueError("unsupported observation status")
        _require_builtin_str(self.summary, "summary")
        if not self.summary.strip():
            raise ValueError("summary must contain non-whitespace text")
        if self.path is not None:
            _require_path(self.path, "path")
        if self.detail is not None:
            _require_builtin_str(self.detail, "detail")
            if not self.detail.strip():
                raise ValueError("detail must contain non-whitespace text")


@dataclass(frozen=True, slots=True)
class HumanReviewFinding:
    """Represent one candidate issue whose disposition belongs to the human.

    Parameters
    ----------
    finding_id
        Stable version-1 harness identifier for this candidate issue.
    severity
        One of ``blocker``, ``high``, ``medium``, ``low``, or ``advisory``.
    statement
        Concise substantive issue statement preserved exactly.
    path
        Optional normalized root-relative POSIX path associated with the issue.
    supporting_observation_ids
        Ordered tuple of unique observation identifiers supporting the issue.
    unresolved_limitation
        Nonempty limitation or question requiring human disposition.

    Notes
    -----
    Harness generation does not accept this finding or recommend a human
    disposition.
    """

    finding_id: str
    severity: str
    statement: str
    path: str | None
    supporting_observation_ids: tuple[str, ...]
    unresolved_limitation: str

    def __post_init__(self) -> None:
        _require_identifier(self.finding_id, "finding_id")
        _require_builtin_str(self.severity, "severity")
        if self.severity not in _FINDING_SEVERITIES:
            raise ValueError("unsupported finding severity")
        _require_builtin_str(self.statement, "statement")
        if not self.statement.strip():
            raise ValueError("statement must contain non-whitespace text")
        if self.path is not None:
            _require_path(self.path, "path")
        _require_tuple(self.supporting_observation_ids, "supporting_observation_ids")
        supporting_observation_ids = tuple(
            identifier for identifier in self.supporting_observation_ids
        )
        for identifier in supporting_observation_ids:
            _require_identifier(identifier, "supporting_observation_ids item")
        if len(set(supporting_observation_ids)) != len(supporting_observation_ids):
            raise ValueError(
                "supporting_observation_ids must contain unique identifiers"
            )
        object.__setattr__(
            self, "supporting_observation_ids", supporting_observation_ids
        )
        _require_builtin_str(self.unresolved_limitation, "unresolved_limitation")
        if not self.unresolved_limitation.strip():
            raise ValueError("unresolved_limitation must contain non-whitespace text")


@dataclass(frozen=True, slots=True)
class HumanReviewPacket:
    """Immutable result prepared for direct human review.

    Parameters
    ----------
    target
        Exact review target supplied to packet preparation.
    observations
        Canonically ordered deterministic observations.
    findings
        Canonically ordered candidate findings.
    limitations
        Canonically ordered substantive limitations.
    status
        ``ready_for_human_review`` or ``blocked_by_invalid_observation``.

    Notes
    -----
    This ResultObject is semantically a DataObject. It stores no human decision,
    recommendation, acceptance, correction authorization, persistence handle, or
    workflow state. Cross-object compatibility is owned by
    :class:`PrepareHumanReviewPacket`.
    """

    target: HumanReviewTarget
    observations: tuple[HumanReviewObservation, ...]
    findings: tuple[HumanReviewFinding, ...]
    limitations: tuple[str, ...]
    status: str

    def __post_init__(self) -> None:
        if type(self.target) is not HumanReviewTarget:
            raise TypeError("target must be HumanReviewTarget")
        _require_tuple(self.observations, "observations")
        if any(type(item) is not HumanReviewObservation for item in self.observations):
            raise TypeError("observations must contain HumanReviewObservation")
        _require_tuple(self.findings, "findings")
        if any(type(item) is not HumanReviewFinding for item in self.findings):
            raise TypeError("findings must contain HumanReviewFinding")
        _require_tuple(self.limitations, "limitations")
        for limitation in self.limitations:
            _require_builtin_str(limitation, "limitations item")
            if not limitation.strip():
                raise ValueError("limitations items must contain non-whitespace text")
        _require_builtin_str(self.status, "status")
        if self.status not in _PACKET_STATUSES:
            raise ValueError("unsupported packet status")
        object.__setattr__(
            self, "observations", tuple(item for item in self.observations)
        )
        object.__setattr__(self, "findings", tuple(item for item in self.findings))
        object.__setattr__(
            self, "limitations", tuple(item for item in self.limitations)
        )


class PrepareHumanReviewPacket:
    """Prepare a canonical review packet from explicit immutable inputs.

    The action is fieldless and stateless. It performs cross-object relationship
    validation and deterministic ordering only.
    """

    __slots__ = ()

    def execute(
        self,
        target: HumanReviewTarget,
        observations: tuple[HumanReviewObservation, ...],
        findings: tuple[HumanReviewFinding, ...],
        limitations: tuple[str, ...],
    ) -> HumanReviewPacket:
        """Validate and prepare one immutable packet.

        Parameters
        ----------
        target
            Exact caller-supplied review target.
        observations
            Explicit observations in any declared order.
        findings
            Explicit candidate findings in any declared order.
        limitations
            Explicit substantive limitations in any declared order.

        Returns
        -------
        HumanReviewPacket
            Canonically ordered packet. A failed observation yields
            ``blocked_by_invalid_observation``; otherwise the packet is
            ``ready_for_human_review``.

        Raises
        ------
        TypeError
            If an input or tuple member has the wrong semantic type.
        ValueError
            If identifiers are duplicated, a finding references an unknown
            observation, a path falls outside the target, or limitation text is
            empty.

        Notes
        -----
        The operation preserves substantive text exactly and performs no external
        action or human decision.
        """
        if type(target) is not HumanReviewTarget:
            raise TypeError("target must be HumanReviewTarget")
        _require_tuple(observations, "observations")
        if any(type(item) is not HumanReviewObservation for item in observations):
            raise TypeError("observations must contain HumanReviewObservation")
        _require_tuple(findings, "findings")
        if any(type(item) is not HumanReviewFinding for item in findings):
            raise TypeError("findings must contain HumanReviewFinding")
        _require_tuple(limitations, "limitations")
        for limitation in limitations:
            _require_builtin_str(limitation, "limitations item")
            if not limitation.strip():
                raise ValueError("limitations items must contain non-whitespace text")

        observation_ids = tuple(item.observation_id for item in observations)
        if len(set(observation_ids)) != len(observation_ids):
            raise ValueError("observation identifiers must be unique")
        finding_ids = tuple(item.finding_id for item in findings)
        if len(set(finding_ids)) != len(finding_ids):
            raise ValueError("finding identifiers must be unique")

        known_observations = set(observation_ids)
        target_paths = set(target.paths)
        for observation in observations:
            if observation.path is not None and observation.path not in target_paths:
                raise ValueError("observation path must belong to target paths")
        for finding in findings:
            if finding.path is not None and finding.path not in target_paths:
                raise ValueError("finding path must belong to target paths")
            if not set(finding.supporting_observation_ids) <= known_observations:
                raise ValueError("finding references an unknown observation")

        canonical_observations = tuple(
            sorted(observations, key=lambda item: item.observation_id)
        )
        canonical_findings = tuple(sorted(findings, key=lambda item: item.finding_id))
        canonical_limitations = tuple(sorted(limitations))
        status = (
            "blocked_by_invalid_observation"
            if any(item.status == "failed" for item in canonical_observations)
            else "ready_for_human_review"
        )
        return HumanReviewPacket(
            target,
            canonical_observations,
            canonical_findings,
            canonical_limitations,
            status,
        )
