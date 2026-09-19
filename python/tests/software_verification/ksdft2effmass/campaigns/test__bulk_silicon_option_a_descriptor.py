r"""Software verification of maintained bulk-silicon Option-A descriptor.

Evidence profile: routine

Bounded artifact scope: exact retained inputs, canonical-unit provenance, nine unique
SCF/diagnostic branches, C48/K8 reuse, generic fan-in, and typed collection request.

Facet and represented meaning

The descriptor is the primary artifact. The generic plane-wave compiler, Workflow,
CPN, units, and analysis owners are composed through their existing contracts.

Intrinsic and cross-object scope

The test verifies material-specific descriptor content and its generic compilation.
It does not reproduce generic validators or conversion arithmetic.

VVUQ and scientific exclusions

Retained files and synthetic firing outputs are software fixtures. No scientific
executable is invoked and no convergence, parameter selection, numerical verification,
scientific validation, uncertainty quantification, warning disposition, authority,
persistence, or human acceptance is established.
"""

from hashlib import sha256
from pathlib import Path

import pytest

import ksdft2effmass.campaigns as campaigns
from ksdft2effmass.campaigns._bulk_silicon_production_convergence import (
    BULK_SILICON_OPTION_A_DESCRIPTOR,
    BulkSiliconOptionADescriptor,
)
from ksdft2effmass.campaigns._plane_wave_study import (
    CompiledPlaneWaveStudy,
    PlaneWaveParameterStudyCompiler,
    PlaneWaveStudyCompilationCompiled,
)
from ksdft2effmass.petrinet.colored import (
    ColoredPetriNetBinding,
    ColoredPetriNetBindingAssignment,
    ColoredPetriNetBindingSelector,
    ColoredPetriNetDefinitionValidator,
    ColoredPetriNetFiringInput,
    ColoredPetriNetFiringOutcomeKind,
    ColoredPetriNetMarking,
    ColoredPetriNetMarkingValidator,
    ColoredPetriNetSelectionOutcomeKind,
    ColoredPetriNetTransitionEnabler,
    ColoredPetriNetTransitionFirer,
    ColoredPetriNetTransitionIdentity,
    ColoredPetriNetValue,
    ColoredPetriNetValueKind,
)
from ksdft2effmass.units import (
    MetalUnitConversionLimitation,
    UnitIdentity,
)
from ksdft2effmass.workflows import ArtifactProducerKind

pytestmark = pytest.mark.software_verification


