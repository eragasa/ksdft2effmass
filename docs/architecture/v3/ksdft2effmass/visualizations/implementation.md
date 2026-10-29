# Implementation

## Typed projection boundary

`BaseVisualizationData` owns final `to_dict`, `from_dict`, `to_json`, and `from_json`
behavior through the shared typed-value codec. A family projection implements only its
exact typed mapping and reconstruction. Generic code does not inspect, flatten, rename,
or supply defaults for scientific fields.

Projection bytes are canonical scientific inputs to presentation authentication. They
are not a filesystem artifact contract and do not establish that the source calculation
is scientifically valid.

## Authentication boundary

A root verification interface supplies exactly two behaviors required by generic
visualization code:

1. whether the complete concrete verification passed; and
2. the SHA-256 digest of the authenticated canonical projection bytes.

`BaseModelAnalysisVerification` implements that interface for the current families.
`BaseVisualizer` accepts the root interface rather than importing a model-system type.
This prevents the root visualization package from depending outward on
`model_systems`.

Authentication compares the digest of `data.to_json()` with the digest retained by the
verification aggregate and fails closed before figure construction. It does not trust a
caller-authored digest or a stored pass label.

## Figure composition

The composition layers remain separate:

- `BasePlot.draw(axis)` owns one data-to-mark relation;
- `BaseSubplot.draw(axis)` owns axis-local composition and presentation;
- `BaseFigure.draw()` owns layout and figure-wide presentation;
- `BaseFigureRenderer.visualize()` owns conversion to an admitted visualization; and
- `BaseVisualizer.visualize()` owns the complete authenticated family inventory.

A family may use a direct figure action when decomposition into smaller plot/subplot
actions would not create a cohesive reusable owner. Empty marker classes and generic
helpers are not introduced merely to satisfy the layering vocabulary.

## Rendering and PNG admission

`PngFigureRenderer` binds a closed plot-enum member, a concrete figure action, and a
positive integer DPI. Its terminal `visualize()` operation draws the figure, encodes PNG
bytes in memory, closes the Matplotlib figure on both success and failure, and constructs
`PngVisualization`.

`PngVisualization` requires:

- an enum member with a safe nonempty `.png` basename;
- immutable built-in `bytes`;
- successful decoding as a nonempty PNG image; and
- the fixed `image/png` media type.

Image decoding establishes container admission only. Pixel equivalence, typography,
scientific interpretation, and cross-platform byte identity require separate evidence.

## Family package rule

Each family `visualizations/` package owns:

```text
visualizations/
├── __init__.py
├── data.py
├── inventory.py
├── visualizer.py
└── figures.py or figures/
```

`data.py` owns the authenticated scientific projection. `inventory.py` owns the closed
plot enum. Figure modules own only presentation of already projected values.
`visualizer.py` authenticates the projection and composes the complete inventory.
`__init__.py` exports only supported family contracts.

Larger families split `figures/` by scientific figure family, not one file per class.
There is no `helpers.py`, `utils.py`, generic figure registry, runtime plugin discovery,
or caller-extensible plot-name string.

## Migration rule

The source migration is direct:

1. add the root package and root verification interface;
2. move family modules into plural `visualizations/` packages;
3. update imports, public exports, tests, Sphinx pages, direct scripts, and implementation
   hashing paths;
4. prove unchanged typed projection bytes and closed plot inventories; and
5. delete every old singular `visualization.py` module.

The migration does not retain import shims. Historical execution records continue to
identify their original source bytes and Git commit.
