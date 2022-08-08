"""gendiff.formatters.stylish module."""

import json
from types import MappingProxyType  # Immutable dict for constant (WPS407)

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

KEY_DIFF_SIGNS = MappingProxyType({
    ADDED: '+',
    CHANGED_FROM: '-',
    CHANGED_TO: '+',
    NESTED: ' ',
    REMOVED: '-',
    UNCHANGED: ' ',
})

VALUES_CONVERT_PAIRS = MappingProxyType({
    True: 'true',
    False: 'false',
    None: 'null',
})


def render(diff_data):
    """Render difference data in stylish format.

    Args:
        diff_data (dict): Dictionary with differences.

    Returns:
        (str): String with differences in stylish format.
    """
    def walk(subtree, depth=1):
        level_diff = []
        for key, status_with_value in subtree.items():
            if status_with_value[DIFF_CHANGE_TYPE] == NESTED:
                level_diff.append(format_diff_output(
                    compared_key=key,
                    compared_value='\n'.join(walk(
                        status_with_value[DIFF_VALUE],
                        depth + 1,
                    )),
                    change_state=status_with_value[DIFF_CHANGE_TYPE],
                    depth=depth,
                ))
                continue
            level_diff.append(format_diff_output(
                compared_key=key,
                compared_value=status_with_value[DIFF_VALUE],
                change_state=status_with_value[DIFF_CHANGE_TYPE],
                depth=depth,
            ))
        return level_diff

    return '\n'.join(['{', *walk(diff_data), '}'])


def format_diff_output(
    compared_key,
    compared_value,
    change_state,
    depth,
):
    """Generate formatted string with diff between two files at specific key.

    Args:
        compared_key (str): Key.
        compared_value (any): Value.
        change_state (str): Type of difference.
        depth (int): Number of current level in nested structure.

    Returns:
        (str): String with difference of two files at specific key.
    """
    indent = generate_indent(level=depth)

    if change_state == NESTED:
        return '{0}{1} {2}: {{\n{3}\n{4}}}'.format(
            indent[:-2],  # amount of spaces according depth.
            KEY_DIFF_SIGNS[change_state],  # Diff sign.
            compared_key,
            format_child(
                convert_value(compared_value),
                depth,
            ),
            indent,
        )

    if change_state == CHANGED:
        change = []
        change.append('{0}{1} {2}: {3}'.format(
            indent[:-2],  # amount of spaces according depth.
            KEY_DIFF_SIGNS[CHANGED_FROM],
            compared_key,
            format_child(
                convert_value(compared_value[CHANGED_FROM]),
                depth,
            ),
        ))
        change.append('{0}{1} {2}: {3}'.format(
            indent[:-2],  # amount of spaces according depth.
            KEY_DIFF_SIGNS[CHANGED_TO],
            compared_key,
            format_child(
                convert_value(compared_value[CHANGED_TO]),
                depth,
            ),
        ))
        return '\n'.join(change)

    return '{0}{1} {2}: {3}'.format(
        indent[:-2],  # amount of spaces according depth.
        KEY_DIFF_SIGNS[change_state],
        compared_key,
        format_child(
            convert_value(compared_value),
            depth,
        ),
    )


def format_child(child, depth):
    """Format child to output.

    Args:
        child (any): Child to format.
        depth (int): Depth of parent.

    Returns:
        (any): Formatted child.
    """
    if isinstance(child, dict):
        elements = ['{']
        elements_indent = generate_indent(depth + 1)
        for key, child_value in child.items():
            if isinstance(child_value, dict):
                elements.append('{0}{1}: {2}'.format(
                    elements_indent,
                    key,
                    format_child(child_value, depth + 1),
                ))
                continue
            elements.append('{0}{1}: {2}'.format(
                elements_indent,
                key,
                child_value,
            ))
        elements.append('{0}}}'.format(
            generate_indent(depth),
        ))
        return '\n'.join(elements)
    return child


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

    Args:
        value_to_convert (any): Value to convert to JSON format.

    Returns:
        (any): Converted value to JSON format.
    """
    if value_to_convert in (True, False, None):  # noqa: WPS510
        return json.dumps(value_to_convert)
    return value_to_convert
