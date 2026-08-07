r"""Software verification of ``CpnToken``.

Facet and represented meaning
--------------------------------
Software verification of ``CpnToken`` public token-state contract.

Software-verification evidence covers the public ``CpnToken`` DataObject: a finite
software representation of workflow-control token state. No physical model or
mathematical operator is represented by these synthetic cases.

Intrinsic and cross-object scope
--------------------------------
The sole primary SUT is ``CpnToken``. The owned contract comprises public constructor
invariants, canonical stored identities, and operational immutability; its oracle is the
documented exact token contract and Python exception taxonomy. Inputs use synthetic
identifiers and the approved nonnegative signed-i64 control range without exercising
external services.

VVUQ and scientific exclusions
------------------------------
Passing confirms only the stated represented-software behavior; failure may indicate
production, fixture, oracle, or public-contract drift. This module does not provide
numerical verification, scientific validation, uncertainty quantification,
physical-correctness, persistence, SNAKES-adapter, cross-language, or
scientific-execution evidence."""

from collections.abc import Callable
from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.workflows.cpn import (
    CpnToken,
)

pytestmark = pytest.mark.software_verification

SUT = CpnToken


def test_constructor__routing_state__canonicalizes_and_freezes_token(
    token_factory: Callable[..., CpnToken],
) -> None:
    """Evidence ID
    -----------
    SV-CPN-001

    Requirement
    -----------
    ``CpnToken`` preserves the exact accepted state for its
    ``routing_state`` contract.

    Method
    ------
    Construct the public SUT and inspect retained exact public outcomes.

    Oracle
    ------
    The documented public invariant and fixed synthetic inputs provide the independent
    exact state oracle.

    Acceptance
    ----------
    Every retained exact state assertion holds.

    Interpretation
    --------------
    Pass supports only this accepted-state partition; failure may identify
    implementation, fixture, oracle, environment, or contract drift.

    Limitations
    -----------
    Synthetic cases exclude unexercised inputs, engine execution, persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    token = token_factory(
        "token-1",
        parent_run_id="parent-run",
        retry_parent_attempt_id="attempt-0",
        iteration_index=2,
        payload_type_id="payload.type",
        payload_id="payload-1",
        payload_schema_version=1,
        provenance_ids=("provenance-b", "provenance-a"),
        parent_token_ids=("parent-b", "parent-a"),
    )
    assert token.provenance_ids == ("provenance-a", "provenance-b")
    assert token.parent_token_ids == ("parent-a", "parent-b")


def test_constructor__routing_state__rejects_invalid_state(
    token_factory: Callable[..., CpnToken],
) -> None:
    """Evidence ID
    -----------
    SV-CPN-151

    Requirement
    -----------
    ``CpnToken`` rejects the documented invalid state for its
    ``routing_state`` contract.

    Method
    ------
    Exercise the retained synthetic invalid inputs through the public SUT.

    Oracle
    ------
    The documented public invariant and fixed synthetic inputs provide the independent
    exact error-taxonomy oracle.

    Acceptance
    ----------
    Every retained invalid call raises the documented exact public exception.

    Interpretation
    --------------
    Pass supports only this rejection partition; failure may identify
    implementation, fixture, oracle, environment, or contract drift.

    Limitations
    -----------
    Synthetic cases exclude unexercised inputs, engine execution, persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    token = token_factory(
        "token-1",
        parent_run_id="parent-run",
        retry_parent_attempt_id="attempt-0",
        iteration_index=2,
        payload_type_id="payload.type",
        payload_id="payload-1",
        payload_schema_version=1,
        provenance_ids=("provenance-b", "provenance-a"),
        parent_token_ids=("parent-b", "parent-a"),
    )
    with pytest.raises(FrozenInstanceError):
        token.run_id = "changed"  # type: ignore[misc]


