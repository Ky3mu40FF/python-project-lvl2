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


def parse_data(data_format, imported_data):
    """Open file with passed path.

    Args:
        data_format (str): Data format (ex. json, yaml and etc).
        imported_data (str|byte): Data to parse

    Returns:
        (dict): Dict of parsed file (json to dict).

    Raises:
        ValueError: Not supported file format.
    """
    # Get file extension and check if this extension is supported.
    available_parsers = get_available_parsers()
    if data_format not in available_parsers:
        raise ValueError('Given data format ({0}) is not supported'.format(
            data_format,
        ))

    return get_available_parsers()[data_format](imported_data)
