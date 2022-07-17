"""tests for gendiff package."""
from gendiff.scripts.gendiff import main
from .conftest import (
  TEST_FILES_RELATIVE_PATHS,
  FLAT_JSON_1,
  FLAT_JSON_2,
  NESTED_JSON_1,
  NESTED_JSON_2,
)


FLAT_FILES_DIFF = """{
  - follow: false
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}"""

HELP_OUTPUT = '''[-h] [-f FORMAT] first_file second_file

Generate diff

positional arguments:
  first_file
  second_file

optional arguments:
  -h, --help            show this help message and exit
  -f FORMAT, --format FORMAT
                        set format of output'''
NO_ARGS_ERROR_SUBSTRING = "error: the following arguments are required: first_file, second_file"
NO_SECOND_ARG_ERROR_SUBSTRING = "error: the following arguments are required: second_file"


def test_gendiff_main_without_args(capsys):
    try:
        main([])
    except SystemExit:
        pass
    captured = capsys.readouterr()
    assert NO_ARGS_ERROR_SUBSTRING in captured.err


def test_gendiff_main_with_one_arg(capsys):
    try:
        main([TEST_FILES_RELATIVE_PATHS[FLAT_JSON_1]])
    except SystemExit:
        pass
    captured = capsys.readouterr()
    assert NO_SECOND_ARG_ERROR_SUBSTRING in captured.err


def test_gendiff_main_with_all_args(capsys):
    try:
        main([
            *("-f", "stylish"),
            TEST_FILES_RELATIVE_PATHS[FLAT_JSON_1],
            TEST_FILES_RELATIVE_PATHS[FLAT_JSON_2],
        ])
    except SystemExit:
        pass
    captured = capsys.readouterr()
    assert FLAT_FILES_DIFF in captured.out


def test_gendiff_main_call_help(capsys):
    try:
        main(["-h"])
    except SystemExit:
        pass
    captured = capsys.readouterr()
    print(captured.out)
    assert HELP_OUTPUT in captured.out
