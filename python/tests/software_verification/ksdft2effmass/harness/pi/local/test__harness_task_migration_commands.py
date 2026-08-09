r"""Software verification of harness-task-migration-commands-v1.

Facet and represented meaning

Artifact-owned verification of the explicit-file preparation and disposition
commands and their canonical handoff.

Intrinsic and cross-object scope

The owned artifact is ``harness-task-migration-commands-v1``. Tests exercise
filesystem confinement, ActionObject translation, deterministic output, and the
closed command-to-command binding.

VVUQ and scientific exclusions

Passing establishes synthetic software behavior only. It migrates no real Task,
provides no human acceptance, and establishes no scientific claim.
"""

from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path

import pytest

from ksdft2effmass.harness.pi.local import HarnessTaskSerializer
from ksdft2effmass.harness.pi.local.prepare_harness_task_migration_review import (
    main as prepare_main,
)
from ksdft2effmass.harness.pi.local.record_harness_task_migration_disposition import (
    main as disposition_main,
)

from .task_model_examples import make_task

pytestmark = pytest.mark.software_verification


def calculate_sha256(content: bytes) -> str:
    """Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: Synthetic support needs an independent exact-byte identity.

    Method: Hash explicit bytes with the standard-library SHA-256 implementation.

    Oracle: SHA-256 hexadecimal output has its defined 64-character representation.

    Acceptance: The helper returns the standard-library digest unchanged.

    Interpretation: Failure invalidates synthetic identity setup.

    Limitations: This helper makes no independent pass or provenance claim.
    """
    return hashlib.sha256(content).hexdigest()


def write_json_fixture(path: Path, value: object) -> None:
    """Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: Synthetic JSON support uses deterministic readable bytes.

    Method: Serialize one explicit value with fixed indentation and one final LF.

    Oracle: The standard-library serializer and fixed formatting define the bytes.

    Acceptance: The supplied path contains exactly the represented JSON text.

    Interpretation: Failure invalidates synthetic command-input setup.

    Limitations: This helper is test-only and makes no persistence-contract claim.
    """
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def make_preparation_arguments(root: Path, *, stale: str | None = None) -> list[str]:
    """Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: Command tests require one complete non-real migration input set.

    Method: Write explicit synthetic source, candidate, mapping, and profile files.

    Oracle: Accepted public constructors and the documented command formats define it.

    Acceptance: Returned arguments name the complete synthetic files and identities.

    Interpretation: Failure invalidates command test setup.

    Limitations: The helper performs no real migration and owns no independent pass.
    """
    source = b"Synthetic command input.\n"
    task = make_task(
        documentation_path="synthetic/candidate.md",
        intake_path="synthetic/candidate.intake.md",
    )
    (root / "synthetic").mkdir()
    (root / "synthetic/source.md").write_bytes(source)
    (root / "synthetic/candidate.json").write_bytes(
        HarnessTaskSerializer().execute(task)
    )
    mapping = {
        "schema_version": 1,
        "source_path": "synthetic/source.md",
        "source_revision": "a" * 40,
        "git_object": "b" * 40,
        "source_sha256": calculate_sha256(source),
        "byte_count": len(source),
        "documentation_path": "synthetic/candidate.md",
        "mappings": [
            {
                "mapping_id": "intro",
                "start_byte": 0,
                "end_byte": len(source),
                "span_sha256": calculate_sha256(source),
                "disposition": "DOCUMENTATION_OWNED_CONTENT",
                "target_references": ["synthetic/candidate.md"],
                "transformation": "preserve exact bytes",
                "rationale": "synthetic software verification",
            }
        ],
    }
    if stale == "revision":
        mapping["source_revision"] = "c" * 40
    elif stale == "git_object":
        mapping["git_object"] = "c" * 40
    elif stale == "byte_count":
        mapping["byte_count"] = len(source) + 1
    elif stale == "source_sha256":
        mapping["source_sha256"] = "0" * 64
    elif stale == "span_sha256":
        mapping["mappings"][0]["span_sha256"] = "0" * 64  # type: ignore[index]
    elif stale == "coverage":
        mapping["mappings"][0]["end_byte"] = len(source) - 1  # type: ignore[index]
        mapping["mappings"][0]["span_sha256"] = calculate_sha256(  # type: ignore[index]
            source[:-1]
        )
    write_json_fixture(root / "synthetic/mapping.json", mapping)
    template = b"{{content.intro}}\n" if stale == "coverage" else b"{{content.intro}}"
    write_json_fixture(
        root / "synthetic/profile.json",
        {
            "schema_version": 1,
            "profile_id": "synthetic-command-profile",
            "template_encoding": "base64",
            "template_bytes_base64": base64.b64encode(template).decode("ascii"),
            "template_identity": {
                "schema_version": 1,
                "algorithm": "sha256",
                "digest": calculate_sha256(template),
            },
            "final_lf": True,
        },
    )
    return [
        "--repository-root",
        str(root),
        "--source-markdown",
        "synthetic/source.md",
        "--source-revision",
        "a" * 40,
        "--git-object",
        "b" * 40,
        "--candidate-task-json",
        "synthetic/candidate.json",
        "--source-mapping-record",
        "synthetic/mapping.json",
        "--projection-profile",
        "synthetic/profile.json",
        "--output-review-document",
        "synthetic/review.md",
    ]


