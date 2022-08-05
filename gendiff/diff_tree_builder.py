"""diff_tree_generator module."""
# SimpleNamespace is None alternative,
# because None is representing null after json parsing
from types import SimpleNamespace

from gendiff.change_status import (
    ADDED,
    CHANGED,
    CHANGED_FROM,
    CHANGED_TO,
    NESTED,
    REMOVED,
    UNCHANGED,
)

DIFF_CHANGE_STATUS = 'status'
DIFF_VALUE = 'value'


def compare_tree(tree1, tree2):
    """Compare two trees.

    Args:
        tree1 (dict): First tree.
        tree2 (dict): Second tree.

    Returns:
        (dict): Compare result - Dictionary with differences.
    """
    differences = {}
    # Child not found in tree1
    # -> Property was added.
    if type(tree1) is SimpleNamespace:
        return {
            DIFF_CHANGE_STATUS: ADDED,
            DIFF_VALUE: tree2,
        }
    # Child not found in tree2
    # -> Property was removed.
    elif type(tree2) is SimpleNamespace:
        return {
            DIFF_CHANGE_STATUS: REMOVED,
            DIFF_VALUE: tree1,
        }
    # One of the children or both of them are not dicts and they are not equal
    # -> Property was changed.
    elif type(tree1) != type(tree2) or not isinstance(tree1, dict) and tree1 != tree2:
        return {
            DIFF_CHANGE_STATUS: CHANGED,
            DIFF_VALUE: {
                CHANGED_FROM: tree1,
                CHANGED_TO: tree2,
            },
        }
    # Both children are equal
    # -> Property unchanged.
    elif tree1 == tree2:
        return {
            DIFF_CHANGE_STATUS: UNCHANGED,
            DIFF_VALUE: tree1,
        }
    # Both children are dicts and not equal
    # -> Nested properties need to be compared deeper.
    else:
        for key in sorted(set().union(tree1.keys(), tree2.keys())):
            # Try to get child from trees at given key.
            # If key is not exists in specific tree - return SimpleNamespace instance.
            # It's alternative to None to avoid collision with converted null from JSON.
            tree1_value = tree1.get(key, SimpleNamespace())
            tree2_value = tree2.get(key, SimpleNamespace())
            nested_compare_result = compare_tree(tree1_value, tree2_value)
            if isinstance(tree1_value, dict) and isinstance(tree2_value, dict):
                differences[key] = {
                    DIFF_CHANGE_STATUS: NESTED,
                    DIFF_VALUE: nested_compare_result,
                }
            else:
                differences[key] = nested_compare_result

    return differences
