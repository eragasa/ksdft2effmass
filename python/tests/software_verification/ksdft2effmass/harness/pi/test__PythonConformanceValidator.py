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

import ast
import json
from dataclasses import FrozenInstanceError, fields, is_dataclass
from pathlib import Path
from typing import Any

import pytest

from ksdft2effmass.harness.pi.conformance.python import (
    PythonConformanceRequest,
    PythonConformanceResult,
    PythonConformanceValidator,
    PythonModuleSource,
)
from ksdft2effmass.harness.pi.conformance.python.corpus import (
    _PythonTestModuleCorpusBuilder,
    _PythonTestModuleInput,
)
from ksdft2effmass.harness.pi.conformance.python.documentation import (
    _PythonDocumentationRule,
)
from ksdft2effmass.harness.pi.conformance.python.evidence import (
    _PythonEvidenceIdentifierRule,
)
from ksdft2effmass.harness.pi.conformance.python.naming import (
    _PythonNamingRule,
)
from ksdft2effmass.harness.pi.conformance.python.ownership import (
    _PythonOwnershipRule,
)
from ksdft2effmass.harness.pi.conformance.python.parameterization import (
    _PythonParameterizationRule,
)
from ksdft2effmass.harness.pi.conformance.python.parser import parse_module
from ksdft2effmass.harness.pi.conformance.python.repository import (
    _PythonRepositoryConformanceRule,
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


def controlled_source(declaration: bytes, assertions: bytes) -> bytes:
    """Evidence ID: Owns no identifier; supports numeric export-count evidence.

    Requirement: Controlled rule evidence needs one otherwise conforming source with
    explicit module declarations and assertion statements.

    Method: Insert exact caller-supplied bytes into the fixed valid source fixture.

    Oracle: The two fixed replacement anchors identify the declaration and assertion
    locations independently of the rule under test.

    Acceptance: Return source bytes containing each supplied fragment exactly once.

    Interpretation: Failure identifies fixture construction rather than rule behavior.

    Limitations: This helper executes neither the generated source nor its assertions.
    """
    source = VALID_SOURCE.replace(
        b"\n\ndef test_artifact__literal_value__equals_itself():",
        b"\n\n"
        + declaration
        + b"\n\ndef test_artifact__literal_value__equals_itself():",
        1,
    )
    return source.replace(b"    assert 1 == 1", assertions, 1)


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


def test_method__execute_private_target__retains_artifact_ownership() -> None:
    """Evidence ID: software-verification.harness.python-conformance.private-target

    Requirement: A routine artifact-owned module may directly test one imported private
    implementation class through the exact ``test___ClassName.py`` filename while the
    evidence owner remains the represented subsystem artifact.

    Method: Supply a literal routine module whose private SUT assignment, explicit
    import, filename, and artifact ownership declaration agree exactly.

    Oracle: The accepted private-target/artifact-owner distinction fixes the exact
    filename and retains ``artifact_owned`` rather than ``class_owned`` ownership.

    Acceptance: Validation passes with one artifact-owned module and no class-owned
    module.

    Interpretation: Failure identifies private-target filename or ownership-mode drift.

    Limitations: The private target is implementation access only and is not a public
    API or class-owned evidence owner.
    """
    path = "test___PrivateCodec.py"
    source = b'''r"""Software verification of private codec subsystem artifact.

Evidence profile: routine

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

Routine verification of one private codec target.

Intrinsic and cross-object scope

The subsystem artifact is primary.

VVUQ and scientific exclusions

Passing establishes software structure only, not validation or UQ.
"""

from demo import _PrivateCodec

SUT = _PrivateCodec


def test_artifact__codec__retains_literal_contract():
    """Evidence ID: software-verification.fixture.private-codec.literal-contract

    Requirement: The controlled private codec fixture retains exact construction.

    Method: Construct the controlled fixture through its private target alias.

    Oracle: Exact Python class construction supplies the result.

    Acceptance: Construction returns one private codec instance.

    Interpretation: Failure identifies controlled fixture drift.

    Limitations: This fixture makes no public API or scientific claim.
    """
    assert type(SUT()) is SUT
'''
    ownership = json.dumps(
        {
            "schema_version": 1,
            "modules": [
                {
                    "path": path,
                    "mode": "artifact_owned",
                    "evidence_class": "software_verification",
                    "evidence_profile": "routine",
                    "artifact": "private codec subsystem artifact",
                }
            ],
        },
        separators=(",", ":"),
    ).encode()
    result = SUT().execute(
        PythonConformanceRequest(
            (PythonModuleSource(path, source),), "ownership.json", ownership
        )
    )
    assert result.status == "PASS"
    assert result.artifact_owned_modules == 1
    assert result.class_owned_modules == 0


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


def test_artifact__parsed_module_model__is_deeply_immutable_at_rule_boundary() -> None:
    """Evidence ID: software-verification.harness.python-conformance.model.deep-immutability

    Requirement: The one parsed module model exposes immutable derived values and no
    mutable AST or function-node collection to independent rule owners.

    Method: Parse one literal module, inspect its public surface, and attempt mutation.

    Oracle: Frozen dataclass semantics and tuple-valued names define the boundary.

    Acceptance: Public AST attributes are absent, names are a tuple, and assignment
    raises ``FrozenInstanceError``.

    Interpretation: Failure indicates mutable syntax escaping the parser owner.

    Limitations: Python's deliberate low-level object introspection is excluded.
    """  # noqa: E501
    model = parse_module(PATH, ROUTINE_SOURCE)
    assert model.function_names == ("test_artifact__literal_value__equals_itself",)
    assert not hasattr(model, "tree")
    assert isinstance(model.functions, tuple)
    assert all(type(value).__module__ != "ast" for value in model.functions)
    assert model.source_bytes == ROUTINE_SOURCE
    assert model.source_byte_count == len(ROUTINE_SOURCE)
    assert len(model.source_sha256) == 64
    assert not hasattr(model, "_tree")
    assert not hasattr(model, "_functions")
    with pytest.raises(FrozenInstanceError):
        model.path = "changed.py"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        model.functions[0].name = "changed"  # type: ignore[misc]


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
    from ksdft2effmass.harness.pi.conformance.python import parser

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


@pytest.mark.parametrize(
    ("declaration", "assertions"),
    (
        pytest.param(
            b"",
            b"    assert len(api.__all__) == 2",
            id="direct_all_literal",
        ),
        pytest.param(
            b'EXPECTED = ("A", "B")',
            b"    assert tuple(api.__all__) == EXPECTED\n    assert len(EXPECTED) == 2",
            id="linked_inventory_literal",
        ),
        pytest.param(
            b"",
            b"    assert len(api.__all__)",
            id="count_truthiness",
        ),
        pytest.param(
            b"from demo import __all__ as EXPORTED",
            b"    assert len(EXPORTED) == 2",
            id="imported_all_alias",
        ),
        pytest.param(
            b"EXPORTED = api.__all__",
            b"    assert len(EXPORTED)",
            id="assigned_all_alias",
        ),
        pytest.param(
            b"",
            b"    exported = api.__all__\n"
            b"    second = exported\n"
            b"    assert len(second) == 2",
            id="local_transitive_alias",
        ),
    ),
)
def test_method__execute_numeric_export_count__reports_structural_finding(
    declaration: bytes, assertions: bytes
) -> None:
    """Evidence ID: software-verification.harness.export-count.rule

    Requirement: Maintained tests must not bind package export completeness to a
    literal numeric count, directly or through names linked to ``__all__``.

    Method: Validate controlled sources containing literal, inventory-linked,
    count-truthiness, imported-alias, assigned-alias, and local transitive-alias
    export assertions.

    Oracle: The v1 testing requirement permits exact export-name inventories but
    prohibits numeric export totals as unstable nonsemantic duplication.

    Acceptance: Every prohibited partition yields exactly one
    ``TE.NUMERIC_EXPORT_COUNT`` finding.

    Interpretation: Failure permits fixed export totals to return to maintained test
    evidence or rejects the wrong structural boundary.

    Limitations: Semantic accuracy of the expected export names remains review-owned.
    """
    result = SUT().execute(
        PythonConformanceRequest(
            (PythonModuleSource(PATH, controlled_source(declaration, assertions)),),
            "ownership.json",
            VALID_OWNERSHIP,
        )
    )
    assert (
        tuple(item.code for item in result.findings).count("TE.NUMERIC_EXPORT_COUNT")
        == 1
    )


@pytest.mark.parametrize(
    ("declaration", "assertions"),
    (
        pytest.param(
            b'EXPECTED = ("A", "B")',
            b"    assert tuple(api.__all__) == EXPECTED",
            id="exact_inventory",
        ),
        pytest.param(
            b"VALUES = (1, 2)",
            b"    assert len(VALUES) == 2",
            id="unrelated_length",
        ),
    ),
)
def test_method__execute_noncount_export_checks__remain_allowed(
    declaration: bytes, assertions: bytes
) -> None:
    """Evidence ID: software-verification.harness.python-conformance.export-contract

    Requirement: The numeric export-count rule must preserve exact export-name
    comparison and unrelated length assertions.

    Method: Validate one exact ``__all__`` inventory comparison and one unrelated
    literal length check.

    Oracle: Only numeric completeness claims about an export surface are prohibited.

    Acceptance: Both controlled sources pass structural validation without a numeric
    export-count finding.

    Interpretation: Failure broadens the rule beyond the authorized export-count
    boundary.

    Limitations: This test does not execute either controlled assertion.
    """
    result = SUT().execute(
        PythonConformanceRequest(
            (PythonModuleSource(PATH, controlled_source(declaration, assertions)),),
            "ownership.json",
            VALID_OWNERSHIP,
        )
    )
    assert result.status == "PASS"
    assert all(item.code != "TE.NUMERIC_EXPORT_COUNT" for item in result.findings)


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


@pytest.mark.parametrize(
    ("label", "defect"),
    (
        pytest.param("Method", "valid", id="method_valid"),
        pytest.param("Oracle", "valid", id="oracle_valid"),
        pytest.param("Interpretation", "valid", id="interpretation_valid"),
        pytest.param("Limitations", "valid", id="limitations_valid"),
        pytest.param("Method", "empty", id="method_empty"),
        pytest.param("Oracle", "wrong_order", id="oracle_wrong_order"),
        pytest.param("Oracle", "duplicate", id="oracle_duplicate"),
        pytest.param("Method", "zero_spacing", id="method_zero_spacing"),
        pytest.param(
            "Interpretation", "excess_spacing", id="interpretation_excess_spacing"
        ),
        pytest.param("Limitations", "absorption", id="limitations_absorption"),
    ),
)
def test_method__execute_optional_paragraphs__enforces_exact_present_grammar(
    label: str, defect: str
) -> None:
    """Evidence ID: software-verification.harness.python-conformance.optional-paragraphs

    Requirement: Method, Oracle, Interpretation, and Limitations remain optional for
    routine evidence, while every present optional field uses the exact paragraph
    grammar, canonical order, nonempty content, uniqueness, and one blank separator.

    Method: Insert one valid optional field or one isolated malformed present-field
    partition into the accepted routine source and execute structural validation.

    Oracle: The routine profile and exact Label-value paragraph grammar fix every
    accepted and rejected semantic partition.

    Acceptance: Valid partitions pass; empty, misordered, duplicate, zero-spacing,
    excess-spacing, and following-field absorption partitions each yield exactly one
    function-document finding.

    Interpretation: Failure identifies optionality being confused with lax grammar.

    Limitations: Prose truth and semantic oracle independence remain separate.
    """
    before = label in {"Method", "Oracle"}
    anchor = b"    Acceptance: Equality is exactly true." if before else b'    """'
    paragraph = f"    {label}: Controlled optional detail.".encode()
    if defect == "valid":
        replacement = paragraph + b"\n\n" + anchor
    elif defect == "empty":
        replacement = f"    {label}:\n\n".encode() + anchor
    elif defect == "wrong_order":
        anchor = b'    """'
        replacement = paragraph + b"\n\n" + anchor
    elif defect == "duplicate":
        replacement = paragraph + b"\n\n" + paragraph + b"\n\n" + anchor
    elif defect == "zero_spacing":
        replacement = paragraph + b"\n" + anchor
    elif defect == "excess_spacing":
        replacement = (
            paragraph
            + b"\n\n\n    Limitations: Following optional detail.\n\n"
            + anchor
        )
    else:
        replacement = (
            paragraph + b"\n    Provenance: Following optional detail.\n\n" + anchor
        )
    if anchor == b'    """':
        prefix, separator, suffix = ROUTINE_SOURCE.rpartition(anchor)
        assert separator == anchor
        source = prefix + b"\n" + replacement + suffix
    else:
        source = ROUTINE_SOURCE.replace(anchor, replacement, 1)
    result = SUT().execute(
        PythonConformanceRequest(
            (PythonModuleSource(PATH, source),),
            "ownership.json",
            ROUTINE_OWNERSHIP,
            profile_path=PROFILE_PATH,
            profile_payload=PROFILE_PAYLOAD,
        )
    )
    function_docs = tuple(
        item for item in result.findings if item.code == "TE.FUNCTION_DOC"
    )
    if defect == "valid":
        assert result.status == "PASS"
        assert function_docs == ()
    else:
        assert len(function_docs) == 1


def test_artifact__immutable_corpus__contains_only_deeply_immutable_ast_free_facts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Evidence ID: software-verification.harness.python-conformance.corpus.immutable

    Requirement: The corpus and every recursively contained or accessor-returned fact
    are frozen, AST-free, and free of mutable containers.

    Method: Build one corpus, recursively inspect all dataclass fields and accessors,
    then attempt nested assignment.

    Oracle: Frozen dataclasses, enums, scalars, bytes, and tuples are the complete
    accepted fact vocabulary.

    Acceptance: Recursive inspection finds no AST or mutable container and nested
    assignment raises FrozenInstanceError.

    Interpretation: Failure identifies mutable or parser-owned state crossing corpus.

    Limitations: Deliberate low-level object introspection is excluded.
    """
    corpus = _PythonTestModuleCorpusBuilder().execute(
        (_PythonTestModuleInput(PATH, ROUTINE_SOURCE),)
    )

    def inspect(value: object) -> object:
        assert not isinstance(value, ast.AST)
        assert not isinstance(value, (list, dict, set, bytearray))
        if is_dataclass(value) and not isinstance(value, type):
            assert all(
                (inspect(getattr(value, field.name)), True)[1]
                for field in fields(value)
            )
        elif isinstance(value, tuple):
            assert all((inspect(item), True)[1] for item in value)
        return None

    inspect(corpus)
    inspect(corpus.models[0].function_names)
    inspect(corpus.models[0].functions[0].is_test)
    inspect(corpus.model_for(PATH))
    with pytest.raises(FrozenInstanceError):
        corpus.models[0].functions[0].name = "changed"  # type: ignore[misc]


def test_artifact__rule_owners__reuse_corpus_without_parse_or_filesystem_read(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Evidence ID: software-verification.harness.python-conformance.rules.no-reparse

    Requirement: Every named rule owner consumes the immutable corpus model without
    parsing source or reading a filesystem.

    Method: Build one model, prohibit AST parsing and Path reads, then execute naming,
    documentation, ownership, parameterization, evidence, and repository rule owners.

    Oracle: Rule owners accept only explicit immutable facts and policy inputs.

    Acceptance: Every owner completes after both prohibited boundaries are installed.

    Interpretation: Failure identifies duplicated syntax or ambient filesystem work.

    Limitations: Initial corpus construction intentionally performs its one AST parse.
    """
    corpus = _PythonTestModuleCorpusBuilder().execute(
        (_PythonTestModuleInput(PATH, ROUTINE_SOURCE),)
    )
    model = corpus.models[0]

    def prohibited(*args: Any, **kwargs: Any) -> Any:
        raise AssertionError("rule owner crossed parser or filesystem boundary")

    monkeypatch.setattr(
        "ksdft2effmass.harness.pi.conformance.python.parser.ast.parse",
        prohibited,
    )
    monkeypatch.setattr(Path, "read_bytes", prohibited)
    owner = json.loads(ROUTINE_OWNERSHIP)["modules"][0]
    assert _PythonNamingRule().execute(model) == ()
    docs = _PythonDocumentationRule().execute(model, "routine", None)
    assert docs.module_findings == ()
    assert _PythonOwnershipRule().execute(model, owner) == ()
    assert _PythonParameterizationRule().execute(model).findings == ()
    assert _PythonEvidenceIdentifierRule().execute(model, {}) == ()
    assert _PythonRepositoryConformanceRule().execute(model).findings == ()


def test_artifact__corpus_builder__defensively_owns_caller_source_inventory() -> None:
    """Evidence ID: software-verification.harness.python-conformance.corpus.defensive

    Requirement: Mutating a caller-owned source inventory after construction cannot
    alter a built corpus or its source identity facts.

    Method: Build from a caller list, replace and clear that list, and inspect corpus
    bytes, digest, byte count, and model inventory.

    Oracle: The builder snapshots inputs into frozen dataclasses and tuples.

    Acceptance: Corpus state remains exactly equal to the original source snapshot.

    Interpretation: Failure identifies aliasing across the corpus boundary.

    Limitations: Bytes are intrinsically immutable under Python semantics.
    """
    caller_inputs = [_PythonTestModuleInput(PATH, ROUTINE_SOURCE)]
    corpus = _PythonTestModuleCorpusBuilder().execute(caller_inputs)  # type: ignore[arg-type]
    caller_inputs[0] = _PythonTestModuleInput("changed.py", b"pass\n")
    caller_inputs.clear()
    assert tuple(model.path for model in corpus.models) == (PATH,)
    assert corpus.models[0].source_bytes == ROUTINE_SOURCE
    assert corpus.models[0].source_byte_count == len(ROUTINE_SOURCE)
    assert len(corpus.models[0].source_sha256) == 64
