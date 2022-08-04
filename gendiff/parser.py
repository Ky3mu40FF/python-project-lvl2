"""parser module."""

import json
from types import MappingProxyType  # Immutable dict for constant (WPS407)

import yaml


def json_parser(input_file):
    """Parse json file.

    Args:
        input_file (file): Opened json file.

    Returns:
        (dict): Dict of parsed file (json to dict).
    """
    return json.loads(input_file)


def yaml_parser(input_file):
    """Parse yaml file.

    Args:
        input_file (file): Opened yaml file.

    Returns:
        (dict): Dict of parsed file (yaml to dict).
    """
    return yaml.safe_load(input_file)


def get_available_parsers():
    """Give a list of available parsers.

    Returns:
        (dict[str, func]): Available parsers for each supported formats.
    """
    return MappingProxyType({
        'json': json_parser,
        'yaml': yaml_parser,
    })


def parse_file(file_format, file_content):
    """Open file with passed path.

    Args:
        file_format (str): File format (ex. json, yaml and etc).
        file_content (str|byte): File to parse

    Returns:
        (dict): Dict of parsed file (json to dict).
    """
    return get_available_parsers()[file_format](file_content)
