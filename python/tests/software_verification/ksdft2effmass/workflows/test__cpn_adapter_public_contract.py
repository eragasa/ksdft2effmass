r"""Software verification of the Workflow CPN-adapter public contract family.

Evidence profile: routine

Bounded artifact scope: public immutable mapping, request, result, enum, and package
export agreement for Workflow-to-CPN adaptation.

Facet and represented meaning

The artifact fixes explicit immutable correlation records and the closed adapter
outcome vocabulary at the supported Workflow package boundary.

Intrinsic and cross-object scope

Tests cover exact exports, intrinsic discrimination, identified-token requirements,
and deterministic adapter-result identity.

VVUQ and scientific exclusions

This is structural software verification. It establishes no value-conversion
correctness, Task execution, scientific validation, uncertainty quantification, or
human acceptance.
"""

from dataclasses import replace

import pytest
from _cpn_adapter_fixtures import adapter_request

import ksdft2effmass.workflows as api
from ksdft2effmass.petrinet.colored import (
    ColoredPetriNetColorIdentity,
    ColoredPetriNetToken,
    ColoredPetriNetValue,
    ColoredPetriNetValueKind,
)
from ksdft2effmass.workflows import (
    ColoredPetriNetWorkflowActivationMode,
    ColoredPetriNetWorkflowAdapter,
    WorkflowResultTokenMapping,
)

pytestmark = pytest.mark.software_verification


def test_public_api__package__exports_complete_adapter_family() -> None:
    """Check exact availability of the accepted adapter contract family.

    Evidence ID: SV-WFA-CONTRACT-001

    Requirement: The supported Workflow root exposes every mapping, request, result,
    enum, identity, and ActionObject selected for effect-free CPN adaptation.

    Acceptance: Every exact accepted name resolves publicly and is listed in
    ``__all__``.
    """
    expected = {
        "ColoredPetriNetWorkflowActivationFailureCode",
        "ColoredPetriNetWorkflowActivationMode",
        "ColoredPetriNetWorkflowActivationOutcomeKind",
        "ColoredPetriNetWorkflowActivationRequest",
        "ColoredPetriNetWorkflowActivationResult",
        "ColoredPetriNetWorkflowActivationResultIdentity",
        "ColoredPetriNetWorkflowAdapter",
        "ColoredPetriNetWorkflowMapping",
        "ColoredPetriNetWorkflowSelectionPolicy",
        "WorkflowResultTokenMapping",
    }

    assert expected <= set(api.__all__)
    assert all(hasattr(api, name) for name in expected)


def test_artifact__mapping__requires_individually_identified_tokens() -> None:
    """Check the explicit Workflow-result correlation boundary.

    Evidence ID: SV-WFA-CONTRACT-002

    Requirement: A Workflow result maps only to an individually identified generic
    token; anonymous multiset values cannot close exact result correlation.

    Acceptance: Replacing the valid mapped token with an equal anonymous token raises
    ``ValueError``.
    """
    request = adapter_request(ColoredPetriNetWorkflowActivationMode.DIRECT, None)
    mapping = request.result_token_mappings[0]
    anonymous = ColoredPetriNetToken(
        ColoredPetriNetColorIdentity(mapping.token.color_identity.value),
        ColoredPetriNetValue(
            ColoredPetriNetValueKind.INTEGER, mapping.token.value.value
        ),
    )

    with pytest.raises(ValueError):
        WorkflowResultTokenMapping(
            mapping.input_name,
            mapping.result_identity,
            mapping.variable_identity,
            mapping.place_identity,
            anonymous,
        )


def test_artifact__request__enforces_direct_mode_discrimination() -> None:
    """Check direct versus automatic request discrimination.

    Evidence ID: SV-WFA-CONTRACT-003

    Requirement: Direct mode requires one exact direct binding and automatic mode
    prohibits that field.

    Acceptance: Removing a direct request's binding or attaching it to automatic mode
    raises ``ValueError``.
    """
    direct = adapter_request(ColoredPetriNetWorkflowActivationMode.DIRECT, None)

    with pytest.raises(ValueError):
        replace(direct, direct_binding=None)
    with pytest.raises(ValueError):
        replace(
            direct,
            mode=ColoredPetriNetWorkflowActivationMode.AUTOMATIC,
        )


def test_artifact__result_identity__is_deterministic_and_outcome_closed() -> None:
    """Check exact repeated adapter-result identity and closed outcome correlation.

    Evidence ID: SV-WFA-CONTRACT-004

    Requirement: Equal represented requests and deterministic generic operations
    produce equal lowercase SHA-256 adapter-result identities.

    Acceptance: Two executions return equal 64-character identities and equal closed
    results.
    """
    request = adapter_request(ColoredPetriNetWorkflowActivationMode.DIRECT, None)

    first = ColoredPetriNetWorkflowAdapter().execute(request)
    second = ColoredPetriNetWorkflowAdapter().execute(request)

    assert first == second
    assert first.identity == second.identity
    assert len(first.identity.value) == 64
    assert first.identity.value == first.identity.value.lower()
