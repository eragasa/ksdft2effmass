"""Pure explicit-input records, packet preparation, and human decision recording.

The module represents deterministic harness observations about an explicitly
identified review target and records an already-made human decision from explicit
inputs. It performs no natural-language interpretation, repository discovery,
filesystem or Git access, subprocess execution, clock access, networking, database
persistence, checkpoint mutation, or successor activation. Software observations and
runtime decision representation remain distinct from human authority and from
numerical or scientific evidence.
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
_PACKET_STATUSES = {"ready_for_human_review", "blocked_by_failed_observation"}
_DECISION_DISPOSITIONS = {
    "accepted",
    "bounded_correction",
    "deferred",
    "rejected",
}
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
        ``ready_for_human_review`` or ``blocked_by_failed_observation``.

    Notes
    -----
    This ResultObject is semantically a DataObject. It stores no human decision,
    recommendation, acceptance, correction authorization, persistence handle, or
    workflow state. Cross-object compatibility is owned by
    :class:`HumanReviewPreparer`.
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


@dataclass(frozen=True, slots=True)
class HumanReviewDecision:
    """Represent one explicit decision already made by a human.

    Parameters
    ----------
    packet
        Exact immutable packet being dispositioned.
    human_response
        Nonempty built-in string preserved exactly without interpretation.
    disposition
        Caller-supplied normalized member of ``accepted``,
        ``bounded_correction``, ``deferred``, or ``rejected``.
    authorized_scope
        Ordered immutable tuple of unique nonempty exact scope statements.
        ``bounded_correction`` requires at least one item; every other disposition
        prohibits scope.

    Notes
    -----
    This immutable ResultObject is semantically a DataObject. It records a decision
    supplied by the caller but does not infer intent, authenticate an actor, establish
    human authority, persist state, or activate work.
    """

    packet: HumanReviewPacket
    human_response: str
    disposition: str
    authorized_scope: tuple[str, ...]

    def __post_init__(self) -> None:
        if type(self.packet) is not HumanReviewPacket:
            raise TypeError("packet must be HumanReviewPacket")
        _require_builtin_str(self.human_response, "human_response")
        if not self.human_response:
            raise ValueError("human_response must be nonempty")
        _require_builtin_str(self.disposition, "disposition")
        if self.disposition not in _DECISION_DISPOSITIONS:
            raise ValueError("unsupported disposition")
        _require_tuple(self.authorized_scope, "authorized_scope")
        authorized_scope = tuple(item for item in self.authorized_scope)
        for item in authorized_scope:
            _require_builtin_str(item, "authorized_scope item")
            if not item:
                raise ValueError("authorized_scope items must be nonempty")
        if len(set(authorized_scope)) != len(authorized_scope):
            raise ValueError("authorized_scope must contain unique items")
        if self.disposition == "bounded_correction" and not authorized_scope:
            raise ValueError("bounded_correction requires authorized_scope")
        if self.disposition != "bounded_correction" and authorized_scope:
            raise ValueError("authorized_scope requires bounded_correction")
        object.__setattr__(self, "authorized_scope", authorized_scope)


class HumanReviewDecisionRecorder:
    """Record an explicit normalized human decision without interpreting text.

    The action is fieldless and stateless. Packet-to-decision compatibility is its
    only cross-object policy.
    """

    __slots__ = ()

    def execute(
        self,
        packet: HumanReviewPacket,
        human_response: str,
        disposition: str,
        authorized_scope: tuple[str, ...],
    ) -> HumanReviewDecision:
        """Construct one immutable decision from explicit caller-supplied values.

        Parameters
        ----------
        packet
            Exact prepared packet retained by the decision.
        human_response
            Exact nonempty built-in string to preserve without interpretation.
        disposition
            Explicit normalized disposition; no text-to-disposition inference occurs.
        authorized_scope
            Explicit ordered scope. It is required only for
            ``bounded_correction`` and prohibited for other dispositions.

        Returns
        -------
        HumanReviewDecision
            Immutable exact decision representation.

        Raises
        ------
        TypeError
            If the packet or decision fields have wrong semantic types.
        ValueError
            If intrinsic decision invariants fail, the packet is not a canonical
            ``HumanReviewPreparer`` result, or ``accepted`` is supplied for a packet
            blocked by a failed observation.

        Notes
        -----
        A ready packet may be accepted while advisory findings or limitations remain.
        This operation performs no natural-language interpretation, persistence,
        filesystem, Git, checkpoint, subprocess, clock, network, database, or
        successor action and does not establish caller authority.
        """
        if type(packet) is not HumanReviewPacket:
            raise TypeError("packet must be HumanReviewPacket")
        try:
            canonical_packet = HumanReviewPreparer().execute(
                packet.target,
                packet.observations,
                packet.findings,
                packet.limitations,
            )
        except ValueError as error:
            raise ValueError(
                "packet must equal its canonical prepared result"
            ) from error
        if packet != canonical_packet:
            raise ValueError("packet must equal its canonical prepared result")
        if (
            disposition == "accepted"
            and packet.status == "blocked_by_failed_observation"
        ):
            raise ValueError("accepted disposition requires a ready packet")
        return HumanReviewDecision(
            packet,
            human_response,
            disposition,
            authorized_scope,
        )


class HumanReviewPreparer:
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
            ``blocked_by_failed_observation``; otherwise the packet is
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
            "blocked_by_failed_observation"
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
