# maithili_dsl/transpiler/linter.py

import re

LINT_CONFIG = {
    "enforce_snake_case": False,
    "max_line_length": 80,
    "check_comments": False
}

def is_snake_case(name):
    return bool(re.match(r'^[a-z_][a-z0-9_]*$', name))

def translate_exception_to_maithili(exc):
    translations = {
        "SyntaxError": "वाक्य संरचना में त्रुटि अछि।",
        "NameError": "कोनो नाम घोषित नहि अछि।",
        "TypeError": "प्रकार त्रुटि – गलत प्रकारक मान।",
        "ValueError": "मान त्रुटि – अमान्य मान।",
        "AttributeError": "गुण त्रुटि – वस्तु में अपेक्षित गुण नहि अछि।",
        "IndexError": "सूची सीमा त्रुटि – अनुक्रमणिका बाहर अछि।",
        "KeyError": "कुंजी त्रुटि – कुंजी भेटल नहि।"
    }
    name = type(exc).__name__
    return translations.get(name, f"त्रुटि: {name} – {str(exc)}")

def lint_maithili_code(code, config=LINT_CONFIG):
    errors = []
    lines = code.splitlines()
    declared_functions = set()

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()

        # Check for suspicious control flow or structure lines
        if stripped.endswith(":") and not stripped.startswith(tuple(" \t")):
            if not stripped.split()[0] in ["कार्य", "यदि", "नहि त", "वर्ग", "प्रत्येक"]:
                errors.append(f"पंक्ति {i}: संदिग्ध ढाँचा – '{stripped}'")

        # Check for improper assignment syntax
        if "=" in stripped and stripped.startswith("="):
            errors.append(f"पंक्ति {i}: '=' चिह्नक पहिले कोनो मान अपेक्षित अछि")

        # Check for unbalanced parentheses or quotes
        if stripped.count("(") != stripped.count(")"):
            errors.append(f"पंक्ति {i}: गोल ब्रैकेट असंतुलित अछि")
        if stripped.count("\"") % 2 != 0:
            errors.append(f"पंक्ति {i}: उद्धरण चिह्न जोड़ा में नहि अछि")

        # Check for indentation (must start with 4-space or tab if inside block)
        if line and not line.startswith(" ") and not stripped.endswith(":") and i > 1:
            prev = lines[i-2].strip()
            if prev.endswith(":") and not line.startswith("    ") and not line.startswith("\t"):
                errors.append(f"पंक्ति {i}: इनडेन्टेशन अपेक्षित अछि — '{line.strip()}'")

        # Naming style and assignment validation
        if "=" in stripped and not stripped.startswith("#"):
            var_name = stripped.split("=")[0].strip()
            if not var_name.isidentifier():
                errors.append(f"पंक्ति {i}: चर नाम '{var_name}' वैध नहि अछि")
            elif config.get("enforce_snake_case") and not is_snake_case(var_name):
                errors.append(f"पंक्ति {i}: चर नाम '{var_name}' snake_case में नहि अछि")

        # Line length check
        if config.get("max_line_length") and len(line) > config["max_line_length"]:
            errors.append(f"पंक्ति {i}: पंक्ति बहुत लंबा अछि ({len(line)} वर्ण)")

        # Comment validation
        if config.get("check_comments") and "#" in stripped:
            comment = stripped.split("#", 1)[1].strip()
            if not comment:
                errors.append(f"पंक्ति {i}: टिप्पणी खाली अछि")

        # Detect function definitions
        if stripped.startswith("कार्य"):
            try:
                fname = stripped.split()[1].split("(")[0]
                declared_functions.add(fname)
                if config.get("enforce_snake_case") and not is_snake_case(fname):
                    errors.append(f"पंक्ति {i}: कार्य नाम '{fname}' snake_case में नहि अछि")
            except IndexError:
                errors.append(f"पंक्ति {i}: कार्य नाम सही रूप में परिभाषित नहि अछि")

    # Post-scan: warn if declared functions are unused (except main)
    for f in declared_functions:
        used = any(f in line for line in lines if not line.strip().startswith("कार्य"))
        if not used:
            errors.append(f"चेतावनी: कार्य '{f}' केहनो ठाम प्रयोग नहि कएल गेल अछि")

    return errors
