# Read

# read

Reads plain text or data from a file.

By default, the file will be read as UTF-8 and returned as a [string](../foundations/str.md).

If you specify `encoding: none`, this returns raw [bytes](../foundations/bytes.md) instead.

## Example

```typst
An example for a HTML file: \
#let text = read("example.html")
#raw(text, block: true, lang: "html")

Raw bytes:
#read("tiger.jpg", encoding: none)
```

```typst
#read(
  path,
  encoding: none | str
) -> str bytes
```

## Parameters

- path:
  - description: Path to a file. For more details, see the [Paths section](../syntax.md#paths).
  - type: str
  - default: None
- encoding:
  - description: The encoding to read the file with. If set to `none`, this function returns raw bytes.
  - type: none | str
  - default: "utf8"


