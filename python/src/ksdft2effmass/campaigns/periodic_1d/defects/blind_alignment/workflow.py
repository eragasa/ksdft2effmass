"""Complete typed campaign composition for periodic-1D blind alignment."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..matched_extraction import RepresentedOperator, SupercellBasis
from .baseline import BlindAlignmentBaselineData
from .case_execution import (
    BlindAlignmentCaseExecutionActionizer,
    BlindAlignmentCaseExecutionRequest,
    BlindAlignmentCaseExecutionResult,
    BlindAlignmentInferenceRoute,
)
from .construction import (
    BlindAlignmentHiddenTruth,
    BlindAlignmentObservationConstructionRequest,
    BlindAlignmentObservationConstructionResult,
    BlindAlignmentObservationConstructor,
)
from .inference import BlindAlignmentInferenceActionizer
from .input_records import (
    BlindAlignmentCampaignInput,
    BlindAlignmentStoppingCase,
)
from .records import (
    BlindAlignmentInferenceRequest,
    BlindAlignmentObservation,
    ComplexMatrix,
)
from .result_records import (
    BlindAlignmentCampaignResult,
    BlindAlignmentConditioningDiagnosticResult,
    BlindAlignmentDiagnosticSuiteResult,
    BlindAlignmentEnergyAnchorDiagnosticResult,
    BlindAlignmentGaugeCaseResult,
    BlindAlignmentInformationBoundary,
    BlindAlignmentNoiseCaseResult,
    BlindAlignmentPrincipalAngleDiagnosticResult,
    BlindAlignmentProvenance,
    BlindAlignmentRankReconciliationResult,
    BlindAlignmentSpinReconciliationResult,
    BlindAlignmentStoppedCaseResult,
    BlindAlignmentStoppingControlResult,
    BlindAlignmentSuccessfulCaseResult,
)


@dataclass(frozen=True, slots=True)
class BlindAlignmentCampaignWorkflowRequest:
    """Request complete campaign composition from authenticated typed inputs.

    Parameters
    ----------
    specification
        Closed version-one campaign input.
    baseline
        Authenticated matched-extraction baseline.
    provenance
        Explicit provenance supplied by the calling execution adapter. The Workflow
        neither discovers paths nor fabricates execution identity.
    """

    specification: BlindAlignmentCampaignInput
    baseline: BlindAlignmentBaselineData
    provenance: BlindAlignmentProvenance

    def __post_init__(self) -> None:
        """Require exact specification, baseline, and provenance record types."""
        if not isinstance(self.specification, BlindAlignmentCampaignInput):
            raise TypeError("specification must be BlindAlignmentCampaignInput")
        if not isinstance(self.baseline, BlindAlignmentBaselineData):
            raise TypeError("baseline must be BlindAlignmentBaselineData")
        if not isinstance(self.provenance, BlindAlignmentProvenance):
            raise TypeError("provenance must be BlindAlignmentProvenance")


class BlindAlignmentCampaignWorkflow:
    """Compose all exact, sensitivity, gauge, stop, and boundary-diagnostic cases."""

    __slots__ = ()

    def execute(
        self, request: BlindAlignmentCampaignWorkflowRequest
    ) -> BlindAlignmentCampaignResult:
        """Calculate the complete typed synthetic campaign result.

        Parameters
        ----------
        request
            Typed specification, authenticated baseline, and explicit provenance.

        Returns
        -------
        BlindAlignmentCampaignResult
            Complete semantic result ready for canonical serialization.

        Raises
        ------
        TypeError
            If the request has the wrong public type or a case disposition violates its
            declared campaign role.
        ValueError
            If authored controls are dimensionally inconsistent or expected stopping
            boundaries are not reached.
        """
        if not isinstance(request, BlindAlignmentCampaignWorkflowRequest):
            raise TypeError("request must be BlindAlignmentCampaignWorkflowRequest")
        specification = request.specification
        baseline = request.baseline
        exact = tuple(
            self._require_success(
                self._run(
                    self._construct(
                        baseline,
                        case.identifier,
                        case.defect_id,
                        case.spin_count,
                        case.minimum_anchor_singular_value,
                        0.0,
                        0,
                        specification.core_radius_cells,
                    ),
                    specification,
                    baseline.cell_count,
                )
            )
            for case in specification.exact_cases
        )
        noise = specification.noise_sweep
        noise_results = tuple(
            BlindAlignmentNoiseCaseResult(
                case=self._require_success(
                    self._run(
                        self._construct(
                            baseline,
                            f"{noise.identifier}-{radians:.1e}",
                            noise.defect_id,
                            noise.spin_count,
                            noise.minimum_anchor_singular_value,
                            radians,
                            noise.generator_seed,
                            specification.core_radius_cells,
                        ),
                        specification,
                        baseline.cell_count,
                    )
                ),
                unitary_noise_radians=radians,
            )
            for radians in noise.unitary_noise_radians
        )
        return BlindAlignmentCampaignResult(
            experiment_id=specification.experiment_id,
            information_boundary=self._information_boundary(specification),
            policy=specification.policy,
            core_radius_cells=specification.core_radius_cells,
            exact_full_rank_cases=exact,
            noise_sweep=noise_results,
            gauge_equivalent_case=self._gauge(specification, baseline),
            stopping_cases=self._stopping_controls(specification, baseline),
            debugging_diagnostics=self._diagnostics(specification, baseline),
            source_identities=baseline.source_identities,
            error_accounting=self._error_accounting(),
            limitations=self._limitations(),
            provenance=request.provenance,
        )

    @staticmethod
    def _construct(
        baseline: BlindAlignmentBaselineData,
        identifier: str,
        defect_id: str,
        spin_count: int,
        minimum_anchor_singular_value: float,
        unitary_noise_radians: float,
        generator_seed: int,
        core_radius_cells: int,
    ) -> BlindAlignmentObservationConstructionResult:
        """Construct one full-dimensional observation and separate hidden truth."""
        return BlindAlignmentObservationConstructor().execute(
            BlindAlignmentObservationConstructionRequest(
                baseline=baseline,
                identifier=identifier,
                defect_id=defect_id,
                spin_count=spin_count,
                minimum_anchor_singular_value=minimum_anchor_singular_value,
                unitary_noise_radians=unitary_noise_radians,
                generator_seed=generator_seed,
                core_radius_cells=core_radius_cells,
            )
        )

    @staticmethod
    def _run(
        construction: BlindAlignmentObservationConstructionResult,
        specification: BlindAlignmentCampaignInput,
        cell_count: int,
        *,
        route: str = "ordinary",
    ) -> BlindAlignmentCaseExecutionResult:
        """Execute one ordinary or explicitly reconciled case."""
        inference_route: BlindAlignmentInferenceRoute
        if route == "ordinary":
            inference_route = "ordinary"
        elif route == "reconciled_partial":
            inference_route = "reconciled_partial"
        else:
            raise ValueError("unsupported workflow inference route")
        return BlindAlignmentCaseExecutionActionizer().execute(
            BlindAlignmentCaseExecutionRequest(
                construction=construction,
                policy=specification.policy,
                cell_count=cell_count,
                eigenvalue_degeneracy_tolerance=specification.algebraic_tolerance,
                inference_route=inference_route,
            )
        )

    def _gauge(
        self,
        specification: BlindAlignmentCampaignInput,
        baseline: BlindAlignmentBaselineData,
    ) -> BlindAlignmentGaugeCaseResult:
        """Calculate identified-sector recovery and completion nonuniqueness."""
        case = specification.gauge_case
        base = self._construct(
            baseline,
            case.identifier,
            case.defect_id,
            case.spin_count,
            case.minimum_nonzero_anchor_singular_value,
            0.0,
            0,
            specification.core_radius_cells,
        )
        observation = base.observation
        dimension = observation.reference_operator.basis.dimension
        active_dimension = case.identified_site_count * 2 * case.spin_count
        if active_dimension >= dimension:
            raise ValueError("gauge case must leave a nonempty complement")
        singular = np.zeros(dimension)
        singular[:active_dimension] = np.linspace(
            1.0,
            case.minimum_nonzero_anchor_singular_value,
            active_dimension,
        )
        transform = base.hidden_truth.candidate_to_reference
        partial = self._replace(
            base,
            anchor_cross_covariance=np.diag(singular) @ transform,
            allow_partial_alignment=True,
        )
        execution = self._run(partial, specification, baseline.cell_count)
        successful = self._require_success(execution)
        inference = execution.inference
        if inference.reference_projector is None:
            raise ValueError("gauge case must return an identified projector")
        projector = inference.reference_projector
        complement = np.eye(dimension) - projector
        values, vectors = np.linalg.eigh(complement)
        complement_basis = vectors[:, values > 0.5]
        complement_noise = self._unitary_noise(
            complement_basis.shape[1],
            case.complement_rotation_radians,
            case.generator_seed,
        )
        complement_rotation = (
            projector + complement_basis @ complement_noise @ complement_basis.conj().T
        )
        candidate = observation.candidate_operator.matrix
        host = observation.reference_operator.matrix
        identity = np.eye(dimension)
        first_completion = transform
        second_completion = complement_rotation @ transform
        first_extraction = (
            first_completion
            @ (candidate - baseline.energy_shift * identity)
            @ first_completion.conj().T
            - host
        )
        second_extraction = (
            second_completion
            @ (candidate - baseline.energy_shift * identity)
            @ second_completion.conj().T
            - host
        )
        return BlindAlignmentGaugeCaseResult(
            case=successful,
            identified_dimension=active_dimension,
            unidentified_complement_dimension=dimension - active_dimension,
            full_completion_extraction_disagreement=self._norm(
                first_extraction - second_extraction
            ),
            compressed_completion_extraction_disagreement=self._norm(
                projector @ (first_extraction - second_extraction) @ projector
            ),
            partial_map_agreement_between_completions=self._norm(
                projector @ first_completion - projector @ second_completion
            ),
        )

    def _stopping_controls(
        self,
        specification: BlindAlignmentCampaignInput,
        baseline: BlindAlignmentBaselineData,
    ) -> tuple[BlindAlignmentStoppingControlResult, ...]:
        """Calculate all authored structured negative controls."""
        return tuple(
            BlindAlignmentStoppingControlResult(
                case.kind,
                self._require_stop(
                    self._run(
                        self._stopping_construction(case, specification, baseline),
                        specification,
                        baseline.cell_count,
                    )
                ),
            )
            for case in specification.stopping_cases
        )

    def _stopping_construction(
        self,
        case: BlindAlignmentStoppingCase,
        specification: BlindAlignmentCampaignInput,
        baseline: BlindAlignmentBaselineData,
    ) -> BlindAlignmentObservationConstructionResult:
        """Construct one kind-specific negative-control observation."""
        base = self._construct(
            baseline,
            case.identifier,
            "orbital-onsite",
            1,
            0.75,
            0.0,
            0,
            specification.core_radius_cells,
        )
        observation = base.observation
        dimension = observation.reference_operator.basis.dimension
        if case.kind == "anchor-condition":
            if not isinstance(case.numeric_value, float):
                raise TypeError("anchor-condition value must be a float")
            anchors = (
                np.diag(np.linspace(1.0, case.numeric_value, dimension))
                @ baseline.candidate_to_reference_spinless
            )
            return self._replace(base, anchor_cross_covariance=anchors)
        if case.kind == "principal-angle":
            if not isinstance(case.numeric_value, float):
                raise TypeError("principal-angle value must be a float")
            singular = np.ones(dimension)
            singular[-1] = np.cos(case.numeric_value)
            return self._replace(base, retained_subspace_overlap=np.diag(singular))
        if case.kind == "rank-mismatch":
            if type(case.numeric_value) is not int:
                raise TypeError("rank mismatch value must be an integer")
            candidate_dimension = dimension + case.numeric_value
            candidate_matrix = observation.candidate_operator.matrix[
                :candidate_dimension, :candidate_dimension
            ]
            candidate_basis = self._reduced_basis(
                observation.candidate_operator.basis,
                candidate_dimension,
                "rank-mismatched-candidate",
            )
            return self._replace(
                base,
                candidate_operator=RepresentedOperator(
                    observation.candidate_operator.identifier,
                    candidate_basis,
                    candidate_matrix,
                ),
                anchor_cross_covariance=observation.anchor_cross_covariance[
                    :, :candidate_dimension
                ],
                retained_subspace_overlap=observation.retained_subspace_overlap[
                    :, :candidate_dimension
                ],
            )
        if case.kind == "spin-mismatch":
            if type(case.numeric_value) is not int:
                raise TypeError("spin mismatch value must be an integer")
            basis = observation.candidate_operator.basis
            mismatched_basis = SupercellBasis(
                state_space_id=basis.state_space_id,
                cell_count=basis.cell_count // case.numeric_value,
                orbital_count=basis.orbital_count,
                spin_count=case.numeric_value,
                reduced_momentum=basis.reduced_momentum,
                site_ordering=basis.site_ordering,
                orbital_ordering=basis.orbital_ordering,
                spin_ordering="up-down-fast",
                coordinate_frame=basis.coordinate_frame,
                energy_unit=basis.energy_unit,
                energy_reference=basis.energy_reference,
                geometry_id=basis.geometry_id,
                subspace_id=basis.subspace_id,
            )
            return self._replace(
                base,
                candidate_operator=RepresentedOperator(
                    observation.candidate_operator.identifier,
                    mismatched_basis,
                    observation.candidate_operator.matrix,
                ),
            )
        if case.kind == "energy-anchor":
            return self._replace(
                base,
                exterior_energy_anchor=np.zeros(
                    (dimension, dimension), dtype=np.complex128
                ),
            )
        raise ValueError("unsupported stopping-control kind")

    def _diagnostics(
        self,
        specification: BlindAlignmentCampaignInput,
        baseline: BlindAlignmentBaselineData,
    ) -> BlindAlignmentDiagnosticSuiteResult:
        """Calculate neighboring probes for every structured stopping boundary."""
        controls = specification.diagnostics
        conditioning = tuple(
            self._conditioning_diagnostic(
                minimum,
                controls.conditioning_additive_anchor_noise,
                controls.conditioning_noise_seed,
                specification,
                baseline,
            )
            for minimum in controls.conditioning_minimum_singular_values
        )
        angles = tuple(
            self._angle_diagnostic(angle, specification, baseline)
            for angle in controls.principal_angle_radians
        )
        energy = tuple(
            self._energy_diagnostic(rank, specification, baseline)
            for rank in controls.energy_anchor_ranks
        )
        return BlindAlignmentDiagnosticSuiteResult(
            conditioning_boundary=conditioning,
            principal_angle_boundary=angles,
            rank_reconciliation=self._rank_diagnostic(
                controls.rank_drop, specification, baseline
            ),
            spin_reconciliation=self._spin_diagnostic(specification, baseline),
            energy_anchor_boundary=energy,
            interpretation=(
                "Neighboring admissible probes diagnose the stopping boundaries; "
                "they do not weaken or replace the original negative controls."
            ),
        )

    def _conditioning_diagnostic(
        self,
        minimum: float,
        additive_norm: float,
        seed: int,
        specification: BlindAlignmentCampaignInput,
        baseline: BlindAlignmentBaselineData,
    ) -> BlindAlignmentConditioningDiagnosticResult:
        """Calculate one additive-noise conditioning-boundary probe."""
        identifier = f"conditioning-{minimum:.1e}"
        base = self._construct(
            baseline,
            identifier,
            "orbital-onsite",
            1,
            minimum,
            0.0,
            0,
            specification.core_radius_cells,
        )
        dimension = base.observation.reference_operator.basis.dimension
        noise = self._normalized_complex_noise(dimension, dimension, seed)
        modified = self._replace(
            base,
            anchor_cross_covariance=(
                base.observation.anchor_cross_covariance + additive_norm * noise
            ),
        )
        return BlindAlignmentConditioningDiagnosticResult(
            outcome=self._run(modified, specification, baseline.cell_count).outcome,
            requested_minimum_anchor_singular_value=minimum,
            additive_anchor_noise_spectral_norm=additive_norm,
        )

    def _angle_diagnostic(
        self,
        angle: float,
        specification: BlindAlignmentCampaignInput,
        baseline: BlindAlignmentBaselineData,
    ) -> BlindAlignmentPrincipalAngleDiagnosticResult:
        """Calculate one retained-subspace principal-angle boundary probe."""
        identifier = f"principal-angle-{angle:.2f}"
        base = self._construct(
            baseline,
            identifier,
            "orbital-onsite",
            1,
            0.75,
            0.0,
            0,
            specification.core_radius_cells,
        )
        dimension = base.observation.reference_operator.basis.dimension
        singular = np.ones(dimension)
        singular[-1] = np.cos(angle)
        modified = self._replace(base, retained_subspace_overlap=np.diag(singular))
        return BlindAlignmentPrincipalAngleDiagnosticResult(
            outcome=self._run(modified, specification, baseline.cell_count).outcome,
            requested_principal_angle_radians=angle,
            minimum_subspace_overlap_singular_value=float(np.cos(angle)),
            diagnostic_reference_basis_indices=(dimension - 1,),
        )

    def _energy_diagnostic(
        self,
        requested_rank: int,
        specification: BlindAlignmentCampaignInput,
        baseline: BlindAlignmentBaselineData,
    ) -> BlindAlignmentEnergyAnchorDiagnosticResult:
        """Calculate one exterior energy-anchor rank boundary probe."""
        identifier = f"energy-anchor-rank-{requested_rank}"
        base = self._construct(
            baseline,
            identifier,
            "orbital-onsite",
            1,
            0.75,
            0.0,
            0,
            specification.core_radius_cells,
        )
        exterior = base.observation.exterior_energy_anchor
        indices = np.flatnonzero(np.diag(exterior).real > 0.5)
        if requested_rank > indices.size:
            raise ValueError("requested energy-anchor rank exceeds exterior rank")
        anchor = np.zeros_like(exterior)
        selected = indices[:requested_rank]
        anchor[selected, selected] = 1.0
        modified = self._replace(base, exterior_energy_anchor=anchor)
        return BlindAlignmentEnergyAnchorDiagnosticResult(
            outcome=self._run(modified, specification, baseline.cell_count).outcome,
            requested_energy_anchor_rank=requested_rank,
        )

    def _rank_diagnostic(
        self,
        rank_drop: int,
        specification: BlindAlignmentCampaignInput,
        baseline: BlindAlignmentBaselineData,
    ) -> BlindAlignmentRankReconciliationResult:
        """Calculate direct rank stop and explicit rectangular reconciliation."""
        host = baseline.pristine_spinless
        transform = baseline.candidate_to_reference_spinless
        reference_dimension = host.shape[0]
        candidate_dimension = reference_dimension - rank_drop
        if candidate_dimension < 1:
            raise ValueError("rank diagnostic must retain a nonempty sector")
        isometry = transform[:, :candidate_dimension]
        projector = isometry @ isometry.conj().T
        candidate = (
            isometry.conj().T @ host @ isometry
            + baseline.energy_shift * np.eye(candidate_dimension)
        )
        reference_basis = self._flat_basis(
            reference_dimension, "rank-reference", "reference-zero"
        )
        candidate_basis = self._flat_basis(
            candidate_dimension,
            "rank-candidate",
            "candidate-shifted-zero",
        )
        observation = BlindAlignmentObservation(
            identifier="rank-reconciled-partial-isometry",
            reference_operator=RepresentedOperator(
                "rank-reference", reference_basis, host
            ),
            candidate_operator=RepresentedOperator(
                "rank-candidate", candidate_basis, candidate
            ),
            anchor_cross_covariance=(
                isometry @ np.diag(np.linspace(1.0, 0.75, candidate_dimension))
            ),
            retained_subspace_overlap=isometry,
            exterior_energy_anchor=projector,
            allow_partial_alignment=True,
        )
        truth = BlindAlignmentHiddenTruth(
            candidate_to_reference=isometry,
            planted_defect=np.zeros_like(host, dtype=np.complex128),
            energy_shift=baseline.energy_shift,
        )
        construction = BlindAlignmentObservationConstructionResult(observation, truth)
        direct = BlindAlignmentInferenceActionizer().execute(
            BlindAlignmentInferenceRequest(observation, specification.policy)
        )
        if direct.issue_codes != ("BLIND_ALIGNMENT.RANK_MISMATCH",):
            raise ValueError("direct unequal-rank comparison must stop")
        reconciled = self._run(
            construction,
            specification,
            baseline.cell_count,
            route="reconciled_partial",
        )
        return BlindAlignmentRankReconciliationResult(
            case=self._require_success(reconciled),
            direct_comparison_issue_code=direct.issue_codes[0],
            reference_dimension=reference_dimension,
            candidate_dimension=candidate_dimension,
            dropped_dimension=rank_drop,
            resolution="explicit_rectangular_partial_isometry",
        )

    def _spin_diagnostic(
        self,
        specification: BlindAlignmentCampaignInput,
        baseline: BlindAlignmentBaselineData,
    ) -> BlindAlignmentSpinReconciliationResult:
        """Calculate direct spin mismatch and explicit spinor lift."""
        mismatch = self._construct(
            baseline,
            "spin-mismatch-diagnostic",
            "orbital-onsite",
            1,
            0.75,
            0.0,
            0,
            specification.core_radius_cells,
        )
        basis = mismatch.observation.candidate_operator.basis
        spin_basis = SupercellBasis(
            state_space_id=basis.state_space_id,
            cell_count=basis.cell_count // 2,
            orbital_count=basis.orbital_count,
            spin_count=2,
            reduced_momentum=basis.reduced_momentum,
            site_ordering=basis.site_ordering,
            orbital_ordering=basis.orbital_ordering,
            spin_ordering="up-down-fast",
            coordinate_frame=basis.coordinate_frame,
            energy_unit=basis.energy_unit,
            energy_reference=basis.energy_reference,
            geometry_id=basis.geometry_id,
            subspace_id=basis.subspace_id,
        )
        mismatch = self._replace(
            mismatch,
            candidate_operator=RepresentedOperator(
                mismatch.observation.candidate_operator.identifier,
                spin_basis,
                mismatch.observation.candidate_operator.matrix,
            ),
        )
        direct = BlindAlignmentInferenceActionizer().execute(
            BlindAlignmentInferenceRequest(mismatch.observation, specification.policy)
        )
        if direct.issue_codes != ("BLIND_ALIGNMENT.SPIN_MISMATCH",):
            raise ValueError("direct spin comparison must stop")
        lifted = self._construct(
            baseline,
            "spin-lifted-reconciliation",
            "spin-mixing",
            2,
            0.65,
            0.0,
            0,
            specification.core_radius_cells,
        )
        lifted_result = self._require_success(
            self._run(lifted, specification, baseline.cell_count)
        )
        defect = lifted.hidden_truth.planted_defect
        spatial_dimension = defect.shape[0] // 2
        tensor = defect.reshape(spatial_dimension, 2, spatial_dimension, 2)
        spin_independent = 0.5 * np.einsum("asbs->ab", tensor)
        spin_lift = np.kron(spin_independent, np.eye(2))
        return BlindAlignmentSpinReconciliationResult(
            direct_comparison_issue_code=direct.issue_codes[0],
            resolution="explicit_spin_lift_to_common_spinor_space",
            spin_independent_restriction_residual=self._norm(defect - spin_lift),
            lossless_spin_restriction_available=False,
            lifted_alignment=lifted_result,
        )

    @staticmethod
    def _replace(
        construction: BlindAlignmentObservationConstructionResult,
        *,
        candidate_operator: RepresentedOperator | None = None,
        anchor_cross_covariance: ComplexMatrix | None = None,
        retained_subspace_overlap: ComplexMatrix | None = None,
        exterior_energy_anchor: ComplexMatrix | None = None,
        allow_partial_alignment: bool | None = None,
    ) -> BlindAlignmentObservationConstructionResult:
        """Replace explicitly selected inference-visible observation fields."""
        original = construction.observation
        observation = BlindAlignmentObservation(
            identifier=original.identifier,
            reference_operator=original.reference_operator,
            candidate_operator=(
                original.candidate_operator
                if candidate_operator is None
                else candidate_operator
            ),
            anchor_cross_covariance=(
                original.anchor_cross_covariance
                if anchor_cross_covariance is None
                else anchor_cross_covariance
            ),
            retained_subspace_overlap=(
                original.retained_subspace_overlap
                if retained_subspace_overlap is None
                else retained_subspace_overlap
            ),
            exterior_energy_anchor=(
                original.exterior_energy_anchor
                if exterior_energy_anchor is None
                else exterior_energy_anchor
            ),
            allow_partial_alignment=(
                original.allow_partial_alignment
                if allow_partial_alignment is None
                else allow_partial_alignment
            ),
        )
        return BlindAlignmentObservationConstructionResult(
            observation, construction.hidden_truth
        )

    @staticmethod
    def _flat_basis(
        dimension: int, coordinate_frame: str, energy_reference: str
    ) -> SupercellBasis:
        """Describe a generic finite identified sector of an explicit dimension."""
        return SupercellBasis(
            state_space_id="blind-alignment-identified-sector",
            cell_count=dimension,
            orbital_count=1,
            spin_count=1,
            reduced_momentum=0.0,
            site_ordering="identified-coordinate-order",
            orbital_ordering="single-coordinate",
            spin_ordering="not-applicable",
            coordinate_frame=coordinate_frame,
            energy_unit="E_G",
            energy_reference=energy_reference,
            geometry_id="one-dimensional-supercell-16",
            subspace_id="blind-alignment-diagnostic-sector",
        )

    @staticmethod
    def _reduced_basis(
        original: SupercellBasis, dimension: int, coordinate_frame: str
    ) -> SupercellBasis:
        """Describe one deliberately dimension-reduced mismatch control."""
        return SupercellBasis(
            state_space_id=original.state_space_id,
            cell_count=dimension,
            orbital_count=1,
            spin_count=1,
            reduced_momentum=original.reduced_momentum,
            site_ordering=original.site_ordering,
            orbital_ordering="identified-coordinate",
            spin_ordering="not-applicable",
            coordinate_frame=coordinate_frame,
            energy_unit=original.energy_unit,
            energy_reference=original.energy_reference,
            geometry_id=original.geometry_id,
            subspace_id=original.subspace_id,
        )

    @staticmethod
    def _unitary_noise(dimension: int, radians: float, seed: int) -> ComplexMatrix:
        """Construct deterministic nearest-neighbor Hermitian-generator rotation."""
        if radians == 0.0:
            return np.eye(dimension, dtype=np.complex128)
        generator = np.zeros((dimension, dimension), dtype=np.complex128)
        rng = np.random.default_rng(seed)
        for index in range(dimension - 1):
            value = rng.normal() + 1j * rng.normal()
            generator[index, index + 1] = value
            generator[index + 1, index] = value.conjugate()
        norm = float(np.linalg.norm(generator, 2))
        if norm == 0.0:
            raise ValueError("unitary-noise generator must be nonzero")
        values, vectors = np.linalg.eigh(generator / norm)
        return np.asarray(
            vectors @ np.diag(np.exp(1j * radians * values)) @ vectors.conj().T,
            dtype=np.complex128,
        )

    @staticmethod
    def _normalized_complex_noise(rows: int, columns: int, seed: int) -> ComplexMatrix:
        """Construct deterministic complex noise with unit spectral norm."""
        rng = np.random.default_rng(seed)
        values = rng.normal(size=(rows, columns)) + 1j * rng.normal(
            size=(rows, columns)
        )
        norm = float(np.linalg.norm(values, 2))
        if norm == 0.0:
            raise ValueError("additive anchor noise must be nonzero")
        return np.asarray(values / norm, dtype=np.complex128)

    @staticmethod
    def _require_success(
        execution: BlindAlignmentCaseExecutionResult,
    ) -> BlindAlignmentSuccessfulCaseResult:
        """Require a successful case role and return its flattened outcome."""
        if not isinstance(execution.outcome, BlindAlignmentSuccessfulCaseResult):
            raise ValueError("campaign case expected successful inference")
        return execution.outcome

    @staticmethod
    def _require_stop(
        execution: BlindAlignmentCaseExecutionResult,
    ) -> BlindAlignmentStoppedCaseResult:
        """Require a stopped case role and return its flattened outcome."""
        if not isinstance(execution.outcome, BlindAlignmentStoppedCaseResult):
            raise ValueError("campaign negative control expected a structured stop")
        return execution.outcome

    @staticmethod
    def _norm(matrix: ComplexMatrix) -> float:
        """Return the represented Frobenius norm as a Python float."""
        return float(np.linalg.norm(matrix, "fro"))

    @staticmethod
    def _information_boundary(
        specification: BlindAlignmentCampaignInput,
    ) -> BlindAlignmentInformationBoundary:
        """Construct the fixed version-one inference information declaration."""
        return BlindAlignmentInformationBoundary(
            observation_contract=specification.observation_information,
            inference_inputs=(
                "reference Hamiltonian",
                "candidate Hamiltonian",
                "anchor cross-covariance",
                "retained-subspace overlap",
                "exterior energy anchor",
                "spin-space metadata",
                "frozen inference policy",
            ),
            withheld_from_inference=(
                "authored candidate-to-reference map",
                "authored scalar energy shift",
                "planted defect operator",
                "authored translation, orbital, phase, and spin parameters",
            ),
            oracle_use="Post hoc evaluation only.",
        )

    @staticmethod
    def _error_accounting() -> tuple[tuple[str, str], ...]:
        """Return deterministic distinct version-one error-channel declarations."""
        return tuple(
            sorted(
                {
                    "observation_error": (
                        "Controlled by the authored unitary perturbation of the anchor "
                        "cross-covariance and reported independently."
                    ),
                    "alignment_error": (
                        "Reported against the hidden map only after inference."
                    ),
                    "energy_reference_error": (
                        "Reported separately from unitary-map and extraction errors."
                    ),
                    "extraction_error": (
                        "Reported against the planted full or compressed operator."
                    ),
                    "model_class_error": (
                        "Reported as a distinct onsite-class residual for every "
                        "successful extraction."
                    ),
                    "scientific_validation": "Not performed.",
                    "uncertainty_quantification": "Not performed.",
                }.items()
            )
        )

    @staticmethod
    def _limitations() -> tuple[str, ...]:
        """Return fixed version-one scientific and evidentiary limitations."""
        return (
            "All observations, defects, and hidden maps are synthetic.",
            (
                "The cross-covariance and subspace-overlap records are authored "
                "observables rather than outputs of independent electronic-structure "
                "calculations."
            ),
            (
                "Partial alignment establishes only compressed active-sector "
                "recovery; no full operator is identified on the anchor-null "
                "complement."
            ),
            (
                "No silicon, dopant, DFT, production Wannier, scientific-validation, "
                "transferability, or UQ claim is made."
            ),
        )
