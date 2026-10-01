r"""Software verification of public particle-in-a-box auxiliary campaigns.

Evidence profile: routine

Bounded artifact scope: convergence, higher-eigenpair, norm, and identifiability
Workflows, retained numerical payloads, and independent verifiers.

Facet and represented meaning

The artifact consists of four public Workflows and their independent public verifier
classes behind thin calculation-directory adapters.

Intrinsic and cross-object scope

Retained numerical compatibility, current provenance production, and independent
verification are included.

VVUQ and scientific exclusions

These tests preserve declared illustrative numerical-verification artifacts. They do
not establish semiconductor validation, uncertainty quantification, or human
acceptance.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import cast

import pytest

from ksdft2effmass.campaigns.piab1d import (
    JsonValue,
    ParticleInBoxConvergenceVerifier,
    ParticleInBoxConvergenceWorkflow,
    ParticleInBoxEigenpairSweepVerifier,
    ParticleInBoxEigenpairSweepWorkflow,
    ParticleInBoxIdentifiabilityVerifier,
    ParticleInBoxIdentifiabilityWorkflow,
    ParticleInBoxNormSweepVerifier,
    ParticleInBoxNormSweepWorkflow,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestParticleInBoxAuxiliaryCampaigns:
    """Own software evidence for the auxiliary particle-in-a-box campaigns."""

    def test_artifact__convergence__preserves_retained_numerics(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-AUX-001

        Requirement: The public convergence Workflow preserves the retained numerical
        document and its independent verifier reports authored and retained forms.

        Acceptance: Authored and retained numerical payloads are equal after excluding
        provenance; both typed reports pass separate source-authentication and
        numerical-reconstruction outcomes.
        """
        root, calculation = self.paths()
        encoded = ParticleInBoxConvergenceWorkflow().execute(
            calculation / "convergence-input.json",
            calculation / "run_convergence.py",
            root,
        )
        self.assert_numerical_payload(encoded, calculation / "convergence-result.json")
        authored = tmp_path / "convergence.json"
        authored.write_bytes(encoded)
        verifier = ParticleInBoxConvergenceVerifier()
        authored_report = verifier.execute(authored, root)
        retained_report = verifier.execute(
            calculation / "convergence-result.json", root
        )

        assert authored_report.source_authentication.passes
        assert authored_report.numerical_reconstruction.passes
        assert authored_report.passes
        assert retained_report.source_authentication.passes
        assert retained_report.numerical_reconstruction.passes
        assert retained_report.passes
        assert (
            authored_report.numerical_reconstruction.refinement_count
            == retained_report.numerical_reconstruction.refinement_count
        )
        authored_numerical = authored_report.numerical_reconstruction
        retained_numerical = retained_report.numerical_reconstruction
        authored_observations = authored_numerical.reconstructed_mode_observation_count
        retained_observations = retained_numerical.reconstructed_mode_observation_count
        assert authored_observations == retained_observations

    def test_artifact__convergence_report__separates_failure_channels(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-AUX-005

        Requirement: Convergence source authentication, numerical reconstruction, and
        aggregate disposition remain distinct.

        Acceptance: An input-digest change fails only source authentication, while a
        relative-error change fails only numerical reconstruction; both fail their
        aggregate dispositions.
        """
        root, calculation = self.paths()
        retained_path = calculation / "convergence-result.json"
        retained = cast(
            dict[str, JsonValue], json.loads(retained_path.read_text(encoding="utf-8"))
        )

        source_payload = cast(
            dict[str, JsonValue], json.loads(json.dumps(retained, allow_nan=False))
        )
        provenance = cast(dict[str, JsonValue], source_payload["provenance"])
        provenance["input_sha256"] = "0" * 64
        source_path = tmp_path / "convergence-source-mismatch.json"
        source_path.write_text(
            json.dumps(source_payload, indent=2, sort_keys=True, allow_nan=False)
            + "\n",
            encoding="utf-8",
        )

        numerical_payload = cast(
            dict[str, JsonValue], json.loads(json.dumps(retained, allow_nan=False))
        )
        refinements = cast(list[JsonValue], numerical_payload["refinements"])
        first_refinement = cast(dict[str, JsonValue], refinements[0])
        modes = cast(list[JsonValue], first_refinement["modes"])
        first_mode = cast(dict[str, JsonValue], modes[0])
        first_mode["relative_error"] = cast(float, first_mode["relative_error"]) + 0.1
        numerical_path = tmp_path / "convergence-numerical-mismatch.json"
        numerical_path.write_text(
            json.dumps(numerical_payload, indent=2, sort_keys=True, allow_nan=False)
            + "\n",
            encoding="utf-8",
        )

        verifier = ParticleInBoxConvergenceVerifier()
        source_report = verifier.execute(source_path, root)
        numerical_report = verifier.execute(numerical_path, root)

        assert not source_report.source_authentication.passes
        assert source_report.numerical_reconstruction.passes
        assert not source_report.passes
        assert numerical_report.source_authentication.passes
        assert not numerical_report.numerical_reconstruction.passes
        assert not numerical_report.passes

    def test_artifact__convergence_report__remains_active_under_optimized_python(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-AUX-006

        Requirement: Convergence numerical and aggregate dispositions remain active
        when Python removes language-level assertions under optimization.

        Acceptance: A ``python -O`` subprocess reports source pass, numerical failure,
        and aggregate failure after a relative-error perturbation.
        """
        root, calculation = self.paths()
        retained = cast(
            dict[str, JsonValue],
            json.loads(
                (calculation / "convergence-result.json").read_text(encoding="utf-8")
            ),
        )
        refinements = cast(list[JsonValue], retained["refinements"])
        first_refinement = cast(dict[str, JsonValue], refinements[0])
        modes = cast(list[JsonValue], first_refinement["modes"])
        first_mode = cast(dict[str, JsonValue], modes[0])
        first_mode["relative_error"] = cast(float, first_mode["relative_error"]) + 0.1
        changed = tmp_path / "optimized-convergence-mismatch.json"
        changed.write_text(
            json.dumps(retained, indent=2, sort_keys=True, allow_nan=False) + "\n",
            encoding="utf-8",
        )
        command = (
            "from pathlib import Path; "
            "from ksdft2effmass.campaigns.piab1d import "
            "ParticleInBoxConvergenceVerifier; "
            "report=ParticleInBoxConvergenceVerifier().execute("
            "Path(__import__('sys').argv[1]), Path(__import__('sys').argv[2])); "
            "print(report.source_authentication.passes, "
            "report.numerical_reconstruction.passes, report.passes); "
            "raise SystemExit(0 if report.source_authentication.passes "
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

    def test_contract__verification_package_preserves_convergence_identity(
        self,
    ) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-AUX-007

        Requirement: The verification package owns the convergence verifier while the
        supported PIAB1D root route preserves exact object identity.

        Acceptance: Package, defining-module, and root imports resolve to one class.
        """
        from ksdft2effmass.campaigns.piab1d.verification import (
            ParticleInBoxConvergenceVerifier as PackageVerifier,
        )
        from ksdft2effmass.campaigns.piab1d.verification.convergence import (
            ParticleInBoxConvergenceVerifier as DefiningVerifier,
        )

        assert ParticleInBoxConvergenceVerifier is PackageVerifier
        assert ParticleInBoxConvergenceVerifier is DefiningVerifier

    def test_artifact__eigenpair_sweep__preserves_retained_numerics(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-AUX-002

        Requirement: The public higher-eigenpair Workflow preserves the retained
        numerical document and independent verification.

        Acceptance: Authored and retained numerical payloads are equal after excluding
        provenance, and the verifier accepts both documents.
        """
        root, calculation = self.paths()
        encoded = ParticleInBoxEigenpairSweepWorkflow().execute(
            calculation / "eigenpair-sweep-input.json",
            calculation / "run_eigenpair_sweep.py",
            root,
        )
        self.assert_numerical_payload(
            encoded, calculation / "eigenpair-sweep-result.json"
        )
        authored = tmp_path / "eigenpairs.json"
        authored.write_bytes(encoded)
        verifier = ParticleInBoxEigenpairSweepVerifier()
        verifier.execute(authored)
        verifier.execute(calculation / "eigenpair-sweep-result.json")

    def test_artifact__norm_sweep__preserves_retained_numerics(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-AUX-003

        Requirement: The public norm Workflow preserves the retained numerical
        document and independent verification.

        Acceptance: Authored and retained numerical payloads are equal after excluding
        provenance, and the verifier accepts both documents.
        """
        root, calculation = self.paths()
        encoded = ParticleInBoxNormSweepWorkflow().execute(
            calculation / "norm-sweep-input.json",
            calculation / "run_norm_sweep.py",
            root,
        )
        self.assert_numerical_payload(encoded, calculation / "norm-sweep-result.json")
        authored = tmp_path / "norms.json"
        authored.write_bytes(encoded)
        verifier = ParticleInBoxNormSweepVerifier()
        verifier.execute(authored)
        verifier.execute(calculation / "norm-sweep-result.json")

    def test_artifact__identifiability__preserves_retained_numerics(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-AUX-004

        Requirement: The public identifiability Workflow preserves the retained
        numerical document and independent verification.

        Acceptance: Authored and retained numerical payloads are equal after excluding
        provenance, and the verifier accepts both documents.
        """
        root, calculation = self.paths()
        encoded = ParticleInBoxIdentifiabilityWorkflow().execute(
            calculation / "identifiability-input.json",
            calculation / "result.json",
            calculation / "run_identifiability.py",
            root,
        )
        self.assert_numerical_payload(
            encoded, calculation / "identifiability-result.json"
        )
        authored = tmp_path / "identifiability.json"
        authored.write_bytes(encoded)
        verifier = ParticleInBoxIdentifiabilityVerifier()
        verifier.execute(authored)
        verifier.execute(calculation / "identifiability-result.json")

    @staticmethod
    def paths() -> tuple[Path, Path]:
        """Return the repository and maintained calculation roots."""
        root = Path(__file__).resolve().parents[6]
        return root, root / "calculations" / "research-monograph" / "particle-in-box"

    @staticmethod
    def assert_numerical_payload(encoded: bytes, retained_path: Path) -> None:
        """Assert equality after excluding implementation provenance."""
        authored = cast(dict[str, JsonValue], json.loads(encoded.decode("utf-8")))
        retained = cast(
            dict[str, JsonValue], json.loads(retained_path.read_text(encoding="utf-8"))
        )
        authored.pop("provenance")
        retained.pop("provenance")
        assert authored == retained
