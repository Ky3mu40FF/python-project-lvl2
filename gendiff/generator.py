"""generator module."""

from types import MappingProxyType  # Immutable dict for constant (WPS407)

from .parser import get_parsed_file

KEY_DIFF_SIGNS = MappingProxyType({
    'REMAINED': ' ',
    'REMOVED': '-',
    'ADDED': '+',
})


def format_diff_output(diff, key, param_value):
    """Generate formatted string with diff between two files at specific key.

    Args:
        diff (str): Type of difference.
        key (str): Key to compare.
        param_value: Value for specific key.

    Returns:
        (str): String with difference of two files at specific key.
    """
    return '  {0} {1}: {2}'.format(diff, key, param_value)


def get_changes(data1, data2, key):
    """Generate list with diff between two files at specific key.

    Args:
        data1 (dict): Dict of first parsed file.
        data2 (dict): Dict of second parsed file.
        key (str): Key to compare.

    Returns:
        (List): List with differences of two files at specific key.
    """
    if key in (data1.keys() & data2.keys()):
        if data1[key] == data2[key]:
            return [format_diff_output(
                KEY_DIFF_SIGNS['REMAINED'],
                key,
                data1[key],
            )]
        return [
            format_diff_output(
                KEY_DIFF_SIGNS['REMOVED'],
                key,
                data1[key],
            ),
            format_diff_output(
                KEY_DIFF_SIGNS['ADDED'],
                key,
                data2[key],
            ),
        ]
    elif key in (data1.keys() - data2.keys()):
        return [format_diff_output(
            KEY_DIFF_SIGNS['REMOVED'],
            key,
            data1[key],
        )]
    elif key in (data2.keys() - data1.keys()):
        return [format_diff_output(
            KEY_DIFF_SIGNS['ADDED'],
            key,
            data2[key],
        )]


def generate_diff(first_file, second_file):
    """Generate string with diffs between two files.

    Args:
        first_file (dict): Dict of first parsed file.
        second_file (dict): Dict of second parsed file.

    Returns:
        (str): String with differences of two files.
    """
    try:
        data1 = get_parsed_file(first_file)
    except ValueError as e1_info:
        print(e1_info)
        return ''

    try:
        data2 = get_parsed_file(second_file)
    except ValueError as e2_info:
        print(e2_info)
        return ''

    key_diffs = []
    for key in sorted(iter(data1.keys() | data2.keys())):
        key_diffs.extend(get_changes(data1, data2, key))

    return '{0}\n{1}\n{2}'.format('{', '\n'.join(key_diffs), '}')
