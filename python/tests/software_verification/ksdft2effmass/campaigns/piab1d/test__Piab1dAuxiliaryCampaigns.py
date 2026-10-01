r"""Software verification of public particle-in-a-box auxiliary campaigns.

Evidence profile: routine

Bounded artifact scope: convergence, eigenpair-sweep, norm, and identifiability
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
from pathlib import Path
from typing import cast

import pytest

from ksdft2effmass.campaigns.piab1d import (
    JsonValue,
    Piab1dConvergenceResultsVerifier,
    Piab1dConvergenceWorkflow,
    Piab1dEigenpairSweepResultsVerifier,
    Piab1dEigenpairSweepWorkflow,
    Piab1dIdentifiabilityResultsVerifier,
    Piab1dIdentifiabilityWorkflow,
    Piab1dNormSweepResultsVerifier,
    Piab1dNormSweepWorkflow,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestPiab1dAuxiliaryCampaigns:
    """Own software evidence for the auxiliary PIAB1D campaigns."""

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
        encoded = Piab1dConvergenceWorkflow().execute(
            calculation / "convergence-input.json",
            calculation / "run_convergence.py",
            root,
        )
        self.assert_numerical_payload(encoded, calculation / "convergence-result.json")
        authored = tmp_path / "convergence.json"
        authored.write_bytes(encoded)
        verifier = Piab1dConvergenceResultsVerifier()
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
            authored_report.numerical_reconstruction.count("refinements")
            == retained_report.numerical_reconstruction.count("refinements")
            == 6
        )
        authored_numerical = authored_report.numerical_reconstruction
        retained_numerical = retained_report.numerical_reconstruction
        authored_observations = authored_numerical.count("mode_observations")
        retained_observations = retained_numerical.count("mode_observations")
        assert authored_observations == retained_observations == 36

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

        verifier = Piab1dConvergenceResultsVerifier()
        source_report = verifier.execute(source_path, root)
        numerical_report = verifier.execute(numerical_path, root)

        assert not source_report.source_authentication.passes
        assert source_report.numerical_reconstruction.passes
        assert not source_report.passes
        assert numerical_report.source_authentication.passes
        assert not numerical_report.numerical_reconstruction.passes
        assert not numerical_report.passes

    def test_contract__verification_package_preserves_convergence_identity(
        self,
    ) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-AUX-007

        Requirement: The verification package owns the convergence verifier while the
        supported PIAB1D root route preserves exact object identity.

        Acceptance: Package, defining-module, and root imports resolve to one class.
        """
        from ksdft2effmass.campaigns.piab1d.verification import (
            Piab1dConvergenceResultsVerifier as PackageVerifier,
        )
        from ksdft2effmass.campaigns.piab1d.verification.convergence import (
            Piab1dConvergenceResultsVerifier as DefiningVerifier,
        )

        assert Piab1dConvergenceResultsVerifier is PackageVerifier
        assert Piab1dConvergenceResultsVerifier is DefiningVerifier

    def test_artifact__eigenpair_sweep__preserves_retained_numerics(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-AUX-002

        Requirement: The public eigenpair-sweep Workflow preserves the retained
        numerical document and typed independent verification.

        Acceptance: Authored and retained numerical payloads are equal after excluding
        provenance; both reports pass source and numerical outcomes and derive the same
        grid, eigenpair, and fixed-mode-series counts from decoded collections.
        """
        root, calculation = self.paths()
        encoded = Piab1dEigenpairSweepWorkflow().execute(
            calculation / "eigenpair-sweep-input.json",
            calculation / "run_eigenpair_sweep.py",
            root,
        )
        self.assert_numerical_payload(
            encoded, calculation / "eigenpair-sweep-result.json"
        )
        authored = tmp_path / "eigenpairs.json"
        authored.write_bytes(encoded)
        verifier = Piab1dEigenpairSweepResultsVerifier()
        authored_report = verifier.execute(authored, root)
        retained_report = verifier.execute(
            calculation / "eigenpair-sweep-result.json", root
        )

        assert authored_report.source_authentication.passes
        assert authored_report.numerical_reconstruction.passes
        assert authored_report.passes
        assert retained_report.source_authentication.passes
        assert retained_report.numerical_reconstruction.passes
        assert retained_report.passes
        authored_numerical = authored_report.numerical_reconstruction
        retained_numerical = retained_report.numerical_reconstruction
        authored_counts = (
            authored_numerical.count("grids"),
            authored_numerical.count("eigenpairs"),
            authored_numerical.count("fixed_mode_series"),
        )
        retained_counts = (
            retained_numerical.count("grids"),
            retained_numerical.count("eigenpairs"),
            retained_numerical.count("fixed_mode_series"),
        )
        assert authored_counts == retained_counts == (6, 504, 3)

    def test_artifact__eigenpair_report__separates_failure_channels(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-AUX-008

        Requirement: Eigenpair-sweep source authentication, numerical reconstruction,
        and aggregate disposition remain distinct.

        Acceptance: An input-digest change fails only source authentication, while a
        computed-energy change fails only numerical reconstruction; both fail their
        aggregate dispositions.
        """
        root, calculation = self.paths()
        retained_path = calculation / "eigenpair-sweep-result.json"
        retained = cast(
            dict[str, JsonValue], json.loads(retained_path.read_text(encoding="utf-8"))
        )
        source_payload = cast(
            dict[str, JsonValue], json.loads(json.dumps(retained, allow_nan=False))
        )
        provenance = cast(dict[str, JsonValue], source_payload["provenance"])
        provenance["input_sha256"] = "0" * 64
        source_path = tmp_path / "eigenpair-source-mismatch.json"
        source_path.write_text(
            json.dumps(source_payload, indent=2, sort_keys=True, allow_nan=False)
            + "\n",
            encoding="utf-8",
        )

        numerical_payload = cast(
            dict[str, JsonValue], json.loads(json.dumps(retained, allow_nan=False))
        )
        grids = cast(list[JsonValue], numerical_payload["grids"])
        first_grid = cast(dict[str, JsonValue], grids[0])
        eigenpairs = cast(list[JsonValue], first_grid["eigenpairs"])
        first_eigenpair = cast(dict[str, JsonValue], eigenpairs[0])
        first_eigenpair["computed_energy"] = (
            cast(float, first_eigenpair["computed_energy"]) + 1.0
        )
        numerical_path = tmp_path / "eigenpair-numerical-mismatch.json"
        numerical_path.write_text(
            json.dumps(numerical_payload, indent=2, sort_keys=True, allow_nan=False)
            + "\n",
            encoding="utf-8",
        )

        verifier = Piab1dEigenpairSweepResultsVerifier()
        source_report = verifier.execute(source_path, root)
        numerical_report = verifier.execute(numerical_path, root)

        assert not source_report.source_authentication.passes
        assert source_report.numerical_reconstruction.passes
        assert not source_report.passes
        assert numerical_report.source_authentication.passes
        assert not numerical_report.numerical_reconstruction.passes
        assert not numerical_report.passes

    def test_contract__verification_package_preserves_eigenpair_identity(self) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-AUX-010

        Requirement: The verification package owns the eigenpair-sweep verifier while
        the supported PIAB1D root route preserves exact object identity.

        Acceptance: Package, defining-module, and root imports resolve to one class.
        """
        from ksdft2effmass.campaigns.piab1d.verification import (
            Piab1dEigenpairSweepResultsVerifier as PackageVerifier,
        )
        from ksdft2effmass.campaigns.piab1d.verification.eigenpair_sweep import (
            Piab1dEigenpairSweepResultsVerifier as DefiningVerifier,
        )

        assert Piab1dEigenpairSweepResultsVerifier is PackageVerifier
        assert Piab1dEigenpairSweepResultsVerifier is DefiningVerifier

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
        encoded = Piab1dNormSweepWorkflow().execute(
            calculation / "norm-sweep-input.json",
            calculation / "run_norm_sweep.py",
            root,
        )
        self.assert_numerical_payload(encoded, calculation / "norm-sweep-result.json")
        authored = tmp_path / "norms.json"
        authored.write_bytes(encoded)
        verifier = Piab1dNormSweepResultsVerifier()
        authored_report = verifier.execute(authored, root)
        retained_report = verifier.execute(calculation / "norm-sweep-result.json", root)
        assert authored_report.source_authentication.passes
        assert authored_report.numerical_reconstruction.passes
        assert authored_report.passes
        assert retained_report.passes
        assert authored_report.numerical_reconstruction.count("grids") == 6

    def test_artifact__norm_sweep__reports_changed_analytical_norm(
        self, tmp_path: Path
    ) -> None:
        """A changed analytical norm produces a numerical failure report."""
        root, calculation = self.paths()
        payload = cast(
            dict[str, JsonValue],
            json.loads(
                (calculation / "norm-sweep-result.json").read_text(encoding="utf-8")
            ),
        )
        grids = cast(list[JsonValue], payload["grids"])
        first = cast(dict[str, JsonValue], grids[0])
        residuals = cast(dict[str, JsonValue], first["operator_residuals"])
        unmatched = cast(dict[str, JsonValue], residuals["unmatched_compression"])
        raw = cast(dict[str, JsonValue], unmatched["raw"])
        raw["maximum_entry"] = cast(float, raw["maximum_entry"]) + 1.0
        changed = tmp_path / "changed-norm-sweep.json"
        changed.write_text(json.dumps(payload), encoding="utf-8")

        report = Piab1dNormSweepResultsVerifier().execute(changed, root)
        assert report.source_authentication.passes
        assert not report.numerical_reconstruction.passes
        assert not report.passes

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
        encoded = Piab1dIdentifiabilityWorkflow().execute(
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
        verifier = Piab1dIdentifiabilityResultsVerifier()
        authored_report = verifier.execute(authored, root)
        retained_report = verifier.execute(
            calculation / "identifiability-result.json", root
        )
        assert authored_report.source_authentication.passes
        assert authored_report.numerical_reconstruction.passes
        assert authored_report.passes
        assert retained_report.passes
        assert authored_report.numerical_reconstruction.count("model_classes") == 4

    def test_artifact__identifiability__reports_changed_fitted_norm(
        self, tmp_path: Path
    ) -> None:
        """A changed fitted norm produces a numerical failure report."""
        root, calculation = self.paths()
        payload = cast(
            dict[str, JsonValue],
            json.loads(
                (calculation / "identifiability-result.json").read_text(
                    encoding="utf-8"
                )
            ),
        )
        fits = cast(dict[str, JsonValue], payload["model_class_fits"])
        scalar = cast(dict[str, JsonValue], fits["scalar_identity"])
        scalar["unexplained_frobenius_norm"] = (
            cast(float, scalar["unexplained_frobenius_norm"]) + 1.0
        )
        changed = tmp_path / "changed-identifiability.json"
        changed.write_text(json.dumps(payload), encoding="utf-8")

        report = Piab1dIdentifiabilityResultsVerifier().execute(changed, root)
        assert report.source_authentication.passes
        assert not report.numerical_reconstruction.passes
        assert not report.passes

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
