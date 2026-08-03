"""Software verification of ``OperatorRecord`` metadata invariants.

Represented contract
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
"""

from collections.abc import Mapping
from typing import Any, cast

import pytest
from operator_record_fixtures import make_record

from ksdft2effmass.operators import OperatorRecord

pytestmark = pytest.mark.software_verification


@pytest.mark.parametrize(
    "invalid_identifier",
    [
        pytest.param(None, id="SV-OR-018-none"),
        pytest.param(True, id="SV-OR-018-boolean-true"),
        pytest.param(False, id="SV-OR-018-boolean-false"),
        pytest.param(1, id="SV-OR-018-integer"),
        pytest.param(1.5, id="SV-OR-018-float"),
        pytest.param(b"record", id="SV-OR-018-bytes"),
        pytest.param(object(), id="SV-OR-018-arbitrary-object"),
    ],
)
def test_invalid_identifier_semantic_types_are_rejected(
    invalid_identifier: object,
) -> None:
    """SV-OR-018: require record-identifier string semantics independently.

    Evidence ID
        ``SV-OR-018``; IDs identify representative wrong types.
    Requirement
        ``identifier`` is a Python string and is not created by coercion.
    Method
        Keep every other field valid and use ``Any`` only at the invalid public
        boundary.
    Oracle
        The approved field contract and wrong-type taxonomy require ``TypeError``.
    Acceptance
        Every case raises ``TypeError`` and diagnostic fragments identify the
        record identifier and string requirement.
    Interpretation
        Passing establishes identifier typing independently of operator kind.
    Limitations
        It does not judge naming suitability, compatibility, scientific
        validation, UQ, or Rust conformance.
    """

    with pytest.raises(TypeError) as exc_info:
        make_record(identifier=cast(Any, invalid_identifier))

    message = str(exc_info.value)
    assert "identifier" in message
    assert "string" in message


def test_empty_identifier_is_rejected() -> None:
    """SV-OR-019: reject the correctly typed empty identifier.

    Evidence ID
        ``SV-OR-019``.
    Requirement
        Record identifier is nonempty and is not normalized before validation.
    Method
        Construct with ``identifier=""`` and otherwise valid state.
    Oracle
        The approved nonempty invariant requires field-specific ``ValueError``.
    Acceptance
        ``ValueError`` identifies identifier and empty value.
    Interpretation
        Passing establishes the semantic-type/value taxonomy split.
    Limitations
        It does not add vocabulary policy or establish scientific validation,
        UQ, or Rust conformance.
    """

    with pytest.raises(ValueError) as exc_info:
        make_record(identifier="")

    message = str(exc_info.value)
    assert "identifier" in message
    assert "must not be empty" in message


@pytest.mark.parametrize(
    "invalid_kind",
    [
        pytest.param(None, id="SV-OR-020-none"),
        pytest.param(True, id="SV-OR-020-boolean-true"),
        pytest.param(False, id="SV-OR-020-boolean-false"),
        pytest.param(1, id="SV-OR-020-integer"),
        pytest.param(1.5, id="SV-OR-020-float"),
        pytest.param(b"kind", id="SV-OR-020-bytes"),
        pytest.param(object(), id="SV-OR-020-arbitrary-object"),
    ],
)
def test_invalid_operator_kind_semantic_types_are_rejected(
    invalid_kind: object,
) -> None:
    """SV-OR-020: require operator-kind string semantics independently.

    Evidence ID
        ``SV-OR-020``; IDs identify representative wrong types.
    Requirement
        ``operator_kind`` is a Python string and is not created by coercion.
    Method
        Keep every other field valid and use ``Any`` only at the invalid public
        boundary.
    Oracle
        The approved field contract and wrong-type taxonomy require ``TypeError``.
    Acceptance
        Every case raises ``TypeError`` and diagnostic fragments identify
        operator kind and string requirement.
    Interpretation
        Passing establishes kind typing independently of identifier.
    Limitations
        It validates no operator vocabulary, physical meaning, scientific
        validation, UQ, or Rust conformance.
    """

    with pytest.raises(TypeError) as exc_info:
        make_record(operator_kind=cast(Any, invalid_kind))

    message = str(exc_info.value)
    assert "operator kind" in message
    assert "string" in message


def test_empty_operator_kind_is_rejected() -> None:
    """SV-OR-021: reject the correctly typed empty operator kind.

    Evidence ID
        ``SV-OR-021``.
    Requirement
        Operator-kind metadata is nonempty and remains an open exact string.
    Method
        Construct with ``operator_kind=""`` and otherwise valid state.
    Oracle
        The approved nonempty invariant requires field-specific ``ValueError``.
    Acceptance
        ``ValueError`` identifies operator kind and empty value.
    Interpretation
        Passing establishes the semantic-type/value taxonomy split.
    Limitations
        It adds no enumeration and establishes no scientific validation, UQ, or
        Rust conformance.
    """

    with pytest.raises(ValueError) as exc_info:
        make_record(operator_kind="")

    message = str(exc_info.value)
    assert "operator kind" in message
    assert "must not be empty" in message


