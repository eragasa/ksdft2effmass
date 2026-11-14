"""Production calculation for periodic-2D parent capability qualification."""

from __future__ import annotations

import hashlib
import json

import numpy as np
from projectkoios.physkit.units import Unitless
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.periodic.models import PeriodicModelRole
from ksdft2effmass.periodic.periodic2d.models import (
    Periodic2DCosinePotentialModel,
    Periodic2DPlaneWaveHamiltonian,
    Periodic2DPlaneWaveHamiltonianRequest,
)
from ksdft2effmass.solidstate import (
    BoundaryTwistLift,
    BoundaryTwistMeshEnumerator,
    FiniteLatticeShape,
    LatticeDimension,
    LatticeDisplacement,
    LocalizedPerturbation,
    LocalizedPerturbationOperatorConstructor,
    QuotientSeamOperatorConstructor,
    ScalarHoppingModel,
    ScalarHoppingTerm,
    TwistedSupercellOperatorConstructor,
    TwistGaugeBridgeConstructor,
    TwistGaugeEquivalenceAnalyzer,
)

from .parent_qualification import (
    ParentQualificationCriterionEvaluator,
    ParentQualificationDefinition,
    ParentQualificationResult,
    QualifiedParentMetrics,
    QualifiedPerturbationMetrics,
)

type ComplexCsr = sparse.csr_array


