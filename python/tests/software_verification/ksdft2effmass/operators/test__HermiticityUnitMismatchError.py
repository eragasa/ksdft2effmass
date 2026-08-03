r"""Software verification for ``HermiticityUnitMismatchError``.

System and operational boundary
-------------------------------
``HermiticityUnitMismatchError`` is the structured public exception used when
an Analyzer's declared energy-unit policy differs exactly from the
``OperatorRecord`` energy metadata. The roles are distinct and ordered:

.. code-block:: text

   Analyzer unit policy       u_analyzer
   OperatorRecord metadata    u_record
   exact mismatch             u_analyzer != u_record
   structured error           HermiticityUnitMismatchError

The exception retains both role-specific strings. It performs no normalization,
case folding, unit conversion, registry lookup, dimensional analysis, or
physical-equivalence inference. It does not perform Hermiticity analysis.
``HermiticityAnalyzer`` owns production detection and propagation; these direct
constructor tests independently verify only the exception's intrinsic state.

Evidence class, strategy, and oracle
------------------------------------
This cohesive module provides software-verification evidence ``SV-HUME-001``
through ``SV-HUME-008``. The approved source and Sphinx public contracts define
the oracle: ``ValueError`` hierarchy, ordered exact string retention,
role-specific ``TypeError`` and ``ValueError`` taxonomy, exact case-sensitive
mismatch semantics, human-readable diagnostics, reason exclusion, and no
approved exception serialization API.

Interpretation and exclusions
-----------------------------
Passing establishes the direct structured-error contract. Failure may indicate a
constructor regression, documentation mismatch, or evidence defect requiring
investigation. The synthetic strings do not establish that either unit is
physically valid or scientifically suitable. These tests construct no Analyzer,
``OperatorRecord``, matrix, tolerance, or residual. They provide no numerical
verification, scientific validation, uncertainty quantification, dimensional-
equivalence evidence, conversion-factor evidence, or Rust conformance.
"""

from typing import Any, cast

import pytest

from ksdft2effmass.operators import HermiticityUnitMismatchError

pytestmark = pytest.mark.software_verification


def make_error(
    *,
    analyzer_energy_unit: str = "eV",
    record_energy_unit: str = "hartree",
) -> HermiticityUnitMismatchError:
    """Directly construct a valid public unit-mismatch exception.

    Evidence ID
        Supporting fixture for ``SV-HUME-001`` through ``SV-HUME-003``,
        ``SV-HUME-007``, and ``SV-HUME-008``; it owns no separate identifier.
    Requirement
        Defaults are distinct nonempty strings in ordered Analyzer and record
        roles.
    Method
        Pass the two caller-supplied strings unchanged to the public exception
        constructor without ``Any`` or ``cast``.
    Oracle
        The approved structured-error contract admits exact nonempty string
        disagreement.
    Acceptance
        Construction returns ``HermiticityUnitMismatchError`` for the defaults.
    Interpretation
        The result is deterministic synthetic in-memory software evidence.
    Limitations
        The helper performs no conversion or dimensional analysis and constructs
        no Analyzer or ``OperatorRecord``. It establishes no physical unit
        validity, numerical verification, scientific validation, uncertainty
        quantification, or Rust conformance.
    """

    return HermiticityUnitMismatchError(
        analyzer_energy_unit,
        record_energy_unit,
    )


def test_public_construction_and_exception_taxonomy() -> None:
    """SV-HUME-001: construct the public structured ``ValueError`` subtype.

    Evidence ID
        ``SV-HUME-001``.
    Requirement
        Two distinct nonempty public strings directly construct the exception,
        which remains a ``ValueError`` and an ``Exception``.
    Method
        Construct through the supported public import with ``"eV"`` in the
        Analyzer role and ``"hartree"`` in the record role.
    Oracle
        The approved public exception contract specifies the documented
        hierarchy and two-unit constructor.
    Acceptance
        Construction succeeds and both hierarchy checks are true.
    Interpretation
        Passing establishes direct public construction and exception taxonomy.
    Limitations
        ``Exception.args``, traceback formatting, source location, hashability,
        pickling, private state, numerical verification, scientific validation,
        uncertainty quantification, and Rust conformance are untested.
    """

    error = HermiticityUnitMismatchError("eV", "hartree")

    assert isinstance(error, ValueError)
    assert isinstance(error, Exception)


