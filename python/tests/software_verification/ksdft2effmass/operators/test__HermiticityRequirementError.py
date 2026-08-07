r"""Software verification of ``HermiticityRequirementError``.

Facet and represented meaning
-----------------------------
This class-owned module owns the HermiticityRequirementError facet. System under
test
-----------------
``HermiticityResult`` is the immutable structured analysis result containing the
Hermiticity residual :math:`\varepsilon_{\mathrm H}`, tolerance :math:`\tau`,
and their common energy unit. ``HermiticityRequirementError`` is the structured
public enforcement failure that retains one such result when the criterion

.. math::

\varepsilon_{\mathrm H} > \tau

holds. ``HermiticityAnalyzer.require()`` is the production ActionObject operation
that emits the exception. These direct constructor tests instead verify that the
exception independently protects its own failed-result invariant.

Equality is an accepted boundary:

.. math::

\varepsilon_{\mathrm H} = \tau.

It therefore must not be represented as a requirement failure. Residual,
tolerance, and unit remain authoritative fields of the retained result rather
than duplicated exception fields. The exception message is a secondary human-
readable summary and is not a machine-parsing protocol.

Evidence class, strategy, and oracle
------------------------------------
This cohesive module provides software-verification evidence ``SV-HRE-001``
through ``SV-HRE-007``. The approved architectural and Sphinx public contract is
the oracle. Direct construction verifies
public hierarchy, exact result identity retention, stable diagnostic semantics,
``TypeError`` versus ``ValueError`` taxonomy, exclusion of free-form reasons,
and absence of an approved exception serialization API without invoking the
Analyzer.

Interpretation and exclusions
-----------------------------
Passing establishes the direct public exception contract and its in-memory
structured state. Failure may indicate an exception regression, a documentation
mismatch, or an evidence defect requiring investigation. These tests do not
independently verify the numerical residual algorithm, matrix arithmetic, or a
physical tolerance choice. They establish no physical Hermiticity, DFT validity,
Wannier-representation validity, model validity, scientific validation,
uncertainty quantification, or Rust conformance.

Intrinsic and cross-object scope
--------------------------------
The primary owner is ``HermiticityRequirementError``; collaborators only construct
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

from ksdft2effmass.operators import HermiticityRequirementError, HermiticityResult

pytestmark = pytest.mark.software_verification

SUT = HermiticityRequirementError


def make_failed_result(
    *,
    residual: float = 1.0,
    tolerance: float = 0.0,
    energy_unit: str = "eV",
) -> HermiticityResult:
    r"""Evidence ID
    Owns no identifier; supports evidence in this module.
    Requirement
    Defaults satisfy ``residual > tolerance`` and therefore construct a failed public
    ``HermiticityResult`` suitable for the exception.
    Method
    Pass the caller's explicit scalar values and unit unchanged to the public
    ResultObject constructor, without ``Any`` or ``cast``.
    Oracle
    The public ``is_hermitian`` property defines acceptance as ``residual <=
    tolerance``.
    Acceptance
    The returned public result has ``is_hermitian`` false for the defaults.
    Interpretation
    The result is deterministic synthetic software evidence; the helper performs no
    Hermiticity analysis.
    Limitations
    No matrix, DFT record, Wannier representation, or physical operator is involved. The
    helper establishes no numerical correctness, physical Hermiticity, scientific
    validation, uncertainty quantification, or Rust conformance.
    """

    return HermiticityResult(
        residual=residual,
        tolerance=tolerance,
        energy_unit=energy_unit,
    )


def test_constructor__public_construction_and_exception_taxonomy__is_enforced() -> None:
    r"""Evidence ID
    SV-HRE-001
    Requirement
    One failed public result directly constructs ``HermiticityrequirementError``, which
    remains a ``ValueError`` and an ``Exception``.
    Method
    Construct a synthetic failed result and pass it to the public exception constructor
    without Analyzer execution.
    Oracle
    The approved public exception contract specifies ``ValueError`` inheritance and a
    one-result constructor.
    Acceptance
    Construction succeeds and both documented hierarchy checks are true.
    Interpretation
    Passing establishes public direct construction and exception taxonomy.
    Limitations
    ``Exception.args``, traceback formatting, source location, memory layout,
    hashability, numerical verification, scientific validation, uncertainty
    quantification, and Rust conformance are unspecified or untested.
    """

    result = make_failed_result()

    error = HermiticityRequirementError(result)

    assert isinstance(error, ValueError)
    assert isinstance(error, Exception)


def test_field__represented_state__exact_failed_result_identity_is_retained() -> None:
    r"""Evidence ID
    SV-HRE-002
    Requirement
    Callers receive the identical failed ``HermiticityResult`` through ``error.result``,
    preserving residual, tolerance, and energy unit.
    Method
    Construct one failed result and compare the public retained object by identity and
    its documented public fields by exact equality.
    Oracle
    The structured-exception contract designates the supplied ResultObject as
    authoritative machine-readable evidence.
    Acceptance
    ``error.result is result`` and all three fields plus failed status agree.
    Interpretation
    Passing establishes lossless in-memory audit-result identity retention.
    Limitations
    ResultObject constructor invariants belong to its own evidence modules. No Analyzer,
    numerical algorithm, scientific validation, uncertainty quantification, or Rust
    conformance is tested.
    """

    result = make_failed_result(residual=2.5, tolerance=0.25, energy_unit="meV")

    error = HermiticityRequirementError(result)

    assert error.result is result
    assert error.result.residual == result.residual
    assert error.result.tolerance == result.tolerance
    assert error.result.energy_unit == result.energy_unit
    assert not error.result.is_hermitian


def test_protocol__str__human_readable_hermiticity_failure_summary() -> None:
    r"""Evidence ID
    SV-HRE-003
    Requirement
    The exception provides a human-readable statement that the operator matrix is not
    Hermitian within tolerance while ``error.result`` remains the programmatic evidence.
    Method
    Construct a failed result with distinct readable residual, tolerance, and unit, then
    inspect only the documented semantic phrase.
    Oracle
    The approved public documentation promises a concise not-Hermitian- within-tolerance
    summary, not exact numeric formatting.
    Acceptance
    The stable semantic phrase occurs in ``str(error)`` and the exact result remains
    retained.
    Interpretation
    Passing establishes a useful human diagnostic without requiring callers to parse
    message text for residual, tolerance, or unit.
    Limitations
    Punctuation, capitalization, separators, float formatting, and numeric duplication
    in the message are not compatibility guarantees. No numerical verification,
    scientific validation, uncertainty quantification, or Rust conformance is
    established.
    """

    result = HermiticityResult(
        residual=1.0e-6,
        tolerance=1.0e-12,
        energy_unit="eV",
    )

    error = HermiticityRequirementError(result)

    assert "not hermitian within tolerance" in str(error).casefold()
    assert error.result is result


@pytest.mark.parametrize(
    "invalid_result",
    [
        pytest.param(None, id="none_wrong_type"),
        pytest.param("not a result", id="string_wrong_type"),
        pytest.param(True, id="true_wrong_type"),
        pytest.param(False, id="false_wrong_type"),
        pytest.param(object(), id="object_wrong_type"),
    ],
)
def test_constructor__invalid_result_types_are_rejected__is_enforced(
    invalid_result: object,
) -> None:
    r"""Evidence ID
    SV-HRE-004
    Requirement
    Only ``HermiticityResult`` instances are accepted; ``None``, strings, both Boolean
    values, and arbitrary objects are wrong semantic types.
    Method
    Pass each representative value at a deliberate invalid constructor boundary, using
    ``Any`` and ``cast`` only at that boundary.
    Oracle
    The public constructor documents ``TypeError`` and the stable owner-type diagnostic
    fragment ``HermiticityResult``.
    Acceptance
    Every invalid value raises exactly ``TypeError`` and names the required owner type.
    Interpretation
    Passing establishes wrong-type taxonomy without coercion.
    Limitations
    Correctly typed successful Results are a separate invariant family. No Analyzer,
    numerical verification, scientific validation, uncertainty quantification, or Rust
    conformance is tested.
    """

    with pytest.raises(TypeError) as exc_info:
        HermiticityRequirementError(cast(Any, invalid_result))

    assert "HermiticityResult" in str(exc_info.value)


@pytest.mark.parametrize(
    "result",
    [
        pytest.param(HermiticityResult(0.0, 0.0, "eV"), id="exact_zero"),
        pytest.param(HermiticityResult(1e-13, 1e-12, "eV"), id="tolerance"),
        pytest.param(HermiticityResult(1e-12, 1e-12, "eV"), id="tolerance"),
    ],
)
def test_constructor__successful_results_are_rejected__is_enforced(
    result: HermiticityResult,
) -> None:
    r"""Evidence ID
    SV-HRE-005
    Requirement
    Results satisfying ``residual <= tolerance`` are successful and cannot form
    structured requirement failures.
    Method
    Select three independently explicit public Results, interpret each with
    ``result.is_hermitian``, and pass it directly to the exception.
    Oracle
    The approved public property defines the inclusive acceptance boundary; the
    exception contract requires a failed Result.
    Acceptance
    Every Result reports success, then raises exactly ``ValueError`` with the stable
    failed-result requirement phrase.
    Interpretation
    Passing establishes correct invariant rejection, especially at ``residual ==
    tolerance``.
    Limitations
    The test does not recompute a residual, choose a physical tolerance, or execute the
    Analyzer. It establishes no numerical verification, scientific validation,
    uncertainty quantification, or Rust conformance.
    """

    assert result.residual <= result.tolerance
    assert result.is_hermitian

    with pytest.raises(ValueError) as exc_info:
        HermiticityRequirementError(result)

    assert "failed HermiticityResult" in str(exc_info.value)


@pytest.mark.parametrize(
    "reason_form",
    [
        pytest.param("positional", id="sv_hre_006_positional_reason"),
        pytest.param("keyword", id="sv_hre_006_keyword_reason"),
    ],
)
def test_constructor__input_boundary__free_form_reason_and_extra_argument_are(
    reason_form: str,
) -> None:
    r"""Evidence ID
    SV-HRE-006
    Requirement
    The constructor accepts only one structured Result; extra free-form reasons raise
    ``TypeError`` and valid exceptions expose no ``reason``.
    Method
    Invoke the constructor through an ``Any``-typed invalid-signature boundary for each
    reason form, then inspect a valid instance.
    Oracle
    The approved one-parameter signature and retained-result model define no free-form
    reason parameter or attribute.
    Acceptance
    Both extra-argument forms raise exactly ``TypeError`` and ``reason`` is absent from
    a valid exception.
    Interpretation
    Passing prevents arbitrary text from competing with the authoritative structured
    ``HermiticityResult``.
    Limitations
    Signature-generated ``TypeError`` wording is not frozen. Analyzer execution,
    numerical verification, scientific validation, uncertainty quantification, and Rust
    conformance are not tested.
    """

    invalid_constructor = cast(Any, HermiticityRequirementError)

    if reason_form == "positional":
        with pytest.raises(TypeError):
            invalid_constructor(make_failed_result(), "synthetic reason")
    else:
        with pytest.raises(TypeError):
            invalid_constructor(make_failed_result(), reason="synthetic reason")

    error = HermiticityRequirementError(make_failed_result())
    assert not hasattr(error, "reason")


def test_method__serialize__exception_has_no_serialization_api() -> None:
    r"""Evidence ID
    SV-HRE-007
    Requirement
    The exception is an in-memory structured Python failure with no approved independent
    JSON, dictionary, serializer, or deserializer API.
    Method
    Inspect both a valid instance and the public class for six explicitly excluded
    method names.
    Oracle
    ``OperatorRecordJsonSerializer`` serializes only ``OperatorRecord``; no exception or
    retained-``HermiticityResult`` JSON schema is approved.
    Acceptance
    Every excluded method name is absent from instance and class.
    Interpretation
    Passing establishes serialization exclusion while preserving ``error.result`` as the
    in-memory machine-readable interface.
    Limitations
    Pickling and future schemas are unspecified. Future Rust error mapping is conceptual
    only; no Rust implementation, numerical verification, scientific validation, or
    uncertainty quantification is established.
    """

    error = HermiticityRequirementError(make_failed_result())

    assert all(
        (not hasattr(error, method_name))
        and (not hasattr(HermiticityRequirementError, method_name))
        for method_name in (
            "to_json",
            "to_dict",
            "serialize",
            "from_json",
            "from_dict",
            "deserialize",
        )
    )
