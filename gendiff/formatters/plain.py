"""gendiff.formatters.stylish module."""

from types import MappingProxyType

from ..change_state import (
    ADDED,
    CHANGED_AFTER,
    CHANGED_BEFORE,
    NESTED,
    REMOVED,
)

KEY_DIFF_TEMPLATES = MappingProxyType({
    ADDED: "Property '{0}' was added with value: {1}",
    CHANGED_BEFORE: "Property '{0}' was updated. From {1} to {2}",
    CHANGED_AFTER: "Property '{0}' was updated. From {1} to {2}",
    NESTED: '',
    REMOVED: "Property '{0}' was removed",
})

VALUES_CONVERT_PAIRS = MappingProxyType({
    True: 'true',
    False: 'false',
    None: 'null',
})


def is_value_hashable(object_to_check):
    """Check if given object hashable.

    Args:
        object_to_check (any): Object to chek if it is hashable.

    Returns:
        (bool): True if hashable. False otherwise.
    """
    try:
        hash(object_to_check)
    except Exception:
        return False
    return True


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
    # Check if given value not hashable (dict for example).
    # to prevent exception at searching for value
    # in keys of VALUES_CONVERT_PAIRS dict.
    if not is_value_hashable(value_to_convert):
        if isinstance(value_to_convert, dict):
            return '[complex value]'
        return repr(value_to_convert)
    if not (isinstance(value_to_convert, bool) or value_to_convert is None):
        return repr(value_to_convert)
    # Return value from defined converting pairs.
    # Otherwise return printable representational string of the given value.
    return VALUES_CONVERT_PAIRS.get(
        value_to_convert,
        repr(value_to_convert),
    )


def sort_diff_dict(dict_to_sort):
    """Sort given dictionary with tuple as a key.

    This functions sorts dictionary with structure:
    {(change_state, property): value}.
    First it sorts by change_state.
    Than it sorts by property.
    Sorting by change_state is for keep order: before -> after.
    Sorting by property is ascending/alphabetically.

    Args:
        dict_to_sort (dict): Dictionary to sort.

    Returns:
        (dict): Sorted dictionary.
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


def filter_diff_dict(dict_to_filter):
    """Filter given dict to exclude unnecessary change_states.

    Args:
        dict_to_filter (dict): Dictionary to filter.

    Returns:
        (dict): Filtered dictionary.
    """
    return {
        composite_key: compared_value
        for composite_key, compared_value in dict_to_filter.items()
        if composite_key.state in KEY_DIFF_TEMPLATES
    }


def differences_to_plain_format_string(dict_with_diffs):
    """Convert prepared dict with differences to plain format string.

    Args:
        dict_with_diffs (dict): Prepared dictionary with differences.

    Returns:
        (str): Differences in Plain format.
    """
    output_lines = []
    for affected_property, template_and_values in dict_with_diffs.items():
        output_lines.append(template_and_values['template'].format(
            affected_property,
            *template_and_values['values'],
        ))
    return '\n'.join(output_lines)


def render(diff_data):
    """Render dictionary with differences between two datasets into string.

    Args:
        diff_data (dict): Dictionary with differences.

    Returns:
        (str): String showing differences between two datasets.
    """
    def walk(subtree, path=''):
        level_diff = {}
        adapted_diff_dict = filter_diff_dict(sort_diff_dict(subtree))
        for composite_key, compared_value in adapted_diff_dict.items():

            affected_property = '.'.join(
                [path, composite_key.property],
            ).strip('.')

            if composite_key.state == NESTED:
                level_diff.update(walk(compared_value, affected_property))
                continue

            level_diff.setdefault(affected_property, {})
            level_diff[affected_property].update({
                'template': KEY_DIFF_TEMPLATES[composite_key.state],
            })
            level_diff[affected_property].setdefault(
                'values',
                [],
            ).append(convert_value(compared_value))

        return level_diff

    return differences_to_plain_format_string(walk(diff_data))
