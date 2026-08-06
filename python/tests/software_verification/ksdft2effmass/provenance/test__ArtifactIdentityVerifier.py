r"""Software verification of ``ArtifactIdentityVerifier``.

Facet and represented meaning
-----------------------------
This module verifies stateless comparison of observed digest/size values with a sealed
artifact reference.

Intrinsic and cross-object scope
--------------------------------
``ArtifactIdentityVerifier`` is the sole SUT. Public artifact records are collaborators;
direct literal equality supplies the oracle. The action accepts observations and has no
file acquisition API.

VVUQ and scientific exclusions
------------------------------
Passing establishes comparison and boundary behavior only. It excludes file I/O,
digest computation, format truth, numerical verification, scientific validation, UQ,
portability, and cross-language conformance.
"""

from dataclasses import fields
from inspect import signature

import pytest

from ksdft2effmass.provenance import (
    ArtifactIdentity,
    ArtifactIdentityVerificationStatus,
    ArtifactIdentityVerifier,
    ArtifactReference,
    ArtifactSpecification,
)

SUT = ArtifactIdentityVerifier
pytestmark = pytest.mark.software_verification


def make_artifact_reference() -> ArtifactReference:
    """Evidence ID
    Owns no identifier; supports SV-PROV-049, SV-PROV-154 through SV-PROV-160, and
    SV-PROV-162.
    Requirement
    Provide one explicit valid sealed-reference collaborator.
    Method
    Construct public nested records with a synthetic fixed digest and byte size.
    Oracle
    Literal constructor inputs make every expected reference field visible.
    Acceptance
    A valid ArtifactReference with artifact-1, digest ``a`` repeated 64, and size 10 is
    returned.
    Interpretation
    Failure is test setup failure rather than verifier evidence.
    Limitations
    The digest is synthetic and no artifact bytes are read.
    """
    return ArtifactReference(
        ArtifactIdentity("artifact-1", "a" * 64, 10),
        ArtifactSpecification("out/a", "bin", "result", "retain"),
        "manifest-1",
    )


@pytest.mark.parametrize(
    ("observed_sha256", "observed_byte_size", "status"),
    [
        pytest.param(
            "a" * 64, 10, ArtifactIdentityVerificationStatus.VERIFIED, id="verified"
        ),
        pytest.param(
            "b" * 64,
            10,
            ArtifactIdentityVerificationStatus.MISMATCH,
            id="digest_mismatch",
        ),
        pytest.param(
            "a" * 64,
            11,
            ArtifactIdentityVerificationStatus.MISMATCH,
            id="size_mismatch",
        ),
        pytest.param(
            "b" * 64,
            11,
            ArtifactIdentityVerificationStatus.MISMATCH,
            id="digest_and_size_mismatch",
        ),
    ],
)
def test_method__execute_identity_comparison__returns_exact_status(
    observed_sha256: str,
    observed_byte_size: int,
    status: ArtifactIdentityVerificationStatus,
) -> None:
    """Evidence ID
    SV-PROV-049
    Requirement
    execute returns VERIFIED only when observed digest and size both match the
    reference.
    Method
    Partition matching, each single mismatch, and simultaneous digest/size mismatch.
    Oracle
    Direct equality of visible literal digest and integer pairs predicts each status.
    Acceptance
    Each execution returns the exact independently listed status.
    Interpretation
    Failure indicates incorrect exact comparison or conjunction logic.
    Limitations
    Observation acquisition and digest computation are excluded.
    """
    result = SUT().execute(
        make_artifact_reference(), observed_sha256, observed_byte_size
    )
    assert result.status is status


def test_method__execute_result_mapping__copies_expected_and_observed_identity() -> (
    None
):
    """Evidence ID
    SV-PROV-154
    Requirement
    execute maps reference identity and observed values into the result without
    coercion.
    Method
    Execute with distinct observed digest and size and inspect all result fields.
    Oracle
    Fixed public reference fields and independent observed literals fix expected state.
    Acceptance
    The five result fields equal artifact-1, expected a-digest/10, and observed
    b-digest/11.
    Interpretation
    Failure indicates action-to-result mapping drift.
    Limitations
    The represented values are synthetic.
    """
    result = SUT().execute(make_artifact_reference(), "b" * 64, 11)
    assert (
        result.artifact_id,
        result.expected_sha256,
        result.observed_sha256,
        result.expected_byte_size,
        result.observed_byte_size,
    ) == ("artifact-1", "a" * 64, "b" * 64, 10, 11)


def test_method__execute_reference_type__rejects_mapping_lookalike() -> None:
    """Evidence ID
    SV-PROV-050
    Requirement
    reference must be an ArtifactReference rather than a mapping lookalike.
    Method
    Pass an empty mapping with otherwise valid observations.
    Oracle
    The public action signature requires TypeError without coercion.
    Acceptance
    execute raises TypeError.
    Interpretation
    Failure indicates an unintentionally broadened collaborator boundary.
    Limitations
    Subclass behavior is not separately partitioned.
    """
    with pytest.raises(TypeError):
        SUT().execute({}, "a" * 64, 1)  # type: ignore[arg-type]


