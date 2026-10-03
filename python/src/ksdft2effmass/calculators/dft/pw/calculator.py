"""Backend-neutral nominal base for plane-wave DFT calculators.

The abstract base expresses only typed application composition. Concrete native
inputs, outputs, diagnostics, executable configuration, and effects remain owned by
external-system integrations. Nominal membership grants no execution authority,
selects no backend, and establishes no physical or numerical equivalence between
backends.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from ksdft2effmass.workflows import TaskExecutionContext


class AbstractPlaneWaveCalculator[InputT, OutputT](ABC):
    """Provide one exact plane-wave DFT calculator operation.

    The input and output types remain concrete integration-owned records. Application
    composition fixes both type parameters for one injected backend operation. This
    ABC is not a backend registry, executable-discovery mechanism, authority service,
    or universal electronic-structure interface.

    Notes
    -----
    A caller may invoke this capability only after the separately owned Workflow
    authority and dispatch gates admit the exact operation. Implementations return new
    immutable outputs and must not mutate the input or execution context.
    """

    __slots__ = ()

    @abstractmethod
    def execute(
        self,
        simulation_input: InputT,
        context: TaskExecutionContext,
    ) -> OutputT:
        """Execute one already-admitted concrete calculator operation.

        Parameters
        ----------
        simulation_input
            Exact integration-owned native input record selected by application
            composition.
        context
            Immutable Workflow execution context admitted for this operation. The
            context carries correlation identities but does not authorize an external
            effect.

        Returns
        -------
        OutputT
            New immutable integration-owned output for the exact input and context.
        """
        raise NotImplementedError
