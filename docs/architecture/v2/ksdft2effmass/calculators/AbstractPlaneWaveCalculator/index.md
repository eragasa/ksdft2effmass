# `AbstractPlaneWaveCalculator`

## Status

**Accepted nominal-ABC migration contract; implementation pending.**

## Responsibility

`AbstractPlaneWaveCalculator[InputT, OutputT](ABC, Generic[InputT, OutputT])` is the
backend-neutral nominal calculator boundary for one exact plane-wave operation. Its
abstract `execute(simulation_input, context) -> OutputT` signature preserves exact
integration-owned input and output types.

The ABC performs no implementation discovery and grants no execution authority.
`TaskExecutionContext` supplies correlation only. A concrete implementation that can
cause an external effect must remain behind the separately authorized simulation
control boundary; this ABC is not a substitute for
`AbstractSimulationDispatchEffect`.

## Nominal closure

Concrete calculators inherit explicitly. Matching method names without inheritance do
not establish membership. Virtual subclass registration, structural fallback,
registries, and compatibility aliases are prohibited.

`LocalQuantumEspressoExecutor` belongs to the authority-bearing dispatch-effect route
and is not admitted as a calculator merely because it exposes an incompatible
`execute` method.

## Related architecture

- [Schematic](schematic.md)
- [Repository-wide migration](../../protocol-to-abc-migration.md)
- [`AbstractSimulationDispatchEffect`](../../workflows/AbstractSimulationDispatchEffect/index.md)
