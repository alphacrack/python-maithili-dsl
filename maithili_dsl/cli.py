import sys
from pathlib import Path
from maithili_dsl.transpiler.transpile import transpile_maithili_code
from maithili_dsl.transpiler.linter import lint_maithili_code, translate_exception_to_maithili

# Optional: Extendable built-in Python library map (Maithili ⇄ Python)
MAITHILI_MODULES = {
    "गणित": "math",
    "समय": "time",
    "यादृच्छिक": "random",
    "तिथि": "datetime",
    "पुन": "re",
    "संग्रह": "collections",
    "सिस्टम": "sys",
    "पथ": "os.path",
    "ओएस": "os",
    "आँकड़ा": "statistics"
}

def translate_imports(maithili_code):
    for maithili_mod, py_mod in MAITHILI_MODULES.items():
        maithili_code = maithili_code.replace(f"आयात {maithili_mod}", f"import {py_mod}")
        maithili_code = maithili_code.replace(f"{maithili_mod}.", f"{py_mod}.")
    return maithili_code

def run_dmai_file(file_path):
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File '{file_path}' not found.")
        return

    with open(path, 'r', encoding='utf-8') as file:
        maithili_code = file.read()

    errors = lint_maithili_code(maithili_code)
    if errors:
        print("⚠️ लिंटर चेतावनी:")
        for err in errors:
            print("  -", err)
        print("कोड चलायल नहि गेल।\n")
        return

    try:
        maithili_code = translate_imports(maithili_code)
        python_code = transpile_maithili_code(maithili_code)
        exec(python_code, globals())
    except Exception as e:
        translated = translate_exception_to_maithili(e)
        print("⚠️ त्रुटि:", translated)
def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python_maithili <file.dmai>")
    else:
        run_dmai_file(sys.argv[1])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_dmai.py <file.dmai>")
    else:
        run_dmai_file(sys.argv[1])