def test_constructor__payload_reference__requires_all_fields_or_none(
    token_factory: Callable[..., CpnToken],
) -> None:
    """Verify rejection of a partial payload reference.

    Evidence ID
    SV-CPN-002

    Requirement
    A public ``CpnToken`` payload reference must supply payload type, payload identity,
    and schema version together, or omit all three.

    Method
    Construct through ``token_factory`` with only ``payload_type_id`` present, creating
    the controlled-invalid partial-reference boundary. No warnings are expected.

    Oracle
    The documented all-or-none payload-reference invariant independently makes a
    one-field reference invalid and assigns invariant violations to ``ValueError``.

    Acceptance
    Construction raises ``ValueError`` with text matching ``all present or all absent``.

    Interpretation
    A pass confirms enforcement of relational payload-reference completeness. A failure
    may arise from constructor, fixture, message, taxonomy, or contract drift and would
    permit unusable represented state if construction succeeds.

    Limitations
    The synthetic reference does not test payload content, schema validity, persistence,
    numerical verification, physical correctness, scientific validation, uncertainty
    quantification, or cross-language behavior."""
    with pytest.raises(ValueError, match="all present or all absent"):
        token_factory("token-1", payload_type_id="payload.type")


def test_field__iteration_index__rejects_boolean(
    token_factory: Callable[..., CpnToken],
) -> None:
    """Verify Boolean rejection at the iteration-index boundary.

    Evidence ID
    SV-CPN-003

    Requirement
    The public ``iteration_index`` field must accept an exact integer contract rather
    than treating Python Boolean values as integers.

    Method
    Invoke public token construction through ``token_factory`` with
    ``iteration_index=True`` as a controlled semantic-type fault. No warnings are
    expected.

    Oracle
    The documented public type taxonomy distinguishes ``bool`` from the exact
    nonnegative integer required for an iteration index and assigns wrong semantic types
    to ``TypeError``.

    Acceptance
    Construction raises ``TypeError`` whose message names ``iteration_index``.

    Interpretation
    A pass confirms the Boolean/integer boundary; any other result may indicate
    constructor, fixture, error-message, taxonomy, or contract drift.

    Limitations
    This case excludes integer width and overflow, payload behavior, numerical
    verification, physical correctness, scientific validation, uncertainty
    quantification, and cross-language conformance."""
    with pytest.raises(TypeError, match="iteration_index"):
        token_factory("token-1", iteration_index=True)


def test_constructor__required_identities__rejects_wrong_types(
    token_factory: Callable[..., CpnToken],
) -> None:
    """Evidence ID
    -----------
    SV-CPN-063

    Requirement
    -----------
    ``CpnToken`` rejects wrong semantic types at the public
    constructor boundary for its
    ``required_identities`` contract.

    Method
    ------
    Exercise each preserved synthetic wrong-type input through the public SUT with
    no warning acceptance or private-state mutation.

    Oracle
    ------
    The documented public exact-type taxonomy and Python exception taxonomy
    independently require ``TypeError`` for these inputs.

    Acceptance
    ----------
    Every preserved partition assertion raises exactly ``TypeError``; retained
    exact setup and state assertions also hold.

    Interpretation
    --------------
    Pass supports only this named type partition; failure may identify implementation,
    fixture, oracle-transcription, environment, or public-contract drift.

    Limitations
    -----------
    Synthetic cases exclude unexercised inputs, engine execution, persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    with pytest.raises(TypeError):
        token_factory(1)
    with pytest.raises(TypeError):
        token_factory("token", color_id=1)
    with pytest.raises(TypeError):
        token_factory("token", workflow_id=1)
    with pytest.raises(TypeError):
        token_factory("token", run_id=1)
    with pytest.raises(TypeError):
        token_factory("token", attempt_id=1)


def test_constructor__required_identities__rejects_invalid_values(
    token_factory: Callable[..., CpnToken],
) -> None:
    """Evidence ID
    -----------
    SV-CPN-113

    Requirement
    -----------
    ``CpnToken`` rejects malformed values of accepted semantic
    types for its
    ``required_identities`` contract.

    Method
    ------
    Exercise each preserved synthetic invalid-value input through the public SUT with
    no warning acceptance or private-state mutation.

    Oracle
    ------
    The documented public value invariant and Python exception taxonomy
    independently require ``ValueError`` for these inputs.

    Acceptance
    ----------
    Every preserved partition assertion raises exactly ``ValueError``; retained
    exact setup and state assertions also hold.

    Interpretation
    --------------
    Pass supports only this named value partition; failure may identify implementation,
    fixture, oracle-transcription, environment, or public-contract drift.

    Limitations
    -----------
    Synthetic cases exclude unexercised inputs, engine execution, persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    with pytest.raises(ValueError):
        token_factory("")
    with pytest.raises(ValueError):
        token_factory("token", color_id="")
    with pytest.raises(ValueError):
        token_factory("token", workflow_id="")
    with pytest.raises(ValueError):
        token_factory("token", run_id="")
    with pytest.raises(ValueError):
        token_factory("token", attempt_id="")


