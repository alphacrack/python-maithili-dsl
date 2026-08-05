"""Unit tests for the Maithili linter.

Covers the post-fix behavior: == is not flagged as assignment, नव
(constructor) is not flagged as unused, and all the structural checks
still fire on genuinely broken input.
"""
import pytest

from maithili_dsl.transpiler.linter import (
    LINT_CONFIG,
    is_snake_case,
    lint_maithili_code,
    translate_exception_to_maithili,
)


# ---------------------------------------------------------------------------
# Clean / passing code
# ---------------------------------------------------------------------------

def test_empty_code_has_no_errors():
    assert lint_maithili_code("") == []


def test_simple_function_with_usage_passes():
    code = (
        "कार्य नमस्कार():\n"
        "    छपाउ(\"hi\")\n"
        "\n"
        "नमस्कार()\n"
    )
    assert lint_maithili_code(code) == []


def test_function_name_inside_longer_identifier_is_unused():
    code = (
        "कार्य जोड़():\n"
        "    फेर करू १\n"
        "\n"
        "जोड़ल = ५\n"
    )

    errors = lint_maithili_code(code)

    assert "चेतावनी: कार्य 'जोड़' केहनो ठाम प्रयोग नहि कएल गेल अछि" in errors


def test_function_name_inside_string_is_unused():
    code = (
        "कार्य जोड़():\n"
        "    फेर करू १\n"
        "\n"
        "छपाउ(\"जोड़()\")\n"
    )

    errors = lint_maithili_code(code)

    assert "चेतावनी: कार्य 'जोड़' केहनो ठाम प्रयोग नहि कएल गेल अछि" in errors


def test_class_with_constructor_passes():
    code = (
        "वर्ग व्यक्ति:\n"
        "    कार्य नव(स्वयं, नाम):\n"
        "        स्वयं.नाम = नाम\n"
        "\n"
        "व्यक्ति१ = व्यक्ति(\"सुमन\")\n"
    )
    errors = lint_maithili_code(code)
    # The नव constructor is called implicitly via instantiation,
    # so it MUST NOT be flagged as unused.
    unused_errors = [e for e in errors if "नव" in e and "प्रयोग नहि" in e]
    assert unused_errors == [], f"नव falsely flagged as unused: {errors}"


# ---------------------------------------------------------------------------
# Comparison operators are not assignments
# ---------------------------------------------------------------------------

class TestComparisonNotFlaggedAsAssignment:
    """Pre-fix bug: `x == 5` parsed as an assignment with var name
    `x ` and produced a spurious 'invalid variable name' error."""

    def test_equality_operator(self):
        code = "यदि x == ५:\n    छपाउ(x)\n"
        errors = lint_maithili_code(code)
        assert not any("चर नाम" in e for e in errors), (
            f"== comparison falsely flagged: {errors}"
        )

    def test_inequality_operator(self):
        code = "यदि x != ५:\n    छपाउ(x)\n"
        errors = lint_maithili_code(code)
        assert not any("चर नाम" in e for e in errors)

    def test_lte_operator(self):
        code = "यदि x <= ५:\n    छपाउ(x)\n"
        errors = lint_maithili_code(code)
        assert not any("चर नाम" in e for e in errors)

    def test_gte_operator(self):
        code = "यदि x >= ५:\n    छपाउ(x)\n"
        errors = lint_maithili_code(code)
        assert not any("चर नाम" in e for e in errors)


@pytest.mark.parametrize("operator", ["+=", "-=", "*=", "/=", "//=", "%=", "**="])
def test_augmented_assignment_not_flagged_as_invalid_name(operator):
    code = f"क = ०\nक {operator} १\n"
    errors = lint_maithili_code(code)
    assert not any("चर नाम" in error for error in errors)


# ---------------------------------------------------------------------------
# Structural errors still fire
# ---------------------------------------------------------------------------

def test_leading_equals_sign_flagged():
    errors = lint_maithili_code("= ५\n")
    assert any("'=' चिह्नक पहिले" in e for e in errors)


def test_unbalanced_parens_flagged():
    errors = lint_maithili_code("छपाउ(x\n")
    assert any("गोल ब्रैकेट" in e for e in errors)


def test_unbalanced_quotes_flagged():
    errors = lint_maithili_code('छपाउ("hi)\n')
    assert any("उद्धरण" in e for e in errors)


def test_suspicious_block_flagged():
    errors = lint_maithili_code("कोनो चीज:\nwde\n")
    assert any("संदिग्ध ढाँचा" in e for e in errors)


def test_missing_indent_after_colon_flagged():
    code = "कार्य f():\nछपाउ(\"x\")\n"
    errors = lint_maithili_code(code)
    assert any("इनडेन्टेशन" in e for e in errors)


# ---------------------------------------------------------------------------
# Line length
# ---------------------------------------------------------------------------

def test_long_line_flagged_by_default():
    long_line = "x = \"" + ("अ" * 100) + "\"\n"
    errors = lint_maithili_code(long_line)
    assert any("पंक्ति बहुत लंबा" in e for e in errors)


