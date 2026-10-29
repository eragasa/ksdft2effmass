# Schematics

## Ownership and dependency direction

```mermaid
flowchart TB
    S[ksdft2effmass.serialization] --> V[ksdft2effmass.visualizations]
    A[Root verification authentication contract] --> V
    V --> P[PIAB1D visualizations]
    V --> Q[QHO1D visualizations]
    V --> M[Mathieu1D visualizations]
    V --> F[Periodic1D Fourier-locality visualizations]
    V --> C[Periodic1D composite-alignment visualizations]

    P -. no reverse import .-> X[Model and family result owners]
    Q -. no reverse import .-> X
    M -. no reverse import .-> X
    F -. no reverse import .-> X
    C -. no reverse import .-> X
```

The dotted arrows express the prohibited reverse dependency: the root visualization
package does not import a family owner.

## Authentication and rendering sequence

```mermaid
sequenceDiagram
    participant B as Exact result bytes
    participant V as Family verifier
    participant D as Family visualization data
    participant Z as Family visualizer
    participant R as PNG renderer

    B->>V: bind and independently verify
    V->>D: derive typed projection
    D->>V: canonical projection bytes
    V->>V: retain projection SHA-256
    D->>Z: bind projection
    V->>Z: bind passing verification
    Z->>Z: authenticate exact projection digest
    Z->>R: bind enum member, figure, and DPI
    R->>R: draw, encode, close, admit PNG
    R-->>Z: immutable PNG value
```

## Type ownership

```mermaid
classDiagram
    class BaseVisualizationData
    class BaseVisualizationVerification
    class BasePlot
    class BaseSubplot
    class BaseFigure
    class BaseFigureRenderer
    class PngFigureRenderer
    class PngVisualization
    class BaseVisualizer
    class FamilyVisualizationData
    class FamilyVerification
    class FamilyVisualizer

    FamilyVisualizationData --|> BaseVisualizationData
    FamilyVerification --|> BaseVisualizationVerification
    PngFigureRenderer --|> BaseFigureRenderer
    PngFigureRenderer --> BaseFigure
    PngFigureRenderer --> PngVisualization
    FamilyVisualizer --|> BaseVisualizer
    FamilyVisualizer --> FamilyVisualizationData
    FamilyVisualizer --> FamilyVerification
```
