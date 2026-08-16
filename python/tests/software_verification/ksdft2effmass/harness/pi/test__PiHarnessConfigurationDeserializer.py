r"""Software verification of ``PiHarnessConfigurationDeserializer``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module verifies strict normalization of the supported Pi project-settings JSON
subset.

Intrinsic and cross-object scope

``PiHarnessConfigurationDeserializer`` is the sole system under test. File selection,
Pi runtime discovery, and database projection remain outside this ActionObject.

VVUQ and scientific exclusions

This is software verification only. It establishes no Pi runtime availability,
scientific validation, uncertainty quantification, or human acceptance.
"""

import json

import pytest

from ksdft2effmass.harness.pi import PiHarnessConfigurationDeserializer

pytestmark = pytest.mark.software_verification
SUT = PiHarnessConfigurationDeserializer


def test_method__execute__normalizes_only_exact_disabled_overrides() -> None:
    """Evidence ID: software-verification.harness.pi-configuration.deserialize

    Requirement: Deserialization retains exactly true disabled overrides in sorted
    runtime-name order while false, absent, and unrelated fields remain non-disabling.

    Method: Supply reversed true overrides, one false override, one override without
    ``disabled``, and unknown Pi-owned fields.

    Oracle: JSON boolean identity and exact object keys independently determine the
    consumed subset.

    Acceptance: The result contains only the two true runtime names in sorted order.

    Interpretation: Failure indicates broad Pi-schema ownership, coercion, or unstable
    normalization.

    Limitations: The test does not invoke Pi or establish its complete settings schema.
    """
    payload = json.dumps(
        {
            "theme": "unknown-pi-owned-field",
            "subagents": {
                "unknown": {"retained_by_pi": True},
                "agentOverrides": {
                    "example.beta": {"disabled": True, "model": "unchanged"},
                    "example.alpha": {"disabled": True},
                    "example.gamma": {"disabled": False},
                    "example.delta": {"thinking": "high"},
                },
            },
        }
    ).encode()
    result = PiHarnessConfigurationDeserializer().execute(payload)
    assert result.disabled_agent_runtime_names == (
        "example.alpha",
        "example.beta",
    )


def test_method__execute__rejects_nonboolean_disabled() -> None:
    """Evidence ID: software-verification.harness.agent-settings.invalid-disabled

    Requirement: The consumed ``disabled`` field accepts JSON booleans only.

    Method: Supply a matching override whose disabled field is string ``"true"``.

    Oracle: JSON distinguishes strings from booleans without coercion.

    Acceptance: Deserialization raises ``TypeError`` identifying the disabled field.

    Interpretation: Failure indicates coercion of malformed project settings.

    Limitations: Rejection establishes no Pi runtime or scientific claim.
    """
    payload = json.dumps(
        {"subagents": {"agentOverrides": {"example.alpha": {"disabled": "true"}}}}
    ).encode()
    with pytest.raises(TypeError, match="disabled must be boolean"):
        PiHarnessConfigurationDeserializer().execute(payload)


@pytest.mark.parametrize(
    "payload",
    (
        pytest.param(b"[]", id="top_level_array"),
        pytest.param(b'{"subagents": []}', id="subagents_array"),
        pytest.param(
            b'{"subagents":{"agentOverrides":[]}}',
            id="overrides_array",
        ),
        pytest.param(
            b'{"subagents":{"agentOverrides":{"example.alpha":[]}}}',
            id="override_array",
        ),
    ),
)
def test_method__execute__rejects_nonobject_consumed_structure(payload: bytes) -> None:
    """Evidence ID: software-verification.harness.pi-configuration.object-shape

    Requirement: Every consumed settings layer is a JSON object.

    Method: Replace the root, subagents, overrides, or one override with an array.

    Oracle: JSON object and array values are distinct exact semantic types.

    Acceptance: Every partition raises ``TypeError``.

    Interpretation: Failure indicates ambiguous consumed settings structure.

    Limitations: Unknown fields outside the consumed subset remain intentionally
    unvalidated.
    """
    with pytest.raises(TypeError):
        PiHarnessConfigurationDeserializer().execute(payload)


def test_method__execute__rejects_nonbytes_and_invalid_json() -> None:
    """Evidence ID: software-verification.harness.pi-configuration.payload

    Requirement: Deserialization accepts exact UTF-8 JSON bytes only.

    Method: Supply a string and malformed JSON bytes.

    Oracle: The method signature requires bytes and the standard JSON grammar rejects
    the malformed payload.

    Acceptance: String raises ``TypeError`` and malformed bytes raise ``ValueError``.

    Interpretation: Failure indicates implicit input coercion or unbounded decoding.

    Limitations: File selection and source identity are outside this ActionObject.
    """
    with pytest.raises(TypeError):
        PiHarnessConfigurationDeserializer().execute("{}")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="UTF-8 JSON"):
        PiHarnessConfigurationDeserializer().execute(b"{")
