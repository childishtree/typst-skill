# Locate

# locate

Determines the location of an element in the document.

Takes a selector that must match exactly one element and returns that element's [`location`](location.md). This location can, in particular, be used to retrieve the physical [`page`](location.md#definitions-page) number and [`position`](location.md#definitions-position) (page, x, y) for that element.

## Examples

Locating a specific element:

```typst
#context [
  Introduction is at: \
  #locate(<intro>).position()
]

= Introduction <intro>
```

```typst
#locate(
  selector
) -> location
```

## Parameters

- selector:
  - description: A selector that should match exactly one element. This element will be located. Especially useful in combination with - [`here`](here.md) to locate the current context, - a [`location`](location.md) retrieved from some queried element via the [`location()`](../foundations/content.md#definitions-location) method on content.
  - type: label | selector | location | function
  - default: None