def test_line_length_config_override():
    config = dict(LINT_CONFIG, max_line_length=200)
    long_line = "x = \"" + ("अ" * 100) + "\"\n"
    errors = lint_maithili_code(long_line, config=config)
    assert not any("पंक्ति बहुत लंबा" in e for e in errors)


# ---------------------------------------------------------------------------
# Unused function detection
# ---------------------------------------------------------------------------

def test_unused_regular_function_flagged():
    code = "कार्य अप्रयुक्त():\n    फेर करू १\n"
    errors = lint_maithili_code(code)
    assert any("अप्रयुक्त" in e and "प्रयोग नहि" in e for e in errors)


def test_used_function_not_flagged():
    code = (
        "कार्य प्रयुक्त():\n"
        "    फेर करू १\n"
        "\n"
        "प्रयुक्त()\n"
    )
    errors = lint_maithili_code(code)
    assert not any("प्रयुक्त" in e and "प्रयोग नहि" in e for e in errors)


def test_init_never_flagged_even_when_not_called_by_name():
    # नव is called implicitly via class instantiation — never by name.
    code = (
        "वर्ग क:\n"
        "    कार्य नव(स्वयं):\n"
        "        स्वयं.x = १\n"
        "\n"
        "ओब = क()\n"
    )
    errors = lint_maithili_code(code)
    assert not any("नव" in e and "प्रयोग नहि" in e for e in errors)


# ---------------------------------------------------------------------------
# is_snake_case / snake_case enforcement toggle
# ---------------------------------------------------------------------------

def test_is_snake_case_positive_cases():
    assert is_snake_case("foo_bar")
    assert is_snake_case("x")
    assert is_snake_case("_private")
    assert is_snake_case("name123")


def test_is_snake_case_negative_cases():
    assert not is_snake_case("CamelCase")
    assert not is_snake_case("")
    assert not is_snake_case("1startswithdigit")


def test_snake_case_not_enforced_by_default():
    code = "camelCase = १\n"
    errors = lint_maithili_code(code)
    assert not any("snake_case" in e for e in errors)


def test_snake_case_enforced_when_enabled():
    config = dict(LINT_CONFIG, enforce_snake_case=True)
    code = "camelCase = 1\n"
    errors = lint_maithili_code(code, config=config)
    assert any("snake_case" in e for e in errors)


# ---------------------------------------------------------------------------
# Exception translation
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("exc_type,must_contain", [
    (SyntaxError, "वाक्य संरचना"),
    (NameError, "नाम"),
    (TypeError, "प्रकार"),
    (ValueError, "मान"),
    (AttributeError, "गुण"),
    (IndexError, "सूची सीमा"),
    (KeyError, "कुंजी"),
])
def test_known_exceptions_translated(exc_type, must_contain):
    exc = exc_type("demo")
    out = translate_exception_to_maithili(exc)
    assert must_contain in out


def test_unknown_exception_falls_through():
    class CustomError(Exception):
        pass

    out = translate_exception_to_maithili(CustomError("demo"))
    assert "CustomError" in out

# ---------------------------------------------------------------------------
# Regression: parens and quotes inside string literals (issue #30)
# ---------------------------------------------------------------------------


def test_parens_inside_double_quoted_string_not_flagged():
    code = 'छपाउ("(क")\n'
    errors = lint_maithili_code(code)
    assert not any(
        "गोल ब्रैकेट" in e
        for e in errors
    ), f"parens inside double-quoted string falsely flagged: {errors}"


def test_parens_inside_single_quoted_string_not_flagged():
    code = "छपाउ('(क')\n"
    errors = lint_maithili_code(code)
    assert not any(
        "गोल ब्रैकेट" in e
        for e in errors
    ), f"parens inside single-quoted string falsely flagged: {errors}"


def test_quote_inside_string_not_flagged():
    code = 'छपाउ("it\'s ok")\n'
    assert "it's ok" in code
    errors = lint_maithili_code(code)
    assert not any("उद्धरण" in e for e in errors), (
        f"apostrophe in double-quoted string falsely flagged: {errors}"
    )


def test_unbalanced_single_quote_flagged():
    code = "छपाउ('hi)\n"
    errors = lint_maithili_code(code)
    assert any("उद्धरण" in e for e in errors), (
        f"unbalanced single quote not flagged: {errors}"
    )


def test_genuinely_unbalanced_parens_still_flagged():
    errors = lint_maithili_code("छपाउ(x\n")
    assert any(
        "गोल ब्रैकेट" in e
        for e in errors
    ), f"genuinely unbalanced parens not flagged: {errors}"


def test_genuinely_unbalanced_quotes_still_flagged():
    errors = lint_maithili_code('छपाउ("hi)\n')
    assert any("उद्धरण" in e for e in errors), (
        f"genuinely unbalanced quotes not flagged: {errors}"
    )
