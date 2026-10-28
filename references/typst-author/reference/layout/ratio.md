# Ratio

A ratio of a whole.

A ratio is written as a number, followed by a percent sign. Ratios most often appear as part of a [relative length](relative.md), to specify the size of some layout element relative to the page or some container.

```typst
#rect(width: 25%)
```

However, they can also describe any other property that is relative to some base, e.g. an amount of [horizontal scaling](scale.md#parameters-x) or the [height of parentheses](../math/lr.md#functions-lr-size) relative to the height of the content they enclose.

## Scripting

Within your own code, you can use ratios as you like. You can multiply them with various other types as shown below:

| Multiply by | Example | Result |
| --- | --- | --- |
| [`ratio`](ratio.md) | `27% * 10%` | `2.7%` |
| [`length`](length.md) | `27% * 100pt` | `27pt` |
| [`relative`](relative.md) | `27% * (10% + 100pt)` | `2.7% + 27pt` |
| [`angle`](angle.md) | `27% * 100deg` | `27deg` |
| [`int`](../foundations/int.md) | `27% * 2` | `54%` |
| [`float`](../foundations/float.md) | `27% * 0.37037` | `10%` |
| [`fraction`](fraction.md) | `27% * 3fr` | `0.81fr` |

When ratios are [displayed](../foundations/repr.md) in the document, they are rounded to two significant digits for readability.


