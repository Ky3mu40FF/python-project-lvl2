"""file_handler module."""

import os
from collections import namedtuple
from types import MappingProxyType  # Immutable dict for constant (WPS407)

SUPPORTED_FILE_FORMATS = MappingProxyType({
    'json': ['.json'],
    'yaml': ['.yml', '.yaml'],
})


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


def open_file(filepath):
    """Open local file with passed path.

    Args:
        filepath (str): String with path to file.

    Returns:
        (namedtuple[format, data]): Opened file with format.
    """
    _, file_ext = os.path.splitext(filepath)

    file_format = get_file_format(file_ext)

    OpenedFile = namedtuple('OpenedFile', ['file_format', 'file_content'])

    with open(filepath, 'r') as input_file:
        return OpenedFile(
            file_format,
            input_file.read(),
        )
