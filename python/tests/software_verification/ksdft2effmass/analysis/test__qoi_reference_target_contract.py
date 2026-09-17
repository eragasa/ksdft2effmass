r"""Software verification of public scalar QoI and DFT reference target.

Evidence profile: routine

Bounded artifact scope: public scalar QoI and calculated DFT reference-target records.

Facet and represented meaning

The artifact defines calculator-independent scalar QoI meaning and correlates one
finite calculated DFT value to exact result, provenance, method, and artifact
identities.

Intrinsic and cross-object scope

The public ``ksdft2effmass.analysis`` record family is primary. Constructor
invariants, immutable field preservation, exact package exports, successful and failed
evaluation results, and separation of parent-model and numerical assessments are
included. Evaluator execution, comparison, serialization, calculator execution, and
LAMMPS contracts are excluded.

VVUQ and scientific exclusions

This is software verification using synthetic identities and values. It establishes
neither DFT convergence nor physical truth, numerical verification, scientific
validation, uncertainty quantification, calculator equivalence, or human acceptance.
"""

from dataclasses import FrozenInstanceError, replace

import ksdft2effmass.analysis as analysis
import pytest
from ksdft2effmass.analysis import (
    DftReferenceCalculationIdentity,
    DftReferenceCalculatorIdentity,
    DftReferenceMethodIdentity,
    DftScalarQuantityOfInterestReferenceTarget,
    NormalizedObservationRequirementIdentity,
    QuantityOfInterestCompleteness,
    QuantityOfInterestConventionIdentity,
    QuantityOfInterestEvaluationFailureCode,
    QuantityOfInterestEvaluatorIdentity,
    QuantityOfInterestIdentity,
    QuantityOfInterestReferenceAssessmentIdentity,
    QuantityOfInterestReferenceTargetIdentity,
    QuantityOfInterestStateSpaceIdentity,
    QuantityOfInterestSubjectIdentity,
    ScalarQuantityOfInterestDefinition,
    ScalarQuantityOfInterestEvaluationFailure,
    ScalarQuantityOfInterestValue,
)
from ksdft2effmass.workflows import (
    ArtifactManifestEntryIdentity,
    ArtifactManifestIdentity,
    ArtifactProducerProvenanceIdentity,
    ResultObjectIdentity,
)

pytestmark = pytest.mark.software_verification


