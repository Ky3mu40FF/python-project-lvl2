"""diff_tree_generator module."""

from gendiff.change_type import (
    ADDED,
    CHANGED,
    CHANGED_FROM,
    CHANGED_TO,
    NESTED,
    REMOVED,
    UNCHANGED,
)

DIFF_CHANGE_TYPE = 'change_type'
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

    for key in sorted(set().union(tree1.keys(), tree2.keys())):

        if key not in tree1.keys() and key in tree2.keys():
            differences[key] = {
                DIFF_CHANGE_TYPE: ADDED,
                DIFF_VALUE: tree2[key],
            }
        elif key in tree1.keys() and key not in tree2.keys():
            differences[key] = {
                DIFF_CHANGE_TYPE: REMOVED,
                DIFF_VALUE: tree1[key],
            }
        elif tree1[key] == tree2[key]:
            differences[key] = {
                DIFF_CHANGE_TYPE: UNCHANGED,
                DIFF_VALUE: tree1[key],
            }
        elif isinstance(tree1[key], dict) and isinstance(tree2[key], dict):
            differences[key] = {
                DIFF_CHANGE_TYPE: NESTED,
                DIFF_VALUE: compare_tree(tree1[key], tree2[key]),
            }
        else:
            differences[key] = {
                DIFF_CHANGE_TYPE: CHANGED,
                DIFF_VALUE: {
                    CHANGED_FROM: tree1[key],
                    CHANGED_TO: tree2[key],
                },
            }

    return differences
