"""generator module."""

from .change_state import (
    ADDED,
    CHANGED_AFTER,
    CHANGED_BEFORE,
    NESTED,
    REMOVED,
    UNCHANGED,
)
from .formatters import FORMATTERS
from .parser import get_parsed_file


def set_state(state, key, child):
    return {(state, key): child}


def compare_children(key, child1, child2):
    children_comparison_result = {}
    any_nested = isinstance(child1, dict) or isinstance(child2, dict)

    if child1 == child2:
        children_comparison_result.update(set_state(
            UNCHANGED,
            key,
            child1,
        ))
    # If none of passed childs is nested and childs are not equal
    elif not (any_nested) and (child1 != child2):
        children_comparison_result.update(set_state(
            CHANGED_BEFORE,
            key,
            child1,
        ))
        children_comparison_result.update(set_state(
            CHANGED_AFTER,
            key,
            child2,
        ))
    elif any_nested and child1 != child2:
        children_comparison_result.update(set_state(
            NESTED,
            key,
            get_change_states(child1, child2),
        ))
    return children_comparison_result


def get_change_states(data1, data2):
    """
    Get change states between two datasets.

    Args:
        data1 (dict): DATA1.
        data2 (dict): DATA2.

    Returns:
        (dict): COMPARE RESULT.
    """
    data_with_change_states = {}

    for common_key in data1.keys() & data2.keys():
        data_with_change_states.update(compare_children(
            common_key,
            data1[common_key],
            data2[common_key],
        ))

    for removed_key in data1.keys() - data2.keys():
        data_with_change_states.update(set_state(
            REMOVED,
            removed_key,
            data1[removed_key],
        ))

    for added_key in data2.keys() - data1.keys():
        data_with_change_states.update(set_state(
            ADDED,
            added_key,
            data2[added_key],
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


def generate_diff(first_file, second_file, formatter):
    """
    Generate string with diffs between two files.

    Args:
        first_file (dict): Dict of first parsed file.
        second_file (dict): Dict of second parsed file.
        formatter (string): SELECTED FORMATTER NAME.

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

    diff = get_change_states(data1, data2)

    return format_diff(diff, FORMATTERS[formatter])
