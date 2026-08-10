r"""Software verification of ``PythonConformanceValidator``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

This module verifies the explicit-byte structural-validation action and result ordering.

Intrinsic and cross-object scope

The sole SUT is ``PythonConformanceValidator``; request records are collaborators and
controlled literal source/JSON inputs provide independent exact rule oracles.

VVUQ and scientific exclusions

Passing establishes controlled software behavior only, not oracle independence, test
cohesion, numerical verification, scientific validation, UQ, or human acceptance.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from ksdft2effmass.harness.pi.evidence import (
    PythonConformanceRequest,
    PythonConformanceResult,
    PythonConformanceValidator,
    PythonModuleSource,
)

pytestmark = pytest.mark.software_verification
SUT = PythonConformanceValidator
PATH = "test__controlled_artifact.py"
VALID_SOURCE = b'''r"""Software verification of controlled artifact.

Facet and represented meaning

This fixture represents one exact public artifact value.

Intrinsic and cross-object scope

The controlled artifact is primary and literal equality supplies the oracle.

VVUQ and scientific exclusions

Passing establishes software structure only, not validation or UQ.
"""


def test_artifact__literal_value__equals_itself():
    """Evidence ID: SV-TEV-FIX-001

    Requirement: The controlled literal retains exact equality.

    Method: Compare one literal with itself.

    Oracle: Python integer equality fixes the result.

    Acceptance: The equality is exactly true.

    Interpretation: Failure identifies controlled fixture drift.

    Limitations: No scientific, numerical, or UQ claim is made.
    """
    assert 1 == 1
'''
VALID_OWNERSHIP = json.dumps(
    {
        "schema_version": 1,
        "modules": [
            {
                "path": PATH,
                "mode": "artifact_owned",
                "evidence_class": "software_verification",
                "artifact": "controlled artifact",
            }
        ],
    },
    separators=(",", ":"),
).encode()


def test_constructor__action_object__is_stateless_and_fieldless() -> None:
    """Evidence ID: SV-TEV-017

    Requirement: PythonConformanceValidator is a concrete stateless ActionObject.

    Method: Construct two instances and inspect their instance storage boundary.

    Oracle: The accepted placement contract requires no root, filesystem, cache, or
    state.

    Acceptance: Both construct, lack instance dictionaries, and the class slots are
    empty.

    Interpretation: Failure identifies unauthorized retained state or contract drift.

    Limitations: Execute semantics are covered separately.
    """
    first = SUT()
    second = SUT()
    assert type(first) is type(second) is SUT
    assert not hasattr(first, "__dict__")
    assert SUT.__slots__ == ()


def test_method__execute_valid_source__returns_exact_inventory() -> None:
    """Evidence ID: SV-TEV-018

    Requirement: Execute accepts a controlled conforming artifact-owned module and
    reports its
    exact static inventory.

    Method: Supply literal source and ownership bytes directly through the public
    request.

    Oracle: Manual inspection gives one module, one test, one evidence owner, no helpers
    or
    parameter cases, and one artifact-owned software-verification owner.

    Acceptance: The exact status, paths, findings, owner counts, and function counts
    match.

    Interpretation: Failure identifies validator, fixture, or accepted-rule drift.

    Limitations: A structural pass does not establish semantic quality or scientific
    claims.
    """
    request = PythonConformanceRequest(
        (PythonModuleSource(PATH, VALID_SOURCE),),
        "ownership.json",
        VALID_OWNERSHIP,
    )
    result = SUT().execute(request)
    assert type(result) is PythonConformanceResult
    assert result.status == "PASS"
    assert result.paths == (PATH,)
    assert result.findings == ()
    assert result.artifact_owned_modules == result.modules == result.test_functions == 1
    assert result.class_owned_modules == result.helper_functions == 0
    assert (
        result.parameterized_functions == result.static_collected_parameter_cases == 0
    )
    assert result.unique_evidence_owners == 1


def test_method__execute_invalid_source__retains_multiple_finding_order() -> None:
    """Evidence ID: SV-TEV-019

    Requirement: Execute retains multiple findings in deterministic rule traversal
    order.

    Method: Supply one controlled source with a nonraw opening, missing headings,
    malformed
    test name, and incomplete function documentation.

    Oracle: The documented traversal checks module opening, module documentation, then
    the
    top-level function name and documentation in that order.

    Acceptance: Status is FAIL and the first four codes equal the literal expected
    sequence.

    Interpretation: Failure identifies rule presence, aggregation, or
    deterministic-order drift.

    Limitations: This representative invalid source does not exhaust every validator
    code.
    """
    source = PythonModuleSource(
        PATH,
        b'"""Software verification of controlled artifact."""\n\n'
        b"def test_bad():\n    pass\n",
    )
    request = PythonConformanceRequest((source,), "ownership.json", VALID_OWNERSHIP)
    result = SUT().execute(request)
    assert result.status == "FAIL"
    assert tuple(item.code for item in result.findings[:4]) == (
        "TE.MODULE_OPENING",
        "TE.MODULE_DOC",
        "TE.TEST_NAME",
        "TE.FUNCTION_DOC",
    )
    assert result.findings_by_code == tuple(sorted(result.findings_by_code))


@pytest.mark.parametrize(
    ("ownership_payload", "migration_payload", "expected_code"),
    (
        pytest.param(b"null", None, "TE.OWNERSHIP_INPUT", id="invalid_ownership_shape"),
        pytest.param(
            VALID_OWNERSHIP, b"null", "TE.MIGRATION_INPUT", id="invalid_migration_shape"
        ),
    ),
)
def test_method__execute_metadata_contract__reports_controlled_invalidity(
    ownership_payload: bytes,
    migration_payload: bytes | None,
    expected_code: str,
) -> None:
    """Evidence ID: SV-TEV-020

    Requirement: Malformed ownership and migration metadata become their stable public
    findings.

    Method: Supply one correct source with a controlled malformed JSON object at each
    layer.

    Oracle: The closed version-one metadata contracts assign distinct exact finding
    codes.

    Acceptance: The result fails and contains the declared code for the selected layer.

    Interpretation: Failure identifies metadata routing, code, or accepted-contract
    drift.

    Limitations: This covers representative shape defects, not every metadata rule.
    """
    request = PythonConformanceRequest(
        (PythonModuleSource(PATH, VALID_SOURCE),),
        "ownership.json",
        ownership_payload,
        None,
        "migration.json" if migration_payload is not None else None,
        migration_payload,
    )
    result = SUT().execute(request)
    assert result.status == "FAIL"
    assert expected_code in tuple(item.code for item in result.findings)


def test_method__execute_explicit_bytes__is_repeatable_without_filesystem_reads(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Evidence ID: SV-TEV-021

    Requirement: Execute depends only on the explicit request and returns equal repeated
    results.

    Method: Construct one request, make ``Path.read_bytes`` fail if called, and execute
    twice.

    Oracle: The placement contract prohibits hidden filesystem access and immutable
    value
    semantics require equal outputs for identical explicit inputs.

    Acceptance: No injected filesystem failure occurs and the two results are exactly
    equal.

    Interpretation: Failure identifies hidden I/O, retained state, nondeterminism, or
    equality drift.

    Limitations: Other process-global services and performance characteristics are
    excluded.
    """
    request = PythonConformanceRequest(
        (PythonModuleSource(PATH, VALID_SOURCE),),
        "ownership.json",
        VALID_OWNERSHIP,
    )

    def reject_read_bytes(path: Path) -> bytes:
        raise AssertionError(f"unexpected filesystem read: {path}")

    monkeypatch.setattr(Path, "read_bytes", reject_read_bytes)
    action = SUT()
    assert action.execute(request) == action.execute(request)


