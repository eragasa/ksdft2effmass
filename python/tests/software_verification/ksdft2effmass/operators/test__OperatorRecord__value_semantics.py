r"""Software verification of ``OperatorRecord``.

Facet and represented meaning

-----------------------------
This class-owned module owns the value semantics facet. Represented contract
--------------------
This facet owns exact structural equality across all eight stored fields, exact
matrix entry/position semantics, provenance mapping-content equality, unrelated-
object protocol behavior, and public unhashability.

Ownership and interpretation
----------------------------
DataObject equality is stricter than compatibility: identifiers, geometry system,
and provenance still participate even when compatibility analysis ignores them.
No approximate tolerance, compatibility rule, norm, subtraction, or physical-
equivalence policy is used. The approved public/Sphinx contract is the oracle;
failure may indicate implementation, documentation, or evidence defects rather
than scientific invalidity.

VVUQ boundaries
---------------
This module provides software-verification evidence ``SV-OR-038`` through
``SV-OR-042``. Matrix exactness is a software representation contract, not a
numerical algorithm, so numerical verification is not applicable. Scientific
validation, uncertainty quantification, and Rust conformance have not been
performed.

Intrinsic and cross-object scope

--------------------------------
The primary owner is ``OperatorRecord``; collaborators only construct inputs or
expose public outcomes. Accepted public contracts, literal expected values, Python
language semantics, and assigned schema or fixture artifacts provide the oracles. No
runtime warning is accepted unless a test explicitly states otherwise.

VVUQ and scientific exclusions

------------------------------
Passing establishes only the documented software contract and exact or explicitly
bounded acceptance rules. Failure may identify implementation, fixture, oracle,
environment, or contract defects. It does not establish numerical verification,
physical correctness, scientific validation, UQ, portability, or cross-language
agreement.
"""

from collections.abc import Hashable

import numpy as np
import pytest
from operator_record_fixtures import (
    make_basis,
    make_energy_reference,
    make_geometry,
    make_record,
    make_state_space,
)

from ksdft2effmass.operators import OperatorRecord

pytestmark = pytest.mark.software_verification

SUT = OperatorRecord

EQUALITY_FIELDS = (
    "identifier",
    "operator_kind",
    "matrix",
    "state_space",
    "basis",
    "geometry",
    "energy_reference",
    "provenance",
)


def test_method__eq__exact_structural_equality_uses_every_stored_field() -> None:
    r"""Evidence ID: SV-OR-038

    Requirement: Equal independently constructed records match all eight stored fields;
    changing any
    one field makes them unequal.

    Method: Construct one baseline, one identical value, and eight valid single-field
    variants
    through public constructors.

    Oracle: The approved exact DataObject contract includes fields even when
    compatibility rules
    deliberately ignore them.

    Acceptance: Baseline equals the identical record and differs from every variant.

    Interpretation: Passing establishes complete structural equality ownership.

    Limitations: It does not execute compatibility, determine physical equivalence, use
    approximate
    comparison, establish scientific validation, UQ, or Rust conformance.
    """

    baseline = make_record()
    identical = make_record()
    variants = (
        make_record(identifier="other-record"),
        make_record(operator_kind="other_operator_kind"),
        make_record([[1.0, 0.25j], [-0.25j, 3.0]]),
        make_record(
            state_space=make_state_space(dimension=2, identifier="other-space")
        ),
        make_record(basis=make_basis(identifier="other-basis")),
        make_record(geometry=make_geometry(system="other-system")),
        make_record(energy_reference=make_energy_reference(zero="other zero")),
        make_record(provenance={"source": "other"}),
    )

    assert baseline == identical
    assert len(variants) == 8
    assert all(baseline != variant for variant in variants)


