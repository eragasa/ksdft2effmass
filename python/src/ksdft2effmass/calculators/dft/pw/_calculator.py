"""Backend-neutral structural port for plane-wave DFT calculators.

The port expresses only typed application composition. Concrete native inputs,
outputs, diagnostics, executable configuration, and effects remain owned by external
system integrations. Protocol conformance grants no execution authority, selects no
backend, and establishes no physical or numerical equivalence between backends.
"""

from __future__ import annotations

from typing import Protocol, TypeVar, runtime_checkable

from ksdft2effmass.workflows import TaskExecutionContext

_InputT = TypeVar("_InputT", contravariant=True)
_OutputT = TypeVar("_OutputT", covariant=True)


@runtime_checkable
class PlaneWaveCalculator(Protocol[_InputT, _OutputT]):
    """Provide one exact plane-wave DFT calculator operation.

    The input and output types remain concrete integration-owned records. Application
    composition fixes both type parameters for one injected backend operation. This
    protocol is not a backend registry, executable-discovery mechanism, authority
    service, or universal electronic-structure interface.

    Notes
    -----
    A caller may invoke the port only after the separately owned Workflow authority
    and dispatch gates admit the exact operation. Implementations return new immutable
    outputs and must not mutate the input or execution context.
    """

    def execute(
        self,
        simulation_input: _InputT,
        context: TaskExecutionContext,
    ) -> _OutputT:
        """Execute one already-admitted concrete calculator operation.

        Parameters
        ----------
        simulation_input
            Exact integration-owned native input record selected by application
            composition.
        context
            Immutable Workflow execution context admitted for this operation. The
            context carries correlation and authority-related identities but does not
            by itself authorize an external effect.

        Returns
        -------
        _OutputT
            New immutable integration-owned output for the exact input and context.

        Notes
        -----
        Implementations must independently enforce the applicable executor-boundary
        authorization and confinement checks before performing an external effect.
        """
        ...
