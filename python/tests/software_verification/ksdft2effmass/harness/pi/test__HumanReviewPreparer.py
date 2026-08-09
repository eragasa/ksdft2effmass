r"""Software verification of ``HumanReviewPreparer``.

Facet and represented meaning
Software verification of deterministic explicit-input human-review packet preparation.

Intrinsic and cross-object scope
The sole primary SUT is ``HumanReviewPreparer``. It owns target membership,
identifier relationships, canonical ordering, and packet-status derivation.

VVUQ and scientific exclusions
Passing establishes only the stated software contract. Preparation performs no human
disposition, correction, acceptance, numerical verification, scientific validation,
or uncertainty quantification.
"""

from dataclasses import replace
from pathlib import Path

import pytest

from ksdft2effmass.harness.pi import (
    HumanReviewFinding,
    HumanReviewObservation,
    HumanReviewPreparer,
    HumanReviewTarget,
)

pytestmark = pytest.mark.software_verification
SUT = HumanReviewPreparer
PATH_A = "python/src/example.py"
PATH_B = "python/tests/test_example.py"


def make_target() -> HumanReviewTarget:
    """Evidence ID
    Owns no identifier; supports preparation evidence.
    Requirement
    Action tests require one valid two-path target.
    Method
    Construct the target from fixed public inputs.
    Oracle
    The accepted target constructor defines valid support input.
    Acceptance
    Return one HumanReviewTarget.
    Interpretation
    Failure identifies setup drift.
    Limitations
    This helper owns no independent evidence claim.
    """
    return HumanReviewTarget(
        "human-review.example",
        "a" * 40,
        "ExampleSubject",
        (PATH_A, PATH_B),
        "software_verification",
        ("docs/contract.md",),
    )


def make_observation(identifier: str, path: str = PATH_A) -> HumanReviewObservation:
    """Evidence ID
    Owns no identifier; supports preparation evidence.
    Requirement
    Action tests require controlled valid observations.
    Method
    Construct one passed observation from explicit identity and path.
    Oracle
    The accepted observation constructor defines valid support input.
    Acceptance
    Return one HumanReviewObservation.
    Interpretation
    Failure identifies setup drift.
    Limitations
    This helper owns no independent evidence claim.
    """
    return HumanReviewObservation(
        identifier,
        "focused check",
        "passed",
        f"Exact summary for {identifier}.",
        path,
        f"Exact detail for {identifier}.",
    )


def make_finding(
    identifier: str,
    observation_id: str,
    path: str | None = PATH_B,
) -> HumanReviewFinding:
    """Evidence ID
    Owns no identifier; supports preparation evidence.
    Requirement
    Action tests require controlled valid candidate findings.
    Method
    Construct one advisory finding from explicit identity, support, and path.
    Oracle
    The accepted finding constructor defines valid support input.
    Acceptance
    Return one HumanReviewFinding.
    Interpretation
    Failure identifies setup drift.
    Limitations
    This helper owns no independent evidence claim.
    """
    return HumanReviewFinding(
        identifier,
        "advisory",
        f"Exact statement for {identifier}.",
        path,
        (observation_id,),
        f"Exact unresolved limitation for {identifier}.",
    )


def test_constructor__action_object__is_stateless_and_fieldless() -> None:
    """Evidence ID
    ``SV-HARNESS-143``.
    Requirement
    HumanReviewPreparer is a concrete fieldless stateless ActionObject.
    Method
    Construct two instances and inspect their storage boundary.
    Oracle
    The accepted action contract requires no retained root, client, clock, or state.
    Acceptance
    Instances have empty slots and no instance dictionary.
    Interpretation
    Failure identifies unauthorized retained state.
    Limitations
    Static storage does not by itself establish semantic correctness.
    """
    first = SUT()
    second = SUT()
    assert SUT.__slots__ == ()
    assert not hasattr(first, "__dict__")
    assert not hasattr(second, "__dict__")


