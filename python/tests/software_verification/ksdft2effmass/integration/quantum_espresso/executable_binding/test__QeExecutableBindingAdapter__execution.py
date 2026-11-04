r"""Software verification of exact QE executable-binding adaptation.

Evidence profile: routine

Bounded artifact scope: pure projection from one KSD QE executable configuration to
one Project Koios Simulations calculator executable binding.

Facet and represented meaning

The tests verify exact program/kind namespaces, version and byte identity retention,
lexical path handling, and rejection of provider-invalid byte counts.

VVUQ and scientific exclusions

The tests perform no filesystem observation or process invocation and establish no
calculator compatibility, numerical verification, scientific validation, uncertainty
quantification, authority, or scientific acceptance.
"""

from pathlib import Path

import pytest
from projectkoios.simulations.execution import (
    CalculatorExecutableBinding,
    CalculatorExecutableIdentity,
)

from ksdft2effmass.integration.quantum_espresso import (
    QeDiagnosticClassifierIdentity,
    QeExecutableBindingAdapter,
    QeExecutableConfiguration,
    QeExecutableConfigurationIdentity,
    QeExecutableKind,
    QeProgram,
)
from ksdft2effmass.workflows.artifacts import ArtifactContentIdentity

pytestmark = pytest.mark.software_verification


class TestQeExecutableBindingAdapter:
    """Own software evidence for calculator-neutral executable binding."""

    @staticmethod
    def _configuration(
        *,
        program: QeProgram = QeProgram.PW,
        executable_kind: QeExecutableKind = (QeExecutableKind.QUANTUM_ESPRESSO),
        program_version: str = "7.5",
        byte_count: int = 17,
    ) -> QeExecutableConfiguration:
        return QeExecutableConfiguration(
            identity=QeExecutableConfigurationIdentity("qe-executable-configuration"),
            program=program,
            executable_kind=executable_kind,
            executable_content_identity=ArtifactContentIdentity(
                algorithm="sha256",
                digest="a" * 64,
                byte_count=byte_count,
            ),
            program_version=program_version,
            argument_suffix=(),
            environment_additions=(),
            classifier_identity=QeDiagnosticClassifierIdentity(
                "qe-diagnostic-classifier"
            ),
            contract_version="qe-executable-configuration:1",
        )

    def test__QeExecutableBindingAdapter__maps_exact_pw_identity(
        self, tmp_path: Path
    ) -> None:
        """Retain exact actual-QE program version, size, digest, and path."""
        configuration = self._configuration()
        executable_path = tmp_path / "pw.x"

        result = QeExecutableBindingAdapter().execute(configuration, executable_path)

        assert type(result) is CalculatorExecutableBinding
        assert result == CalculatorExecutableBinding(
            identity=CalculatorExecutableIdentity(
                calculator_name="Quantum ESPRESSO pw.x",
                calculator_version="7.5",
                byte_size=17,
                sha256="a" * 64,
            ),
            path=executable_path,
        )

    def test__QeExecutableBindingAdapter__separates_fixture_namespace(
        self, tmp_path: Path
    ) -> None:
        """Never represent deterministic fixture bytes as a QE executable."""
        configuration = self._configuration(
            program=QeProgram.BANDS,
            executable_kind=QeExecutableKind.DETERMINISTIC_FIXTURE,
            program_version="fixture-1",
        )

        result = QeExecutableBindingAdapter().execute(
            configuration, tmp_path / "bands-fixture"
        )

        assert result.identity.calculator_name == (
            "deterministic fixture for Quantum ESPRESSO bands.x role"
        )
        assert result.identity.calculator_version == "fixture-1"

    def test__QeExecutableBindingAdapter__does_not_observe_path(
        self, tmp_path: Path
    ) -> None:
        """Construct a lexical binding even when the represented path is absent."""
        executable_path = tmp_path / "absent" / "pw.x"

        result = QeExecutableBindingAdapter().execute(
            self._configuration(), executable_path
        )

        assert not executable_path.exists()
        assert result.path == executable_path

    def test__QeExecutableBindingAdapter__rejects_invalid_provider_binding(
        self, tmp_path: Path
    ) -> None:
        """Reject nonpositive executable size and nonabsolute deployment paths."""
        adapter = QeExecutableBindingAdapter()

        with pytest.raises(ValueError, match="byte_size must be a positive integer"):
            adapter.execute(
                self._configuration(byte_count=0),
                tmp_path / "empty-pw.x",
            )
        with pytest.raises(ValueError, match="path must be absolute"):
            adapter.execute(self._configuration(), Path("pw.x"))