def test_exact_analyzer_and_record_unit_roles_are_retained() -> None:
    """SV-HUME-002: retain exact unit values in their ordered public roles.

    Evidence ID
        ``SV-HUME-002``.
    Requirement
        The Analyzer-policy unit and record-metadata unit remain distinguishable
        and are not swapped during exception construction.
    Method
        Construct with clearly distinct values and compare each public field by
        string equality, including explicit cross-role inequalities.
    Oracle
        The approved structured-error contract assigns one public field to each
        ordered constructor role.
    Acceptance
        Each field equals its corresponding input and differs from the opposite
        role's input.
    Interpretation
        Passing establishes role fidelity by value without requiring string
        object identity.
    Limitations
        The Analyzer tolerance would use ``analyzer_energy_unit`` and the stored
        matrix/residual would use ``record_energy_unit``; this test constructs
        neither and does not test propagation, conversion, numerical
        verification, scientific validation, UQ, or Rust conformance.
    """

    analyzer_energy_unit = "eV"
    record_energy_unit = "hartree"

    error = HermiticityUnitMismatchError(
        analyzer_energy_unit,
        record_energy_unit,
    )

    assert error.analyzer_energy_unit == analyzer_energy_unit
    assert error.record_energy_unit == record_energy_unit
    assert error.analyzer_energy_unit != record_energy_unit
    assert error.record_energy_unit != analyzer_energy_unit


def test_human_readable_unit_mismatch_summary() -> None:
    """SV-HUME-003: summarize the mismatch while fields remain authoritative.

    Evidence ID
        ``SV-HUME-003``.
    Requirement
        The message identifies an energy-unit mismatch, includes both unit
        values, and distinguishes Analyzer and record roles.
    Method
        Construct a valid mismatch and inspect only stable semantic role/value
        content in ``str(error)``.
    Oracle
        Approved public documentation promises a role-labeled human-readable
        mismatch summary but not incidental punctuation, quoting, or separators.
    Acceptance
        Case-insensitive role phrases and both exact input values occur in the
        message; structured fields retain the same values.
    Interpretation
        Passing establishes a useful diagnostic without requiring message
        parsing for programmatic state.
    Limitations
        Full message equality, capitalization, punctuation, separators, physical
        unit validity, numerical verification, scientific validation,
        uncertainty quantification, and Rust conformance are not established.
    """

    error = make_error()
    message = str(error)
    folded_message = message.casefold()

    assert "energy unit" in folded_message
    assert "analyzer energy unit" in folded_message
    assert "record energy unit" in folded_message
    assert error.analyzer_energy_unit in message
    assert error.record_energy_unit in message