class TestQoiReferenceTargetContract:
    """Own software evidence for the public QoI reference-target artifact."""

    @staticmethod
    def definition() -> ScalarQuantityOfInterestDefinition:
        """Return one complete synthetic scalar-energy QoI definition."""
        return ScalarQuantityOfInterestDefinition(
            identity=QuantityOfInterestIdentity("cohesive-energy-per-atom"),
            subject_identity=QuantityOfInterestSubjectIdentity("silicon.bulk.cell.1"),
            state_space_identity=QuantityOfInterestStateSpaceIdentity(
                "silicon.bulk.ground-state"
            ),
            convention_identity=QuantityOfInterestConventionIdentity(
                "cohesive-energy.reference.v1"
            ),
            evaluator_identity=QuantityOfInterestEvaluatorIdentity(
                "cohesive-energy-evaluator.v1"
            ),
            observation_requirement_identities=(
                NormalizedObservationRequirementIdentity("total-energy"),
                NormalizedObservationRequirementIdentity("isolated-atom-energies"),
                NormalizedObservationRequirementIdentity("atom-counts"),
            ),
            completeness=QuantityOfInterestCompleteness.COMPLETE,
            unit="electron_volt_per_atom",
        )

    @classmethod
    def evaluation(
        cls,
        *,
        value: float = -4.63,
        evaluator_identity: QuantityOfInterestEvaluatorIdentity | None = None,
    ) -> ScalarQuantityOfInterestValue:
        """Return one successful synthetic scalar QoI evaluation."""
        definition = cls.definition()
        if evaluator_identity is None:
            evaluator_identity = definition.evaluator_identity
        return ScalarQuantityOfInterestValue(
            identity=ResultObjectIdentity("evaluation.silicon.cohesive-energy.v1"),
            quantity=definition,
            source_observation_set_result_identity=ResultObjectIdentity(
                "observations.silicon.dft.v1"
            ),
            evaluator_identity=evaluator_identity,
            value=value,
        )

    @classmethod
    def target(
        cls,
        *,
        value: float = -4.63,
        entries: tuple[ArtifactManifestEntryIdentity, ...] | None = None,
    ) -> DftScalarQuantityOfInterestReferenceTarget:
        """Return one synthetic DFT-calculated reference target."""
        if entries is None:
            entries = (
                ArtifactManifestEntryIdentity("entry.qe-output"),
                ArtifactManifestEntryIdentity("entry.qe-schema"),
            )
        return DftScalarQuantityOfInterestReferenceTarget(
            identity=QuantityOfInterestReferenceTargetIdentity(
                "target.silicon.cohesive-energy.v1"
            ),
            evaluation=cls.evaluation(value=value),
            calculation_identity=DftReferenceCalculationIdentity(
                "calculation.silicon.reference.v1"
            ),
            calculator_identity=DftReferenceCalculatorIdentity("quantum-espresso.7.5"),
            method_identity=DftReferenceMethodIdentity(
                "dft-method.silicon.reference.v1"
            ),
            source_result_identity=ResultObjectIdentity("result.silicon.reference.v1"),
            source_provenance_identity=ArtifactProducerProvenanceIdentity(
                "provenance.silicon.reference.v1"
            ),
            source_artifact_manifest_identity=ArtifactManifestIdentity(
                "manifest.silicon.reference.v1"
            ),
            source_artifact_entry_identities=entries,
            parent_model_assessment_identity=QuantityOfInterestReferenceAssessmentIdentity(
                "assessment.parent-model.silicon.v1"
            ),
            numerical_error_assessment_identity=QuantityOfInterestReferenceAssessmentIdentity(
                "assessment.numerical.silicon.v1"
            ),
        )

    def test_fields__definition__preserves_scientific_identity_and_requirements(
        self,
    ) -> None:
        """Evidence ID: SV-QOI-REFERENCE-001

        Requirement: A scalar QoI definition preserves its subject, state space,
        conventions, evaluator, ordered observation requirements, completeness, and
        unit without embedding a reference target or calculator selection.

        Acceptance: Public fields equal the exact constructed values, the requirement
        order is retained, and the frozen record rejects assignment.
        """
        definition = self.definition()

        assert definition.identity == QuantityOfInterestIdentity(
            "cohesive-energy-per-atom"
        )
        assert definition.subject_identity == QuantityOfInterestSubjectIdentity(
            "silicon.bulk.cell.1"
        )
        assert definition.state_space_identity == QuantityOfInterestStateSpaceIdentity(
            "silicon.bulk.ground-state"
        )
        assert definition.convention_identity == QuantityOfInterestConventionIdentity(
            "cohesive-energy.reference.v1"
        )
        assert definition.evaluator_identity == QuantityOfInterestEvaluatorIdentity(
            "cohesive-energy-evaluator.v1"
        )
        assert tuple(
            item.value for item in definition.observation_requirement_identities
        ) == (
            "total-energy",
            "isolated-atom-energies",
            "atom-counts",
        )
        assert definition.completeness is QuantityOfInterestCompleteness.COMPLETE
        assert definition.unit == "electron_volt_per_atom"
        assert (
            replace(definition, state_space_identity=None).state_space_identity is None
        )
        with pytest.raises(FrozenInstanceError):
            definition.unit = "rydberg_per_atom"  # type: ignore[misc]

    def test_fields__reference_target__correlates_calculated_dft_evidence(
        self,
    ) -> None:
        """Evidence ID: SV-QOI-REFERENCE-002

        Requirement: A DFT scalar reference target correlates one finite value to its
        complete QoI definition and exact calculation, calculator, method, result,
        provenance, manifest, source-entry, parent-model, and numerical-assessment
        identities.

        Acceptance: Every public field equals the independently constructed value and
        parent-model and numerical assessments remain distinct.
        """
        target = self.target()

        assert target.evaluation == self.evaluation()
        assert target.quantity == self.definition()
        assert target.value == -4.63
        assert target.unit == "electron_volt_per_atom"
        assert target.calculation_identity == DftReferenceCalculationIdentity(
            "calculation.silicon.reference.v1"
        )
        assert target.calculator_identity == DftReferenceCalculatorIdentity(
            "quantum-espresso.7.5"
        )
        assert target.method_identity == DftReferenceMethodIdentity(
            "dft-method.silicon.reference.v1"
        )
        assert target.source_result_identity == ResultObjectIdentity(
            "result.silicon.reference.v1"
        )
        assert target.source_provenance_identity == ArtifactProducerProvenanceIdentity(
            "provenance.silicon.reference.v1"
        )
        assert target.source_artifact_manifest_identity == ArtifactManifestIdentity(
            "manifest.silicon.reference.v1"
        )
        assert tuple(
            item.value for item in target.source_artifact_entry_identities
        ) == (
            "entry.qe-output",
            "entry.qe-schema",
        )
        assert target.parent_model_assessment_identity != (
            target.numerical_error_assessment_identity
        )

    def test_construction__definition__rejects_incomplete_or_ambiguous_contracts(
        self,
    ) -> None:
        """Evidence ID: SV-QOI-REFERENCE-003

        Requirement: A scalar QoI requires a nonempty unique requirement tuple and a
        nonempty exact unit string.

        Acceptance: Empty requirements, duplicate requirements, a list in place of the
        tuple, and an empty unit each raise the documented exception category.
        """
        definition = self.definition()
        requirement = NormalizedObservationRequirementIdentity("total-energy")

        with pytest.raises(ValueError, match="must not be empty"):
            replace(definition, observation_requirement_identities=())
        with pytest.raises(ValueError, match="must be unique"):
            replace(
                definition,
                observation_requirement_identities=(requirement, requirement),
            )
        with pytest.raises(TypeError, match="must be a tuple"):
            replace(
                definition,
                observation_requirement_identities=[requirement],  # type: ignore[arg-type]
            )
        with pytest.raises(ValueError, match="unit must not be empty"):
            replace(definition, unit="")

    def test_construction__evaluation_and_target__reject_invalid_state(
        self,
    ) -> None:
        """Evidence ID: SV-QOI-REFERENCE-004

        Requirement: A scalar evaluation requires a finite built-in float and exact
        evaluator correlation, while a DFT reference target requires a successful
        evaluation and a nonempty, unique, lexically sorted source-entry tuple.

        Acceptance: Wrong numeric types, nonfinite values, evaluator mismatch, failed
        evaluation substitution, and malformed source-entry collections raise the
        documented exception category.
        """
        evaluation = self.evaluation()
        target = self.target()
        first = ArtifactManifestEntryIdentity("entry.a")
        second = ArtifactManifestEntryIdentity("entry.b")

        with pytest.raises(TypeError, match="float excluding bool and int"):
            replace(evaluation, value=True)
        with pytest.raises(TypeError, match="float excluding bool and int"):
            replace(evaluation, value=1)
        with pytest.raises(ValueError, match="value must be finite"):
            replace(evaluation, value=float("nan"))
        with pytest.raises(ValueError, match="value must be finite"):
            replace(evaluation, value=float("inf"))
        with pytest.raises(ValueError, match="must equal"):
            replace(
                evaluation,
                evaluator_identity=QuantityOfInterestEvaluatorIdentity("other.v1"),
            )
        failure = ScalarQuantityOfInterestEvaluationFailure(
            identity=ResultObjectIdentity("evaluation.failure.v1"),
            quantity=self.definition(),
            source_observation_set_result_identity=ResultObjectIdentity(
                "observations.silicon.dft.v1"
            ),
            evaluator_identity=self.definition().evaluator_identity,
            code=QuantityOfInterestEvaluationFailureCode.INCOMPLETE,
            detail="required total energy is absent",
        )
        with pytest.raises(TypeError, match="must be ScalarQuantityOfInterestValue"):
            replace(target, evaluation=failure)  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="must not be empty"):
            replace(target, source_artifact_entry_identities=())
        with pytest.raises(ValueError, match="unique and lexically sorted"):
            replace(target, source_artifact_entry_identities=(first, first))
        with pytest.raises(ValueError, match="unique and lexically sorted"):
            replace(target, source_artifact_entry_identities=(second, first))
        with pytest.raises(TypeError, match="must be a tuple"):
            replace(
                target,
                source_artifact_entry_identities=[first],  # type: ignore[arg-type]
            )

    def test_fields__evaluation_failure__retains_closed_failure_without_value(
        self,
    ) -> None:
        """Evidence ID: SV-QOI-REFERENCE-006

        Requirement: A failed scalar QoI evaluation retains exact quantity,
        observation-set, evaluator, failure-code, and diagnostic correlation and
        cannot be mistaken for a scalar value result.

        Acceptance: Public fields equal the exact constructed values, no ``value``
        attribute exists, and empty detail or evaluator mismatch is rejected.
        """
        definition = self.definition()
        failure = ScalarQuantityOfInterestEvaluationFailure(
            identity=ResultObjectIdentity("evaluation.failure.v1"),
            quantity=definition,
            source_observation_set_result_identity=ResultObjectIdentity(
                "observations.silicon.dft.v1"
            ),
            evaluator_identity=definition.evaluator_identity,
            code=QuantityOfInterestEvaluationFailureCode.INCOMPATIBLE,
            detail="energy-reference conventions differ",
        )

        assert failure.quantity == definition
        assert failure.code is QuantityOfInterestEvaluationFailureCode.INCOMPATIBLE
        assert failure.detail == "energy-reference conventions differ"
        assert not hasattr(failure, "value")
        with pytest.raises(ValueError, match="detail must not be empty"):
            replace(failure, detail="")
        with pytest.raises(ValueError, match="must equal"):
            replace(
                failure,
                evaluator_identity=QuantityOfInterestEvaluatorIdentity("other.v1"),
            )

    def test_public_api__analysis_package__exports_only_supported_qoi_contracts(
        self,
    ) -> None:
        """Evidence ID: SV-QOI-REFERENCE-005

        Requirement: The analysis package exports the supported scalar QoI and DFT
        reference-target records and explicit scalar codec while private comparison
        and parameter-study probes remain absent.

        Acceptance: ``analysis.__all__`` equals the exact supported inventory and the
        private probe names are not package attributes.
        """
        assert analysis.__all__ == [
            "DftReferenceCalculationIdentity",
            "DftReferenceCalculatorIdentity",
            "DftReferenceMethodIdentity",
            "DftScalarQuantityOfInterestReferenceTarget",
            "NormalizedObservationRequirementIdentity",
            "QuantityOfInterestCompleteness",
            "QuantityOfInterestConventionIdentity",
            "QuantityOfInterestEvaluationFailureCode",
            "QuantityOfInterestEvaluatorIdentity",
            "QuantityOfInterestIdentity",
            "QuantityOfInterestReferenceAssessmentIdentity",
            "QuantityOfInterestReferenceTargetIdentity",
            "QuantityOfInterestResultValueSerializer",
            "QuantityOfInterestStateSpaceIdentity",
            "QuantityOfInterestSubjectIdentity",
            "ScalarQuantityOfInterestDefinition",
            "ScalarQuantityOfInterestEvaluationFailure",
            "ScalarQuantityOfInterestEvaluationResult",
            "ScalarQuantityOfInterestValue",
        ]
        assert not hasattr(analysis, "ParameterStudyRevision")
        assert not hasattr(analysis, "FiniteSequenceParameterStudyRefiner")