def test_constructor__optional_identities__rejects_wrong_types(
    token_factory: Callable[..., CpnToken],
) -> None:
    """Evidence ID
    -----------
    SV-CPN-064

    Requirement
    -----------
    ``CpnToken`` rejects wrong semantic types at the public
    constructor boundary for its
    ``optional_identities`` contract.

    Method
    ------
    Exercise each preserved synthetic wrong-type input through the public SUT with
    no warning acceptance or private-state mutation.

    Oracle
    ------
    The documented public exact-type taxonomy and Python exception taxonomy
    independently require ``TypeError`` for these inputs.

    Acceptance
    ----------
    Every preserved partition assertion raises exactly ``TypeError``; retained
    exact setup and state assertions also hold.

    Interpretation
    --------------
    Pass supports only this named type partition; failure may identify implementation,
    fixture, oracle-transcription, environment, or public-contract drift.

    Limitations
    -----------
    Synthetic cases exclude unexercised inputs, engine execution, persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    with pytest.raises(TypeError):
        token_factory("token", parent_run_id=1)
    with pytest.raises(TypeError):
        token_factory("token", retry_parent_attempt_id=1)
    with pytest.raises(TypeError):
        token_factory("token", correlation_id=1)
    with pytest.raises(TypeError):
        token_factory("token", authorization_id=1)
    complete_payload = {
        "payload_type_id": "type",
        "payload_id": "payload",
        "payload_schema_version": 1,
    }
    with pytest.raises(TypeError):
        token_factory("token", **(complete_payload | {"payload_type_id": 1}))
    with pytest.raises(TypeError):
        token_factory("token", **(complete_payload | {"payload_id": 1}))


def test_constructor__optional_identities__rejects_invalid_values(
    token_factory: Callable[..., CpnToken],
) -> None:
    """Evidence ID
    -----------
    SV-CPN-114

    Requirement
    -----------
    ``CpnToken`` rejects malformed values of accepted semantic
    types for its
    ``optional_identities`` contract.

    Method
    ------
    Exercise each preserved synthetic invalid-value input through the public SUT with
    no warning acceptance or private-state mutation.

    Oracle
    ------
    The documented public value invariant and Python exception taxonomy
    independently require ``ValueError`` for these inputs.

    Acceptance
    ----------
    Every preserved partition assertion raises exactly ``ValueError``; retained
    exact setup and state assertions also hold.

    Interpretation
    --------------
    Pass supports only this named value partition; failure may identify implementation,
    fixture, oracle-transcription, environment, or public-contract drift.

    Limitations
    -----------
    Synthetic cases exclude unexercised inputs, engine execution, persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    with pytest.raises(ValueError):
        token_factory("token", parent_run_id="")
    with pytest.raises(ValueError):
        token_factory("token", retry_parent_attempt_id="")
    with pytest.raises(ValueError):
        token_factory("token", correlation_id="")
    with pytest.raises(ValueError):
        token_factory("token", authorization_id="")
    complete_payload = {
        "payload_type_id": "type",
        "payload_id": "payload",
        "payload_schema_version": 1,
    }
    with pytest.raises(ValueError):
        token_factory("token", **(complete_payload | {"payload_type_id": ""}))
    with pytest.raises(ValueError):
        token_factory("token", **(complete_payload | {"payload_id": ""}))


