"""Software verification of ``Periodic1DFiniteHoppingToyModel``.

Evidence profile: routine

Bounded artifact scope: nominal one-dimensional toy-model membership, stable identity,
ordered finite hopping blocks, matrix ownership, units, and Hermiticity relation.

Facet and represented meaning
-----------------------------
The model represents one configured finite-range periodic hopping family rather than a
campaign, encoded document, or individual represented Bloch fiber.

Intrinsic and cross-object scope
--------------------------------
Exact model role and dimension, immutable block state, strict matrix scalar types,
ordered displacement coverage, and pairwise Hermiticity are covered.

VVUQ and scientific exclusions
------------------------------
Inputs are synthetic test data. Passing establishes software behavior only, not a
material Hamiltonian, numerical verification, scientific validation, or uncertainty
quantification.
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt
import pytest

import ksdft2effmass.periodic1d.campaign.model.toy_defects as legacy_toy_defects
import ksdft2effmass.periodic1d.campaign.model.toy_defects.hopping as legacy_hopping
from ksdft2effmass.periodic import (
    Periodic1DModel,
    PeriodicModel,
    PeriodicModelRole,
    PeriodicToyModelCatalog,
)
from ksdft2effmass.periodic1d import (
    Periodic1DFiniteHoppingToyModel,
    Periodic1DHoppingBlock,
)

pytestmark = pytest.mark.software_verification


class TestPeriodic1DFiniteHoppingToyModel:
    """Own software evidence for the canonical finite-hopping toy parent."""

    @staticmethod
    def make_model() -> Periodic1DFiniteHoppingToyModel:
        """Return one scalar nearest-neighbor synthetic toy model."""
        return Periodic1DFiniteHoppingToyModel(
            model_id="test.periodic1d.finite-hopping",
            blocks=(
                Periodic1DHoppingBlock(-1, np.asarray([[-1.0]], dtype=np.float64)),
                Periodic1DHoppingBlock(0, np.asarray([[0.5]], dtype=np.float64)),
                Periodic1DHoppingBlock(1, np.asarray([[-1.0]], dtype=np.float64)),
            ),
            energy_unit="dimensionless",
            hermiticity_tolerance=1.0e-14,
        )

    def test_construction__identity__has_nominal_dimension_and_toy_role(self) -> None:
        """Evidence ID: SV-PERIODIC1D-HOPPING-MODEL-001

        Requirement: The configured finite-hopping parent has stable identity, nominal
        one-dimensional membership, and the exact toy role.

        Acceptance: Public hierarchy, identity, dimension, and role equal the contract.
        """
        model = self.make_model()

        assert isinstance(model, PeriodicModel)
        assert isinstance(model, Periodic1DModel)
        assert model.model_id == "test.periodic1d.finite-hopping"
        assert model.spatial_dimension == 1
        assert model.model_role is PeriodicModelRole.TOY
        assert model.orbital_count == 1
        catalog = PeriodicToyModelCatalog((model,))
        assert catalog.model_ids == (model.model_id,)
        assert catalog.spatial_dimensions == (1,)

    def test_construction__blocks__owns_ordered_nonwriteable_complex_matrices(
        self,
    ) -> None:
        """Evidence ID: SV-PERIODIC1D-HOPPING-MODEL-002

        Requirement: Hopping order is semantic and matrices are defensively stored as
        finite non-writeable C-contiguous ``complex128`` arrays.

        Acceptance: Displacements remain ``(-1, 0, 1)`` and every storage invariant
        equals the independently declared contract.
        """
        model = self.make_model()

        assert tuple(block.displacement_cells for block in model.blocks) == (-1, 0, 1)
        for block in model.blocks:
            assert block.matrix.dtype == np.complex128
            assert block.matrix.flags.c_contiguous
            assert not block.matrix.flags.writeable

    @pytest.mark.parametrize(
        "matrix",
        (
            pytest.param(np.asarray([[True]], dtype=np.bool_), id="boolean_matrix"),
            pytest.param(np.asarray([["1.0"]]), id="numeric_string_matrix"),
        ),
    )
    def test_construction__matrix__rejects_coercible_nonscientific_scalars(
        self,
        matrix: npt.NDArray[np.generic],
    ) -> None:
        """Evidence ID: SV-PERIODIC1D-HOPPING-MODEL-003

        Requirement: Public hopping matrices reject Boolean and numeric-string arrays
        rather than coercing them to complex coefficients.

        Acceptance: Each explicit semantic partition raises ``TypeError``.
        """
        with pytest.raises(TypeError, match="matrix dtype must be"):
            Periodic1DHoppingBlock(0, matrix)  # type: ignore[arg-type]

    def test_construction__model_id__rejects_empty_identity(self) -> None:
        """Evidence ID: SV-PERIODIC1D-HOPPING-MODEL-004

        Requirement: Every configured scientific model has a nonempty stable identity.

        Acceptance: Empty identity construction raises ``ValueError``.
        """
        model = self.make_model()
        with pytest.raises(ValueError, match="model_id must be nonempty"):
            Periodic1DFiniteHoppingToyModel(
                "",
                model.blocks,
                model.energy_unit,
                model.hermiticity_tolerance,
            )

    def test_construction__hermiticity__rejects_unpaired_hopping(self) -> None:
        """Evidence ID: SV-PERIODIC1D-HOPPING-MODEL-005

        Requirement: Every directed hopping block has its Hermitian opposite partner.

        Acceptance: A zero-and-positive-only family raises ``ValueError``.
        """
        with pytest.raises(ValueError, match="Hermiticity"):
            Periodic1DFiniteHoppingToyModel(
                "test.periodic1d.unpaired",
                (
                    Periodic1DHoppingBlock(0, np.asarray([[0.5]], dtype=np.complex128)),
                    Periodic1DHoppingBlock(
                        1, np.asarray([[-1.0]], dtype=np.complex128)
                    ),
                ),
                "dimensionless",
                1.0e-14,
            )

    def test_public_api__campaign_route__does_not_export_migrated_model(self) -> None:
        """Evidence ID: SV-PERIODIC1D-HOPPING-MODEL-006

        Requirement: Canonical ownership is ``ksdft2effmass.periodic1d`` without a
        campaign-owned compatibility alias.

        Acceptance: The former campaign package exports neither migrated public name.
        """
        assert "Periodic1DFiniteHoppingToyModel" not in legacy_toy_defects.__all__
        assert "Periodic1DHoppingBlock" not in legacy_toy_defects.__all__
        assert not hasattr(legacy_toy_defects, "Periodic1DFiniteHoppingToyModel")
        assert not hasattr(legacy_toy_defects, "Periodic1DHoppingBlock")
        assert not hasattr(legacy_hopping, "Periodic1DFiniteHoppingToyModel")
        assert not hasattr(legacy_hopping, "Periodic1DHoppingBlock")