def test_method__execute__orders_inputs_and_preserves_substantive_text() -> None:
    """Evidence ID
    ``SV-HARNESS-144``.
    Requirement
    Preparation sorts observations, findings, and limitations deterministically while
    preserving every substantive string exactly.
    Method
    Supply reverse-ordered valid records and limitations to the public action.
    Oracle
    Identifier and exact lexical ordering plus caller-supplied strings are exact.
    Acceptance
    Output tuples are sorted by identifiers/text and record text is byte-for-byte equal.
    Interpretation
    Failure identifies ordering, relationship, or text-rewriting drift.
    Limitations
    Sorting does not evaluate the correctness of represented observations.
    """
    observation_b = make_observation("human-review.observation.b", PATH_B)
    observation_a = make_observation("human-review.observation.a", PATH_A)
    finding_b = make_finding(
        "human-review.finding.b", observation_b.observation_id, PATH_B
    )
    finding_a = make_finding(
        "human-review.finding.a", observation_a.observation_id, PATH_A
    )
    packet = SUT().execute(
        make_target(),
        (observation_b, observation_a),
        (finding_b, finding_a),
        ("Z limitation.", "A limitation."),
    )
    assert tuple(item.observation_id for item in packet.observations) == (
        observation_a.observation_id,
        observation_b.observation_id,
    )
    assert tuple(item.finding_id for item in packet.findings) == (
        finding_a.finding_id,
        finding_b.finding_id,
    )
    assert packet.limitations == ("A limitation.", "Z limitation.")
    assert packet.observations[0].summary == observation_a.summary
    assert packet.findings[0].statement == finding_a.statement
    assert packet.status == "ready_for_human_review"


