r"""Software verification of ``PlaneWaveParameterStudyCompiler``.

Evidence profile: routine

Bounded artifact scope: effect-free compilation of one plane-wave parameter study.

Facet and represented meaning

The module verifies exact QoI observation coverage, run-scoped Task composition,
dependencies, complete-binding reuse, and failure correlation.

Intrinsic and cross-object scope

``PlaneWaveParameterStudyCompiler`` is the sole system under test. Collaborating
records are fixed synthetic inputs; calculator execution and QoI evaluation are
excluded.

VVUQ and scientific exclusions

This is software verification using synthetic identities and values. It establishes
no physical convergence, backend equivalence, scientific validation, UQ, execution
authority, or human acceptance.
"""

from dataclasses import replace

import pytest

from ksdft2effmass.analysis._parameter_study import (
    NormalizedObservationRequirementIdentity,
    ParameterFactorKind,
    ParameterStudyCandidate,
    ParameterStudyCandidateIdentity,
    ParameterStudyIdentity,
    ParameterStudyKind,
    ParameterStudyRevision,
    ParameterStudyRevisionIdentity,
    ParameterStudySubjectIdentity,
    QuantityOfInterestCompleteness,
    QuantityOfInterestDefinition,
    QuantityOfInterestIdentity,
    ScalarQuantityOfInterestCriterion,
)
from ksdft2effmass.calculators.dft.pw import (
    PlaneWaveBackendBinding,
    PlaneWaveBackendBindingIdentity,
    PlaneWaveBackendIdentity,
    PlaneWaveBackendSupplement,
    PlaneWaveBackendSupplementIdentity,
    PlaneWaveEnergyCutoff,
    PlaneWaveEnergyUnit,
    PlaneWaveNativeConfigurationIdentity,
    PlaneWaveObservationRequirementIdentity,
    PlaneWavePhysicalModelIdentity,
    PlaneWaveSimulationSpecification,
    PlaneWaveSimulationSpecificationIdentity,
)
from ksdft2effmass.campaigns._plane_wave_study import (
    PlaneWaveObservationRequirementBinding,
    PlaneWaveParameterStudyCompiler,
    PlaneWaveQuantityOfInterestBinding,
    PlaneWaveStudyCandidateBinding,
    PlaneWaveStudyCompilationCompiled,
    PlaneWaveStudyCompilationFailure,
    PlaneWaveStudyCompilationFailureCode,
    PlaneWaveStudyCompilationIdentity,
    PlaneWaveStudyCompilationOutcome,
    PlaneWaveStudyCompilationRequest,
    PlaneWaveStudyCompilerIdentity,
    PlaneWaveStudySubjectBinding,
    PlaneWaveStudyTaskDependency,
)
from ksdft2effmass.workflows import (
    TaskDefinitionIdentity,
    TaskInstance,
    TaskInstanceIdentity,
    WorkflowIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = PlaneWaveParameterStudyCompiler


class TestPlaneWaveParameterStudyCompiler:
    """Own software evidence for effect-free parameter-study compilation."""

    @staticmethod
    def candidates(
        values: tuple[float, ...] = (30.0, 36.0, 42.0),
    ) -> tuple[ParameterStudyCandidate, ...]:
        """Return ordered fixed-subject synthetic cutoff candidates."""
        subject = ParameterStudySubjectIdentity("model.scalar.non-soc")
        return tuple(
            ParameterStudyCandidate(
                ParameterStudyCandidateIdentity(f"candidate.{index}.{value:g}"),
                subject,
                ParameterFactorKind.NUMERICAL,
                "wavefunction_cutoff",
                value,
                "rydberg",
            )
            for index, value in enumerate(values)
        )

    @classmethod
    def revision(
        cls,
        candidates: tuple[ParameterStudyCandidate, ...] | None = None,
    ) -> ParameterStudyRevision:
        """Return one valid numerical-convergence revision."""
        return ParameterStudyRevision(
            ParameterStudyRevisionIdentity("cutoff-study.revision.1"),
            ParameterStudyIdentity("cutoff-study"),
            ParameterStudyKind.NUMERICAL_CONVERGENCE,
            candidates or cls.candidates(),
            (
                ScalarQuantityOfInterestCriterion(
                    QuantityOfInterestIdentity("total-energy-per-atom"),
                    "rydberg_per_atom",
                    0.25,
                ),
            ),
            None,
        )

    @staticmethod
    def qoi_definition() -> QuantityOfInterestDefinition:
        """Return the total-energy QoI and normalized requirement."""
        return QuantityOfInterestDefinition(
            QuantityOfInterestIdentity("total-energy-per-atom"),
            (NormalizedObservationRequirementIdentity("normalized.total-energy"),),
            QuantityOfInterestCompleteness.COMPLETE,
        )

    @staticmethod
    def backend_binding(
        candidate: ParameterStudyCandidate,
        physical_model: PlaneWavePhysicalModelIdentity | None = None,
        binding_suffix: str | None = None,
        observations: tuple[PlaneWaveObservationRequirementIdentity, ...] | None = None,
    ) -> PlaneWaveBackendBinding:
        """Return one exact synthetic backend binding for a candidate."""
        suffix = binding_suffix or candidate.identity.value
        return PlaneWaveBackendBinding(
            PlaneWaveBackendBindingIdentity(f"binding.{suffix}"),
            PlaneWaveSimulationSpecification(
                PlaneWaveSimulationSpecificationIdentity(f"spec.{suffix}"),
                physical_model
                or PlaneWavePhysicalModelIdentity("pw-model.scalar.non-soc"),
                PlaneWaveEnergyCutoff(candidate.value, PlaneWaveEnergyUnit.RYDBERG),
                observations
                or (
                    PlaneWaveObservationRequirementIdentity("calculator.total-energy"),
                ),
            ),
            PlaneWaveBackendSupplement(
                PlaneWaveBackendSupplementIdentity(f"supplement.{suffix}"),
                PlaneWaveBackendIdentity("quantum-espresso.7.5"),
                PlaneWaveNativeConfigurationIdentity(f"native-config:{suffix}"),
            ),
        )

    @staticmethod
    def task_instance(
        candidate: ParameterStudyCandidate,
        suffix: str | None = None,
    ) -> TaskInstance:
        """Return one run-scoped Task instance for a candidate."""
        selected = suffix or candidate.identity.value
        return TaskInstance(
            TaskInstanceIdentity(f"task-instance.{selected}"),
            TaskDefinitionIdentity("plane-wave.scf.v1"),
            None,
        )

    @classmethod
    def quantity_binding(cls) -> PlaneWaveQuantityOfInterestBinding:
        """Return the explicit analysis-to-calculator observation mapping."""
        return PlaneWaveQuantityOfInterestBinding(
            cls.qoi_definition(),
            (
                PlaneWaveObservationRequirementBinding(
                    NormalizedObservationRequirementIdentity("normalized.total-energy"),
                    PlaneWaveObservationRequirementIdentity("calculator.total-energy"),
                ),
            ),
        )

    @classmethod
    def request(
        cls,
        revision: ParameterStudyRevision,
        candidate_bindings: tuple[PlaneWaveStudyCandidateBinding, ...] | None = None,
        quantity_bindings: tuple[PlaneWaveQuantityOfInterestBinding, ...] | None = None,
        dependencies: tuple[PlaneWaveStudyTaskDependency, ...] = (),
    ) -> PlaneWaveStudyCompilationRequest:
        """Return one complete effect-free compilation request."""
        physical_model = PlaneWavePhysicalModelIdentity("pw-model.scalar.non-soc")
        bindings = (
            candidate_bindings
            if candidate_bindings is not None
            else tuple(
                PlaneWaveStudyCandidateBinding(
                    candidate,
                    cls.backend_binding(candidate, physical_model),
                    cls.task_instance(candidate),
                )
                for candidate in revision.candidates
            )
        )
        return PlaneWaveStudyCompilationRequest(
            PlaneWaveStudyCompilationIdentity("compilation.cutoff-study.revision.1"),
            PlaneWaveStudyCompilerIdentity("plane-wave-study-compiler.v1"),
            WorkflowIdentity("workflow.cutoff-study.revision.1"),
            revision,
            PlaneWaveStudySubjectBinding(
                revision.candidates[0].subject_identity, physical_model
            ),
            (
                quantity_bindings
                if quantity_bindings is not None
                else (cls.quantity_binding(),)
            ),
            bindings,
            dependencies,
        )

    @staticmethod
    def compiler() -> PlaneWaveParameterStudyCompiler:
        """Return the exact compiler implementation under test."""
        return SUT(PlaneWaveStudyCompilerIdentity("plane-wave-study-compiler.v1"))

    def test_method__execute__requires_qoi_observation_coverage(self) -> None:
        """Evidence ID: SV-PLANE-WAVE-STUDY-008

        Requirement: Compilation correlates every criterion to a typed QoI,
        normalized-to-calculator observation mapping, and requested observations.

        Acceptance: A complete mapping compiles; missing observations, QoI bindings,
        and analysis mappings return exact closed failures.
        """
        revision = self.revision()
        compiler = self.compiler()
        compiled = compiler.execute(self.request(revision))
        assert type(compiled) is PlaneWaveStudyCompilationCompiled
        assert compiled.study.request.revision is revision

        source = self.request(revision)
        missing_bindings = tuple(
            replace(
                item,
                backend_binding=self.backend_binding(
                    item.candidate,
                    item.backend_binding.specification.physical_model_identity,
                    observations=(
                        PlaneWaveObservationRequirementIdentity("calculator.stress"),
                    ),
                ),
            )
            for item in source.candidate_bindings
        )
        missing = compiler.execute(self.request(revision, missing_bindings))
        assert type(missing) is PlaneWaveStudyCompilationFailure
        assert missing.outcome is PlaneWaveStudyCompilationOutcome.UNSUPPORTED
        assert missing.code is (
            PlaneWaveStudyCompilationFailureCode.REQUIRED_OBSERVATION_MISSING
        )

        no_qoi = compiler.execute(self.request(revision, quantity_bindings=()))
        assert type(no_qoi) is PlaneWaveStudyCompilationFailure
        assert no_qoi.code is (
            PlaneWaveStudyCompilationFailureCode.QOI_BINDING_COVERAGE_MISMATCH
        )

        wrong_mapping = PlaneWaveQuantityOfInterestBinding(
            self.qoi_definition(),
            (
                PlaneWaveObservationRequirementBinding(
                    NormalizedObservationRequirementIdentity("normalized.stress"),
                    PlaneWaveObservationRequirementIdentity("calculator.total-energy"),
                ),
            ),
        )
        mismatch = compiler.execute(
            self.request(revision, quantity_bindings=(wrong_mapping,))
        )
        assert type(mismatch) is PlaneWaveStudyCompilationFailure
        assert mismatch.code is (
            PlaneWaveStudyCompilationFailureCode.QOI_OBSERVATION_MAPPING_MISMATCH
        )

    def test_method__execute__builds_instances_dependencies_and_exact_reuse(
        self,
    ) -> None:
        """Evidence ID: SV-PLANE-WAVE-STUDY-009

        Requirement: A compiled study retains full request provenance, run-scoped
        Task instances, explicit dependencies, and exact complete-binding reuse.

        Acceptance: Exact composition and dependencies are retained; equal bindings
        reuse one Task, while invalid Task sharing and identity conflicts fail closed.
        """
        revision = self.revision()
        request = self.request(revision)
        first_task = request.candidate_bindings[0].task_instance
        second_task = request.candidate_bindings[1].task_instance
        dependency = PlaneWaveStudyTaskDependency(
            first_task.identity, second_task.identity
        )
        compiled = self.compiler().execute(
            replace(request, task_dependencies=(dependency,))
        )
        assert type(compiled) is PlaneWaveStudyCompilationCompiled
        assert compiled.study.request.task_dependencies == (dependency,)
        assert compiled.study.workflow_composition.task_instances == tuple(
            item.task_instance for item in request.candidate_bindings
        )
        assert compiled.study.reuse == ()

        duplicate_candidates = self.candidates(values=(30.0, 30.0))
        duplicate_revision = self.revision(duplicate_candidates)
        shared_backend = self.backend_binding(duplicate_candidates[0])
        shared_task = self.task_instance(duplicate_candidates[0], "shared")
        reuse_bindings = (
            PlaneWaveStudyCandidateBinding(
                duplicate_candidates[0], shared_backend, shared_task
            ),
            PlaneWaveStudyCandidateBinding(
                duplicate_candidates[1], shared_backend, shared_task
            ),
        )
        reused = self.compiler().execute(
            self.request(duplicate_revision, reuse_bindings)
        )
        assert type(reused) is PlaneWaveStudyCompilationCompiled
        assert reused.study.workflow_composition.task_instances == (shared_task,)
        assert reused.study.reuse[0].candidate_identity == (
            duplicate_candidates[1].identity
        )
        assert reused.study.reuse[0].canonical_candidate_identity == (
            duplicate_candidates[0].identity
        )

        distinct_bindings = (
            request.candidate_bindings[0],
            replace(request.candidate_bindings[1], task_instance=first_task),
            request.candidate_bindings[2],
        )
        invalid = self.compiler().execute(self.request(revision, distinct_bindings))
        assert type(invalid) is PlaneWaveStudyCompilationFailure
        assert invalid.code is (
            PlaneWaveStudyCompilationFailureCode.DISTINCT_BINDINGS_SHARE_TASK
        )

        conflicting_task = TaskInstance(
            first_task.identity,
            TaskDefinitionIdentity("different-task-definition.v1"),
            None,
        )
        task_identity_conflict = self.compiler().execute(
            self.request(
                revision,
                (
                    request.candidate_bindings[0],
                    replace(
                        request.candidate_bindings[1],
                        task_instance=conflicting_task,
                    ),
                    request.candidate_bindings[2],
                ),
            )
        )
        assert type(task_identity_conflict) is PlaneWaveStudyCompilationFailure
        assert task_identity_conflict.code is (
            PlaneWaveStudyCompilationFailureCode.TASK_INSTANCE_IDENTITY_CONFLICT
        )

    def test_method__execute_failure__retains_exact_correlation(self) -> None:
        """Evidence ID: SV-PLANE-WAVE-STUDY-010

        Requirement: A failure retains the exact request and executed compiler;
        nominal binding identity cannot authorize reuse of unequal binding content.

        Acceptance: Unequal bindings sharing an identity return a correlated conflict;
        a different compiler returns a correlated compiler-identity mismatch.
        """
        revision = self.revision()
        request = self.request(revision)
        first = request.candidate_bindings[0]
        second = request.candidate_bindings[1]
        conflicting = (
            first,
            replace(
                second,
                backend_binding=replace(
                    second.backend_binding,
                    identity=first.backend_binding.identity,
                ),
                task_instance=first.task_instance,
            ),
            request.candidate_bindings[2],
        )
        request = self.request(revision, conflicting)
        result = self.compiler().execute(request)
        assert type(result) is PlaneWaveStudyCompilationFailure
        assert result.request is request
        assert result.executed_compiler_identity == request.compiler_identity
        assert result.outcome is PlaneWaveStudyCompilationOutcome.INVALID
        assert result.code is (
            PlaneWaveStudyCompilationFailureCode.BACKEND_BINDING_IDENTITY_CONFLICT
        )

        wrong_compiler = SUT(
            PlaneWaveStudyCompilerIdentity("plane-wave-study-compiler.v2")
        ).execute(request)
        assert type(wrong_compiler) is PlaneWaveStudyCompilationFailure
        assert wrong_compiler.request is request
        assert wrong_compiler.executed_compiler_identity == (
            PlaneWaveStudyCompilerIdentity("plane-wave-study-compiler.v2")
        )
        assert wrong_compiler.executed_compiler_identity != (
            wrong_compiler.request.compiler_identity
        )
        assert wrong_compiler.code is (
            PlaneWaveStudyCompilationFailureCode.COMPILER_IDENTITY_MISMATCH
        )
