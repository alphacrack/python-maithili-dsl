"""Maithili DSL — run Python code written in Devanagari Maithili script."""
from maithili_dsl.transpiler.transpile import transpile_maithili_code
from maithili_dsl.transpiler.linter import lint_maithili_code, translate_exception_to_maithili
from maithili_dsl.transpiler.numeral import convert_devanagari_numerals

__version__ = "0.4.0"

__all__ = [
    "__version__",
    "transpile_maithili_code",
    "lint_maithili_code",
    "translate_exception_to_maithili",
    "convert_devanagari_numerals",
]
