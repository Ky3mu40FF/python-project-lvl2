"""generator module."""

from collections import namedtuple

from .change_state import (
    ADDED,
    CHANGED_AFTER,
    CHANGED_BEFORE,
    NESTED,
    REMOVED,
    UNCHANGED,
)
from .file_handler import open_file
from .formatters.formatters import FORMATTERS
from .parser import parse_file


def set_state(change_state, key, child):
    """Create pair in format {(state, key): value}.

    Args:
        change_state (str): Change state of current pair key:value.
        key (any): Key of pair.
        child (any): Value of pair

    Returns:
        (dict): Compared pair key:value with change state.
    """
    CompositeKey = namedtuple(
        'Composite_Key',
        [
            'state',
            'property',
        ],
    )
    return {CompositeKey(change_state, key): child}


def get_proper_child_format(child1, child2):
    """Compare or return children in case are they dicts or not.

    Args:
        child1 (any): Child from first dataset.
        child2 (any): Child from second dataset.

    Returns:
        (any): Children compare result in proper format:
            dict with change state or first not dict child as is.
    """
    if not isinstance(child1, dict):
        return child1
    if not isinstance(child2, dict):
        return child2
    return compare_two_trees(child1, child2)


def compare_children(key, child1, child2):
    """Compare children from two datasets at given key.

    Args:
        key (any): Same key from both datasets.
        child1 (any): Child from first dataset.
        child2 (any): Child from second dataset.

    Returns:
        (dict): Compare result in format {(state, key): value}.
    """
    children_comparison_result = {}
    both_nested = isinstance(child1, dict) and isinstance(child2, dict)

    if child1 == child2:
        children_comparison_result.update(set_state(
            change_state=UNCHANGED,
            key=key,
            child=get_proper_child_format(child1, child1),
        ))
    elif (child1 != child2) and both_nested:
        children_comparison_result.update(set_state(
            change_state=NESTED,
            key=key,
            child=get_proper_child_format(child1, child2),
        ))
    else:
        children_comparison_result.update(set_state(
            change_state=CHANGED_BEFORE,
            key=key,
            child=get_proper_child_format(child1, child1),
        ))
        children_comparison_result.update(set_state(
            change_state=CHANGED_AFTER,
            key=key,
            child=get_proper_child_format(child2, child2),
        ))
    return children_comparison_result


def compare_two_trees(tree1, tree2):
    """Get change states between two datasets.

    Args:
        tree1 (dict): First dict to compare and to set change state.
        tree2 (dict): Second dict to compare and to set change state.

    Returns:
        (dict): COMPARE RESULT.
    """
    data_with_change_states = {}

    for common_key in tree1.keys() & tree2.keys():
        data_with_change_states.update(compare_children(
            common_key,
            tree1[common_key],
            tree2[common_key],
        ))

    for removed_key in tree1.keys() - tree2.keys():
        # Get value after compare_children function using composite key
        formatted_value = compare_children(
            removed_key,
            tree1[removed_key],
            tree1[removed_key],
        )[(UNCHANGED, removed_key)]
        data_with_change_states.update(set_state(
            REMOVED,
            removed_key,
            formatted_value,
        ))

    for added_key in tree2.keys() - tree1.keys():
        # Get value after compare_children function using composite key
        formatted_value = compare_children(
            added_key,
            tree2[added_key],
            tree2[added_key],
        )[(UNCHANGED, added_key)]
        data_with_change_states.update(set_state(
            ADDED,
            added_key,
            formatted_value,
        ))

    return data_with_change_states


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

    diff = compare_two_trees(tree1, tree2)

    return format_diff(diff, FORMATTERS[formatter])
