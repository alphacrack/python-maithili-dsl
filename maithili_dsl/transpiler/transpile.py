import re
from .mappings import DEVNAGIRI_KEYWORD_MAP
from .numeral import convert_devanagari_numerals

# Devanagari "word character" class: letters (Lo), marks (Mn, Mc), and digits.
# Standard \b doesn't work for Devanagari because combining marks (virama ्,
# anusvara ं, visarga ः, matras) are category Mn/Mc and not matched by \w.
_DEVANAGARI_WORD_CHAR = (
    r'[\u0900-\u097F]'  # Devanagari block (letters, marks, digits, signs)
)

# A "word character" for our purposes: ASCII \w OR anything in Devanagari block
_WORD_CHAR = r'(?:[\w' + '\u0900-\u097F' + r'])'


def _tokenize_preserving_strings(code):
    """Split code into tokens, separating string literals from code regions.

    Returns a list of (is_string, text) tuples. String literals are returned
    intact and should not be modified by keyword replacement.
    """
    tokens = []
    # Match single-quoted, double-quoted strings, and # comments
    pattern = re.compile(r'''("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'|#.*)''')

    last_end = 0
    for match in pattern.finditer(code):
        start, end = match.span()
        # Code region before this string/comment
        if start > last_end:
            tokens.append((False, code[last_end:start]))
        # The string literal or comment itself
        tokens.append((True, match.group(0)))
        last_end = end

    # Remaining code after last string/comment
    if last_end < len(code):
        tokens.append((False, code[last_end:]))

    return tokens


def _make_keyword_pattern(keyword):
    """Create a regex pattern that matches a keyword at word boundaries.

    Uses custom boundary logic that understands Devanagari combining marks
    (virama, anusvara, visarga, matras) as part of words, since Python's
    \\b only recognizes \\w characters (which excludes Mn/Mc categories).
    """
    # Negative lookbehind/lookahead for our extended word characters
    before = r'(?<!' + _DEVANAGARI_WORD_CHAR[4:-1] + r')'  # strip (?:...) wrapper
    after = r'(?!' + _DEVANAGARI_WORD_CHAR[4:-1] + r')'

    # Simpler approach: use negative lookbehind/lookahead for Devanagari block chars
    before = r'(?<![\w\u0900-\u097F])'
    after = r'(?![\w\u0900-\u097F])'

    return re.compile(before + re.escape(keyword) + after)


# Pre-compile all keyword patterns for performance
_KEYWORD_PATTERNS = {
    maithili_kw: (_make_keyword_pattern(maithili_kw), py_kw)
    for maithili_kw, py_kw in DEVNAGIRI_KEYWORD_MAP.items()
}


def _replace_keywords_in_code(code_text):
    """Replace Maithili keywords with Python equivalents using word boundaries.

    Uses custom Devanagari-aware boundary matching so that keywords inside
    longer identifiers are not replaced (e.g., नवयुग won't match नव).
    """
    result = code_text
    for maithili_kw, (pattern, py_kw) in _KEYWORD_PATTERNS.items():
        result = pattern.sub(py_kw, result)
    return result


def transpile_maithili_code(maithili_code):
    """Transpile Maithili (Devanagari) source code to Python.

    1. Convert Devanagari numerals (०-९) to ASCII (0-9)
    2. Tokenize to identify string literals
    3. Replace keywords only in code regions (not inside strings or comments)
    """
    code = convert_devanagari_numerals(maithili_code)

    tokens = _tokenize_preserving_strings(code)

    result_parts = []
    for is_string, text in tokens:
        if is_string:
            # Leave string literals and comments untouched
            result_parts.append(text)
        else:
            # Replace keywords only in code regions
            result_parts.append(_replace_keywords_in_code(text))

    return ''.join(result_parts)
