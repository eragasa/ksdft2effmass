r"""Software verification of ``StateSpace``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

-----------------------------
This class-owned module owns the construction facet. This module owns public
construction, exact field mapping, accepted dimension
scalar canonicalization, arbitrary positive structural dimensions, exact string
preservation, and standalone-serialization exclusion. ``StateSpace`` represents
finite metadata for :math:`\dim\mathcal H=N` through
``state_space.dimension == N``. It stores exactly ``identifier``, ``kind``, and
``dimension``.

The DataObject validates its own metadata and canonicalizes admitted Python and
NumPy integer scalars to built-in ``int``. It allocates no basis, vector, or
matrix and imposes no dimension cap. Matrix-dimension and basis-order agreement
belong to ``OperatorRecord``. The approved architecture and Sphinx contract are
the oracle. Passing establishes only the documented construction contract;
failure may indicate an implementation regression, documentation mismatch, or
evidence defect.

This module provides software-verification evidence ``SV-SS-001`` through
``SV-SS-005``. It establishes no physical Hilbert space, basis completeness,
operator-domain correctness, matrix compatibility, DFT or Wannier validity,
scientific validation, uncertainty quantification, or Rust conformance.

Intrinsic and cross-object scope

--------------------------------
The primary owner is ``StateSpace``; collaborators only construct inputs or expose
public outcomes. Accepted public contracts, literal expected values, Python language
semantics, and assigned schema or fixture artifacts provide the oracles. No runtime
warning is accepted unless a test explicitly states otherwise.

VVUQ and scientific exclusions

------------------------------
Passing establishes only the documented software contract and exact or explicitly
bounded acceptance rules. Failure may identify implementation, fixture, oracle,
environment, or contract defects. It does not establish numerical verification,
physical correctness, scientific validation, UQ, portability, or cross-language
agreement.
"""

import numpy as np
import pytest

from ksdft2effmass.operators import StateSpace

pytestmark = pytest.mark.software_verification

SUT = StateSpace


