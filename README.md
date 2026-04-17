# README.md

# 📜 Devnagiri Maithili DSL

A modern Python-compatible programming DSL that lets you write code in **Maithili** using the **Devanagari script**.

---

## 🔧 Features
- ✅ Full Maithili syntax mapped to Python
- ✅ Supports OOP (classes, methods, self)
- ✅ Devanagari numerals (`०-९`)
- ✅ Built-in module translation (e.g., `गणित` → `math`)
- ✅ Runtime error messages in Maithili
- ✅ Linter with style & syntax feedback in Maithili
- ✅ Command-line tool: run `.dmai` files with `python_maithili` (cross-platform)

---

## 🚀 Getting Started

### 📦 Installation
Clone the repo:
```bash
git clone https://github.com/alphacrack/python-maithili-dsl.git
cd python-maithili-dsl
```

### 🔧 Install CLI Tool (cross-platform)
```bash
pip install .
```

Now you can run Maithili scripts using either entry point:
```bash
python_maithili examples/hello.dmai
# or, without installing the console script:
python -m maithili_dsl examples/hello.dmai
```
✅ Works on Mac, Windows, and Linux, on Python 3.9 – 3.12.

---

## 📄 Example: `examples/person.dmai`
```python
वर्ग व्यक्ति:
    कार्य नव(स्वयं, नाम):
        स्वयं.नाम = नाम

    कार्य बोलू(स्वयं):
        छपाउ("हमर नाम " + स्वयं.नाम + " अछि।")

व्यक्ति१ = व्यक्ति("सुमन")
व्यक्ति१.बोलू()
```
Output:
```
हमर नाम सुमन अछि।
```

---

## 🧠 Maithili Keywords
| Maithili       | Python       |
|----------------|--------------|
| `कार्य`         | `def`         |
| `वर्ग`          | `class`       |
| `फेर करू`      | `return`      |
| `स्वयं`         | `self`        |
| `यदि`          | `if`          |
| `नहि त`        | `else`        |
| `प्रत्येक`      | `for`         |
| `में`          | `in`          |
| `सत्य`         | `True`        |
| `मिथ्या`       | `False`       |
| `शून्य`         | `None`        |

---

## 📦 Built-in Modules Mapping
| Maithili      | Python        |
|---------------|---------------|
| `गणित`        | `math`        |
| `समय`         | `time`        |
| `यादृच्छिक`   | `random`      |
| `तिथि`        | `datetime`    |
| `पुन`         | `re`          |
| `संग्रह`       | `collections` |
| `सिस्टम`       | `sys`         |
| `पथ`          | `os.path`     |
| `ओएस`         | `os`          |
| `आँकड़ा`       | `statistics`  |

---

## 🧹 Linting & Errors
- ❗ Common mistakes caught before running
- ❗ Runtime errors shown in Maithili:
```bash
⚠️ त्रुटि: कोनो नाम घोषित नहि अछि।
```

---

## 🔐 Security
`.dmai` scripts are executed in a sandbox: a restricted `__builtins__`
mapping (no `exec` / `eval` / `open` / `compile` / `breakpoint`) and a
module import whitelist mapped from `MAITHILI_MODULES`. Raw Python
`import` statements that weren't translated from Maithili names are
rejected before execution.

To report a vulnerability, see [SECURITY.md](SECURITY.md).

---

## 🧪 Testing
Contributions are expected to come with tests. Run the full suite:
```bash
pip install -r requirements-dev.txt
pytest -v --cov=maithili_dsl --cov-report=term-missing
```
Coverage gates: ≥85% overall, ≥90% on `cli.py`, `transpile.py`, and
`linter.py`. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full
workflow.

---

## 🤝 Contributing
See [`CONTRIBUTING.md`](CONTRIBUTING.md) to learn how you can help build and improve this DSL.

---

## 📄 License
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 🌐 Future Goals
- 🌍 Tirhuta script support
- 🌐 Web REPL for `.dmai`
- 🔌 VS Code extension
- `while` (`जबतक`) and `try`/`except` (`प्रयास`/`अपवाद`) keywords
- Type hints and `mypy` in CI

---
