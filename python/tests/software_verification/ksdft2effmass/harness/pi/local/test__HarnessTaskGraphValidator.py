r"""Software verification of ``HarnessTaskGraphValidator``.

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

from ksdft2effmass.harness.pi.local import HarnessTaskGraphValidator

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
