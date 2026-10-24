r"""Software verification of public PIAB1D auxiliary studies.

Evidence profile: routine

Bounded artifact scope: convergence, higher-eigenpair, norm, and identifiability
Workflows, retained numerical payloads, and independent verifiers.

Facet and represented meaning

The artifact consists of four public Workflows and their independent public verifier
classes behind thin calculation-directory adapters.

Intrinsic and cross-object scope

Retained numerical compatibility, explicitly isolated eigensolver-residual roundoff
changes, current provenance production, and independent verification are included.

VVUQ and scientific exclusions

These tests preserve declared illustrative numerical-verification artifacts. They do
not establish semiconductor validation, uncertainty quantification, or human
acceptance.
"""

import json
from pathlib import Path
from typing import cast

import pytest

from ksdft2effmass.model_systems.piab1d import JsonValue

from ..convergence import Piab1dConvergenceWorkflow
from ..eigenpair_sweep import Piab1dEigenpairSweepWorkflow
from ..identifiability import Piab1dIdentifiabilityWorkflow
from ..norm_sweep import Piab1dNormSweepWorkflow
from ..verification import (
    Piab1dConvergenceVerifier,
    Piab1dEigenpairSweepVerifier,
    Piab1dIdentifiabilityVerifier,
    Piab1dNormSweepVerifier,
)

pytestmark = [pytest.mark.software_verification, pytest.mark.expensive]


class TestPiab1dAuxiliaryStudies:
    """Own software evidence for the auxiliary PIAB1D studies."""

    def test_artifact__convergence__preserves_retained_numerics(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-AUX-001

        Requirement: The public convergence Workflow preserves the retained numerical
        document and its independent verifier accepts both authored and retained forms.

        Acceptance: Authored and retained numerical payloads are equal after excluding
        provenance, and the verifier accepts both documents.
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
        verifier = Piab1dConvergenceVerifier()
        verifier.execute(authored)
        verifier.execute(calculation / "convergence-result.json")

    def test_artifact__eigenpair_sweep__preserves_retained_numerics(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-AUX-002

        Requirement: The migrated higher-eigenpair Workflow preserves every retained
        field except algebraic residual roundoff owned by the current PhysKit solver.

        Acceptance: Non-residual numerical fields remain exact, both residual profiles
        satisfy the declared bound, and the verifier accepts both documents.
        """
        root, calculation = self.paths()
        encoded = Piab1dEigenpairSweepWorkflow().execute(
            calculation / "eigenpair-sweep-input.json",
            calculation / "run_eigenpair_sweep.py",
            root,
        )
        self.assert_eigenpair_migration_payload(
            encoded, calculation / "eigenpair-sweep-result.json"
        )
        authored = tmp_path / "eigenpairs.json"
        authored.write_bytes(encoded)
        verifier = Piab1dEigenpairSweepVerifier()
        verifier.execute(authored)
        verifier.execute(calculation / "eigenpair-sweep-result.json")

    def test_artifact__norm_sweep__preserves_retained_numerics(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-AUX-003

        Requirement: The migrated norm Workflow preserves every retained field except
        norms of algebraic eigensolver residuals owned by the current PhysKit solver.

        Acceptance: Non-residual numerical fields remain exact, both residual profiles
        satisfy the declared bound, and the verifier accepts both documents.
        """
        root, calculation = self.paths()
        encoded = Piab1dNormSweepWorkflow().execute(
            calculation / "norm-sweep-input.json",
            calculation / "run_norm_sweep.py",
            root,
        )
        self.assert_norm_migration_payload(
            encoded, calculation / "norm-sweep-result.json"
        )
        authored = tmp_path / "norms.json"
        authored.write_bytes(encoded)
        verifier = Piab1dNormSweepVerifier()
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
        verifier = Piab1dIdentifiabilityVerifier()
        verifier.execute(authored)
        verifier.execute(calculation / "identifiability-result.json")

    @staticmethod
    def paths() -> tuple[Path, Path]:
        """Return the repository and maintained calculation roots."""
        root = Path(__file__).resolve().parents[4]
        return root, root / "calculations" / "piab1d"

    @staticmethod
    def payloads(
        encoded: bytes, retained_path: Path
    ) -> tuple[dict[str, JsonValue], dict[str, JsonValue]]:
        """Return authored and retained payloads without provenance."""
        authored = cast(dict[str, JsonValue], json.loads(encoded.decode("utf-8")))
        retained = cast(
            dict[str, JsonValue], json.loads(retained_path.read_text(encoding="utf-8"))
        )
        authored.pop("provenance")
        retained.pop("provenance")
        return authored, retained

    @classmethod
    def assert_numerical_payload(cls, encoded: bytes, retained_path: Path) -> None:
        """Assert exact numerical equality after excluding provenance."""
        authored, retained = cls.payloads(encoded, retained_path)
        assert authored == retained

    @classmethod
    def assert_eigenpair_migration_payload(
        cls, encoded: bytes, retained_path: Path
    ) -> None:
        """Isolate the expected owner-migration change to residual roundoff."""
        authored, retained = cls.payloads(encoded, retained_path)
        for payload in (authored, retained):
            grids = cast(list[JsonValue], payload["grids"])
            for grid_value in grids:
                grid = cast(dict[str, JsonValue], grid_value)
                records = cast(list[JsonValue], grid["eigenpairs"])
                residuals = []
                for record_value in records:
                    record = cast(dict[str, JsonValue], record_value)
                    residuals.append(
                        float(cast(float, record.pop("scaled_eigenpair_residual")))
                    )
                maximum = float(
                    cast(float, grid.pop("maximum_scaled_eigenpair_residual"))
                )
                assert maximum == max(residuals)
                assert all(0.0 <= value < 1.0e-13 for value in residuals)
        assert authored == retained

    @classmethod
    def assert_norm_migration_payload(cls, encoded: bytes, retained_path: Path) -> None:
        """Isolate norm changes to the algebraic eigensolver-residual record."""
        authored, retained = cls.payloads(encoded, retained_path)
        for payload in (authored, retained):
            grids = cast(list[JsonValue], payload["grids"])
            for grid_value in grids:
                grid = cast(dict[str, JsonValue], grid_value)
                residual = cast(
                    dict[str, JsonValue],
                    grid.pop("full_eigenpair_algebraic_residual"),
                )
                relative = cast(
                    dict[str, JsonValue], residual["relative_to_hamiltonian"]
                )
                assert set(relative) == {"frobenius", "spectral", "maximum_entry"}
                assert all(
                    0.0 <= float(cast(float, value)) < 1.0e-13
                    for value in relative.values()
                )
        assert authored == retained
