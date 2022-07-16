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

KEY_DIFF_TEMPLATES = MappingProxyType({
    ADDED: "Property '{0}' was added with value: {1}",
    CHANGED_BEFORE: "Property '{0}' was updated. From {1} to {2}",
    NESTED: "",
    REMOVED: "Property '{0}' was removed",
})

VALUES_CONVERT_PAIRS = MappingProxyType({
    True: 'true',
    False: 'false',
    None: 'null',
})


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
    if '__hash__' in dir(value_to_convert):
        return '[complex value]' if isinstance(value_to_convert, dict) else repr(value_to_convert)
    # If value not found in keys,
    # than return value as is
    return VALUES_CONVERT_PAIRS.get(
        value_to_convert,
        value_to_convert,
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


def format_message(affected_property, values, state):
    return KEY_DIFF_TEMPLATES[state].format(
        affected_property,
        *values,
    )


def render(diff_data):
    """Render dictionary with differences between two datasets into string.

    Args:
        diff_data (dict): Dictionary with differences.

    Returns:
        (str): String showing differences between two datasets.
    """
    def walk(subtree, path=''):
        level_diff = []

        sorted_dict = sort_diff_dict(subtree)

        for state_with_key, compared_value in sorted_dict.items():
            state, key = state_with_key
            if not state in KEY_DIFF_TEMPLATES:
                continue

            affected_property = '.'.join([path, key]) if path else key

            if state == NESTED:
                level_diff.extend(walk(
                    subtree=compared_value,
                    path=affected_property,
                ))
                continue
            values = [convert_value(compared_value),]

            if state == CHANGED_BEFORE:
                values.append(convert_value(sorted_dict[(CHANGED_AFTER, key)]))
            
            level_diff.append(format_message(
                affected_property=affected_property,
                values=values,
                state=state,
            ))
            
        return level_diff

    return '\n'.join(walk(diff_data))
