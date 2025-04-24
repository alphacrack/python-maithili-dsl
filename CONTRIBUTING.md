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

---

## 🚀 Getting Started

### 📦 Installation
Clone the repo:
```bash
git clone https://github.com/youruser/maithili-dsl.git
cd maithili-dsl
```

Run a sample file:
```bash
python run_dmai.py examples/hello.dmai
```

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

# CONTRIBUTING.md

# 🤝 Contributing to Maithili DSL

Welcome! Your contributions help make the Maithili DSL stronger and more accessible.

## 🛠 Setup Instructions
1. Clone the repo:
   ```bash
   git clone https://github.com/youruser/maithili-dsl.git
   cd maithili-dsl
   ```
2. Run a sample file:
   ```bash
   python run_dmai.py examples/hello.dmai
   ```

## 🧩 How You Can Contribute
- 📚 Improve keyword mappings and add new features
- 🧪 Write tests and examples
- 🌐 Help add Tirhuta script support
- ✍️ Translate documentation into Maithili

## 📬 Submitting Changes
- Fork the repository
- Make your changes on a branch
- Open a Pull Request (PR) with a clear title & description

Thanks for your interest! ❤️