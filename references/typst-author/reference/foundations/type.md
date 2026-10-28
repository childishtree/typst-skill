# Type

Describes a kind of value.

To style your document, you need to work with values of different kinds: Lengths specifying the size of your elements, colors for your text and shapes, and more. Typst categorizes these into clearly defined _types_ and tells you where it expects which type of value.

Apart from basic types for numeric values and [typical](int.md) [types](float.md) [known](str.md) [from](array.md) [programming](dictionary.md) languages, Typst provides a special type for [_content._](content.md) A value of this type can hold anything that you can enter into your document: Text, elements like headings and shapes, and style information.

## Example

```typst
#let x = 10
#if type(x) == int [
  #x is an integer!
] else [
  #x is another value...
]

An image is of type
#type(image("glacier.jpg")).
```

The type of `10` is `int`. Now, what is the type of `int` or even `type`?

```typst
#type(int) \
#type(type)
```

Unlike other types like `int`, [none](none.md) and [auto](auto.md) do not have a name representing them. To test if a value is one of these, compare your value to them directly, e.g:

```typst
#let val = none
#if val == none [
  Yep, it's none.
]
```

Note that `type` will return [`content`](content.md) for all document elements. To programmatically determine which kind of content you are dealing with, see [`content.func`](content.md#definitions-func).

## Constructor
## type

Determines a value's type.

```typst
#type(12) \
#type(14.7) \
#type("hello") \
#type(<glacier>) \
#type([Hi]) \
#type(x => x + 1) \
#type(type)
```

```typst
#type(
  value
) -> type
```

### Parameters

- value:
  - description: The value whose type\'s to determine.
  - type: any
  - default: None


