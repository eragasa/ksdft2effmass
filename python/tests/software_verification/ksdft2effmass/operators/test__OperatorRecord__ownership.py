r"""Software verification of ``OperatorRecord``.

Facet and represented meaning
-----------------------------
This class-owned module owns the ownership facet. Represented contract
--------------------
This facet owns defensive matrix/provenance copying, operational matrix
immutability, C-order canonicalization from supported layouts, read-only
provenance exposure, and frozen/slotted outer record state.

Ownership and interpretation
----------------------------
Tests exercise only public arrays, mappings, fields, and ordinary mutation
operations. They do not assert private matrix backing types or array ``.base``
mechanics. The approved public/Sphinx contract is the oracle. Passing establishes
ordinary public-API ownership; failure may indicate implementation,
documentation, or evidence defects, not physical-model invalidity.

VVUQ boundaries
---------------
This module provides software-verification evidence ``SV-OR-032`` through
``SV-OR-037``. No norm, decomposition, Hermiticity analysis, DFT, Wannier,
experiment, or impurity calculation is performed. Numerical verification is not
applicable. Scientific validation, uncertainty quantification, and Rust
conformance have not been performed.

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

from collections.abc import Mapping
from dataclasses import FrozenInstanceError
from typing import Any, cast

import numpy as np
import pytest
from operator_record_fixtures import make_record

from ksdft2effmass.operators import OperatorRecord

pytestmark = pytest.mark.software_verification

SUT = OperatorRecord


def test_field__matrix_is_defensively_owned_from_array_and_view__is_exact() -> None:
    r"""Evidence ID
    SV-OR-032
    Requirement
    Stored matrix values cannot change when caller-owned source storage is later
    mutated.
    Method
    Construct once from a direct array and once from a noncontiguous view, then mutate
    the direct source and the view's underlying base array.
    Oracle
    Literal pre-mutation values define expected represented state.
    Acceptance
    Both stored matrices retain exact original values.
    Interpretation
    Passing establishes defensive matrix ownership for both source forms.
    Limitations
    It does not inspect private backing objects, establish physical validity, scientific
    validation, UQ, or Rust conformance.
    """

    direct = np.array([[1.0, 2.0], [3.0, 4.0]])
    direct_record = make_record(direct)
    base = np.array([[1.0, 9.0, 2.0, 9.0], [3.0, 9.0, 4.0, 9.0]])
    view = base[:, ::2]
    view_record = make_record(view)

    direct[:, :] = -1.0
    base[:, :] = -2.0

    assert direct_record.matrix.tolist() == [[1 + 0j, 2 + 0j], [3 + 0j, 4 + 0j]]
    assert view_record.matrix.tolist() == [[1 + 0j, 2 + 0j], [3 + 0j, 4 + 0j]]


def test_field__matrix_is_operationally_immutable_through_public__is_exact() -> None:
    r"""Evidence ID
    SV-OR-033
    Requirement
    Stored matrices reject ordinary item assignment and ``setflags(write=True)``; a
    reversible flag alone is insufficient.
    Method
    Attempt both public NumPy mutation routes on one valid record.
    Oracle
    NumPy's public read-only mutation taxonomy is ``ValueError``.
    Acceptance
    Both attempts raise exactly ``ValueError`` and values remain unchanged.
    Interpretation
    Passing establishes operational immutability through ordinary public APIs.
    Limitations
    It asserts no private backing type or adversarial memory manipulation and
    establishes no scientific validation, UQ, or Rust conformance.
    """

    record = make_record([[1, 2], [3, 4]])
    expected = record.matrix.copy()

    with pytest.raises(ValueError) as item_exc:
        record.matrix[0, 0] = 99
    assert type(item_exc.value) is ValueError
    with pytest.raises(ValueError) as flags_exc:
        record.matrix.setflags(write=True)
    assert type(flags_exc.value) is ValueError
    assert np.array_equal(record.matrix, expected)


def test_field__represented__non_c_inputs_have_equal_c_contiguous_canonical() -> None:
    r"""Evidence ID
    SV-OR-034
    Requirement
    Approved NumPy layouts produce exact equal C-contiguous, defensively owned record
    matrices.
    Method
    Construct equivalent records from C-order, Fortran-order, and strided view inputs,
    inspect public flags/values, then mutate every source.
    Oracle
    The literal matrix ``[[1, 2], [3, 4]]`` and exact equality define the independent
    expected representation.
    Acceptance
    All records compare equal, values match, all stored arrays are C-order, and
    subsequent source mutation has no effect.
    Interpretation
    Passing establishes deterministic canonical layout across admitted inputs.
    Limitations
    It does not inspect private ``.base`` state, benchmark layout, perform scientific
    validation, UQ, or Rust conformance.
    """

    c_input = np.array([[1.0, 2.0], [3.0, 4.0]], order="C")
    fortran_input = np.array([[1.0, 2.0], [3.0, 4.0]], order="F")
    view_base = np.array([[1.0, 8.0, 2.0, 8.0], [3.0, 8.0, 4.0, 8.0]])
    view_input = view_base[:, ::2]

    c_record = make_record(c_input)
    fortran_record = make_record(fortran_input)
    view_record = make_record(view_input)

    assert all(
        (record.matrix.tolist() == [[1 + 0j, 2 + 0j], [3 + 0j, 4 + 0j]])
        and (record.matrix.flags.c_contiguous)
        and (not record.matrix.flags.writeable)
        for record in (c_record, fortran_record, view_record)
    )
    assert c_record == fortran_record == view_record

    c_input[:, :] = -1
    fortran_input[:, :] = -2
    view_base[:, :] = -3
    assert c_record == fortran_record == view_record


def test_field__provenance_is_defensively_owned_from_mutable_mapping__is_exact() -> (
    None
):
    r"""Evidence ID
    SV-OR-035
    Requirement
    Replacing, adding, or removing caller dictionary entries cannot alter stored
    provenance.
    Method
    Construct from a three-entry dictionary, perform all three mutations, and compare
    exposed content with an independent pre-mutation copy.
    Oracle
    Literal original key/value content defines expected mapping state.
    Acceptance
    Stored provenance remains exactly the original content.
    Interpretation
    Passing establishes defensive provenance ownership.
    Limitations
    It does not validate provenance truth, serialization, scientific validation, UQ, or
    Rust conformance.
    """

    provenance = {"source": "before", "code": "synthetic", "remove": "retained"}
    expected = dict(provenance)
    record = make_record(provenance=provenance)

    provenance["source"] = "after"
    provenance["added"] = "caller only"
    del provenance["remove"]

    assert dict(record.provenance) == expected


def test_field__public_provenance_is_read_only_mapping__is_exact() -> None:
    r"""Evidence ID
    SV-OR-036
    Requirement
    Public provenance satisfies ``Mapping`` and exposes no successful item assignment,
    deletion, or update route.
    Method
    Check the abstract public interface; use ``Any`` only for deliberate invalid
    mutation attempts; inspect update-method absence.
    Oracle
    The approved read-only Mapping contract fixes content and mutation rejection, not a
    concrete implementation type.
    Acceptance
    Mapping membership holds, assignment/deletion raise ``TypeError``, and no public
    ``update`` method is exposed.
    Interpretation
    Passing establishes read-only provenance through ordinary public APIs.
    Limitations
    It does not require ``MappingProxyType``, test serializer behavior, scientific
    validation, UQ, or Rust conformance.
    """

    record = make_record(provenance={"source": "synthetic"})
    provenance = cast(Any, record.provenance)

    assert isinstance(record.provenance, Mapping)
    with pytest.raises(TypeError):
        provenance["source"] = "changed"
    with pytest.raises(TypeError):
        del provenance["source"]
    assert not hasattr(record.provenance, "update")
    assert dict(record.provenance) == {"source": "synthetic"}


@pytest.mark.parametrize(
    ("attribute", "replacement"),
    [
        pytest.param("identifier", "other", id="identifier"),
        pytest.param("operator_kind", "other", id="kind"),
        pytest.param("matrix", np.eye(2), id="matrix"),
        pytest.param("state_space", object(), id="sv_or_037_state_space"),
        pytest.param("basis", object(), id="sv_or_037_basis"),
        pytest.param("geometry", object(), id="sv_or_037_geometry"),
        pytest.param("energy_reference", object(), id="reference"),
        pytest.param("provenance", {}, id="provenance"),
        pytest.param("dynamic", "forbidden", id="sv_or_037_dynamic_attribute"),
    ],
)
def test_field__outer_record_state_is_frozen_and_slotted__is_exact(
    attribute: str,
    replacement: object,
) -> None:
    r"""Evidence ID
    SV-OR-037
    Requirement
    The record is frozen/slotted: fields cannot be reassigned, dynamic state cannot be
    added, and no instance ``__dict__`` exists.
    Method
    Use ordinary ``setattr`` only, without invariant bypasses.
    Oracle
    The approved frozen dataclass contract produces ``FrozenInstanceError``.
    Acceptance
    Every assignment raises exactly ``FrozenInstanceError`` and ``__dict__`` is absent.
    Interpretation
    Passing establishes outer DataObject immutability independently of nested
    matrix/provenance mutation evidence.
    Limitations
    It does not use ``object.__setattr__``, inspect private slots, establish scientific
    validation, UQ, or Rust conformance.
    """

    record = make_record()

    with pytest.raises(FrozenInstanceError) as exc_info:
        setattr(record, attribute, replacement)
    assert type(exc_info.value) is FrozenInstanceError
    assert not hasattr(record, "__dict__")
