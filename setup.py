
# setup.py

from setuptools import setup, find_packages

setup(
    name='python_maithili',
    version='0.1.0',
    description='Run Python code written in Maithili using Devanagari script',
    author='Bishwas Jha',
    author_email='jha.bishwas@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'python_maithili=maithili_dsl.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)