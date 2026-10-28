# Alignment

Where to align something along an axis.

Possible values are:

- `start`: Aligns at the [start](direction.md#definitions-start) of the [text direction](../text/text.md#parameters-dir).
- `end`: Aligns at the [end](direction.md#definitions-end) of the [text direction](../text/text.md#parameters-dir).
- `left`: Align at the left.
- `center`: Aligns in the middle, horizontally.
- `right`: Aligns at the right.
- `top`: Aligns at the top.
- `horizon`: Aligns in the middle, vertically.
- `bottom`: Align at the bottom.

These values are available globally and also in the alignment type's scope, so you can write either of the following two:

```typst
#align(center)[Hi]
#align(alignment.center)[Hi]
```

## 2D alignments

To align along both axes at the same time, add the two alignments using the `+` operator. For example, `top + right` aligns the content to the top right corner.

```typst
#set page(height: 3cm)
#align(center + bottom)[Hi]
```

## Fields

The `x` and `y` fields hold the alignment's horizontal and vertical components, respectively (as yet another `alignment`). They may be `none`.

```typst
#(top + right).x \
#left.x \
#left.y (none)
```


## Methods

## alignment.axis

The axis this alignment belongs to.

- `"horizontal"` for `start`, `left`, `center`, `right`, and `end`
- `"vertical"` for `top`, `horizon`, and `bottom`
- `none` for 2-dimensional alignments

```typst
#left.axis() \
#bottom.axis()
```

## alignment.inv

The inverse alignment.

```typst
#top.inv() \
#left.inv() \
#center.inv() \
#(left + bottom).inv()
```