@pytest.mark.parametrize(
    ("role", "invalid_unit"),
    [
        pytest.param("analyzer", None, id="SV-HUME-004-analyzer-none"),
        pytest.param("analyzer", True, id="SV-HUME-004-analyzer-boolean-true"),
        pytest.param(
            "analyzer",
            False,
            id="SV-HUME-004-analyzer-boolean-false",
        ),
        pytest.param("analyzer", 7, id="SV-HUME-004-analyzer-integer"),
        pytest.param("analyzer", object(), id="SV-HUME-004-analyzer-object"),
        pytest.param("record", None, id="SV-HUME-004-record-none"),
        pytest.param("record", True, id="SV-HUME-004-record-boolean-true"),
        pytest.param("record", False, id="SV-HUME-004-record-boolean-false"),
        pytest.param("record", 7, id="SV-HUME-004-record-integer"),
        pytest.param("record", object(), id="SV-HUME-004-record-object"),
    ],
)
def test_invalid_unit_types_are_rejected(role: str, invalid_unit: object) -> None:
    """SV-HUME-004: reject wrong unit types with role-specific ``TypeError``.

    Evidence ID
        ``SV-HUME-004``; parameter IDs identify every invalid role/value family.
    Requirement
        ``None``, each Boolean value, integers, and arbitrary objects are rejected
        independently in both unit roles, with a diagnostic identifying the
        invalid role.
    Method
        Pass one value per parameter through ``Any``/``cast`` only at the
        deliberate invalid constructor boundary while keeping the opposite role
        valid.
    Oracle
        The approved public taxonomy requires ``TypeError`` and the precise
        role-specific diagnostic fragment.
    Acceptance
        Every independently collected case raises exactly ``TypeError`` naming
        either ``analyzer energy unit`` or ``record energy unit`` as selected.
    Interpretation
        Passing establishes independent role and invalid-family validation
        without coercion.
    Limitations
        Empty and equal strings are correctly typed invariant failures tested
        separately. No Analyzer, conversion, numerical verification, scientific
        validation, uncertainty quantification, or Rust conformance is tested.
    """

    invalid_constructor = cast(Any, HermiticityUnitMismatchError)
    expected_fragment = f"{role} energy unit"

    with pytest.raises(TypeError) as exc_info:
        if role == "analyzer":
            invalid_constructor(invalid_unit, "hartree")
        else:
            invalid_constructor("eV", invalid_unit)

    assert expected_fragment in str(exc_info.value)


@pytest.mark.parametrize(
    "empty_role",
    [
        pytest.param("analyzer", id="SV-HUME-005-empty-analyzer-unit"),
        pytest.param("record", id="SV-HUME-005-empty-record-unit"),
    ],
)
def test_empty_unit_strings_are_rejected(empty_role: str) -> None:
    """SV-HUME-005: reject each empty role with role-specific ``ValueError``.

    Evidence ID
        ``SV-HUME-005``; parameter IDs identify the empty role.
    Requirement
        Both role-specific unit strings must be nonempty; an empty correctly
        typed string violates the invariant rather than the type boundary.
    Method
        Supply ``""`` independently in each role while the opposite role is a
        valid nonempty string.
    Oracle
        The approved public taxonomy requires ``ValueError`` and a diagnostic
        naming the empty role.
    Acceptance
        Each case raises exactly ``ValueError`` with its role-specific fragment.
    Interpretation
        Passing establishes independent nonempty-string validation.
    Limitations
        Whitespace-only strings are not normalized or rejected by this contract;
        no trimming, registry validation, Analyzer execution, numerical
        verification, scientific validation, UQ, or Rust conformance is tested.
    """

    with pytest.raises(ValueError) as exc_info:
        if empty_role == "analyzer":
            HermiticityUnitMismatchError("", "hartree")
        else:
            HermiticityUnitMismatchError("eV", "")

    assert f"{empty_role} energy unit" in str(exc_info.value)


