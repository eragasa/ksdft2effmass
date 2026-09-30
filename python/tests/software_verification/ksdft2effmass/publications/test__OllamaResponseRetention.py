r"""Software verification of ``OllamaResponseRetention``.

Evidence profile: routine

Bounded artifact scope: atomic local-model response retention.

Facet and represented meaning

The ActionObject retains exact bounded bytes under mode-0600 files, never replaces an
existing request artifact, and rejects data outside its hard response bound.

Intrinsic and cross-object scope

The retention owner performs local wire-artifact persistence only. Parsing, manuscript
composition, and scientific interpretation remain with their existing owners.

VVUQ and scientific exclusions

Synthetic bytes establish retention mechanics only, not model quality, evidence
correctness, scientific validation, publication readiness, or human acceptance.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

import ksdft2effmass.publications as publications
from ksdft2effmass.publications import OllamaResponseRetention
from ksdft2effmass.publications.authoring.adapters.ollama_retention import (
    OllamaResponseRetention as DefiningRetention,
)

pytestmark = pytest.mark.software_verification
SUT = OllamaResponseRetention


class TestOllamaResponseRetention:
    """Verify bounded atomic exact-response retention."""

    REQUEST_ID = "manuscript-inference-request:sha256:" + "a" * 64

    def test_method__retain_raw__writes_exact_mode_0600_bytes_atomically(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-PUBLICATIONS-AUTHORING-030

        Requirement: Exact local response bytes must be durably published with narrow
        permissions before parsing can discard them.

        Acceptance: Retained bytes, digest, count, filename, file mode, and directory
        mode agree exactly with the synthetic response.
        """
        payload = b'{"synthetic":"response"}'
        artifact = DefiningRetention(root=tmp_path / "runtime").retain_raw(
            self.REQUEST_ID, payload
        )
        assert artifact.path.read_bytes() == payload
        assert artifact.sha256 == hashlib.sha256(payload).hexdigest()
        assert artifact.byte_count == len(payload)
        assert artifact.path.name == f"raw-{self.REQUEST_ID}.json"
        assert artifact.path.stat().st_mode & 0o777 == 0o600
        assert artifact.path.parent.stat().st_mode & 0o777 == 0o700

    def test_method__retain_raw__never_replaces_existing_request_artifact(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-PUBLICATIONS-AUTHORING-031

        Requirement: A repeated request identity must not overwrite retained evidence.

        Acceptance: The second publication raises ``FileExistsError`` and the first
        exact bytes and digest remain unchanged.
        """
        retention = DefiningRetention(root=tmp_path / "runtime")
        first = retention.retain_raw(self.REQUEST_ID, b"first")
        with pytest.raises(FileExistsError):
            retention.retain_raw(self.REQUEST_ID, b"second")
        assert first.path.read_bytes() == b"first"
        assert first.sha256 == hashlib.sha256(b"first").hexdigest()

    @pytest.mark.parametrize(
        "payload",
        (
            pytest.param(b"", id="empty"),
            pytest.param(
                b"x" * (DefiningRetention.MAX_RAW_RESPONSE_BYTES + 1),
                id="over_bound",
            ),
        ),
    )
    def test_method__retain_raw__rejects_outside_hard_byte_bound(
        self, tmp_path: Path, payload: bytes
    ) -> None:
        """Evidence ID: SV-PUBLICATIONS-AUTHORING-032

        Requirement: Empty or oversized raw responses must never become artifacts.

        Acceptance: Each invalid partition raises ``ValueError`` and creates no file.
        """
        root = tmp_path / "runtime"
        with pytest.raises(ValueError, match="byte count"):
            DefiningRetention(root=root).retain_raw(self.REQUEST_ID, payload)
        assert not root.exists()

    def test_public_api__retention__preserves_defining_class_identity(self) -> None:
        """Evidence ID: SV-PUBLICATIONS-AUTHORING-033

        Requirement: The curated facade exposes the defining retention ActionObject.

        Acceptance: Defining-module and root-facade imports are the same class object.
        """
        assert OllamaResponseRetention is DefiningRetention
        assert publications.OllamaResponseRetention is DefiningRetention
