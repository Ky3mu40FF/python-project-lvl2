"""gendiff.formatters.stylish module."""

from operator import sub
from types import MappingProxyType  # Immutable dict for constant (WPS407)

KEY_DIFF_SIGNS = MappingProxyType({
    'EQUAL': ' ',
    'NESTED': ' ',
    'REMOVED': '-',
    'ADDED': '+',
})

VALUES_CONVERT_PAIRS = MappingProxyType({
    True: 'true',
    False: 'false',
})

INDENT_CHAR = ' '


def convert_value(value):
    if value is None:
        return 'null'
    elif isinstance(value, bool):
        return VALUES_CONVERT_PAIRS[value]
    else:
        return value



def format_diff_output(key, diff, depth):
    """Generate formatted string with diff between two files at specific key.

    Args:
        diff (str): Type of difference.
        key (str): Key to compare.
        param_value: Value for specific key.

    Returns:
        (str): String with difference of two files at specific key.
    """
    indent = INDENT_CHAR * 4 * depth

    #if diff['status'] == 'NESTED':
    if diff['nested']:
        return '{0}{1} {2}: {{\n{3}\n{4}}}'.format(
            indent[0:-2],  # amount of spaces according depth.
            KEY_DIFF_SIGNS[diff['status']],  # Diff sign.
            key,
            convert_value(diff['value']),
            indent,
        )
    else:
        return '{0}{1} {2}: {3}'.format(
            indent[0: -2],  # amount of spaces according depth.
            KEY_DIFF_SIGNS[diff['status']],  # Diff sign.
            key,
            convert_value(diff['value']),
        )


def render(diff_data):
    """Format diff between two data.
    
    Args:
        diff_data (dict): DIFF.

    Returns:
        (dict): COMPARE RESULT."""
    result = []

    def walk(subtree, depth=1):
        level_diff = []
        for key, value in sorted(subtree.items()):
            if value['status'] == 'NESTED':
                formatted_nested_value = walk(value['value'], depth + 1)
                level_diff.append(format_diff_output(
                    key, 
                    {
                        'status': 'NESTED',
                        'value': '\n'.join(formatted_nested_value),
                        'nested': isinstance(value['value'], dict),
                    }, 
                    depth,
                ))
            elif value['status'] == 'MODIFIED':
                if not isinstance(value['old_value'], dict):
                    level_diff.append(format_diff_output(
                        key, 
                        {
                            'status': 'REMOVED',
                            'value': value['old_value'],
                            'nested': isinstance(value['old_value'], dict),
                        }, 
                        depth,
                    ))
                else:
                    level_diff.append(format_diff_output(
                        key, 
                        {
                            'status': 'REMOVED',
                            'value': '\n'.join(walk(value['old_value'], depth + 1)),
                            'nested': isinstance(value['old_value'], dict),
                        }, 
                        depth,
                    ))
                if not isinstance(value['value'], dict):
                    level_diff.append(format_diff_output(
                        key, 
                        {
                            'status': 'ADDED',
                            'value': value['value'],
                            'nested': isinstance(value['value'], dict),
                        }, 
                        depth,
                    ))
                else:
                    level_diff.append(format_diff_output(
                        key, 
                        {
                            'status': 'ADDED',
                            'value': '\n'.join(walk(value['value'], depth + 1)),
                            'nested': isinstance(value['value'], dict),
                        }, 
                        depth,
                    ))
            else:
                #level_diff.append(format_diff_output(key, value, depth))
                if not isinstance(value['value'], dict):
                    level_diff.append(format_diff_output(
                        key, 
                        {
                            'status': value['status'],
                            'value': value['value'],
                            'nested': isinstance(value['value'], dict),
                        }, 
                        depth,
                    ))
                else:
                    level_diff.append(format_diff_output(
                        key, 
                        {
                            'status': value['status'],
                            'value': '\n'.join(walk(value['value'], depth + 1)),
                            'nested': isinstance(value['value'], dict),
                        }, 
                        depth,
                    ))
        return level_diff
            
    result.append('{')
    result.extend(walk(diff_data))
    result.append('}')

    return '\n'.join(result)