def test_method__eq__matrix_equality_is_exact_complex_and_position_sensitive() -> None:
    r"""Evidence ID: SV-OR-039

    Requirement: Matrix equality uses exact entry values and positions, including
    complex components;
    any nonzero representable perturbation is observable.

    Method: Compare zero baseline with a smallest-positive-binary64 perturbation,
    complex
    perturbation, and position-swapped pair without approximation.

    Oracle: Exact literal/IEEE values and positions independently define inequality.

    Acceptance: Every matrix variant compares unequal; independently identical matrices
    compare
    equal.

    Interpretation: Passing establishes ``np.array_equal``-style exact semantics rather
    than
    tolerance-based equality.

    Limitations: It uses no approximate comparison, calculates no error norm, and does
    not determine
    physical equivalence, scientific validation, UQ, or Rust conformance.
    """

    tiny = np.nextafter(0.0, 1.0)
    assert tiny > 0.0
    baseline = make_record([[0.0, 0.0], [0.0, 0.0]])
    identical = make_record([[0.0, 0.0], [0.0, 0.0]])
    tiny_variant = make_record([[tiny, 0.0], [0.0, 0.0]])
    complex_variant = make_record([[1j, 0.0], [0.0, 0.0]])
    positioned = make_record([[0.0, 1.0], [0.0, 0.0]])
    repositioned = make_record([[0.0, 0.0], [1.0, 0.0]])

    assert baseline == identical
    assert baseline != tiny_variant
    assert baseline != complex_variant
    assert positioned != repositioned


def test_method__eq__uses_provenance_content() -> None:
    r"""Evidence ID: SV-OR-040

    Requirement: Equal key/value content compares equal independent of insertion order;
    changed,
    removed, added, or renamed content compares unequal.

    Method: Construct valid records with explicitly authored provenance mappings.

    Oracle: Python mapping-content equality is the approved provenance semantics.

    Acceptance: Reordered content is equal; every content variation is unequal.

    Interpretation: Passing establishes mapping rather than sequence semantics.

    Limitations: It does not validate provenance truth, serialization order, scientific
    validation,
    UQ, or Rust conformance.
    """

    baseline = make_record(provenance={"source": "synthetic", "code": "test"})
    reordered = make_record(provenance={"code": "test", "source": "synthetic"})
    changed_value = make_record(provenance={"source": "different", "code": "test"})
    removed_key = make_record(provenance={"source": "synthetic"})
    added_key = make_record(
        provenance={"source": "synthetic", "code": "test", "extra": "value"}
    )
    changed_key = make_record(provenance={"origin": "synthetic", "code": "test"})

    assert baseline == reordered
    assert baseline != changed_value
    assert baseline != removed_key
    assert baseline != added_key
    assert baseline != changed_key


def test_method__eq__equality_protocol_returns_notimplemented_for_unrelated() -> None:
    r"""Evidence ID: SV-OR-041

    Requirement: Direct ``__eq__`` returns ``NotImplemented`` for unrelated objects and
    ordinary
    comparison yields inequality.

    Method: Compare one valid record with a fresh arbitrary object.

    Oracle: The approved Python data-model protocol defines reflected handling.

    Acceptance: Direct result is exactly ``NotImplemented`` and ordinary equality is
    false while
    inequality is true.

    Interpretation: Passing establishes cooperative equality behavior without duck
    typing.

    Limitations: It does not compare subclasses or establish scientific validation, UQ,
    or Rust
    conformance.
    """

    record = make_record()
    unrelated = object()

    assert record.__eq__(unrelated) is NotImplemented
    assert not (record == unrelated)
    assert record != unrelated


def test_method__hash__operator_record_is_publicly_unhashable() -> None:
    r"""Evidence ID: SV-OR-042

    Requirement: Array-valued exact state has no approved content hash.

    Method: Inspect the public class protocol, abstract Hashable behavior, and ordinary
    ``hash()`` failure.

    Oracle: ``OperatorRecord.__hash__ is None`` is the approved public contract.

    Acceptance: Class hash is ``None``, instance is not ``Hashable``, and ``hash``
    raises exactly
    ``TypeError``.

    Interpretation: Passing prevents accidental matrix/provenance hash introduction.

    Limitations: It does not propose a Rust hash, test identity hashing, establish
    scientific
    validation, UQ, or Rust conformance.
    """

    record = make_record()

    assert OperatorRecord.__hash__ is None
    assert not isinstance(record, Hashable)
    with pytest.raises(TypeError) as exc_info:
        hash(record)
    assert type(exc_info.value) is TypeError