def test_method__execute_docstring_format__requires_inline_labels_and_blank_lines() -> (
    None
):
    """Evidence ID: SV-TEV-026

    Requirement: Evidence fields use ``Label: value`` paragraphs separated by blank
    lines.

    Method: Replace the valid fixture with one standalone label and with zero or two
    blank lines between paragraphs.

    Oracle: The accepted maintained-evidence documentation grammar requires inline
    labels and exactly one blank line.

    Acceptance: Each controlled source fails with ``TE.FUNCTION_DOC``.

    Interpretation: Failure indicates that compact or standalone field syntax remains
    accepted.

    Limitations: Module-section spacing and prose quality beyond structure are not
    assessed.
    """
    standalone = VALID_SOURCE.replace(
        b"Evidence ID: SV-TEV-FIX-001", b"Evidence ID\n    SV-TEV-FIX-001", 1
    )
    adjacent = VALID_SOURCE.replace(
        b"SV-TEV-FIX-001\n\n    Requirement:",
        b"SV-TEV-FIX-001\n    Requirement:",
        1,
    )
    excess = VALID_SOURCE.replace(
        b"SV-TEV-FIX-001\n\n    Requirement:",
        b"SV-TEV-FIX-001\n\n\n    Requirement:",
        1,
    )
    standalone_result = SUT().execute(
        PythonConformanceRequest(
            (PythonModuleSource(PATH, standalone),),
            "ownership.json",
            VALID_OWNERSHIP,
        )
    )
    adjacent_result = SUT().execute(
        PythonConformanceRequest(
            (PythonModuleSource(PATH, adjacent),),
            "ownership.json",
            VALID_OWNERSHIP,
        )
    )
    assert (
        tuple(item.code for item in standalone_result.findings).count("TE.FUNCTION_DOC")
        == 1
    )
    excess_result = SUT().execute(
        PythonConformanceRequest(
            (PythonModuleSource(PATH, excess),),
            "ownership.json",
            VALID_OWNERSHIP,
        )
    )
    assert (
        tuple(item.code for item in adjacent_result.findings).count("TE.FUNCTION_DOC")
        == 1
    )
    assert (
        tuple(item.code for item in excess_result.findings).count("TE.FUNCTION_DOC")
        == 1
    )


