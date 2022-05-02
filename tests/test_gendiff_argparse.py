"""tests for gendiff package."""
from gendiff.scripts.gendiff import main
from .conftest import JSON_FILES_RELATIVE_PATHS


file1_file2_json_diff = """{
  - follow: False
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: True
}"""

help_output = '''[-h] [-f FORMAT] first_file second_file

Generate diff

positional arguments:
  first_file
  second_file

optional arguments:
  -h, --help            show this help message and exit
  -f FORMAT, --format FORMAT
                        set format of output'''
no_args_error_substring = "error: the following arguments are required: first_file, second_file"
no_second_arg_error_substring = "error: the following arguments are required: second_file"


def test_gendiff_main_without_args(capsys):
    try:
        main([])
    except SystemExit:
        pass
    captured = capsys.readouterr()
    assert no_args_error_substring in captured.err


def test_gendiff_main_with_one_arg(capsys):
    try:
        main([JSON_FILES_RELATIVE_PATHS['flat_file1']])
    except SystemExit:
        pass
    captured = capsys.readouterr()
    assert no_second_arg_error_substring in captured.err


def test_gendiff_main_with_all_args(capsys):
    try:
        main([
            *("-f", "json"),
            JSON_FILES_RELATIVE_PATHS['flat_file1'],
            JSON_FILES_RELATIVE_PATHS['flat_file2'],
        ])
    except SystemExit:
        pass
    captured = capsys.readouterr()
    assert file1_file2_json_diff in captured.out


def test_gendiff_main_call_help(capsys):
    try:
        main(["-h"])
    except SystemExit:
        pass
    captured = capsys.readouterr()
    print(captured.out)
    assert help_output in captured.out
