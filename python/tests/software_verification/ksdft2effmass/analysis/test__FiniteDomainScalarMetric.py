r"""Software verification of ``FiniteDomainScalarMetric``.

Evidence profile: routine

Bounded artifact scope: exact scalar diagnostic identity and unit for finite-domain
channel ResultObjects.

Facet and represented meaning

The DataObject prevents channel values with different meanings or units from sharing an
unidentified numeric field.

Intrinsic and cross-object scope

Unitless identity retention and empty-identity rejection are included.

VVUQ and scientific exclusions

This is software contract evidence, not numerical or scientific validation, UQ,
campaign execution, or human acceptance.
"""

import pytest

from ksdft2effmass.analysis.finite_domains import FiniteDomainScalarMetric
from ksdft2effmass.operators import Unitless

pytestmark = pytest.mark.software_verification
SUT = FiniteDomainScalarMetric


class TestFiniteDomainScalarMetric:
    """Own software evidence for exact scalar metric identity."""

    def test_constructor__identity_and_unit__requires_explicit_nonempty_values(
        self,
    ) -> None:
        """Evidence ID: SV-ANALYSIS-FINITE-DOMAIN-METRIC-001

        Requirement: Every channel metric has a nonempty identity and explicit unit.

        Acceptance: A unitless metric retains both fields and an empty identity raises
        ``ValueError``.
        """
        metric = FiniteDomainScalarMetric("synthetic_metric", Unitless())

        assert metric.identifier == "synthetic_metric"
        assert type(metric.unit) is Unitless
        with pytest.raises(ValueError, match="nonempty"):
            FiniteDomainScalarMetric("", Unitless())
