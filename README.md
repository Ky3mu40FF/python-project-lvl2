# Status
### Hexlet tests and linter status:
[![Actions Status](https://github.com/Ky3mu40FF/python-project-lvl2/workflows/hexlet-check/badge.svg)](https://github.com/Ky3mu40FF/python-project-lvl2/actions)
### CodeClimate Maintainability and Test Coverage status:
[![Maintainability](https://api.codeclimate.com/v1/badges/3560112894cb9d62bb4e/maintainability)](https://codeclimate.com/github/Ky3mu40FF/python-project-lvl2/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/3560112894cb9d62bb4e/test_coverage)](https://codeclimate.com/github/Ky3mu40FF/python-project-lvl2/test_coverage)
### Internal tests and linter status:
![Tests and Linter Status](https://github.com/Ky3mu40FF/python-project-lvl2/workflows/code-check/badge.svg)

# Description
This package searchs difference between two files in JSON or YAML formats and displays result in multiple formats.

Supported input formats:
- JSON
- YAML

Supported output formats:
- Plain
- Stylish
- JSON

# Requirements
- Python >= 3.8 (<3.8 not tested)

# Dev-requirements
- Poetry >= 1.0.0

# Install from index (TestPyPI)
Install this package using pip:
- Ubuntu:

    `python3 -m pip install --user --index-url https://test.pypi.org/simple/ gendiff-ky3mu40ff==1.0.0`

# Build and install from source:
1. Clone this repository and move to project directory
2. Install poetry: `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -`
3. Install all dependencies: `make install`
4. Build package: `make build`
5. Install package to user environment: `make package-install`
6. Run program. Pass two files and select one of the available output formats. Default is Stylish.

# Asciinema records
## Using gendiff with flat json and yaml files (Step 5):
[![asciicast](https://asciinema.org/a/fHTqjkrZypwcPQu321nAmvy6H.svg)](https://asciinema.org/a/fHTqjkrZypwcPQu321nAmvy6H)
## Using gendiff with nested json and yaml files (Step 6):
[![asciicast](https://asciinema.org/a/IcSKETp2253K5BOSGLChnuLI5.svg)](https://asciinema.org/a/IcSKETp2253K5BOSGLChnuLI5)
## Using gendiff with plain formatter (Step 7):
[![asciicast](https://asciinema.org/a/nIg4jXBU57LEovAaDQjbQyM20.svg)](https://asciinema.org/a/nIg4jXBU57LEovAaDQjbQyM20)
## Using gendiff with json formatter (Step 8):
[![asciicast](https://asciinema.org/a/7H1kRyFJEgDHnAl68dCjnQIAB.svg)](https://asciinema.org/a/7H1kRyFJEgDHnAl68dCjnQIAB)