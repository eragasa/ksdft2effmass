r"""Software verification of ``_HarnessProjectionRequest``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module owns the intrinsic behavior of
``_HarnessProjectionRequest``.

Intrinsic and cross-object scope

Only the owner's bounded contract is exercised with literal or immutable inputs.

VVUQ and scientific exclusions

This is software verification only; scientific validation and UQ are excluded.
"""

from pathlib import Path

import pytest

from ksdft2effmass.harness.pi import PiHarnessConfiguration
from ksdft2effmass.harness.pi.local.dbcontrol.records import (
    _HarnessProjectionRequest,
)

SUT = _HarnessProjectionRequest

pytestmark = pytest.mark.software_verification


def test_constructor__canonical_evidence_inputs__are_explicit_and_immutable() -> None:
    """Evidence ID: software-verification.harness.sqlite-control.migration-request.canonical-evidence-inputs

    Requirement: Canonical evidence construction receives source modules, profile policy,
    and predecessor migration relationships as explicit repository-relative inputs.

    Method: Construct the private request with one path for each canonical input.

    Oracle: The supplied immutable tuple and paths define the complete evidence boundary.

    Acceptance: Every value is retained exactly and omission of profile or migration for
    a nonempty module corpus raises ``ValueError``.

    Interpretation: Failure indicates ambient discovery or generated-inventory authority.

    Limitations: Input contents are validated by the migrator Action.
    """  # noqa: E501
    root = Path("/repository")
    request = _HarnessProjectionRequest(
        root,
        evidence_module_paths=(Path("python/tests/test__owner.py"),),
        evidence_profile_matrix_path=Path("harness/pi/evidence/profile.json"),
        evidence_migration_path=Path("harness/evidence/migration.json"),
    )
    assert request.evidence_module_paths == (Path("python/tests/test__owner.py"),)
    assert request.evidence_migration_path == Path("harness/evidence/migration.json")
    with pytest.raises(ValueError):
        _HarnessProjectionRequest(
            root, evidence_module_paths=(Path("python/tests/test__owner.py"),)
        )


def test_constructor__canonical_resource_inputs__are_explicit_and_complete() -> None:
    """Evidence ID: software-verification.harness.sqlite-control.migration-request.canonical-resource-inputs

    Requirement: Canonical resource construction receives the profile, generic and
    local manifests, and both resource roots as explicit repository-relative inputs.

    Method: Construct a request with the complete resource selection and then omit one
    required path and supply one absolute root.

    Oracle: The five immutable paths define one closed canonical resource boundary.

    Acceptance: Complete paths are retained exactly, partial selection raises
    ``ValueError``, and an absolute resource root raises ``ValueError``.

    Interpretation: Failure indicates ambient resource discovery or an unconfined input.

    Limitations: Manifest and source semantics are validated by the migration Action.
    """  # noqa: E501
    root = Path("/repository")
    request = _HarnessProjectionRequest(
        root,
        resource_profile_path=Path("harness/local/profiles/project.json"),
        generic_resource_manifest_path=Path("harness/pi/resource-manifest.json"),
        generic_resource_root_path=Path("harness/pi"),
        local_resource_manifest_path=Path("harness/local/resource-manifest.json"),
        local_resource_root_path=Path("harness/local"),
    )
    assert request.generic_resource_root_path == Path("harness/pi")
    assert request.local_resource_root_path == Path("harness/local")
    with pytest.raises(ValueError, match="supplied together"):
        _HarnessProjectionRequest(
            root,
            resource_profile_path=Path("harness/local/profiles/project.json"),
        )
    with pytest.raises(ValueError, match="repository-relative"):
        _HarnessProjectionRequest(
            root,
            resource_profile_path=Path("harness/local/profiles/project.json"),
            generic_resource_manifest_path=Path("harness/pi/resource-manifest.json"),
            generic_resource_root_path=Path("/harness/pi"),
            local_resource_manifest_path=Path("harness/local/resource-manifest.json"),
            local_resource_root_path=Path("harness/local"),
        )


def test_constructor__pi_configuration__is_explicit_and_type_checked() -> None:
    """Evidence ID: software-verification.harness.migration-request.pi-configuration

    Requirement: Migration receives normalized Pi Harness configuration explicitly.

    Method: Construct with one immutable configuration and then with a plain object.

    Oracle: The private field requires exactly ``PiHarnessConfiguration``.

    Acceptance: The valid value is retained by identity and the plain object raises
    ``TypeError``.

    Interpretation: Failure indicates ambient settings parsing or a weakened input
    boundary.

    Limitations: JSON deserialization and agent projection are tested separately.
    """
    configuration = PiHarnessConfiguration(1, ("example.disabled",))
    request = _HarnessProjectionRequest(
        Path("/repository"), pi_harness_configuration=configuration
    )
    assert request.pi_harness_configuration is configuration
    with pytest.raises(TypeError, match="PiHarnessConfiguration"):
        _HarnessProjectionRequest(
            Path("/repository"),
            pi_harness_configuration=object(),  # type: ignore[arg-type]
        )


def test_constructor__relative_root__raises_value_error() -> None:
    """Evidence ID: software-verification.harness.sqlite-control.migration-request.relative-root-raises-value-error

    Requirement: The migration request accepts only an explicit absolute repository root.

    Method: Construct the private request with a relative ``Path``.

    Oracle: ``Path("repository")`` is relative by Python path semantics.

    Acceptance: Construction raises exactly ``ValueError``.

    Interpretation: Failure indicates an ambient-root persistence boundary regression.

    Limitations: Filesystem existence and migration behavior are not exercised.
    """  # noqa: E501
    with pytest.raises(ValueError):
        _HarnessProjectionRequest(Path("repository"))
