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

from ksdft2effmass.campaigns.research_monograph import (
    Periodic1DCampaignJsonDecoder,
)
from ksdft2effmass.operators import Unitless

pytestmark = pytest.mark.software_verification
SUT = Periodic1DCampaignJsonDecoder


class TestPeriodic1DCampaignJsonDecoder:
    """Own contract evidence for the public campaign JSON decoder."""

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
