"""gendiff.formatters.stylish module."""

import json
from types import MappingProxyType

from gendiff.change_type import (
    ADDED,
    CHANGED,
    CHANGED_FROM,
    CHANGED_TO,
    NESTED,
    REMOVED,
    UNCHANGED,
)
from gendiff.diff_properties import DIFF_CHANGE_TYPE, DIFF_VALUE

KEY_DIFF_TEMPLATES = MappingProxyType({
    ADDED: "Property '{0}' was added with value: {1}",
    CHANGED: "Property '{0}' was updated. From {1} to {2}",
    NESTED: '',
    REMOVED: "Property '{0}' was removed",
})

VALUES_CONVERT_PAIRS = MappingProxyType({
    True: 'true',
    False: 'false',
    None: 'null',
})

PLAIN_CHANGE_TYPE = 'change_type'
PLAIN_TEMPLATE = 'template'
PLAIN_VALUE = 'value'


def render(diff_data):
    """Render dictionary with differences between two datasets into string.

    Args:
        diff_data (dict): Dictionary with differences.

    Returns:
        (str): String showing differences between two datasets.
    """
    diff_data_with_templates = prepare_templates_based_on_status(diff_data)

    return differences_to_plain_format_string(diff_data_with_templates)


def prepare_templates_based_on_status(diff_data):
    """Set template for each type of difference.

    Args:
        diff_data (dict): Dictionary with differences.

    Returns:
        (dict): Dictionary with differences and matching templates to fill.
    """
    def walk(subtree, path=''):
        level_diff = {}
        for key, status_with_value in filter_subtree(subtree).items():

            affected_property = '.'.join(
                [path, key],
            ).strip('.')

            if status_with_value[DIFF_CHANGE_TYPE] == NESTED:
                level_diff.update(walk(
                    status_with_value[DIFF_VALUE],
                    affected_property,
                ))
                continue

            level_diff.setdefault(affected_property, {})
            level_diff[affected_property].update({
                PLAIN_CHANGE_TYPE: status_with_value[DIFF_CHANGE_TYPE],
                PLAIN_TEMPLATE: KEY_DIFF_TEMPLATES[status_with_value[DIFF_CHANGE_TYPE]],
            })
            level_diff[affected_property][PLAIN_VALUE] = status_with_value[DIFF_VALUE]

        return level_diff

    return walk(diff_data)


def differences_to_plain_format_string(dict_with_diffs):
    """Convert prepared dict with differences to plain format string.

    Args:
        dict_with_diffs (dict): Prepared dictionary with differences.

    Returns:
        (str): Differences in Plain format.
    """
    output_lines = []
    for affected_property, template_and_values in dict_with_diffs.items():
        if template_and_values[PLAIN_CHANGE_TYPE] == CHANGED:
            output_lines.append(template_and_values[PLAIN_TEMPLATE].format(
                affected_property,
                convert_value(template_and_values[PLAIN_VALUE][CHANGED_FROM]),
                convert_value(template_and_values[PLAIN_VALUE][CHANGED_TO]),
            ))
        else:
            output_lines.append(template_and_values[PLAIN_TEMPLATE].format(
                affected_property,
                convert_value(template_and_values[PLAIN_VALUE]),
            ))
    return '\n'.join(output_lines)


def convert_value(value_to_convert):
    """Convert given value from Python format to JSON format.

    Args:
        value_to_convert (any): Value to convert to JSON format.

    Returns:
        (any): Converted value to JSON format.
    """
    if isinstance(value_to_convert, dict):
        return '[complex value]'
    elif value_to_convert in (True, False, None):  # noqa: WPS510
        return json.dumps(value_to_convert)
    return repr(value_to_convert)


def filter_subtree(subtree):
    """Filter subtree to exclude unchanged elements.

    Args:
        subtree (dict): Subtree to filter.

    Returns:
        (dict): Filtered subtree.
    """
    return {
        subtree_key: subtree_value
        for (subtree_key, subtree_value) in subtree.items()
        if subtree_value[DIFF_CHANGE_TYPE] != UNCHANGED
    }