def test_field__iteration_index__preserves_valid_state(
    token_factory: Callable[..., CpnToken],
) -> None:
    """Evidence ID
    -----------
    SV-CPN-065

    Requirement
    -----------
    ``CpnToken`` preserves the documented exact valid-state behavior for its
    ``iteration_index`` contract.

    Method
    ------
    Construct the public SUT with the retained valid synthetic inputs and inspect
    exact public state.

    Oracle
    ------
    The fixed inputs and documented canonical public representation provide the
    independent exact oracle.

    Acceptance
    ----------
    Every retained exact identity, equality, ordering, type, and represented-state
    assertion holds.

    Interpretation
    --------------
    Pass supports this valid-state mapping; failure may identify implementation,
    fixture, oracle, environment, or contract drift.

    Limitations
    -----------
    Synthetic cases exclude unexercised inputs, engine execution, persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    assert token_factory("token", iteration_index=0).iteration_index == 0


def test_field__iteration_index__rejects_wrong_types(
    token_factory: Callable[..., CpnToken],
) -> None:
    """Evidence ID
    -----------
    SV-CPN-136

    Requirement
    -----------
    ``CpnToken`` rejects wrong semantic types for its ``iteration_index`` contract.

    Method
    ------
    Exercise every retained synthetic wrong-type input through the public SUT
    without private mutation.

    Oracle
    ------
    The documented exact-type taxonomy independently requires ``TypeError`` for
    every retained call.

    Acceptance
    ----------
    Every retained wrong-type call raises exactly ``TypeError``.

    Interpretation
    --------------
    Pass supports this type partition; failure may identify implementation, fixture,
    oracle, environment, or contract drift.

    Limitations
    -----------
    Synthetic cases exclude unexercised inputs, engine execution, persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    with pytest.raises(TypeError):
        token_factory("token", iteration_index=1.0)


def test_field__iteration_index__rejects_invalid_values(
    token_factory: Callable[..., CpnToken],
) -> None:
    """Evidence ID
    -----------
    SV-CPN-115

    Requirement
    -----------
    ``CpnToken`` rejects malformed values of accepted semantic
    types for its
    ``iteration_index`` contract.

    Method
    ------
    Exercise each preserved synthetic invalid-value input through the public SUT with
    no warning acceptance or private-state mutation.

    Oracle
    ------
    The documented public value invariant and Python exception taxonomy
    independently require ``ValueError`` for these inputs.

    Acceptance
    ----------
    Every preserved partition assertion raises exactly ``ValueError``; retained
    exact setup and state assertions also hold.

    Interpretation
    --------------
    Pass supports only this named value partition; failure may identify implementation,
    fixture, oracle-transcription, environment, or public-contract drift.

    Limitations
    -----------
    Synthetic cases exclude unexercised inputs, engine execution, persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    with pytest.raises(ValueError):
        token_factory("token", iteration_index=-1)


def test_field__payload_schema_version__preserves_valid_state(
    token_factory: Callable[..., CpnToken],
) -> None:
    """Evidence ID
    -----------
    SV-CPN-066

    Requirement
    -----------
    ``CpnToken`` preserves the documented exact valid-state behavior for its
    ``payload_schema_version`` contract.

    Method
    ------
    Construct the public SUT with the retained valid synthetic inputs and inspect
    exact public state.

    Oracle
    ------
    The fixed inputs and documented canonical public representation provide the
    independent exact oracle.

    Acceptance
    ----------
    Every retained exact identity, equality, ordering, type, and represented-state
    assertion holds.

    Interpretation
    --------------
    Pass supports this valid-state mapping; failure may identify implementation,
    fixture, oracle, environment, or contract drift.

    Limitations
    -----------
    Synthetic cases exclude unexercised inputs, engine execution, persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    base = {"payload_type_id": "type", "payload_id": "payload"}
    assert (
        token_factory("token", **base, payload_schema_version=0).payload_schema_version
        == 0
    )


