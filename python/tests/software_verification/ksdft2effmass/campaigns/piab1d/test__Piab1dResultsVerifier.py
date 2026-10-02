r"""Software verification of ``Piab1dResultsVerifier``.

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
from pathlib import Path
from typing import cast

import pytest

from ksdft2effmass.campaigns.piab1d import (
    JsonValue,
    Piab1dResidualStudyEvaluator,
    Piab1dResultsVerifier,
    Piab1dStudyInputDeserializer,
    Piab1dStudyResultSerializer,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]
SUT = Piab1dResultsVerifier


class TestPiab1dResultsVerifier:
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

        report = Piab1dResultsVerifier().execute(result, root)

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
        definition = Piab1dStudyInputDeserializer().execute(input_path.read_bytes())
        result = Piab1dResidualStudyEvaluator().execute(definition)
        encoded = Piab1dStudyResultSerializer().execute(
            result,
            input_path,
            calculation / "run_experiment.py",
            root,
        )
        authored = tmp_path / "authored-result.json"
        authored.write_bytes(encoded)

        report = Piab1dResultsVerifier().execute(authored, root)

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
        definition = Piab1dStudyInputDeserializer().execute(input_path.read_bytes())
        result = Piab1dResidualStudyEvaluator().execute(definition)
        authored = tmp_path / "length-two-result.json"
        authored.write_bytes(
            Piab1dStudyResultSerializer().execute(
                result,
                input_path,
                calculation / "run_experiment.py",
                root,
            )
        )

        report = Piab1dResultsVerifier().execute(authored, root)

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
        definition = Piab1dStudyInputDeserializer().execute(input_path.read_bytes())
        result = Piab1dResidualStudyEvaluator().execute(definition)
        authored = tmp_path / "single-point-result.json"
        authored.write_bytes(
            Piab1dStudyResultSerializer().execute(
                result,
                input_path,
                calculation / "run_experiment.py",
                root,
            )
        )

        report = Piab1dResultsVerifier().execute(authored, root)
        boundary_check = next(
            check
            for check in report.numerical_reconstruction.checks
            if check.channel.value == "boundary_realization"
        )

        assert boundary_check.maximum_defect == 0.0
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

        report = Piab1dResultsVerifier().execute(changed, root)

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

        report = Piab1dResultsVerifier().execute(changed, root)
        failed_channels = tuple(
            check.channel.value
            for check in report.numerical_reconstruction.checks
            if not check.passes
        )

        assert report.source_authentication.passes
        assert not report.numerical_reconstruction.passes
        assert failed_channels == ("computed_discrete_spectrum",)
        assert not report.passes

    def test_contract__verification_package_preserves_verifier_identity(self) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-015

        Requirement: The verification package and PIAB1D root expose the class from
        its defining module without an intermediate compatibility module.

        Acceptance: Package and defining-module imports are the same class object as
        the supported PIAB1D root import.
        """
        from ksdft2effmass.campaigns.piab1d.verification import (
            Piab1dResultsVerifier as PackageVerifier,
        )
        from ksdft2effmass.campaigns.piab1d.verification.core import (
            Piab1dResultsVerifier as DefiningVerifier,
        )

        assert Piab1dResultsVerifier is PackageVerifier
        assert Piab1dResultsVerifier is DefiningVerifier

    @pytest.mark.parametrize(
        "encoded",
        ([[True]], [["1.25"]]),
        ids=("boolean", "numeric-string"),
    )
    def test_method__matrix_value__rejects_scalar_coercion(
        self, encoded: JsonValue
    ) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-016

        Requirement: Matrix decoding rejects booleans and numeric strings rather than
        coercing them to binary64 values.

        Acceptance: Each disallowed encoded scalar raises ``TypeError``.
        """
        with pytest.raises(TypeError, match="JSON real"):
            SUT.matrix_value(encoded, "matrix", (1, 1))

    @pytest.mark.parametrize(
        "relative_path",
        ("/tmp/outside.json", "../outside.json"),
        ids=("absolute", "parent-traversal"),
    )
    def test_constructor__source_identity__rejects_nonrelative_paths(
        self, relative_path: str
    ) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-017

        Requirement: A source identity intrinsically owns a normalized repository-
        relative POSIX path.

        Acceptance: Absolute and parent-traversing paths raise ``ValueError``.
        """
        from ksdft2effmass.campaigns.piab1d.verification.source import (
            Piab1dSourceIdentity,
            Piab1dSourceIdentityRole,
        )

        with pytest.raises(ValueError, match="relative POSIX path"):
            Piab1dSourceIdentity(
                Piab1dSourceIdentityRole.INPUT,
                relative_path,
                "0" * 64,
            )

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
