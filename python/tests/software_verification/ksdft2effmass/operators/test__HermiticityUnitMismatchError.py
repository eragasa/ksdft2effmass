r"""Software verification of ``HermiticityUnitMismatchError``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

-----------------------------
This class-owned module owns the HermiticityUnitMismatchError facet. System and
operational boundary
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

Intrinsic and cross-object scope

--------------------------------
The primary owner is ``HermiticityUnitMismatchError``; collaborators only construct
inputs or expose public outcomes. Accepted public contracts, literal expected
values, Python language semantics, and assigned schema or fixture artifacts provide
the oracles. No runtime warning is accepted unless a test explicitly states
otherwise.

VVUQ and scientific exclusions

------------------------------
Passing establishes only the documented software contract and exact or explicitly
bounded acceptance rules. Failure may identify implementation, fixture, oracle,
environment, or contract defects. It does not establish numerical verification,
physical correctness, scientific validation, UQ, portability, or cross-language
agreement.
"""

from typing import Any, cast

import pytest

from ksdft2effmass.operators import HermiticityUnitMismatchError

pytestmark = pytest.mark.software_verification

SUT = HermiticityUnitMismatchError


def make_error(
    *,
    analyzer_energy_unit: str = "eV",
    record_energy_unit: str = "hartree",
) -> HermiticityUnitMismatchError:
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: Defaults are distinct nonempty strings in ordered Analyzer and record
    roles.

    Method: Pass the two caller-supplied strings unchanged to the public exception
    constructor
    without ``Any`` or ``cast``.

    Oracle: The approved structured-error contract admits exact nonempty string
    disagreement.

    Acceptance: Construction returns ``HermiticityUnitMismatchError`` for the defaults.

    Interpretation: The result is deterministic synthetic in-memory software evidence.

    Limitations: The helper performs no conversion or dimensional analysis and
    constructs no Analyzer
    or ``OperatorRecord``. It establishes no physical unit validity, numerical
    verification, scientific validation, uncertainty quantification, or Rust
    conformance.
    """

    return HermiticityUnitMismatchError(
        analyzer_energy_unit,
        record_energy_unit,
    )


def test_constructor__public_construction_and_exception_taxonomy__is_enforced() -> None:
    r"""Evidence ID: SV-HUME-001

    Requirement: Two distinct nonempty public strings directly construct the exception,
    which remains
    a ``ValueError`` and an ``Exception``.

    Method: Construct through the supported public import with ``"eV"`` in the Analyzer
    role and
    ``"hartree"`` in the record role.

    Oracle: The approved public exception contract specifies the documented hierarchy
    and
    two-unit constructor.

    Acceptance: Construction succeeds and both hierarchy checks are true.

    Interpretation: Passing establishes direct public construction and exception
    taxonomy.

    Limitations: ``Exception.args``, traceback formatting, source location, hashability,
    pickling,
    private state, numerical verification, scientific validation, uncertainty
    quantification, and Rust conformance are untested.
    """

    error = HermiticityUnitMismatchError("eV", "hartree")

    assert isinstance(error, ValueError)
    assert isinstance(error, Exception)


def test_field__exact_analyzer_and_record_unit_roles_are_retained__is_exact() -> None:
    r"""Evidence ID: SV-HUME-002

    Requirement: The Analyzer-policy unit and record-metadata unit remain
    distinguishable and are not
    swapped during exception construction.

    Method: Construct with clearly distinct values and compare each public field by
    string
    equality, including explicit cross-role inequalities.

    Oracle: The approved structured-error contract assigns one public field to each
    ordered
    constructor role.

    Acceptance: Each field equals its corresponding input and differs from the opposite
    role's
    input.

    Interpretation: Passing establishes role fidelity by value without requiring string
    object identity.

    Limitations: The Analyzer tolerance would use ``analyzer_energy_unit`` and the
    stored
    matrix/residual would use ``record_energy_unit``; this test constructs neither and
    does not test propagation, conversion, numerical verification, scientific
    validation, UQ, or Rust conformance.
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


