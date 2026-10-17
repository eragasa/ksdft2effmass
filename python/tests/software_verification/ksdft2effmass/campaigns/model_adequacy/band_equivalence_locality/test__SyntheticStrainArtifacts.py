"""Software verification for typed synthetic-strain artifact boundaries."""

import json
import math
from pathlib import Path

import pytest
from jsonschema import ValidationError  # type: ignore[import-untyped]

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain import (
    SyntheticStrainCalculator,
    SyntheticStrainPath,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain_response import (  # noqa: E501
    StrainResponseModel,
    StrainWitnessControl,
    calculate_strain_witness_scan,
    calculate_synthetic_strain_response,
)
from ksdft2effmass.campaigns.model_adequacy.band_equivalence_locality.strain_schemas import (  # noqa: E501
    SyntheticStrainSchema,
    SyntheticStrainSchemaKind,
)
from ksdft2effmass.campaigns.model_adequacy.band_equivalence_locality.strain_serialization import (  # noqa: E501
    M0_RESULT_SCHEMA_ID,
    M1_RESULT_SCHEMA_ID,
    M2_RESULT_SCHEMA_ID,
    WITNESS_RESULT_SCHEMA_ID,
    SyntheticStrainResponseResultSerializer,
    SyntheticStrainResultSerializer,
    SyntheticStrainWitnessResultSerializer,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestSyntheticStrainArtifacts:
    """Establish canonical geometry, witness, and response result artifacts."""

    def test_m0_result__serializes_explicit_fields_and_validates(self) -> None:
        result = SyntheticStrainCalculator().execute(
            SyntheticStrainPath.RHOMBIC_2D,
            4,
            (0.0, 1.0),
            math.pi / 8.0,
            (1.0e-3, 1.0e-5),
        )

        artifact = SyntheticStrainResultSerializer().execute(result)
        content = artifact.canonical_bytes()
        document = json.loads(content)
        schema = SyntheticStrainSchema(SyntheticStrainSchemaKind.M0_RESULT)
        schema.validate(content)

        assert document["schema"] == M0_RESULT_SCHEMA_ID == schema.identity
        assert document["path"] == result.path.value
        assert document["tail_tolerances"] == list(result.tail_tolerances)
        assert document["points"][1]["metric"] == [
            list(row) for row in result.points[1].metric
        ]
        assert content == (
            json.dumps(
                document,
                allow_nan=False,
                separators=(",", ":"),
                sort_keys=True,
            )
            + "\n"
        ).encode("utf-8")

    def test_witness_result__serializes_control_and_validates(self) -> None:
        result = calculate_strain_witness_scan(
            SyntheticStrainPath.RHOMBIC_2D,
            StrainWitnessControl.GEOMETRY_ONLY,
            4,
            (0.0, 1.0),
            math.pi / 8.0,
        )

        artifact = SyntheticStrainWitnessResultSerializer().execute(result)
        document = json.loads(artifact.canonical_bytes())
        schema = SyntheticStrainSchema(SyntheticStrainSchemaKind.WITNESS_RESULT)
        schema.validate(artifact.canonical_bytes())

        assert document["schema"] == WITNESS_RESULT_SCHEMA_ID == schema.identity
        assert document["control"] == StrainWitnessControl.GEOMETRY_ONLY.value
        assert document["points"][1]["strain_fraction"] == 1.0

    @pytest.mark.parametrize(
        ("model", "beta", "kind", "identity"),
        (
            (
                StrainResponseModel.M1_FROZEN,
                0.0,
                SyntheticStrainSchemaKind.M1_RESULT,
                M1_RESULT_SCHEMA_ID,
            ),
            (
                StrainResponseModel.M2_RADIAL,
                1.0,
                SyntheticStrainSchemaKind.M2_RESULT,
                M2_RESULT_SCHEMA_ID,
            ),
        ),
    )
    def test_response_result__selects_model_schema_and_preserves_channels(
        self,
        model: StrainResponseModel,
        beta: float,
        kind: SyntheticStrainSchemaKind,
        identity: str,
    ) -> None:
        result = calculate_synthetic_strain_response(
            SyntheticStrainPath.RHOMBIC_2D,
            model,
            4,
            5,
            1.0 / 3.0,
            (0.0, 1.0),
            math.pi / 8.0,
            beta,
            (1.0e-3,),
        )

        artifact = SyntheticStrainResponseResultSerializer().execute(result)
        document = json.loads(artifact.canonical_bytes())
        schema = SyntheticStrainSchema(kind)
        schema.validate(artifact.canonical_bytes())

        assert document["schema"] == identity == schema.identity
        assert document["model"] == model.value
        assert document["radial_decay_beta"] == beta
        assert document["points"][1]["delta_offsite_power"] == (
            result.points[1].delta_offsite_power
        )
        assert document["points"][1]["aligned_strain_perturbation"] == {
            "maximum_band": result.points[1].aligned_strain_perturbation.maximum_band,
            "maximum_hamiltonian": (
                result.points[1].aligned_strain_perturbation.maximum_hamiltonian
            ),
            "rms_band": result.points[1].aligned_strain_perturbation.rms_band,
            "rms_hamiltonian": (
                result.points[1].aligned_strain_perturbation.rms_hamiltonian
            ),
        }

    def test_schema__rejects_unlisted_fields_and_cross_model_documents(self) -> None:
        result = calculate_synthetic_strain_response(
            SyntheticStrainPath.RHOMBIC_2D,
            StrainResponseModel.M1_FROZEN,
            4,
            5,
            1.0 / 3.0,
            (0.0,),
            math.pi / 8.0,
            0.0,
            (1.0e-3,),
        )
        content = SyntheticStrainResponseResultSerializer().execute(result)
        document = json.loads(content.canonical_bytes())
        document["undeclared"] = True
        changed = (
            json.dumps(document, allow_nan=False, separators=(",", ":"), sort_keys=True)
            + "\n"
        ).encode("utf-8")

        with pytest.raises(ValidationError):
            SyntheticStrainSchema(SyntheticStrainSchemaKind.M1_RESULT).validate(changed)
        with pytest.raises(ValidationError):
            SyntheticStrainSchema(SyntheticStrainSchemaKind.M2_RESULT).validate(
                content.canonical_bytes()
            )

    def test_schema_resources__are_canonical_and_writable(self, tmp_path: Path) -> None:
        for kind in SyntheticStrainSchemaKind:
            schema = SyntheticStrainSchema(kind)
            content = schema.canonical_bytes()
            decoded = json.loads(content)

            assert decoded["$id"] == schema.identity
            assert content == (
                json.dumps(
                    decoded,
                    allow_nan=False,
                    separators=(",", ":"),
                    sort_keys=True,
                )
                + "\n"
            ).encode("utf-8")
            assert schema.write_to(tmp_path / kind.value).read_bytes() == content