@pytest.mark.parametrize(
    "invalid_dependency",
    [
        pytest.param(None, id="SV-OR-022-none"),
        pytest.param("state", id="SV-OR-022-string"),
        pytest.param(object(), id="SV-OR-022-arbitrary-object"),
    ],
)
def test_invalid_state_space_objects_are_rejected(invalid_dependency: object) -> None:
    """SV-OR-022: require an actual StateSpace dependency.

    Evidence ID
        ``SV-OR-022``; IDs identify representative wrong dependency types.
    Requirement
        ``state_space`` is a validated public StateSpace, not duck-typed state.
    Method
        Replace only that dependency using ``Any`` at the invalid boundary.
    Oracle
        The approved nominal dependency contract requires field-specific
        ``TypeError``.
    Acceptance
        Diagnostic fragments identify ``state_space`` and ``StateSpace``.
    Interpretation
        Passing establishes the dependency type boundary only.
    Limitations
        StateSpace intrinsic invariants, scientific validation, UQ, and Rust
        conformance are outside this evidence.
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
        pytest.param(None, id="SV-OR-023-none"),
        pytest.param("basis", id="SV-OR-023-string"),
        pytest.param(object(), id="SV-OR-023-arbitrary-object"),
    ],
)
def test_invalid_basis_objects_are_rejected(invalid_dependency: object) -> None:
    """SV-OR-023: require an actual Basis dependency.

    Evidence ID
        ``SV-OR-023``; IDs identify representative wrong dependency types.
    Requirement
        ``basis`` is a validated public Basis, not duck-typed metadata.
    Method
        Replace only that dependency using ``Any`` at the invalid boundary.
    Oracle
        The approved nominal dependency contract requires field-specific
        ``TypeError``.
    Acceptance
        Diagnostic fragments identify ``basis`` and ``Basis``.
    Interpretation
        Passing establishes the dependency type boundary only.
    Limitations
        Basis intrinsic invariants, scientific validation, UQ, and Rust
        conformance are outside this evidence.
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
        pytest.param(None, id="SV-OR-024-none"),
        pytest.param("geometry", id="SV-OR-024-string"),
        pytest.param(object(), id="SV-OR-024-arbitrary-object"),
    ],
)
def test_invalid_geometry_objects_are_rejected(invalid_dependency: object) -> None:
    """SV-OR-024: require an actual Geometry dependency.

    Evidence ID
        ``SV-OR-024``; IDs identify representative wrong dependency types.
    Requirement
        ``geometry`` is a validated public Geometry, not duck-typed metadata.
    Method
        Replace only that dependency using ``Any`` at the invalid boundary.
    Oracle
        The approved nominal dependency contract requires field-specific
        ``TypeError``.
    Acceptance
        Diagnostic fragments identify ``geometry`` and ``Geometry``.
    Interpretation
        Passing establishes the dependency type boundary only.
    Limitations
        Geometry intrinsic/numerical evidence, scientific validation, UQ, and
        Rust conformance are outside this evidence.
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
        pytest.param(None, id="SV-OR-025-none"),
        pytest.param("reference", id="SV-OR-025-string"),
        pytest.param(object(), id="SV-OR-025-arbitrary-object"),
    ],
)
def test_invalid_energy_reference_objects_are_rejected(
    invalid_dependency: object,
) -> None:
    """SV-OR-025: require an actual EnergyReference dependency.

    Evidence ID
        ``SV-OR-025``; IDs identify representative wrong dependency types.
    Requirement
        ``energy_reference`` is a validated public EnergyReference.
    Method
        Replace only that dependency using ``Any`` at the invalid boundary.
    Oracle
        The approved nominal dependency contract requires field-specific
        ``TypeError``.
    Acceptance
        Diagnostic fragments identify ``energy_reference`` and
        ``EnergyReference``.
    Interpretation
        Passing establishes the dependency type boundary only.
    Limitations
        EnergyReference intrinsic invariants, scientific validation, UQ, and
        Rust conformance are outside this evidence.
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
        pytest.param([("source", "test")], id="SV-OR-026-iterable-pairs"),
        pytest.param([], id="SV-OR-026-list"),
        pytest.param((), id="SV-OR-026-tuple"),
        pytest.param("source", id="SV-OR-026-string"),
        pytest.param(b"source", id="SV-OR-026-bytes"),
        pytest.param(
            ((key, value) for key, value in (("source", "test"),)),
            id="SV-OR-026-generator",
        ),
        pytest.param(object(), id="SV-OR-026-arbitrary-object"),
    ],
)
def test_invalid_provenance_containers_are_rejected(
    invalid_provenance: object,
) -> None:
    """SV-OR-026: require Mapping provenance without iterable coercion.

    Evidence ID
        ``SV-OR-026``; IDs identify non-Mapping container families.
    Requirement
        Provenance is a ``Mapping``; iterable pairs and other containers are not
        silently passed through ``dict()``.
    Method
        Pass each invalid object at the deliberate public boundary.
    Oracle
        The approved nominal container contract requires ``TypeError``.
    Acceptance
        Every diagnostic identifies provenance and mapping semantics.
    Interpretation
        Passing establishes strict provenance-container ownership.
    Limitations
        Mapping contents are separate evidence; no scientific validation, UQ, or
        Rust conformance is established.
    """

    with pytest.raises(TypeError) as exc_info:
        make_record(provenance=cast(Any, invalid_provenance))
    message = str(exc_info.value).lower()
    assert "provenance" in message
    assert "mapping" in message


