#!/usr/bin/env python3
"""gendiff main module."""

import argparse


def main(argv=None):
    """Gendiff entry point.

    Args:
        argv (str): String with passed arguments.
    """
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', help='set format of output')
    args = parser.parse_args(argv)
    print('format: {0}, first_file: {1}, second_file: {2}'.format(
        args.format,
        args.first_file,
        args.second_file,
    ))


if __name__ == '__main__':
    main()