class ParentQualificationCalculator:
    """Qualify exact parents through maintained production construction routes."""

    __slots__ = ()

    def execute(
        self, definition: ParentQualificationDefinition
    ) -> ParentQualificationResult:
        """Return aggregate qualification metrics over every planned shape and twist."""
        if type(definition) is not ParentQualificationDefinition:
            raise TypeError("definition must be ParentQualificationDefinition")
        anisotropic_full, anisotropic_compact = self._anisotropic_models(definition)
        swapped_full = self._swapped_model(
            anisotropic_full,
            identifier="anisotropic_lambda_0p7_0p3_0.pretruncation",
        )
        swapped = self._swapped_model(
            anisotropic_compact,
            identifier="anisotropic_lambda_0p7_0p3_0",
        )
        parents = (
            definition.isotropic_parent,
            anisotropic_compact,
            swapped,
        )
        pretruncation_parents = (
            definition.isotropic_pretruncation_parent,
            anisotropic_full,
            swapped_full,
        )
        expected_ids = tuple(value[0] for value in definition.expected_parent_digests)
        if tuple(parent.identifier for parent in parents) != expected_ids:
            raise ValueError("constructed parent identities differ from the definition")

        parent_metrics = tuple(
            self._parent_metrics(definition, parent, pretruncation)
            for parent, pretruncation in zip(
                parents, pretruncation_parents, strict=True
            )
        )
        perturbation_metrics = tuple(
            self._perturbation_metrics(definition, perturbation)
            for perturbation in definition.perturbations
        )
        separability = self._separability_metric(definition)
        failures = ParentQualificationCriterionEvaluator().execute(
            definition,
            parent_metrics,
            perturbation_metrics,
            separability,
        )
        return ParentQualificationResult(
            definition,
            parent_metrics,
            perturbation_metrics,
            separability,
            failures,
        )

    def _parent_metrics(
        self,
        definition: ParentQualificationDefinition,
        parent: ScalarHoppingModel,
        pretruncation: ScalarHoppingModel,
    ) -> QualifiedParentMetrics:
        """Evaluate coefficient and represented-route metrics for one parent."""
        symmetry_operations = (
            self._d4_operations()
            if parent.identifier == definition.isotropic_parent.identifier
            else self._d2_operations()
        )
        hopping_hermiticity, hopping_symmetry = self._hopping_metrics(
            parent, symmetry_operations
        )
        represented_hermiticity = 0.0
        gauge_bridge = 0.0
        route_evaluations = 0
        uniform_constructor = TwistedSupercellOperatorConstructor()
        seam_constructor = QuotientSeamOperatorConstructor()
        bridge_constructor = TwistGaugeBridgeConstructor()
        equivalence = TwistGaugeEquivalenceAnalyzer()
        twists = BoundaryTwistMeshEnumerator().execute(definition.twist_mesh)
        for shape in definition.shapes:
            for representative in twists:
                twist = BoundaryTwistLift(LatticeDimension.TWO, representative.turns)
                uniform = uniform_constructor.execute(
                    f"{parent.identifier}.uniform", parent, shape, twist
                )
                seam = seam_constructor.execute_hopping(
                    f"{parent.identifier}.seam", parent, shape, twist
                )
                route_evaluations += 2
                represented_hermiticity = max(
                    represented_hermiticity,
                    self._hermiticity(uniform.matrix.to_csr()),
                    self._hermiticity(seam.matrix.to_csr()),
                )
                bridge = bridge_constructor.execute(shape, uniform.twist_fiber)
                comparison = equivalence.execute(
                    uniform,
                    seam,
                    bridge,
                    absolute_tolerance=definition.tolerances.gauge_bridge_absolute,
                )
                if comparison.maximum_absolute_residual is None:
                    raise ValueError(
                        "qualified parent gauge comparison is incompatible"
                    )
                gauge_bridge = max(gauge_bridge, comparison.maximum_absolute_residual)
        truncation_maximum, truncation_frobenius = self._truncation_metrics(
            definition, pretruncation, parent
        )
        return QualifiedParentMetrics(
            parent_identifier=parent.identifier,
            hopping_count=len(parent.terms),
            hopping_digest=self._historical_digest(parent),
            hopping_hermiticity_maximum_absolute=hopping_hermiticity,
            hopping_symmetry_maximum_absolute=hopping_symmetry,
            represented_hermiticity_maximum_absolute=represented_hermiticity,
            gauge_bridge_maximum_absolute=gauge_bridge,
            route_evaluations=route_evaluations,
            inherited_truncation_maximum_absolute=truncation_maximum,
            inherited_truncation_frobenius=truncation_frobenius,
        )

    def _perturbation_metrics(
        self,
        definition: ParentQualificationDefinition,
        perturbation: LocalizedPerturbation,
    ) -> QualifiedPerturbationMetrics:
        """Evaluate represented routes for one typed localized perturbation."""
        if type(perturbation) is not LocalizedPerturbation:
            raise TypeError("perturbation must be LocalizedPerturbation")
        represented_hermiticity = 0.0
        gauge_bridge = 0.0
        route_evaluations = 0
        uniform_constructor = LocalizedPerturbationOperatorConstructor()
        seam_constructor = QuotientSeamOperatorConstructor()
        bridge_constructor = TwistGaugeBridgeConstructor()
        equivalence = TwistGaugeEquivalenceAnalyzer()
        twists = BoundaryTwistMeshEnumerator().execute(definition.twist_mesh)
        for shape in definition.shapes:
            for representative in twists:
                twist = BoundaryTwistLift(LatticeDimension.TWO, representative.turns)
                uniform = uniform_constructor.execute(
                    f"{perturbation.identifier}.uniform",
                    perturbation,
                    shape,
                    twist,
                )
                seam = seam_constructor.execute_perturbation(
                    f"{perturbation.identifier}.seam",
                    perturbation,
                    shape,
                    twist,
                )
                route_evaluations += 2
                represented_hermiticity = max(
                    represented_hermiticity,
                    self._hermiticity(uniform.matrix.to_csr()),
                    self._hermiticity(seam.matrix.to_csr()),
                )
                bridge = bridge_constructor.execute(shape, uniform.twist_fiber)
                comparison = equivalence.execute(
                    uniform,
                    seam,
                    bridge,
                    absolute_tolerance=definition.tolerances.gauge_bridge_absolute,
                )
                if comparison.maximum_absolute_residual is None:
                    raise ValueError(
                        "qualified perturbation gauge comparison is incompatible"
                    )
                gauge_bridge = max(gauge_bridge, comparison.maximum_absolute_residual)
        return QualifiedPerturbationMetrics(
            perturbation_identifier=perturbation.identifier,
            term_count=len(perturbation.terms),
            represented_hermiticity_maximum_absolute=represented_hermiticity,
            gauge_bridge_maximum_absolute=gauge_bridge,
            route_evaluations=route_evaluations,
        )

    @staticmethod
    def _lowest_band(momentum: float, strength: float, cutoff: int) -> float:
        """Evaluate the one-dimensional cosine lowest band for separable production."""
        indices = np.arange(-cutoff, cutoff + 1, dtype=np.float64)
        matrix = np.diag(np.square(momentum + indices))
        coupling = strength / 2.0
        matrix += np.diag(np.full(2 * cutoff, coupling), 1)
        matrix += np.diag(np.full(2 * cutoff, coupling), -1)
        return float(np.linalg.eigvalsh(matrix)[0])

    def _anisotropic_models(
        self, definition: ParentQualificationDefinition
    ) -> tuple[ScalarHoppingModel, ScalarHoppingModel]:
        """Reconstruct full and radius-limited anisotropic hopping models."""
        mesh = definition.reciprocal_mesh_size
        momenta = np.fft.fftfreq(mesh)
        x_energies = np.asarray(
            [
                self._lowest_band(
                    float(momentum),
                    definition.anisotropic_lambda_x,
                    definition.plane_wave_cutoff,
                )
                for momentum in momenta
            ],
            dtype=np.float64,
        )
        y_energies = np.asarray(
            [
                self._lowest_band(
                    float(momentum),
                    definition.anisotropic_lambda_y,
                    definition.plane_wave_cutoff,
                )
                for momentum in momenta
            ],
            dtype=np.float64,
        )
        energies = x_energies[:, np.newaxis] + y_energies[np.newaxis, :]
        ix = np.arange(mesh, dtype=np.float64)[:, np.newaxis]
        iy = np.arange(mesh, dtype=np.float64)[np.newaxis, :]
        half = mesh // 2
        terms: list[ScalarHoppingTerm] = []
        for rx in range(-half, half + 1):
            for ry in range(-half, half + 1):
                phase = np.exp(
                    2.0j * np.pi * (ix * float(rx) + iy * float(ry)) / float(mesh)
                )
                value = complex(np.sum(energies * phase) / float(mesh * mesh))
                terms.append(
                    ScalarHoppingTerm(
                        LatticeDisplacement(LatticeDimension.TWO, (rx, ry)),
                        float(value.real),
                        float(value.imag),
                    )
                )
        basis = definition.isotropic_parent.basis_identifier
        reference = definition.isotropic_parent.energy_reference
        full = ScalarHoppingModel(
            identifier="anisotropic_lambda_0p3_0p7_0.pretruncation",
            dimension=LatticeDimension.TWO,
            terms=tuple(terms),
            energy_unit=Unitless(),
            energy_reference=reference,
            basis_identifier=basis,
        )
        compact_terms = tuple(
            term
            for term in full.terms
            if sum(value * value for value in term.displacement.components)
            <= definition.hopping_maximum_squared_radius
        )
        compact = ScalarHoppingModel(
            identifier="anisotropic_lambda_0p3_0p7_0",
            dimension=LatticeDimension.TWO,
            terms=compact_terms,
            energy_unit=Unitless(),
            energy_reference=reference,
            basis_identifier=basis,
        )
        if len(full.terms) != 225 or len(compact.terms) != 61:
            raise ValueError("anisotropic parent support inventory changed")
        return full, compact

    @classmethod
    def _swapped_model(
        cls, parent: ScalarHoppingModel, *, identifier: str
    ) -> ScalarHoppingModel:
        """Construct one separately identified axis-swapped parent."""
        if type(identifier) is not str:
            raise TypeError("identifier must be a string")
        if not identifier:
            raise ValueError("identifier must be nonempty")
        terms: list[ScalarHoppingTerm] = []
        for term in parent.terms:
            displacement_x, displacement_y = cls._pair(term.displacement.components)
            terms.append(
                ScalarHoppingTerm(
                    LatticeDisplacement(
                        LatticeDimension.TWO,
                        (displacement_y, displacement_x),
                    ),
                    term.real,
                    term.imaginary,
                )
            )
        ordered = tuple(sorted(terms, key=lambda value: value.displacement.components))
        return ScalarHoppingModel(
            identifier=identifier,
            dimension=LatticeDimension.TWO,
            terms=ordered,
            energy_unit=parent.energy_unit,
            energy_reference=parent.energy_reference,
            basis_identifier=parent.basis_identifier,
        )

    def _truncation_metrics(
        self,
        definition: ParentQualificationDefinition,
        full: ScalarHoppingModel,
        compact: ScalarHoppingModel,
    ) -> tuple[float, float]:
        """Return maximum finite-matrix truncation losses at historical twists."""
        constructor = TwistedSupercellOperatorConstructor()
        shape = FiniteLatticeShape(LatticeDimension.TWO, (8, 8))
        maximum = 0.0
        frobenius = 0.0
        for turns in ((0.0, 0.0), (0.37, -0.23)):
            twist = BoundaryTwistLift(LatticeDimension.TWO, turns)
            full_matrix = constructor.execute(
                f"{full.identifier}.truncation-parent", full, shape, twist
            ).matrix.to_csr()
            compact_matrix = constructor.execute(
                f"{compact.identifier}.truncation-compact", compact, shape, twist
            ).matrix.to_csr()
            difference = full_matrix - compact_matrix
            difference.sum_duplicates()
            difference.eliminate_zeros()
            maximum = max(maximum, self._maximum_sparse(difference))
            frobenius = max(
                frobenius,
                float(np.sqrt(np.sum(np.square(np.abs(difference.data))))),
            )
        return maximum, frobenius

    def _separability_metric(self, definition: ParentQualificationDefinition) -> float:
        """Compare selected maintained 2D fibers with separable energies."""
        model = Periodic2DCosinePotentialModel(
            definition.anisotropic_lambda_x,
            definition.anisotropic_lambda_y,
            definition.anisotropic_lambda_xy,
            role=PeriodicModelRole.CONTROL_MODEL,
        )
        momenta = (
            (0.0, 0.0),
            (1.0 / 15.0, -2.0 / 15.0),
            (7.0 / 15.0, 5.0 / 15.0),
            (-7.0 / 15.0, -6.0 / 15.0),
        )
        maximum = 0.0
        for kx, ky in momenta:
            represented = Periodic2DPlaneWaveHamiltonian(
                Periodic2DPlaneWaveHamiltonianRequest(
                    model,
                    kx,
                    ky,
                    definition.plane_wave_cutoff,
                )
            ).result()
            observed = float(np.linalg.eigvalsh(represented.matrix)[0])
            expected = self._lowest_band(
                kx, definition.anisotropic_lambda_x, definition.plane_wave_cutoff
            ) + self._lowest_band(
                ky, definition.anisotropic_lambda_y, definition.plane_wave_cutoff
            )
            maximum = max(maximum, abs(observed - expected))
        return maximum

    @staticmethod
    def _historical_digest(model: ScalarHoppingModel) -> str:
        """Return the historical compact-hopping canonical SHA-256 identity."""
        payload = [
            [
                *ParentQualificationCalculator._pair(term.displacement.components),
                float(term.real),
                float(term.imaginary),
            ]
            for term in model.terms
        ]
        return hashlib.sha256(
            json.dumps(payload, separators=(",", ":")).encode("utf-8")
        ).hexdigest()

    @staticmethod
    def _hopping_metrics(
        model: ScalarHoppingModel,
        operations: tuple[tuple[tuple[int, int], tuple[int, int]], ...],
    ) -> tuple[float, float]:
        """Return Hermiticity and declared point-operation covariance residuals."""
        values: dict[tuple[int, int], complex] = {
            ParentQualificationCalculator._pair(term.displacement.components): (
                term.value
            )
            for term in model.terms
        }
        hermiticity = 0.0
        symmetry = 0.0
        for displacement, value in values.items():
            reverse = (-displacement[0], -displacement[1])
            if reverse not in values:
                raise ValueError(f"missing Hermitian partner {reverse}")
            hermiticity = max(hermiticity, abs(values[reverse] - value.conjugate()))
            for operation in operations:
                transformed = (
                    operation[0][0] * displacement[0]
                    + operation[0][1] * displacement[1],
                    operation[1][0] * displacement[0]
                    + operation[1][1] * displacement[1],
                )
                if transformed not in values:
                    raise ValueError(f"missing symmetry partner {transformed}")
                symmetry = max(symmetry, abs(values[transformed] - value))
        return float(hermiticity), float(symmetry)

    @staticmethod
    def _hermiticity(matrix: ComplexCsr) -> float:
        """Return the maximum sparse Hermiticity residual without densification."""
        difference = matrix - matrix.conjugate().transpose()
        difference.sum_duplicates()
        difference.eliminate_zeros()
        return ParentQualificationCalculator._maximum_sparse(difference)

    @staticmethod
    def _maximum_sparse(matrix: ComplexCsr) -> float:
        """Return the finite maximum absolute sparse entry."""
        if matrix.data.size == 0:
            return 0.0
        magnitudes = np.abs(matrix.data)
        if not np.all(np.isfinite(magnitudes)):
            raise ValueError("sparse residual must remain finite")
        return float(np.max(magnitudes))

    @staticmethod
    def _pair(
        values: tuple[int] | tuple[int, int] | tuple[int, int, int],
    ) -> tuple[int, int]:
        """Close one validated two-dimensional integer tuple."""
        if len(values) != 2:
            raise AssertionError("two-dimensional integer components were lost")
        return values[0], values[1]

    @staticmethod
    def _d4_operations() -> tuple[tuple[tuple[int, int], tuple[int, int]], ...]:
        """Return the exact frozen D4 operation inventory."""
        return (
            ((1, 0), (0, 1)),
            ((0, -1), (1, 0)),
            ((-1, 0), (0, -1)),
            ((0, 1), (-1, 0)),
            ((-1, 0), (0, 1)),
            ((1, 0), (0, -1)),
            ((0, 1), (1, 0)),
            ((0, -1), (-1, 0)),
        )

    @staticmethod
    def _d2_operations() -> tuple[tuple[tuple[int, int], tuple[int, int]], ...]:
        """Return the exact frozen anisotropic D2 operation inventory."""
        return (
            ((1, 0), (0, 1)),
            ((-1, 0), (0, -1)),
            ((-1, 0), (0, 1)),
            ((1, 0), (0, -1)),
        )
