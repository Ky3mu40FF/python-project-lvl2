#!/usr/bin/env python3
"""gendiff main module."""

import argparse

from ..generator import generate_diff


def main(argv=None):
    """Gendiff entry point.

    Args:
        argv (str): String with passed arguments.
    """
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument(
        '-f',
        '--format',
        help='set format of output',
        default='stylish',
    )
    args = parser.parse_args(argv)
    print(generate_diff(
        args.first_file,
        args.second_file,
        args.format,
    ))


if __name__ == '__main__':
    main()
