import sys
import re
import builtins as _builtins
from pathlib import Path
from maithili_dsl.transpiler.transpile import transpile_maithili_code
from maithili_dsl.transpiler.linter import lint_maithili_code, translate_exception_to_maithili

# Extendable built-in Python library map (Maithili → Python)
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

# Modules that .dmai scripts are allowed to import
_ALLOWED_MODULES = set(MAITHILI_MODULES.values())

# Safe builtins — excludes __import__, exec, eval, compile, open, breakpoint
_SAFE_BUILTIN_NAMES = [
    'abs', 'all', 'any', 'bin', 'bool', 'chr', 'dict', 'dir',
    'divmod', 'enumerate', 'filter', 'float', 'format', 'frozenset',
    'getattr', 'hasattr', 'hash', 'hex', 'id', 'input', 'int',
    'isinstance', 'issubclass', 'iter', 'len', 'list', 'map', 'max',
    'min', 'next', 'object', 'oct', 'ord', 'pow', 'print', 'property',
    'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice',
    'sorted', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip',
    # Required for class definitions (Python internally uses __build_class__)
    '__build_class__',
    # Required for name lookup in class bodies
    '__name__',
]


def _make_safe_import():
    """Create an __import__ that only allows whitelisted modules."""
    real_import = _builtins.__import__

    def safe_import(name, globals=None, locals=None, fromlist=(), level=0):
        # Allow the base module (e.g., 'os' from 'os.path')
        base_module = name.split('.')[0]
        if name not in _ALLOWED_MODULES and base_module not in _ALLOWED_MODULES:
            raise ImportError(f"आयात अनुमति नहि अछि: '{name}'")
        return real_import(name, globals, locals, fromlist, level)

    return safe_import


def translate_imports(maithili_code):
    """Translate Maithili module names to Python equivalents.

    Returns (translated_code, set_of_translated_module_names) so the
    sandbox can distinguish legitimately translated imports from
    raw Python imports injected by a malicious .dmai file.
    """
    translated_modules = set()
    for maithili_mod, py_mod in MAITHILI_MODULES.items():
        if f"आयात {maithili_mod}" in maithili_code or f"{maithili_mod}." in maithili_code:
            translated_modules.add(py_mod.split('.')[0])
        maithili_code = maithili_code.replace(f"आयात {maithili_mod}", f"import {py_mod}")
        maithili_code = maithili_code.replace(f"{maithili_mod}.", f"{py_mod}.")
    return maithili_code, translated_modules


def _validate_imports(python_code, translated_modules):
    """Check that all import statements only reference modules that were
    translated from Maithili names (not raw Python module names).

    This catches imports BEFORE exec runs them, since Python's import
    statement doesn't always go through __import__ in all cases.

    Args:
        python_code: The transpiled Python code.
        translated_modules: Set of module names that were legitimately
            translated from Maithili names in this file.
    """
    errors = []
    for line in python_code.splitlines():
        stripped = line.strip()
        if stripped.startswith('import '):
            module_part = stripped[len('import '):].strip()
            module_name = module_part.split('.')[0].split(' ')[0]
            if module_name not in translated_modules:
                errors.append(f"आयात अनुमति नहि अछि: '{module_name}'")
        elif stripped.startswith('from '):
            match = re.match(r'from\s+(\S+)\s+import', stripped)
            if match:
                module_name = match.group(1).split('.')[0]
                if module_name not in translated_modules:
                    errors.append(f"आयात अनुमति नहि अछि: '{module_name}'")
    return errors


def run_dmai_file(file_path):
    """Load, lint, transpile, and execute a .dmai file."""
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
        maithili_code, translated_modules = translate_imports(maithili_code)
        python_code = transpile_maithili_code(maithili_code)

        # Validate imports before execution — only allow modules that
        # were translated from Maithili names, not raw Python imports
        import_errors = _validate_imports(python_code, translated_modules)
        if import_errors:
            for err in import_errors:
                print(f"⚠️ त्रुटि: {err}")
            return

        # Build sandboxed execution environment
        safe_builtins = {name: getattr(_builtins, name) for name in _SAFE_BUILTIN_NAMES}
        safe_builtins['__import__'] = _make_safe_import()

        exec_globals = {"__builtins__": safe_builtins}
        exec(python_code, exec_globals)

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
