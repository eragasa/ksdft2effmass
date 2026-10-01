# ruff: noqa: E501
r"""Software verification for ``BlindAlignmentInputDeserializer``.

Evidence profile: claim_bearing

Facet and represented meaning
-----------------------------
The module owns version-one JSON adaptation into immutable blind-alignment campaign
controls.

Intrinsic and cross-object scope
--------------------------------
The retained input supplies the authoritative field vocabulary. Runtime mutations
exercise version, closed-field, Boolean, and numeric-string rejection. Reading that
retained artifact makes this an integration test rather than an isolated unit test.

VVUQ and scientific exclusions
------------------------------
A pass establishes wire adaptation only. It does not authenticate referenced files,
execute inference, verify retained numerical results, validate silicon, or perform
uncertainty quantification.
"""

import json
from pathlib import Path
from typing import cast

import pytest

from ksdft2effmass.campaigns.periodic_1d import (
    Periodic1DJsonValue,
)
from ksdft2effmass.campaigns.periodic_1d.defects.blind_alignment.serialization import (
    BlindAlignmentInputDeserializer,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]
SUT = BlindAlignmentInputDeserializer


class TestBlindAlignmentInputDeserializer:
    """Own strict version-one blind-alignment input adaptation evidence."""

    @staticmethod
    def retained_input_path() -> Path:
        """Return the immutable retained input used as the wire oracle."""
        directory = Path(__file__).resolve().parents[7]
        return directory / (
            "calculations/research-monograph/"
            "impurity-defect-1d-blind-alignment/input.json"
        )

    def retained_document(self) -> dict[str, Periodic1DJsonValue]:
        """Decode a mutable test-only copy of the retained JSON object."""
        return cast(
            dict[str, Periodic1DJsonValue],
            json.loads(self.retained_input_path().read_text(encoding="utf-8")),
        )

    @staticmethod
    def encode(document: dict[str, Periodic1DJsonValue]) -> bytes:
        """Encode one mutated runtime-scratch document."""
        return (json.dumps(document, sort_keys=True) + "\n").encode()

    def test_method__execute__decodes_retained_version_one_contract(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-008.

        Requirement: The deserializer must decode every retained version-one input
        field into the corresponding immutable typed record.

        Method: Decode the authenticated-by-repository retained input bytes without
        running the historical campaign.

        Oracle: Exact retained identifiers, policy values, case inventories, and
        diagnostic sequences.

        Acceptance: All selected typed fields equal their authored retained values.

        Interpretation: A pass establishes complete version-one input adaptation.

        Limitations: File identity authentication and numerical execution are outside
        this deserializer test.
        """
        result = SUT().execute(self.retained_input_path().read_bytes())

        assert result.experiment_id == (
            "research-monograph-impurity-defect-1d-blind-alignment-v1"
        )
        assert result.policy.anchor_rank_tolerance == 1.0e-10
        assert result.policy.maximum_anchor_condition_number == 1.0e6
        assert result.policy.maximum_principal_angle_radians == 0.35
        assert result.policy.minimum_energy_anchor_rank == 4
        assert result.core_radius_cells == 2
        assert tuple(value.identifier for value in result.exact_cases) == (
            "exact-spinless-full-rank",
            "exact-spinor-full-rank",
        )
        assert result.noise_sweep.unitary_noise_radians == (
            0.0,
            1.0e-8,
            1.0e-6,
            1.0e-4,
            1.0e-3,
            1.0e-2,
        )
        assert tuple(value.kind for value in result.stopping_cases) == (
            "anchor-condition",
            "principal-angle",
            "rank-mismatch",
            "spin-mismatch",
            "energy-anchor",
        )
        assert result.diagnostics.energy_anchor_ranks == (0, 1, 2, 3, 4, 8, 22)

    def test_method__execute__rejects_unsupported_schema(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-009.

        Requirement: Unsupported input schemas must stop before field interpretation.

        Method: Change only ``schema_version`` in a test-owned decoded copy.

        Oracle: Exact version-one gate and ``ValueError`` message.

        Acceptance: Decoding raises ``ValueError`` for the unsupported version.

        Interpretation: A pass establishes active schema gating under runtime checks.

        Limitations: This does not define migration behavior for a future schema.
        """
        document = self.retained_document()
        document["schema_version"] = 2

        with pytest.raises(ValueError, match="unsupported input schema version"):
            SUT().execute(self.encode(document))

    @pytest.mark.parametrize(
        ("field", "value", "message"),
        (
            pytest.param(
                "minimum_energy_anchor_rank",
                True,
                "minimum energy-anchor rank must be an integer",
                id="boolean_integer",
            ),
            pytest.param(
                "maximum_principal_angle_radians",
                "0.35",
                "maximum principal angle must be a real number",
                id="numeric_string",
            ),
        ),
    )
    def test_method__execute__rejects_erased_numeric_representations(
        self, field: str, value: Periodic1DJsonValue, message: str
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-010.

        Requirement: Boolean integers and numeric strings must not enter public
        numeric campaign fields.

        Method: Replace one inference-policy value while preserving valid JSON.

        Oracle: The explicit built-in numeric-type contract.

        Acceptance: Each semantic partition raises ``TypeError`` with its exact field
        message.

        Interpretation: A pass establishes strict runtime numeric typing.

        Limitations: Other malformed values are covered by their owning record
        invariants rather than this parameter family.
        """
        document = self.retained_document()
        policy = cast(dict[str, Periodic1DJsonValue], document["inference_policy"])
        policy[field] = value

        with pytest.raises(TypeError, match=message):
            SUT().execute(self.encode(document))

    def test_method__execute__rejects_additional_fields(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-011.

        Requirement: The version-one input is a closed record and must reject
        additional root fields.

        Method: Add one unknown root field to a test-owned copy.

        Oracle: Exact retained root-field inventory.

        Acceptance: Decoding raises ``ValueError`` identifying the additional field.

        Interpretation: A pass prevents silent extension or reinterpretation of v1.

        Limitations: This wire check makes no scientific claim about field values.
        """
        document = self.retained_document()
        document["unexpected"] = "value"

        with pytest.raises(ValueError, match="additional: unexpected"):
            SUT().execute(self.encode(document))