class TestBulkSiliconOptionADescriptor:
    """Own maintained evidence for the material-specific descriptor artifact."""

    @staticmethod
    def repository_root() -> Path:
        """Return the checkout root containing this maintained test module."""
        return Path(__file__).resolve().parents[5]

    @staticmethod
    def compiled() -> CompiledPlaneWaveStudy:
        """Compile the maintained descriptor with the generic compiler."""
        request = BULK_SILICON_OPTION_A_DESCRIPTOR.compilation_request
        result = PlaneWaveParameterStudyCompiler(request.compiler_identity).execute(
            request
        )
        assert type(result) is PlaneWaveStudyCompilationCompiled
        return result.study

    @staticmethod
    def advance_canonically(
        study: CompiledPlaneWaveStudy,
        marking: ColoredPetriNetMarking,
    ) -> tuple[ColoredPetriNetMarking, ColoredPetriNetTransitionIdentity]:
        """Apply one pure generic CPN firing with a synthetic result identity."""
        enablement = ColoredPetriNetTransitionEnabler().execute(
            study.definition, marking
        )
        selection = ColoredPetriNetBindingSelector().execute(
            study.definition, enablement
        )
        assert selection.outcome is ColoredPetriNetSelectionOutcomeKind.SELECTED
        assert selection.selected_binding is not None
        transition_identity = selection.selected_binding.transition_identity
        transition = next(
            value
            for value in study.definition.transitions
            if value.identity == transition_identity
        )
        external = ColoredPetriNetBinding(
            transition_identity,
            tuple(
                ColoredPetriNetBindingAssignment(
                    variable,
                    ColoredPetriNetValue(
                        ColoredPetriNetValueKind.STRING,
                        f"synthetic-result:{transition_identity.value}",
                    ),
                )
                for variable in transition.external_output_variable_identities
            ),
        )
        firing = ColoredPetriNetTransitionFirer().execute(
            ColoredPetriNetFiringInput(
                study.definition,
                transition_identity,
                marking,
                enablement,
                selection,
                selection.selected_binding,
                None,
                external,
            )
        )
        assert firing.outcome is ColoredPetriNetFiringOutcomeKind.SUCCESS
        assert firing.successor_marking is not None
        return firing.successor_marking, transition_identity

    @classmethod
    def close_next_branch(
        cls,
        study: CompiledPlaneWaveStudy,
        marking: ColoredPetriNetMarking,
    ) -> ColoredPetriNetMarking:
        """Apply the next canonical SCF and diagnostic-NSCF firings."""
        after_scf, _scf = cls.advance_canonically(study, marking)
        after_nscf, _nscf = cls.advance_canonically(study, after_scf)
        return after_nscf

    def test_artifact__descriptor_values__defines_ten_logical_candidates(self) -> None:
        """Evidence ID: SV-BULK-SI-OPTION-A-DESCRIPTOR-001

        Requirement: The maintained descriptor contains six cutoff and four mesh
        candidates under one fixed subject, represented by nine unique retained cases.

        Acceptance: Counts and C48/K8 logical sharing are exact, reciprocal meshes
        retain native half shifts, SCF bindings select the authorized QE 7.2 identity,
        future storage uses the selected absolute root, and diagnostic NSCFs are not
        misrepresented as regular portable meshes.
        """
        descriptor = BULK_SILICON_OPTION_A_DESCRIPTOR
        request = descriptor.compilation_request

        assert type(descriptor) is BulkSiliconOptionADescriptor
        assert descriptor.external_workspace_root == (
            "/Users/eugene/projects/ksdft2effmass"
        )
        assert len(descriptor.cases) == 9
        assert tuple(len(value.candidate_identities) for value in descriptor.cases) == (
            1,
            1,
            1,
            2,
            1,
            1,
            1,
            1,
            1,
        )
        assert tuple(len(value.candidates) for value in request.revisions) == (6, 4)
        assert len(request.candidate_bindings) == 10
        assert request.candidate_bindings[7].task_bindings == (
            request.candidate_bindings[3].task_bindings
        )
        assert all(
            value.task_bindings[
                0
            ].backend_binding.specification.reciprocal_mesh.half_step_shifts
            == (True, True, True)
            for value in request.candidate_bindings
            if value.task_bindings[0].backend_binding is not None
        )
        assert all(
            value.task_bindings[1].backend_binding is None
            for value in request.candidate_bindings
        )
        assert {
            value.task_bindings[0].backend_binding.supplement.backend_identity.value
            for value in request.candidate_bindings
            if value.task_bindings[0].backend_binding is not None
        } == {"quantum-espresso.pw.x.7.2"}

    def test_artifact__canonical_conversions__retain_sources_and_limitations(
        self,
    ) -> None:
        """Evidence ID: SV-BULK-SI-OPTION-A-DESCRIPTOR-002

        Requirement: Native Rydberg values are explicitly converted to canonical eV
        with exact definition, source-artifact, content, and limitation provenance.

        Acceptance: All nine branch cutoffs and the criterion retain complete success
        results; no native value is relabelled or source record rewritten.
        """
        descriptor = BULK_SILICON_OPTION_A_DESCRIPTOR
        conversions = tuple(value.cutoff_conversion for value in descriptor.cases) + (
            descriptor.criterion_conversion,
        )

        assert all(
            value.request.source.unit is UnitIdentity.RYDBERG
            and value.output.unit is UnitIdentity.ELECTRON_VOLT
            and value.definition.identity == "rydberg-to-electron-volt"
            and value.request.source_correlation is not None
            and value.request.source_correlation.content_identity is not None
            for value in conversions
        )
        assert all(
            value.limitations
            == (
                MetalUnitConversionLimitation.BINARY64_OUTPUT_ROUNDED,
                MetalUnitConversionLimitation.FACTOR_UNCERTAINTY_NOT_PROPAGATED,
            )
            for value in conversions
        )
        assert descriptor.cases[0].cutoff_conversion.request.source.value == 30.0
        assert descriptor.cases[0].cutoff_conversion.output.value == (408.170793689715)
        assert (
            descriptor.compilation_request.revisions[0].criteria[0].absolute_tolerance
            == descriptor.criterion_conversion.output.value
        )

    def test_artifact__retained_inputs__match_repository_bytes(self) -> None:
        """Evidence ID: SV-BULK-SI-OPTION-A-DESCRIPTOR-003

        Requirement: Maintained descriptor artifact identities identify the exact
        compact retained input and bootstrap-disposition bytes.

        Acceptance: Every path exists with matching byte count and SHA-256; provenance
        remains ``ImportedRetainedFixture`` rather than fabricated Workflow history.
        """
        descriptor = BULK_SILICON_OPTION_A_DESCRIPTOR
        root = self.repository_root()

        artifacts = tuple(
            artifact
            for case in descriptor.cases
            for artifact in (case.scf_input, case.nscf_input)
        )
        observed = tuple(
            (
                artifact.repository_path,
                len((root / artifact.repository_path).read_bytes()),
                sha256((root / artifact.repository_path).read_bytes()).hexdigest(),
            )
            for artifact in artifacts
        )
        expected = tuple(
            (
                artifact.repository_path,
                artifact.content_identity.byte_count,
                artifact.content_identity.digest,
            )
            for artifact in artifacts
        )
        assert observed == expected
        provenance_path = root / descriptor.provenance.source_reference
        provenance_payload = provenance_path.read_bytes()
        assert (
            descriptor.provenance.kind is ArtifactProducerKind.IMPORTED_RETAINED_FIXTURE
        )
        assert (
            len(provenance_payload) == descriptor.provenance.content_identity.byte_count
        )
        assert sha256(provenance_payload).hexdigest() == (
            descriptor.provenance.content_identity.digest
        )

    def test_artifact__generic_compilation__produces_exact_nine_branch_fan_in(
        self,
    ) -> None:
        """Evidence ID: SV-BULK-SI-OPTION-A-DESCRIPTOR-004

        Requirement: Generic compilation maps ten logical candidates onto nine unique
        SCF/NSCF branches, one all-branch collection, and separate analysis.

        Acceptance: The plan has 20 Tasks/transitions, 19 dependencies, two exact
        per-role reuse records, valid CPN state, and no invented K8 Task identity.
        """
        study = self.compiled()

        assert len(study.workflow_composition.task_instances) == 20
        assert len(study.definition.transitions) == 20
        assert len(study.task_dependencies) == 19
        assert len(study.reuse) == 2
        assert study.candidates[7].tasks == study.candidates[3].tasks
        task_values = tuple(
            value.identity.value for value in study.workflow_composition.task_instances
        )
        assert all("K8" not in value for value in task_values)
        assert (
            ColoredPetriNetDefinitionValidator().execute(study.definition).issues == ()
        )
        assert (
            ColoredPetriNetMarkingValidator()
            .execute(study.definition, study.initial_marking)
            .issues
            == ()
        )

    def test_artifact__fan_in__enables_collection_then_analysis(
        self,
    ) -> None:
        """Evidence ID: SV-BULK-SI-OPTION-A-DESCRIPTOR-005

        Requirement: Collection remains disabled until every unique branch closes;
        analysis remains disabled until collection produces its typed result identity.

        Acceptance: Eighteen canonical branch firings enable only collection, whose
        firing then enables only analysis.
        """
        study = self.compiled()
        marking = self.close_next_branch(study, study.initial_marking)
        marking = self.close_next_branch(study, marking)
        marking = self.close_next_branch(study, marking)
        marking = self.close_next_branch(study, marking)
        marking = self.close_next_branch(study, marking)
        marking = self.close_next_branch(study, marking)
        marking = self.close_next_branch(study, marking)
        marking = self.close_next_branch(study, marking)
        marking = self.close_next_branch(study, marking)

        enablement = ColoredPetriNetTransitionEnabler().execute(
            study.definition, marking
        )
        assert enablement.enabled_bindings is not None
        assert tuple(
            value.transition_identity for value in enablement.enabled_bindings
        ) == (study.collection_transition_identity,)

        marking, transition = self.advance_canonically(study, marking)
        assert transition == study.collection_transition_identity
        enablement = ColoredPetriNetTransitionEnabler().execute(
            study.definition, marking
        )
        assert enablement.enabled_bindings is not None
        assert tuple(
            value.transition_identity for value in enablement.enabled_bindings
        ) == (study.analysis_transition_identity,)

    def test_artifact__collection_request__is_typed_and_ordered(
        self,
    ) -> None:
        """Evidence ID: SV-BULK-SI-OPTION-A-DESCRIPTOR-006

        Requirement: Collection is defined by an analysis-owned typed request with
        exact revision, candidate, role, Task-reuse, result, and producer-provenance
        slots rather than an unstructured payload token.

        Acceptance: Request order matches both revisions, has SCF/NSCF roles, and
        identifies exact C48 Task reuse for logical K8 twice.
        """
        study = self.compiled()
        collection = study.observation_collection_request
        request = BULK_SILICON_OPTION_A_DESCRIPTOR.compilation_request

        assert collection.revision_identities == tuple(
            value.identity for value in request.revisions
        )
        assert collection.candidate_identities == tuple(
            value.candidate.identity for value in request.candidate_bindings
        )
        assert tuple(value.value for value in collection.role_identities) == (
            "scf",
            "diagnostic-nscf",
        )
        assert len(collection.reuse) == 2
        assert all(
            value.candidate_identity.value.endswith("mesh.K8")
            and value.canonical_candidate_identity.value.endswith("cutoff.C48")
            for value in collection.reuse
        )

    def test_artifact__package_surface__keeps_descriptor_and_compiler_private(
        self,
    ) -> None:
        """Evidence ID: SV-BULK-SI-OPTION-A-DESCRIPTOR-007

        Requirement: Material values and revisable generic compilation stay private.

        Acceptance: The campaigns package root exports neither the descriptor nor the
        retired bulk-specific compiler, which no longer exists in production source.
        """
        assert not hasattr(campaigns, "BULK_SILICON_OPTION_A_DESCRIPTOR")
        assert not hasattr(campaigns, "BulkSiliconProductionConvergenceCompiler")
