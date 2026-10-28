# Visualize

Drawing and data visualization.

If you want to create more advanced drawings or plots, also have a look at the [CeTZ](https://github.com/johannes-wolf/cetz) package as well as more specialized [packages](https://typst.app/universe/) for your use case.

## Accessibility

All shapes and paths drawn by Typst are automatically marked as [artifacts](../pdf/artifact.md) to make them invisible to Assistive Technology (AT) during PDF export. However, their contents (if any) remain accessible.

If you are using the functions in this model to create an illustration with semantic meaning, make it accessible by wrapping it in a [`figure`](../model/figure.md) function call. Use its [`alt` parameter](../model/figure.md#parameters-alt) to provide an [alternative description](../../guides/accessibility.md#textual-representations).

## Definitions

| Name | Description |
| --- | --- |
| [`circle`](circle.md) | A circle with optional content. |
| [`color`](color.md) | A color in a specific color space. |
| [`curve`](curve.md) | A curve consisting of movements, lines, and Bézier segments. |
| [`ellipse`](ellipse.md) | An ellipse with optional content. |
| [`gradient`](gradient.md) | A color gradient. |
| [`image`](image.md) | A raster or vector graphic. |
| [`line`](line.md) | A line from one point to another. |
| [`path`](path.md) | A path through a list of points, connected by Bézier curves. |
| [`polygon`](polygon.md) | A closed polygon. |
| [`rect`](rect.md) | A rectangle with optional content. |
| [`square`](square.md) | A square with optional content. |
| [`stroke`](stroke.md) | Defines how to draw a line. |
| [`tiling`](tiling.md) | A repeating tiling fill. |

