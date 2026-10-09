"""Campaign-facing specialization of shared strict JSON decoding.

``CampaignJsonDecoder`` adds campaign ownership vocabulary only. Strict UTF-8 parsing,
duplicate-key rejection, closed JSON values, primitive checks, and binary64 conversion
are owned by :mod:`ksdft2effmass.serialization.json`.
"""

from ksdft2effmass.serialization.json import StrictJsonDecoder


class CampaignJsonDecoder(StrictJsonDecoder):
    """Decode strict JSON values at a campaign serialization boundary.

    The inherited decoder performs no schema selection, scientific construction, source
    authentication, filesystem access, provenance inference, or acceptance decision.
    Campaign serializers remain responsible for those domain-specific boundaries.
    """

    __slots__ = ()
