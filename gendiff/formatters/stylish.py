"""gendiff.formatters.stylish module."""

from types import MappingProxyType  # Immutable dict for constant (WPS407)

from ..change_state import (
    ADDED,
    CHANGED_AFTER,
    CHANGED_BEFORE,
    NESTED,
    REMOVED,
    UNCHANGED,
)

KEY_DIFF_SIGNS = MappingProxyType({
    ADDED: '+',
    CHANGED_AFTER: '+',
    CHANGED_BEFORE: '-',
    NESTED: ' ',
    REMOVED: '-',
    UNCHANGED: ' ',
})

VALUES_CONVERT_PAIRS = MappingProxyType({
    True: 'true',
    False: 'false',
    None: 'null',
})


def generate_indent(
    level,
    indent_char=' ',
    chars_per_level=4,
):
    """Generate indent given lenght and using specified character.

    Args:
        level (int): Number of current level in nested structure.
        indent_char (str): Characted that will be displayed as indent.
        chars_per_level (int): Count of indent characters in one level.

    Returns:
        (str): Indent for current level in nested structure.
    """
    return indent_char * chars_per_level * level


def convert_value(value_to_convert):
    """Convert given value from Python format to JSON format.

    If value should be converted to JSON format,
    function will return string with converted value.
    Else same value will be returned.

    Args:
        value_to_convert (any): Value to convert to JSON format.

    Returns:
        (any): Converted value to JSON format.
    """
    if not (isinstance(value_to_convert, bool) or value_to_convert is None):
        return value_to_convert
    # If value not found in keys,
    # than return value as is
    return VALUES_CONVERT_PAIRS.get(
        value_to_convert,
        value_to_convert,
    )


def format_diff_output(
    compared_key,
    compared_value,
    change_state,
    is_nested,
    depth,
):
    """Generate formatted string with diff between two files at specific key.

    Args:
        compared_key (str): Key.
        compared_value (any): Value.
        change_state (str): Type of difference.
        is_nested (bool): Is given value nested?
        depth (int): Number of current level in nested structure.

    Returns:
        (str): String with difference of two files at specific key.
    """
    indent = generate_indent(level=depth)

    if is_nested:
        return '{0}{1} {2}: {{\n{3}\n{4}}}'.format(
            indent[:-2],  # amount of spaces according depth.
            KEY_DIFF_SIGNS[change_state],  # Diff sign.
            compared_key,
            convert_value(compared_value),
            indent,
        )

    return '{0}{1} {2}: {3}'.format(
        indent[:-2],  # amount of spaces according depth.
        KEY_DIFF_SIGNS[change_state],
        compared_key,
        convert_value(compared_value),
    )


def sort_diff_dict(dict_to_sort):
    """Sort given dictionary with tuple as a key.

    This functions sorts dictionary with next structure:
    {(change_state, key): value}.
    First it sorts by change_state.
    Than it sorts by key value.
    Sorting by change_state is for keep order: before -> after.
    Sorting by key is ascending/alphabetically.

    Args:
        dict_to_sort (dict): Dictionary to sort.

    Returns:
        (str): String with difference of two files at specific key.
    """
    # Sorting dictionary by change state stored in composite key
    dict_sorted_by_change_state = {
        tuple_key: dict_to_sort[tuple_key]
        for tuple_key in sorted(
            dict_to_sort.keys(),
            key=lambda key_to_sort: key_to_sort[0],
            reverse=True,
        )
    }
    # Sorting and returning dictionary by keys's value stored in composite key
    return {
        tuple_key: dict_sorted_by_change_state[tuple_key]
        for tuple_key in sorted(
            dict_sorted_by_change_state.keys(),
            key=lambda key_to_sort: key_to_sort[1],
            reverse=False,
        )
    }


def render(diff_data):
    """Render dictionary with differences between two datasets into string.

    Args:
        diff_data (dict): Dictionary with differences.

    Returns:
        (str): String showing differences between two datasets.
    """
    def walk(subtree, depth=1):
        level_diff = []

        for state_with_key, compared_value in sort_diff_dict(subtree).items():
            state, key = state_with_key

            if isinstance(compared_value, dict):
                level_diff.append(format_diff_output(
                    compared_key=key,
                    compared_value='\n'.join(walk(compared_value, depth + 1)),
                    change_state=state,
                    is_nested=True,
                    depth=depth,
                ))
                continue

            level_diff.append(format_diff_output(
                compared_key=key,
                compared_value=compared_value,
                change_state=state,
                is_nested=False,
                depth=depth,
            ))

        return level_diff

    return '\n'.join(['{', *walk(diff_data), '}'])
