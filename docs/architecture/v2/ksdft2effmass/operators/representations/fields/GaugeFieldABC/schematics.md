# Schematics

```mermaid
classDiagram
    SquareMatrixFieldABC <|-- GaugeFieldABC
    GaugeFieldABC <|-- NumpyGaugeField
    GaugeFieldABC ..> Evidence : checked separately
```
