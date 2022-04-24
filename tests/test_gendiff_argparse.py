"""tests for gendiff package."""
from gendiff.scripts.gendiff import main


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
        main(["./tests/fixtures/file1.json"])
    except SystemExit:
        pass
    captured = capsys.readouterr()
    assert no_second_arg_error_substring in captured.err


def test_gendiff_main_with_all_args(capsys):
    try:
        main([
            *("-f", "json"),
            "./tests/fixtures/file1.json",
            "./tests/fixtures/file2.json",
        ])
    except SystemExit:
        pass
    captured = capsys.readouterr()
    assert """{
  - follow: False
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: True
}""" in captured.out


def test_gendiff_main_call_help(capsys):
    try:
        main(["-h"])
    except SystemExit:
        pass
    captured = capsys.readouterr()
    print(captured.out)
    assert help_output in captured.out
