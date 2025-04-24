def convert_devanagari_numerals(code):
    from .mappings import DEVNAGIRI_NUMERAL_MAP
    for dev, ascii_num in DEVNAGIRI_NUMERAL_MAP.items():
        code = code.replace(dev, ascii_num)
    return code
