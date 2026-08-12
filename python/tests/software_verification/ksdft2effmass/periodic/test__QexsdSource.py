r"""Software verification of ``QexsdSource``.

Evidence profile: routine

Bounded artifact scope: explicit controlled QEXSD bytes and source identity.

Facet and represented meaning

The source binds immutable bytes to a strict path, digest, and count.

Intrinsic and cross-object scope

Only intrinsic construction and immutable value semantics are tested.

VVUQ and scientific exclusions

Controlled bytes are not calculated physical data; no scientific claim is made.
"""

from dataclasses import FrozenInstanceError

import pytest
from qexsd_fixtures import CONTROLLED_QEXSD, controlled_source_bytes

from ksdft2effmass.periodic import QexsdSource

SUT = QexsdSource
pytestmark = pytest.mark.software_verification


def test_constructor__source_identity__maps_exact_immutable_bytes() -> None:
    """Evidence ID: SV-PERIODIC-001

    Requirement: Valid exact bytes, canonical path, SHA-256, and count are retained.

    Acceptance: Fields equal the supplied values and frozen assignment is rejected.
    """
    digest, count = controlled_source_bytes()
    source = QexsdSource(
        "/external/data-file-schema.xml", digest, count, CONTROLLED_QEXSD
    )
    assert source.content is CONTROLLED_QEXSD
    assert (source.sha256, source.byte_count) == (digest, count)
    with pytest.raises(FrozenInstanceError):
        source.byte_count = 0  # type: ignore[misc]


@pytest.mark.parametrize(
    ("path", "digest", "count"),
    [
        pytest.param("relative.xml", None, None, id="relative_path"),
        pytest.param("/external/source.xml", "0" * 64, None, id="digest_mismatch"),
        pytest.param("/external/source.xml", None, 1, id="byte_count_mismatch"),
    ],
)
def test_constructor__source_contract__rejects_invalid_identity(
    path: str, digest: str | None, count: int | None
) -> None:
    """Evidence ID: SV-PERIODIC-002

    Requirement: Path is canonical absolute POSIX and digest/count match exact bytes.

    Acceptance: Every named invalid partition raises ValueError.
    """
    actual_digest, actual_count = controlled_source_bytes()
    with pytest.raises(ValueError):
        QexsdSource(
            path,
            actual_digest if digest is None else digest,
            actual_count if count is None else count,
            CONTROLLED_QEXSD,
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        pytest.param("sha256", b"x" * 64, id="digest_bytes"),
        pytest.param("byte_count", True, id="boolean_count"),
        pytest.param("content", bytearray(CONTROLLED_QEXSD), id="mutable_bytes"),
    ],
)
def test_constructor__semantic_types__rejects_coercible_values(
    field: str, value: object
) -> None:
    """Evidence ID: SV-PERIODIC-003

    Requirement: Source public fields reject wrong semantic types without coercion.

    Acceptance: Every named partition raises TypeError.
    """
    digest, count = controlled_source_bytes()
    values: dict[str, object] = {
        "canonical_path": "/external/source.xml",
        "sha256": digest,
        "byte_count": count,
        "content": CONTROLLED_QEXSD,
    }
    values[field] = value
    with pytest.raises(TypeError):
        QexsdSource(**values)  # type: ignore[arg-type]
