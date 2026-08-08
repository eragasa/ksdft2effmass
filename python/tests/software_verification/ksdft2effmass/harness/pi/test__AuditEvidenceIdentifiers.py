r"""Software verification of ``AuditEvidenceIdentifiers``.

Facet and represented meaning
Software verification of the public evidence-identifier and executable-marker audit.

Intrinsic and cross-object scope
The sole primary SUT is ``AuditEvidenceIdentifiers``. Caller-supplied module bytes and
an explicit project profile are the complete operation boundary.

VVUQ and scientific exclusions
Passing establishes only the stated structural software contract. Semantic cohesion,
oracle independence, numerical correctness, scientific validation, uncertainty
quantification, and human acceptance are excluded.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from ksdft2effmass.harness.pi import (
    AuditEvidenceIdentifiers,
    DeserializeJsonRecord,
    EvidenceAuditResult,
    ProjectProfile,
    WireRecordKind,
)

pytestmark = pytest.mark.software_verification
SUT = AuditEvidenceIdentifiers


def load_profile() -> ProjectProfile:
    """Evidence ID
    Owns no identifier; supports action evidence.
    Requirement
    Action tests require one independently valid explicit profile.
    Method
    Decode the maintained generic profile fixture through the public decoder.
    Oracle
    The accepted fixture and public decoder define valid support input.
    Acceptance
    Return one ProjectProfile.
    Interpretation
    Failure identifies invalid setup rather than audit behavior.
    Limitations
    This helper owns no independent evidence claim.
    """
    root = Path(__file__).resolve().parents[6]
    decoded = DeserializeJsonRecord().execute(
        WireRecordKind.ProjectProfile,
        (root / "harness/pi/fixtures/valid/project-profile.json").read_bytes(),
    )
    assert isinstance(decoded.record, ProjectProfile)
    return decoded.record


def source(docstring: str, marker: str = "verification_alpha") -> bytes:
    """Evidence ID
    Owns no identifier; supports action evidence.
    Requirement
    Parser tests require deterministic marked source with a known function line.
    Method
    Interpolate controlled docstring and marker text into fixed Python source.
    Oracle
    Python source syntax fixes the represented support module.
    Acceptance
    Return UTF-8 bytes with the test function on line three.
    Interpretation
    Failure identifies test setup drift.
    Limitations
    This helper does not determine audit acceptance.
    """
    return (
        f"import pytest\npytestmark = pytest.mark.{marker}\n"
        f'def test_owner():\n    """{docstring}"""\n'
    ).encode()


def issue_codes(result: EvidenceAuditResult) -> list[str]:
    """Evidence ID
    Owns no identifier; supports action evidence.
    Requirement
    Assertions require a visible projection of public issue codes.
    Method
    Read codes from the public ValidationResult issues.
    Oracle
    Public result fields define the exact projection.
    Acceptance
    Return codes in retained result order.
    Interpretation
    Failure identifies result-shape drift.
    Limitations
    This helper does not reproduce issue classification policy.
    """
    return [issue.code for issue in result.validation.issues]


def test_constructor__action_object__is_stateless_and_fieldless() -> None:
    """Evidence ID
    ``SV-HARNESS-033``.
    Requirement
    AuditEvidenceIdentifiers is a concrete stateless ActionObject.
    Method
    Construct two instances and inspect their public storage boundary.
    Oracle
    The accepted action contract requires no retained root, profile, cache, client,
    or mutable state.
    Acceptance
    Construction succeeds and instances expose no instance dictionary or fields.
    Interpretation
    Failure identifies production or accepted-contract drift.
    Limitations
    This is exact software verification only.
    """
    first = SUT()
    second = SUT()
    assert not hasattr(first, "__dict__")
    assert not hasattr(second, "__dict__")
    assert SUT.__slots__ == ()


def test_method__execute__normalizes_indented_field_and_preserves_line() -> None:
    """Evidence ID
    ``SV-HARNESS-113``.
    Requirement
    An indented multiline Evidence ID field owns one occurrence at the function line.
    Method
    Supply convention-compliant source bytes with a fielded owner declaration.
    Oracle
    The accepted test-evidence convention and one-based function-line contract are
    independent exact oracles.
    Acceptance
    The audit passes with VX-A-001 at line three and no ID_INVALID finding.
    Interpretation
    Failure reproduces the reported clean=False indentation defect.
    Limitations
    Exact docstring-field source positioning is not reported separately.
    """
    payload = source(
        "Summary.\n\n    Evidence ID\n        ``VX-A-001``.\n"
        "    Requirement\n        Public behavior."
    )
    result = SUT().execute(
        (("tests/classification-alpha/test_owner.py", payload),), load_profile()
    )
    assert result.validation.status == "PASS"
    assert [(item.evidence_id, item.line) for item in result.occurrences] == [
        ("VX-A-001", 3)
    ]
    assert "PIH.EVIDENCE.ID_INVALID" not in issue_codes(result)


def test_method__execute__accepts_historical_first_line_owner() -> None:
    """Evidence ID
    ``SV-HARNESS-114``.
    Requirement
    A historical first-line declaration remains an accepted owner.
    Method
    Supply one marked module whose test docstring starts with an identifier.
    Oracle
    The current compatibility contract explicitly retains first-line ownership.
    Acceptance
    The action passes with exactly VX-A-002.
    Interpretation
    Failure indicates incompatible removal of accepted historical syntax.
    Limitations
    No historical file is changed by this test.
    """
    result = SUT().execute(
        (
            (
                "tests/classification-alpha/test_owner.py",
                source("VX-A-002: historical owner description."),
            ),
        ),
        load_profile(),
    )
    assert result.validation.status == "PASS"
    assert [item.evidence_id for item in result.occurrences] == ["VX-A-002"]


def test_method__execute__expands_inclusive_range_in_deterministic_order() -> None:
    """Evidence ID
    ``SV-HARNESS-115``.
    Requirement
    One permitted inclusive same-prefix range expands in deterministic occurrence order.
    Method
    Supply modules in reverse path order with a three-ID range and one single owner.
    Oracle
    Inclusive integer expansion and the public ID/path/line sort contract are exact.
    Acceptance
    Four occurrences are ordered by identifier, then path and line.
    Interpretation
    Failure indicates range-boundary or deterministic-ordering drift.
    Limitations
    Parameter collection semantics are outside this AST audit.
    """
    ranged = source(
        "Evidence ID\n    ``VX-A-001`` through ``VX-A-003``\n"
        "Requirement\n    Shared parameterized behavior."
    )
    single = source("VX-A-004: historical owner.")
    result = SUT().execute(
        (
            ("tests/classification-alpha/test_z.py", single),
            ("tests/classification-alpha/test_a.py", ranged),
        ),
        load_profile(),
    )
    assert result.validation.status == "PASS"
    assert [item.evidence_id for item in result.occurrences] == [
        "VX-A-001",
        "VX-A-002",
        "VX-A-003",
        "VX-A-004",
    ]


@pytest.mark.parametrize(
    ("declaration", "expected_code"),
    (
        pytest.param(
            "Evidence ID\n    ``VX-A-001``.\nEvidence ID\n"
            "    ``VX-A-002``.\nRequirement\n    X.",
            "PIH.EVIDENCE.ID_INVALID",
            id="multiple_fields",
        ),
        pytest.param(
            "Evidence ID\nRequirement\n    X.",
            "PIH.EVIDENCE.ID_INVALID",
            id="empty_field",
        ),
        pytest.param(
            "Evidence ID\n    VX-A-001 and VX-A-002.\nRequirement\n    X.",
            "PIH.EVIDENCE.RANGE_CONFLICT",
            id="independent_ids",
        ),
        pytest.param(
            "Evidence ID\n    VX-A-003 through VX-A-001.\nRequirement\n    X.",
            "PIH.EVIDENCE.RANGE_CONFLICT",
            id="descending_range",
        ),
        pytest.param(
            "Evidence ID\n    VX-A-001 through VX-B-003.\nRequirement\n    X.",
            "PIH.EVIDENCE.RANGE_CONFLICT",
            id="cross_prefix_range",
        ),
        pytest.param(
            "Evidence ID\n    VX-A-XYZ.\nRequirement\n    X.",
            "PIH.EVIDENCE.ID_INVALID",
            id="malformed_identifier",
        ),
    ),
)
def test_method__execute__rejects_invalid_owner_declarations(
    declaration: str, expected_code: str
) -> None:
    """Evidence ID
    ``SV-HARNESS-116``.
    Requirement
    Ambiguous, empty, malformed, descending, and cross-prefix declarations fail closed.
    Method
    Audit explicit semantic declaration partitions in one otherwise valid module.
    Oracle
    The accepted evidence-ID grammar fixes each exact issue-code partition.
    Acceptance
    Each partition fails with only its expected declaration issue code.
    Interpretation
    Failure indicates grammar acceptance or issue-classification drift.
    Limitations
    Namespace and module-marker failures are covered separately.
    """
    result = SUT().execute(
        (("tests/classification-alpha/test_owner.py", source(declaration)),),
        load_profile(),
    )
    assert result.occurrences == ()
    assert issue_codes(result) == [expected_code]


@pytest.mark.parametrize(
    ("path", "payload", "expected_code"),
    (
        pytest.param(
            "tests/classification-alpha/test_owner.py",
            source("VX-B-001: wrong scope namespace."),
            "PIH.EVIDENCE.NAMESPACE_UNDECLARED",
            id="namespace_violation",
        ),
        pytest.param(
            "outside/test_owner.py",
            source("VX-A-001: outside scope."),
            "PIH.EVIDENCE.NAMESPACE_UNDECLARED",
            id="scope_violation",
        ),
        pytest.param(
            "tests/classification-alpha/test_owner.py",
            b'def test_owner():\n    """VX-A-001"""\n',
            "PIH.EVIDENCE.MARKER_UNDECLARED",
            id="missing_marker",
        ),
        pytest.param(
            "tests/classification-alpha/test_owner.py",
            source("VX-A-001: owner.", marker="verification_beta"),
            "PIH.EVIDENCE.MARKER_UNDECLARED",
            id="incorrect_marker",
        ),
        pytest.param(
            "tests/classification-alpha/test_owner.py",
            b"import pytest\npytestmark = (pytest.mark.verification_alpha, "
            b"pytest.mark.verification_beta)\n"
            b'def test_owner():\n    """VX-A-001"""\n',
            "PIH.EVIDENCE.MARKER_UNDECLARED",
            id="multiple_markers",
        ),
        pytest.param(
            "tests/classification-alpha/test_owner.py",
            b"\xff",
            "PIH.EVIDENCE.SOURCE_INVALID",
            id="invalid_utf8",
        ),
        pytest.param(
            "tests/classification-alpha/test_owner.py",
            b"not python !",
            "PIH.EVIDENCE.SOURCE_INVALID",
            id="invalid_python",
        ),
    ),
)
def test_method__execute_valid_and_invalid__returns_exact_partition(
    path: str, payload: bytes, expected_code: str
) -> None:
    """Evidence ID
    ``SV-HARNESS-057``.
    Requirement
    Invalid source, scope, namespace, and executable-marker partitions fail closed.
    Method
    Invoke the action with one controlled invalid partition at a time.
    Oracle
    Explicit profile rules and Python decoding/parsing provide exact public oracles.
    Acceptance
    Each result has no occurrences and includes the expected closed issue code.
    Interpretation
    Failure indicates input, scope, marker, or issue-ordering drift.
    Limitations
    This structural check does not execute the supplied source.
    """
    result = SUT().execute(((path, payload),), load_profile())
    assert result.occurrences == ()
    assert expected_code in issue_codes(result)


def test_method__execute__reports_duplicate_and_protected_gap_deterministically() -> (
    None
):
    """Evidence ID
    ``SV-HARNESS-117``.
    Requirement
    Duplicate executable ownership fails and exact protected gaps warn
    deterministically.
    Method
    Audit reversed duplicate modules and one profile-declared unowned function twice.
    Oracle
    Public issue ordering, duplicate code, and the protected-gap profile tuple are
    exact.
    Acceptance
    Reversed inputs produce equal ordered issues; the protected gap is one warning.
    Interpretation
    Failure indicates owner uniqueness, profile debt, or deterministic-ordering drift.
    Limitations
    Protected debt is controlled fixture input, not current repository debt.
    """
    first = (
        "tests/classification-alpha/test_b.py",
        b'def test_owner():\n    """VX-A-001: owner."""\n',
    )
    second = ("tests/classification-alpha/test_a.py", source("VX-A-001: owner."))
    forward = SUT().execute((first, second), load_profile())
    reverse = SUT().execute((second, first), load_profile())
    assert forward.validation == reverse.validation
    assert issue_codes(forward) == [
        "PIH.EVIDENCE.ID_DUPLICATE",
        "PIH.EVIDENCE.MARKER_UNDECLARED",
    ]

    path = "tests/classification-alpha/test_gap.py"
    profile = replace(
        load_profile(), protected_unowned_functions=((path, "test_owner"),)
    )
    gap = SUT().execute(((path, source("")),), profile)
    assert gap.validation.status == "WARN"
    assert issue_codes(gap) == ["PIH.EVIDENCE.PROTECTED_GAP"]


def test_method__execute__uses_only_supplied_modules_from_any_cwd(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Evidence ID
    ``SV-HARNESS-118``.
    Requirement
    Execution is explicit-input only and independent of repository discovery and CWD.
    Method
    Change to a temporary nonrepository directory containing an invalid Python file,
    then supply only one valid in-memory module.
    Oracle
    The public signature contains no root, discovery, Git, or filesystem input.
    Acceptance
    The supplied module passes and the unsupplied local file has no effect.
    Interpretation
    Failure indicates hidden discovery or CWD coupling.
    Limitations
    Filesystem write behavior is excluded because the action receives bytes only.
    """
    (tmp_path / "test_unlisted.py").write_bytes(b"not python !")
    monkeypatch.chdir(tmp_path)
    result = SUT().execute(
        (
            (
                "tests/classification-alpha/test_owner.py",
                source("VX-A-001: explicit owner."),
            ),
        ),
        load_profile(),
    )
    assert result.validation.status == "PASS"
    assert [item.path for item in result.occurrences] == [
        "tests/classification-alpha/test_owner.py"
    ]
