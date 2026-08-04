"""Software verification for ``CpnDefinitionValidator`` as the sole primary SUT.

Evidence class: software verification. Requirement and strategy are stated per
case; public construction/execution supplies the method and exact state or the
documented exception taxonomy supplies the independent oracle. Passing verifies
only the named class contract. It does not provide numerical verification,
scientific validation, uncertainty quantification, persistence, SNAKES-adapter,
Rust-conformance, or scientific-execution evidence. Collaborators are synthetic
setup only.
"""

import pytest

from ksdft2effmass.workflows.cpn import (
    CpnDefinitionValidator,
    CpnNetDefinition,
)

pytestmark = pytest.mark.software_verification

SUT = CpnDefinitionValidator


def test_cpn_sv_p1_011_complete_net_mapping_validates(
    executable_net: CpnNetDefinition,
) -> None:
    """SV-CPN-011: complete executable representation of the CPN tuple.

    Requirement
    -----------
    The version-1 P1 contract requires complete executable representation of the CPN
    tuple.

    Method
    ------
    Run ``CpnDefinitionValidator.execute`` on the complete ``executable_net``.

    Independent oracle
    ------------------
    The synthetic fixture explicitly supplies every member of
    N=(P,T,A,Sigma,C,G,E,I) with consistent references.

    Acceptance criterion
    --------------------
    The validator-owned ``is_valid`` result is true and carries no issue.

    Failure interpretation
    ----------------------
    Any issue means a known-consistent public net is rejected or incomplete.

    Limitations
    -----------
    This establishes contract structure, not scientific-workflow adequacy.
    """
    result = CpnDefinitionValidator().execute(executable_net)
    assert result.is_valid
