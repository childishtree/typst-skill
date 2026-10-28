# YAML

# yaml

Reads structured data from a YAML file.

The file must contain a valid YAML object or array. The YAML values will be converted into corresponding Typst values as listed in the [table below](#conversion).

The function returns a dictionary, an array or, depending on the YAML file, another YAML data type.

The YAML files in the example contain objects with authors as keys, each with a sequence of their own submapping with the keys "title" and "published".

## Example

```typst
#let bookshelf(contents) = {
  for (author, works) in contents {
    author
    for work in works [
      - #work.title (#work.published)
    ]
  }
}

#bookshelf(
  yaml("scifi-authors.yaml")
)
```

## Conversion details

| YAML value | Converted into Typst |
| --- | --- |
| null-values (`null`, `~` or empty ``) | `none` |
| boolean | [`bool`](../foundations/bool.md) |
| number | [`float`](../foundations/float.md) or [`int`](../foundations/int.md) |
| string | [`str`](../foundations/str.md) |
| sequence | [`array`](../foundations/array.md) |
| mapping | [`dictionary`](../foundations/dictionary.md) |

| Typst value | Converted into YAML |
| --- | --- |
| types that can be converted from YAML | corresponding YAML value |
| [`bytes`](../foundations/bytes.md) | string via [`repr`](../foundations/repr.md) |
| [`symbol`](../foundations/symbol.md) | string |
| [`content`](../foundations/content.md) | a mapping describing the content |
| other types ([`length`](../layout/length.md), etc.) | string via [`repr`](../foundations/repr.md) |

### Notes

- In most cases, YAML numbers will be converted to floats or integers depending on whether they are whole numbers. However, be aware that integers larger than 263-1 or smaller than -263 will be converted to floating-point numbers, which may result in an approximative value.
- Custom YAML tags are ignored, though the loaded value will still be present.
- Bytes are not encoded as YAML sequences for performance and readability reasons. Consider using [`cbor.encode`](cbor.md#definitions-encode) for binary data.
- The `repr` function is [for debugging purposes only](../foundations/repr.md#debugging-only), and its output is not guaranteed to be stable across Typst versions.

```typst
#yaml(
  source
) -> any
```

## Parameters

- source:
  - description: A [path](../syntax.md#paths) to a YAML file or raw YAML bytes.
  - type: str | bytes
  - default: None


## Definitions
### yaml.decode

Reads structured data from a YAML string/bytes.

```typst
#yaml.decode(
  data
) -> any
```

#### Parameters

- data:
  - description: YAML data.
  - type: str | bytes
  - default: None

### yaml.encode

Encode structured data into a YAML string.

```typst
#yaml.encode(
  value
) -> str
```

#### Parameters

- value:
  - description: Value to be encoded.
  - type: any
  - default: None


