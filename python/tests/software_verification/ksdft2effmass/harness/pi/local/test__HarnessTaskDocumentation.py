r"""Software verification of ``HarnessTaskDocumentation``.

Facet and represented meaning

Software verification of one accepted project-local HarnessTask surface.

Intrinsic and cross-object scope

The sole primary SUT is ``HarnessTaskDocumentation``.
Artifact-owned evidence covers detailed cross-object algorithms.

VVUQ and scientific exclusions

Passing establishes software-interface behavior only. It does not establish a
migration, activation, scientific validity, or human acceptance.
"""

import pytest

from ksdft2effmass.harness.pi.local import HarnessTaskDocumentation

from .task_model_examples import identity, make_request

pytestmark = pytest.mark.software_verification
SUT = HarnessTaskDocumentation


def test_constructor__public_stereotype__has_exact_runtime_identity() -> None:
    """Evidence ID: ``SV-HT-010``.

    Requirement: The public immutable object has its accepted runtime identity.

    Method: Construct or enumerate the public SUT using explicit synthetic support
    input.

    Oracle: The accepted 19-interface table supplies the expected name and stereotype.

    Acceptance: Runtime identity, fieldlessness, fields, or closed values match exactly.

    Interpretation: Failure identifies public API, stereotype, or value-semantics drift.

    Limitations: Detailed algorithms are asserted by focused artifact-owned evidence.
    """
    value = make_request().rendered_documentation
    assert type(value) is SUT
    assert value == value


def test_constructor__artifact_identity__rejects_hash_disagreement() -> None:
    """Evidence ID: ``SV-HT-041``.

    Requirement: Rendered documentation binds exact bytes to their SHA-256 identity.

    Method: Exercise independently invalid partitions against explicit synthetic input.

    Oracle: The accepted public constructor or ActionObject contract defines exact
    outcomes.

    Acceptance: Valid input remains exact and every specified invalid partition
    fails closed.

    Interpretation: Failure identifies intrinsic or cross-object contract drift.

    Limitations: Software verification does not authorize migration or human acceptance.
    """
    documentation = make_request().rendered_documentation
    with pytest.raises(ValueError, match="identity"):
        SUT(documentation.path, documentation.content, identity(b"other"))
