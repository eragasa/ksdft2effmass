r"""Software verification of ``PiHarnessAgentDefinition``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module verifies intrinsic normalized agent-definition invariants.

Intrinsic and cross-object scope

``PiHarnessAgentDefinition`` is the sole system under test. Descriptor parsing,
configuration composition, and persistence are owned separately.

VVUQ and scientific exclusions

This is software verification only and establishes no Pi runtime availability,
scientific validation, uncertainty quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.harness.pi import ArtifactIdentity, PiHarnessAgentDefinition

pytestmark = pytest.mark.software_verification
SUT = PiHarnessAgentDefinition


def make_definition(**changes: object) -> PiHarnessAgentDefinition:
    """Evidence ID: Owns no identifier; supports definition construction evidence.

    Requirement: Definition tests receive one valid baseline with explicit replacements.

    Method: Merge supplied field replacements into one literal valid field mapping.

    Oracle: The public constructor fields define the fixture shape.

    Acceptance: Return one constructed definition or propagate its invariant failure.

    Interpretation: Failure indicates fixture construction drift.

    Limitations: This helper owns no independent behavior claim.
    """
    values = {
        "schema_version": 1,
        "name": "agent",
        "package": "example",
        "runtime_name": "example.agent",
        "source_path": ".pi/agents/agent.md",
        "source_identity": ArtifactIdentity(1, "sha256", "0" * 64),
        "acceptance_role": "writer",
        "selected_skills": ("alpha",),
        "enabled": True,
    }
    values.update(changes)
    return PiHarnessAgentDefinition(**values)  # type: ignore[arg-type]


def test_constructor__fields__preserves_valid_definition() -> None:
    """Evidence ID: software-verification.harness.agent-definition.constructs

    Requirement: A valid definition preserves exact descriptor and enablement state.

    Method: Construct one complete literal definition.

    Oracle: Frozen dataclass field equality is exact Python behavior.

    Acceptance: Runtime name, selected skills, and enabled state equal their inputs.

    Interpretation: Failure indicates coercion or field loss.

    Limitations: Construction performs no parsing, persistence, or runtime discovery.
    """
    result = make_definition()
    assert result.runtime_name == "example.agent"
    assert result.selected_skills == ("alpha",)
    assert result.enabled is True


def test_constructor__runtime_name__must_match_package_and_name() -> None:
    """Evidence ID: software-verification.harness.agent-definition.runtime-name

    Requirement: Runtime name exactly equals the represented package and descriptor
    name composition.

    Method: Construct with a different package-qualified runtime name.

    Oracle: The intrinsic contract defines exact ``package.name`` composition.

    Acceptance: Construction raises ``ValueError``.

    Interpretation: Failure permits contradictory represented identities.

    Limitations: This does not claim Pi runtime resolution succeeds.
    """
    with pytest.raises(ValueError, match="package.name"):
        make_definition(runtime_name="other.agent")