def prepare_synthetic_review(
    root: Path, capsys: pytest.CaptureFixture[str]
) -> dict[str, object]:
    """Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: Disposition tests start from one successfully prepared result.

    Method: Invoke preparation on the shared synthetic input set and decode stdout.

    Oracle: Status zero and JSON decoding define valid support setup.

    Acceptance: The returned mapping is the emitted structured result.

    Interpretation: Failure invalidates downstream disposition setup.

    Limitations: This helper makes no independent acceptance claim.
    """
    arguments = make_preparation_arguments(root)
    assert prepare_main(arguments) == 0
    first = json.loads(capsys.readouterr().out)
    review_path = root / "synthetic/review.md"
    original_bytes = review_path.read_bytes()
    original_stat = review_path.stat()
    assert prepare_main(arguments) == 0
    recovered = json.loads(capsys.readouterr().out)
    recovered_stat = review_path.stat()
    assert recovered == first
    assert review_path.read_bytes() == original_bytes
    assert (
        recovered_stat.st_ino,
        recovered_stat.st_mode,
        recovered_stat.st_size,
        recovered_stat.st_mtime_ns,
    ) == (
        original_stat.st_ino,
        original_stat.st_mode,
        original_stat.st_size,
        original_stat.st_mtime_ns,
    )
    assert not tuple((root / "synthetic").glob(".review.md.*"))
    return recovered


def test_artifact__arguments__requires_closed_explicit_interface() -> None:
    """Evidence ID: ``SV-HT-063``.

    Requirement: Preparation requires every explicit root, identity, input, and output.

    Method: Invoke the parser without arguments.

    Oracle: ``argparse`` requires the documented closed argument set.

    Acceptance: Parsing terminates with status 2 before filesystem access.

    Interpretation: Failure exposes an ambient or default input path.

    Limitations: This test does not exercise valid packet construction.
    """
    with pytest.raises(SystemExit) as raised:
        prepare_main([])
    assert raised.value.code == 2


@pytest.mark.parametrize(
    "stale",
    (
        pytest.param("revision", id="source_revision"),
        pytest.param("git_object", id="git_object"),
        pytest.param("byte_count", id="byte_count"),
        pytest.param("source_sha256", id="source_sha256"),
        pytest.param("span_sha256", id="mapping_span_sha256"),
    ),
)
def test_artifact__source_identity__rejects_stale_explicit_values(
    tmp_path: Path, stale: str, capsys: pytest.CaptureFixture[str]
) -> None:
    """Evidence ID: ``SV-HT-064``.

    Requirement: Source revision, Git object, byte count, source SHA, and span SHA bind.

    Method: Change exactly one synthetic mapping-record identity partition.

    Oracle: Exact caller-supplied source bytes and identities must agree.

    Acceptance: Every stale partition returns status 1 and writes no review document.

    Interpretation: Failure permits stale source or mapping substitution.

    Limitations: Git identity is checked for agreement, not queried from Git.
    """
    assert prepare_main(make_preparation_arguments(tmp_path, stale=stale)) == 1
    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "INVALID_PACKET"
    assert not (tmp_path / "synthetic/review.md").exists()