def test_method__execute__is_idempotent_for_identical_inputs_from_any_cwd(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Evidence ID
    ``SV-HARNESS-145``.
    Requirement
    Identical explicit inputs produce equal packets without CWD or repository discovery.
    Method
    Change to an unrelated temporary directory and execute the same action twice.
    Oracle
    Pure function semantics and exact dataclass equality are exact.
    Acceptance
    Both packets compare equal and the temporary directory remains empty.
    Interpretation
    Failure identifies nondeterminism, hidden discovery, or mutation.
    Limitations
    Dedicated dependency inspection covers forbidden external modules separately.
    """
    monkeypatch.chdir(tmp_path)
    observation = make_observation("human-review.observation.a")
    inputs = (
        make_target(),
        (observation,),
        (make_finding("human-review.finding.a", observation.observation_id),),
        ("Human disposition remains separate.",),
    )
    first = SUT().execute(*inputs)
    second = SUT().execute(*inputs)
    assert first == second
    assert tuple(tmp_path.iterdir()) == ()


def test_method__execute__maps_failed_observation_to_blocked_packet() -> None:
    """Evidence ID
    ``SV-HARNESS-146``.
    Requirement
    A valid observation reporting failure yields the nonacceptance blocked packet
    status.
    Method
    Prepare a packet containing one explicitly failed observation.
    Oracle
    The accepted packet-status derivation maps failed to blocked_by_failed_observation.
    Acceptance
    The exact blocked status is returned without a PASS or disposition field.
    Interpretation
    Failure identifies deterministic status-policy drift.
    Limitations
    The action does not decide whether the reported failure is substantively correct.
    """
    observation = replace(
        make_observation("human-review.observation.failed"), status="failed"
    )
    packet = SUT().execute(make_target(), (observation,), (), ())
    assert packet.status == "blocked_by_failed_observation"
    assert "disposition" not in packet.__dataclass_fields__


@pytest.mark.parametrize(
    "kind",
    (
        pytest.param("observation", id="duplicate_observation_identifiers"),
        pytest.param("finding", id="duplicate_finding_identifiers"),
    ),
)
def test_method__execute__rejects_duplicate_record_identifiers(kind: str) -> None:
    """Evidence ID
    ``SV-HARNESS-147``.
    Requirement
    Observation and finding identifiers are each unique within one packet.
    Method
    Supply a duplicate pair in one record family at a time.
    Oracle
    Identifier uniqueness is an exact packet relationship invariant.
    Acceptance
    Each duplicate partition raises ValueError.
    Interpretation
    Failure identifies ambiguous packet ownership.
    Limitations
    Uniqueness is local to one packet.
    """
    observation = make_observation("human-review.observation.a")
    finding = make_finding("human-review.finding.a", observation.observation_id)
    observations = (
        (observation, observation) if kind == "observation" else (observation,)
    )
    findings = (finding, finding) if kind == "finding" else (finding,)
    with pytest.raises(ValueError):
        SUT().execute(make_target(), observations, findings, ())


def test_method__execute__rejects_unknown_supporting_observation() -> None:
    """Evidence ID
    ``SV-HARNESS-148``.
    Requirement
    Every finding support identifier must name an observation in the same packet.
    Method
    Supply one valid finding that references an absent well-formed observation ID.
    Oracle
    Exact set membership supplies the independent relationship oracle.
    Acceptance
    Preparation raises ValueError.
    Interpretation
    Failure identifies dangling finding support.
    Limitations
    The action does not assess evidentiary adequacy of known support.
    """
    observation = make_observation("human-review.observation.a")
    finding = make_finding("human-review.finding.a", "human-review.observation.absent")
    with pytest.raises(ValueError):
        SUT().execute(make_target(), (observation,), (finding,), ())


@pytest.mark.parametrize(
    "kind",
    (
        pytest.param("observation", id="observation_outside_target"),
        pytest.param("finding", id="finding_outside_target"),
    ),
)
def test_method__execute__rejects_paths_outside_target(kind: str) -> None:
    """Evidence ID
    ``SV-HARNESS-149``.
    Requirement
    Every path-bearing observation or finding belongs to the exact target path set.
    Method
    Supply one lexically valid outside path in each record family.
    Oracle
    Exact path-set membership is the accepted relationship rule.
    Acceptance
    Each outside-target partition raises ValueError.
    Interpretation
    Failure identifies review-scope leakage.
    Limitations
    Membership does not establish filesystem existence.
    """
    observation = make_observation(
        "human-review.observation.a",
        "python/outside.py" if kind == "observation" else PATH_A,
    )
    finding = make_finding(
        "human-review.finding.a",
        observation.observation_id,
        "python/outside.py" if kind == "finding" else PATH_B,
    )
    with pytest.raises(ValueError):
        SUT().execute(make_target(), (observation,), (finding,), ())


@pytest.mark.parametrize(
    ("position", "value"),
    (
        pytest.param(0, object(), id="wrong_target"),
        pytest.param(1, [], id="mutable_observations"),
        pytest.param(1, (object(),), id="wrong_observation_member"),
        pytest.param(2, [], id="mutable_findings"),
        pytest.param(2, (object(),), id="wrong_finding_member"),
        pytest.param(3, [], id="mutable_limitations"),
        pytest.param(3, (" ",), id="blank_limitation"),
    ),
)
def test_method__execute__rejects_wrong_input_types(
    position: int, value: object
) -> None:
    """Evidence ID
    ``SV-HARNESS-150``.
    Requirement
    Packet preparation accepts only exact public object and immutable tuple inputs.
    Method
    Replace one valid positional input with each wrong-type semantic partition.
    Oracle
    The public execute signature and exact-type contract supply rejection behavior.
    Acceptance
    Every partition raises TypeError or ValueError before returning a packet.
    Interpretation
    Failure identifies input-boundary or mutable-container drift.
    Limitations
    Intrinsic record field types are covered by their class-owned modules.
    """
    observation = make_observation("human-review.observation.a")
    values: list[object] = [make_target(), (observation,), (), ("Limitation.",)]
    values[position] = value
    with pytest.raises((TypeError, ValueError)):
        SUT().execute(*values)  # type: ignore[arg-type]
