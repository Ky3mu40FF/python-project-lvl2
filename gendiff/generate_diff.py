"""generator module."""
from gendiff.diff_tree_builder import compare_tree
from gendiff.file_handler import open_file
from gendiff.formatters.formatters import FORMATTERS
from gendiff.parser import parse_file


def generate_diff(first_file, second_file, formatter='stylish'):
    """
    Generate string with diffs between two files.

    Args:
        first_file (dict): Dict of first parsed file.
        second_file (dict): Dict of second parsed file.
        formatter (string): SELECTED FORMATTER NAME.

    Returns:
        (str): String with differences of two files.
    """
    tree1 = get_data(first_file)
    tree2 = get_data(second_file)

    if not all([tree1, tree2]):
        return ''

    diff = compare_tree(tree1, tree2)
    return format_diff(diff, FORMATTERS[formatter])


def get_data(file_path):
    """
    Try to open and parse given data.

    Args:
        file_path (str): String with path to file.

    Returns:
        (any): Parsed file. None if import or parsing failed.
    """
    opened_file = open_file(file_path)
    return parse_file(
        opened_file.file_format,
        opened_file.file_content,
    )


def format_diff(diff, formatter):
    """
    Format diff with selected formatter.

    Args:
        diff (dict): Dict with diff between two datas.
        formatter (str): String with formatter name.

    Returns:
        (str): Formatted diff.
    """
    return formatter(diff)
