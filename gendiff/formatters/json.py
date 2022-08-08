"""gendiff.formatters.json module."""

import json


def render(diff_data):
    """Render dictionary with differences between two datasets as json string.

    Args:
        diff_data (dict): Dictionary with differences.

    Returns:
        (str): JSON string showing differences between two datasets.
    """
    return json.dumps(
        obj=diff_data,
        indent=4,
        sort_keys=True,
    )
