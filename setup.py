"""Legacy setup shim — canonical metadata lives in pyproject.toml.

Kept for compatibility with tools that still invoke setup.py directly.
Version is read from the package __init__ via regex (not import) so
the shim works in isolated build environments where the package is
not yet importable.
"""
import re
from pathlib import Path

from setuptools import setup, find_packages


def _read_version() -> str:
    init_py = Path(__file__).parent / "maithili_dsl" / "__init__.py"
    text = init_py.read_text(encoding="utf-8")
    match = re.search(r'^__version__\s*=\s*["\']([^"\']+)["\']', text, re.M)
    if not match:
        raise RuntimeError("Could not locate __version__ in maithili_dsl/__init__.py")
    return match.group(1)


setup(
    name='python_maithili',
    version=_read_version(),
    description='Run Python code written in Maithili using Devanagari script',
    author='Bishwas Jha',
    author_email='jha.bishwas@gmail.com',
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'python_maithili=maithili_dsl.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
