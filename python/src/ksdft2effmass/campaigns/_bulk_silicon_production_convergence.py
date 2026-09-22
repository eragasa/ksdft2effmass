"""Maintained execution-free Option-A bulk-silicon study descriptor.

The descriptor binds exact retained compact inputs, imported-fixture provenance,
canonical-unit conversion results, ten logical candidates, nine unique ordered
SCF-to-diagnostic-NSCF branches, C48/K8 reuse, and the generic plane-wave study
compiler request. It performs no file access, scientific execution, parameter
selection, acceptance, persistence, authority decision, or native rendering.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath

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
    PlaneWaveQuantityOfInterestBinding,
    PlaneWaveStudyCandidateBinding,
    PlaneWaveStudyCompilationIdentity,
    PlaneWaveStudyCompilationRequest,
    PlaneWaveStudyCompilerIdentity,
    PlaneWaveStudySubjectBinding,
    PlaneWaveStudyTaskBinding,
    PlaneWaveStudyTaskRoleIdentity,
)
from ksdft2effmass.petrinet.colored import (
    ColoredPetriNetDefinitionIdentity,
    ColoredPetriNetMarkingIdentity,
)
from ksdft2effmass.units import (
    ContentIdentity,
    MetalQuantityConverter,
    MetalUnitConversionOutcome,
    MetalUnitConversionRequest,
    MetalUnitConversionSourceCorrelation,
    MetalUnitConversionSuccess,
    UnitIdentity,
    UnitScalar,
)
from ksdft2effmass.workflows import (
    ArtifactContentIdentity,
    ArtifactIdentity,
    ArtifactProducerKind,
    ArtifactProducerProvenanceIdentity,
    ImportedRetainedFixture,
    TaskDefinitionIdentity,
    TaskInstance,
    TaskInstanceIdentity,
    WorkflowIdentity,
)


@dataclass(frozen=True, slots=True)
class BulkSiliconOptionAInputArtifact:
    """Retain one exact compact repository input used by the descriptor."""

    identity: ArtifactIdentity
    repository_path: str
    content_identity: ArtifactContentIdentity

    def __post_init__(self) -> None:
        if type(self.identity) is not ArtifactIdentity:
            raise TypeError("identity must be ArtifactIdentity")
        if type(self.repository_path) is not str:
            raise TypeError("repository_path must be a built-in str")
        path = PurePosixPath(self.repository_path)
        if (
            not self.repository_path
            or path.is_absolute()
            or self.repository_path.startswith("~")
            or "\\" in self.repository_path
            or self.repository_path != path.as_posix()
            or any(part in {".", ".."} for part in path.parts)
        ):
            raise ValueError("repository_path must be a portable relative path")
        if type(self.content_identity) is not ArtifactContentIdentity:
            raise TypeError("content_identity must be ArtifactContentIdentity")

    @property
    def native_configuration_value(self) -> str:
        """Return exact artifact/content correlation for native configuration."""
        content = self.content_identity
        return (
            f"{self.identity.value}:{content.algorithm}:"
            f"{content.digest}:{content.byte_count}"
        )


@dataclass(frozen=True, slots=True)
class BulkSiliconOptionACaseDescriptor:
    """Describe one unique retained SCF-to-diagnostic-NSCF branch."""

    identity: str
    candidate_identities: tuple[ParameterStudyCandidateIdentity, ...]
    scf_input: BulkSiliconOptionAInputArtifact
    nscf_input: BulkSiliconOptionAInputArtifact
    cutoff_conversion: MetalUnitConversionSuccess

    def __post_init__(self) -> None:
        if type(self.identity) is not str:
            raise TypeError("identity must be a built-in str")
        if not self.identity:
            raise ValueError("identity must not be empty")
        if type(self.candidate_identities) is not tuple or any(
            type(value) is not ParameterStudyCandidateIdentity
            for value in self.candidate_identities
        ):
            raise TypeError(
                "candidate_identities must be a tuple of "
                "ParameterStudyCandidateIdentity"
            )
        if not self.candidate_identities or len(set(self.candidate_identities)) != len(
            self.candidate_identities
        ):
            raise ValueError("candidate identities must be nonempty and unique")
        if type(self.scf_input) is not BulkSiliconOptionAInputArtifact:
            raise TypeError("scf_input must be BulkSiliconOptionAInputArtifact")
        if type(self.nscf_input) is not BulkSiliconOptionAInputArtifact:
            raise TypeError("nscf_input must be BulkSiliconOptionAInputArtifact")
        if type(self.cutoff_conversion) is not MetalUnitConversionSuccess:
            raise TypeError("cutoff_conversion must be MetalUnitConversionSuccess")
        if self.cutoff_conversion.outcome is not MetalUnitConversionOutcome.CONVERTED:
            raise ValueError("cutoff_conversion must be converted")
        if self.cutoff_conversion.request.source.unit is not UnitIdentity.RYDBERG or (
            self.cutoff_conversion.output.unit is not UnitIdentity.ELECTRON_VOLT
        ):
            raise ValueError("case cutoff must convert Rydberg to electron volt")
        correlation = self.cutoff_conversion.request.source_correlation
        if (
            correlation is None
            or correlation.artifact_identity != self.scf_input.identity.value
        ):
            raise ValueError("case cutoff conversion must correlate to its SCF input")
        expected_content = ContentIdentity(
            f"sha256:{self.scf_input.content_identity.digest}"
        )
        if correlation.content_identity != expected_content:
            raise ValueError("case cutoff conversion must retain SCF content identity")


@dataclass(frozen=True, slots=True)
class BulkSiliconOptionADescriptor:
    """Own the complete maintained material-specific Option-A composition input."""

    provenance: ImportedRetainedFixture
    external_workspace_root: str
    criterion_conversion: MetalUnitConversionSuccess
    cases: tuple[BulkSiliconOptionACaseDescriptor, ...]
    compilation_request: PlaneWaveStudyCompilationRequest

    def __post_init__(self) -> None:
        if type(self.provenance) is not ImportedRetainedFixture:
            raise TypeError("provenance must be ImportedRetainedFixture")
        if type(self.external_workspace_root) is not str:
            raise TypeError("external_workspace_root must be a built-in str")
        root = PurePosixPath(self.external_workspace_root)
        if (
            not self.external_workspace_root
            or not root.is_absolute()
            or self.external_workspace_root != root.as_posix()
            or any(part in {".", ".."} for part in root.parts)
        ):
            raise ValueError("external_workspace_root must be an absolute POSIX path")
        if type(self.criterion_conversion) is not MetalUnitConversionSuccess:
            raise TypeError("criterion_conversion must be MetalUnitConversionSuccess")
        if type(self.cases) is not tuple or any(
            type(value) is not BulkSiliconOptionACaseDescriptor for value in self.cases
        ):
            raise TypeError("cases must be a tuple of BulkSiliconOptionACaseDescriptor")
        if not self.cases:
            raise ValueError("cases must not be empty")
        if len({value.identity for value in self.cases}) != len(self.cases):
            raise ValueError("case identities must be unique")
        if type(self.compilation_request) is not PlaneWaveStudyCompilationRequest:
            raise TypeError(
                "compilation_request must be PlaneWaveStudyCompilationRequest"
            )
        artifacts = tuple(
            artifact
            for case in self.cases
            for artifact in (case.scf_input, case.nscf_input)
        )
        if len({value.identity for value in artifacts}) != len(artifacts):
            raise ValueError("input artifact identities must be unique")
        if len({value.repository_path for value in artifacts}) != len(artifacts):
            raise ValueError("input repository paths must be unique")
        logical_candidates = tuple(
            candidate.identity
            for revision in self.compilation_request.revisions
            for candidate in revision.candidates
        )
        represented_candidates = tuple(
            candidate for case in self.cases for candidate in case.candidate_identities
        )
        if len(set(represented_candidates)) != len(represented_candidates) or set(
            represented_candidates
        ) != set(logical_candidates):
            raise ValueError(
                "cases must represent every logical candidate exactly once"
            )
        request_candidates = tuple(
            value.candidate.identity
            for value in self.compilation_request.candidate_bindings
        )
        if request_candidates != logical_candidates:
            raise ValueError("compilation bindings must follow logical candidate order")
        criterion = self.compilation_request.revisions[0].criteria[0]
        if criterion.absolute_tolerance != self.criterion_conversion.output.value or (
            criterion.unit != "electron_volt_per_atom"
        ):
            raise ValueError("criterion must equal its retained canonical conversion")
        for case in self.cases:
            canonical_candidate = case.candidate_identities[0]
            candidate_binding = next(
                value
                for value in self.compilation_request.candidate_bindings
                if value.candidate.identity == canonical_candidate
            )
            native_values = tuple(
                value.native_configuration_identity.value
                for value in candidate_binding.task_bindings
            )
            if native_values != (
                case.scf_input.native_configuration_value,
                case.nscf_input.native_configuration_value,
            ):
                raise ValueError("case inputs must equal compiled native identities")
            scf_binding = candidate_binding.task_bindings[0].backend_binding
            if scf_binding is None or (
                scf_binding.specification.wavefunction_cutoff.value
                != case.cutoff_conversion.output.value
            ):
                raise ValueError(
                    "case SCF cutoff must equal retained conversion output"
                )


@dataclass(frozen=True, slots=True)
class BulkSiliconOptionADescriptorComposer:
    """Compose the maintained descriptor from exact retained identities only."""

    _CASE_RECORDS = (
        (
            "C30",
            "cutoff",
            30.0,
            8,
            "7521611b6045015b72e34b2cc6749084c69b31beb4e74a32caa1db893d5f1120",
            756,
            "062f8226454c49c616bb7b99ed4834706923a27d2a09987abe83421890bc03a4",
            785,
        ),
        (
            "C36",
            "cutoff",
            36.0,
            8,
            "3f62f2b8b3b43dbfd592779e1ebf60c3b200cef994b216b1a858dde83ee6b0ba",
            756,
            "3d1f9a942409b5fe39aac4eb0771f64e9d44d42d6ef981d21ac98955387ea0a0",
            785,
        ),
        (
            "C42",
            "cutoff",
            42.0,
            8,
            "bdfdac7397283db99a8679d92d653e7611f43bd86e685d0219328d416e720ff2",
            756,
            "8967efb8c6b9ebfe182a18e3c9bb53360d193d1da3fef6b8f9d6ad807f4dd093",
            785,
        ),
        (
            "C48",
            "cutoff",
            48.0,
            8,
            "cadb2a3024f39858f91b23bd1c1c22e2b2d0f161f2960c39ea1abf48cf00ee17",
            756,
            "5f6fde9bcc5e0823982f97a4815c66d8d0af48e86bcf89cab5bab953cd47e69f",
            785,
        ),
        (
            "C54",
            "cutoff",
            54.0,
            8,
            "56b68d3dce5cae17911b53f135b139d07c4b9dea2b3206af634fee1c110fa8ff",
            756,
            "317a0aae10b9109ed57f0bb57a400972af40e236ffc8146fcc71afa93d697717",
            785,
        ),
        (
            "C60",
            "cutoff",
            60.0,
            8,
            "7462e94ffce991202abc9ff7e9d0267d337239f79f3bfd6912aad3a81c95c3e8",
            756,
            "43a5634cef3ee39224fcbc58ce0dddf309af335bc88e078fbdc5adcd5ea2210a",
            785,
        ),
        (
            "K6",
            "mesh",
            48.0,
            6,
            "8fdffca94147b040e5148dffa766b4db5d9df1e4231702e92ccb853ad485ccda",
            753,
            "544857dfb28cc70f238649bf9f9d01abfcd756cd67c8e27937de550c13732210",
            782,
        ),
        (
            "K10",
            "mesh",
            48.0,
            10,
            "608b1bf4d90184fba1a7ea779518dc7024af176811d620b37b8d757c7a50f43a",
            759,
            "3a38bb93e77ec08f2dc966041799c4d025bbe3444f2a67578856edaf6f6e1e08",
            785,
        ),
        (
            "K12",
            "mesh",
            48.0,
            12,
            "0db0e43ecba028c6b5ef0ed2a74f13393e117eb7f0138eb211039792989d23c0",
            759,
            "97063529f58a053099e1a8cf809096e8e039a52d3c02b3db3aa5bf91a6d7f145",
            785,
        ),
    )

    def execute(self) -> BulkSiliconOptionADescriptor:
        """Return the exact immutable descriptor without reading or writing files."""
        subject = ParameterStudySubjectIdentity(
            "bulk-silicon.pbe.scalar-relativistic.non-soc"
        )
        physical_model = PlaneWavePhysicalModelIdentity(
            "bulk-silicon.pbe.oncv.scalar-relativistic.non-soc"
        )
        criterion_conversion = self._conversion(
            1.0e-5,
            MetalUnitConversionSourceCorrelation(
                artifact_identity=(
                    "docs/computational/"
                    "bulk-silicon-production-convergence-design.md#energy-criterion"
                ),
                content_identity=ContentIdentity(
                    "sha256:36879e2d159455710952a9ed982bd8712feff4ba263093cc0952f4add253e706"
                ),
            ),
        )
        criterion = ScalarQuantityOfInterestCriterion(
            QuantityOfInterestIdentity("bulk-silicon.total-energy-per-atom"),
            "electron_volt_per_atom",
            criterion_conversion.output.value,
        )
        cutoff_candidates: list[ParameterStudyCandidate] = []
        mesh_candidates: list[ParameterStudyCandidate] = []
        cases: list[BulkSiliconOptionACaseDescriptor] = []
        branch_by_label: dict[
            str, tuple[PlaneWaveStudyTaskBinding, PlaneWaveStudyTaskBinding]
        ] = {}
        for (
            label,
            series,
            cutoff_rydberg,
            mesh_count,
            scf_digest,
            scf_bytes,
            nscf_digest,
            nscf_bytes,
        ) in self._CASE_RECORDS:
            scf_input = self._artifact(label, series, "scf", scf_digest, scf_bytes)
            nscf_input = self._artifact(label, series, "nscf", nscf_digest, nscf_bytes)
            conversion = self._conversion(
                cutoff_rydberg,
                MetalUnitConversionSourceCorrelation(
                    artifact_identity=scf_input.identity.value,
                    content_identity=ContentIdentity(f"sha256:{scf_digest}"),
                ),
            )
            candidate_ids = (
                (
                    self._candidate_identity("cutoff", "C48"),
                    self._candidate_identity("mesh", "K8"),
                )
                if label == "C48"
                else (
                    self._candidate_identity(
                        "cutoff" if series == "cutoff" else "mesh", label
                    ),
                )
            )
            branch = self._branch(
                label,
                conversion.output.value,
                mesh_count,
                physical_model,
                scf_input,
                nscf_input,
            )
            branch_by_label[label] = branch
            cases.append(
                BulkSiliconOptionACaseDescriptor(
                    label,
                    candidate_ids,
                    scf_input,
                    nscf_input,
                    conversion,
                )
            )
            if series == "cutoff":
                cutoff_candidates.append(
                    ParameterStudyCandidate(
                        self._candidate_identity("cutoff", label),
                        subject,
                        ParameterFactorKind.NUMERICAL,
                        "wavefunction_cutoff",
                        conversion.output.value,
                        "electron_volt",
                    )
                )
            else:
                mesh_candidates.append(
                    ParameterStudyCandidate(
                        self._candidate_identity("mesh", label),
                        subject,
                        ParameterFactorKind.NUMERICAL,
                        "reciprocal_mesh_axis_count",
                        float(mesh_count),
                        "points_per_axis",
                    )
                )
        mesh_candidates.insert(
            1,
            ParameterStudyCandidate(
                self._candidate_identity("mesh", "K8"),
                subject,
                ParameterFactorKind.NUMERICAL,
                "reciprocal_mesh_axis_count",
                8.0,
                "points_per_axis",
            ),
        )
        cutoff_study = ParameterStudyRevision(
            ParameterStudyRevisionIdentity("bulk-silicon.option-a.cutoff.revision-1"),
            ParameterStudyIdentity("bulk-silicon.option-a.cutoff"),
            ParameterStudyKind.NUMERICAL_CONVERGENCE,
            tuple(cutoff_candidates),
            (criterion,),
            None,
        )
        mesh_study = ParameterStudyRevision(
            ParameterStudyRevisionIdentity("bulk-silicon.option-a.mesh.revision-1"),
            ParameterStudyIdentity("bulk-silicon.option-a.mesh"),
            ParameterStudyKind.NUMERICAL_CONVERGENCE,
            tuple(mesh_candidates),
            (criterion,),
            None,
        )
        scf_role = PlaneWaveStudyTaskRoleIdentity("scf")
        candidate_bindings = tuple(
            PlaneWaveStudyCandidateBinding(
                candidate,
                branch_by_label[
                    (
                        "C48"
                        if candidate.identity == self._candidate_identity("mesh", "K8")
                        else candidate.identity.value.rsplit(".", maxsplit=1)[-1]
                    )
                ],
                scf_role,
            )
            for candidate in cutoff_study.candidates + mesh_study.candidates
        )
        qoi_definition = QuantityOfInterestDefinition(
            QuantityOfInterestIdentity("bulk-silicon.total-energy-per-atom"),
            (NormalizedObservationRequirementIdentity("normalized.total-energy"),),
            QuantityOfInterestCompleteness.COMPLETE,
        )
        compiler_identity = PlaneWaveStudyCompilerIdentity(
            "plane-wave-parameter-study-compiler.v2"
        )
        request = PlaneWaveStudyCompilationRequest(
            PlaneWaveStudyCompilationIdentity(
                "bulk-silicon.option-a.convergence.compilation.v1"
            ),
            compiler_identity,
            WorkflowIdentity("bulk-silicon.option-a.convergence.v1"),
            ColoredPetriNetDefinitionIdentity("bulk-silicon.option-a.convergence.v1"),
            ColoredPetriNetMarkingIdentity(
                "bulk-silicon.option-a.convergence.initial.v1"
            ),
            (cutoff_study, mesh_study),
            PlaneWaveStudySubjectBinding(subject, physical_model),
            (
                PlaneWaveQuantityOfInterestBinding(
                    qoi_definition,
                    (
                        PlaneWaveObservationRequirementBinding(
                            scf_role,
                            qoi_definition.observation_requirement_identities[0],
                            PlaneWaveObservationRequirementIdentity(
                                "calculator.total-energy"
                            ),
                        ),
                    ),
                ),
            ),
            candidate_bindings,
            TaskInstance(
                TaskInstanceIdentity("bulk-silicon.option-a.collect"),
                TaskDefinitionIdentity(
                    "analysis.collect-parameter-study-observations.v1"
                ),
                None,
            ),
            TaskInstance(
                TaskInstanceIdentity("bulk-silicon.option-a.analyze"),
                TaskDefinitionIdentity("analysis.plane-wave-parameter-study.v1"),
                None,
            ),
            ParameterStudyObservationCollectionIdentity(
                "bulk-silicon.option-a.observations.v1"
            ),
        )
        return BulkSiliconOptionADescriptor(
            provenance=self._provenance(),
            external_workspace_root="/Users/eugene/projects/ksdft2effmass",
            criterion_conversion=criterion_conversion,
            cases=tuple(cases),
            compilation_request=request,
        )

    @staticmethod
    def _candidate_identity(study: str, label: str) -> ParameterStudyCandidateIdentity:
        """Return one exact material-specific logical candidate identity."""
        return ParameterStudyCandidateIdentity(f"bulk-silicon.option-a.{study}.{label}")

    @staticmethod
    def _artifact(
        label: str,
        series: str,
        stage: str,
        digest: str,
        byte_count: int,
    ) -> BulkSiliconOptionAInputArtifact:
        """Return one retained compact input from its exact maintained identity."""
        suffix = "scf.in" if stage == "scf" else "diagnostic.nscf.in"
        repository_path = (
            "calculations/bulk-silicon/production-convergence-preflight/inputs/"
            f"{series}/{label}.{suffix}"
        )
        return BulkSiliconOptionAInputArtifact(
            ArtifactIdentity(f"bulk-silicon.option-a.{label}.{stage}.input"),
            repository_path,
            ArtifactContentIdentity("sha256", digest, byte_count),
        )

    @staticmethod
    def _conversion(
        value: float, correlation: MetalUnitConversionSourceCorrelation
    ) -> MetalUnitConversionSuccess:
        """Return one complete retained Rydberg-to-electron-volt conversion result."""
        result = MetalQuantityConverter().convert(
            MetalUnitConversionRequest(
                UnitScalar(value, UnitIdentity.RYDBERG),
                UnitIdentity.ELECTRON_VOLT,
                correlation,
            )
        )
        if type(result) is not MetalUnitConversionSuccess:
            raise ValueError(
                "maintained Option-A conversion must be supported and finite"
            )
        return result

    @staticmethod
    def _branch(
        label: str,
        cutoff_electron_volt: float,
        mesh_count: int,
        physical_model: PlaneWavePhysicalModelIdentity,
        scf_input: BulkSiliconOptionAInputArtifact,
        nscf_input: BulkSiliconOptionAInputArtifact,
    ) -> tuple[PlaneWaveStudyTaskBinding, PlaneWaveStudyTaskBinding]:
        """Return one exact ungated SCF and native diagnostic-NSCF Task branch."""
        scf_role = PlaneWaveStudyTaskRoleIdentity("scf")
        nscf_role = PlaneWaveStudyTaskRoleIdentity("diagnostic-nscf")
        total_energy = PlaneWaveObservationRequirementIdentity(
            "calculator.total-energy"
        )
        eigenvalues = PlaneWaveObservationRequirementIdentity("calculator.eigenvalues")
        scf_native = PlaneWaveNativeConfigurationIdentity(
            scf_input.native_configuration_value
        )
        scf_backend_binding = PlaneWaveBackendBinding(
            PlaneWaveBackendBindingIdentity(
                f"bulk-silicon.option-a.{label}.scf.binding"
            ),
            PlaneWaveSimulationSpecification(
                PlaneWaveSimulationSpecificationIdentity(
                    f"bulk-silicon.option-a.{label}.scf.specification"
                ),
                physical_model,
                PlaneWaveEnergyCutoff(
                    UnitScalar(cutoff_electron_volt, UnitIdentity.ELECTRON_VOLT)
                ),
                PlaneWaveReciprocalMesh(
                    (mesh_count, mesh_count, mesh_count), (True, True, True)
                ),
                (total_energy,),
            ),
            PlaneWaveBackendSupplement(
                PlaneWaveBackendSupplementIdentity(
                    f"bulk-silicon.option-a.{label}.scf.supplement"
                ),
                PlaneWaveBackendIdentity("quantum-espresso.pw.x.7.2"),
                scf_native,
            ),
        )
        return (
            PlaneWaveStudyTaskBinding(
                scf_role,
                TaskInstance(
                    TaskInstanceIdentity(f"bulk-silicon.option-a.{label}.scf"),
                    TaskDefinitionIdentity("quantum-espresso.pw.scf.v1"),
                    None,
                ),
                scf_native,
                (total_energy,),
                scf_backend_binding,
            ),
            PlaneWaveStudyTaskBinding(
                nscf_role,
                TaskInstance(
                    TaskInstanceIdentity(
                        f"bulk-silicon.option-a.{label}.diagnostic-nscf"
                    ),
                    TaskDefinitionIdentity("quantum-espresso.pw.diagnostic-nscf.v1"),
                    None,
                ),
                PlaneWaveNativeConfigurationIdentity(
                    nscf_input.native_configuration_value
                ),
                (eigenvalues,),
                None,
            ),
        )

    @staticmethod
    def _provenance() -> ImportedRetainedFixture:
        """Return retained bootstrap provenance without Workflow-history upgrade."""
        content = ArtifactContentIdentity(
            "sha256",
            "03b25b9eca084ef5475b48855543fecccec5c20d154dab95238e1d347980b1bf",
            4371,
        )
        return ImportedRetainedFixture(
            identity=ArtifactProducerProvenanceIdentity(
                "bulk-silicon.option-a.bootstrap-fixture"
            ),
            schema_version=1,
            kind=ArtifactProducerKind.IMPORTED_RETAINED_FIXTURE,
            artifact_identity=ArtifactIdentity(
                "bulk-silicon.production-convergence.bootstrap-disposition"
            ),
            content_identity=content,
            evidence_identity_values=(
                "calculated_result",
                "provisional_numerical_verification_evidence",
            ),
            claim_boundary_identity_values=(
                "no_accepted_parameter_setting",
                "no_canonical_scientific_workflow_run",
                "no_scientific_validation_claim",
            ),
            fixture_identity="bulk-silicon.option-a.bootstrap-fixture",
            fixture_revision="e9c6a1453a6a9dfac8c13256d7d146f6b6ec1716",
            source_identity="bulk-silicon.production-reference.convergence",
            source_reference=(
                "calculations/bulk-silicon/production-convergence-preflight/"
                "bootstrap-execution-disposition.json"
            ),
            import_identity="bulk-silicon.option-a.fixture-import.v1",
            import_receipt_identity="bulk-silicon.option-a.fixture-receipt.v1",
            retained_source_identity=(
                "bulk-silicon.production-convergence.direct-bootstrap"
            ),
            retained_content_identity=content,
            retained_checksum_identity=f"sha256:{content.digest}",
            retained_provenance_identity="execution-provenance.record-version-1",
            evidence_classification=(
                "audited_provisional_numerical_verification_evidence"
            ),
        )


BULK_SILICON_OPTION_A_DESCRIPTOR = BulkSiliconOptionADescriptorComposer().execute()
"""Maintained immutable execution-free Option-A descriptor."""
