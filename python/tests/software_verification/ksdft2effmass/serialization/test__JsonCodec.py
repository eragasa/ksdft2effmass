r"""Software verification of ``JsonCodec``.

Evidence profile: routine

Bounded artifact scope: public JSON serialization abstract contracts.

Facet and represented meaning

Production JSON codecs with direct value-returning methods share nominal abstract
serialization and deserialization ownership.

Intrinsic and cross-object scope

ActionObjects returning operational ResultObjects are intentionally excluded.

VVUQ and scientific exclusions

This structural test makes no scientific, numerical, or wire-compatibility claim.
"""

import pytest

from ksdft2effmass.campaigns.research_monograph.impurity_defect_2d import (
    FiniteDomainEffectsCaseInventoryJsonSerializer,
)
from ksdft2effmass.campaigns.research_monograph.periodic_1d import (
    Periodic1DCompositeCampaignJsonSerializer,
    Periodic1DIsolatedBandCampaignJsonSerializer,
    Periodic1DIsolatedBandResultJsonSerializer,
    Periodic1DRetainedResultJsonSerializer,
    Periodic1DStressCampaignJsonSerializer,
    Periodic1DStressResultJsonSerializer,
)
from ksdft2effmass.ksdft.pw import KohnShamPlaneWaveCalculationRecordJsonSerializer
from ksdft2effmass.operators import OperatorRecordJsonSerializer
from ksdft2effmass.provenance import ProvenanceJsonSerializer
from ksdft2effmass.serialization import JsonCodec

pytestmark = pytest.mark.software_verification
SUT = JsonCodec

type CodecClass = (
    type[FiniteDomainEffectsCaseInventoryJsonSerializer]
    | type[Periodic1DIsolatedBandCampaignJsonSerializer]
    | type[Periodic1DStressCampaignJsonSerializer]
    | type[Periodic1DCompositeCampaignJsonSerializer]
    | type[Periodic1DRetainedResultJsonSerializer]
    | type[Periodic1DIsolatedBandResultJsonSerializer]
    | type[Periodic1DStressResultJsonSerializer]
    | type[KohnShamPlaneWaveCalculationRecordJsonSerializer]
    | type[OperatorRecordJsonSerializer]
    | type[ProvenanceJsonSerializer]
)

CODEC_CLASSES = (
    pytest.param(
        FiniteDomainEffectsCaseInventoryJsonSerializer,
        id="finite_domain_inventory_wire",
    ),
    pytest.param(
        Periodic1DIsolatedBandCampaignJsonSerializer,
        id="isolated_campaign_wire",
    ),
    pytest.param(
        Periodic1DStressCampaignJsonSerializer,
        id="stress_campaign_wire",
    ),
    pytest.param(
        Periodic1DCompositeCampaignJsonSerializer,
        id="composite_campaign_wire",
    ),
    pytest.param(
        Periodic1DRetainedResultJsonSerializer,
        id="retained_result_wire",
    ),
    pytest.param(
        Periodic1DIsolatedBandResultJsonSerializer,
        id="isolated_result_wire",
    ),
    pytest.param(
        Periodic1DStressResultJsonSerializer,
        id="stress_result_wire",
    ),
    pytest.param(
        KohnShamPlaneWaveCalculationRecordJsonSerializer,
        id="plane_wave_calculation_wire",
    ),
    pytest.param(OperatorRecordJsonSerializer, id="represented_operator_wire"),
    pytest.param(ProvenanceJsonSerializer, id="provenance_record_wire"),
)


class TestJsonCodec:
    """Own structural evidence for the shared public JSON codec ABC."""

    @pytest.mark.parametrize("codec_class", CODEC_CLASSES)
    def test_method__subclass_contract__covers_direct_json_codecs(
        self, codec_class: CodecClass
    ) -> None:
        """Evidence ID: SV-SERIALIZATION-001

        Requirement: Direct JSON codecs inherit the common nominal ABC.

        Acceptance: Every explicitly inventoried production codec is a ``JsonCodec``
        subclass.
        """
        assert issubclass(codec_class, SUT)
