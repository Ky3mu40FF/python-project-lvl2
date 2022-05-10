"""tests for gendiff package."""
from gendiff.scripts.gendiff import main
from .conftest import JSON_FILES_RELATIVE_PATHS


file1_file2_diff = """{
  - follow: false
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}"""

file3_file4_diff = """{
    common: {
      + follow: false
        setting1: Value 1
      - setting2: 200
      - setting3: true
      + setting3: null
      + setting4: blah blah
      + setting5: {
            key5: value5
        }
        setting6: {
            doge: {
              - wow: 
              + wow: so much
            }
            key: value
          + ops: vops
        }
    }
    group1: {
      - baz: bas
      + baz: bars
        foo: bar
      - nest: {
            key: value
        }
      + nest: str
    }
  - group2: {
        abc: 12345
        deep: {
            id: 45
        }
    }
  + group3: {
        deep: {
            id: {
                number: 45
            }
        }
        fee: 100500
    }
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
            *("-f", "stylish"),
            JSON_FILES_RELATIVE_PATHS['flat_file1'],
            JSON_FILES_RELATIVE_PATHS['flat_file2'],
        ])
    except SystemExit:
        pass
    captured = capsys.readouterr()
    assert file1_file2_diff in captured.out


def test_gendiff_main_call_help(capsys):
    try:
        main(["-h"])
    except SystemExit:
        pass
    captured = capsys.readouterr()
    print(captured.out)
    assert help_output in captured.out
