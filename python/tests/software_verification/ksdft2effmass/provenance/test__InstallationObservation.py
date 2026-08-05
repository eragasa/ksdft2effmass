"""Evidence class and represented meaning
Software verification of external-tool installation observations.
Owned contract, oracle, and scope
InstallationObservation is the SUT; field, digest, provenance, and
installation/verification separation rules are the oracle.
VVUQ and scientific exclusions
Evidence excludes discovery, capability verification, execution, numerical verification,
scientific validation, UQ, and cross-language conformance.
"""

from dataclasses import fields

import pytest

from ksdft2effmass.provenance import InstallationObservation

SUT = InstallationObservation
pytestmark = pytest.mark.software_verification


def test_constructor__installation_observation_fields__maps_exact_metadata() -> None:
    """Evidence ID
    SV-PROV-031
    Requirement
    Installation observation maps eight exact metadata fields including optional digest
    and provenance identities.
    Method
    Construct with a synthetic digest and inspect every field.
    Oracle
    The accepted P2 record vocabulary independently fixes the expected tuple.
    Acceptance
    All fields equal supplied values exactly.
    Interpretation
    Failure indicates field mapping or optional-digest drift.
    Limitations
    No installation is discovered and the digest is synthetic.
    """
    value = SUT("install-1", "spec-1", "qe", "7.3", "pw.x", "c" * 64, "env-1", "prov-1")
    assert (
        value.installation_id,
        value.specification_id,
        value.tool_id,
        value.observed_version,
        value.executable_or_package_id,
        value.executable_sha256,
        value.environment_record_id,
        value.provenance_id,
    ) == ("install-1", "spec-1", "qe", "7.3", "pw.x", "c" * 64, "env-1", "prov-1")


def test_field__installation_verification_separation__excludes_capability_status() -> (
    None
):
    """Evidence ID
    SV-PROV-032
    Requirement
    Installation observation contains no capability, verification status, evidence
    artifacts, or runtime handle.
    Method
    Inspect the complete public dataclass field vocabulary.
    Oracle
    The accepted installation-versus-verification architecture fixes eight fields only.
    Acceptance
    Field names match the exact approved tuple and exclude runtime/capability state.
    Interpretation
    Failure indicates lifecycle responsibility leakage.
    Limitations
    Reflection cannot detect hidden behavior outside the declared DataObject fields.
    """
    assert tuple(field.name for field in fields(SUT)) == (
        "installation_id",
        "specification_id",
        "tool_id",
        "observed_version",
        "executable_or_package_id",
        "executable_sha256",
        "environment_record_id",
        "provenance_id",
    )


def test_constructor__optional_digest__accepts_none_and_rejects_invalid_sha256() -> (
    None
):
    """Evidence ID
    SV-PROV-033
    Requirement
    Executable digest may be absent; when present it is exactly lowercase SHA-256.
    Method
    Construct with None then with uppercase and short digest alternatives.
    Oracle
    The public optional digest contract determines acceptance exactly.
    Acceptance
    None is retained and malformed digests raise ValueError.
    Interpretation
    Failure indicates optionality or digest validation drift.
    Limitations
    Digest computation and executable identity truth are not tested.
    """
    assert SUT("i", "s", "t", "1", "exe", None, "env", "prov").executable_sha256 is None
    for digest in ("D" * 64, "d" * 63):
        with pytest.raises(ValueError):
            SUT("i", "s", "t", "1", "exe", digest, "env", "prov")
