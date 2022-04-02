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
    args = parser.parse_args(argv)
    print(args)


if __name__ == '__main__':
    main()