def test_method__execute_request_type__rejects_foreign_object() -> None:
    """Evidence ID: SV-TEV-022

    Requirement: Execute accepts exactly PythonConformanceRequest values.

    Method: Invoke the public action with a generic foreign object.

    Oracle: The public method contract assigns TypeError to a wrong semantic request
    type.

    Acceptance: The invocation raises TypeError.

    Interpretation: Failure identifies action-boundary type-policy drift.

    Limitations: Correctly typed malformed evidence is represented as findings and
    covered above.
    """
    with pytest.raises(TypeError):
        SUT().execute(object())  # type: ignore[arg-type]


PROFILE_PATH = "harness/pi/evidence/python-test-evidence-profile-matrix-v1.json"
PROFILE_PAYLOAD = (Path(__file__).resolve().parents[6] / PROFILE_PATH).read_bytes()
ROUTINE_SOURCE = b'''r"""Software verification of routine artifact.

Evidence profile: routine

Bounded artifact scope: one controlled routine software artifact.

Facet and represented meaning

This fixture represents one exact routine software contract.

Intrinsic and cross-object scope

The bounded artifact is primary and owns no cross-object scientific behavior.

VVUQ and scientific exclusions

Passing excludes numerical verification, scientific validation, UQ, and acceptance.
"""


def test_artifact__literal_value__equals_itself():
    """Evidence ID: SV-TEV-ROUTINE-FIX-001

    Requirement: The controlled literal retains exact equality.

    Acceptance: Equality is exactly true.
    """
    assert 1 == 1
'''
ROUTINE_OWNERSHIP = json.dumps(
    {
        "schema_version": 1,
        "modules": [
            {
                "path": PATH,
                "mode": "artifact_owned",
                "evidence_class": "software_verification",
                "evidence_profile": "routine",
                "artifact": "routine artifact",
            }
        ],
    },
    separators=(",", ":"),
).encode()


def test_method__execute_routine_profile__accepts_exact_required_fields() -> None:
    """Evidence ID: software-verification.harness.python-conformance.profile.routine

    Requirement: Routine evidence requires Evidence ID, Requirement, and Acceptance
    while its module declares profile, bounded scope, and VVUQ exclusions.

    Method: Validate one literal routine module with only the three required per-test
    fields against the canonical generic profile resource.

    Oracle: HC01 decision D and the canonical profile matrix fix the exact required
    field set independently of validator implementation.

    Acceptance: Validation passes with one retained stable evidence owner.

    Interpretation: Failure identifies profile loading or routine documentation drift.

    Limitations: Semantic assertion quality and human acceptance remain excluded.
    """
    result = SUT().execute(
        PythonConformanceRequest(
            (PythonModuleSource(PATH, ROUTINE_SOURCE),),
            "ownership.json",
            ROUTINE_OWNERSHIP,
            profile_path=PROFILE_PATH,
            profile_payload=PROFILE_PAYLOAD,
        )
    )
    assert result.status == "PASS"
    assert result.unique_evidence_owners == 1


def test_method__execute_routine_profile__rejects_duplicate_optional_field() -> None:
    """Evidence ID: software-verification.harness.python-conformance.profile.optional-unique

    Requirement: Every present optional routine evidence field occurs once in canonical
    order as a paragraph-valid declaration.

    Method: Add two optional Oracle paragraphs to the accepted routine fixture.

    Oracle: The canonical profile makes Oracle optional, not repeatable.

    Acceptance: Validation fails with exactly one function-document finding.

    Interpretation: Failure identifies incomplete optional-field enforcement.

    Limitations: Oracle semantics and scientific adequacy remain excluded.
    """  # noqa: E501
    source = ROUTINE_SOURCE.replace(
        b"    Acceptance: Equality is exactly true.\n",
        b"    Oracle: Literal equality.\n\n    Oracle: Python equality.\n\n"
        b"    Acceptance: Equality is exactly true.\n",
    )
    result = SUT().execute(
        PythonConformanceRequest(
            (PythonModuleSource(PATH, source),),
            "ownership.json",
            ROUTINE_OWNERSHIP,
            profile_path=PROFILE_PATH,
            profile_payload=PROFILE_PAYLOAD,
        )
    )
    assert result.status == "FAIL"
    assert tuple(item.code for item in result.findings).count("TE.FUNCTION_DOC") == 1


