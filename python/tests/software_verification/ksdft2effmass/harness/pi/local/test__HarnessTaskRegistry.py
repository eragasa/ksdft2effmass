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

from ksdft2effmass.harness import HarnessTask, HarnessTaskRegistry

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


def test_method__descendant_task_ids__returns_depth_first_proper_descendants() -> None:
    """Evidence ID: SV-HT-115

    Requirement: Recursive descendant lookup derives one exact proper subtree from
    canonical parent fields in deterministic depth-first pre-order.

    Method: Register one root, two direct children, and two grandchildren under the
    first child, then query the root and a leaf.

    Oracle: The supplied ``parent_task_id`` fields independently define the tree; the
    public registry contract fixes direct-child registry order and parent-before-child
    depth-first traversal.

    Acceptance: The root query returns ``("b", "c", "d", "e")`` and the leaf query
    returns an empty tuple without including either queried root.

    Interpretation: Failure identifies missing, duplicated, reordered, or improperly
    root-inclusive descendant derivation.

    Limitations: The query establishes no planning authorization or execution order.
    """
    root = make_task(task_id="a", documentation_path="docs/a.md")
    first = make_task(
        task_id="b", parent_task_id="a", documentation_path="docs/b.md"
    )
    first_child = make_task(
        task_id="c", parent_task_id="b", documentation_path="docs/c.md"
    )
    second_child = make_task(
        task_id="d", parent_task_id="b", documentation_path="docs/d.md"
    )
    second = make_task(
        task_id="e", parent_task_id="a", documentation_path="docs/e.md"
    )
    registry = SUT(1, (root, first, first_child, second_child, second))

    assert registry.descendant_task_ids("a") == ("b", "c", "d", "e")
    assert registry.descendant_task_ids("c") == ()


def test_method__descendant_task_ids__fails_closed_and_supports_deep_trees() -> None:
    """Evidence ID: SV-HT-116

    Requirement: Descendant lookup rejects invalid or unknown roots and reachable
    parent cycles while traversing valid deep trees without recursion-depth failure.

    Method: Query wrong-type and unknown roots, a three-Task reachable cycle, and a
    1,100-edge synthetic parent chain.

    Oracle: Public identifier semantics define input failures; canonical parent edges
    define the cycle and exact deep-chain descendants independently of implementation.

    Acceptance: Wrong types raise ``TypeError``; unknown roots and cycles raise
    ``ValueError``; the deep query returns every non-root identity in parent order.

    Interpretation: Failure identifies coercion, silent cycle truncation, looping, or
    recursion-depth coupling.

    Limitations: Complete graph validation remains owned by
    ``HarnessTaskGraphValidator``.
    """
    singleton = SUT(1, (make_task(task_id="known"),))
    with pytest.raises(TypeError):
        singleton.descendant_task_ids(1)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="unknown task_id"):
        singleton.descendant_task_ids("missing")

    cycle = SUT(
        1,
        (
            make_task(task_id="a", parent_task_id="c"),
            make_task(task_id="b", parent_task_id="a"),
            make_task(task_id="c", parent_task_id="b"),
        ),
    )
    with pytest.raises(ValueError, match="cycle"):
        cycle.descendant_task_ids("a")

    task_ids = tuple(f"task.{index:04d}" for index in range(1101))
    tasks = tuple(
        make_task(
            task_id=task_id,
            parent_task_id=None if index == 0 else task_ids[index - 1],
            documentation_path=f"docs/{index:04d}.md",
        )
        for index, task_id in enumerate(task_ids)
    )
    assert SUT(1, tasks).descendant_task_ids(task_ids[0]) == task_ids[1:]
