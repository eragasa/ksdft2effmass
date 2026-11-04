"""Adapt KSD Quantum ESPRESSO executable configuration to provider identity.

The adapter projects exact immutable executable-byte and version fields into Project
Koios Simulations' calculator-neutral binding. It performs no filesystem observation,
executable preparation, process invocation, authority decision, compatibility claim,
or scientific validation. KSD retains its QE program role, argument/environment
policy, diagnostic classifier identity, and Workflow correlations.
"""

from __future__ import annotations

from pathlib import Path

from projectkoios.simulations.execution import (
    CalculatorExecutableBinding,
    CalculatorExecutableIdentity,
)

from .contracts import (
    QeExecutableConfiguration,
    QeExecutableKind,
    QeProgram,
)


class QeExecutableBindingAdapter:
    """Project one exact KSD QE configuration into a Simulations binding.

    Notes
    -----
    The fieldless adapter is effect-free. The returned binding only represents an
    expected executable identity at an absolute lexical path. A separate
    ``CalculatorExecutablePreparer`` must observe that path, and later staging or
    process owners must close their own mutable-state boundaries. Neither this adapter
    nor the returned value grants execution authority.
    """

    __slots__ = ()

    def execute(
        self,
        configuration: QeExecutableConfiguration,
        executable_path: Path,
    ) -> CalculatorExecutableBinding:
        """Return the calculator-neutral exact executable binding.

        Parameters
        ----------
        configuration
            Exact KSD QE program, executable kind, version, byte identity, argument,
            environment, and diagnostic-classifier configuration.
        executable_path
            Absolute lexical deployment path. The adapter does not access it.

        Returns
        -------
        CalculatorExecutableBinding
            Project Koios Simulations binding with the exact mapped calculator name,
            version, byte count, SHA-256 digest, and deployment path.

        Raises
        ------
        TypeError
            If ``configuration`` or ``executable_path`` has the wrong semantic type.
        ValueError
            If the path is not absolute and parent-traversal-free or if the represented
            executable byte count is not positive.
        """
        if type(configuration) is not QeExecutableConfiguration:
            raise TypeError("configuration must be QeExecutableConfiguration")
        if not isinstance(executable_path, Path):
            raise TypeError("executable_path must be pathlib.Path")

        content_identity = configuration.executable_content_identity
        return CalculatorExecutableBinding(
            identity=CalculatorExecutableIdentity(
                calculator_name=self._calculator_name(configuration),
                calculator_version=configuration.program_version,
                byte_size=content_identity.byte_count,
                sha256=content_identity.digest,
            ),
            path=executable_path,
        )

    @staticmethod
    def _calculator_name(
        configuration: QeExecutableConfiguration,
    ) -> str:
        """Return the exact provider namespace for one program and executable kind."""
        program_name = "pw.x" if configuration.program is QeProgram.PW else "bands.x"
        if configuration.executable_kind is QeExecutableKind.QUANTUM_ESPRESSO:
            return f"Quantum ESPRESSO {program_name}"
        return f"deterministic fixture for Quantum ESPRESSO {program_name} role"
