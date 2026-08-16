r"""Software verification of ``PiHarnessConfiguration``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module verifies immutable normalized Pi settings consumed by Harness operations.

Intrinsic and cross-object scope

``PiHarnessConfiguration`` is the sole system under test. JSON interpretation and
control projection are owned separately.

VVUQ and scientific exclusions

This is software verification only. It establishes no Pi runtime availability,
scientific validation, uncertainty quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.harness.pi import PiHarnessConfiguration

pytestmark = pytest.mark.software_verification
SUT = PiHarnessConfiguration


def test_constructor__fields__preserves_sorted_disabled_runtime_names() -> None:
    """Evidence ID: software-verification.harness.pi-configuration.constructs

    Requirement: Version-1 configuration preserves exact sorted disabled runtime names.

    Method: Construct one value from two package-qualified built-in strings.

    Oracle: Frozen dataclass field equality and tuple ordering are exact Python
    semantics.

    Acceptance: The public fields equal the supplied version and tuple exactly.

    Interpretation: Failure indicates field loss, coercion, or reordering.

    Limitations: Construction does not parse JSON or inspect Pi runtime discovery.
    """
    names = ("example.alpha", "example.beta")
    configuration = PiHarnessConfiguration(1, names)
    assert configuration.schema_version == 1
    assert configuration.disabled_agent_runtime_names == names


@pytest.mark.parametrize(
    "names",
    (
        pytest.param(["example.alpha"], id="mutable_list"),
        pytest.param(("example.beta", "example.alpha"), id="unsorted_tuple"),
        pytest.param(("example.alpha", "example.alpha"), id="duplicate_tuple"),
    ),
)
def test_constructor__disabled_names__rejects_noncanonical_collections(
    names: object,
) -> None:
    """Evidence ID: software-verification.harness.pi-configuration.canonical-names

    Requirement: Disabled runtime names form one immutable sorted unique tuple.

    Method: Supply a mutable list, an unsorted tuple, and a duplicate tuple.

    Oracle: The public contract requires exact tuple type and strictly sorted
    uniqueness.

    Acceptance: Every noncanonical partition raises ``TypeError`` or ``ValueError``.

    Interpretation: Failure indicates mutable or ambiguous configuration state.

    Limitations: The cases do not define Pi's complete runtime-name grammar.
    """
    with pytest.raises((TypeError, ValueError)):
        PiHarnessConfiguration(1, names)  # type: ignore[arg-type]


def test_constructor__schema_version__rejects_bool_and_unsupported_version() -> None:
    """Evidence ID: software-verification.harness.pi-configuration.version

    Requirement: Schema version accepts exactly built-in integer ``1`` excluding bool.

    Method: Construct with ``True`` and integer ``2``.

    Oracle: Python distinguishes bool from exact int, and version 1 is the closed
    supported vocabulary.

    Acceptance: Bool raises ``TypeError`` and version 2 raises ``ValueError``.

    Interpretation: Failure indicates widened or ambiguous version behavior.

    Limitations: No serialization-version migration is exercised.
    """
    with pytest.raises(TypeError):
        PiHarnessConfiguration(True, ())
    with pytest.raises(ValueError):
        PiHarnessConfiguration(2, ())
