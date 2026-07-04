# Math Formulas in Typst

Comprehensive guide to math formula editing in Typst. For a runnable example, see [assets/examples/math-cheatsheet.typ](../../assets/examples/math-cheatsheet.typ).

## Basic Concepts

- Enclose formulas between `$` `$` with `$ space formula space $` format — the formula will be centered.
- Single letters in formulas are treated as variables. Use `#` to access outside variables. Multi-letter names must be quoted.
- Typst provides many symbols, variants, and shorthand sequences like `=>`.
- Functions accept named and positional arguments. Outside `$` `$`, prefix with `math.`.
- Number formulas with `#set math.equation(numbering: ...)`, label with `<name>`, and reference with `@name`.

```typst
#set math.equation(numbering: "(1)", supplement: [Formula:])

$ A = pi r^2 $
$ "area" = pi dot "radius"^2 $
$ cal(A) := { x in RR | x "is natural" } $

#let x = 5
$ #x < 17 $
$ x < y => x gt.eq.not y $

$ frac(a^2, 2) $
$ vec(1, 2, delim: "[") $
$ mat(1, 2; 3, 4) $
$ lim_x = op("lim", limits: #true)_x $
```

## Equation Alignment

Use `&` to align multi-step derivations at specific points:

```typst
$ sum_(k=0)^n k
  &= 1 + 2 + 3 + ... + n \
  &= (n(n+1)) / 2 " (comment here)" \
  &= 1/2(n(n+1)) \
  &= 1/2(n^2+n) \
  &= 1/2 n^2 + 1/2 n $
```

## Math Fonts / Variants

| Variant  | Example           |
| -------- | ----------------- |
| `serif`  | `$serif(N B R)$` |
| `sans`   | `$sans(N B R)$`  |
| `frak`   | `$frak(N B R)$`  |
| `mono`   | `$mono(N B R)$`  |
| `bb`     | `$bb(N B R)$`    |
| `cal`    | `$cal(N B R)$`   |

## Accents

| Accent           | Syntax                              |
| ---------------- | ----------------------------------- |
| `grave`          | `$grave(a)$`                        |
| `acute`          | `$acute(a)$`                        |
| `acute.double`   | `$acute.double(a)$`                 |
| `hat`            | `$hat(a)$`                          |
| `tilde`          | `$tilde(a)$`                        |
| `macron`         | `$macron(a)$`                       |
| `breve`          | `$breve(a)$`                        |
| `diaer`          | `$diaer(a)$`                        |
| `circle`         | `$circle(a)$`                       |
| `caron`          | `$caron(a)$`                        |
| `dot`            | `$dot(a)$`                          |
| `dot.double`     | `$dot.double(a)$`                   |
| `dot.triple`     | `$dot.triple(a)$`                   |
| `dot.quad`       | `$dot.quad(a)$`                     |
| `arrow`          | `$arrow("AB")$`                     |
| `arrow.l`        | `$arrow.l("AB")$`                   |

## Under/Over Annotations

| Function          | Example                                      |
| ----------------- | -------------------------------------------- |
| `underline`       | `$underline(1 + 2 + ... + 5)$`              |
| `overline`        | `$overline(1 + 2 + ... + 5)$`               |
| `underbrace`      | `$underbrace(1+...+5, "numbers")$`           |
| `overbrace`       | `$overbrace(1+...+5, "numbers")$`            |
| `underbracket`    | `$underbracket(1+...+5, "numbers")$`         |
| `overbracket`     | `$overbracket(1+...+5, "numbers")$`          |

## Attaching Symbols (Sub/Superscripts)

**Syntax-based sub/superscripts:**
```typst
$ sum_(i=0)^n a_i = 2^(1+i) $
```

**`attach` function** — place symbols at all corners:
```typst
$ attach(Pi, t: alpha, b: beta, tl: 1, tr: 2+3, bl: 4+5, br: 6) $
```

**`scripts` vs `limits`:**
```typst
$ scripts(sum)_1^2 != sum_1^2 $    // scripts stays inline
$ limits(A)_1^2 != A_1^2 $         // limits goes above/below
```

## Binomial Coefficients

```typst
$ binom(n, k) $
```

## Cancel / Cross Out

```typst
// Cancel terms (for simplification)
$ (a dot b dot cancel(x)) / cancel(x) $

// Inverted slash
$ (a cancel((b + c), inverted: #true)) / cancel(b + c, inverted: #true) $

// Cross out
$ cancel(Pi, cross: #true) $
```

