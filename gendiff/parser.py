"""parser module."""

import json
import os
from types import MappingProxyType  # Immutable dict for constant (WPS407)

import yaml

SUPPORTED_FILE_FORMATS = MappingProxyType({
    'json': ['.json'],
    'yaml': ['.yml', '.yaml'],
})


def json_parser(input_file):
    """Parse json file.

    Args:
        input_file (file): Opened json file.

    Returns:
        (dict): Dict of parsed file (json to dict).
    """
    return json.load(input_file)


def yaml_parser(input_file):
    """Parse yaml file.

    Args:
        input_file (file): Opened yaml file.

    Returns:
        (dict): Dict of parsed file (yaml to dict).
    """
    return yaml.safe_load(input_file)


def get_file_format(file_extension):
    """Get file format using file extension.

    Args:
        file_extension (str): File extension.

    Returns:
        format (str): File format.
    """
    for file_format, extensions in SUPPORTED_FILE_FORMATS.items():
        if file_extension in extensions:
            return file_format


def get_available_parsers():
    """Give a list of available parsers.

    Returns:
        (dict[str, func]): Available parsers for each supported formats.
    """
    return MappingProxyType({
        'json': json_parser,
        'yaml': yaml_parser,
    })


def get_parsed_file(filepath):
    """Open file with passed path.

    Args:
        filepath (str): String with path to file.

    Returns:
        (dict): Dict of parsed file (json to dict).

    Raises:
        ValueError: Not supported file format.
    """
    # Get file extension and check if this extension is supported.
    _, file_ext = os.path.splitext(filepath)
    if not any(file_ext in ext for ext in SUPPORTED_FILE_FORMATS.values()):
        raise ValueError('File with "{0}" extension is not supported'.format(
            file_ext,
        ))

    # Get file format using extension
    file_format = get_file_format(file_ext)

    with open(filepath, 'r') as input_file:
        parsed_file = get_available_parsers()[file_format](input_file)
    return parsed_file
