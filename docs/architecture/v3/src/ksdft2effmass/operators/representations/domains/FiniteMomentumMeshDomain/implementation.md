# Implementation

The class is decorated `@final` and `@dataclass(frozen=True, slots=True)` and implements
`FiniteDomainABC`. `__post_init__` performs exact text, mesh, and enum checks. The dataclass
owns the metadata object graph but delegates mesh-array ownership to `CenteredUniformMesh`.
