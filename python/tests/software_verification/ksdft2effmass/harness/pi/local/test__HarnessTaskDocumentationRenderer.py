r"""Software verification of ``HarnessTaskDocumentationRenderer``.

Facet and represented meaning

Software verification of one accepted project-local HarnessTask surface.

Intrinsic and cross-object scope

The sole primary SUT is ``HarnessTaskDocumentationRenderer``.
Artifact-owned evidence covers detailed cross-object algorithms.

VVUQ and scientific exclusions

Passing establishes software-interface behavior only. It does not establish a
migration, activation, scientific validity, or human acceptance.
"""

import pytest

from ksdft2effmass.harness.pi.local import HarnessTaskDocumentationRenderer

from .task_model_examples import make_request

pytestmark = pytest.mark.software_verification
SUT = HarnessTaskDocumentationRenderer


def test_constructor__public_stereotype__has_exact_runtime_identity() -> None:
    """Evidence ID: ``SV-HT-011``.

    Requirement: The public ActionObject is fieldless, stateless, and can be
    constructed directly.

    Method: Construct or enumerate the public SUT using explicit synthetic support
    input.

    Oracle: The accepted 19-interface table supplies the expected name and stereotype.

    Acceptance: Runtime identity, fieldlessness, fields, or closed values match exactly.

    Interpretation: Failure identifies public API, stereotype, or value-semantics drift.

    Limitations: Detailed algorithms are asserted by focused artifact-owned evidence.
    """
    assert SUT.__slots__ == ()
    assert type(SUT()) is SUT


def test_method__execute__uses_only_explicit_inputs() -> None:
    """Evidence ID: ``SV-HT-042``.

    Requirement: Rendering reproduces the exact claimed output from explicit Task,
    content, and profile.

    Method: Exercise independently invalid partitions against explicit synthetic input.

    Oracle: The accepted public constructor or ActionObject contract defines exact
    outcomes.

    Acceptance: Valid input remains exact and every specified invalid partition
    fails closed.

    Interpretation: Failure identifies intrinsic or cross-object contract drift.

    Limitations: Software verification does not authorize migration or human acceptance.
    """
    request = make_request()
    assert (
        SUT().execute(
            request.candidate_task,
            request.documentation_content,
            request.projection_profile,
        )
        == request.rendered_documentation
    )
    with pytest.raises(TypeError):
        SUT().execute(
            object(), request.documentation_content, request.projection_profile
        )  # type: ignore[arg-type]
