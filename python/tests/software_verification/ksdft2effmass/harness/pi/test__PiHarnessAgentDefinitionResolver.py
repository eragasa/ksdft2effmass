r"""Software verification of ``PiHarnessAgentDefinitionResolver``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module verifies descriptor and configuration composition before persistence.

Intrinsic and cross-object scope

``PiHarnessAgentDefinitionResolver`` is the sole system under test. File selection and
database projection remain outside the ActionObject.

VVUQ and scientific exclusions

This is software verification only and establishes no Pi runtime availability,
scientific validation, uncertainty quantification, or human acceptance.
"""

import hashlib

import pytest

from ksdft2effmass.harness.pi import (
    PiHarnessAgentDefinitionResolver,
    PiHarnessConfiguration,
)

pytestmark = pytest.mark.software_verification
SUT = PiHarnessAgentDefinitionResolver


def descriptor_bytes() -> bytes:
    """Evidence ID: Owns no identifier; supports descriptor-resolution evidence.

    Requirement: Resolver tests receive one exact valid descriptor payload.

    Method: Return a fixed UTF-8 Markdown byte literal.

    Oracle: The consumed frontmatter contract defines the fixture fields.

    Acceptance: Return the exact bytes without transformation.

    Interpretation: Failure indicates fixture drift.

    Limitations: This helper owns no independent behavior claim.
    """
    return b"""---
name: example-writer
package: example
skills: zeta, alpha
acceptanceRole: writer
---
Prompt.
"""


def test_method__execute__resolves_projection_ready_definition() -> None:
    """Evidence ID: software-verification.harness.agent-definition.resolve

    Requirement: Descriptor and configuration composition resolves exact identities,
    normalized skills and role, source identity, and repository enablement.

    Method: Resolve one descriptor whose exact runtime name is disabled.

    Oracle: Frontmatter literals, SHA-256, and the supplied disabled-name tuple provide
    independent exact expected values.

    Acceptance: Every represented field equals the exact expected value and enabled is
    false.

    Interpretation: Failure indicates descriptor parsing or enablement policy inside
    persistence rather than this ActionObject.

    Limitations: No file access, database write, or Pi runtime discovery occurs.
    """
    payload = descriptor_bytes()
    result = PiHarnessAgentDefinitionResolver().execute(
        ".pi/agents/example-writer.md",
        payload,
        PiHarnessConfiguration(1, ("example.example-writer",)),
    )
    assert result.name == "example-writer"
    assert result.package == "example"
    assert result.runtime_name == "example.example-writer"
    assert result.acceptance_role == "writer"
    assert result.selected_skills == ("alpha", "zeta")
    assert result.source_identity.digest == hashlib.sha256(payload).hexdigest()
    assert result.enabled is False


def test_method__execute__rejects_incomplete_or_unsupported_descriptor() -> None:
    """Evidence ID: software-verification.harness.agent-definition.invalid-descriptor

    Requirement: Consumed descriptor frontmatter must identify a role with a supported
    acceptance value.

    Method: Resolve one document without frontmatter and one with an unsupported role.

    Oracle: The public contract requires closed frontmatter, name, and writer or
    read-only acceptance role.

    Acceptance: Both inputs raise ``ValueError`` before producing a definition.

    Interpretation: Failure indicates permissive or persistence-owned interpretation.

    Limitations: The test does not define unconsumed Pi descriptor fields.
    """
    resolver = PiHarnessAgentDefinitionResolver()
    with pytest.raises(ValueError):
        resolver.execute("agent.md", b"Prompt", PiHarnessConfiguration(1, ()))
    with pytest.raises(ValueError, match="unsupported acceptanceRole"):
        resolver.execute(
            "agent.md",
            b"---\nname: agent\nacceptanceRole: operator\n---\n",
            PiHarnessConfiguration(1, ()),
        )
