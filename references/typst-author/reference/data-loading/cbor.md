# CBOR

# cbor

Reads structured data from a CBOR file.

The file must contain a valid CBOR serialization. The CBOR values will be converted into corresponding Typst values as listed in the [table below](#conversion).

The function returns a dictionary, an array or, depending on the CBOR file, another CBOR data type.

## Conversion details

| CBOR value | Converted into Typst |
| --- | --- |
| integer | [`int`](../foundations/int.md) (or [`float`](../foundations/float.md)) |
| bytes | [`bytes`](../foundations/bytes.md) |
| float | [`float`](../foundations/float.md) |
| text | [`str`](../foundations/str.md) |
| bool | [`bool`](../foundations/bool.md) |
| null | `none` |
| array | [`array`](../foundations/array.md) |
| map | [`dictionary`](../foundations/dictionary.md) |

| Typst value | Converted into CBOR |
| --- | --- |
| types that can be converted from CBOR | corresponding CBOR value |
| [`symbol`](../foundations/symbol.md) | text |
| [`content`](../foundations/content.md) | a map describing the content |
| other types ([`length`](../layout/length.md), etc.) | text via [`repr`](../foundations/repr.md) |

### Notes

- Be aware that CBOR integers larger than 263-1 or smaller than -263 will be converted to floating point numbers, which may result in an approximative value.
- CBOR tags are not supported, and an error will be thrown.
- The `repr` function is [for debugging purposes only](../foundations/repr.md#debugging-only), and its output is not guaranteed to be stable across Typst versions.

```typst
#cbor(
  source
) -> any
```

## Parameters

- source:
  - description: A [path](../syntax.md#paths) to a CBOR file or raw CBOR bytes.
  - type: str | bytes
  - default: None


## Definitions
### cbor.decode

Reads structured data from CBOR bytes.

```typst
#cbor.decode(
  data
) -> any
```

#### Parameters

- data:
  - description: CBOR data.
  - type: bytes
  - default: None

### cbor.encode

Encode structured data into CBOR bytes.

```typst
#cbor.encode(
  value
) -> bytes
```

#### Parameters

- value:
  - description: Value to be encoded.
  - type: any
  - default: None


