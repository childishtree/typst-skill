# Introspection

Interactions between document parts.

This category is home to Typst's introspection capabilities: With the `counter` function, you can access and manipulate page, section, figure, and equation counters or create custom ones. Meanwhile, the `query` function lets you search for elements in the document to construct things like a list of figures or headers which show the current chapter title.

Most of the functions are _contextual._ It is recommended to read the chapter on [context](../context.md) before continuing here.

## Definitions

| Name | Description |
| --- | --- |
| [`counter`](counter.md) | Counts through pages, elements, and more. |
| [`here`](here.md) | Provides the current location in the document. |
| [`locate`](locate.md) | Determines the location of an element in the document. |
| [`location`](location.md) | Identifies an element in the document. |
| [`metadata`](metadata.md) | Exposes a value to the query system without producing visible content. |
| [`query`](query.md) | Finds elements in the document. |
| [`state`](state.md) | Manages stateful parts of your document. |

