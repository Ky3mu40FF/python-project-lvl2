"""gendiff.formatters.json module."""

import json

from ..change_state import (
    ADDED,
    CHANGED_AFTER,
    CHANGED_BEFORE,
    NESTED,
    REMOVED,
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


def remove_redundant_info(data_with_redundance):
    """Remove redundant "state" properties.

    Args:
        data_with_redundance (any): Data with redundance.

    Returns:
        (any): Data with removed redundant info.
    """
    if not isinstance(data_with_redundance, dict):
        return data_with_redundance

    cleaned = {}
    for composite_key, compared_value in data_with_redundance.items():
        cleaned.update({
            composite_key.property: remove_redundant_info(compared_value),
        })


def format_diff(composite_key, compared_value):
    """Format diff info for further export in JSON.

    Args:
        composite_key (tuple): Composite key with state and property.
        compared_value (any): Value.

    Returns:
        (dict): Formatted diffrence.
    """
    level_diff = {}
    if composite_key.state in {ADDED, REMOVED}:
        level_diff.update({
            composite_key.property: {
                'state': composite_key.state,
                'value': remove_redundant_info(compared_value),
            },
        })
    elif composite_key.state in {CHANGED_BEFORE, CHANGED_AFTER}:
        level_diff.setdefault(
            composite_key.property,
            {
                'state': 'changed',
                'values': {
                    CHANGED_BEFORE: None,
                    CHANGED_AFTER: None,
                },
            },
        )
        level_diff[composite_key.property]['values'].update(
            {composite_key.state: remove_redundant_info(compared_value)},
        )
    return level_diff


def render(diff_data):
    """Render dictionary with differences between two datasets as json string.

    Args:
        diff_data (dict): Dictionary with differences.

    Returns:
        (str): JSON string showing differences between two datasets.
    """
    def walk(subtree):
        level_diff = {}

        for composite_key, compared_value in sort_diff_dict(subtree).items():
            if composite_key.state == NESTED:
                level_diff.update({
                    composite_key.property: walk(compared_value),
                })
                continue

            level_diff.update(format_diff(composite_key, compared_value))

        return level_diff
    
    return json.dumps(
            obj=walk(diff_data),
            indent=4,
        )
