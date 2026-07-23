# Examples

This directory contains runnable Maithili DSL (`.dmai`) programs that demonstrate
the language. Run any of them with either entry point:

```bash
python_maithili examples/hello.dmai
# or, without installing the console script:
python -m maithili_dsl examples/hello.dmai
```

> **Note:** `error.dmai` is intentionally broken — it is used by CI to verify
> that the linter/transpiler correctly rejects invalid programs. It is expected
> to exit with a non-zero status and should not be run as a normal example.

## `hello.dmai`

Prints a greeting in Maithili.

- **Keywords/modules shown:** `कार्य` (function definition), `छपाउ` (print),
  top-level call.
- **Expected output:**

  ```
  हम मैथिली में कोड कऽ रहल छी।
  ```

## `person.dmai`

Defines a `व्यक्ति` (person) class, instantiates it, and calls a method.

- **Keywords/modules shown:** `वर्ग` (class), `नव` (constructor), `स्वयं` (self),
  method definition and invocation.
- **Expected output:**

  ```
  हमर नाम सुमन अछि।
  ```

## `calculator.dmai`

Implements basic arithmetic (`जोड़`/`घटाउ`/`गुणा`/`भाग`) and prints a
multiplication table.

- **Keywords/modules shown:** functions returning values, `str()`, `range()`,
  string concatenation, loops (`प्रत्येक`).
- **Expected output (abridged):**

  ```
  === मैथिली कैलकुलेटर ===
  जोड़ का परिणाम: 15
  घटाउ का परिणाम: 5
  गुणा का परिणाम: 50
  भाग का परिणाम: 2.0
  ```

## `shopping_list.dmai`

Builds a list, appends/removes items, iterates, and computes a sum and average.

- **Keywords/modules shown:** lists (`[]`), `append`/`remove`, `len()`,
  `यदि` (if), `प्रत्येक` (for), arithmetic and averages.
- **Expected output (abridged):**

  ```
  === खरीदारी सूची ===
  - दूध
  - रोटी
  - अंडा
  - चावल
  कुल वस्तु: 4
  दूध सूची में अछि!
  अंडा हटाएल गेल। नई सूची:
  - दूध
  - रोटी
  - चावल
  ```

## `error.dmai`

Intentionally invalid program (uses non-Maithili tokens and broken syntax) used
to confirm the linter rejects bad input.

- **Keywords/modules shown:** n/a (negative test case).
- **Expected output:** none — the run exits with a non-zero status.
