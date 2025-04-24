from .mappings import DEVNAGIRI_KEYWORD_MAP
from .numeral import convert_devanagari_numerals

def transpile_maithili_code(maithili_code):
    code = convert_devanagari_numerals(maithili_code)
    for maithili_kw, py_kw in DEVNAGIRI_KEYWORD_MAP.items():
        code = code.replace(maithili_kw, py_kw)
    return code