@pytest.mark.parametrize(
    "mutation",
    (
        pytest.param("unsupported_schema", id="unsupported_schema"),
        pytest.param("unknown_field", id="unknown_field"),
        pytest.param("missing_class", id="missing_class"),
        pytest.param("missing_profile", id="missing_profile"),
        pytest.param("duplicate_combination", id="duplicate_combination"),
        pytest.param("malformed_requirement", id="malformed_requirement"),
    ),
)
def test_method__execute_profile_matrix__rejects_closed_structure_defects(
    mutation: str,
) -> None:
    """Evidence ID: software-verification.harness.python-conformance.profile.closed

    Requirement: The profile matrix rejects unsupported versions, unknown or missing
    fields, missing classes or profiles, duplicate combinations, and malformed rules.

    Method: Apply one isolated structural mutation to the canonical literal resource.

    Oracle: The accepted closed version-one resource contract enumerates each rejected
    partition.

    Acceptance: Every partition yields exactly a TE.PROFILE_INPUT finding.

    Interpretation: Failure identifies incomplete profile-policy closure.

    Limitations: Resource-manifest hashing and semantic review are separate.
    """
    value = json.loads(PROFILE_PAYLOAD)
    if mutation == "unsupported_schema":
        value["schema_version"] = 2
    elif mutation == "unknown_field":
        value["unknown"] = None
    elif mutation == "missing_class":
        value["evidence_classes"].pop()
    elif mutation == "missing_profile":
        value["profiles"].pop()
    elif mutation == "duplicate_combination":
        value["combinations"].append(value["combinations"][0])
    else:
        value["profiles"][0]["required_test_fields"] = ["unknown"]
    result = SUT().execute(
        PythonConformanceRequest(
            (PythonModuleSource(PATH, ROUTINE_SOURCE),),
            "ownership.json",
            ROUTINE_OWNERSHIP,
            profile_path=PROFILE_PATH,
            profile_payload=json.dumps(value, separators=(",", ":")).encode(),
        )
    )
    assert tuple(item.code for item in result.findings).count("TE.PROFILE_INPUT") == 1


def test_method__execute_module_model__parses_each_source_exactly_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Evidence ID: software-verification.harness.conformance.module.single-pass

    Requirement: One AST parse supplies all rule and repository-conformance owners for
    each selected module.

    Method: Count parser-boundary calls while validating one conforming literal module.

    Oracle: The accepted R2.3 architecture requires exactly one parse per source.

    Acceptance: Validation passes and the parser call count is exactly one.

    Interpretation: Failure identifies duplicated syntax work or parse bypass.

    Limitations: Runtime performance beyond parse count is not measured.
    """
    from ksdft2effmass.harness.pi.evidence.python_conformance import parser

    original = parser.ast.parse
    calls = 0

    def counted_parse(*args: Any, **kwargs: Any) -> Any:
        nonlocal calls
        calls += 1
        return original(*args, **kwargs)

    monkeypatch.setattr(parser.ast, "parse", counted_parse)
    result = SUT().execute(
        PythonConformanceRequest(
            (PythonModuleSource(PATH, VALID_SOURCE),),
            "ownership.json",
            VALID_OWNERSHIP,
        )
    )
    assert result.status == "PASS"
    assert calls == 1


def test_method__execute_private_class_owner__reports_ownership_finding() -> None:
    """Evidence ID: software-verification.harness.conformance.ownership.private-class

    Requirement: Class-owned evidence is limited to a public class as sole SUT.

    Method: Supply a closed ownership entry naming one private implementation class.

    Oracle: The R2.3 ownership contract prohibits leading-underscore class owners.

    Acceptance: Validation reports TE.PRIVATE_CLASS_OWNER.

    Interpretation: Failure permits private implementation to masquerade as public API.

    Limitations: Cohesion of an accepted artifact-owned replacement is reviewed
    separately.
    """
    ownership = json.dumps(
        {
            "schema_version": 1,
            "modules": [
                {
                    "path": PATH,
                    "mode": "class_owned",
                    "evidence_class": "software_verification",
                    "sut": "_Private",
                }
            ],
        },
        separators=(",", ":"),
    ).encode()
    result = SUT().execute(
        PythonConformanceRequest(
            (PythonModuleSource(PATH, VALID_SOURCE),),
            "ownership.json",
            ownership,
        )
    )
    assert "TE.PRIVATE_CLASS_OWNER" in tuple(item.code for item in result.findings)
