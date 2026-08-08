r"""Software verification of ``RecordHumanReviewDecision``.

Facet and represented meaning
Software verification of pure explicit recording of one already-made human decision.

Intrinsic and cross-object scope
The sole primary SUT is ``RecordHumanReviewDecision``. Packet identity transfer,
blocked-packet compatibility, explicit disposition handling, idempotency, nonmutation,
and absence of interpretation or external effects are covered.

VVUQ and scientific exclusions
Passing establishes only the stated software contract. It does not infer or
authenticate human authority, persist a decision, or establish numerical verification,
scientific validation, or UQ.
"""

import ast
from dataclasses import replace
from pathlib import Path

import pytest

from ksdft2effmass.harness.pi import (
    HumanReviewDecision,
    HumanReviewFinding,
    HumanReviewObservation,
    HumanReviewPacket,
    HumanReviewTarget,
    RecordHumanReviewDecision,
)

pytestmark = pytest.mark.software_verification
SUT = RecordHumanReviewDecision


def make_packet(status: str = "ready_for_human_review") -> HumanReviewPacket:
    """Evidence ID
    Owns no identifier; supports recording evidence.
    Requirement
    Recording tests require one explicit packet with advisories and limitations.
    Method
    Construct fixed public target, observation, finding, and packet records.
    Oracle
    Their accepted constructors define valid support input.
    Acceptance
    Return one HumanReviewPacket with the requested valid status.
    Interpretation
    Failure identifies setup drift rather than recording behavior.
    Limitations
    The helper does not prepare or disposition the packet.
    """
    target = HumanReviewTarget(
        "human-review.example",
        "0123456789abcdef0123456789abcdef01234567",
        "ExampleSubject",
        ("python/src/example.py",),
        "software_verification",
        ("docs/contract.md",),
    )
    observation = HumanReviewObservation(
        "human-review.observation.focused",
        "focused tests",
        "passed" if status == "ready_for_human_review" else "failed",
        "Focused software-verification tests completed.",
        "python/src/example.py",
    )
    finding = HumanReviewFinding(
        "human-review.finding.advisory",
        "advisory",
        "One advisory remains for human judgment.",
        None,
        (observation.observation_id,),
        "Software verification cannot establish human authority.",
    )
    return HumanReviewPacket(
        target,
        (observation,),
        (finding,),
        ("One explicit limitation remains.",),
        status,
    )


def test_constructor__action_object__is_stateless_and_fieldless() -> None:
    """Evidence ID
    ``SV-HARNESS-161``.
    Requirement
    RecordHumanReviewDecision is a concrete fieldless stateless ActionObject.
    Method
    Construct two instances and inspect their storage boundaries.
    Oracle
    The accepted action contract requires no retained packet, actor, clock, client,
    persistence handle, or mutable state.
    Acceptance
    Both instances lack dictionaries and the class declares empty slots.
    Interpretation
    Failure identifies unauthorized retained state.
    Limitations
    Static storage does not establish runtime compatibility behavior.
    """
    first = SUT()
    second = SUT()
    assert SUT.__slots__ == ()
    assert not hasattr(first, "__dict__")
    assert not hasattr(second, "__dict__")


def test_method__execute__transfers_identity_preserves_text_and_is_idempotent() -> None:
    """Evidence ID
    ``SV-HARNESS-162``.
    Requirement
    Recording copies exact packet identity, preserves response text, and is
    deterministic without mutating the packet.
    Method
    Snapshot one ready packet and execute twice with identical explicit inputs.
    Oracle
    Packet target fields, exact string equality, dataclass equality, and frozen packet
    value semantics are independent exact oracles.
    Acceptance
    Equal decisions contain exact identity and response values, and the packet equals
    its pre-execution snapshot.
    Interpretation
    Failure identifies identity drift, text rewriting, nondeterminism, or mutation.
    Limitations
    Equality is runtime value equality, not persisted identity.
    """
    packet = make_packet()
    snapshot = replace(packet)
    response = "\n Accept this exact packet; keep punctuation! \t"
    inputs = (packet, response, "accepted", ())
    first = SUT().execute(*inputs)
    second = SUT().execute(*inputs)
    assert first == second
    assert type(first) is HumanReviewDecision
    assert first.review_id == packet.target.review_id
    assert first.reviewed_revision == packet.target.revision
    assert first.human_response == response
    assert packet == snapshot


@pytest.mark.parametrize(
    ("disposition", "scope"),
    (
        pytest.param("accepted", (), id="accepted"),
        pytest.param(
            "bounded_correction",
            ("Modify exactly one named surface.",),
            id="bounded_correction",
        ),
        pytest.param("deferred", (), id="deferred"),
        pytest.param("rejected", (), id="rejected"),
    ),
)
def test_method__execute__records_each_explicit_normalized_disposition(
    disposition: str, scope: tuple[str, ...]
) -> None:
    """Evidence ID
    ``SV-HARNESS-163``.
    Requirement
    The action records every normalized disposition when explicit scope is compatible.
    Method
    Execute once for each closed-vocabulary disposition and its required scope shape.
    Oracle
    Caller-supplied normalized values and exact tuple equality are exact.
    Acceptance
    The returned decision retains disposition and scope unchanged.
    Interpretation
    Failure identifies hidden mapping or disposition-routing drift.
    Limitations
    The action does not decide which disposition the human intended.
    """
    decision = SUT().execute(make_packet(), "Exact response.", disposition, scope)
    assert decision.disposition == disposition
    assert decision.authorized_scope == scope


