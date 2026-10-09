"""Artifact-owned evidence for canonical matched-extraction ownership."""

import importlib.util
from pathlib import Path

import numpy as np
import pytest

from ksdft2effmass.operators import OperatorRecord
from ksdft2effmass.periodic1d import (
    Periodic1DSupercellOperatorMetadata,
    Periodic1DSupercellOperatorProvenance,
)
from ksdft2effmass.periodic1d.campaign import extraction
from ksdft2effmass.periodic1d.campaign.extraction import matched

pytestmark = pytest.mark.software_verification


class TestCanonicalMatchedExtractionFamily:
    """Verify canonical identity, former-route removal, and row-030 adaptation."""

    def test_artifact__facade__exports_defining_class_objects(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-MATCHED-ROUTE-001."""
        assert (
            extraction.MatchedDefectExtractionWorkflow
            is matched.MatchedDefectExtractionWorkflow
        )
        assert extraction.DefectExerciseInput is matched.DefectExerciseInput

    def test_artifact__former_route__is_absent_without_forwarder(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-MATCHED-ROUTE-002."""
        assert (
            importlib.util.find_spec(
                "ksdft2effmass.campaigns.periodic_1d.defects.matched_extraction"
            )
            is None
        )

    def test_artifact__represented_envelope__uses_general_operator_record(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-MATCHED-ROUTE-003."""
        labels = ("site-0/orbital-0", "site-0/orbital-1")
        metadata = Periodic1DSupercellOperatorMetadata(
            "finite-supercell-space",
            "periodic-1d synthetic supercell",
            "ordered-supercell-basis",
            "site-major orbital-fast orthonormal basis",
            labels,
            ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
            "embedded-one-cell-geometry",
            "periodic along first cell vector",
            "dimensionless Cartesian row lattice vectors",
            "primitive_cell_length",
            "shared_zero",
            "E_G",
            Periodic1DSupercellOperatorProvenance(
                "synthetic-parent", "synthetic-source", "construction", "test"
            ),
        )
        basis = matched.SupercellBasis(
            "finite-supercell-space",
            1,
            2,
            1,
            0.0,
            "canonical-cyclic-sites",
            "low-pair-smooth-frame",
            "not-applicable",
            "canonical",
            "E_G",
            "shared_zero",
            "embedded-one-cell-geometry",
            "accepted-low-pair-composite",
            metadata,
        )
        represented = matched.RepresentedOperator(
            "synthetic-record", basis, np.eye(2, dtype=np.complex128)
        )

        assert isinstance(represented.operator_record, OperatorRecord)
        assert represented.matrix is represented.operator_record.matrix
        assert represented.operator_record.basis.ordering == labels

    def test_artifact__layout__mirrors_source_and_tests(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-MATCHED-ROUTE-004."""
        python_root = Path(__file__).resolve().parents[7]
        relative = Path("ksdft2effmass/periodic1d/campaign/extraction/matched")
        assert (python_root / "src" / relative / "workflow.py").is_file()
        assert (
            python_root
            / "tests"
            / "software_verification"
            / relative
            / "test__MatchedDefectExtractionWorkflow.py"
        ).is_file()