## Cases (Piecewise Functions)

Support multiple delimiter styles:

```typst
// Parentheses
$ f(x,y) := cases(delim: "(", 1 "if" x < 0, 2 "else") $

// Brackets
$ f(x,y) := cases(delim: "[", 1 "if" x < 0, 2 "else") $

// Curly braces (default)
$ f(x,y) := cases(1 "if" x < 0, 2 "else") $

// Vertical bars
$ f(x,y) := cases(delim: "|", 1 "if" x < 0, 2 "else") $

// Double vertical bars
$ f(x,y) := cases(delim: bar.double, 1 "if" x < 0, 2 "else") $
```

## Fractions

```typst
$ 1/2 < (x+1)/2 $
$ ((x+1)) / 2 = frac(a, b) $
```

## Common Functions and Scaled Brackets

**Functions:**
```typst
$ abs(x/2) $     // absolute value
$ norm(x/2) $    // norm
$ floor(x/2) $   // floor
$ ceil(x/2) $    // ceiling
$ round(x/2) $   // round
```

**Scaled brackets with `lr`:**
```typst
$ lr((a, (b-1/2), c), size: #50%) $
$ lr((a, (b/2), c), size: #150%) $
```

## Vectors

Multiple delimiter styles via the `vec` function:

| Delimiter      | Syntax                                 |
| -------------- | -------------------------------------- |
| Parentheses    | `$ vec(a, b, c) $` (default)          |
| Brackets       | `$ vec(delim: "[", a, b, c) $`        |
| Curly braces   | `$ vec(delim: "{", a, b, c) $`        |
| Vertical bars  | `$ vec(delim: "|", a, b, c) $`        |
| Double bars    | `$ vec(delim: bar.double, a, b, c) $` |

```typst
$ vec(a, b, c) dot vec(1, 2, 3) = a + 2b + 3c $
```

## Matrices

Multiple delimiter styles via the `mat` function:

| Delimiter      | Syntax                                 |
| -------------- | -------------------------------------- |
| Parentheses    | `$ mat(1, 2; 3, 4) $` (default)       |
| Brackets       | `$ mat(delim: "[", 1, 2; 3, 4) $`     |
| Curly braces   | `$ mat(delim: "{", 1, 2; 3, 4) $`     |
| Vertical bars  | `$ mat(delim: "|", 1, 2; 3, 4) $`     |
| Double bars    | `$ mat(delim: bar.double, 1, 2; 3, 4) $` |

Rows separated by `;`, columns by `,`. Use `...`, `dots.v`, `dots.down` for ellipsis.

## Roots and Radicals

```typst
$ sqrt(x^2) = x = sqrt(x)^2 $       // square root
$ root(3, x^3) = x = root(3, x)^3 $ // nth root
```

## Predefined Functions

| Function   | Description             | Function   | Description              |
| ---------- | ----------------------- | ---------- | ------------------------ |
| `sin`      | Sine                    | `arcsin`   | Arc sine                 |
| `cos`      | Cosine                  | `arccos`   | Arc cosine               |
| `tan`      | Tangent                 | `arctan`   | Arc tangent              |
| `cot`/`ctg`| Cotangent               | `sinh`     | Hyperbolic sine          |
| `sec`      | Secant                  | `cosh`     | Hyperbolic cosine        |
| `csc`      | Cosecant                | `tanh`     | Hyperbolic tangent       |
| `coth`     | Hyperbolic cotangent    | `exp`      | Exponential              |
| `ln`       | Natural log             | `lg`       | Base-10 log              |
| `log`      | Logarithm               | `gcd`      | Greatest common divisor  |
| `max`      | Maximum                 | `min`      | Minimum                  |
| `inf`      | Infimum                 | `sup`      | Supremum                 |
| `lim`      | Limit                   | `liminf`   | Limit inferior           |
| `limsup`   | Limit superior          | `det`      | Matrix determinant       |
| `dim`      | Vector space dimension  | `ker`      | Kernel                   |
| `hom`      | Homomorphism            | `arg`      | Argument                 |
| `deg`      | Degree conversion       | `Pr`       | Probability              |
| `sinc`     | Sinc function           |            |                          |

## Custom Operators

```typst
$ op("myop", limits: #true)_(n->oo) n $
```

## Style Overrides in Math

```typst
#show math.sum: set text(size: 20pt)
$ sum_(i in NN) 1 + i $
```
