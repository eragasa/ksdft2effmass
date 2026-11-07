# Implementation

```python
class FiniteDomainABC(ABC):
    @property
    @abstractmethod
    def identity(self) -> str: ...

    @property
    @abstractmethod
    def cardinality(self) -> int: ...
```

The class has empty slots and no constructor. It is public from its defining module and
appears in that module's `__all__`.