def make_state_space(
    *,
    identifier: str = "two-level",
    kind: str = "finite synthetic",
    dimension: int = 2,
) -> StateSpace:
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: Valid fixtures use explicit typed fields and pass them unchanged to the
    public
    constructor.

    Method: Construct ``StateSpace`` with the supplied metadata.

    Oracle: The approved public contract defines the three constructor roles and
    object-owned
    canonicalization.

    Acceptance: A valid public ``StateSpace`` is returned.

    Interpretation: The helper provides synthetic metadata without hidden coercion.

    Limitations: It performs no basis construction, allocates no vector or matrix
    storage, and
    establishes no physical or scientific validity, scientific validation, uncertainty
    quantification, or Rust conformance.
    """

    return StateSpace(identifier=identifier, kind=kind, dimension=dimension)


def test_constructor__public_fields_are_mapped_exactly__is_enforced() -> None:
    r"""Evidence ID: SV-SS-001

    Requirement: Public construction stores exactly supplied identifier, kind, and
    positive dimension
    values in their declared roles and built-in types.

    Method: Construct through ``ksdft2effmass.operators.StateSpace`` using distinct
    valid
    synthetic values and inspect the public fields.

    Oracle: The approved three-field DataObject contract defines mapping and stored
    built-in
    types independently of source location.

    Acceptance: All values match exactly and types are exactly ``str``, ``str``, and
    ``int``.

    Interpretation: Passing establishes supported construction and stored-field mapping.

    Limitations: It does not establish basis or matrix compatibility, physical meaning,
    scientific
    validation, uncertainty quantification, or Rust conformance.
    """

    state_space = StateSpace(
        identifier="two-level",
        kind="finite synthetic",
        dimension=2,
    )

    assert state_space.identifier == "two-level"
    assert state_space.kind == "finite synthetic"
    assert state_space.dimension == 2
    assert type(state_space.identifier) is str
    assert type(state_space.kind) is str
    assert type(state_space.dimension) is int


@pytest.mark.parametrize(
    "dimension",
    [
        pytest.param(1, id="sv_ss_002_python_integer"),
        pytest.param(np.int32(2), id="sv_ss_002_numpy_int32"),
        pytest.param(np.int64(2), id="sv_ss_002_numpy_int64"),
    ],
)
def test_constructor__accepted_dimension_scalars_canonicalize_to__is_enforced(
    dimension: int | np.integer,
) -> None:
    r"""Evidence ID: SV-SS-002

    Requirement: Python and NumPy integer scalars are admitted with value preservation
    and canonical
    built-in ``int`` storage; positive one is valid.

    Method: Construct independently with each representative scalar.

    Oracle: The approved runtime and typing contracts admit these integer families and
    require
    canonical stored ``int`` state.

    Acceptance: Stored dimension equals ``int(dimension)`` and has exact type ``int``.

    Interpretation: Passing synchronizes runtime admission, value preservation, and
    stored type across
    representative widths.

    Limitations: It does not approve Boolean semantics or every third-party integer-like
    protocol and
    establishes no numerical or scientific validation, UQ, or Rust conformance.
    """

    state_space = StateSpace(
        identifier="two-level",
        kind="finite synthetic",
        dimension=dimension,
    )

    assert state_space.dimension == int(dimension)
    assert type(state_space.dimension) is int


def test_field__arbitrary_positive_structural_dimension_has_no__is_exact() -> None:
    r"""Evidence ID: SV-SS-003

    Requirement: ``StateSpace`` imposes positivity only, with no approved maximum
    dimension or
    allocation policy.

    Method: Construct synthetic metadata with the Python integer ``10**1000``.

    Oracle: The intrinsic contract treats dimension as structural metadata; matrix and
    basis
    constraints remain separate ``OperatorRecord`` invariants.

    Acceptance: The arbitrary-precision value is preserved exactly as built-in ``int``.

    Interpretation: Passing establishes that construction itself adds no dimension cap
    or vector/matrix
    allocation.

    Limitations: It does not promise that an ``OperatorRecord`` matrix of this dimension
    can be
    allocated or processed and establishes no scientific validation, UQ, or Rust
    conformance.
    """

    dimension = 10**1000
    state_space = make_state_space(dimension=dimension)

    assert state_space.dimension == dimension
    assert type(state_space.dimension) is int


def test_field__represented_state__valid_strings_are_preserved_exactly_without() -> (
    None
):
    r"""Evidence ID: SV-SS-004

    Requirement: Valid nonempty identifier and kind metadata are stored without
    stripping, case
    folding, slug conversion, Unicode normalization, or enumeration.

    Method: Construct with mixed-case nonempty strings and compare exact values.

    Oracle: The approved metadata contract requires exact preservation and no
    normalization
    policy.

    Acceptance: Both stored strings equal their inputs exactly.

    Interpretation: Passing establishes preservation of these valid descriptive strings.

    Limitations: It does not approve every possible semantic label or whitespace-only
    metadata and
    establishes no physical validity, scientific validation, UQ, or Rust conformance.
    """

    identifier = "State-Space-A"
    kind = "Finite Synthetic"
    state_space = make_state_space(identifier=identifier, kind=kind)

    assert state_space.identifier == identifier
    assert state_space.kind == kind


def test_method__serialize__state_space_has_no_standalone_serialization_api() -> None:
    r"""Evidence ID: SV-SS-005

    Requirement: Neither instance nor class exposes the six unapproved standalone JSON,
    dictionary,
    serializer, or deserializer method names.

    Method: Inspect a valid instance and the public class for each excluded name.

    Oracle: Schema version 1 assigns nested state-space serialization exclusively to
    ``OperatorRecordJsonSerializer`` and approves no independent wire format.

    Acceptance: Every excluded method is absent from instance and class.

    Interpretation: Passing establishes the current nested-only serialization boundary.

    Limitations: Pickling and future approved schemas are unspecified. No record round
    trip,
    scientific validation, uncertainty quantification, or Rust conformance is
    established.
    """

    state_space = make_state_space()

    assert all(
        (not hasattr(state_space, method_name))
        and (not hasattr(StateSpace, method_name))
        for method_name in (
            "to_json",
            "to_dict",
            "serialize",
            "from_json",
            "from_dict",
            "deserialize",
        )
    )
