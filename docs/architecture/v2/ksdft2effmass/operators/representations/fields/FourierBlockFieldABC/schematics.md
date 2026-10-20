# Schematics

```mermaid
classDiagram
    SquareMatrixFieldABC <|-- FourierBlockFieldABC
    FourierBlockFieldABC <|-- NumpyFourierBlockField
    FiniteTranslationDomain --> NumpyFourierBlockField
```
