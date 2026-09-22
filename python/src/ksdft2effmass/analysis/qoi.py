"""Calculator-independent scalar QoI and DFT reference-target records.

This module represents the scientific identity and observation requirements of one
scalar quantity of interest (QoI) separately from a calculated density-functional
theory (DFT) reference value.  A QoI definition identifies what is measured; a DFT
reference target records one finite calculated value and the exact represented source
that produced it.

The records are immutable and perform no calculator execution, native parsing, unit
conversion, comparison, tolerance evaluation, fitting, scientific acceptance, or
serialization.  A DFT reference target is a calculated result with separately cited
parent-model and numerical-error assessments when those assessments exist.  It is not
an assertion of physical truth or scientific validation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum

from ksdft2effmass.workflows import (
    ArtifactManifestEntryIdentity,
    ArtifactManifestIdentity,
    ArtifactProducerProvenanceIdentity,
    ResultObjectIdentity,
)


@dataclass(frozen=True, slots=True)
class QuantityOfInterestIdentity:
    """Nominal identity of one calculator-independent quantity of interest.

    Parameters
    ----------
    value
        Nonempty owner-local lexical identity.  It is not a display label, unit,
        evaluator identity, or wire-format identifier.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact built-in string identity."""
        if type(self.value) is not str:
            raise TypeError("quantity-of-interest identity value must be a string")
        if not self.value:
            raise ValueError("quantity-of-interest identity value must not be empty")


@dataclass(frozen=True, slots=True)
class QuantityOfInterestSubjectIdentity:
    """Nominal identity of the modeled subject to which a QoI applies.

    Parameters
    ----------
    value
        Nonempty owner-local identity of the structure, state, comparison subject, or
        other represented scientific subject.  Equality does not itself establish
        physical equivalence.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact built-in string identity."""
        if type(self.value) is not str:
            raise TypeError("quantity-of-interest subject identity must be a string")
        if not self.value:
            raise ValueError("quantity-of-interest subject identity must not be empty")


@dataclass(frozen=True, slots=True)
class QuantityOfInterestStateSpaceIdentity:
    """Nominal identity of the state space in which a QoI is interpreted.

    Parameters
    ----------
    value
        Nonempty owner-local identity.  The referenced scientific specification owns
        basis, spin, geometry, and other state-space meaning.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact built-in string identity."""
        if type(self.value) is not str:
            raise TypeError(
                "quantity-of-interest state-space identity must be a string"
            )
        if not self.value:
            raise ValueError(
                "quantity-of-interest state-space identity must not be empty"
            )


@dataclass(frozen=True, slots=True)
class QuantityOfInterestConventionIdentity:
    """Nominal identity of the conventions required to interpret a QoI.

    Parameters
    ----------
    value
        Nonempty owner-local identity of an exact convention set.  Applicable energy
        zero, normalization, basis, gauge, geometry, stress-sign, and ordering rules
        belong to the referenced specification rather than this lexical identity.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact built-in string identity."""
        if type(self.value) is not str:
            raise TypeError("quantity-of-interest convention identity must be a string")
        if not self.value:
            raise ValueError(
                "quantity-of-interest convention identity must not be empty"
            )


@dataclass(frozen=True, slots=True)
class QuantityOfInterestEvaluatorIdentity:
    """Nominal identity and version of a deterministic QoI evaluator.

    Parameters
    ----------
    value
        Nonempty owner-local identity.  Construction does not assert that an evaluator
        implementation exists or has been numerically verified.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact built-in string identity."""
        if type(self.value) is not str:
            raise TypeError("quantity-of-interest evaluator identity must be a string")
        if not self.value:
            raise ValueError(
                "quantity-of-interest evaluator identity must not be empty"
            )


@dataclass(frozen=True, slots=True)
class NormalizedObservationRequirementIdentity:
    """Nominal identity of one normalized observation required by a QoI.

    Parameters
    ----------
    value
        Nonempty owner-local identity.  The Workflow observation contract owns the
        normalized representation and provenance to which the identity refers.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact built-in string identity."""
        if type(self.value) is not str:
            raise TypeError("observation-requirement identity value must be a string")
        if not self.value:
            raise ValueError("observation-requirement identity value must not be empty")


@dataclass(frozen=True, slots=True)
class QuantityOfInterestReferenceTargetIdentity:
    """Nominal identity of one immutable QoI reference target.

    Parameters
    ----------
    value
        Nonempty owner-local identity distinct from the QoI, calculation, result, and
        artifact identities correlated by the target.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact built-in string identity."""
        if type(self.value) is not str:
            raise TypeError("reference-target identity value must be a string")
        if not self.value:
            raise ValueError("reference-target identity value must not be empty")


@dataclass(frozen=True, slots=True)
class DftReferenceCalculationIdentity:
    """Nominal identity of the DFT calculation used as a reference source.

    Parameters
    ----------
    value
        Nonempty owner-local calculation identity.  It is not a claim of convergence,
        successful execution, or scientific adequacy.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact built-in string identity."""
        if type(self.value) is not str:
            raise TypeError("DFT reference-calculation identity must be a string")
        if not self.value:
            raise ValueError("DFT reference-calculation identity must not be empty")


@dataclass(frozen=True, slots=True)
class DftReferenceCalculatorIdentity:
    """Nominal identity and version of the DFT calculator implementation.

    Parameters
    ----------
    value
        Nonempty owner-local identity.  Equal labels do not establish equivalence of
        executables, builds, methods, or numerical results.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact built-in string identity."""
        if type(self.value) is not str:
            raise TypeError("DFT calculator identity must be a string")
        if not self.value:
            raise ValueError("DFT calculator identity must not be empty")


@dataclass(frozen=True, slots=True)
class DftReferenceMethodIdentity:
    """Nominal identity of the complete represented DFT method and settings.

    Parameters
    ----------
    value
        Nonempty owner-local identity of an exact method specification.  The
        referenced specification, not this string, owns pseudopotential,
        exchange-correlation, spin, relativistic, cutoff, mesh, and solver meaning.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact built-in string identity."""
        if type(self.value) is not str:
            raise TypeError("DFT method identity must be a string")
        if not self.value:
            raise ValueError("DFT method identity must not be empty")


@dataclass(frozen=True, slots=True)
class QuantityOfInterestReferenceAssessmentIdentity:
    """Nominal identity of one separately retained reference-error assessment.

    Parameters
    ----------
    value
        Nonempty owner-local identity.  The referenced assessment owns its metric,
        evidence, assumptions, and limitations.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact built-in string identity."""
        if type(self.value) is not str:
            raise TypeError("reference-assessment identity must be a string")
        if not self.value:
            raise ValueError("reference-assessment identity must not be empty")


class QuantityOfInterestCompleteness(StrEnum):
    """Closed completeness required from normalized observations.

    Attributes
    ----------
    COMPLETE
        Every observation declared by the QoI definition is required.
    DECLARED_SUBSET
        The definition explicitly permits an evaluator-owned declared subset.  This
        value does not allow a caller to omit observations silently.
    """

    COMPLETE = "complete"
    DECLARED_SUBSET = "declared_subset"


class QuantityOfInterestEvaluationFailureCode(StrEnum):
    """Closed failure code for a scalar QoI evaluation attempt.

    Attributes
    ----------
    UNAVAILABLE
        One or more required normalized observations are represented as unavailable.
    INCOMPLETE
        The supplied normalized observation set omits required observations.
    INCOMPATIBLE
        Supplied observations do not satisfy the subject, unit, convention, state,
        or other compatibility requirements of the QoI definition.
    INVALID
        The evaluation request is intrinsically malformed.
    ERROR
        The selected evaluator failed without producing a scalar value.
    """

    UNAVAILABLE = "unavailable"
    INCOMPLETE = "incomplete"
    INCOMPATIBLE = "incompatible"
    INVALID = "invalid"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class ScalarQuantityOfInterestDefinition:
    """Calculator-independent definition of one scalar quantity of interest.

    Parameters
    ----------
    identity
        Exact nominal QoI identity.
    subject_identity
        Exact modeled-subject identity.
    state_space_identity
        Optional exact state-space identity required for interpretation.  ``None``
        means the scalar contract does not require a shared represented state space;
        it does not make unlike states compatible.
    convention_identity
        Exact convention-set identity, including every applicable normalization,
        energy-reference, basis, gauge, geometry, spin, and ordering convention.
    evaluator_identity
        Exact identity and version of the deterministic evaluator intended to produce
        the scalar value.
    observation_requirement_identities
        Nonempty immutable tuple of unique normalized-observation requirements.  The
        declared order is retained and may be significant to the evaluator contract.
    completeness
        Closed completeness rule applied to the declared requirements.
    unit
        Nonempty exact unit string selected by the owning scientific specification.
        Construction performs no conversion or dimensional analysis.

    Notes
    -----
    The definition contains no reference value, tolerance, weight, loss, calculator
    selection, native input, execution authority, or acceptance decision.
    """

    identity: QuantityOfInterestIdentity
    subject_identity: QuantityOfInterestSubjectIdentity
    state_space_identity: QuantityOfInterestStateSpaceIdentity | None
    convention_identity: QuantityOfInterestConventionIdentity
    evaluator_identity: QuantityOfInterestEvaluatorIdentity
    observation_requirement_identities: tuple[
        NormalizedObservationRequirementIdentity, ...
    ]
    completeness: QuantityOfInterestCompleteness
    unit: str

    def __post_init__(self) -> None:
        """Validate exact nominal fields and immutable requirement closure."""
        if type(self.identity) is not QuantityOfInterestIdentity:
            raise TypeError("identity must be QuantityOfInterestIdentity")
        if type(self.subject_identity) is not QuantityOfInterestSubjectIdentity:
            raise TypeError(
                "subject_identity must be QuantityOfInterestSubjectIdentity"
            )
        if (
            self.state_space_identity is not None
            and type(self.state_space_identity)
            is not QuantityOfInterestStateSpaceIdentity
        ):
            raise TypeError(
                "state_space_identity must be "
                "QuantityOfInterestStateSpaceIdentity or None"
            )
        if type(self.convention_identity) is not QuantityOfInterestConventionIdentity:
            raise TypeError(
                "convention_identity must be QuantityOfInterestConventionIdentity"
            )
        if type(self.evaluator_identity) is not QuantityOfInterestEvaluatorIdentity:
            raise TypeError(
                "evaluator_identity must be QuantityOfInterestEvaluatorIdentity"
            )
        requirements = self.observation_requirement_identities
        if type(requirements) is not tuple or any(
            type(item) is not NormalizedObservationRequirementIdentity
            for item in requirements
        ):
            raise TypeError(
                "observation_requirement_identities must be a tuple of "
                "NormalizedObservationRequirementIdentity"
            )
        if not requirements:
            raise ValueError("observation_requirement_identities must not be empty")
        if len(set(requirements)) != len(requirements):
            raise ValueError("observation requirement identities must be unique")
        if type(self.completeness) is not QuantityOfInterestCompleteness:
            raise TypeError("completeness must be QuantityOfInterestCompleteness")
        if type(self.unit) is not str:
            raise TypeError("unit must be a string")
        if not self.unit:
            raise ValueError("unit must not be empty")


@dataclass(frozen=True, slots=True)
class ScalarQuantityOfInterestValue:
    """Successful scalar QoI evaluation from one normalized observation set.

    Parameters
    ----------
    identity
        Exact immutable workflow-facing identity of this evaluation result.
    quantity
        Complete scalar QoI definition that interprets ``value``.
    source_observation_set_result_identity
        Exact :class:`~ksdft2effmass.workflows.ResultObjectIdentity` of the normalized
        observation set consumed by the evaluator.  This record does not assert that
        the source result is present or compatible outside the retained evaluation
        operation.
    evaluator_identity
        Exact evaluator identity used for the operation.  It must equal
        ``quantity.evaluator_identity``.
    value
        Finite built-in floating-point value in ``quantity.unit``.  Integers,
        Booleans, numeric strings, NaN, and infinities are rejected.

    Notes
    -----
    This ResultObject records a successful software operation.  It performs no unit
    conversion or comparison and establishes no numerical convergence, scientific
    validation, uncertainty quantification, or acceptance.
    """

    identity: ResultObjectIdentity
    quantity: ScalarQuantityOfInterestDefinition
    source_observation_set_result_identity: ResultObjectIdentity
    evaluator_identity: QuantityOfInterestEvaluatorIdentity
    value: float

    def __post_init__(self) -> None:
        """Validate exact result correlation and finite scalar representation."""
        if type(self.identity) is not ResultObjectIdentity:
            raise TypeError("identity must be ResultObjectIdentity")
        if type(self.quantity) is not ScalarQuantityOfInterestDefinition:
            raise TypeError("quantity must be ScalarQuantityOfInterestDefinition")
        if (
            type(self.source_observation_set_result_identity)
            is not ResultObjectIdentity
        ):
            raise TypeError(
                "source_observation_set_result_identity must be ResultObjectIdentity"
            )
        if type(self.evaluator_identity) is not QuantityOfInterestEvaluatorIdentity:
            raise TypeError(
                "evaluator_identity must be QuantityOfInterestEvaluatorIdentity"
            )
        if self.evaluator_identity != self.quantity.evaluator_identity:
            raise ValueError(
                "evaluator_identity must equal quantity.evaluator_identity"
            )
        if type(self.value) is not float:
            raise TypeError("value must be a float excluding bool and int")
        if not math.isfinite(self.value):
            raise ValueError("value must be finite")

    @property
    def unit(self) -> str:
        """Return the exact output unit declared by the QoI definition."""
        return self.quantity.unit


@dataclass(frozen=True, slots=True)
class ScalarQuantityOfInterestEvaluationFailure:
    """Closed failure from one scalar QoI evaluation attempt.

    Parameters
    ----------
    identity
        Exact immutable workflow-facing identity of this failure result.
    quantity
        Complete scalar QoI definition that the operation attempted to evaluate.
    source_observation_set_result_identity
        Exact workflow-facing identity of the supplied normalized observation set.
    evaluator_identity
        Exact evaluator identity used for the attempt.  It must equal
        ``quantity.evaluator_identity``.
    code
        Closed unavailable, incomplete, incompatible, invalid, or error category.
    detail
        Nonempty diagnostic text.  It is not a scientific conclusion or acceptance
        decision and must not contain credentials or restricted data.

    Notes
    -----
    A failure contains no scalar value and must not be converted into zero, NaN, a
    default, or a successful reference target.
    """

    identity: ResultObjectIdentity
    quantity: ScalarQuantityOfInterestDefinition
    source_observation_set_result_identity: ResultObjectIdentity
    evaluator_identity: QuantityOfInterestEvaluatorIdentity
    code: QuantityOfInterestEvaluationFailureCode
    detail: str

    def __post_init__(self) -> None:
        """Validate exact failure correlation and closed failure representation."""
        if type(self.identity) is not ResultObjectIdentity:
            raise TypeError("identity must be ResultObjectIdentity")
        if type(self.quantity) is not ScalarQuantityOfInterestDefinition:
            raise TypeError("quantity must be ScalarQuantityOfInterestDefinition")
        if (
            type(self.source_observation_set_result_identity)
            is not ResultObjectIdentity
        ):
            raise TypeError(
                "source_observation_set_result_identity must be ResultObjectIdentity"
            )
        if type(self.evaluator_identity) is not QuantityOfInterestEvaluatorIdentity:
            raise TypeError(
                "evaluator_identity must be QuantityOfInterestEvaluatorIdentity"
            )
        if self.evaluator_identity != self.quantity.evaluator_identity:
            raise ValueError(
                "evaluator_identity must equal quantity.evaluator_identity"
            )
        if type(self.code) is not QuantityOfInterestEvaluationFailureCode:
            raise TypeError("code must be QuantityOfInterestEvaluationFailureCode")
        if type(self.detail) is not str:
            raise TypeError("detail must be a string")
        if not self.detail:
            raise ValueError("detail must not be empty")


type ScalarQuantityOfInterestEvaluationResult = (
    ScalarQuantityOfInterestValue | ScalarQuantityOfInterestEvaluationFailure
)


@dataclass(frozen=True, slots=True)
class DftScalarQuantityOfInterestReferenceTarget:
    """One scalar QoI reference target evaluated from an identified DFT calculation.

    Parameters
    ----------
    identity
        Exact immutable reference-target identity.
    evaluation
        Successful scalar QoI evaluation produced from an identified normalized
        observation-set result.  Its complete QoI definition and finite value define
        the target's ``quantity`` and ``value`` properties.
    calculation_identity
        Exact identity of the source DFT calculation.
    calculator_identity
        Exact calculator implementation and version identity.
    method_identity
        Exact represented physical-model and numerical-method identity.
    source_result_identity
        Exact immutable ResultObject identity from which the target was evaluated.
        Imported retained results use their actual represented result identity rather
        than fabricated Workflow lineage.
    source_provenance_identity
        Exact closed producer-provenance record identity.
    source_artifact_manifest_identity
        Exact immutable artifact-manifest revision containing source evidence.
    source_artifact_entry_identities
        Nonempty tuple of exact source manifest-entry identities, unique and sorted
        lexically by identity value for deterministic representation.
    parent_model_assessment_identity
        Optional identity of a separately retained parent-model limitation or error
        assessment.  ``None`` means no such assessment is represented, not zero error.
    numerical_error_assessment_identity
        Optional identity of a separately retained numerical or discretization error
        assessment.  ``None`` means no such assessment is represented, not zero error.

    Notes
    -----
    This record labels ``value`` as a calculated DFT reference.  It does not establish
    convergence, physical truth, calculator equivalence, model-reduction error,
    scientific validation, uncertainty quantification, fitting policy, or human
    acceptance.  Parent-model and numerical assessments remain separate by contract.
    """

    identity: QuantityOfInterestReferenceTargetIdentity
    evaluation: ScalarQuantityOfInterestValue
    calculation_identity: DftReferenceCalculationIdentity
    calculator_identity: DftReferenceCalculatorIdentity
    method_identity: DftReferenceMethodIdentity
    source_result_identity: ResultObjectIdentity
    source_provenance_identity: ArtifactProducerProvenanceIdentity
    source_artifact_manifest_identity: ArtifactManifestIdentity
    source_artifact_entry_identities: tuple[ArtifactManifestEntryIdentity, ...]
    parent_model_assessment_identity: (
        QuantityOfInterestReferenceAssessmentIdentity | None
    )
    numerical_error_assessment_identity: (
        QuantityOfInterestReferenceAssessmentIdentity | None
    )

    def __post_init__(self) -> None:
        """Validate exact correlation, scalar, artifact, and assessment fields."""
        if type(self.identity) is not QuantityOfInterestReferenceTargetIdentity:
            raise TypeError(
                "identity must be QuantityOfInterestReferenceTargetIdentity"
            )
        if type(self.evaluation) is not ScalarQuantityOfInterestValue:
            raise TypeError("evaluation must be ScalarQuantityOfInterestValue")
        if type(self.calculation_identity) is not DftReferenceCalculationIdentity:
            raise TypeError(
                "calculation_identity must be DftReferenceCalculationIdentity"
            )
        if type(self.calculator_identity) is not DftReferenceCalculatorIdentity:
            raise TypeError(
                "calculator_identity must be DftReferenceCalculatorIdentity"
            )
        if type(self.method_identity) is not DftReferenceMethodIdentity:
            raise TypeError("method_identity must be DftReferenceMethodIdentity")
        if type(self.source_result_identity) is not ResultObjectIdentity:
            raise TypeError("source_result_identity must be ResultObjectIdentity")
        if (
            type(self.source_provenance_identity)
            is not ArtifactProducerProvenanceIdentity
        ):
            raise TypeError(
                "source_provenance_identity must be ArtifactProducerProvenanceIdentity"
            )
        if type(self.source_artifact_manifest_identity) is not ArtifactManifestIdentity:
            raise TypeError(
                "source_artifact_manifest_identity must be ArtifactManifestIdentity"
            )
        entries = self.source_artifact_entry_identities
        if type(entries) is not tuple or any(
            type(item) is not ArtifactManifestEntryIdentity for item in entries
        ):
            raise TypeError(
                "source_artifact_entry_identities must be a tuple of "
                "ArtifactManifestEntryIdentity"
            )
        if not entries:
            raise ValueError("source_artifact_entry_identities must not be empty")
        entry_values = tuple(item.value for item in entries)
        if entry_values != tuple(sorted(entry_values)) or len(set(entries)) != len(
            entries
        ):
            raise ValueError(
                "source_artifact_entry_identities must be unique and lexically sorted"
            )
        optional_assessments = (
            (
                "parent_model_assessment_identity",
                self.parent_model_assessment_identity,
            ),
            (
                "numerical_error_assessment_identity",
                self.numerical_error_assessment_identity,
            ),
        )
        for field_name, assessment in optional_assessments:
            if assessment is not None and type(assessment) is not (
                QuantityOfInterestReferenceAssessmentIdentity
            ):
                raise TypeError(
                    f"{field_name} must be "
                    "QuantityOfInterestReferenceAssessmentIdentity or None"
                )

    @property
    def quantity(self) -> ScalarQuantityOfInterestDefinition:
        """Return the exact QoI definition carried by the successful evaluation."""
        return self.evaluation.quantity

    @property
    def value(self) -> float:
        """Return the finite calculated value carried by the successful evaluation."""
        return self.evaluation.value

    @property
    def unit(self) -> str:
        """Return the exact unit declared by the evaluated QoI definition."""
        return self.evaluation.unit
