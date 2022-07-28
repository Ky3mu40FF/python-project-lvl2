"""file_handler module."""

import os
from collections import namedtuple
from types import MappingProxyType  # Immutable dict for constant (WPS407)
from urllib.parse import urlparse

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


def open_local_file(filepath):
    """Open local file with passed path.

    Args:
        filepath (str): String with path to file.

    Returns:
        (namedtuple[format, data]): Opened file with format.

    Raises:
        IOError: File does not exists or Not supported file format.
    """
    if not os.path.exists(filepath):
        raise IOError('File does not exists. \nFilepath: {0}'.format(
            filepath,
        ))

    # Get file extension and check if this extension is supported.
    _, file_ext = os.path.splitext(filepath)
    if not any(file_ext in ext for ext in SUPPORTED_FILE_FORMATS.values()):
        raise IOError('File with "{0}" extension is not supported'.format(
            file_ext,
        ))

    # Get file format using extension
    file_format = get_file_format(file_ext)

    ImportedData = namedtuple('ImportedData', ['data_format', 'data'])

    with open(filepath, 'r') as input_file:
        return ImportedData(
            file_format,
            input_file.read(),
        )


def import_data(url):
    """Get info about data to import and choose way to import.

    Args:
        url (str): String with url to data.

    Returns:
        (namedtuple[format, data]): Imported data. None if import failed.

    Raises:
        IOError: Not supported URL scheme.
    """
    url_parse_result = urlparse(url)

    imported_data = None

    if not url_parse_result.scheme and not url_parse_result.netloc:
        # Case: local file
        imported_data = open_local_file(url)
    else:
        print('Given URL is not supported.')
        raise IOError('Given URL is not supported.\nURL: {0}'.format(
            url,
        ))

    return imported_data
