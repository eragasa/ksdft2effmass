r"""Software verification of ``Periodic1DCampaignJsonDecoder``.

Evidence profile: claim_bearing

Bounded artifact scope: public periodic-1D campaign JSON primitive decoding.

Facet and represented meaning

The decoder exposes closed JSON representations used by versioned campaign serializers.

Intrinsic and cross-object scope

Exact primitive typing, finite reals, and explicit unitless quantities are included.

VVUQ and scientific exclusions

No campaign execution, numerical result, or scientific conclusion is assessed.
"""

import numpy as np
import pytest

from ksdft2effmass.operators import Unitless
from ksdft2effmass.periodic1d.campaign import Periodic1DCampaignJsonDecoder

pytestmark = pytest.mark.software_verification
SUT = Periodic1DCampaignJsonDecoder


class TestPeriodic1DCampaignJsonDecoder:
    """Own contract evidence for the public campaign JSON decoder."""

    def test_contract__has_canonical_module_ownership(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DECODER-000.

        Requirement: The shared decoder belongs to the canonical campaign namespace.
        Acceptance: Its defining module is canonical rather than a forwarding alias.
        """
        assert Periodic1DCampaignJsonDecoder.__module__ == (
            "ksdft2effmass.periodic1d.campaign.serialization.decoding"
        )

    def test_method__document_and_quantities__decode_closed_representations(
        self,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-005

        Requirement: Public decoding preserves exact JSON types and explicit units.

        Method: Decode one object and adapt its scalar, vector, and integer inventory.

        Oracle: Authored literal values and the required ``Unitless`` marker.

        Acceptance: Values, binary64 vector representation, and unit marker agree.

        Interpretation: A pass verifies reusable public wire decoding mechanics.

        Limitations: Versioned campaign field schemas are tested by their serializers.

        Provenance: Authored deterministic software-verification values.
        """
        decoder = SUT()
        document = decoder.document(b'{"count":3,"scale":0.5,"values":[1,2]}')

        assert decoder.integer(document["count"], "count") == 3
        assert decoder.scalar(document["scale"], "scale").magnitude == 0.5
        vector = decoder.vector(document["values"], "values")
        assert isinstance(vector.unit, Unitless)
        np.testing.assert_array_equal(vector.magnitude, np.asarray([1.0, 2.0]))

    def test_method__complex_vector__decodes_strict_immutable_pairs(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-007.

        Requirement: Reusable periodic-1D complex-vector wire decoding must preserve
        pair order and reject malformed or coercive components.

        Method: Decode finite integer/float pairs plus an empty vector, then exercise
        malformed-length, Boolean, nonfinite, and overflowing components.

        Oracle: Authored ``complex128`` values and the strict JSON numeric contract.

        Acceptance: Values and dtype agree, outputs are non-writeable, and every
        unsupported representation fails through its documented exception category.

        Interpretation: A pass verifies wire adaptation only; it assigns no basis,
        units, provenance, scientific identity, or acceptance status.

        Limitations: Campaign schemas separately own vector cardinality and meaning.
        """
        decoder = SUT()

        vector = decoder.complex_vector([[1, 2.5], [-3.0, 0]], "hoppings")
        empty = decoder.complex_vector([], "empty")

        assert vector.dtype == np.dtype(np.complex128)
        np.testing.assert_array_equal(
            vector, np.asarray([1.0 + 2.5j, -3.0 + 0.0j], dtype=np.complex128)
        )
        assert vector.shape == (2,)
        assert empty.shape == (0,)
        assert not vector.flags.writeable
        assert not empty.flags.writeable
        with pytest.raises(TypeError, match="entries must be complex pairs"):
            decoder.complex_vector([[1, 0, 2]], "hoppings")
        with pytest.raises(TypeError, match="entries must be complex pairs"):
            decoder.complex_vector([1], "hoppings")
        with pytest.raises(TypeError, match="must be a real number"):
            decoder.complex_vector([[True, 0]], "hoppings")
        with pytest.raises(ValueError, match="must be finite"):
            decoder.complex_vector([[float("inf"), 0]], "hoppings")
        with pytest.raises(OverflowError):
            decoder.complex_vector([[10**400, 0]], "hoppings")

    def test_method__real__rejects_boolean_and_nonfinite_values(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-006

        Requirement: Boolean and nonfinite JSON values are not accepted as reals.

        Method: Pass explicit invalid representations to ``real``.

        Oracle: The public numeric-input contract.

        Acceptance: Boolean raises ``TypeError`` and infinity raises ``ValueError``.

        Interpretation: A pass verifies strict numeric boundary behavior.

        Limitations: This does not establish campaign-specific value invariants.

        Provenance: Authored deterministic software-verification values.
        """
        decoder = SUT()

        with pytest.raises(TypeError, match="real number"):
            decoder.real(True, "value")
        with pytest.raises(ValueError, match="finite"):
            decoder.real(float("inf"), "value")
