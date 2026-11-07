"""Contracts for the periodic dimension-to-rank study hierarchy."""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError
from pathlib import Path

import numpy as np
import pytest
from projectkoios.physkit.periodic.lattice.finite_domain import (
    LatticeDimension,
    LatticeDisplacement,
)
from projectkoios.physkit.periodic.lattice.hopping import (
    DenseBlockHoppingModel,
    DenseBlockHoppingTerm,
)
from projectkoios.physkit.units import ComplexMatrixQuantity, PhysicalUnit, Unitless

from ksdft2effmass.periodic.models import PeriodicModelRole
from ksdft2effmass.periodic.periodic1d.rank2.models import (
    Periodic1DRank2BlockHoppingModel,
)
from ksdft2effmass.periodic.periodic2d.rank2.models import (
    Periodic2DRank2BlockHoppingModel,
)
from ksdft2effmass.periodic.periodic3d.rank2.models import (
    Periodic3DRank2BlockHoppingModel,
)
from ksdft2effmass.periodic1d.geometry import Periodic1DLatticeGeometry
from ksdft2effmass.periodic2d.geometry import Periodic2DLatticeGeometry
from ksdft2effmass.periodic3d.geometry import Periodic3DLatticeGeometry
from ksdft2effmass.study.periodic import (
    PeriodicStudy,
    PeriodicStudyModelRole,
    PeriodicStudyOrchestrator,
)
from ksdft2effmass.study.periodic1d import (
    Periodic1DStudy,
    Periodic1DStudyOrchestrator,
)
from ksdft2effmass.study.periodic1d.rank2 import (
    Periodic1DRank2Study,
    Periodic1DRank2StudyOrchestrator,
)
from ksdft2effmass.study.periodic2d import (
    Periodic2DStudy,
    Periodic2DStudyOrchestrator,
)
from ksdft2effmass.study.periodic2d.rank2 import (
    Periodic2DRank2Study,
    Periodic2DRank2StudyOrchestrator,
)
from ksdft2effmass.study.periodic3d import (
    Periodic3DStudy,
    Periodic3DStudyOrchestrator,
)
from ksdft2effmass.study.periodic3d.rank2 import (
    Periodic3DRank2Study,
    Periodic3DRank2StudyOrchestrator,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodicRank2StudyHierarchy:
    """Establish study inheritance, identity, model, dimension, and rank contracts."""

    @staticmethod
    def _representation(dimension: LatticeDimension) -> DenseBlockHoppingModel:
        """Construct a minimal exactly Hermitian rank-two representation.

        Parameters
        ----------
        dimension
            Exact lattice dimension assigned to the zero displacement.

        Returns
        -------
        DenseBlockHoppingModel
            One onsite rank-two coefficient with dimensionless energy unit.

        """
        zero: tuple[int] | tuple[int, int] | tuple[int, int, int]
        if dimension is LatticeDimension.ONE:
            zero = (0,)
        elif dimension is LatticeDimension.TWO:
            zero = (0, 0)
        elif dimension is LatticeDimension.THREE:
            zero = (0, 0, 0)
        else:
            raise ValueError(
                "study representation dimension must be one, two, or three"
            )
        onsite = np.array(
            ((-0.4 + 0.0j, 0.1 - 0.02j), (0.1 + 0.02j, 0.6 + 0.0j)),
            dtype=np.complex128,
        )
        return DenseBlockHoppingModel(
            identifier=f"study-{dimension.value}d-representation-v1",
            dimension=dimension,
            terms=(
                DenseBlockHoppingTerm(
                    displacement=LatticeDisplacement(dimension, zero),
                    coefficient=ComplexMatrixQuantity(onsite, Unitless()),
                ),
            ),
            energy_unit=Unitless(),
            energy_reference="dimensionless-zero-v1",
            basis_identifier="ordered-rank2-basis-v1",
        )

    @classmethod
    def _model_1d(cls) -> Periodic1DRank2BlockHoppingModel:
        """Construct one exact periodic-1D rank-two model."""
        return Periodic1DRank2BlockHoppingModel(
            identifier="study-model-1d-v1",
            role=PeriodicModelRole.CONTROL_MODEL,
            geometry=Periodic1DLatticeGeometry(1.0, PhysicalUnit("bohr")),
            representation=cls._representation(LatticeDimension.ONE),
        )

    @classmethod
    def _model_2d(cls) -> Periodic2DRank2BlockHoppingModel:
        """Construct one exact periodic-2D rank-two model."""
        return Periodic2DRank2BlockHoppingModel(
            identifier="study-model-2d-v1",
            role=PeriodicModelRole.CONTROL_MODEL,
            geometry=Periodic2DLatticeGeometry(
                primitive_basis_rows=((1.0, 0.0), (0.0, 1.0)),
                lattice_unit=PhysicalUnit("bohr"),
            ),
            representation=cls._representation(LatticeDimension.TWO),
        )

    @classmethod
    def _model_3d(
        cls,
        primitive_basis_rows: tuple[
            tuple[float, float, float],
            tuple[float, float, float],
            tuple[float, float, float],
        ],
        *,
        identifier: str,
    ) -> Periodic3DRank2BlockHoppingModel:
        """Construct one exact periodic-3D rank-two model.

        Parameters
        ----------
        primitive_basis_rows
            Ordered row snapshot whose columns are primitive direct-lattice vectors.
        identifier
            Distinct scientific-model identity for the represented structure.

        Returns
        -------
        Periodic3DRank2BlockHoppingModel
            Complete model using the supplied structure data.

        """
        return Periodic3DRank2BlockHoppingModel(
            identifier=identifier,
            role=PeriodicModelRole.CONTROL_MODEL,
            geometry=Periodic3DLatticeGeometry(
                primitive_basis_rows=primitive_basis_rows,
                lattice_unit=PhysicalUnit("bohr"),
            ),
            representation=cls._representation(LatticeDimension.THREE),
        )

    def test__study_model_role__uses_plain_reference_and_candidate_labels(self) -> None:
        """Expose comparison roles without dimension or locality terminology."""
        assert PeriodicStudyModelRole.reference.to_wire() == "reference"
        assert PeriodicStudyModelRole.candidate.to_wire() == "candidate"
        assert PeriodicStudyModelRole.from_wire("reference") is (
            PeriodicStudyModelRole.reference
        )
        assert PeriodicStudyModelRole.from_wire("candidate") is (
            PeriodicStudyModelRole.candidate
        )

    def test__rank2_studies__inherit_the_dimension_to_rank_ladder(self) -> None:
        """Require every concrete study to retain the approved base-class ladder.

        Notes
        -----
        Dimension and retained rank are independent scientific identities. The test
        verifies inherited ownership rather than relying only on equal integer values.

        """
        study_1d = Periodic1DRank2Study(
            "study-1d-v1",
            self._model_1d(),
            PeriodicStudyModelRole.reference,
        )
        study_2d = Periodic2DRank2Study(
            "study-2d-v1",
            self._model_2d(),
            PeriodicStudyModelRole.reference,
        )
        study_3d = Periodic3DRank2Study(
            "study-3d-v1",
            self._model_3d(
                ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
                identifier="study-model-3d-v1",
            ),
            PeriodicStudyModelRole.candidate,
        )

        assert isinstance(study_1d, Periodic1DStudy)
        assert isinstance(study_2d, Periodic2DStudy)
        assert isinstance(study_3d, Periodic3DStudy)
        assert all(
            isinstance(study, PeriodicStudy) for study in (study_1d, study_2d, study_3d)
        )
        assert tuple(
            (study.spatial_dimension, study.band_subspace_rank)
            for study in (study_1d, study_2d, study_3d)
        ) == ((1, 2), (2, 2), (3, 2))

    def test__rank2_orchestrators__return_identity_correlated_studies(self) -> None:
        """Construct each study without copying or replacing its scientific model."""
        model_1d = self._model_1d()
        model_2d = self._model_2d()
        model_3d = self._model_3d(
            ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
            identifier="orchestrated-model-3d-v1",
        )
        orchestrators = (
            Periodic1DRank2StudyOrchestrator(
                "orchestrated-1d-v1",
                model_1d,
                PeriodicStudyModelRole.reference,
            ),
            Periodic2DRank2StudyOrchestrator(
                "orchestrated-2d-v1",
                model_2d,
                PeriodicStudyModelRole.reference,
            ),
            Periodic3DRank2StudyOrchestrator(
                "orchestrated-3d-v1",
                model_3d,
                PeriodicStudyModelRole.candidate,
            ),
        )

        studies = tuple(orchestrator.execute() for orchestrator in orchestrators)

        assert isinstance(orchestrators[0], Periodic1DStudyOrchestrator)
        assert isinstance(orchestrators[1], Periodic2DStudyOrchestrator)
        assert isinstance(orchestrators[2], Periodic3DStudyOrchestrator)
        assert all(
            isinstance(orchestrator, PeriodicStudyOrchestrator)
            for orchestrator in orchestrators
        )
        assert tuple(study.model for study in studies) == (
            model_1d,
            model_2d,
            model_3d,
        )
        assert tuple(study.study_id for study in studies) == (
            "orchestrated-1d-v1",
            "orchestrated-2d-v1",
            "orchestrated-3d-v1",
        )
        assert tuple(orchestrator.model_id for orchestrator in orchestrators) == (
            model_1d.model_id,
            model_2d.model_id,
            model_3d.model_id,
        )
        assert tuple(study.model_role for study in studies) == (
            PeriodicStudyModelRole.reference,
            PeriodicStudyModelRole.reference,
            PeriodicStudyModelRole.candidate,
        )

    def test__periodic3d_rank2_study__is_structure_agnostic(self) -> None:
        """Represent simple-cubic and nonorthogonal structures with one study class.

        Notes
        -----
        Structure identity is carried by the ordered primitive basis in each exact
        model. The study hierarchy therefore requires neither crystal-specific
        subclasses nor conditional structure labels.

        """
        simple_cubic = self._model_3d(
            ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
            identifier="simple-cubic-model-v1",
        )
        face_centered_primitive = self._model_3d(
            ((0.0, 0.5, 0.5), (0.5, 0.0, 0.5), (0.5, 0.5, 0.0)),
            identifier="fcc-primitive-model-v1",
        )

        simple_cubic_study = Periodic3DRank2StudyOrchestrator(
            "simple-cubic-study-v1",
            simple_cubic,
            PeriodicStudyModelRole.reference,
        ).execute()
        face_centered_study = Periodic3DRank2StudyOrchestrator(
            "fcc-study-v1",
            face_centered_primitive,
            PeriodicStudyModelRole.candidate,
        ).execute()

        assert type(simple_cubic_study) is Periodic3DRank2Study
        assert type(face_centered_study) is Periodic3DRank2Study
        assert simple_cubic_study.model.lattice_geometry != (
            face_centered_study.model.lattice_geometry
        )
        assert simple_cubic_study.model is simple_cubic
        assert face_centered_study.model is face_centered_primitive

    def test__rank2_study__rejects_cross_dimensional_model_substitution(self) -> None:
        """Reject a model from another dimensional state-space contract."""
        wrong_dimension_model = self._model_2d()

        with pytest.raises(TypeError, match="Periodic3DRank2BlockHoppingModel"):
            Periodic3DRank2Study(
                "invalid-cross-dimensional-study-v1",
                wrong_dimension_model,  # type: ignore[arg-type]
                PeriodicStudyModelRole.candidate,
            )

    def test__rank2_study__requires_nonempty_builtin_identity(self) -> None:
        """Reject absent or non-string study identity without coercion."""
        model = self._model_1d()

        with pytest.raises(ValueError, match="must be nonempty"):
            Periodic1DRank2Study("", model, PeriodicStudyModelRole.reference)
        with pytest.raises(TypeError, match="built-in string"):
            Periodic1DRank2Study(
                1,  # type: ignore[arg-type]
                model,
                PeriodicStudyModelRole.reference,
            )

    def test__rank2_study__rejects_untyped_comparison_role(self) -> None:
        """Reject a wire string where the explicit study-role enum is required."""
        with pytest.raises(TypeError, match="PeriodicStudyModelRole"):
            Periodic2DRank2Study(
                "invalid-role-study-v1",
                self._model_2d(),
                "reference",  # type: ignore[arg-type]
            )

    def test__rank2_study__is_operationally_immutable(self) -> None:
        """Prevent replacement of the retained scientific-model correlation."""
        study = Periodic2DRank2Study(
            "immutable-study-v1",
            self._model_2d(),
            PeriodicStudyModelRole.reference,
        )

        with pytest.raises(FrozenInstanceError):
            study.study_id = "replacement"  # type: ignore[misc]

    def test__calculation_studies__use_structure_data_not_subclasses(self) -> None:
        """Keep SQ/HEX/FCC/BCT/DIA/SC identity outside the class hierarchy.

        Notes
        -----
        Each named calculation may bind a stable study identity, but it must compose the
        approved dimension-and-rank classes rather than declaring a crystal-specific
        study or orchestrator subclass.

        """
        repository_root = Path(__file__).resolve().parents[4]
        inventory = (
            (
                "periodic1d_rank2",
                "periodic1d-rank2-band-equivalence-hopping-locality",
                "Periodic1DRank2Study",
                "Periodic1DRank2StudyOrchestrator",
                "compose_study",
            ),
            (
                "periodic2d_rank2_sqr",
                "periodic2d-rank2-sqr-band-equivalence-hopping-locality",
                "Periodic2DRank2Study",
                "Periodic2DRank2StudyOrchestrator",
                "calculate_study",
            ),
            (
                "periodic2d_rank2_hex",
                "periodic2d-rank2-hex-band-equivalence-hopping-locality",
                "Periodic2DRank2Study",
                "Periodic2DRank2StudyOrchestrator",
                "calculate_study",
            ),
            (
                "periodic3d_rank2_fcc",
                "periodic3d-rank2-fcc-band-equivalence-hopping-locality",
                "Periodic3DRank2Study",
                "Periodic3DRank2StudyOrchestrator",
                "calculate_study",
            ),
            (
                "periodic3d_rank2_bct",
                "periodic3d-rank2-bct-band-equivalence-hopping-locality",
                "Periodic3DRank2Study",
                "Periodic3DRank2StudyOrchestrator",
                "calculate_study",
            ),
            (
                "periodic3d_rank2_dia",
                "periodic3d-rank2-dia-band-equivalence-hopping-locality",
                "Periodic3DRank2Study",
                "Periodic3DRank2StudyOrchestrator",
                "calculate_study",
            ),
            (
                "periodic3d_rank2_sc",
                "periodic3d-rank2-sc-band-equivalence-hopping-locality",
                "Periodic3DRank2Study",
                "Periodic3DRank2StudyOrchestrator",
                "calculate_study",
            ),
        )

        for (
            directory,
            expected_id,
            study_name,
            orchestrator_name,
            function_name,
        ) in inventory:
            path = (
                repository_root
                / "calculations"
                / directory
                / "band_equivalence_hopping_locality"
                / "study.py"
            )
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            class_names = tuple(
                node.name for node in tree.body if isinstance(node, ast.ClassDef)
            )
            function_names = tuple(
                node.name for node in tree.body if isinstance(node, ast.FunctionDef)
            )
            imported_names = {
                alias.name
                for node in tree.body
                if isinstance(node, ast.ImportFrom)
                for alias in node.names
            }
            study_ids = tuple(
                node.value.value
                for node in tree.body
                if isinstance(node, ast.AnnAssign)
                and isinstance(node.target, ast.Name)
                and node.target.id == "STUDY_ID"
                and isinstance(node.value, ast.Constant)
                and type(node.value.value) is str
            )

            assert class_names == ()
            assert function_names == (function_name,)
            assert {study_name, orchestrator_name} <= imported_names
            assert study_ids == (expected_id,)
            if function_name == "calculate_study":
                assert any(
                    name.endswith("Rank2HoppingLocalityAnalyzer")
                    for name in imported_names
                )
                assert any(
                    name.endswith("Rank2HoppingLocalityAnalysisRequest")
                    for name in imported_names
                )
