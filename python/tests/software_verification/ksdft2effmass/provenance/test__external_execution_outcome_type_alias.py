r"""Software verification of external execution outcome type alias.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

-----------------------------
This artifact-owned software evidence verifies the concrete internal artifact
``ksdft2effmass.provenance.external_execution.ExternalExecutionOutcome``. The
alias names exactly the successful-result and structured-failure record families
in declaration order without creating a runtime wrapper or stored state.

Intrinsic and cross-object scope

--------------------------------
The primary artifact is the defining-module type alias. ``ExternalExecutionResult``
and ``ExternalExecutionFailure`` are its exact union arguments. The package
module is inspected only to verify the accepted nonexport boundary. Python union
introspection and the accepted package inventory provide the oracles.

VVUQ and scientific exclusions

------------------------------
Passing establishes only the internal typing decomposition, argument order,
nonexport boundary, and absence of a runtime wrapper. It does not establish
result or failure field behavior, execution success, output correctness,
provenance truth, numerical verification, scientific validation, UQ,
portability, or cross-language agreement.
"""  # noqa: E501

from types import UnionType
from typing import get_args, get_origin

import pytest

import ksdft2effmass.provenance as provenance_package
from ksdft2effmass.provenance import (
    ExternalExecutionFailure,
    ExternalExecutionResult,
)
from ksdft2effmass.provenance.external_execution import ExternalExecutionOutcome

pytestmark = pytest.mark.software_verification


def test_artifact__external_execution_outcome__preserves_internal_union_boundary() -> (
    None
):
    """Evidence ID: SV-PROV-226

    Requirement: The internal defining-module alias is exactly the ordered
    result/failure union,
    is not a public package export, and adds no runtime wrapper or stored state.

    Method: Inspect union arguments and origin, package attribute absence, and alias
    state.

    Oracle: The accepted decomposition orders ExternalExecutionResult before
    ExternalExecutionFailure; the accepted package inventory omits the alias, and
    PEP 604 union construction has UnionType origin without an instance dictionary.

    Acceptance: Arguments equal the two classes in declaration order, origin is
    UnionType, the
    package lacks the alias attribute, and the alias has no instance dictionary.

    Interpretation: Passing establishes the exact internal collaborator decomposition
    and boundary;
    failure identifies defining-module, package-inventory, or oracle drift.

    Limitations: The alias is not a field, class, property, or public package object;
    this test
    owns no result/failure behavior or execution and scientific claims.
    """
    assert get_args(ExternalExecutionOutcome) == (
        ExternalExecutionResult,
        ExternalExecutionFailure,
    )
    assert get_origin(ExternalExecutionOutcome) is UnionType
    assert not hasattr(provenance_package, "ExternalExecutionOutcome")
    assert not hasattr(ExternalExecutionOutcome, "__dict__")
