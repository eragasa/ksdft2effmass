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
import math
from pathlib import Path
from typing import cast

import pytest

from ksdft2effmass.campaigns.research_monograph import (
    ParticleInBoxConvergenceVerifier,
    ParticleInBoxConvergenceWorkflow,
    ParticleInBoxEigenpairSweepVerifier,
    ParticleInBoxEigenpairSweepWorkflow,
    ParticleInBoxIdentifiabilityVerifier,
    ParticleInBoxIdentifiabilityWorkflow,
    ParticleInBoxNormSweepVerifier,
    ParticleInBoxNormSweepWorkflow,
)
from ksdft2effmass.campaigns.research_monograph.particle_in_box import JsonValue

pytestmark = pytest.mark.software_verification


class TestParticleInBoxAuxiliaryCampaigns:
    """Own software evidence for the auxiliary particle-in-a-box campaigns."""

    def test_artifact__convergence__preserves_retained_numerics(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-AUX-001

        Requirement: The public convergence Workflow preserves the retained numerical
        document and its independent verifier accepts both authored and retained forms.

        Acceptance: After excluding provenance, nonnumeric structure agrees exactly,
        binary64 values are finite, and the verifier independently accepts both
        numerical documents under its channel-specific bounds.
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
        verifier.execute(authored)
        verifier.execute(calculation / "convergence-result.json")

    def test_artifact__eigenpair_sweep__preserves_retained_numerics(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-MONOGRAPH-PIB-AUX-002

        Requirement: The public higher-eigenpair Workflow preserves the retained
        numerical document and independent verification.

        Acceptance: After excluding provenance, nonnumeric structure agrees exactly,
        binary64 values are finite, and the verifier independently accepts both
        numerical documents under its channel-specific bounds.
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

        Acceptance: After excluding provenance, nonnumeric structure agrees exactly,
        binary64 values are finite, and the verifier independently accepts both
        numerical documents under its channel-specific bounds.
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

        Acceptance: After excluding provenance, nonnumeric structure agrees exactly,
        binary64 values are finite, and the verifier independently accepts both
        numerical documents under its channel-specific bounds.
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
        root = Path(__file__).resolve().parents[7]
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
        assert TestParticleInBoxAuxiliaryCampaigns.numerically_compatible(
            authored, retained
        )

    @classmethod
    def numerically_compatible(cls, authored: JsonValue, retained: JsonValue) -> bool:
        """Compare nonnumeric structure exactly and require finite binary64 values."""
        if type(retained) is float:
            return (
                type(authored) is float
                and math.isfinite(authored)
                and math.isfinite(retained)
            )
        if type(authored) is not type(retained):
            return False
        if isinstance(retained, dict):
            return (
                isinstance(authored, dict)
                and authored.keys() == retained.keys()
                and all(
                    cls.numerically_compatible(authored[key], retained[key])
                    for key in retained
                )
            )
        if isinstance(retained, list):
            return (
                isinstance(authored, list)
                and len(authored) == len(retained)
                and all(
                    cls.numerically_compatible(authored_value, retained_value)
                    for authored_value, retained_value in zip(
                        authored, retained, strict=True
                    )
                )
            )
        return authored == retained
