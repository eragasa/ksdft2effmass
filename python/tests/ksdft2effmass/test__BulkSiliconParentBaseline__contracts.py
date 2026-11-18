"""Software checks for the selected silicon parent and retained-source boundary.

These checks establish document-contract consistency only. They do not authenticate
new pseudopotential artifacts, establish convergence, or validate silicon physics.
"""

from pathlib import Path

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestBulkSiliconParentBaseline:
    """Keep current family selection separate from exact artifacts and old results."""

    def test_common_baseline__matches_accepted_library_selection(
        self, repository_root: Path
    ) -> None:
        authority = (
            repository_root / "specification/dft-pseudopotential-library/v1/index.md"
        ).read_text(encoding="utf-8")
        assert (
            "| Primary common B/Si/P baseline | PseudoDojo ONCVPSP v0.5 | PBE | "
            "Scalar-relativistic | Stringent | PSP8 | UPF2 |"
        ) in authority
        paths = (
            "specification/ksdft2Effmass.physical-specification.v1.md",
            "specification/ksdft2Effmass.numerical-specification.v1.md",
            "calculations/Si/bulk/protocol/decisions/"
            "qe-simulation-design-from-rankn.md",
        )
        for path in paths:
            text = " ".join(
                (repository_root / path).read_text(encoding="utf-8").split()
            )
            assert "PseudoDojo ONCVPSP v0.5" in text
            assert "PBE" in text
            assert "scalar-relativistic" in text
            assert "stringent" in text
            assert "dft-pseudopotential-library/v1/index.md" in text
            assert "UPF2" in text
            assert "PSP8" in text

    def test_current_artifact__does_not_borrow_historical_identity(
        self, repository_root: Path
    ) -> None:
        numerical = (
            repository_root
            / "specification/ksdft2Effmass.numerical-specification.v1.md"
        ).read_text(encoding="utf-8")
        current, historical = numerical.split(
            "### Historical artifact identity", maxsplit=1
        )
        for digest in (
            "bfbd01ccd4b67584dcf19a490a76e9b688c25026775ce2f4a4b6a13f900dad81",
            "39822757f53f36e3bf3bfb779356152a8d3f21199c7db9dd5a931e5d18c45282",
        ):
            assert digest not in current
            assert digest in historical
        assert "remain pending before use" in " ".join(current.split())
        assert "Historical identity only" in historical
        assert "not repeated by this reconciliation" in historical

    def test_dopant_spin_branches__keep_final_boron_soc_separate(
        self, repository_root: Path
    ) -> None:
        physical = " ".join(
            (
                repository_root
                / "specification/ksdft2Effmass.physical-specification.v1.md"
            )
            .read_text(encoding="utf-8")
            .split()
        )
        assert "collinear spin-polarized, scalar-relativistic, non-SOC" in physical
        assert "PseudoDojo ONCVPSP v0.4, PBE, fully relativistic, stringent" in physical
        assert "matching fully relativistic Si host" in physical
        assert (
            "scalar-relativistic non-SOC B:Si calculation may be retained only "
            "as an early method-development branch"
        ) in physical

    def test_new_parent_plan__does_not_inherit_retained_sssp_qualification(
        self, repository_root: Path
    ) -> None:
        plan = (
            repository_root / "calculations/Si/bulk/protocol/decisions/"
            "qe-simulation-design-from-rankn.md"
        ).read_text(encoding="utf-8")
        qualification = plan.split("### QE0:", maxsplit=1)[1].split(
            "### QE2:", maxsplit=1
        )[0]
        assert "PseudoDojo v0.5" in qualification
        assert "Exact artifact acquisition and verification remain pending" in (
            " ".join(qualification.split())
        )
        assert "No setting is inherited" in qualification
        assert "SSSP `42/336 Ry` occurrence" in qualification
        assert "SSSP 1.3.0 PBE Efficiency" in plan
        assert "SSSP v2.0 Precision" in " ".join(plan.split())
        assert "No Quantum ESPRESSO execution is authorized" in plan
        assert "not a prerequisite for parent qualification" in plan

    def test_convergence_tolerances__remain_numerical_not_material_acceptance(
        self, repository_root: Path
    ) -> None:
        numerical = (
            repository_root
            / "specification/ksdft2Effmass.numerical-specification.v1.md"
        ).read_text(encoding="utf-8")
        for row in (
            "| Total energy per Si atom | `1e-5 Ry/atom` between successive "
            "accepted settings |",
            "| Equilibrium lattice constant | `1e-4 Å` or the larger fitted "
            "uncertainty |",
            "| Indirect Kohn--Sham gap | `1 meV` between successive accepted "
            "settings |",
            "| Conduction-valley position along the selected high-symmetry line | "
            "`0.002` in fractional path coordinate |",
            "| Longitudinal electron effective mass | `0.5%` relative change |",
            "| Transverse electron effective mass | `0.5%` relative change |",
            "| Withheld-point band energies for the selected bulk validation set | "
            "`1 meV` maximum absolute change at fixed band/path labeling |",
        ):
            assert row in numerical
        assert "They are not scientific validation against experiment" in numerical
