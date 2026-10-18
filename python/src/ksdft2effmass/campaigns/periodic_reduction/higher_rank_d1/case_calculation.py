"""Pure calculation of one higher-rank D1 rank/depth case."""

from __future__ import annotations

import math

import numpy as np
from projectkoios.numerics.finite_periodic.meshes import CenteredUniformMesh
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array
from projectkoios.numerics.numpy.validation import immutable_complex128_array
from projectkoios.physkit.solidstate.tb import (
    FinitePeriodicMatrixFourierSeries,
    FinitePeriodicMatrixFourierTensorEvaluator,
    FinitePeriodicMatrixFourierTransformer,
    FinitePeriodicMatrixHermiticityAnalyzer,
    FinitePeriodicMatrixParsevalAnalyzer,
    FinitePeriodicMatrixSamples,
)
from projectkoios.physkit.units import Unitless

from ksdft2effmass.analysis.matrix_field.diagnostics import (
    FourierMatrixBlockNormInventoryAnalyzer1D,
    MatrixErrorDecompositionAnalyzer,
    MatrixFieldComparisonAnalyzer,
    MatrixFieldComparisonDiagnostics,
    MatrixFieldHermiticityAnalyzer,
    MatrixFieldIsometryAnalyzer,
    MatrixProjectorFieldAnalyzer,
    ScalarRefinementAnalyzer,
    SymmetricRangeTailAnalyzer1D,
)
from ksdft2effmass.analysis.pareto import SampledParetoClassifier

from .alignment import (
    HigherRankD1A1NumericallyUnresolvedSelection,
    HigherRankD1A1QualifiedSelection,
    HigherRankD1A1RankDeficientSelection,
    HigherRankD1A1Selection,
    HigherRankD1A2NumericallyUnresolvedSelection,
    HigherRankD1A2RankDeficientSelection,
    HigherRankD1A2Selection,
    HigherRankD1A2SelectionResult,
    HigherRankD1AlignmentSelector,
)
from .definition import (
    CHANNELS,
    CONSTRUCTION_MESH_SIZES,
    EVALUATION_MESH_SIZE,
    EXACT_ISOLATION,
    FINAL_CONSTRUCTION_MESH_SIZE,
    SUPPORTS,
    HigherRankD1CaseDefinition,
)
from .model import HigherRankD1ModelConstructor, HigherRankD1SampledFields
from .numerical_backend import (
    HigherRankD1AlignmentBackendError,
    HigherRankD1NumericalExceptionHandler,
    HigherRankD1TransportBackendError,
)
from .records import (
    HigherRankD1BlockNorm,
    HigherRankD1CaseResult,
    HigherRankD1ChannelMeshDiagnostics,
    HigherRankD1ChannelMeshRecord,
    HigherRankD1FourierDiagnostics,
    HigherRankD1Gate,
    HigherRankD1InapplicableChannelMeshDiagnostics,
    HigherRankD1MeshDiagnostics,
    HigherRankD1ParetoPoint,
    HigherRankD1RefinementRecord,
    HigherRankD1ResidualSummary,
    HigherRankD1ScalarLedger,
    HigherRankD1ScalarLedgerEntry,
    HigherRankD1SupportDiagnostics,
    HigherRankD1SupportMonotonicity,
    HigherRankD1TailDiagnostics,
)
from .transport import (
    HigherRankD1TransportAnalyzer,
    HigherRankD1TransportDiagnostics,
    HigherRankD1TransportNumericallyUnresolvedDiagnostics,
    HigherRankD1TransportResult,
)


