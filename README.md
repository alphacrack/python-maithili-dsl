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
git clone https://github.com/youruser/maithili-dsl.git
cd maithili-dsl
```

### 🔧 Install CLI Tool (cross-platform)
```bash
pip install .
```

Now you can run Maithili scripts using:
```bash
python_maithili examples/hello.dmai
```
✅ Works on Mac, Windows, and Linux!

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
- 🧪 Unit testing + CI/CD

---