def test_method__execute_digest_type__rejects_non_string() -> None:
    """Evidence ID
    SV-PROV-155
    Requirement
    observed_sha256 accepts only a built-in string.
    Method
    Execute with bytes and a valid reference and size.
    Oracle
    The public semantic type contract requires TypeError without coercion.
    Acceptance
    execute raises TypeError.
    Interpretation
    Failure indicates weakened digest typing.
    Limitations
    Malformed string values are independently partitioned.
    """
    with pytest.raises(TypeError):
        SUT().execute(make_artifact_reference(), b"a" * 64, 1)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "observed_sha256",
    [
        pytest.param("", id="empty_digest"),
        pytest.param("A" * 64, id="uppercase_digest"),
        pytest.param("g" * 64, id="nonhex_digest"),
        pytest.param("a" * 63, id="short_digest"),
    ],
)
def test_method__execute_digest_value__rejects_malformed_sha256(
    observed_sha256: str,
) -> None:
    """Evidence ID
    SV-PROV-156
    Requirement
    observed_sha256 requires exactly 64 lowercase hexadecimal characters.
    Method
    Partition empty, uppercase, nonhex, and short built-in strings.
    Oracle
    The public lowercase SHA-256 grammar rejects all four malformed literals.
    Acceptance
    Each case raises ValueError.
    Interpretation
    Failure indicates malformed observed-digest acceptance.
    Limitations
    Valid syntax does not prove digest computation.
    """
    with pytest.raises(ValueError):
        SUT().execute(make_artifact_reference(), observed_sha256, 1)


def test_method__execute_byte_size_type__rejects_numeric_string() -> None:
    """Evidence ID
    SV-PROV-157
    Requirement
    observed_byte_size accepts only a built-in integer.
    Method
    Execute with numeric string ``"1"`` and valid other inputs.
    Oracle
    The public type boundary requires TypeError without coercion.
    Acceptance
    execute raises TypeError.
    Interpretation
    Failure indicates numeric-string coercion or weakened typing.
    Limitations
    Boolean is independently partitioned.
    """
    with pytest.raises(TypeError):
        SUT().execute(make_artifact_reference(), "a" * 64, "1")  # type: ignore[arg-type]


def test_method__execute_byte_size_boolean__rejects_bool() -> None:
    """Evidence ID
    SV-PROV-158
    Requirement
    Boolean observations are rejected as byte sizes.
    Method
    Execute with True and valid reference and digest.
    Oracle
    The built-in-int-excluding-bool contract requires TypeError.
    Acceptance
    execute raises TypeError.
    Interpretation
    Failure indicates accidental Boolean acceptance.
    Limitations
    Other wrong types are covered separately.
    """
    with pytest.raises(TypeError):
        SUT().execute(make_artifact_reference(), "a" * 64, True)


@pytest.mark.parametrize(
    "observed_byte_size",
    [pytest.param(0, id="minimum_u64"), pytest.param(2**64 - 1, id="maximum_u64")],
)
def test_method__execute_byte_size_bounds__accepts_inclusive_u64(
    observed_byte_size: int,
) -> None:
    """Evidence ID
    SV-PROV-159
    Requirement
    observed_byte_size accepts both inclusive unsigned 64-bit endpoints.
    Method
    Execute independently at zero and 2**64 minus one.
    Oracle
    The mathematical u64 interval fixes the valid endpoints.
    Acceptance
    The returned observed size equals the supplied endpoint exactly.
    Interpretation
    Failure indicates an off-by-one range defect.
    Limitations
    No allocation proportional to the size occurs.
    """
    assert (
        SUT()
        .execute(make_artifact_reference(), "a" * 64, observed_byte_size)
        .observed_byte_size
        == observed_byte_size
    )


@pytest.mark.parametrize(
    "observed_byte_size",
    [pytest.param(-1, id="negative_one"), pytest.param(2**64, id="u64_overflow")],
)
def test_method__execute_byte_size_value__rejects_outside_u64(
    observed_byte_size: int,
) -> None:
    """Evidence ID
    SV-PROV-160
    Requirement
    observed_byte_size rejects integers outside the unsigned 64-bit interval.
    Method
    Execute at the immediate lower and upper out-of-range values.
    Oracle
    The mathematical u64 interval excludes -1 and 2**64.
    Acceptance
    Each case raises ValueError.
    Interpretation
    Failure indicates a missing or off-by-one range check.
    Limitations
    No file-size observation is performed.
    """
    with pytest.raises(ValueError):
        SUT().execute(make_artifact_reference(), "a" * 64, observed_byte_size)


def test_method__execute_file_api__requires_preobserved_values_only() -> None:
    """Evidence ID
    SV-PROV-161
    Requirement
    The verifier exposes no filesystem path, open-file, or observation-acquisition API.
    Method
    Inspect the stateless dataclass fields and execute signature parameter names.
    Oracle
    The public no-file-I/O contract fixes zero fields and three execute inputs after
    self.
    Acceptance
    Dataclass fields are empty and execute parameters are reference, observed_sha256,
    and observed_byte_size.
    Interpretation
    Failure indicates unauthorized state or file-acquisition surface expansion.
    Limitations
    Reflection does not monitor arbitrary platform system calls.
    """
    assert tuple(field.name for field in fields(SUT)) == ()
    assert tuple(signature(SUT.execute).parameters) == (
        "self",
        "reference",
        "observed_sha256",
        "observed_byte_size",
    )


def test_method__execute_stateless_repeat__returns_equal_results() -> None:
    """Evidence ID
    SV-PROV-162
    Requirement
    Repeated execution with identical immutable inputs is stateless and deterministic.
    Method
    Invoke one action instance twice with the same reference and observations.
    Oracle
    Exact pure comparison of unchanged inputs predicts equal ResultObjects.
    Acceptance
    Both returned values compare exactly equal and action fields remain empty.
    Interpretation
    Failure indicates hidden mutable state or nondeterministic mapping.
    Limitations
    Concurrency and process-level reproducibility are excluded.
    """
    action = SUT()
    reference = make_artifact_reference()
    assert action.execute(reference, "a" * 64, 10) == action.execute(
        reference, "a" * 64, 10
    )
    assert tuple(field.name for field in fields(action)) == ()
