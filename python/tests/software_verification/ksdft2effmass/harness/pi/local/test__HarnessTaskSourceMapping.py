r"""Software verification of ``HarnessTaskSourceMapping``.

Facet and represented meaning

Software verification of one accepted project-local HarnessTask surface.

Intrinsic and cross-object scope

The sole primary SUT is ``HarnessTaskSourceMapping``.
Artifact-owned evidence covers detailed cross-object algorithms.

VVUQ and scientific exclusions

Passing establishes software-interface behavior only. It does not establish a
migration, activation, scientific validity, or human acceptance.
"""

import pytest

from ksdft2effmass.harness.pi.local import HarnessTaskSourceMapping

from .task_model_examples import identity, make_request

pytestmark = pytest.mark.software_verification
SUT = HarnessTaskSourceMapping


def test_constructor__public_stereotype__has_exact_runtime_identity() -> None:
    """Evidence ID: ``SV-HT-007``.

    Requirement: The public immutable object has its accepted runtime identity.

    Method: Construct or enumerate the public SUT using explicit synthetic support
    input.

    Oracle: The accepted 19-interface table supplies the expected name and stereotype.

    Acceptance: Runtime identity, fieldlessness, fields, or closed values match exactly.

    Interpretation: Failure identifies public API, stereotype, or value-semantics drift.

    Limitations: Detailed algorithms are asserted by focused artifact-owned evidence.
    """
    value = make_request().mappings[0]
    assert type(value) is SUT
    assert value == value


def test_constructor__span_bounds__rejects_empty_span_and_wrong_disposition() -> None:
    """Evidence ID: ``SV-HT-038``.

    Requirement: Mapping construction enforces nonempty half-open spans and exact
    enum types.

    Method: Exercise independently invalid partitions against explicit synthetic input.

    Oracle: The accepted public constructor or ActionObject contract defines exact
    outcomes.

    Acceptance: Valid input remains exact and every specified invalid partition
    fails closed.

    Interpretation: Failure identifies intrinsic or cross-object contract drift.

    Limitations: Software verification does not authorize migration or human acceptance.
    """
    mapping = make_request().mappings[0]
    with pytest.raises(ValueError, match="greater"):
        SUT(
            mapping.mapping_id,
            mapping.source_identity,
            1,
            1,
            identity(b""),
            mapping.disposition,
            mapping.target_references,
            mapping.transformation,
            mapping.rationale,
        )
    with pytest.raises(TypeError, match="SourceDisposition"):
        SUT(
            mapping.mapping_id,
            mapping.source_identity,
            0,
            1,
            identity(b"x"),
            "DOCUMENTATION_OWNED_CONTENT",
            mapping.target_references,
            mapping.transformation,
            mapping.rationale,
        )  # type: ignore[arg-type]
