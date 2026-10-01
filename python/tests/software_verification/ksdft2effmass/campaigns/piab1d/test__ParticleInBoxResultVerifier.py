r"""Software verification of ``ParticleInBoxResultVerifier``.

Evidence profile: routine

Bounded artifact scope: independent retained/current version-one result verifier and
its typed source-authentication and numerical-reconstruction report.

Facet and represented meaning

The verifier reconstructs finite identities without importing the implementation it
checks and preserves historical runner compatibility explicitly.

Intrinsic and cross-object scope

Historical provenance admission, current source authentication, independent numerical
checks, and their separate aggregate dispositions are included.

VVUQ and scientific exclusions

A pass establishes only the declared finite numerical identities, not scientific
validation, uncertainty quantification, or human acceptance.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import cast

import pytest

from ksdft2effmass.campaigns.piab1d import (
    JsonValue,
    ParticleInBoxResidualStudyEvaluator,
    ParticleInBoxResultVerifier,
    ParticleInBoxStudyInputDeserializer,
    ParticleInBoxStudyResultSerializer,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]
SUT = ParticleInBoxResultVerifier


class TestParticleInBoxResultVerifier:
    """Own software evidence for the independent result verifier."""

    def test_method__execute__accepts_retained_historical_result(self) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-004

        Requirement: The independent verifier admits the immutable historical runner
        identity without requiring current implementation hashes.

        Acceptance: Verification of the maintained retained result completes without
        an exception.
        """
        root = Path(__file__).resolve().parents[6]
        result = (
            root
            / "calculations"
            / "research-monograph"
            / "particle-in-box"
            / "result.json"
        )

        report = ParticleInBoxResultVerifier().execute(result, root)

        assert report.passes
        assert report.source_authentication.passes
        assert report.numerical_reconstruction.passes
        assert tuple(
            identity.disposition.value
            for identity in report.source_authentication.identities
        ) == (
            "matched_repository_content",
            "recognized_historical_identity",
        )
        assert tuple(
            check.channel.value for check in report.numerical_reconstruction.checks
        ) == (
            "dirichlet_hamiltonian",
            "discrete_closed_form",
            "continuum_closed_form",
            "discrete_to_continuum_ratio",
            "computed_discrete_spectrum",
            "retained_basis_orthonormality",
            "projector_definition",
            "projector_idempotency",
            "embedded_reduction",
            "retained_coordinate_reduction",
            "retained_coordinate_diagonalization",
            "consistent_compression",
            "unmatched_compression",
            "discarded_sector",
            "boundary_realization",
        )

    def test_method__execute__authenticates_current_authored_result(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-012

        Requirement: A newly authored result authenticates its exact input, runner,
        and complete implementation inventory separately from numerical reconstruction.

        Acceptance: Every declared source matches current repository bytes, the
        implementation inventory agrees, and source, numerical, and aggregate
        dispositions pass.
        """
        root = Path(__file__).resolve().parents[6]
        calculation = root / "calculations" / "research-monograph" / "particle-in-box"
        input_path = calculation / "input.json"
        definition = ParticleInBoxStudyInputDeserializer().execute(
            input_path.read_bytes()
        )
        result = ParticleInBoxResidualStudyEvaluator().execute(definition)
        encoded = ParticleInBoxStudyResultSerializer().execute(
            result,
            input_path,
            calculation / "run_experiment.py",
            root,
        )
        authored = tmp_path / "authored-result.json"
        authored.write_bytes(encoded)

        report = ParticleInBoxResultVerifier().execute(authored, root)

        assert report.source_authentication.implementation_inventory_matches
        assert all(
            identity.disposition.value == "matched_repository_content"
            for identity in report.source_authentication.identities
        )
        assert report.source_authentication.passes
        assert report.numerical_reconstruction.passes
        assert report.passes

    def test_method__execute__reconstructs_nonunit_box_length(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-013

        Requirement: Independent reconstruction uses the represented box length in
        both finite-difference and continuum energy scales rather than assuming one.

        Acceptance: A currently authored dimensionless ``L=2`` result passes every
        source, numerical, and aggregate report channel.
        """
        root = Path(__file__).resolve().parents[6]
        calculation = root / "calculations" / "research-monograph" / "particle-in-box"
        input_path = Path(__file__).with_name("resources") / (
            "piab1d-length-two-input.json"
        )
        definition = ParticleInBoxStudyInputDeserializer().execute(
            input_path.read_bytes()
        )
        result = ParticleInBoxResidualStudyEvaluator().execute(definition)
        authored = tmp_path / "length-two-result.json"
        authored.write_bytes(
            ParticleInBoxStudyResultSerializer().execute(
                result,
                input_path,
                calculation / "run_experiment.py",
                root,
            )
        )

        report = ParticleInBoxResultVerifier().execute(authored, root)

        assert report.source_authentication.passes
        assert report.numerical_reconstruction.passes
        assert report.passes

    def test_method__execute__reconstructs_single_point_boundary_reference(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-014

        Requirement: A one-coordinate grid has no distinct endpoints to connect in the
        cyclic comparison reference and therefore has a zero boundary residual.

        Acceptance: A currently authored one-coordinate result passes the boundary
        channel and the complete source, numerical, and aggregate report.
        """
        root = Path(__file__).resolve().parents[6]
        calculation = root / "calculations" / "research-monograph" / "particle-in-box"
        input_path = Path(__file__).with_name("resources") / (
            "piab1d-single-point-input.json"
        )
        definition = ParticleInBoxStudyInputDeserializer().execute(
            input_path.read_bytes()
        )
        result = ParticleInBoxResidualStudyEvaluator().execute(definition)
        authored = tmp_path / "single-point-result.json"
        authored.write_bytes(
            ParticleInBoxStudyResultSerializer().execute(
                result,
                input_path,
                calculation / "run_experiment.py",
                root,
            )
        )

        report = ParticleInBoxResultVerifier().execute(authored, root)
        boundary_check = next(
            check
            for check in report.numerical_reconstruction.checks
            if check.channel.value == "boundary_realization"
        )

        assert boundary_check.maximum_absolute_defect == 0.0
        assert boundary_check.passes
        assert report.source_authentication.passes
        assert report.numerical_reconstruction.passes
        assert report.passes

    def test_method__execute__separates_source_and_numerical_dispositions(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-009

        Requirement: Source authentication, numerical reconstruction, and aggregate
        disposition remain distinct in the typed verification report.

        Acceptance: Changing only the recorded input digest fails source
        authentication and the aggregate while all numerical channels still pass.
        """
        root = Path(__file__).resolve().parents[6]
        retained = (
            root
            / "calculations"
            / "research-monograph"
            / "particle-in-box"
            / "result.json"
        )
        payload = cast(
            dict[str, JsonValue], json.loads(retained.read_text(encoding="utf-8"))
        )
        provenance = cast(dict[str, JsonValue], payload["provenance"])
        provenance["input_sha256"] = "0" * 64
        changed = tmp_path / "source-mismatch.json"
        changed.write_text(
            json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
            encoding="utf-8",
        )

        report = ParticleInBoxResultVerifier().execute(changed, root)

        assert not report.source_authentication.passes
        assert report.numerical_reconstruction.passes
        assert not report.passes

    def test_method__execute__reports_numerical_disagreement_without_source_failure(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-010

        Requirement: A represented numerical disagreement produces a failed numerical
        report rather than being misclassified as a source-identity failure.

        Acceptance: Perturbing one computed eigenvalue fails exactly the computed
        spectrum channel and the aggregate while source authentication still passes.
        """
        root = Path(__file__).resolve().parents[6]
        retained = (
            root
            / "calculations"
            / "research-monograph"
            / "particle-in-box"
            / "result.json"
        )
        payload = cast(
            dict[str, JsonValue], json.loads(retained.read_text(encoding="utf-8"))
        )
        spectra = cast(dict[str, JsonValue], payload["spectra"])
        computed = cast(list[JsonValue], spectra["computed_discrete"])
        computed[0] = cast(float, computed[0]) + 1.0
        changed = tmp_path / "numerical-mismatch.json"
        changed.write_text(
            json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
            encoding="utf-8",
        )

        report = ParticleInBoxResultVerifier().execute(changed, root)
        failed_channels = tuple(
            check.channel.value
            for check in report.numerical_reconstruction.checks
            if not check.passes
        )

        assert report.source_authentication.passes
        assert not report.numerical_reconstruction.passes
        assert failed_channels == ("computed_discrete_spectrum",)
        assert not report.passes

    def test_method__execute__rejects_invalid_schema_under_optimized_python(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-008

        Requirement: Verification requirements remain active when Python removes
        language-level assertions under optimization.

        Acceptance: A retained payload changed to schema version 999 is rejected by a
        ``python -O`` subprocess with a schema-version error.
        """
        root = Path(__file__).resolve().parents[6]
        retained = (
            root
            / "calculations"
            / "research-monograph"
            / "particle-in-box"
            / "result.json"
        )
        invalid = tmp_path / "invalid-result.json"
        invalid.write_bytes(
            retained.read_bytes().replace(
                b'\n  "schema_version": 1,\n',
                b'\n  "schema_version": 999,\n',
                1,
            )
        )
        command = (
            "from pathlib import Path; "
            "from ksdft2effmass.campaigns.piab1d import "
            "ParticleInBoxResultVerifier; "
            "ParticleInBoxResultVerifier().execute(Path(__import__('sys').argv[1]), "
            "Path(__import__('sys').argv[2]))"
        )

        completed = subprocess.run(
            [sys.executable, "-O", "-c", command, str(invalid), str(root)],
            check=False,
            capture_output=True,
            text=True,
        )

        assert completed.returncode != 0
        assert "schema_version" in completed.stderr

    def test_method__execute__reports_failure_under_optimized_python(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-011

        Requirement: Numerical verification and aggregate disposition remain active
        when Python removes language-level assertions under optimization.

        Acceptance: A ``python -O`` subprocess reports source pass, numerical failure,
        and aggregate failure for a one-unit computed-spectrum perturbation.
        """
        root = Path(__file__).resolve().parents[6]
        retained = (
            root
            / "calculations"
            / "research-monograph"
            / "particle-in-box"
            / "result.json"
        )
        payload = cast(
            dict[str, JsonValue], json.loads(retained.read_text(encoding="utf-8"))
        )
        spectra = cast(dict[str, JsonValue], payload["spectra"])
        computed = cast(list[JsonValue], spectra["computed_discrete"])
        computed[0] = cast(float, computed[0]) + 1.0
        changed = tmp_path / "optimized-numerical-mismatch.json"
        changed.write_text(
            json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
            encoding="utf-8",
        )
        command = (
            "from pathlib import Path; "
            "from ksdft2effmass.campaigns.piab1d import "
            "ParticleInBoxResultVerifier; "
            "report=ParticleInBoxResultVerifier().execute("
            "Path(__import__('sys').argv[1]), Path(__import__('sys').argv[2])); "
            "print(report.source_authentication.passes, "
            "report.numerical_reconstruction.passes, report.passes); "
            "raise SystemExit(0 if "
            "report.source_authentication.passes "
            "and not report.numerical_reconstruction.passes "
            "and not report.passes else 1)"
        )

        completed = subprocess.run(
            [sys.executable, "-O", "-c", command, str(changed), str(root)],
            check=False,
            capture_output=True,
            text=True,
        )

        assert completed.returncode == 0
        assert completed.stdout.strip() == "True False False"

    def test_contract__verification_package_preserves_verifier_identity(self) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-015

        Requirement: The verification package owns the defining core verifier while
        established package and compatibility routes preserve exact object identity.

        Acceptance: Canonical package, defining-module, and compatibility imports are
        the same class object as the supported PIAB1D root import.
        """
        from ksdft2effmass.campaigns.piab1d.core_verification import (
            ParticleInBoxResultVerifier as CompatibilityVerifier,
        )
        from ksdft2effmass.campaigns.piab1d.verification import (
            ParticleInBoxResultVerifier as PackageVerifier,
        )
        from ksdft2effmass.campaigns.piab1d.verification.core import (
            ParticleInBoxResultVerifier as DefiningVerifier,
        )

        assert ParticleInBoxResultVerifier is PackageVerifier
        assert ParticleInBoxResultVerifier is DefiningVerifier
        assert ParticleInBoxResultVerifier is CompatibilityVerifier

    def test_artifact__dependency__excludes_particle_in_box_implementation(
        self,
    ) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-007

        Requirement: The verifier must not import the campaign or model implementation
        whose output it verifies.

        Acceptance: Every defining source in the verification package excludes imports
        rooted at the particle-in-a-box producer modules.
        """
        root = Path(__file__).resolve().parents[6]
        verification_root = (
            root
            / "python"
            / "src"
            / "ksdft2effmass"
            / "campaigns"
            / "piab1d"
            / "verification"
        )
        sources = tuple(sorted(verification_root.glob("*.py")))

        assert sources
        for source in sources:
            source_text = source.read_text(encoding="utf-8")
            assert "from ksdft2effmass.analysis" not in source_text
            assert "from ksdft2effmass.operators" not in source_text
            assert "from .particle_in_box import" not in source_text
