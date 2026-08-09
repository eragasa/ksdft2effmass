r"""Software verification of ``HumanReviewTarget``.

Facet and represented meaning

Software verification of the exact immutable identity and scope of one human-review
target.

Intrinsic and cross-object scope

The sole primary SUT is ``HumanReviewTarget``. Lexical target invariants are intrinsic;
packet compatibility and human disposition are excluded.

VVUQ and scientific exclusions

Passing establishes only the stated software contract. Numerical verification,
scientific validation, uncertainty quantification, repository existence, and human
acceptance are excluded.
"""

from dataclasses import FrozenInstanceError, replace

import pytest

from ksdft2effmass.harness.pi import HumanReviewTarget

pytestmark = pytest.mark.software_verification
SUT = HumanReviewTarget
REVISION = "a" * 40
PATHS = ("python/src/example.py", "python/tests/test_example.py")


def make_target() -> HumanReviewTarget:
    """Evidence ID: Owns no identifier; supports target evidence.

    Requirement: Target tests require one intrinsically valid value.

    Method: Construct one target from fixed public inputs.

    Oracle: The accepted constructor contract defines valid support input.

    Acceptance: Return one HumanReviewTarget.

    Interpretation: Failure identifies setup drift.

    Limitations: This helper owns no independent evidence claim.
    """
    return SUT(
        "human-review.example",
        REVISION,
        "ExampleSubject",
        PATHS,
        "software_verification",
        ("docs/contract.md",),
    )


def test_constructor__exact_value__owns_tuples_and_preserves_declared_order() -> None:
    """Evidence ID: ``SV-HARNESS-123``.

    Requirement: A target stores exact built-in values and defensively owns ordered path
    tuples.

    Method: Construct from explicit tuples and inspect every public field.

    Oracle: The accepted target field contract and built-in tuple semantics are exact.

    Acceptance: Values are unchanged, stored collections are exact tuples, and order is
    preserved.

    Interpretation: Failure identifies field, canonical ownership, or ordering drift.

    Limitations: No path existence or Git identity is checked.
    """

    paths = PATHS
    references = ("docs/contract.md",)
    target = SUT(
        "human-review.example",
        REVISION,
        "ExampleSubject",
        paths,
        "software_verification",
        references,
    )
    assert target == make_target()
    assert type(target.paths) is tuple
    assert type(target.contract_references) is tuple
    assert target.paths == PATHS
    assert target.paths is not paths
    assert target.contract_references is not references
    assert all(type(value) is str for value in target.paths)


def test_field__immutability__has_exact_value_semantics() -> None:
    """Evidence ID: ``SV-HARNESS-124``.

    Requirement: Target state is frozen and equal targets have exact value semantics.

    Method: Compare independently constructed targets and attempt field mutation.

    Oracle: Frozen dataclass and exact field equality semantics define acceptance.

    Acceptance: Equal construction compares equal and assignment raises
    FrozenInstanceError.

    Interpretation: Failure identifies mutability or equality drift.

    Limitations: Hash stability across interpreter implementations is not claimed.
    """
    first = make_target()
    second = make_target()
    assert first == second
    assert first is not second
    with pytest.raises(FrozenInstanceError):
        first.revision = "b" * 40  # type: ignore[misc]


@pytest.mark.parametrize(
    "evidence_class",
    (
        pytest.param("software_verification", id="software_verification"),
        pytest.param("numerical_verification", id="numerical_verification"),
        pytest.param("scientific_validation", id="scientific_validation"),
        pytest.param("uncertainty_quantification", id="uncertainty_quantification"),
        pytest.param("not_applicable", id="not_applicable"),
    ),
)
def test_constructor__evidence_class__accepts_closed_vocabulary(
    evidence_class: str,
) -> None:
    """Evidence ID: ``SV-HARNESS-125``.

    Requirement: The target accepts every and only every declared evidence-class value.

    Method: Replace the evidence class with each semantic member of the closed
    vocabulary.

    Oracle: The public five-value vocabulary is the independent exact oracle.

    Acceptance: Every declared value is retained exactly.

    Interpretation: Failure identifies vocabulary or storage drift.

    Limitations: Construction does not establish evidence adequacy.
    """
    assert (
        replace(make_target(), evidence_class=evidence_class).evidence_class
        == evidence_class
    )


@pytest.mark.parametrize(
    ("field", "value", "exception"),
    (
        pytest.param("review_id", "", ValueError, id="empty_review_id"),
        pytest.param(
            "review_id", "contains space", ValueError, id="malformed_review_id"
        ),
        pytest.param("review_id", 7, TypeError, id="non_string_review_id"),
        pytest.param("revision", "A" * 40, ValueError, id="uppercase_revision"),
        pytest.param("revision", "a" * 39, ValueError, id="short_revision"),
        pytest.param("revision", 7, TypeError, id="non_string_revision"),
        pytest.param("represented_subject", " ", ValueError, id="blank_subject"),
        pytest.param(
            "evidence_class",
            "verification",
            ValueError,
            id="closed_vocabulary_violation",
        ),
    ),
)
def test_constructor__identity_fields__rejects_malformed_values(
    field: str, value: object, exception: type[Exception]
) -> None:
    """Evidence ID: ``SV-HARNESS-126``.

    Requirement: Identity, revision, subject, and vocabulary fields fail closed by
    semantic type.

    Method: Replace one otherwise valid field with each malformed semantic partition.

    Oracle: Built-in type, identifier grammar, exact revision grammar, and closed
    vocabulary
    are exact public rules.

    Acceptance: Each partition raises its specified TypeError or ValueError.

    Interpretation: Failure identifies exception-taxonomy or lexical-validation drift.

    Limitations: Git object existence is deliberately excluded.
    """
    with pytest.raises(exception):
        replace(make_target(), **{field: value})  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("field", "value"),
    (
        pytest.param("paths", (), id="empty_paths"),
        pytest.param("paths", ("python/a.py", "python/a.py"), id="duplicate_paths"),
        pytest.param("paths", ("/python/a.py",), id="absolute_path"),
        pytest.param("paths", ("python/../a.py",), id="traversal_path"),
        pytest.param("paths", ("python\\a.py",), id="windows_separator"),
        pytest.param(
            "contract_references", ("./docs/contract.md",), id="noncanonical_reference"
        ),
    ),
)
def test_constructor__root_relative_paths__rejects_invalid_partitions(
    field: str, value: tuple[str, ...]
) -> None:
    """Evidence ID: ``SV-HARNESS-127``.

    Requirement: Review and contract paths are normalized root-relative POSIX paths and
    review paths
    are nonempty and unique.

    Method: Replace one path tuple with each independent malformed partition.

    Oracle: The public lexical path contract supplies exact rejection behavior.

    Acceptance: Every malformed partition raises ValueError without filesystem access.

    Interpretation: Failure identifies path-normalization or uniqueness drift.

    Limitations: The test makes no existence, symlink, or repository-membership claim.
    """
    with pytest.raises(ValueError):
        replace(make_target(), **{field: value})  # type: ignore[arg-type]