class HigherRankD1CaseCalculator:
    """Calculate one complete case while retaining diagnostics, not mesh tensors."""

    __slots__ = ()

    def execute(
        self,
        definition: HigherRankD1CaseDefinition,
    ) -> HigherRankD1CaseResult:
        """Calculate one complete rank/depth case and every applicable diagnostic."""
        if type(definition) is not HigherRankD1CaseDefinition:
            raise TypeError("definition must be HigherRankD1CaseDefinition")
        constructor = HigherRankD1ModelConstructor()
        selector = HigherRankD1AlignmentSelector()
        final_coordinates = constructor.construction_coordinates(
            FINAL_CONSTRUCTION_MESH_SIZE
        )
        final_fields = constructor.execute(
            definition.rank,
            definition.depth,
            final_coordinates,
        )
        a1: HigherRankD1A1Selection
        try:
            a1 = selector.select_a1(
                final_fields.candidate_frames,
                final_fields.reference_frames,
            )
        except HigherRankD1AlignmentBackendError as error:
            a1 = HigherRankD1A1NumericallyUnresolvedSelection(
                selection_mesh_size=FINAL_CONSTRUCTION_MESH_SIZE,
                exception_code=(
                    HigherRankD1NumericalExceptionHandler.exception_code(error)
                ),
            )
        evaluation_coordinates = constructor.evaluation_coordinates(
            EVALUATION_MESH_SIZE
        )
        evaluation_fields = constructor.execute(
            definition.rank,
            definition.depth,
            evaluation_coordinates,
        )
        disjoint = all(
            np.intersect1d(coordinate, evaluation_coordinates).size == 0
            for coordinate in (
                constructor.construction_coordinates(mesh_size)
                for mesh_size in CONSTRUCTION_MESH_SIZES
            )
        )
        case_gates: tuple[HigherRankD1Gate, ...] = ()
        if isinstance(a1, HigherRankD1A1QualifiedSelection):
            case_gates = (
                HigherRankD1Gate.evaluate(
                    "/alignment_selection/A1/unitarity/passes",
                    a1.unitarity_defect,
                    1.0e-12,
                ),
                HigherRankD1Gate.evaluate(
                    "/alignment_selection/A1/stationarity/passes",
                    a1.stationarity_defect,
                    1.0e-12,
                ),
                HigherRankD1Gate.evaluate(
                    "/alignment_selection/A1/objective_identity/passes",
                    a1.objective_identity_defect,
                    1.0e-12,
                ),
                HigherRankD1Gate.evaluate(
                    "/alignment_selection/A1/positive_semidefinite/passes",
                    a1.positive_semidefinite_defect,
                    1.0e-12,
                ),
            )
        elif isinstance(a1, HigherRankD1A1NumericallyUnresolvedSelection):
            case_gates = (
                HigherRankD1Gate.evaluate(
                    "/alignment_selection/A1/numerical_resolution/passes",
                    1.0,
                    0.0,
                ),
            )
        endpoint_fields = constructor.execute(
            definition.rank,
            definition.depth,
            constructor.positive_endpoint_coordinates(),
        )
        meshes: list[HigherRankD1MeshDiagnostics] = []
        for mesh_size in CONSTRUCTION_MESH_SIZES:
            fields = (
                final_fields
                if mesh_size == FINAL_CONSTRUCTION_MESH_SIZE
                else constructor.execute(
                    definition.rank,
                    definition.depth,
                    constructor.construction_coordinates(mesh_size),
                )
            )
            a2: HigherRankD1A2SelectionResult
            try:
                a2 = selector.select_a2(
                    fields.candidate_frames,
                    fields.reference_frames,
                )
            except HigherRankD1AlignmentBackendError as error:
                a2 = HigherRankD1A2NumericallyUnresolvedSelection(
                    mesh_size=mesh_size,
                    rank=definition.rank,
                    exception_code=(
                        HigherRankD1NumericalExceptionHandler.exception_code(error)
                    ),
                )
            meshes.append(
                self._mesh(
                    definition,
                    fields,
                    endpoint_fields.reference_frames[0],
                    evaluation_coordinates,
                    evaluation_fields,
                    a1,
                    a2,
                    all(gate.passes for gate in case_gates),
                )
            )
        refinement = self._refinement(tuple(meshes))
        failed = (
            tuple(gate.path for gate in case_gates if not gate.passes)
            + tuple(
                gate.path
                for mesh in meshes
                for gate in self._all_gates(mesh)
                if not gate.passes
            )
            + tuple(
                record.path for record in refinement if not record.diagnostics.passes
            )
        )
        return HigherRankD1CaseResult(
            case_id=definition.case_id,
            rank=definition.rank,
            depth=definition.depth,
            exact_isolation=EXACT_ISOLATION,
            exact_attack_angle_bound=constructor.exact_attack_angle_bound(
                definition.rank
            ),
            basis_identifier=definition.basis_identifier,
            energy_unit="E_ref",
            energy_reference="zero-of-P0-formulas",
            evaluation_mesh_size=EVALUATION_MESH_SIZE,
            construction_evaluation_disjoint=disjoint,
            evaluation_noninfluence_confirmed=True,
            a1_selection=a1,
            meshes=tuple(meshes),
            gates=case_gates,
            refinement=refinement,
            failed_gate_paths=failed,
            qualification=self._case_qualification(a1, tuple(meshes), failed),
        )

    def _mesh(
        self,
        definition: HigherRankD1CaseDefinition,
        fields: HigherRankD1SampledFields,
        endpoint_frame: Complex128Array,
        evaluation_coordinates: Float64Array,
        evaluation_fields: HigherRankD1SampledFields,
        a1: HigherRankD1A1Selection,
        a2: HigherRankD1A2SelectionResult,
        case_technical_prerequisites_pass: bool,
    ) -> HigherRankD1MeshDiagnostics:
        mesh_size = int(fields.reduced_coordinates.size)
        rank = definition.rank
        parent_hermiticity = MatrixFieldHermiticityAnalyzer().execute(
            fields.parent_operators, 1.0
        )
        reference_isometry = MatrixFieldIsometryAnalyzer().execute(
            fields.reference_frames
        )
        candidate_isometry = MatrixFieldIsometryAnalyzer().execute(
            fields.candidate_frames
        )
        gauge_isometry = MatrixFieldIsometryAnalyzer().execute(fields.gauges)
        reference_projectors = fields.reference_frames @ np.swapaxes(
            fields.reference_frames.conjugate(), -1, -2
        )
        candidate_projectors = fields.candidate_frames @ np.swapaxes(
            fields.candidate_frames.conjugate(), -1, -2
        )
        reference_projector = MatrixProjectorFieldAnalyzer().execute(
            np.asarray(reference_projectors, dtype=np.complex128)
        )
        candidate_projector = MatrixProjectorFieldAnalyzer().execute(
            np.asarray(candidate_projectors, dtype=np.complex128)
        )
        projector_equality = self._residual(
            np.asarray(
                candidate_projectors - reference_projectors, dtype=np.complex128
            ),
            math.sqrt(rank),
        )
        parent_spectra = np.linalg.eigvalsh(fields.parent_operators)[:, :rank]
        parent_spectrum_difference = np.abs(parent_spectra - fields.retained_energies)
        parent_spectrum_maximum = float(np.max(parent_spectrum_difference))
        parent_spectrum_rms = float(np.sqrt(np.mean(parent_spectrum_difference**2)))
        transport: HigherRankD1TransportResult
        try:
            transport = HigherRankD1TransportAnalyzer().execute(
                fields.reference_frames, endpoint_frame
            )
        except HigherRankD1TransportBackendError as error:
            transport = HigherRankD1TransportNumericallyUnresolvedDiagnostics(
                mesh_size=mesh_size,
                rank=rank,
                stage=error.stage,
                attempted_link_count=error.attempted_link_count,
                exception_code=(
                    HigherRankD1NumericalExceptionHandler.exception_code(error)
                ),
            )
        sampled_isolation = float(
            np.min(
                np.min(fields.exterior_energies, axis=1)
                - np.max(fields.retained_energies, axis=1)
            )
        )
        sampled_angle = HigherRankD1ModelConstructor.sampled_attack_angle_maximum(
            rank, definition.depth, fields.reduced_coordinates
        )
        coordinate_defect = self._coordinate_defect(fields.reduced_coordinates)
        gates = [
            HigherRankD1Gate.evaluate(
                f"/meshes/{mesh_size}/coordinate_construction/passes",
                coordinate_defect,
                1.0e-14,
            ),
            HigherRankD1Gate.evaluate(
                f"/meshes/{mesh_size}/parent_hermiticity/passes",
                parent_hermiticity.normalized_maximum_frobenius_defect,
                1.0e-12,
            ),
            HigherRankD1Gate.evaluate(
                f"/meshes/{mesh_size}/reference_isometry/passes",
                reference_isometry.maximum_frobenius_defect,
                1.0e-12,
            ),
            HigherRankD1Gate.evaluate(
                f"/meshes/{mesh_size}/candidate_isometry/passes",
                candidate_isometry.maximum_frobenius_defect,
                1.0e-12,
            ),
            HigherRankD1Gate.evaluate(
                f"/meshes/{mesh_size}/gauge_unitarity/passes",
                gauge_isometry.maximum_frobenius_defect,
                1.0e-12,
            ),
            HigherRankD1Gate.evaluate(
                f"/meshes/{mesh_size}/projector_idempotency/passes",
                max(
                    reference_projector.maximum_idempotency_frobenius_defect,
                    candidate_projector.maximum_idempotency_frobenius_defect,
                ),
                1.0e-12,
            ),
            HigherRankD1Gate.evaluate(
                f"/meshes/{mesh_size}/projector_equality/passes",
                projector_equality.maximum,
                1.0e-12,
            ),
            HigherRankD1Gate.evaluate(
                f"/meshes/{mesh_size}/parent_retained_spectrum/passes",
                parent_spectrum_maximum,
                1.0e-11,
            ),
        ]
        if isinstance(transport, HigherRankD1TransportDiagnostics):
            gates.extend(
                (
                    HigherRankD1Gate.evaluate(
                        f"/meshes/{mesh_size}/transport_closure/passes",
                        max(
                            transport.endpoint_sewing.frame_defect,
                            transport.endpoint_sewing.projector_defect,
                            transport.primitive_closure_defect,
                            transport.closure_unitarity_defect,
                        ),
                        1.0e-11,
                    ),
                    HigherRankD1Gate.evaluate(
                        f"/meshes/{mesh_size}/transport_phases/passes",
                        max(abs(value) for value in transport.closure_eigenphases),
                        1.0e-10,
                    ),
                )
            )
        else:
            gates.append(
                HigherRankD1Gate.evaluate(
                    f"/meshes/{mesh_size}/transport_resolution/passes",
                    1.0,
                    0.0,
                )
            )
        if isinstance(a2, HigherRankD1A2Selection):
            selection_integrity = max(
                a2.unitarity_defect_maximum,
                a2.stationarity_defect_maximum,
                a2.objective_identity_defect_maximum,
                a2.positive_semidefinite_defect_maximum,
            )
            gates.append(
                HigherRankD1Gate.evaluate(
                    f"/meshes/{mesh_size}/a2_integrity/passes",
                    selection_integrity,
                    1.0e-12,
                )
            )
        else:
            gates.append(
                HigherRankD1Gate.evaluate(
                    f"/meshes/{mesh_size}/a2_resolution/passes",
                    1.0,
                    0.0,
                )
            )
        frozen_gates = tuple(gates)
        channels: list[HigherRankD1ChannelMeshRecord] = []
        for channel in CHANNELS:
            if channel == "A1" and not isinstance(a1, HigherRankD1A1QualifiedSelection):
                downstream = (
                    "inapplicable-aggregate-rank-deficient"
                    if isinstance(a1, HigherRankD1A1RankDeficientSelection)
                    else "inapplicable-alignment-numerically-unresolved"
                )
                channels.append(
                    HigherRankD1InapplicableChannelMeshDiagnostics(
                        mesh_size,
                        channel,
                        a1.status,
                        downstream,
                    )
                )
                continue
            if channel == "A2" and not isinstance(a2, HigherRankD1A2Selection):
                downstream = (
                    "inapplicable-pointwise-rank-deficient"
                    if isinstance(a2, HigherRankD1A2RankDeficientSelection)
                    else "inapplicable-alignment-numerically-unresolved"
                )
                channels.append(
                    HigherRankD1InapplicableChannelMeshDiagnostics(
                        mesh_size,
                        channel,
                        a2.status,
                        downstream,
                    )
                )
                continue
            transformation = self._transformations(channel, fields, a1, a2)
            aligned_frames = np.asarray(
                fields.candidate_frames @ transformation, dtype=np.complex128
            )
            aligned_operators = np.asarray(
                np.swapaxes(transformation.conjugate(), -1, -2)
                @ fields.attacked_operators
                @ transformation,
                dtype=np.complex128,
            )
            direct = self._direct_evaluation_field(channel, evaluation_fields, a1)
            channels.append(
                self._channel(
                    definition,
                    mesh_size,
                    fields,
                    evaluation_coordinates,
                    aligned_frames,
                    aligned_operators,
                    direct,
                    channel,
                    a1,
                    case_technical_prerequisites_pass
                    and all(gate.passes for gate in frozen_gates)
                    and (
                        channel != "A1"
                        or not isinstance(a1, HigherRankD1A1QualifiedSelection)
                        or max(
                            a1.unitarity_defect,
                            a1.stationarity_defect,
                            a1.objective_identity_defect,
                            a1.positive_semidefinite_defect,
                        )
                        <= 1.0e-12
                    ),
                )
            )
        return HigherRankD1MeshDiagnostics(
            mesh_size=mesh_size,
            sampled_isolation=sampled_isolation,
            sampled_attack_angle=sampled_angle,
            coordinate_maximum_defect=coordinate_defect,
            parent_hermiticity=parent_hermiticity,
            reference_isometry=reference_isometry,
            candidate_isometry=candidate_isometry,
            gauge_isometry=gauge_isometry,
            reference_projector=reference_projector,
            candidate_projector=candidate_projector,
            projector_equality=projector_equality,
            parent_retained_spectrum_maximum=parent_spectrum_maximum,
            parent_retained_spectrum_rms=parent_spectrum_rms,
            transport=transport,
            a2_selection=a2,
            channels=tuple(channels),
            gates=frozen_gates,
        )

    def _channel(
        self,
        definition: HigherRankD1CaseDefinition,
        mesh_size: int,
        fields: HigherRankD1SampledFields,
        evaluation_coordinates: Float64Array,
        aligned_frames: Complex128Array,
        aligned_operators: Complex128Array,
        direct_evaluation: Complex128Array,
        channel: str,
        a1: HigherRankD1A1Selection,
        technical_prerequisites_pass: bool,
    ) -> HigherRankD1ChannelMeshDiagnostics:
        rank = definition.rank
        frame_residual = self._residual(
            aligned_frames - fields.reference_frames, math.sqrt(rank)
        )
        aligned_projector = aligned_frames @ np.swapaxes(
            aligned_frames.conjugate(), -1, -2
        )
        reference_projector = fields.reference_frames @ np.swapaxes(
            fields.reference_frames.conjugate(), -1, -2
        )
        projector_residual = self._residual(
            np.asarray(aligned_projector - reference_projector, dtype=np.complex128),
            math.sqrt(rank),
        )
        represented = MatrixFieldComparisonAnalyzer().execute(
            aligned_operators,
            fields.reference_operators,
            1.0,
            1.0e-30,
        )
        represented_hermiticity = MatrixFieldHermiticityAnalyzer().execute(
            aligned_operators, 1.0
        )
        samples = FinitePeriodicMatrixSamples.from_array(
            mesh=CenteredUniformMesh(1, mesh_size, (0.0,)),
            matrix_samples=aligned_operators,
            energy_unit=Unitless(),
            energy_reference="D1-E-ref-zero",
            basis_identifier=definition.basis_identifier,
        )
        transform = FinitePeriodicMatrixFourierTransformer().transform(samples)
        evaluator = FinitePeriodicMatrixFourierTensorEvaluator()
        reconstruction = evaluator.evaluate(
            transform.series, (fields.reduced_coordinates,)
        ).matrix_values
        reconstruction_defect = self._residual(
            np.asarray(reconstruction - aligned_operators, dtype=np.complex128),
            math.sqrt(rank),
        ).normalized_maximum
        hermiticity = FinitePeriodicMatrixHermiticityAnalyzer().analyze(transform)
        parseval = FinitePeriodicMatrixParsevalAnalyzer().analyze(transform)
        parseval_scale = max(
            parseval.sample_mean_squared_frobenius_norm.magnitude,
            parseval.coefficient_sum_squared_frobenius_norm.magnitude,
            rank * 1.0e-30,
        )
        relative_parseval = parseval.absolute_defect.magnitude / parseval_scale
        modes = tuple(int(value) for value in transform.series.integer_modes[:, 0])
        expected_modes = tuple(range(-(mesh_size // 2), mesh_size // 2 + 1))
        fourier_gates = (
            HigherRankD1Gate.evaluate(
                f"/meshes/{mesh_size}/channels/{channel}/fourier/reconstruction/passes",
                reconstruction_defect,
                2.0e-11,
            ),
            HigherRankD1Gate.evaluate(
                f"/meshes/{mesh_size}/channels/{channel}/fourier/hermiticity/passes",
                hermiticity.ordinary_maximum_frobenius_defect.magnitude
                / math.sqrt(rank),
                2.0e-11,
            ),
            HigherRankD1Gate.evaluate(
                f"/meshes/{mesh_size}/channels/{channel}/fourier/parseval/passes",
                relative_parseval,
                2.0e-11,
            ),
        )
        fourier = HigherRankD1FourierDiagnostics(
            representative_count=transform.series.term_count,
            representative_inventory_ordered_unique=(
                modes == tuple(sorted(set(modes)))
            ),
            inversion_closed=all(-value in modes for value in modes),
            index_bijection_passes=(modes == expected_modes),
            no_nyquist_disposition="inapplicable-odd-centered-no-nyquist",
            normalized_reconstruction_defect=reconstruction_defect,
            normalized_hermitian_pairing_defect=(
                hermiticity.ordinary_maximum_frobenius_defect.magnitude
                / math.sqrt(rank)
            ),
            sample_mean_squared_frobenius_norm=(
                parseval.sample_mean_squared_frobenius_norm.magnitude
            ),
            coefficient_sum_squared_frobenius_norm=(
                parseval.coefficient_sum_squared_frobenius_norm.magnitude
            ),
            relative_parseval_defect=relative_parseval,
            gates=fourier_gates,
        )
        inventory = FourierMatrixBlockNormInventoryAnalyzer1D().execute(
            transform.series, 128, 1.0
        )
        block_norms = tuple(
            HigherRankD1BlockNorm(
                item.translation,
                item.raw_frobenius_norm,
                item.normalized_frobenius_norm,
            )
            for item in inventory.blocks
        )
        full_evaluation = evaluator.evaluate(
            transform.series, (evaluation_coordinates,)
        ).matrix_values
        interpolation = MatrixFieldComparisonAnalyzer().execute(
            full_evaluation, direct_evaluation, 1.0, 1.0e-30
        )
        supports = self._supports(
            mesh_size,
            channel,
            transform.series,
            fields.reduced_coordinates,
            evaluation_coordinates,
            full_evaluation,
            direct_evaluation,
        )
        channel_gates = list(fourier_gates)
        channel_gates.extend(
            (
                HigherRankD1Gate.evaluate(
                    f"/meshes/{mesh_size}/channels/{channel}/projector/passes",
                    projector_residual.maximum,
                    1.0e-12,
                ),
                HigherRankD1Gate.evaluate(
                    f"/meshes/{mesh_size}/channels/{channel}/spectrum/passes",
                    represented.errors.normalized_ordered_spectrum_maximum,
                    1.0e-11,
                ),
                HigherRankD1Gate.evaluate(
                    f"/meshes/{mesh_size}/channels/{channel}/interpolation_operator/passes",
                    interpolation.errors.normalized_matrix_frobenius_maximum,
                    1.0e-9,
                ),
                HigherRankD1Gate.evaluate(
                    f"/meshes/{mesh_size}/channels/{channel}/interpolation_spectrum/passes",
                    interpolation.errors.normalized_ordered_spectrum_maximum,
                    1.0e-10,
                ),
            )
        )
        if channel in ("A2", "A3"):
            channel_gates.extend(
                (
                    HigherRankD1Gate.evaluate(
                        f"/meshes/{mesh_size}/channels/{channel}/frame_recovery/passes",
                        frame_residual.normalized_maximum,
                        1.0e-11,
                    ),
                    HigherRankD1Gate.evaluate(
                        f"/meshes/{mesh_size}/channels/{channel}/operator_recovery/passes",
                        represented.errors.normalized_matrix_frobenius_maximum,
                        1.0e-11,
                    ),
                )
            )
        for item in supports:
            channel_gates.extend(item.gates)
        pareto_role = "control-only" if channel in ("A2", "A3") else "primary-outcome"
        pareto_points: tuple[HigherRankD1ParetoPoint, ...] = ()
        if (
            mesh_size == FINAL_CONSTRUCTION_MESH_SIZE
            and technical_prerequisites_pass
            and all(gate.passes for gate in channel_gates)
        ):
            objectives = tuple(
                (
                    float(2 * item.support + 1),
                    item.total.errors.normalized_matrix_frobenius_maximum,
                    item.total.errors.normalized_ordered_spectrum_maximum,
                )
                for item in supports
            )
            efficient = SampledParetoClassifier().execute(objectives)
            pareto_points = tuple(
                HigherRankD1ParetoPoint(
                    support=item.support,
                    retained_block_count=2 * item.support + 1,
                    normalized_total_operator_error=(
                        item.total.errors.normalized_matrix_frobenius_maximum
                    ),
                    normalized_total_spectrum_error=(
                        item.total.errors.normalized_ordered_spectrum_maximum
                    ),
                    pareto_efficient=flag,
                )
                for item, flag in zip(supports, efficient, strict=True)
            )
        elif mesh_size == FINAL_CONSTRUCTION_MESH_SIZE:
            pareto_role = "inapplicable-technical-qualification"
        ledger = self._scalar_ledger(block_norms, interpolation, supports)
        return HigherRankD1ChannelMeshDiagnostics(
            channel=channel,
            mesh_size=mesh_size,
            alignment_status="qualified",
            downstream_applicability="applicable",
            frame_residual=frame_residual,
            projector_residual=projector_residual,
            represented_operator=represented,
            represented_hermiticity=represented_hermiticity,
            fourier=fourier,
            block_norms=block_norms,
            interpolation=interpolation,
            supports=supports,
            pareto_role=(
                pareto_role
                if mesh_size == FINAL_CONSTRUCTION_MESH_SIZE
                else "not-final-mesh"
            ),
            pareto_points=pareto_points,
            scalar_ledger=ledger,
            gates=tuple(channel_gates),
        )

    def _supports(
        self,
        mesh_size: int,
        channel: str,
        series: FinitePeriodicMatrixFourierSeries,
        construction_coordinates: Float64Array,
        evaluation_coordinates: Float64Array,
        full_evaluation: Complex128Array,
        direct_evaluation: Complex128Array,
    ) -> tuple[HigherRankD1SupportDiagnostics, ...]:
        evaluator = FinitePeriodicMatrixFourierTensorEvaluator()
        results: list[HigherRankD1SupportDiagnostics] = []
        previous_tail: HigherRankD1TailDiagnostics | None = None
        previous_support: int | None = None
        for support in SUPPORTS:
            indices = tuple(
                int(index)
                for index in np.flatnonzero(
                    np.abs(series.integer_modes[:, 0]) <= support
                )
            )
            selected = series.take(indices)
            omitted_indices = tuple(
                index for index in range(series.term_count) if index not in indices
            )
            omitted = series.take(omitted_indices)
            omitted_construction = evaluator.evaluate(
                omitted, (construction_coordinates,)
            ).matrix_values
            truncated_evaluation = evaluator.evaluate(
                selected, (evaluation_coordinates,)
            ).matrix_values
            tail_source = SymmetricRangeTailAnalyzer1D().execute(series, support, 1.0)
            tail = HigherRankD1TailDiagnostics(
                squared_weight=tail_source.omitted_squared_frobenius_weight,
                l2_norm=tail_source.omitted_frobenius_l2_norm,
                block_l1_norm=tail_source.omitted_block_l1_norm,
                normalized_squared_weight=(
                    tail_source.normalized_omitted_squared_frobenius_weight
                ),
                normalized_l2_norm=(tail_source.normalized_omitted_frobenius_l2_norm),
                normalized_block_l1_norm=(tail_source.normalized_omitted_block_l1_norm),
            )
            parseval_left = float(
                np.mean(np.linalg.norm(omitted_construction, axis=(-2, -1)) ** 2)
            )
            parseval_right = tail.squared_weight
            parseval_relative = abs(parseval_left - parseval_right) / max(
                parseval_left,
                parseval_right,
                series.matrix_size * 1.0e-30,
            )
            truncation = MatrixFieldComparisonAnalyzer().execute(
                truncated_evaluation, full_evaluation, 1.0, 1.0e-30
            )
            total = MatrixFieldComparisonAnalyzer().execute(
                truncated_evaluation, direct_evaluation, 1.0, 1.0e-30
            )
            interpolation_error = np.asarray(
                full_evaluation - direct_evaluation, dtype=np.complex128
            )
            truncation_error = np.asarray(
                truncated_evaluation - full_evaluation, dtype=np.complex128
            )
            total_error = np.asarray(
                truncated_evaluation - direct_evaluation, dtype=np.complex128
            )
            decomposition = MatrixErrorDecompositionAnalyzer().execute(
                interpolation_error, truncation_error, total_error, 1.0
            )
            monotonicity: tuple[HigherRankD1SupportMonotonicity, ...] = ()
            if previous_tail is not None and previous_support is not None:
                increases = (
                    max(
                        0.0,
                        tail.normalized_squared_weight
                        - previous_tail.normalized_squared_weight,
                    ),
                    max(
                        0.0,
                        tail.normalized_l2_norm - previous_tail.normalized_l2_norm,
                    ),
                    max(
                        0.0,
                        tail.normalized_block_l1_norm
                        - previous_tail.normalized_block_l1_norm,
                    ),
                )
                monotonicity = (
                    HigherRankD1SupportMonotonicity(
                        previous_support,
                        increases[0],
                        increases[1],
                        increases[2],
                        max(increases) <= 2.0e-11,
                    ),
                )
            gates = (
                HigherRankD1Gate.evaluate(
                    f"/meshes/{mesh_size}/channels/{channel}/supports/{support}/parseval/passes",
                    parseval_relative,
                    2.0e-11,
                ),
                HigherRankD1Gate.evaluate(
                    f"/meshes/{mesh_size}/channels/{channel}/supports/{support}/decomposition/passes",
                    decomposition.normalized_maximum_frobenius_defect,
                    2.0e-11,
                ),
                HigherRankD1Gate.evaluate(
                    f"/meshes/{mesh_size}/channels/{channel}/supports/{support}/bounds/passes",
                    max(
                        truncation.perturbation_bounds.normalized_maximum_ordered_spectrum_minus_spectral_norm,
                        truncation.perturbation_bounds.normalized_maximum_ordered_spectrum_minus_frobenius_norm,
                        truncation.perturbation_bounds.normalized_maximum_spectral_norm_minus_frobenius_norm,
                        total.perturbation_bounds.normalized_maximum_ordered_spectrum_minus_spectral_norm,
                        total.perturbation_bounds.normalized_maximum_ordered_spectrum_minus_frobenius_norm,
                        total.perturbation_bounds.normalized_maximum_spectral_norm_minus_frobenius_norm,
                    ),
                    1.0e-11,
                ),
                HigherRankD1Gate.evaluate(
                    f"/meshes/{mesh_size}/channels/{channel}/supports/{support}/monotonicity/passes",
                    (
                        0.0
                        if not monotonicity
                        else max(
                            monotonicity[0].normalized_squared_weight_increase,
                            monotonicity[0].normalized_l2_norm_increase,
                            monotonicity[0].normalized_l1_norm_increase,
                        )
                    ),
                    2.0e-11,
                ),
            )
            results.append(
                HigherRankD1SupportDiagnostics(
                    support=support,
                    translations=tuple(range(-support, support + 1)),
                    tail=tail,
                    monotonicity=monotonicity,
                    sample_parseval_left=parseval_left,
                    sample_parseval_right=parseval_right,
                    relative_parseval_defect=parseval_relative,
                    truncation=truncation,
                    total=total,
                    decomposition=decomposition,
                    gates=gates,
                )
            )
            previous_tail = tail
            previous_support = support
        return tuple(results)

    def _refinement(
        self,
        meshes: tuple[HigherRankD1MeshDiagnostics, ...],
    ) -> tuple[HigherRankD1RefinementRecord, ...]:
        coarse_mesh = meshes[-2]
        fine_mesh = meshes[-1]
        coarse = self._mesh_ledger(coarse_mesh)
        fine = self._mesh_ledger(fine_mesh)
        fine_paths = frozenset(fine.paths)
        common_paths = tuple(path for path in coarse.paths if path in fine_paths)
        analyzer = ScalarRefinementAnalyzer()
        return tuple(
            HigherRankD1RefinementRecord(
                path,
                analyzer.execute(
                    coarse_mesh.mesh_size,
                    fine_mesh.mesh_size,
                    coarse.value(path),
                    fine.value(path),
                    1.0e-30,
                    1.0e-10,
                    1.0e-6,
                ),
            )
            for path in common_paths
        )

    @staticmethod
    def _mesh_ledger(
        mesh: HigherRankD1MeshDiagnostics,
    ) -> HigherRankD1ScalarLedger:
        return HigherRankD1ScalarLedger(
            tuple(
                entry
                for channel in mesh.channels
                if isinstance(channel, HigherRankD1ChannelMeshDiagnostics)
                for entry in channel.scalar_ledger.with_prefix(
                    f"/channels/{channel.channel}"
                ).entries
            )
        )

    @staticmethod
    def _scalar_ledger(
        blocks: tuple[HigherRankD1BlockNorm, ...],
        interpolation: MatrixFieldComparisonDiagnostics,
        supports: tuple[HigherRankD1SupportDiagnostics, ...],
    ) -> HigherRankD1ScalarLedger:
        interpolation_errors = interpolation.errors
        values: list[HigherRankD1ScalarLedgerEntry] = [
            HigherRankD1ScalarLedgerEntry(
                "/interpolation/normalized_operator_maximum",
                interpolation_errors.normalized_matrix_frobenius_maximum,
            ),
            HigherRankD1ScalarLedgerEntry(
                "/interpolation/normalized_spectrum_maximum",
                interpolation_errors.normalized_ordered_spectrum_maximum,
            ),
        ]
        values.extend(
            HigherRankD1ScalarLedgerEntry(
                f"/blocks/{block.translation:+d}",
                block.normalized_frobenius_norm,
            )
            for block in blocks
        )
        for item in supports:
            prefix = f"/supports/{item.support}"
            values.extend(
                (
                    HigherRankD1ScalarLedgerEntry(
                        f"{prefix}/tail_w", item.tail.normalized_squared_weight
                    ),
                    HigherRankD1ScalarLedgerEntry(
                        f"{prefix}/tail_n", item.tail.normalized_l2_norm
                    ),
                    HigherRankD1ScalarLedgerEntry(
                        f"{prefix}/tail_l", item.tail.normalized_block_l1_norm
                    ),
                    HigherRankD1ScalarLedgerEntry(
                        f"{prefix}/truncation_operator_maximum",
                        item.truncation.errors.normalized_matrix_frobenius_maximum,
                    ),
                    HigherRankD1ScalarLedgerEntry(
                        f"{prefix}/truncation_spectrum_maximum",
                        item.truncation.errors.normalized_ordered_spectrum_maximum,
                    ),
                    HigherRankD1ScalarLedgerEntry(
                        f"{prefix}/total_operator_maximum",
                        item.total.errors.normalized_matrix_frobenius_maximum,
                    ),
                    HigherRankD1ScalarLedgerEntry(
                        f"{prefix}/total_spectrum_maximum",
                        item.total.errors.normalized_ordered_spectrum_maximum,
                    ),
                    HigherRankD1ScalarLedgerEntry(
                        f"{prefix}/parseval", item.relative_parseval_defect
                    ),
                    HigherRankD1ScalarLedgerEntry(
                        f"{prefix}/decomposition",
                        item.decomposition.normalized_maximum_frobenius_defect,
                    ),
                )
            )
        return HigherRankD1ScalarLedger(tuple(values))

    @staticmethod
    def _transformations(
        channel: str,
        fields: HigherRankD1SampledFields,
        a1: HigherRankD1A1Selection,
        a2: HigherRankD1A2SelectionResult,
    ) -> Complex128Array:
        rank = fields.rank
        mesh_size = int(fields.reduced_coordinates.size)
        if channel == "A0":
            return np.broadcast_to(
                np.eye(rank, dtype=np.complex128), (mesh_size, rank, rank)
            )
        if channel == "A1":
            if type(a1) is not HigherRankD1A1QualifiedSelection:
                raise ValueError("A1 transformation is inapplicable")
            return np.broadcast_to(a1.transformation, (mesh_size, rank, rank))
        if channel == "A2":
            if not isinstance(a2, HigherRankD1A2Selection):
                raise ValueError("A2 transformation is inapplicable")
            return a2.transformations
        if channel == "A3":
            return np.swapaxes(fields.gauges.conjugate(), -1, -2)
        raise ValueError("unknown channel")

    @staticmethod
    def _direct_evaluation_field(
        channel: str,
        evaluation: HigherRankD1SampledFields,
        a1: HigherRankD1A1Selection,
    ) -> Complex128Array:
        if channel == "A0":
            return evaluation.attacked_operators
        if channel == "A1":
            if type(a1) is not HigherRankD1A1QualifiedSelection:
                raise ValueError("A1 direct field is inapplicable")
            unitary = a1.transformation
            values = np.asarray(
                unitary.conjugate().T @ evaluation.attacked_operators @ unitary,
                dtype=np.complex128,
            )
            return immutable_complex128_array(values, "a1_direct_evaluation")
        if channel in ("A2", "A3"):
            return evaluation.reference_operators
        raise ValueError("unknown channel")

    @staticmethod
    def _residual(
        values: Complex128Array, normalization: float
    ) -> HigherRankD1ResidualSummary:
        norms = np.asarray(np.linalg.norm(values, axis=(-2, -1)), dtype=np.float64)
        maximum = float(np.max(norms))
        rms = float(np.sqrt(np.mean(norms**2)))
        return HigherRankD1ResidualSummary(
            maximum,
            rms,
            maximum / normalization,
            rms / normalization,
            normalization,
        )

    @staticmethod
    def _coordinate_defect(coordinates: Float64Array) -> float:
        mesh_size = int(coordinates.size)
        expected = -0.5 + np.arange(mesh_size, dtype=np.float64) / float(mesh_size)
        return float(np.max(np.abs(coordinates - expected)))

    @staticmethod
    def _case_qualification(
        a1: HigherRankD1A1Selection,
        meshes: tuple[HigherRankD1MeshDiagnostics, ...],
        failed_gate_paths: tuple[str, ...],
    ) -> str:
        numerically_unresolved = isinstance(
            a1, HigherRankD1A1NumericallyUnresolvedSelection
        ) or any(
            isinstance(
                mesh.a2_selection,
                HigherRankD1A2NumericallyUnresolvedSelection,
            )
            or isinstance(
                mesh.transport,
                HigherRankD1TransportNumericallyUnresolvedDiagnostics,
            )
            for mesh in meshes
        )
        if numerically_unresolved:
            return "numerically-unresolved"
        if failed_gate_paths:
            return "invalid-mandatory-gate"
        return "qualified"

    @staticmethod
    def _all_gates(mesh: HigherRankD1MeshDiagnostics) -> tuple[HigherRankD1Gate, ...]:
        channel_gates = tuple(
            gate
            for channel in mesh.channels
            if isinstance(channel, HigherRankD1ChannelMeshDiagnostics)
            for gate in channel.gates
        )
        return mesh.gates + channel_gates


__all__ = ["HigherRankD1CaseCalculator"]