@pytest.mark.parametrize(
    ("analyzer_energy_unit", "record_energy_unit", "is_mismatch"),
    [
        pytest.param("eV", "eV", False, id="SV-HUME-006-equal-ev"),
        pytest.param(
            "hartree",
            "hartree",
            False,
            id="SV-HUME-006-equal-hartree",
        ),
        pytest.param(
            "eV",
            "EV",
            True,
            id="SV-HUME-006-case-sensitive-mismatch",
        ),
    ],
)
def test_exact_mismatch_semantics_and_equal_unit_rejection(
    analyzer_energy_unit: str,
    record_energy_unit: str,
    is_mismatch: bool,
) -> None:
    """SV-HUME-006: enforce exact inequality without case normalization.

    Evidence ID
        ``SV-HUME-006``; parameter IDs distinguish equality and case mismatch.
    Requirement
        Equal strings cannot represent a mismatch and raise ``ValueError``;
        ``"eV"`` versus ``"EV"`` is admitted under exact case-sensitive
        comparison.
    Method
        Select two equal pairs and one case-only differing pair independently of
        the constructor, then inspect the documented outcome and retained values.
    Oracle
        The approved invariant is exact Python string inequality, with no unit
        normalization or physical-equivalence inference.
    Acceptance
        Equal pairs raise exactly ``ValueError`` identifying the need to differ;
        the case-only pair constructs and retains both exact strings.
    Interpretation
        Passing establishes software string semantics only, not that differently
        cased strings denote physically different units.
    Limitations
        Approximate equality, conversion, registry lookup, Analyzer execution,
        numerical verification, scientific validation, uncertainty
        quantification, and Rust conformance are outside this evidence.
    """

    if not is_mismatch:
        assert analyzer_energy_unit == record_energy_unit
        with pytest.raises(ValueError) as exc_info:
            HermiticityUnitMismatchError(
                analyzer_energy_unit,
                record_energy_unit,
            )

        assert "must differ" in str(exc_info.value)
        return

    assert analyzer_energy_unit != record_energy_unit
    error = HermiticityUnitMismatchError(
        analyzer_energy_unit,
        record_energy_unit,
    )
    assert error.analyzer_energy_unit == "eV"
    assert error.record_energy_unit == "EV"


@pytest.mark.parametrize(
    "reason_form",
    [
        pytest.param("positional", id="SV-HUME-007-positional-reason"),
        pytest.param("keyword", id="SV-HUME-007-keyword-reason"),
    ],
)
def test_free_form_reason_and_extra_argument_are_excluded(reason_form: str) -> None:
    """SV-HUME-007: exclude arbitrary reason parameters and state.

    Evidence ID
        ``SV-HUME-007``; parameter IDs distinguish positional and keyword forms.
    Requirement
        The constructor accepts only the two ordered unit strings; extra reasons
        raise ``TypeError`` and valid exceptions expose no public ``reason``.
    Method
        Invoke an ``Any``-typed constructor only at each deliberate invalid-
        signature boundary, then inspect a valid exception.
    Oracle
        The approved two-parameter signature and structured role fields define
        no free-form reason parameter or attribute.
    Acceptance
        Both extra-argument forms raise exactly ``TypeError`` and ``reason`` is
        absent from a valid instance.
    Interpretation
        Passing prevents arbitrary text from competing with the ordered unit
        fields as structured mismatch evidence.
    Limitations
        Signature-generated ``TypeError`` wording, Analyzer propagation,
        numerical verification, scientific validation, uncertainty
        quantification, and Rust conformance are not tested.
    """

    invalid_constructor = cast(Any, HermiticityUnitMismatchError)

    if reason_form == "positional":
        with pytest.raises(TypeError):
            invalid_constructor("eV", "hartree", "synthetic reason")
    else:
        with pytest.raises(TypeError):
            invalid_constructor("eV", "hartree", reason="synthetic reason")

    error = make_error()
    assert not hasattr(error, "reason")


def test_exception_has_no_independent_serialization_api() -> None:
    """SV-HUME-008: verify exclusion of exception serialization methods.

    Evidence ID
        ``SV-HUME-008``.
    Requirement
        The in-memory structured exception exposes none of the six unapproved
        JSON, dictionary, serializer, or deserializer method names.
    Method
        Inspect both a valid instance and the public class for each excluded
        method.
    Oracle
        ``OperatorRecordJsonSerializer`` serializes only ``OperatorRecord``; no
        unit-mismatch exception wire format is approved.
    Acceptance
        Every excluded method name is absent from both instance and class.
    Interpretation
        Passing establishes serialization exclusion while retaining the ordered
        unit strings as in-memory state.
    Limitations
        Pickling and future schemas are unspecified. No Rust serialization or
        conformance, Analyzer execution, numerical verification, scientific
        validation, or uncertainty quantification is established.
    """

    error = make_error()

    for method_name in (
        "to_json",
        "to_dict",
        "serialize",
        "from_json",
        "from_dict",
        "deserialize",
    ):
        assert not hasattr(error, method_name)
        assert not hasattr(HermiticityUnitMismatchError, method_name)
