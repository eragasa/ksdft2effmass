r"""Software verification of JSON schema artifact.

Facet and represented meaning

Software verification of a concrete JSON schema artifact boundary.

Intrinsic and cross-object scope

The JSON schema artifact is primary; exact declared keys supply the oracle.

VVUQ and scientific exclusions

Passing establishes only artifact structure, not numerical verification, scientific
validation, UQ, or physical correctness.
"""

import pytest


def make_schema_case(value):
    """Evidence ID: Owns no identifier; supports SV-EXAMPLE-002.

    Requirement: Setup preserves the supplied schema case.

    Method: Return the explicit public fixture value unchanged.

    Oracle: Python identity of the supplied immutable string is sufficient setup evidence.

    Acceptance: The returned value equals the supplied value exactly.

    Interpretation: Failure identifies fixture setup drift.

    Limitations: The helper makes no independent evidence, validation, or UQ claim.
    """
    return value


@pytest.mark.parametrize(
    "key",
    [
        pytest.param("schema", id="schema_key"),
        pytest.param("title", id="SV-EXAMPLE-002-title"),
    ],
)
def test_artifact__declared_keys__accepts_semantic_cases(key):
    """Evidence ID: SV-EXAMPLE-002

    Requirement: The artifact accepts each declared schema key.

    Method: Exercise explicit semantic keys through the controlled representation.

    Oracle: The fixed declared-key inventory supplies exact expectations.

    Acceptance: Each returned key equals its declared fixture value.

    Interpretation: Failure indicates fixture, artifact, or contract drift.

    Limitations: Runtime semantics, scientific validation, and UQ are excluded.
    """
    assert make_schema_case(key) == key
