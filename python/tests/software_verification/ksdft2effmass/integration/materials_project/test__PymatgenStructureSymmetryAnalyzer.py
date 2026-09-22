r"""Software verification of ``PymatgenStructureSymmetryAnalyzer``.

Evidence profile: claim_bearing

Bounded artifact scope: canonical snapshot decoding, explicit symmetry tolerances,
pymatgen analysis adaptation, and closed immutable symmetry output.

Facet and represented meaning

The module verifies the adapter from one exact retained metal-unit silicon structure
to one tolerance- and analyzer-version-qualified symmetry record.

Intrinsic and cross-object scope

``PymatgenStructureSymmetryAnalyzer`` is the sole system under test. Pymatgen owns the
space-group algorithm; the project adapter owns input units, explicit parameters, and
result representation.

VVUQ and scientific exclusions

This is software verification against the externally sourced mp-149 snapshot. It does
not establish the production PBE-relaxed lattice, independent crystallographic
validation, uncertainty quantification, or electronic-structure correctness.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from ksdft2effmass.integration.materials_project import (
    PymatgenStructureSymmetryAnalyzer,
)

pytestmark = pytest.mark.software_verification
SUT = PymatgenStructureSymmetryAnalyzer


class TestPymatgenStructureSymmetryAnalyzer:
    """Own software evidence for explicit pymatgen symmetry adaptation."""

    @staticmethod
    def snapshot_path() -> Path:
        """Return the exact retained external-reference snapshot path."""
        return (
            Path(__file__).resolve().parents[6]
            / "calculations/bulk-silicon/materials-project/mp-149.structure.json"
        )

    def test_method__execute__returns_tolerance_qualified_diamond_symmetry(
        self,
    ) -> None:
        """Evidence ID: SV-PYMATGEN-STRUCTURE-SYMMETRY-001

        Requirement: Canonical mp-149 geometry maps to a complete immutable symmetry
        record carrying the exact analyzer tolerances and version.

        Method: Analyze the retained credential-free snapshot locally at 0.01 angstrom
        positional tolerance and five-degree angular tolerance.

        Oracle: The Materials Project identifies mp-149 as cubic diamond silicon in
        space group Fd-3m (number 227); its two primitive sites are equivalent.

        Acceptance: Symbol, number, Hall symbol, crystal and point groups, Wyckoff
        symbols, equivalent atoms, tolerances, and analyzer version are explicit.

        Interpretation: Failure identifies snapshot decoding, unit adaptation, parameter
        retention, or pymatgen-result mapping drift.

        Limitations: Agreement with the source classification is not an independent
        scientific validation of the structure or tolerance sensitivity.
        """
        result = SUT().execute(
            self.snapshot_path().read_bytes(),
            symprec_angstrom=0.01,
            angle_tolerance_degree=5.0,
        )

        assert result.space_group_symbol == "Fd-3m"
        assert result.space_group_number == 227
        assert result.hall_symbol == "F 4d 2 3 -1d"
        assert result.crystal_system == "cubic"
        assert result.point_group_symbol == "m-3m"
        assert result.wyckoff_symbols == ("a", "a")
        assert result.equivalent_atoms == (0, 0)
        assert result.symprec_angstrom == 0.01
        assert result.angle_tolerance_degree == 5.0
        assert result.analyzer_version
