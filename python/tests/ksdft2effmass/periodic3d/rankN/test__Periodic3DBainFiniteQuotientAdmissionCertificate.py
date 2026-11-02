"""Fail-closed software binding for the exact Bain quotient criterion."""

from __future__ import annotations

from pathlib import Path
from typing import cast

import pytest

from ksdft2effmass.periodic3d.rankN.bain_quotient_admission import (
    BainPeriodTriple,
    Periodic3DBainFiniteQuotientAdmissionCertificate,
    periodic3d_bain_finite_quotient_is_admitted,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic3DBainFiniteQuotientAdmissionCertificate:
    """Verify the KSD runtime gate without claiming theorem reproduction."""

    def test_rankn_package_initializer_remains_inert(
        self,
        repository_root: Path,
    ) -> None:
        initializer = (
            repository_root
            / "python"
            / "src"
            / "ksdft2effmass"
            / "periodic3d"
            / "rankN"
            / "__init__.py"
        )

        assert initializer.read_text(encoding="utf-8") == (
            '"""Periodic three-dimensional arbitrary-finite-rank capability '
            'namespace."""\n'
        )

    def test_admits_positive_cubic_and_supported_mixed_periods(self) -> None:
        for period in range(1, 17):
            periods = (period, period, period)
            assert periodic3d_bain_finite_quotient_is_admitted(periods)
            certificate = Periodic3DBainFiniteQuotientAdmissionCertificate(periods)
            assert certificate.periods == periods

        certificate = Periodic3DBainFiniteQuotientAdmissionCertificate((2, 6, 6))

        assert certificate.first_period == 2
        assert certificate.second_period == 6
        assert certificate.third_period == 6

    @pytest.mark.parametrize(
        "periods",
        [
            (0, 1, 1),
            (1, 0, 0),
            (1, 2, 3),
            (4, 6, 6),
            (-1, 1, 1),
            cast(BainPeriodTriple, (True, 1, 1)),
            cast(BainPeriodTriple, ("1", 1, 1)),
            cast(BainPeriodTriple, (1, 1)),
            cast(BainPeriodTriple, [1, 1, 1]),
        ],
    )
    def test_predicate_rejects_unsupported_periods(
        self,
        periods: BainPeriodTriple,
    ) -> None:
        assert not periodic3d_bain_finite_quotient_is_admitted(periods)

    def test_certificate_fails_closed_with_specific_input_errors(self) -> None:
        with pytest.raises(TypeError, match="three-tuple"):
            Periodic3DBainFiniteQuotientAdmissionCertificate(
                cast(BainPeriodTriple, (1, 1))
            )
        with pytest.raises(TypeError, match="built-in integers"):
            Periodic3DBainFiniteQuotientAdmissionCertificate(
                cast(BainPeriodTriple, (True, 1, 1))
            )
        with pytest.raises(ValueError, match="positive"):
            Periodic3DBainFiniteQuotientAdmissionCertificate((0, 1, 1))
        with pytest.raises(ValueError, match="N2 == N3"):
            Periodic3DBainFiniteQuotientAdmissionCertificate((1, 2, 3))
        with pytest.raises(ValueError, match="N1 to divide N2"):
            Periodic3DBainFiniteQuotientAdmissionCertificate((4, 6, 6))

    def test_certificate_binds_fixed_matrices_and_formal_source(self) -> None:
        certificate = Periodic3DBainFiniteQuotientAdmissionCertificate((3, 6, 6))

        assert certificate.BAIN_TO_FCC_MATRIX == (
            (1, 1, 0),
            (0, 0, 1),
            (0, -1, 0),
        )
        assert certificate.FCC_TO_BAIN_MATRIX == (
            (1, 0, 1),
            (0, 0, -1),
            (0, 1, 0),
        )
        assert (
            certificate.FORMAL_MERGE_COMMIT
            == "b98d23fe23bb5bc940c6be4cfcbc79c3569c45e7"
        )
        assert certificate.FORMAL_PULL_REQUEST == 58
        assert certificate.FORMAL_ADMISSION_THEOREM.endswith(
            "bainMixedModuliAdmissionCertificate_iff"
        )
        assert certificate.FORMAL_BIJECTION_THEOREM.endswith(
            "bain_integerDiagonalLattice_quotientMap_bijective"
        )
