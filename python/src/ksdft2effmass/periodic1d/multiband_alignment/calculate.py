"""Calculation Action for controlled multiband alignment and locality."""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

from ksdft2effmass.analysis.hopping_diagnostics import (
    BlockHoppingHermiticityAnalyzer1D,
)
from ksdft2effmass.analysis.periodic_bands import (
    BandApproximationErrorAnalyzer1D,
    BandApproximationErrorResult1D,
    BandSpectrumSamples1D,
)
from ksdft2effmass.operators import (
    MODEL_SYSTEM_UNIT_CONVERTER,
    ComplexMatrixQuantity,
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.solid_state import (
    BandFrameAligner1D,
    BandProjectedOperatorPathConstructor1D,
    BlockHoppingInterpolator1D,
    BlockHoppingModel1D,
    BlockHoppingTruncator1D,
    CenteredUniformReciprocalMesh1D,
    PolarBandFrameTransporter1D,
    ReciprocalBandFramePath1D,
    ReciprocalOperatorFourierTransformer1D,
    ReciprocalOperatorSamples1D,
)

from .definition import Periodic1DMultibandAlignmentCalculationDefinition
from .results import (
    Periodic1DMultibandAlignmentCalculationResult,
    Periodic1DMultibandAlignmentDiagnostics,
    Periodic1DMultibandAlignmentRangeResult,
)


class Periodic1DMultibandAlignmentCalculator:
    """Compose parent, frame, alignment, projection, and hopping Actions.

    The deterministic in-process calculation uses no external calculator and
    defines no material or scientific acceptance policy.  Pointwise Procrustes
    recovery and the separately constrained global-unitary family are retained
    as distinct channels.
    """

    __slots__ = ()

    def execute(
        self, definition: Periodic1DMultibandAlignmentCalculationDefinition
    ) -> Periodic1DMultibandAlignmentCalculationResult:
        """Calculate the frozen rank-two frame, alignment, and locality channels.

        Parameters
        ----------
        definition
            Exact M2 controls.  The parent uses one identified internal state space and
            energy unit; reduced momenta are dimensionless.

        Returns
        -------
        Periodic1DMultibandAlignmentCalculationResult
            Correlated invariant, pointwise, globally constrained, transform,
            Hermiticity, and finite-range evidence.

        Raises
        ------
        TypeError
            If ``definition`` is not the exact M2 definition type.
        ValueError
            If the finite parent gap, frame transport, units, or correlations violate
            the frozen controls.

        Notes
        -----
        Pointwise Procrustes alignment and the one-global-unitary channel are distinct
        feasible families.  Staggered evaluation data are diagnostic only.
        """
        if type(definition) is not Periodic1DMultibandAlignmentCalculationDefinition:
            raise TypeError(
                "definition must be Periodic1DMultibandAlignmentCalculationDefinition"
            )
        model = definition.parent_model
        mesh = CenteredUniformReciprocalMesh1D(
            model.hopping_model.reciprocal_period,
            definition.reciprocal_mesh_size,
        )
        parent_training = BlockHoppingInterpolator1D().execute(
            model.hopping_model, mesh.coordinates
        )
        training_target = self._spectrum(parent_training, definition.retained_rank)
        raw_frames = self._eigenframes(
            parent_training,
            mesh,
            definition.retained_rank,
            definition.orthonormality_absolute_tolerance,
        )
        transport = PolarBandFrameTransporter1D().execute(
            raw_frames, definition.overlap_singular_value_threshold
        )
        reference = transport.transported
        attack_rotations = self._attack_rotations(definition, mesh.coordinates)
        attacked = self._rotate_path(reference, attack_rotations)
        pointwise = BandFrameAligner1D().execute(reference, attacked)
        constrained_rotation = self._global_rotation(reference, attacked)
        constrained = self._rotate_path(
            attacked,
            tuple(
                constrained_rotation.magnitude.copy()
                for _ in range(definition.reciprocal_mesh_size)
            ),
        )

        projector = BandProjectedOperatorPathConstructor1D()
        reference_operator = projector.execute(
            parent_training, reference, definition.coordinate_absolute_tolerance
        )
        attacked_operator = projector.execute(
            parent_training, attacked, definition.coordinate_absolute_tolerance
        )
        aligned_operator = projector.execute(
            parent_training,
            pointwise.aligned,
            definition.coordinate_absolute_tolerance,
        )
        constrained_operator = projector.execute(
            parent_training, constrained, definition.coordinate_absolute_tolerance
        )

        transformer = ReciprocalOperatorFourierTransformer1D()
        reference_transform = transformer.execute(
            reference_operator,
            mesh,
            definition.coordinate_absolute_tolerance,
            definition.reconstruction_absolute_tolerance,
        )
        attacked_transform = transformer.execute(
            attacked_operator,
            mesh,
            definition.coordinate_absolute_tolerance,
            definition.reconstruction_absolute_tolerance,
        )
        aligned_transform = transformer.execute(
            aligned_operator,
            mesh,
            definition.coordinate_absolute_tolerance,
            definition.reconstruction_absolute_tolerance,
        )

        withheld_coordinates = VectorQuantity(
            model.hopping_model.reciprocal_period.magnitude
            * np.asarray(definition.withheld_reduced_momenta, dtype=np.float64),
            model.hopping_model.reciprocal_period.unit,
        )
        parent_withheld = BlockHoppingInterpolator1D().execute(
            model.hopping_model, withheld_coordinates
        )
        withheld_target = self._spectrum(parent_withheld, definition.retained_rank)
        external_gap = self._external_gap_minimum(
            definition, parent_training, parent_withheld
        )

        diagnostics = Periodic1DMultibandAlignmentDiagnostics(
            transport=transport,
            pointwise_alignment=pointwise,
            constrained_rotation=constrained_rotation,
            external_gap_minimum=external_gap,
            attack_frame_maximum_frobenius_defect=self._frame_defect(
                reference, attacked
            ),
            pointwise_rotation_recovery_maximum_frobenius_defect=(
                self._rotation_recovery_defect(pointwise.rotations, attack_rotations)
            ),
            constrained_frame_maximum_frobenius_defect=self._frame_defect(
                reference, constrained
            ),
            attacked_operator_maximum_frobenius_defect=self._operator_defect(
                reference_operator, attacked_operator
            ),
            pointwise_operator_maximum_frobenius_defect=self._operator_defect(
                reference_operator, aligned_operator
            ),
            constrained_operator_maximum_frobenius_defect=self._operator_defect(
                reference_operator, constrained_operator
            ),
        )
        hermiticity_analyzer = BlockHoppingHermiticityAnalyzer1D()
        reference_hermiticity = hermiticity_analyzer.execute(
            reference_transform.hopping_model,
            definition.hermiticity_absolute_tolerance,
            definition.reciprocal_mesh_size,
        )
        attacked_hermiticity = hermiticity_analyzer.execute(
            attacked_transform.hopping_model,
            definition.hermiticity_absolute_tolerance,
            definition.reciprocal_mesh_size,
        )
        aligned_hermiticity = hermiticity_analyzer.execute(
            aligned_transform.hopping_model,
            definition.hermiticity_absolute_tolerance,
            definition.reciprocal_mesh_size,
        )
        range_study = tuple(
            self._range_result(
                definition,
                maximum_range,
                training_target,
                withheld_target,
                reference_transform.hopping_model,
                attacked_transform.hopping_model,
                aligned_transform.hopping_model,
            )
            for maximum_range in definition.hopping_ranges
        )
        return Periodic1DMultibandAlignmentCalculationResult(
            definition=definition,
            training_target=training_target,
            withheld_target=withheld_target,
            diagnostics=diagnostics,
            reference_transform=reference_transform,
            attacked_transform=attacked_transform,
            aligned_transform=aligned_transform,
            reference_hermiticity=reference_hermiticity,
            attacked_hermiticity=attacked_hermiticity,
            aligned_hermiticity=aligned_hermiticity,
            range_study=range_study,
        )

    def _external_gap_minimum(
        self,
        definition: Periodic1DMultibandAlignmentCalculationDefinition,
        training: ReciprocalOperatorSamples1D,
        withheld: ReciprocalOperatorSamples1D,
    ) -> ScalarQuantity:
        """Return the minimum retained/excluded finite-mesh energy gap.

        Both training and staggered evaluation paths are inspected against the frozen
        lower bound; the result is a finite diagnostic, not a gap theorem.
        """
        rank = definition.retained_rank
        gaps = [
            float(values[rank] - values[rank - 1])
            for samples in (training, withheld)
            for values in (
                np.linalg.eigvalsh(matrix.magnitude) for matrix in samples.matrices
            )
        ]
        unit = training.matrices[0].unit
        result = ScalarQuantity(min(gaps), unit)
        lower_bound = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
            definition.external_gap_lower_bound, unit
        )
        if result.magnitude < lower_bound.magnitude:
            raise ValueError("parent external gap does not pass the frozen lower bound")
        return result

    def _range_result(
        self,
        definition: Periodic1DMultibandAlignmentCalculationDefinition,
        maximum_range: int,
        training_target: BandSpectrumSamples1D,
        withheld_target: BandSpectrumSamples1D,
        reference_model: BlockHoppingModel1D,
        attacked_model: BlockHoppingModel1D,
        aligned_model: BlockHoppingModel1D,
    ) -> Periodic1DMultibandAlignmentRangeResult:
        """Truncate three gauge channels and compare common spectral targets."""
        if any(
            type(model) is not BlockHoppingModel1D
            for model in (reference_model, attacked_model, aligned_model)
        ):
            raise TypeError("range models must be BlockHoppingModel1D")
        truncator = BlockHoppingTruncator1D()
        reference = truncator.execute(reference_model, maximum_range)
        attacked = truncator.execute(attacked_model, maximum_range)
        aligned = truncator.execute(aligned_model, maximum_range)
        interpolator = BlockHoppingInterpolator1D()
        analyzer = BandApproximationErrorAnalyzer1D()

        def error(
            target: BandSpectrumSamples1D, model: BlockHoppingModel1D
        ) -> BandApproximationErrorResult1D:
            """Evaluate one truncated channel on one identified target mesh."""
            return analyzer.execute(
                target,
                interpolator.execute(model, target.coordinates),
                definition.coordinate_absolute_tolerance,
            )

        return Periodic1DMultibandAlignmentRangeResult(
            reference,
            attacked,
            aligned,
            error(training_target, reference.truncated),
            error(training_target, attacked.truncated),
            error(training_target, aligned.truncated),
            error(withheld_target, reference.truncated),
            error(withheld_target, attacked.truncated),
            error(withheld_target, aligned.truncated),
        )

    @staticmethod
    def _spectrum(
        samples: ReciprocalOperatorSamples1D, retained_rank: int
    ) -> BandSpectrumSamples1D:
        """Return the lowest retained eigenvalues of represented parent samples."""
        values = np.asarray(
            [
                np.linalg.eigvalsh(matrix.magnitude)[:retained_rank]
                for matrix in samples.matrices
            ],
            dtype=np.float64,
        )
        return BandSpectrumSamples1D(
            samples.coordinates,
            samples.reciprocal_period,
            MatrixQuantity(values, samples.matrices[0].unit),
        )

    @staticmethod
    def _eigenframes(
        parent: ReciprocalOperatorSamples1D,
        mesh: CenteredUniformReciprocalMesh1D,
        retained_rank: int,
        orthonormality_absolute_tolerance: float,
    ) -> ReciprocalBandFramePath1D:
        """Construct raw low-eigenvector frames before polar transport."""
        frames = tuple(
            ComplexMatrixQuantity(
                np.linalg.eigh(matrix.magnitude)[1][:, :retained_rank], Unitless()
            )
            for matrix in parent.matrices
        )
        ambient = parent.matrix_dimension
        return ReciprocalBandFramePath1D(
            mesh,
            frames,
            ComplexMatrixQuantity(np.eye(ambient, dtype=np.complex128), Unitless()),
            orthonormality_absolute_tolerance,
        )

    @staticmethod
    def _attack_rotations(
        definition: Periodic1DMultibandAlignmentCalculationDefinition,
        coordinates: VectorQuantity,
    ) -> tuple[npt.NDArray[np.complex128], ...]:
        r"""Evaluate the frozen real-rotation attack at every momentum.

        The angle is ``theta_0 + sum_q c_q sin(2 pi q k)`` in radians.
        """
        reduced = (
            coordinates.magnitude
            / definition.parent_model.hopping_model.reciprocal_period.magnitude
        )
        rotations: list[npt.NDArray[np.complex128]] = []
        for momentum in reduced:
            angle = definition.attack_constant_angle + sum(
                coefficient * np.sin(2.0 * np.pi * harmonic * float(momentum))
                for harmonic, coefficient in enumerate(
                    definition.attack_sine_coefficients, start=1
                )
            )
            cosine = float(np.cos(angle))
            sine = float(np.sin(angle))
            rotations.append(
                np.asarray([[cosine, -sine], [sine, cosine]], dtype=np.complex128)
            )
        return tuple(rotations)

    @staticmethod
    def _rotate_path(
        source: ReciprocalBandFramePath1D,
        rotations: tuple[npt.NDArray[np.complex128], ...],
    ) -> ReciprocalBandFramePath1D:
        """Right-multiply each frame by its same-space unitary rotation."""
        if len(rotations) != source.mesh.point_count:
            raise ValueError("one rotation is required per reciprocal point")
        return ReciprocalBandFramePath1D(
            source.mesh,
            tuple(
                ComplexMatrixQuantity(
                    frame.magnitude @ rotation,
                    Unitless(),
                )
                for frame, rotation in zip(source.frames, rotations, strict=True)
            ),
            source.sewing_map,
            source.orthonormality_absolute_tolerance,
        )

    @staticmethod
    def _global_rotation(
        reference: ReciprocalBandFramePath1D,
        candidate: ReciprocalBandFramePath1D,
    ) -> ComplexMatrixQuantity:
        """Return the polar/SVD optimizer over the one-global-unitary family."""
        aggregate = sum(
            (
                candidate_frame.magnitude.conj().T @ reference_frame.magnitude
                for reference_frame, candidate_frame in zip(
                    reference.frames, candidate.frames, strict=True
                )
            ),
            np.zeros((reference.rank, reference.rank), dtype=np.complex128),
        )
        left, _, right_h = np.linalg.svd(aggregate)
        return ComplexMatrixQuantity(left @ right_h, Unitless())

    @staticmethod
    def _frame_defect(
        reference: ReciprocalBandFramePath1D,
        candidate: ReciprocalBandFramePath1D,
    ) -> float:
        """Return the maximum pointwise Frobenius frame defect."""
        return float(
            max(
                np.linalg.norm(left.magnitude - right.magnitude)
                for left, right in zip(reference.frames, candidate.frames, strict=True)
            )
        )

    @staticmethod
    def _rotation_recovery_defect(
        recovered: tuple[ComplexMatrixQuantity, ...],
        attacks: tuple[npt.NDArray[np.complex128], ...],
    ) -> float:
        """Compare recovered pointwise rotations with inverse attack rotations."""
        return float(
            max(
                np.linalg.norm(rotation.magnitude - attack.conj().T)
                for rotation, attack in zip(recovered, attacks, strict=True)
            )
        )

    @staticmethod
    def _operator_defect(
        reference: ReciprocalOperatorSamples1D,
        candidate: ReciprocalOperatorSamples1D,
    ) -> ScalarQuantity:
        """Return the maximum represented-operator Frobenius defect in energy units."""
        if reference.matrices[0].unit != candidate.matrices[0].unit:
            raise ValueError("operator comparison requires one energy unit")
        defect = float(
            max(
                np.linalg.norm(left.magnitude - right.magnitude)
                for left, right in zip(
                    reference.matrices, candidate.matrices, strict=True
                )
            )
        )
        return ScalarQuantity(defect, reference.matrices[0].unit)


__all__ = ["Periodic1DMultibandAlignmentCalculator"]