@pytest.mark.parametrize(
    "invalid_key",
    [
        pytest.param(True, id="SV-OR-027-boolean"),
        pytest.param(1, id="SV-OR-027-integer"),
        pytest.param(b"source", id="SV-OR-027-bytes"),
        pytest.param(None, id="SV-OR-027-none"),
        pytest.param(object(), id="SV-OR-027-arbitrary-object"),
    ],
)
def test_invalid_provenance_key_types_are_rejected(invalid_key: object) -> None:
    """SV-OR-027: require provenance key string semantics independently.

    Evidence ID
        ``SV-OR-027``; IDs identify wrong key families.
    Requirement
        Every provenance key is a Python string without coercion.
    Method
        Keep one valid string value and place the invalid object only as key.
    Oracle
        The approved mapping-content taxonomy requires ``TypeError``.
    Acceptance
        Diagnostic identifies provenance keys/values and strings.
    Interpretation
        Passing establishes key typing independently of value typing.
    Limitations
        It does not validate provenance truth, scientific validation, UQ, or Rust
        conformance.
    """

    provenance = {cast(Any, invalid_key): "test"}
    with pytest.raises(TypeError) as exc_info:
        make_record(provenance=cast(Any, provenance))
    message = str(exc_info.value)
    assert "provenance" in message
    assert "strings" in message


def test_empty_provenance_key_is_rejected() -> None:
    """SV-OR-028: reject the correctly typed empty provenance key.

    Evidence ID
        ``SV-OR-028``.
    Requirement
        Every key is nonempty.
    Method
        Construct with one empty key and valid value.
    Oracle
        The approved content invariant requires ``ValueError``.
    Acceptance
        Diagnostic identifies provenance and empty content.
    Interpretation
        Passing establishes key value-taxonomy independently.
    Limitations
        It establishes no provenance truth, scientific validation, UQ, or Rust
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
        pytest.param(True, id="SV-OR-029-boolean"),
        pytest.param(1, id="SV-OR-029-integer"),
        pytest.param(b"test", id="SV-OR-029-bytes"),
        pytest.param(None, id="SV-OR-029-none"),
        pytest.param(object(), id="SV-OR-029-arbitrary-object"),
    ],
)
def test_invalid_provenance_value_types_are_rejected(invalid_value: object) -> None:
    """SV-OR-029: require provenance value string semantics independently.

    Evidence ID
        ``SV-OR-029``; IDs identify wrong value families.
    Requirement
        Every provenance value is a Python string without coercion.
    Method
        Keep one valid key and place the invalid object only as value.
    Oracle
        The approved mapping-content taxonomy requires ``TypeError``.
    Acceptance
        Diagnostic identifies provenance keys/values and strings.
    Interpretation
        Passing establishes value typing independently of key typing.
    Limitations
        It does not validate provenance truth, scientific validation, UQ, or Rust
        conformance.
    """

    provenance = {"source": cast(Any, invalid_value)}
    with pytest.raises(TypeError) as exc_info:
        make_record(provenance=cast(Any, provenance))
    message = str(exc_info.value)
    assert "provenance" in message
    assert "strings" in message


def test_empty_provenance_value_is_rejected() -> None:
    """SV-OR-030: reject the correctly typed empty provenance value.

    Evidence ID
        ``SV-OR-030``.
    Requirement
        Every value is nonempty.
    Method
        Construct with one valid key and empty value.
    Oracle
        The approved content invariant requires ``ValueError``.
    Acceptance
        Diagnostic identifies provenance and empty content.
    Interpretation
        Passing establishes value taxonomy independently.
    Limitations
        It establishes no provenance truth, scientific validation, UQ, or Rust
        conformance.
    """

    with pytest.raises(ValueError) as exc_info:
        make_record(provenance={"source": ""})
    message = str(exc_info.value)
    assert "provenance" in message
    assert "must not be empty" in message


def test_explicit_empty_provenance_mapping_is_admitted() -> None:
    """SV-OR-031: preserve an intentionally supplied empty mapping.

    Evidence ID
        ``SV-OR-031``.
    Requirement
        Empty provenance is valid and is not replaced by fixture defaults.
    Method
        Supply ``{}`` explicitly through a helper that distinguishes ``None``
        from empty mappings using ``is None``.
    Oracle
        The approved Mapping contract imposes entry invariants but no nonempty
        container invariant.
    Acceptance
        Construction succeeds and exposed provenance remains empty.
    Interpretation
        Passing establishes empty-mapping admission and fixture transparency.
    Limitations
        Absence of provenance does not establish reproducibility, scientific
        validation, UQ, or Rust conformance.
    """

    provenance: Mapping[str, str] = {}
    record = make_record(provenance=provenance)

    assert dict(record.provenance) == {}
    assert len(record.provenance) == 0
