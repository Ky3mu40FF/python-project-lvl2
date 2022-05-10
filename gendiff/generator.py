"""generator module."""

from .formatters import FORMATTERS
from .parser import get_parsed_file


def compare_data(data1, data2):
    """Compare two data.
    
    Args:
        data1 (): DATA1.
        data2 (): DATA2.

    Returns:
        (dict): COMPARE RESULT."""
    result = {}
    common_keys = data1.keys() & data2.keys()
    removed_keys = data1.keys() - data2.keys()
    added_keys = data2.keys() - data1.keys()

    for key in common_keys:
        if isinstance(data1[key], dict) and isinstance(data2[key], dict):
            result[key] = {
                'status': 'NESTED',
                'value': compare_data(data1[key], data2[key]),
            }
        elif data1[key] == data2[key]:
            result[key] = {
                'status': 'EQUAL',
                'value': data1[key],
            }
        else:
            result[key] = {
                'status': 'MODIFIED',
                'old_value': compare_data(data1[key], data1[key]) if isinstance(data1[key], dict) else data1[key],
                'value': compare_data(data2[key], data2[key]) if isinstance(data2[key], dict) else data2[key],
            }

    for key in removed_keys:
        value = compare_data(data1[key], data1[key]) if isinstance(data1[key], dict) else data1[key]
        result[key] = {
                'status': 'REMOVED', 
                'value': value,
            }

    for key in added_keys:
        value = compare_data(data2[key], data2[key]) if isinstance(data2[key], dict) else data2[key]
        result[key] = {
                'status': 'ADDED', 
                'value': value,
            }

    return result


def format_diff(diff, formatter):
    """Format diff with selected formatter.
    
    Args:
        diff (dict): Dict with diff between two datas.
        formatter (str): String with formatter name.
    
    Returns:
        (str): Formatted diff."""
    return formatter(diff)


def generate_diff(first_file, second_file, formatter):
    """Generate string with diffs between two files.

    Args:
        first_file (dict): Dict of first parsed file.
        second_file (dict): Dict of second parsed file.

    Returns:
        (str): String with differences of two files.
    """
    try:
        data1 = get_parsed_file(first_file)
    except ValueError as file1_exception_info:
        print(file1_exception_info)
        return ''

    try:
        data2 = get_parsed_file(second_file)
    except ValueError as file2_exception_info:
        print(file2_exception_info)
        return ''

    diff = compare_data(data1, data2)

    return format_diff(diff, FORMATTERS[formatter])