def test_artifact__paths__rejects_traversal_and_symlinks(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Evidence ID: ``SV-HT-065``.

    Requirement: Every selected input remains below the explicit root and nonsymlink.

    Method: Independently supply parent traversal and a symlinked source.

    Oracle: Resolved lexical identity and root containment are exact requirements.

    Acceptance: Both operations return status 2 without output.

    Interpretation: Failure exposes an ambient, traversal, or symlink read path.

    Limitations: Parent-component race hardening remains outside the threat model.
    """
    args = make_preparation_arguments(tmp_path)
    args[args.index("synthetic/source.md")] = "../source.md"
    assert prepare_main(args) == 2
    capsys.readouterr()
    source = tmp_path / "synthetic/source.md"
    target = tmp_path / "synthetic/target.md"
    source.rename(target)
    source.symlink_to(target)
    args = make_existing_input_arguments(tmp_path)
    assert prepare_main(args) == 2
    assert json.loads(capsys.readouterr().out)["status"] == "INVALID_INPUT"

    symlink_root = tmp_path / "symlink-output"
    symlink_root.mkdir()
    symlink_args = make_preparation_arguments(symlink_root)
    symlink_target = symlink_root / "synthetic/target-review.md"
    symlink_target.write_bytes(b"target\n")
    (symlink_root / "synthetic/review.md").symlink_to(symlink_target)
    assert prepare_main(symlink_args) == 2
    capsys.readouterr()

    directory_root = tmp_path / "directory-output"
    directory_root.mkdir()
    directory_args = make_preparation_arguments(directory_root)
    (directory_root / "synthetic/review.md").mkdir()
    assert prepare_main(directory_args) == 2
    capsys.readouterr()
    assert not tuple(symlink_root.glob("synthetic/.review.md.*"))
    assert not tuple(directory_root.glob("synthetic/.review.md.*"))


def make_existing_input_arguments(root: Path) -> list[str]:
    """Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: Later command phases reuse the exact original explicit inputs.

    Method: Construct the fixed argument vector without reading or discovering paths.

    Oracle: The documented preparation argument names define the common subset.

    Acceptance: The vector names only the already-created synthetic files.

    Interpretation: Failure invalidates symlink or disposition test setup.

    Limitations: This helper owns no command result or independent pass.
    """
    return [
        "--repository-root",
        str(root),
        "--source-markdown",
        "synthetic/source.md",
        "--source-revision",
        "a" * 40,
        "--git-object",
        "b" * 40,
        "--candidate-task-json",
        "synthetic/candidate.json",
        "--source-mapping-record",
        "synthetic/mapping.json",
        "--projection-profile",
        "synthetic/profile.json",
        "--output-review-document",
        "synthetic/review.md",
    ]


def test_artifact__coverage__propagates_packet_preparation_failure(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Evidence ID: ``SV-HT-066``.

    Requirement: Incomplete mapping coverage fails through packet preparation.

    Method: Supply a valid shorter mapping that leaves one source byte uncovered.

    Oracle: The accepted preparer requires complete source coverage.

    Acceptance: Status is 1 and no partial output exists.

    Interpretation: Failure bypasses an authoritative packet-preparation condition.

    Limitations: Only one synthetic coverage gap is represented.
    """
    assert prepare_main(make_preparation_arguments(tmp_path, stale="coverage")) == 1
    assert json.loads(capsys.readouterr().out)["status"] == "INVALID_PACKET"
    assert not (tmp_path / "synthetic/review.md").exists()


def test_artifact__rendering__is_deterministic_and_canonical(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Evidence ID: ``SV-HT-067``.

    Requirement: Identical explicit inputs produce byte-identical review documents.

    Method: Prepare once, discard the receipt, and prepare against the same output.

    Oracle: Existing packet renderer and canonical compact stdout define exact bytes.

    Acceptance: Bytes, count, SHA, packet binding, and canonical stdout agree exactly.

    Interpretation: Failure identifies nondeterminism or noncanonical translation.

    Limitations: The rendered material is synthetic and non-authoritative.
    """
    args = make_preparation_arguments(tmp_path)
    assert prepare_main(args) == 0
    stdout_one = capsys.readouterr().out
    result_one = json.loads(stdout_one)
    review_path = tmp_path / "synthetic/review.md"
    first = review_path.read_bytes()
    stat_one = review_path.stat()
    assert prepare_main(args) == 0
    stdout_two = capsys.readouterr().out
    stat_two = review_path.stat()
    assert stdout_one == stdout_two
    assert first == review_path.read_bytes()
    assert (stat_one.st_ino, stat_one.st_mode, stat_one.st_mtime_ns) == (
        stat_two.st_ino,
        stat_two.st_mode,
        stat_two.st_mtime_ns,
    )
    assert (
        stdout_one
        == json.dumps(result_one, separators=(",", ":"), sort_keys=True) + "\n"
    )
    assert result_one["result"] == "available"
    assert result_one["packet_binding_sha256"] == (
        "fbb81a733b630e08dc1fb0c74d772eca7fdcf94ca464dffaa7eb87a49658385e"
    )
    assert result_one["candidate_json_sha256"] == (
        "c60f13691acd33e513cc87bc114d9146544c7fa32420bb6d18139e9bbc053270"
    )
    assert result_one["review_document"] == {
        "byte_count": 3314,
        "path": "synthetic/review.md",
        "sha256": "0968c1882b87a53f80195866b5cb79c9a9af441e43ee6f14513d45106b608312",
    }
    assert result_one["review_document"]["sha256"] == calculate_sha256(first)
    assert not tuple((tmp_path / "synthetic").glob(".review.md.*"))


def test_artifact__output__preserves_existing_immutable_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Evidence ID: ``SV-HT-068``.

    Requirement: A differing existing output is a conflict and remains immutable.

    Method: Precreate sentinel output and invoke preparation with valid inputs.

    Oracle: Only byte-identical reconstructed output is recoverable.

    Acceptance: Status is 1 and sentinel bytes remain exact.

    Interpretation: Failure permits silent packet replacement.

    Limitations: Simulated process interruption and parent-directory races are excluded.
    """
    args = make_preparation_arguments(tmp_path)
    output = tmp_path / "synthetic/review.md"
    output.write_bytes(b"sentinel\n")
    before = output.stat()
    assert prepare_main(args) == 1
    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "INVALID_PACKET"
    assert "packet_binding_sha256" not in result
    assert output.read_bytes() == b"sentinel\n"
    after = output.stat()
    assert (before.st_ino, before.st_mode, before.st_mtime_ns) == (
        after.st_ino,
        after.st_mode,
        after.st_mtime_ns,
    )
    assert not tuple((tmp_path / "synthetic").glob(".review.md.*"))


def test_artifact__recovery__rejects_stale_candidate_profile_and_output_path(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Evidence ID: ``SV-HT-072``.

    Requirement: Recovery preserves candidate, profile, and output-path binding.

    Method: Independently stale canonical candidate bytes, profile identity, and path.

    Oracle: Canonical Task JSON, exact template identity, and root confinement bind.

    Acceptance: Stale content returns 1, traversal returns 2, and no output is created.

    Interpretation: Failure permits recovery from substituted durable inputs.

    Limitations: Source and mapping identity partitions are owned by ``SV-HT-064``.
    """
    candidate_root = tmp_path / "candidate"
    candidate_root.mkdir()
    candidate_args = make_preparation_arguments(candidate_root)
    candidate = candidate_root / "synthetic/candidate.json"
    candidate.write_bytes(candidate.read_bytes() + b"\n")
    assert prepare_main(candidate_args) == 1
    capsys.readouterr()

    profile_root = tmp_path / "profile"
    profile_root.mkdir()
    profile_args = make_preparation_arguments(profile_root)
    profile = profile_root / "synthetic/profile.json"
    represented = json.loads(profile.read_bytes())
    represented["template_identity"]["digest"] = "0" * 64
    write_json_fixture(profile, represented)
    assert prepare_main(profile_args) == 1
    capsys.readouterr()

    output_root = tmp_path / "output"
    output_root.mkdir()
    output_args = make_preparation_arguments(output_root)
    output_args[output_args.index("synthetic/review.md")] = "../review.md"
    assert prepare_main(output_args) == 2
    capsys.readouterr()
    assert not (candidate_root / "synthetic/review.md").exists()
    assert not tuple(candidate_root.glob("synthetic/.review.md.*"))
    assert not (profile_root / "synthetic/review.md").exists()
    assert not tuple(profile_root.glob("synthetic/.review.md.*"))
    assert not (output_root / "synthetic/review.md").exists()
    assert not tuple(output_root.glob("synthetic/.review.md.*"))


def test_artifact__disposition__rejects_substitution_and_incompatibility(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Evidence ID: ``SV-HT-069``.

    Requirement: Disposition binds exact packet/document and closed disposition pairs.

    Method: Prepare once, then alter expected packet binding and generic/migration pair.

    Oracle: The preparation result and accepted recorder compatibility table are exact.

    Acceptance: Both operations return 1 and create no disposition record.

    Interpretation: Failure permits packet substitution or incompatible disposition.

    Limitations: Human text is synthetic and caller normalization remains external.
    """
    prepared = prepare_synthetic_review(tmp_path, capsys)
    args = make_disposition_arguments(tmp_path, prepared)
    packet_binding = str(prepared["packet_binding_sha256"])
    args[args.index(packet_binding)] = "0" * 64
    assert disposition_main(args) == 1
    capsys.readouterr()

    candidate_path = tmp_path / "synthetic/candidate.json"
    original_candidate = candidate_path.read_bytes()
    changed_candidate = json.loads(original_candidate)
    changed_candidate["title"] = "Substituted synthetic candidate"
    write_json_fixture(candidate_path, changed_candidate)
    assert disposition_main(make_disposition_arguments(tmp_path, prepared)) == 1
    capsys.readouterr()
    candidate_path.write_bytes(original_candidate)

    review_path = tmp_path / "synthetic/review.md"
    original_review = review_path.read_bytes()
    review_path.write_bytes(original_review + b"substitution\n")
    assert disposition_main(make_disposition_arguments(tmp_path, prepared)) == 1
    capsys.readouterr()
    review_path.write_bytes(original_review)

    alternate_review = tmp_path / "synthetic/alternate-review.md"
    alternate_review.write_bytes(original_review)
    alternate = make_disposition_arguments(tmp_path, prepared)
    alternate[alternate.index("synthetic/review.md")] = "synthetic/alternate-review.md"
    assert disposition_main(alternate) == 1
    capsys.readouterr()

    incompatible = make_disposition_arguments(tmp_path, prepared)
    incompatible[incompatible.index("DEFER_FILE")] = "ACCEPT_FILE_MIGRATION"
    assert disposition_main(incompatible) == 1
    assert json.loads(capsys.readouterr().out)["status"] == "INVALID_DISPOSITION"
    assert not (tmp_path / "synthetic/disposition.json").exists()


def make_disposition_arguments(root: Path, prepared: dict[str, object]) -> list[str]:
    """Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: Disposition tests bind the exact preparation result and response.

    Method: Extend the original arguments with explicit document identities and defer.

    Oracle: The documented disposition CLI and preparation output define the vector.

    Acceptance: Every required disposition argument is present exactly once.

    Interpretation: Failure invalidates disposition test setup.

    Limitations: The response is synthetic and provides no human authority.
    """
    review = prepared["review_document"]
    assert isinstance(review, dict)
    return make_existing_input_arguments(root)[:-2] + [
        "--review-document",
        "synthetic/review.md",
        "--expected-review-sha256",
        str(review["sha256"]),
        "--expected-review-byte-count",
        str(review["byte_count"]),
        "--expected-packet-binding-sha256",
        str(prepared["packet_binding_sha256"]),
        "--human-response",
        "Verbatim synthetic defer response\n",
        "--generic-disposition",
        "deferred",
        "--migration-disposition",
        "DEFER_FILE",
        "--output-disposition-record",
        "synthetic/disposition.json",
    ]


def test_artifact__correction_scope__is_required_only_for_revision(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Evidence ID: ``SV-HT-070``.

    Requirement: Bounded correction requires scope and all other outcomes prohibit it.

    Method: Submit revision without scope and deferral with scope.

    Oracle: ``HumanReviewDecisionRecorder`` owns exact generic scope compatibility.

    Acceptance: Both invalid records return status 1 without output.

    Interpretation: Failure bypasses bounded-correction authorization limits.

    Limitations: Scope text meaning is opaque and not interpreted.
    """
    prepared = prepare_synthetic_review(tmp_path, capsys)
    revision = make_disposition_arguments(tmp_path, prepared)
    revision[revision.index("deferred")] = "bounded_correction"
    revision[revision.index("DEFER_FILE")] = "REVISE_CONTRACT_OR_MAPPING"
    assert disposition_main(revision) == 1
    capsys.readouterr()
    deferred = make_disposition_arguments(tmp_path, prepared)
    deferred.extend(["--authorized-correction-scope", "Not allowed for defer."])
    assert disposition_main(deferred) == 1
    capsys.readouterr()
    assert not (tmp_path / "synthetic/disposition.json").exists()


def test_artifact__end_to_end__records_exact_synthetic_disposition(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Evidence ID: ``SV-HT-071``.

    Requirement: Explicit synthetic inputs flow through preparation and both recorders.

    Method: Discard the first receipt, recover it by repeated preparation, then
    supply an explicit synthetic defer response.

    Oracle: Public ActionObjects, canonical JSON, and retained exact response define
    output.

    Acceptance: Both statuses are 0; exact response, identities, and record hash agree.

    Interpretation: Failure identifies a broken maintained serial-review handoff.

    Limitations: No real migration source is used and no human authority is inferred.
    """
    prepared = prepare_synthetic_review(tmp_path, capsys)
    source_before = (tmp_path / "synthetic/source.md").read_bytes()
    candidate_before = (tmp_path / "synthetic/candidate.json").read_bytes()
    assert disposition_main(make_disposition_arguments(tmp_path, prepared)) == 0
    result = json.loads(capsys.readouterr().out)
    record_bytes = (tmp_path / "synthetic/disposition.json").read_bytes()
    record = json.loads(record_bytes)
    assert record["human_response"] == "Verbatim synthetic defer response\n"
    assert record["generic_disposition"] == "deferred"
    assert record["migration_disposition"] == "DEFER_FILE"
    assert result["disposition_record"]["sha256"] == calculate_sha256(record_bytes)
    assert disposition_main(make_disposition_arguments(tmp_path, prepared)) == 2
    capsys.readouterr()
    assert (tmp_path / "synthetic/disposition.json").read_bytes() == record_bytes
    assert not tuple((tmp_path / "synthetic").glob(".disposition.json.*"))
    assert (tmp_path / "synthetic/source.md").read_bytes() == source_before
    assert (tmp_path / "synthetic/candidate.json").read_bytes() == candidate_before
    assert not (tmp_path / "synthetic/next-review.md").exists()
