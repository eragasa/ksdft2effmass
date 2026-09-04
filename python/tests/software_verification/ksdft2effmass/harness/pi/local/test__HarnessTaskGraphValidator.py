r"""Software verification of ``HarnessTaskGraphValidator``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

Software verification of one accepted project-local HarnessTask surface.

Intrinsic and cross-object scope

The sole primary SUT is ``HarnessTaskGraphValidator``.
Artifact-owned evidence covers detailed cross-object algorithms.

VVUQ and scientific exclusions

Passing establishes software-interface behavior only. It does not establish a
migration, activation, scientific validity, or human acceptance.
"""

import pytest

from ksdft2effmass.harness.pi.local.task_model import (
    _LocalHarnessTaskGraphValidator as HarnessTaskGraphValidator,
)

from .task_model_examples import make_task

pytestmark = pytest.mark.software_verification
SUT = HarnessTaskGraphValidator


def test_constructor__public_stereotype__has_exact_runtime_identity() -> None:
    """Evidence ID: ``SV-HT-004``.

    Requirement: The public ActionObject is fieldless, stateless, and can be
    constructed directly.

    Method: Construct or enumerate the public SUT using explicit synthetic support
    input.

    Oracle: The accepted 19-interface table supplies the expected name and stereotype.

    Acceptance: Runtime identity, fieldlessness, fields, or closed values match exactly.

    Interpretation: Failure identifies public API, stereotype, or value-semantics drift.

    Limitations: Detailed algorithms are asserted by focused artifact-owned evidence.
    """
    assert SUT.__slots__ == ()
    assert type(SUT()) is SUT


def test_method__execute__rejects_empty_graph() -> None:
    """Evidence ID: ``SV-HT-036``.

    Requirement: Graph validation requires one exact nonempty Task tuple.

    Method: Exercise independently invalid partitions against explicit synthetic input.

    Oracle: The accepted public constructor or ActionObject contract defines exact
    outcomes.

    Acceptance: Valid input remains exact and every specified invalid partition
    fails closed.

    Interpretation: Failure identifies intrinsic or cross-object contract drift.

    Limitations: Software verification does not authorize migration or human acceptance.
    """
    with pytest.raises(ValueError, match="nonempty"):
        SUT().execute(())
    with pytest.raises(TypeError):
        SUT().execute([])  # type: ignore[arg-type]


def test_method__execute__reports_duplicate_task_identity() -> None:
    """Evidence ID: ``SV-HT-114``.

    Requirement: Graph validation reports duplicate Task identities before registry
    construction can establish a unique index.

    Method: Supply the same independently valid Task twice to the existing validator.

    Oracle: The graph-validation contract fixes ``PIHL.TASK.DUPLICATE_ID`` as the
    cross-object duplicate finding.

    Acceptance: Validation fails with exactly one duplicate-ID issue.

    Interpretation: Failure identifies lost duplicate detection at the validation
    boundary.

    Limitations: The finding grants no authority and does not construct a registry.
    """
    first = make_task(
        task_id="duplicate.task",
        intake_path="records/first.md",
        documentation_path="docs/first.md",
    )
    second = make_task(
        task_id="duplicate.task",
        intake_path="records/second.md",
        documentation_path="docs/second.md",
    )
    result = SUT().execute((first, second))
    assert tuple((issue.code, issue.detail) for issue in result.issues) == (
        ("PIHL.TASK.DUPLICATE_ID", first.task_id),
    )


def test_method__execute__accepts_valid_supersession_and_absent_intake_paths() -> None:
    """Evidence ID: ``SV-HT-039``.

    Requirement: A replacement reference may identify another supplied Task, and
    absent intake paths do not collide.

    Method: Validate one superseded Task and its replacement with null intake and
    distinct documentation paths.

    Oracle: The version-3 graph contract treats supersession as a checked identity
    relation and ``None`` as no resource.

    Acceptance: Graph validation returns exact PASS with no issues.

    Interpretation: Failure identifies optional-intake graph handling drift.

    Limitations: The synthetic graph establishes no lifecycle or repository claims.
    """
    first = make_task(
        task_id="a",
        superseded_by_task_ids=("b",),
        intake_path=None,
        documentation_path="docs/a.md",
    )
    second = make_task(task_id="b", intake_path=None, documentation_path="docs/b.md")
    result = SUT().execute((first, second))
    assert result.status == "PASS"
    assert result.issues == ()
