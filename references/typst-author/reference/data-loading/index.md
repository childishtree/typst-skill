# Data Loading

Data loading from external files.

These functions help you with loading and embedding data, for example from the results of an experiment.

## Encoding

Some of the functions are also capable of encoding, e.g. [`cbor.encode`](cbor.md#definitions-encode). They facilitate passing structured data to [plugins](../foundations/plugin.md).

However, each data format has its own native types. Therefore, for an arbitrary Typst value, the encode-to-decode roundtrip might be lossy. In general, numbers, strings, and [arrays](../foundations/array.md) or [dictionaries](../foundations/dictionary.md) composed of them can be reliably converted, while other types may fall back to strings via [`repr`](../foundations/repr.md), which is [for debugging purposes only](../foundations/repr.md#debugging-only). Please refer to the page of each data format for details.

## Definitions

| Name | Description |
| --- | --- |
| [`cbor`](cbor.md) | Reads structured data from a CBOR file. |
| [`csv`](csv.md) | Reads structured data from a CSV file. |
| [`json`](json.md) | Reads structured data from a JSON file. |
| [`read`](read.md) | Reads plain text or data from a file. |
| [`toml`](toml.md) | Reads structured data from a TOML file. |
| [`xml`](xml.md) | Reads structured data from an XML file. |
| [`yaml`](yaml.md) | Reads structured data from a YAML file. |