def test_method__execute__accepts_ready_packet_with_advisories_and_limitations() -> (
    None
):
    """Evidence ID
    ``SV-HARNESS-164``.
    Requirement
    Advisory findings and limitations do not automatically block explicit acceptance
    of a ready packet.
    Method
    Accept a ready packet containing one advisory finding and one limitation.
    Oracle
    Only ``blocked_by_invalid_observation`` prohibits accepted disposition.
    Acceptance
    The decision is accepted while the source packet retains its advisory and
    limitation.
    Interpretation
    Failure identifies unauthorized automatic review acceptance policy.
    Limitations
    This test does not judge whether acceptance is substantively wise.
    """
    packet = make_packet()
    decision = SUT().execute(packet, "Accept despite advisory.", "accepted", ())
    assert decision.disposition == "accepted"
    assert packet.findings[0].severity == "advisory"
    assert packet.limitations == ("One explicit limitation remains.",)


def test_method__execute__rejects_acceptance_of_blocked_packet() -> None:
    """Evidence ID
    ``SV-HARNESS-165``.
    Requirement
    A packet blocked by an invalid observation cannot receive accepted disposition.
    Method
    Supply an explicit accepted disposition for a blocked packet.
    Oracle
    The accepted packet-to-decision compatibility rule fixes exact rejection.
    Acceptance
    ValueError is raised with the stable ready-packet message.
    Interpretation
    Failure identifies fail-open acceptance compatibility.
    Limitations
    Other normalized dispositions remain available for blocked packets.
    """
    with pytest.raises(
        ValueError, match="^accepted disposition requires a ready packet$"
    ):
        SUT().execute(
            make_packet("blocked_by_invalid_observation"), "Accept.", "accepted", ()
        )


@pytest.mark.parametrize(
    ("disposition", "scope"),
    (
        pytest.param("bounded_correction", (), id="bounded_without_scope"),
        pytest.param("accepted", ("Scope.",), id="accepted_with_scope"),
        pytest.param("deferred", ("Scope.",), id="deferred_with_scope"),
        pytest.param("rejected", ("Scope.",), id="rejected_with_scope"),
    ),
)
def test_method__execute__rejects_invalid_disposition_scope_combinations(
    disposition: str, scope: tuple[str, ...]
) -> None:
    """Evidence ID
    ``SV-HARNESS-166``.
    Requirement
    Recording preserves the decision object's exact disposition/scope invariant.
    Method
    Execute with each invalid normalized disposition/scope combination.
    Oracle
    HumanReviewDecision owns and supplies the intrinsic rejection rule.
    Acceptance
    Every invalid combination raises ValueError and returns no decision.
    Interpretation
    Failure identifies scope bypass at the action boundary.
    Limitations
    Intrinsic message partitions are covered by HumanReviewDecision evidence.
    """
    with pytest.raises(ValueError):
        SUT().execute(make_packet(), "Exact response.", disposition, scope)


@pytest.mark.parametrize(
    ("response", "disposition"),
    (
        pytest.param(
            "Reject this packet immediately.",
            "accepted",
            id="reject_words_with_explicit_acceptance",
        ),
        pytest.param(
            "I accept everything.",
            "rejected",
            id="accept_words_with_explicit_rejection",
        ),
    ),
)
def test_method__execute__does_not_interpret_human_response(
    response: str, disposition: str
) -> None:
    """Evidence ID
    ``SV-HARNESS-167``.
    Requirement
    Human-response language never overrides the explicit normalized disposition.
    Method
    Pair acceptance-like and rejection-like text with the opposite explicit values.
    Oracle
    Exact caller-supplied disposition, rather than natural-language content, is the
    sole normalized-value oracle.
    Acceptance
    Response and explicit disposition are both preserved exactly without fuzzy match.
    Interpretation
    Failure identifies unauthorized natural-language interpretation.
    Limitations
    The action assumes the caller supplied an already-normalized human decision.
    """
    decision = SUT().execute(make_packet(), response, disposition, ())
    assert decision.human_response == response
    assert decision.disposition == disposition


def test_method__execute__has_no_external_checkpoint_or_successor_effect(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Evidence ID
    ``SV-HARNESS-168``.
    Requirement
    Recording is pure runtime behavior with no filesystem, Git, clock, network,
    subprocess, database, checkpoint, or successor dependency or mutation.
    Method
    Execute from an empty nonrepository directory, compare its contents, and inspect
    the defining module's import and call roots.
    Oracle
    The authorized implementation needs only dataclasses, re, and lexical identity
    rules; the explicit forbidden boundary vocabulary is exact.
    Acceptance
    The directory remains empty, imports stay within the pure set, and no prohibited
    external call root occurs.
    Interpretation
    Failure identifies hidden discovery, persistence, orchestration, or external I/O.
    Limitations
    Static inspection covers maintained source calls, not arbitrary Python runtime
    implementation internals.
    """
    monkeypatch.chdir(tmp_path)
    before = tuple(tmp_path.iterdir())
    decision = SUT().execute(make_packet(), "Defer explicitly.", "deferred", ())
    assert decision.disposition == "deferred"
    assert tuple(tmp_path.iterdir()) == before == ()

    source_path = Path(__file__).resolve().parents[6] / (
        "python/src/ksdft2effmass/harness/pi/human_review.py"
    )
    tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
    imports = {
        node.module.split(".")[-1]
        if isinstance(node, ast.ImportFrom) and node.module
        else node.names[0].name.split(".")[0]
        for node in tree.body
        if isinstance(node, (ast.Import, ast.ImportFrom))
    }
    assert imports == {"__future__", "dataclasses", "re", "identity"}
    prohibited_calls = {
        "open",
        "exec",
        "eval",
        "__import__",
        "compile",
        "connect",
        "run",
        "Popen",
        "system",
        "time",
        "now",
    }
    assert (
        not {
            node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }
        & prohibited_calls
    )
