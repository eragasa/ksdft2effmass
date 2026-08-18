r"""Software verification of ``HarnessTaskRegistry``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module verifies the immutable in-memory registry derived from canonical
``HarnessTask`` values.

Intrinsic and cross-object scope

The sole primary SUT is ``HarnessTaskRegistry``. Intrinsic ordering, uniqueness,
lookup, and derived relationship behavior are covered. Cross-Task missing-reference
and cycle policy remains owned by ``HarnessTaskGraphValidator``.

VVUQ and scientific exclusions

Passing establishes exact software-contract behavior only. It does not establish
Task activation, authority, scientific workflow state, or human acceptance.
"""

import pytest

from ksdft2effmass.harness.pi.local import HarnessTask, HarnessTaskRegistry

from .task_model_examples import make_task

pytestmark = pytest.mark.software_verification
SUT = HarnessTaskRegistry


def test_constructor__tasks__retains_identity_sorted_values() -> None:
    """Evidence ID: SV-HT-100

    Requirement: A registry contains one nonempty Task-ID-sorted unique tuple and
    derives its identity index from those exact Tasks.

    Method: Construct two independently valid synthetic Tasks and one registry.

    Oracle: The public registry contract fixes exact tuple retention and identity
    ordering.

    Acceptance: Stored Tasks retain identity and ``task_ids`` equals ``("a", "b")``.

    Interpretation: Failure identifies registry construction or identity-index drift.

    Limitations: Synthetic Tasks establish no repository membership or activation.
    """
    first = make_task(task_id="a", documentation_path="docs/a.md")
    second = make_task(task_id="b", documentation_path="docs/b.md")
    registry = SUT(1, (first, second))
    assert registry.tasks == (first, second)
    assert registry.task_ids == ("a", "b")


def test_constructor__tasks__rejects_invalid_collections() -> None:
    """Evidence ID: SV-HT-101

    Requirement: Registry construction rejects empty, non-tuple, wrong-member,
    duplicate, and noncanonical Task order partitions.

    Method: Construct each invalid partition directly.

    Oracle: The DataObject contract independently fixes semantic types, nonemptiness,
    uniqueness, and Task-ID order.

    Acceptance: Wrong semantic types raise ``TypeError`` and value invariants raise
    ``ValueError``.

    Interpretation: Failure identifies an intrinsic registry invariant gap.

    Limitations: Graph reference and cycle findings belong to the graph validator.
    """
    first = make_task(task_id="a", documentation_path="docs/a.md")
    second = make_task(task_id="b", documentation_path="docs/b.md")
    with pytest.raises(ValueError, match="nonempty"):
        SUT(1, ())
    with pytest.raises(TypeError, match="tuple"):
        SUT(1, [first])  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="HarnessTask"):
        SUT(1, (object(),))  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="unique and sorted"):
        SUT(1, (first, first))
    with pytest.raises(ValueError, match="unique and sorted"):
        SUT(1, (second, first))


def test_method__task_by_id__returns_exact_task_and_rejects_unknown_identity() -> None:
    """Evidence ID: SV-HT-102

    Requirement: Deterministic identity lookup returns the exact registered object and
    fails closed for invalid or unknown identities.

    Method: Look up one member, an unknown valid identifier, and a wrong semantic type.

    Oracle: The registry's public identity-lookup contract is exact.

    Acceptance: Known lookup preserves object identity; unknown and wrong-type inputs
    raise ``ValueError`` and ``TypeError`` respectively.

    Interpretation: Failure identifies lookup ambiguity or coercion.

    Limitations: Lookup success grants no Task selection or authority.
    """
    task = make_task(task_id="registered.task")
    registry = SUT(1, (task,))
    assert registry.task_by_id("registered.task") is task
    with pytest.raises(ValueError, match="unknown task_id"):
        registry.task_by_id("missing.task")
    with pytest.raises(TypeError):
        registry.task_by_id(1)  # type: ignore[arg-type]


def test_method__relationship_lookup__derives_children_and_prerequisites() -> None:
    """Evidence ID: SV-HT-103

    Requirement: Child and prerequisite lookup derive solely from canonical Task
    fields without a stored child list.

    Method: Register one parent and two children with distinct prerequisite tuples.

    Oracle: ``parent_task_id`` and ``task_prerequisite_ids`` on the supplied Tasks are
    the independent graph-edge sources.

    Acceptance: Child identities are sorted by registry order and prerequisite lookup
    equals the exact canonical tuple.

    Interpretation: Failure identifies duplicated or incorrectly derived topology.

    Limitations: Structural graph validity remains a separate validator result.
    """
    parent = make_task(task_id="a.parent", documentation_path="docs/parent.md")
    first = make_task(
        task_id="b.child",
        parent_task_id=parent.task_id,
        task_prerequisite_ids=(parent.task_id,),
        documentation_path="docs/first.md",
    )
    second = make_task(
        task_id="c.child",
        parent_task_id=parent.task_id,
        documentation_path="docs/second.md",
    )
    registry = SUT(1, (parent, first, second))
    assert registry.child_task_ids(parent.task_id) == (first.task_id, second.task_id)
    assert registry.prerequisite_task_ids(first.task_id) == (parent.task_id,)
    assert registry.prerequisite_task_ids(second.task_id) == ()
    assert all(type(task) is HarnessTask for task in registry.tasks)
