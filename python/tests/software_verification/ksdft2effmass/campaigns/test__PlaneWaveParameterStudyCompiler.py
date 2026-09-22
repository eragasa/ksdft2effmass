r"""Software verification of ``PlaneWaveParameterStudyCompiler``.

Evidence profile: routine

Bounded artifact scope: generic ordered multi-Task plane-wave candidate compilation,
exact per-Task reuse, Workflow/CPN fan-in, and typed observation collection request.

Facet and represented meaning

The module verifies exact candidate/factor binding, SCF-to-diagnostic ordering, reuse,
all-branch collection, separate analysis, and deterministic closed failures.

Intrinsic and cross-object scope

``PlaneWaveParameterStudyCompiler`` is the sole system under test. Generic Workflow,
CPN, calculator, and analysis owners are composed through their public records without
reproducing their internal algorithms.

VVUQ and scientific exclusions

All identities and values are synthetic software fixtures. No scientific executable is
invoked and no convergence, parameter choice, backend equivalence, validation,
uncertainty quantification, authority, persistence, or human acceptance is established.
"""

from dataclasses import replace

import pytest

from ksdft2effmass.analysis._parameter_study import (
    ParameterFactorKind,
    ParameterStudyCandidate,
    ParameterStudyCandidateIdentity,
    ParameterStudyIdentity,
    ParameterStudyKind,
    ParameterStudyObservationCollectionIdentity,
    ParameterStudyRevision,
    ParameterStudyRevisionIdentity,
    ParameterStudySubjectIdentity,
    QuantityOfInterestDefinition,
    ScalarQuantityOfInterestCriterion,
)
from ksdft2effmass.analysis.qoi import (
    NormalizedObservationRequirementIdentity,
    QuantityOfInterestCompleteness,
    QuantityOfInterestIdentity,
)
from ksdft2effmass.calculators.dft.pw import (
    PlaneWaveBackendBinding,
    PlaneWaveBackendBindingIdentity,
    PlaneWaveBackendIdentity,
    PlaneWaveBackendSupplement,
    PlaneWaveBackendSupplementIdentity,
    PlaneWaveEnergyCutoff,
    PlaneWaveNativeConfigurationIdentity,
    PlaneWaveObservationRequirementIdentity,
    PlaneWavePhysicalModelIdentity,
    PlaneWaveReciprocalMesh,
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
    PlaneWaveStudyTaskBinding,
    PlaneWaveStudyTaskRoleIdentity,
)
from ksdft2effmass.petrinet.colored import (
    ColoredPetriNetDefinitionIdentity,
    ColoredPetriNetDefinitionValidator,
    ColoredPetriNetMarkingIdentity,
    ColoredPetriNetMarkingValidator,
    ColoredPetriNetTransitionEnabler,
)
from ksdft2effmass.units import UnitIdentity, UnitScalar
from ksdft2effmass.workflows import (
    TaskDefinitionIdentity,
    TaskInstance,
    TaskInstanceIdentity,
    TaskStartGateSetMode,
    WorkflowIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = PlaneWaveParameterStudyCompiler


class TestPlaneWaveParameterStudyCompiler:
    """Own software evidence for the generic effect-free study compiler."""

    COMPILER_IDENTITY = PlaneWaveStudyCompilerIdentity("plane-wave-study-compiler.v2")
    SCF_ROLE = PlaneWaveStudyTaskRoleIdentity("scf")
    NSCF_ROLE = PlaneWaveStudyTaskRoleIdentity("diagnostic-nscf")
    SUBJECT = ParameterStudySubjectIdentity("model.synthetic.scalar.non-soc")
    PHYSICAL_MODEL = PlaneWavePhysicalModelIdentity(
        "physical-model.synthetic.scalar.non-soc"
    )
    ENERGY = PlaneWaveObservationRequirementIdentity("calculator.total-energy")
    EIGENVALUES = PlaneWaveObservationRequirementIdentity("calculator.eigenvalues")

    @classmethod
    def revisions(
        cls,
    ) -> tuple[ParameterStudyRevision, ParameterStudyRevision]:
        """Return cutoff and mesh revisions sharing one fixed synthetic subject."""
        criterion = ScalarQuantityOfInterestCriterion(
            QuantityOfInterestIdentity("qoi.synthetic"), "electron_volt", 0.01
        )
        cutoff = ParameterStudyRevision(
            ParameterStudyRevisionIdentity("revision.cutoff"),
            ParameterStudyIdentity("study.cutoff"),
            ParameterStudyKind.NUMERICAL_CONVERGENCE,
            (
                ParameterStudyCandidate(
                    ParameterStudyCandidateIdentity("candidate.C48"),
                    cls.SUBJECT,
                    ParameterFactorKind.NUMERICAL,
                    "wavefunction_cutoff",
                    48.0,
                    "electron_volt",
                ),
                ParameterStudyCandidate(
                    ParameterStudyCandidateIdentity("candidate.C60"),
                    cls.SUBJECT,
                    ParameterFactorKind.NUMERICAL,
                    "wavefunction_cutoff",
                    60.0,
                    "electron_volt",
                ),
            ),
            (criterion,),
            None,
        )
        mesh = ParameterStudyRevision(
            ParameterStudyRevisionIdentity("revision.mesh"),
            ParameterStudyIdentity("study.mesh"),
            ParameterStudyKind.NUMERICAL_CONVERGENCE,
            (
                ParameterStudyCandidate(
                    ParameterStudyCandidateIdentity("candidate.K8"),
                    cls.SUBJECT,
                    ParameterFactorKind.NUMERICAL,
                    "reciprocal_mesh_axis_count",
                    8.0,
                    "points_per_axis",
                ),
            ),
            (criterion,),
            None,
        )
        return cutoff, mesh

    @classmethod
    def branch(
        cls, label: str, cutoff: float, mesh_count: int
    ) -> tuple[PlaneWaveStudyTaskBinding, PlaneWaveStudyTaskBinding]:
        """Return one exact ungated SCF/diagnostic-NSCF branch."""
        scf_native = PlaneWaveNativeConfigurationIdentity(f"native.{label}.scf")
        scf_binding = PlaneWaveBackendBinding(
            PlaneWaveBackendBindingIdentity(f"binding.{label}.scf"),
            PlaneWaveSimulationSpecification(
                PlaneWaveSimulationSpecificationIdentity(f"specification.{label}.scf"),
                cls.PHYSICAL_MODEL,
                PlaneWaveEnergyCutoff(UnitScalar(cutoff, UnitIdentity.ELECTRON_VOLT)),
                PlaneWaveReciprocalMesh(
                    (mesh_count, mesh_count, mesh_count), (False, False, False)
                ),
                (cls.ENERGY,),
            ),
            PlaneWaveBackendSupplement(
                PlaneWaveBackendSupplementIdentity(f"supplement.{label}.scf"),
                PlaneWaveBackendIdentity("backend.synthetic"),
                scf_native,
            ),
        )
        return (
            PlaneWaveStudyTaskBinding(
                cls.SCF_ROLE,
                TaskInstance(
                    TaskInstanceIdentity(f"task.{label}.scf"),
                    TaskDefinitionIdentity("plane-wave.scf.v1"),
                    None,
                ),
                scf_native,
                (cls.ENERGY,),
                scf_binding,
            ),
            PlaneWaveStudyTaskBinding(
                cls.NSCF_ROLE,
                TaskInstance(
                    TaskInstanceIdentity(f"task.{label}.nscf"),
                    TaskDefinitionIdentity("plane-wave.diagnostic-nscf.v1"),
                    None,
                ),
                PlaneWaveNativeConfigurationIdentity(f"native.{label}.nscf"),
                (cls.EIGENVALUES,),
                None,
            ),
        )

    @classmethod
    def request(cls) -> PlaneWaveStudyCompilationRequest:
        """Return one valid request where logical K8 exactly reuses C48 Tasks."""
        cutoff, mesh = cls.revisions()
        c48_branch = cls.branch("C48", 48.0, 8)
        c60_branch = cls.branch("C60", 60.0, 8)
        bindings = (
            PlaneWaveStudyCandidateBinding(
                cutoff.candidates[0], c48_branch, cls.SCF_ROLE
            ),
            PlaneWaveStudyCandidateBinding(
                cutoff.candidates[1], c60_branch, cls.SCF_ROLE
            ),
            PlaneWaveStudyCandidateBinding(
                mesh.candidates[0], c48_branch, cls.SCF_ROLE
            ),
        )
        definition = QuantityOfInterestDefinition(
            QuantityOfInterestIdentity("qoi.synthetic"),
            (
                NormalizedObservationRequirementIdentity("normalized.energy"),
                NormalizedObservationRequirementIdentity("normalized.eigenvalues"),
            ),
            QuantityOfInterestCompleteness.COMPLETE,
        )
        return PlaneWaveStudyCompilationRequest(
            PlaneWaveStudyCompilationIdentity("compilation.synthetic"),
            cls.COMPILER_IDENTITY,
            WorkflowIdentity("workflow.synthetic"),
            ColoredPetriNetDefinitionIdentity("cpn.synthetic"),
            ColoredPetriNetMarkingIdentity("marking.synthetic.initial"),
            (cutoff, mesh),
            PlaneWaveStudySubjectBinding(cls.SUBJECT, cls.PHYSICAL_MODEL),
            (
                PlaneWaveQuantityOfInterestBinding(
                    definition,
                    (
                        PlaneWaveObservationRequirementBinding(
                            cls.SCF_ROLE,
                            definition.observation_requirement_identities[0],
                            cls.ENERGY,
                        ),
                        PlaneWaveObservationRequirementBinding(
                            cls.NSCF_ROLE,
                            definition.observation_requirement_identities[1],
                            cls.EIGENVALUES,
                        ),
                    ),
                ),
            ),
            bindings,
            TaskInstance(
                TaskInstanceIdentity("task.collect"),
                TaskDefinitionIdentity("analysis.collect-observations.v1"),
                None,
            ),
            TaskInstance(
                TaskInstanceIdentity("task.analyze"),
                TaskDefinitionIdentity("analysis.parameter-study.v1"),
                None,
            ),
            ParameterStudyObservationCollectionIdentity("collection.synthetic"),
        )

    def test_method__execute__compiles_ordered_multitask_workflow_and_cpn(
        self,
    ) -> None:
        """Evidence ID: SV-PLANE-WAVE-STUDY-009

        Requirement: Generic compilation represents ordered SCF-to-diagnostic Tasks,
        all-branch collection, and separately gated analysis without effects.

        Acceptance: Two unique branches compile to six Tasks/transitions, five
        dependencies, valid CPN state, and exactly two initially enabled SCFs.
        """
        result = SUT(self.COMPILER_IDENTITY).execute(self.request())

        assert type(result) is PlaneWaveStudyCompilationCompiled
        study = result.study
        assert len(study.workflow_composition.task_instances) == 6
        assert len(study.definition.transitions) == 6
        assert len(study.task_dependencies) == 5
        assert (
            ColoredPetriNetDefinitionValidator().execute(study.definition).issues == ()
        )
        assert (
            ColoredPetriNetMarkingValidator()
            .execute(study.definition, study.initial_marking)
            .issues
            == ()
        )
        enablement = ColoredPetriNetTransitionEnabler().execute(
            study.definition, study.initial_marking
        )
        assert enablement.enabled_bindings is not None
        assert tuple(
            value.transition_identity for value in enablement.enabled_bindings
        ) == (
            study.candidates[0].tasks[0].transition_identity,
            study.candidates[1].tasks[0].transition_identity,
        )

    def test_method__execute__retains_per_task_reuse_and_logical_candidate(
        self,
    ) -> None:
        """Evidence ID: SV-PLANE-WAVE-STUDY-011

        Requirement: A logical mesh candidate may reuse exact prior SCF and NSCF
        Tasks while remaining present in candidate and observation order.

        Acceptance: K8 retains C48's two compiled Tasks and produces two role-specific
        reuse records in the analysis-owned collection request.
        """
        result = SUT(self.COMPILER_IDENTITY).execute(self.request())

        assert type(result) is PlaneWaveStudyCompilationCompiled
        study = result.study
        assert study.candidates[2].tasks == study.candidates[0].tasks
        assert len(study.reuse) == 2
        assert tuple(value.task_role_identity for value in study.reuse) == (
            self.SCF_ROLE,
            self.NSCF_ROLE,
        )
        collection = study.observation_collection_request
        assert collection.candidate_identities == tuple(
            value.candidate.identity for value in self.request().candidate_bindings
        )
        assert len(collection.reuse) == 2

    def test_method__execute__preserves_compiled_branch_and_join_gates(self) -> None:
        """Evidence ID: SV-PLANE-WAVE-STUDY-012

        Requirement: Every later branch Task waits for its predecessor, collection
        waits for every unique branch final Task, and analysis waits for collection.

        Acceptance: NSCF gates have one member, collection has two, analysis has one,
        and every gate set uses ``ALL_OF``.
        """
        result = SUT(self.COMPILER_IDENTITY).execute(self.request())

        assert type(result) is PlaneWaveStudyCompilationCompiled
        study = result.study
        first_gate = study.candidates[0].tasks[1].task_instance.start_gate_set
        second_gate = study.candidates[1].tasks[1].task_instance.start_gate_set
        assert first_gate is not None
        assert second_gate is not None
        assert first_gate.mode is TaskStartGateSetMode.ALL_OF
        assert second_gate.mode is TaskStartGateSetMode.ALL_OF
        assert len(first_gate.gates) == 1
        assert len(second_gate.gates) == 1
        collection_gate = study.collection_task_instance.start_gate_set
        analysis_gate = study.analysis_task_instance.start_gate_set
        assert collection_gate is not None
        assert analysis_gate is not None
        assert len(collection_gate.gates) == 2
        assert len(analysis_gate.gates) == 1

    def test_method__execute__returns_correlated_factor_binding_failure(self) -> None:
        """Evidence ID: SV-PLANE-WAVE-STUDY-013

        Requirement: Candidate values agree exactly with the selected portable cutoff
        or isotropic reciprocal-mesh field in canonical project units.

        Acceptance: Changing K8 to 10 without changing its binding returns the exact
        incompatible factor failure and no partial plan.
        """
        request = self.request()
        mesh_binding = request.candidate_bindings[2]
        drifted_candidate = replace(mesh_binding.candidate, value=10.0)
        drifted_revision = replace(
            request.revisions[1], candidates=(drifted_candidate,)
        )
        drifted = replace(
            request,
            revisions=(request.revisions[0], drifted_revision),
            candidate_bindings=request.candidate_bindings[:2]
            + (replace(mesh_binding, candidate=drifted_candidate),),
        )

        result = SUT(self.COMPILER_IDENTITY).execute(drifted)

        assert type(result) is PlaneWaveStudyCompilationFailure
        assert result.request is drifted
        assert result.outcome is PlaneWaveStudyCompilationOutcome.INCOMPATIBLE
        assert (
            result.code
            is PlaneWaveStudyCompilationFailureCode.CANDIDATE_FACTOR_MISMATCH
        )

    def test_method__execute__requires_role_specific_observation_coverage(
        self,
    ) -> None:
        """Evidence ID: SV-PLANE-WAVE-STUDY-008

        Requirement: Every logical candidate supplies every role-specific calculator
        observation required by its QoI definition.

        Acceptance: Removing NSCF eigenvalues from one branch returns the exact
        unsupported observation failure.
        """
        request = self.request()
        candidate = request.candidate_bindings[1]
        nscf = candidate.task_bindings[1]
        replacement_requirement = PlaneWaveObservationRequirementIdentity(
            "calculator.density-of-states"
        )
        drifted_nscf = replace(
            nscf, observation_requirement_identities=(replacement_requirement,)
        )
        drifted_candidate = replace(
            candidate, task_bindings=(candidate.task_bindings[0], drifted_nscf)
        )
        drifted = replace(
            request,
            candidate_bindings=(request.candidate_bindings[0], drifted_candidate)
            + request.candidate_bindings[2:],
        )

        result = SUT(self.COMPILER_IDENTITY).execute(drifted)

        assert type(result) is PlaneWaveStudyCompilationFailure
        assert result.outcome is PlaneWaveStudyCompilationOutcome.UNSUPPORTED
        assert (
            result.code
            is PlaneWaveStudyCompilationFailureCode.REQUIRED_OBSERVATION_MISSING
        )

    def test_method__execute__rejects_identical_content_without_task_reuse(
        self,
    ) -> None:
        """Evidence ID: SV-PLANE-WAVE-STUDY-014

        Requirement: Exact execution-defining Task content has one Task instance;
        duplicate identities are not invented for identical work.

        Acceptance: Giving logical K8 copied content with new Task identities returns
        the exact reuse failure.
        """
        request = self.request()
        alias = request.candidate_bindings[2]
        copied_tasks = tuple(
            replace(
                value,
                task_instance=replace(
                    value.task_instance,
                    identity=TaskInstanceIdentity(
                        f"{value.task_instance.identity.value}.copy"
                    ),
                ),
            )
            for value in alias.task_bindings
        )
        drifted = replace(
            request,
            candidate_bindings=request.candidate_bindings[:2]
            + (replace(alias, task_bindings=copied_tasks),),
        )

        result = SUT(self.COMPILER_IDENTITY).execute(drifted)

        assert type(result) is PlaneWaveStudyCompilationFailure
        assert result.outcome is PlaneWaveStudyCompilationOutcome.INVALID
        assert result.code is (
            PlaneWaveStudyCompilationFailureCode.IDENTICAL_TASK_CONTENT_NOT_REUSED
        )

    def test_method__execute_failure__retains_exact_request_and_compiler(self) -> None:
        """Evidence ID: SV-PLANE-WAVE-STUDY-010

        Requirement: A compilation failure retains the exact request and exact
        compiler identity that rejected it.

        Acceptance: A different compiler returns a correlated compiler-identity
        mismatch without constructing a partial study.
        """
        request = self.request()
        executed_identity = PlaneWaveStudyCompilerIdentity(
            "plane-wave-study-compiler.different"
        )

        result = SUT(executed_identity).execute(request)

        assert type(result) is PlaneWaveStudyCompilationFailure
        assert result.request is request
        assert result.executed_compiler_identity is executed_identity
        assert result.outcome is PlaneWaveStudyCompilationOutcome.INVALID
        assert result.code is (
            PlaneWaveStudyCompilationFailureCode.COMPILER_IDENTITY_MISMATCH
        )
