#!/usr/bin/env python3
"""gendiff main module."""

import argparse

from gendiff.generate_diff import generate_diff


def parse_args():
    """Parse input arguments.

    Returns:
        (any): Parsed arguments.
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
    return parser.parse_args()


def main():
    """Gendiff entry point."""
    args = parse_args()
    print(generate_diff(
        args.first_file,
        args.second_file,
        args.format,
    ))


if __name__ == '__main__':
    main()