def test_field__payload_schema_version__rejects_wrong_types(
    token_factory: Callable[..., CpnToken],
) -> None:
    """Evidence ID
    -----------
    SV-CPN-137

    Requirement
    -----------
    ``CpnToken`` rejects wrong semantic types for its ``payload_schema_version``
    contract.

    Method
    ------
    Exercise every retained synthetic wrong-type input through the public SUT
    without private mutation.

    Oracle
    ------
    The documented exact-type taxonomy independently requires ``TypeError`` for
    every retained call.

    Acceptance
    ----------
    Every retained wrong-type call raises exactly ``TypeError``.

    Interpretation
    --------------
    Pass supports this type partition; failure may identify implementation, fixture,
    oracle, environment, or contract drift.

    Limitations
    -----------
    Synthetic cases exclude unexercised inputs, engine execution, persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    base = {"payload_type_id": "type", "payload_id": "payload"}
    with pytest.raises(TypeError):
        token_factory("token", **base, payload_schema_version=True)


def test_field__payload_schema_version__rejects_invalid_values(
    token_factory: Callable[..., CpnToken],
) -> None:
    """Evidence ID
    -----------
    SV-CPN-116

    Requirement
    -----------
    ``CpnToken`` rejects malformed values of accepted semantic
    types for its
    ``payload_schema_version`` contract.

    Method
    ------
    Exercise each preserved synthetic invalid-value input through the public SUT with
    no warning acceptance or private-state mutation.

    Oracle
    ------
    The documented public value invariant and Python exception taxonomy
    independently require ``ValueError`` for these inputs.

    Acceptance
    ----------
    Every preserved partition assertion raises exactly ``ValueError``; retained
    exact setup and state assertions also hold.

    Interpretation
    --------------
    Pass supports only this named value partition; failure may identify implementation,
    fixture, oracle-transcription, environment, or public-contract drift.

    Limitations
    -----------
    Synthetic cases exclude unexercised inputs, engine execution, persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    base = {"payload_type_id": "type", "payload_id": "payload"}
    with pytest.raises(ValueError):
        token_factory("token", **base, payload_schema_version=-1)


def test_field__expression_visible_controls__enforces_nonnegative_i64_range(
    token_factory: Callable[..., CpnToken],
) -> None:
    """Evidence ID
    -----------
    SV-CPN-082

    Requirement
    -----------
    ``CpnToken`` preserves the exact accepted state for its
    ``expression_visible_controls`` contract.

    Method
    ------
    Construct the public SUT and inspect retained exact public outcomes.

    Oracle
    ------
    The documented public invariant and fixed synthetic inputs provide the independent
    exact state oracle.

    Acceptance
    ----------
    Every retained exact state assertion holds.

    Interpretation
    --------------
    Pass supports only this accepted-state partition; failure may identify
    implementation, fixture, oracle, environment, or contract drift.

    Limitations
    -----------
    Synthetic cases exclude unexercised inputs, engine execution, persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    maximum = 2**63 - 1
    payload_min = token_factory(
        "payload-min",
        payload_type_id="type",
        payload_id="payload-id",
        payload_schema_version=0,
    )
    payload_max = token_factory(
        "payload-max",
        payload_type_id="type",
        payload_id="payload-id",
        payload_schema_version=maximum,
    )
    assert token_factory("iteration-min", iteration_index=0).iteration_index == 0
    assert (
        token_factory("iteration-max", iteration_index=maximum).iteration_index
        == maximum
    )
    assert payload_min.payload_schema_version == 0
    assert payload_max.payload_schema_version == maximum


def test_field__expression_visible_controls__rejects_invalid_state(
    token_factory: Callable[..., CpnToken],
) -> None:
    """Evidence ID
    -----------
    SV-CPN-152

    Requirement
    -----------
    ``CpnToken`` rejects the documented invalid state for its
    ``expression_visible_controls`` contract.

    Method
    ------
    Exercise the retained synthetic invalid inputs through the public SUT.

    Oracle
    ------
    The documented public invariant and fixed synthetic inputs provide the independent
    exact error-taxonomy oracle.

    Acceptance
    ----------
    Every retained invalid call raises the documented exact public exception.

    Interpretation
    --------------
    Pass supports only this rejection partition; failure may identify
    implementation, fixture, oracle, environment, or contract drift.

    Limitations
    -----------
    Synthetic cases exclude unexercised inputs, engine execution, persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    maximum = 2**63 - 1
    token_factory(
        "payload-min",
        payload_type_id="type",
        payload_id="payload-id",
        payload_schema_version=0,
    )
    token_factory(
        "payload-max",
        payload_type_id="type",
        payload_id="payload-id",
        payload_schema_version=maximum,
    )
    with pytest.raises(ValueError, match="signed i64"):
        token_factory("iteration-overflow", iteration_index=2**63)
    with pytest.raises(ValueError, match="signed i64"):
        token_factory(
            "payload-overflow",
            payload_type_id="type",
            payload_id="payload-id",
            payload_schema_version=2**63,
        )


