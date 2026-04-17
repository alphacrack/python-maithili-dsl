"""Unit tests for Devanagari → ASCII numeral conversion."""
import pytest

from maithili_dsl.transpiler.numeral import convert_devanagari_numerals
from maithili_dsl.transpiler.mappings import DEVNAGIRI_NUMERAL_MAP


@pytest.mark.parametrize("dev,ascii_", list(DEVNAGIRI_NUMERAL_MAP.items()))
def test_each_devanagari_digit_converts(dev, ascii_):
    assert convert_devanagari_numerals(dev) == ascii_


def test_multi_digit_number():
    assert convert_devanagari_numerals("१२३४५६७८९०") == "1234567890"


def test_mixed_devanagari_and_ascii():
    assert convert_devanagari_numerals("x = १0 + २") == "x = 10 + 2"


def test_empty_string_passes_through():
    assert convert_devanagari_numerals("") == ""


def test_no_digits_unchanged():
    text = "नमस्कार संसार"
    assert convert_devanagari_numerals(text) == text


def test_digits_inside_identifier():
    # The converter does NOT know about word boundaries — this is
    # intentional (digits are freely convertible everywhere in the
    # file, including inside identifiers).
    assert convert_devanagari_numerals("संख्या१") == "संख्या1"
