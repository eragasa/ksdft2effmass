"""Software verification of ``CampaignJsonDecoder``.

Evidence profile: routine

Facet and represented meaning
-----------------------------
The campaign specialization exposes strict closed JSON wire mechanics inherited from
the shared serialization owner.

Intrinsic and cross-object scope
--------------------------------
Duplicate-key rejection, primitive exact types, finite numeric conversion, SHA-256
syntax, and specialization reuse are covered with synthetic payloads.

VVUQ and scientific exclusions
------------------------------
Passing establishes software behavior only. It does not authenticate artifacts,
validate campaign schemas, or establish scientific correctness.
"""

import numpy as np
import pytest

from ksdft2effmass.campaigns import CampaignJsonDecoder
from ksdft2effmass.periodic1d.campaign import Periodic1DCampaignJsonDecoder
from ksdft2effmass.serialization.json import StrictJsonDecoder

pytestmark = pytest.mark.software_verification


class TestCampaignJsonDecoder:
    """Own campaign-specialization evidence for shared strict JSON decoding."""

    def test_document__closed_json__rejects_duplicate_keys(self) -> None:
        """Evidence ID: SV-CAMPAIGN-JSON-DECODER-001.

        Requirement: Campaign JSON decoding accepts one closed UTF-8 object and
        rejects ambiguous duplicate object keys.

        Acceptance: Exact primitive values are retained and a duplicate key raises
        ``ValueError``.
        """
        decoder = CampaignJsonDecoder()

        assert decoder.document(b'{"enabled":true,"samples":[1,2.5]}') == {
            "enabled": True,
            "samples": [1, 2.5],
        }
        with pytest.raises(ValueError, match="duplicate JSON key"):
            decoder.document(b'{"sample":1,"sample":2}')

    def test_primitives__exact_types__rejects_coercive_inputs(self) -> None:
        """Evidence ID: SV-CAMPAIGN-JSON-DECODER-002.

        Requirement: Primitive decoding rejects Boolean-as-integer and numeric-string
        coercion while accepting finite integer and floating JSON reals.

        Acceptance: Exact values decode and coercive inputs raise ``TypeError``.
        """
        decoder = CampaignJsonDecoder()

        assert decoder.boolean(True, "enabled") is True
        assert decoder.integer(3, "count") == 3
        assert decoder.real(3, "energy") == 3.0
        assert decoder.real(2.5, "energy") == 2.5
        with pytest.raises(TypeError, match="count must be an integer"):
            decoder.integer(True, "count")
        with pytest.raises(TypeError, match="energy must be a real number"):
            decoder.real("2.5", "energy")

    def test_specialization__periodic1d_decoder__inherits_shared_behavior(self) -> None:
        """Evidence ID: SV-CAMPAIGN-JSON-DECODER-003.

        Requirement: A canonical domain decoder reuses the neutral strict primitive
        boundary without importing the transitional campaign package.

        Acceptance: The periodic-1D decoder is a ``StrictJsonDecoder`` but not a
        ``CampaignJsonDecoder`` and applies the shared SHA-256 and nonempty-string
        rules.
        """
        decoder = Periodic1DCampaignJsonDecoder()
        digest = "a" * 64

        assert isinstance(decoder, StrictJsonDecoder)
        assert not isinstance(decoder, CampaignJsonDecoder)
        assert decoder.sha256(digest, "source_sha256") == digest
        with pytest.raises(ValueError, match="must be nonempty"):
            decoder.nonempty_string("", "artifact_kind")

    def test_complex_matrix__pair_wire__is_strict_and_immutable(self) -> None:
        """Evidence ID: SV-CAMPAIGN-JSON-DECODER-004.

        Requirement: The periodic-1D decoder owns the shared complex-pair matrix
        wire adaptation without assigning scientific metadata.

        Acceptance: A rectangular pair wire becomes an immutable ``complex128``
        matrix, while ragged rows and malformed entries fail closed.
        """
        decoder = Periodic1DCampaignJsonDecoder()

        matrix = decoder.complex_matrix(
            [[[1, 2.5], [3.0, -4]], [[5, 0], [-6, 7]]], "hopping"
        )

        assert matrix.dtype == np.dtype(np.complex128)
        assert np.array_equal(
            matrix,
            np.asarray(
                [[1.0 + 2.5j, 3.0 - 4.0j], [5.0 + 0.0j, -6.0 + 7.0j]],
                dtype=np.complex128,
            ),
        )
        assert not matrix.flags.writeable
        with pytest.raises(ValueError, match="must be rectangular"):
            decoder.complex_matrix([[[1, 0]], [[2, 0], [3, 0]]], "hopping")
        with pytest.raises(ValueError, match="must contain real and imaginary"):
            decoder.complex_matrix([[[1, 0, 2]]], "hopping")
        with pytest.raises(TypeError, match="must be a real number"):
            decoder.complex_matrix([[[True, 0]]], "hopping")
        with pytest.raises(OverflowError):
            decoder.complex_matrix([[[10**400, 0]]], "hopping")