def test_constructor__identity_tuples_and_outcome__rejects_wrong_types(
    token_factory: Callable[..., CpnToken],
) -> None:
    """Evidence ID
    -----------
    SV-CPN-067

    Requirement
    -----------
    ``CpnToken`` rejects wrong semantic types at the public
    constructor boundary for its
    ``identity_tuples_and_outcome`` contract.

    Method
    ------
    Exercise each preserved synthetic wrong-type input through the public SUT with
    no warning acceptance or private-state mutation.

    Oracle
    ------
    The documented public exact-type taxonomy and Python exception taxonomy
    independently require ``TypeError`` for these inputs.

    Acceptance
    ----------
    Every preserved partition assertion raises exactly ``TypeError``; retained
    exact setup and state assertions also hold.

    Interpretation
    --------------
    Pass supports only this named type partition; failure may identify implementation,
    fixture, oracle-transcription, environment, or public-contract drift.

    Limitations
    -----------
    Synthetic cases exclude unexercised inputs, engine execution, persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    with pytest.raises(TypeError):
        token_factory("token", provenance_ids=["p"])
    with pytest.raises(TypeError):
        token_factory("token", provenance_ids=(1,))
    with pytest.raises(TypeError):
        token_factory("token", parent_token_ids=["p"])
    with pytest.raises(TypeError):
        token_factory("token", parent_token_ids=(1,))
    with pytest.raises(TypeError):
        token_factory("token", outcome=True)


def test_constructor__identity_tuples_and_outcome__rejects_invalid_values(
    token_factory: Callable[..., CpnToken],
) -> None:
    """Evidence ID
    -----------
    SV-CPN-117

    Requirement
    -----------
    ``CpnToken`` rejects malformed values of accepted semantic
    types for its
    ``identity_tuples_and_outcome`` contract.

    Method
    ------
    Exercise each preserved synthetic invalid-value input through the public SUT with
    no warning acceptance or private-state mutation.

    Oracle
    ------
    The documented public value invariant and Python exception taxonomy
    independently require ``ValueError`` for these inputs.

    Acceptance
    ----------
    Every preserved partition assertion raises exactly ``ValueError``; retained
    exact setup and state assertions also hold.

    Interpretation
    --------------
    Pass supports only this named value partition; failure may identify implementation,
    fixture, oracle-transcription, environment, or public-contract drift.

    Limitations
    -----------
    Synthetic cases exclude unexercised inputs, engine execution, persistence,
    numerical verification, scientific validation, UQ, physics, and portability.
    """
    with pytest.raises(ValueError):
        token_factory("token", provenance_ids=("",))
    with pytest.raises(ValueError):
        token_factory("token", provenance_ids=("p", "p"))
    with pytest.raises(ValueError):
        token_factory("token", parent_token_ids=("",))
    with pytest.raises(ValueError):
        token_factory("token", parent_token_ids=("p", "p"))
