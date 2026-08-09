r"""Software verification of ``OperatorRecord``.

Facet and represented meaning

-----------------------------
This class-owned module owns the metadata invariants facet. Represented contract
--------------------
This facet owns record identifier/operator-kind string boundaries, exact public
dependency type boundaries, and provenance container/key/value invariants,
including explicit empty-mapping admission.

Ownership and interpretation
----------------------------
Dependency intrinsic invariants remain with StateSpace, Basis, Geometry, and
EnergyReference. Tests use ordinary independently valid dependencies and never
mutate frozen state or call private methods. Compatibility and serializer payload
rules are not executed. The approved public/Sphinx contract is the oracle;
failure may indicate implementation, documentation, or evidence defects rather
than scientific invalidity.

VVUQ boundaries
---------------
This module provides software-verification evidence ``SV-OR-018`` through
``SV-OR-031``. No numerical algorithm, DFT, Wannier, experiment, or impurity
calculation is performed. Numerical verification is not applicable. Scientific
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

from collections.abc import Mapping
from typing import Any, cast

import pytest
from operator_record_fixtures import make_record

from ksdft2effmass.operators import OperatorRecord

pytestmark = pytest.mark.software_verification

SUT = OperatorRecord


@pytest.mark.parametrize(
    "invalid_identifier",
    [
        pytest.param(None, id="none"),
        pytest.param(True, id="sv_or_018_boolean_true"),
        pytest.param(False, id="sv_or_018_boolean_false"),
        pytest.param(1, id="sv_or_018_integer"),
        pytest.param(1.5, id="sv_or_018_float"),
        pytest.param(b"record", id="bytes"),
        pytest.param(object(), id="sv_or_018_arbitrary_object"),
    ],
)
def test_constructor__invalid_identifier_wrong_types_are_rejected__is_enforced(
    invalid_identifier: object,
) -> None:
    r"""Evidence ID: SV-OR-018

    Requirement: ``identifier`` is a Python string and is not created by coercion.

    Method: Keep every other field valid and use ``Any`` only at the invalid public
    boundary.

    Oracle: The approved field contract and wrong-type taxonomy require ``TypeError``.

    Acceptance: Every case raises ``TypeError`` and diagnostic fragments identify the
    record
    identifier and string requirement.

    Interpretation: Passing establishes identifier typing independently of operator
    kind.

    Limitations: It does not judge naming suitability, compatibility, scientific
    validation, UQ, or
    Rust conformance.
    """

    with pytest.raises(TypeError) as exc_info:
        make_record(identifier=cast(Any, invalid_identifier))

    message = str(exc_info.value)
    assert "identifier" in message
    assert "string" in message


def test_constructor__empty_identifier_is_rejected__is_enforced() -> None:
    r"""Evidence ID: SV-OR-019

    Requirement: Record identifier is nonempty and is not normalized before validation.

    Method: Construct with ``identifier=""`` and otherwise valid state.

    Oracle: The approved nonempty invariant requires field-specific ``ValueError``.

    Acceptance: ``ValueError`` identifies identifier and empty value.

    Interpretation: Passing establishes the semantic-type/value taxonomy split.

    Limitations: It does not add vocabulary policy or establish scientific validation,
    UQ, or Rust
    conformance.
    """

    with pytest.raises(ValueError) as exc_info:
        make_record(identifier="")

    message = str(exc_info.value)
    assert "identifier" in message
    assert "must not be empty" in message


@pytest.mark.parametrize(
    "invalid_kind",
    [
        pytest.param(None, id="none"),
        pytest.param(True, id="sv_or_020_boolean_true"),
        pytest.param(False, id="sv_or_020_boolean_false"),
        pytest.param(1, id="sv_or_020_integer"),
        pytest.param(1.5, id="sv_or_020_float"),
        pytest.param(b"kind", id="bytes"),
        pytest.param(object(), id="sv_or_020_arbitrary_object"),
    ],
)
def test_constructor__invalid_operator_kind_wrong_types_are__is_enforced(
    invalid_kind: object,
) -> None:
    r"""Evidence ID: SV-OR-020

    Requirement: ``operator_kind`` is a Python string and is not created by coercion.

    Method: Keep every other field valid and use ``Any`` only at the invalid public
    boundary.

    Oracle: The approved field contract and wrong-type taxonomy require ``TypeError``.

    Acceptance: Every case raises ``TypeError`` and diagnostic fragments identify
    operator kind and
    string requirement.

    Interpretation: Passing establishes kind typing independently of identifier.

    Limitations: It validates no operator vocabulary, physical meaning, scientific
    validation, UQ, or
    Rust conformance.
    """

    with pytest.raises(TypeError) as exc_info:
        make_record(operator_kind=cast(Any, invalid_kind))

    message = str(exc_info.value)
    assert "operator kind" in message
    assert "string" in message


def test_constructor__empty_operator_kind_is_rejected__is_enforced() -> None:
    r"""Evidence ID: SV-OR-021

    Requirement: Operator-kind metadata is nonempty and remains an open exact string.

    Method: Construct with ``operator_kind=""`` and otherwise valid state.

    Oracle: The approved nonempty invariant requires field-specific ``ValueError``.

    Acceptance: ``ValueError`` identifies operator kind and empty value.

    Interpretation: Passing establishes the semantic-type/value taxonomy split.

    Limitations: It adds no enumeration and establishes no scientific validation, UQ, or
    Rust
    conformance.
    """

    with pytest.raises(ValueError) as exc_info:
        make_record(operator_kind="")

    message = str(exc_info.value)
    assert "operator kind" in message
    assert "must not be empty" in message


@pytest.mark.parametrize(
    "invalid_dependency",
    [
        pytest.param(None, id="none"),
        pytest.param("state", id="sv_or_022_string"),
        pytest.param(object(), id="sv_or_022_arbitrary_object"),
    ],
)
def test_constructor__invalid_state_space_objects_are_rejected__is_enforced(
    invalid_dependency: object,
) -> None:
    r"""Evidence ID: SV-OR-022

    Requirement: ``state_space`` is a validated public StateSpace, not duck-typed state.

    Method: Replace only that dependency using ``Any`` at the invalid boundary.

    Oracle: The approved nominal dependency contract requires field-specific
    ``TypeError``.

    Acceptance: Diagnostic fragments identify ``state_space`` and ``StateSpace``.

    Interpretation: Passing establishes the dependency type boundary only.

    Limitations: StateSpace intrinsic invariants, scientific validation, UQ, and Rust
    conformance are
    outside this evidence.
    """

    valid = make_record()
    with pytest.raises(TypeError) as exc_info:
        OperatorRecord(
            valid.identifier,
            valid.operator_kind,
            valid.matrix,
            cast(Any, invalid_dependency),
            valid.basis,
            valid.geometry,
            valid.energy_reference,
            valid.provenance,
        )
    message = str(exc_info.value)
    assert "state_space" in message
    assert "StateSpace" in message


@pytest.mark.parametrize(
    "invalid_dependency",
    [
        pytest.param(None, id="none"),
        pytest.param("basis", id="sv_or_023_string"),
        pytest.param(object(), id="sv_or_023_arbitrary_object"),
    ],
)
def test_constructor__invalid_basis_objects_are_rejected__is_enforced(
    invalid_dependency: object,
) -> None:
    r"""Evidence ID: SV-OR-023

    Requirement: ``basis`` is a validated public Basis, not duck-typed metadata.

    Method: Replace only that dependency using ``Any`` at the invalid boundary.

    Oracle: The approved nominal dependency contract requires field-specific
    ``TypeError``.

    Acceptance: Diagnostic fragments identify ``basis`` and ``Basis``.

    Interpretation: Passing establishes the dependency type boundary only.

    Limitations: Basis intrinsic invariants, scientific validation, UQ, and Rust
    conformance are
    outside this evidence.
    """

    valid = make_record()
    with pytest.raises(TypeError) as exc_info:
        OperatorRecord(
            valid.identifier,
            valid.operator_kind,
            valid.matrix,
            valid.state_space,
            cast(Any, invalid_dependency),
            valid.geometry,
            valid.energy_reference,
            valid.provenance,
        )
    message = str(exc_info.value)
    assert "basis" in message
    assert "Basis" in message


@pytest.mark.parametrize(
    "invalid_dependency",
    [
        pytest.param(None, id="none"),
        pytest.param("geometry", id="sv_or_024_string"),
        pytest.param(object(), id="sv_or_024_arbitrary_object"),
    ],
)
def test_constructor__invalid_geometry_objects_are_rejected__is_enforced(
    invalid_dependency: object,
) -> None:
    r"""Evidence ID: SV-OR-024

    Requirement: ``geometry`` is a validated public Geometry, not duck-typed metadata.

    Method: Replace only that dependency using ``Any`` at the invalid boundary.

    Oracle: The approved nominal dependency contract requires field-specific
    ``TypeError``.

    Acceptance: Diagnostic fragments identify ``geometry`` and ``Geometry``.

    Interpretation: Passing establishes the dependency type boundary only.

    Limitations: Geometry intrinsic/numerical evidence, scientific validation, UQ, and
    Rust
    conformance are outside this evidence.
    """

    valid = make_record()
    with pytest.raises(TypeError) as exc_info:
        OperatorRecord(
            valid.identifier,
            valid.operator_kind,
            valid.matrix,
            valid.state_space,
            valid.basis,
            cast(Any, invalid_dependency),
            valid.energy_reference,
            valid.provenance,
        )
    message = str(exc_info.value)
    assert "geometry" in message
    assert "Geometry" in message


@pytest.mark.parametrize(
    "invalid_dependency",
    [
        pytest.param(None, id="none"),
        pytest.param("reference", id="sv_or_025_string"),
        pytest.param(object(), id="sv_or_025_arbitrary_object"),
    ],
)
def test_constructor__invalid_energy_reference_objects_are__is_enforced(
    invalid_dependency: object,
) -> None:
    r"""Evidence ID: SV-OR-025

    Requirement: ``energy_reference`` is a validated public EnergyReference.

    Method: Replace only that dependency using ``Any`` at the invalid boundary.

    Oracle: The approved nominal dependency contract requires field-specific
    ``TypeError``.

    Acceptance: Diagnostic fragments identify ``energy_reference`` and
    ``EnergyReference``.

    Interpretation: Passing establishes the dependency type boundary only.

    Limitations: EnergyReference intrinsic invariants, scientific validation, UQ, and
    Rust
    conformance are outside this evidence.
    """

    valid = make_record()
    with pytest.raises(TypeError) as exc_info:
        OperatorRecord(
            valid.identifier,
            valid.operator_kind,
            valid.matrix,
            valid.state_space,
            valid.basis,
            valid.geometry,
            cast(Any, invalid_dependency),
            valid.provenance,
        )
    message = str(exc_info.value)
    assert "energy_reference" in message
    assert "EnergyReference" in message


@pytest.mark.parametrize(
    "invalid_provenance",
    [
        pytest.param([("source", "test")], id="sv_or_026_iterable_pairs"),
        pytest.param([], id="list"),
        pytest.param((), id="tuple"),
        pytest.param("source", id="sv_or_026_string"),
        pytest.param(b"source", id="bytes"),
        pytest.param(
            ((key, value) for key, value in (("source", "test"),)),
            id="sv_or_026_generator",
        ),
        pytest.param(object(), id="sv_or_026_arbitrary_object"),
    ],
)
def test_constructor__invalid_provenance_containers_are_rejected__is_enforced(
    invalid_provenance: object,
) -> None:
    r"""Evidence ID: SV-OR-026

    Requirement: Provenance is a ``Mapping``; iterable pairs and other containers are
    not silently
    passed through ``dict()``.

    Method: Pass each invalid object at the deliberate public boundary.

    Oracle: The approved nominal container contract requires ``TypeError``.

    Acceptance: Every diagnostic identifies provenance and mapping semantics.

    Interpretation: Passing establishes strict provenance-container ownership.

    Limitations: Mapping contents are separate evidence; no scientific validation, UQ,
    or Rust
    conformance is established.
    """

    with pytest.raises(TypeError) as exc_info:
        make_record(provenance=cast(Any, invalid_provenance))
    message = str(exc_info.value).lower()
    assert "provenance" in message
    assert "mapping" in message


@pytest.mark.parametrize(
    "invalid_key",
    [
        pytest.param(True, id="sv_or_027_boolean"),
        pytest.param(1, id="sv_or_027_integer"),
        pytest.param(b"source", id="bytes"),
        pytest.param(None, id="none"),
        pytest.param(object(), id="sv_or_027_arbitrary_object"),
    ],
)
def test_constructor__invalid_provenance_key_types_are_rejected__is_enforced(
    invalid_key: object,
) -> None:
    r"""Evidence ID: SV-OR-027

    Requirement: Every provenance key is a Python string without coercion.

    Method: Keep one valid string value and place the invalid object only as key.

    Oracle: The approved mapping-content taxonomy requires ``TypeError``.

    Acceptance: Diagnostic identifies provenance keys/values and strings.

    Interpretation: Passing establishes key typing independently of value typing.

    Limitations: It does not validate provenance truth, scientific validation, UQ, or
    Rust
    conformance.
    """

    provenance = {cast(Any, invalid_key): "test"}
    with pytest.raises(TypeError) as exc_info:
        make_record(provenance=cast(Any, provenance))
    message = str(exc_info.value)
    assert "provenance" in message
    assert "strings" in message


def test_constructor__empty_provenance_key_is_rejected__is_enforced() -> None:
    r"""Evidence ID: SV-OR-028

    Requirement: Every key is nonempty.

    Method: Construct with one empty key and valid value.

    Oracle: The approved content invariant requires ``ValueError``.

    Acceptance: Diagnostic identifies provenance and empty content.

    Interpretation: Passing establishes key value-taxonomy independently.

    Limitations: It establishes no provenance truth, scientific validation, UQ, or Rust
    conformance.
    """

    with pytest.raises(ValueError) as exc_info:
        make_record(provenance={"": "test"})
    message = str(exc_info.value)
    assert "provenance" in message
    assert "must not be empty" in message


@pytest.mark.parametrize(
    "invalid_value",
    [
        pytest.param(True, id="sv_or_029_boolean"),
        pytest.param(1, id="sv_or_029_integer"),
        pytest.param(b"test", id="bytes"),
        pytest.param(None, id="none"),
        pytest.param(object(), id="sv_or_029_arbitrary_object"),
    ],
)
def test_constructor__invalid_provenance_value_types_are_rejected__is_enforced(
    invalid_value: object,
) -> None:
    r"""Evidence ID: SV-OR-029

    Requirement: Every provenance value is a Python string without coercion.

    Method: Keep one valid key and place the invalid object only as value.

    Oracle: The approved mapping-content taxonomy requires ``TypeError``.

    Acceptance: Diagnostic identifies provenance keys/values and strings.

    Interpretation: Passing establishes value typing independently of key typing.

    Limitations: It does not validate provenance truth, scientific validation, UQ, or
    Rust
    conformance.
    """

    provenance = {"source": cast(Any, invalid_value)}
    with pytest.raises(TypeError) as exc_info:
        make_record(provenance=cast(Any, provenance))
    message = str(exc_info.value)
    assert "provenance" in message
    assert "strings" in message


def test_constructor__empty_provenance_value_is_rejected__is_enforced() -> None:
    r"""Evidence ID: SV-OR-030

    Requirement: Every value is nonempty.

    Method: Construct with one valid key and empty value.

    Oracle: The approved content invariant requires ``ValueError``.

    Acceptance: Diagnostic identifies provenance and empty content.

    Interpretation: Passing establishes value taxonomy independently.

    Limitations: It establishes no provenance truth, scientific validation, UQ, or Rust
    conformance.
    """

    with pytest.raises(ValueError) as exc_info:
        make_record(provenance={"source": ""})
    message = str(exc_info.value)
    assert "provenance" in message
    assert "must not be empty" in message


def test_constructor__explicit_empty_provenance_mapping_is__is_enforced() -> None:
    r"""Evidence ID: SV-OR-031

    Requirement: Empty provenance is valid and is not replaced by fixture defaults.

    Method: Supply ``{}`` explicitly through a helper that distinguishes ``None`` from
    empty
    mappings using ``is None``.

    Oracle: The approved Mapping contract imposes entry invariants but no nonempty
    container
    invariant.

    Acceptance: Construction succeeds and exposed provenance remains empty.

    Interpretation: Passing establishes empty-mapping admission and fixture
    transparency.

    Limitations: Absence of provenance does not establish reproducibility, scientific
    validation, UQ,
    or Rust conformance.
    """

    provenance: Mapping[str, str] = {}
    record = make_record(provenance=provenance)

    assert dict(record.provenance) == {}
    assert len(record.provenance) == 0