def test_protocol__str__human_readable_unit_mismatch_summary() -> None:
    r"""Evidence ID: SV-HUME-003

    Requirement: The message identifies an energy-unit mismatch, includes both unit
    values, and
    distinguishes Analyzer and record roles.

    Method: Construct a valid mismatch and inspect only stable semantic role/value
    content in
    ``str(error)``.

    Oracle: Approved public documentation promises a role-labeled human-readable
    mismatch
    summary but not incidental punctuation, quoting, or separators.

    Acceptance: Case-insensitive role phrases and both exact input values occur in the
    message;
    structured fields retain the same values.

    Interpretation: Passing establishes a useful diagnostic without requiring message
    parsing for
    programmatic state.

    Limitations: Full message equality, capitalization, punctuation, separators,
    physical unit
    validity, numerical verification, scientific validation, uncertainty quantification,
    and Rust conformance are not established.
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
        pytest.param("analyzer", None, id="none"),
        pytest.param("analyzer", True, id="sv_hume_004_analyzer_boolean_true"),
        pytest.param("analyzer", False, id="sv_hume_004_analyzer_boolean_false"),
        pytest.param("analyzer", 7, id="sv_hume_004_analyzer_integer"),
        pytest.param("analyzer", object(), id="sv_hume_004_analyzer_object"),
        pytest.param("record", None, id="none"),
        pytest.param("record", True, id="sv_hume_004_record_boolean_true"),
        pytest.param("record", False, id="sv_hume_004_record_boolean_false"),
        pytest.param("record", 7, id="sv_hume_004_record_integer"),
        pytest.param("record", object(), id="sv_hume_004_record_object"),
    ],
)
def test_constructor__invalid_unit_types_are_rejected__is_enforced(
    role: str, invalid_unit: object
) -> None:
    r"""Evidence ID: SV-HUME-004

    Requirement: ``None``, each Boolean value, integers, and arbitrary objects are
    rejected
    independently in both unit roles, with a diagnostic identifying the invalid role.

    Method: Pass one value per parameter through ``Any``/``cast`` only at the deliberate
    invalid
    constructor boundary while keeping the opposite role valid.

    Oracle: The approved public taxonomy requires ``TypeError`` and the precise
    role-specific
    diagnostic fragment.

    Acceptance: Every independently collected case raises exactly ``TypeError`` naming
    either
    ``analyzer energy unit`` or ``record energy unit`` as selected.

    Interpretation: Passing establishes independent role and invalid-family validation
    without coercion.

    Limitations: Empty and equal strings are correctly typed invariant failures tested
    separately. No
    Analyzer, conversion, numerical verification, scientific validation, uncertainty
    quantification, or Rust conformance is tested.
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
        pytest.param("analyzer", id="empty_analyzer_unit"),
        pytest.param("record", id="empty_record_unit"),
    ],
)
def test_constructor__empty_unit_strings_are_rejected__is_enforced(
    empty_role: str,
) -> None:
    r"""Evidence ID: SV-HUME-005

    Requirement: Both role-specific unit strings must be nonempty; an empty correctly
    typed string
    violates the invariant rather than the type boundary.

    Method: Supply ``""`` independently in each role while the opposite role is a valid
    nonempty
    string.

    Oracle: The approved public taxonomy requires ``ValueError`` and a diagnostic naming
    the
    empty role.

    Acceptance: Each case raises exactly ``ValueError`` with its role-specific fragment.

    Interpretation: Passing establishes independent nonempty-string validation.

    Limitations: Whitespace-only strings are not normalized or rejected by this
    contract; no
    trimming, registry validation, Analyzer execution, numerical verification,
    scientific validation, UQ, or Rust conformance is tested.
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
        pytest.param("eV", "eV", False, id="sv_hume_006_equal_ev"),
        pytest.param("hartree", "hartree", False, id="sv_hume_006_equal_hartree"),
        pytest.param("eV", "EV", True, id="case_sensitive_mismatch"),
    ],
)
def test_field__exact_mismatch_semantics_and_equal_unit_rejection__is_exact(
    analyzer_energy_unit: str,
    record_energy_unit: str,
    is_mismatch: bool,
) -> None:
    r"""Evidence ID: SV-HUME-006

    Requirement: Equal strings cannot represent a mismatch and raise ``ValueError``;
    ``"eV"`` versus
    ``"EV"`` is admitted under exact case-sensitive comparison.

    Method: Select two equal pairs and one case-only differing pair independently of the
    constructor, then inspect the documented outcome and retained values.

    Oracle: The approved invariant is exact Python string inequality, with no unit
    normalization
    or physical-equivalence inference.

    Acceptance: Equal pairs raise exactly ``ValueError`` identifying the need to differ;
    the
    case-only pair constructs and retains both exact strings.

    Interpretation: Passing establishes software string semantics only, not that
    differently cased
    strings denote physically different units.

    Limitations: Approximate equality, conversion, registry lookup, Analyzer execution,
    numerical
    verification, scientific validation, uncertainty quantification, and Rust
    conformance are outside this evidence.
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
        pytest.param("positional", id="sv_hume_007_positional_reason"),
        pytest.param("keyword", id="sv_hume_007_keyword_reason"),
    ],
)
def test_constructor__input_boundary__free_form_reason_and_extra_argument_are(
    reason_form: str,
) -> None:
    r"""Evidence ID: SV-HUME-007

    Requirement: The constructor accepts only the two ordered unit strings; extra
    reasons raise
    ``TypeError`` and valid exceptions expose no public ``reason``.

    Method: Invoke an ``Any``-typed constructor only at each deliberate invalid-
    signature
    boundary, then inspect a valid exception.

    Oracle: The approved two-parameter signature and structured role fields define no
    free-form
    reason parameter or attribute.

    Acceptance: Both extra-argument forms raise exactly ``TypeError`` and ``reason`` is
    absent from
    a valid instance.

    Interpretation: Passing prevents arbitrary text from competing with the ordered unit
    fields as
    structured mismatch evidence.

    Limitations: Signature-generated ``TypeError`` wording, Analyzer propagation,
    numerical
    verification, scientific validation, uncertainty quantification, and Rust
    conformance are not tested.
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


def test_method__serialize__exception_has_no_serialization_api() -> None:
    r"""Evidence ID: SV-HUME-008

    Requirement: The in-memory structured exception exposes none of the six unapproved
    JSON,
    dictionary, serializer, or deserializer method names.

    Method: Inspect both a valid instance and the public class for each excluded method.

    Oracle: ``OperatorRecordJsonSerializer`` serializes only ``OperatorRecord``; no
    unit-mismatch exception wire format is approved.

    Acceptance: Every excluded method name is absent from both instance and class.

    Interpretation: Passing establishes serialization exclusion while retaining the
    ordered unit strings
    as in-memory state.

    Limitations: Pickling and future schemas are unspecified. No Rust serialization or
    conformance,
    Analyzer execution, numerical verification, scientific validation, or uncertainty
    quantification is established.
    """

    error = make_error()

    assert all(
        (not hasattr(error, method_name))
        and (not hasattr(HermiticityUnitMismatchError, method_name))
        for method_name in (
            "to_json",
            "to_dict",
            "serialize",
            "from_json",
            "from_dict",
            "deserialize",
        )
    )
