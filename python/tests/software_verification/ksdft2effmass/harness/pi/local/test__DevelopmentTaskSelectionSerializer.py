r"""Software verification of ``DevelopmentTaskSelectionSerializer``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module verifies canonical JSON serialization of minimal Task selection state.

Intrinsic and cross-object scope

The sole primary SUT is ``DevelopmentTaskSelectionSerializer``. Canonical field
order, JSON shape, UTF-8 byte representation, and exact-input typing are covered.

VVUQ and scientific exclusions

Passing establishes wire-format software behavior only. It provides no activation,
authority, persistence, scientific validation, or uncertainty-quantification claim.
"""

import pytest

from ksdft2effmass.harness.pi.local import (
    DevelopmentTaskSelection,
    DevelopmentTaskSelectionSerializer,
)

pytestmark = pytest.mark.software_verification
SUT = DevelopmentTaskSelectionSerializer


def test_method__execute__emits_exact_canonical_inactive_json() -> None:
    """Evidence ID: SV-HT-107

    Requirement: Serialization emits the exact version-1 inactive representation.

    Method: Serialize the canonical inactive DataObject and compare exact bytes.

    Oracle: The accepted wire contract independently fixes field order, indentation,
    JSON values, UTF-8, and one final LF.

    Acceptance: Output equals the maintained canonical byte literal.

    Interpretation: Failure identifies wire-format drift.

    Limitations: Byte agreement does not establish repository publication.
    """
    expected = (
        b'{\n  "schema_version": 1,\n  "active_task_id": null,\n'
        b'  "explicit_activation_receipt_ids": [],\n'
        b'  "automatic_successor_activation": false\n}\n'
    )
    assert SUT().execute(DevelopmentTaskSelection(1, None, (), False)) == expected


def test_method__execute__requires_exact_selection_type() -> None:
    """Evidence ID: SV-HT-108

    Requirement: The serializer accepts only the exact public selection DataObject.

    Method: Supply an unrelated object.

    Oracle: The public ActionObject contract fixes exact input typing.

    Acceptance: Serialization raises ``TypeError`` without output.

    Interpretation: Failure identifies implicit mapping or duck-type acceptance.

    Limitations: Deserialization behavior is separately owned.
    """
    with pytest.raises(TypeError, match="DevelopmentTaskSelection"):
        SUT().execute(object())  # type: ignore[arg-type]
