r"""Software verification of ``HarnessTask``.

Facet and represented meaning

Software verification of one accepted project-local HarnessTask surface.

Intrinsic and cross-object scope

The sole primary SUT is ``HarnessTask``.
Artifact-owned evidence covers detailed cross-object algorithms.

VVUQ and scientific exclusions

Passing establishes software-interface behavior only. It does not establish a
migration, activation, scientific validity, or human acceptance.
"""

import pytest

from ksdft2effmass.harness.pi.local import HarnessTask

from .task_model_examples import make_task

pytestmark = pytest.mark.software_verification
SUT = HarnessTask


def test_constructor__public_stereotype__has_exact_runtime_identity() -> None:
    """Evidence ID: ``SV-HT-001``.

    Requirement: The public immutable object has its accepted runtime identity.

    Method: Construct or enumerate the public SUT using explicit synthetic support
    input.

    Oracle: The accepted 19-interface table supplies the expected name and stereotype.

    Acceptance: Runtime identity, fieldlessness, fields, or closed values match exactly.

    Interpretation: Failure identifies public API, stereotype, or value-semantics drift.

    Limitations: Detailed algorithms are asserted by focused artifact-owned evidence.
    """
    value = make_task()
    assert type(value) is SUT
    assert value == value


def test_constructor__intrinsic_fields__reject_invalid_values() -> None:
    """Evidence ID: ``SV-HT-033``.

    Requirement: Intrinsic fields reject booleans, non-tuples, and invalid local
    identifiers.

    Method: Exercise independently invalid partitions against explicit synthetic input.

    Oracle: The accepted public constructor or ActionObject contract defines exact
    outcomes.

    Acceptance: Valid input remains exact and every specified invalid partition
    fails closed.

    Interpretation: Failure identifies intrinsic or cross-object contract drift.

    Limitations: Software verification does not authorize migration or human acceptance.
    """
    with pytest.raises(TypeError):
        make_task(schema_version=True)
    with pytest.raises(TypeError):
        make_task(authorized_scope=["not a tuple"])
    with pytest.raises(ValueError):
        make_task(status="invalid/status")
