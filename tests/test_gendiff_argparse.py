"""tests for gendiff package."""
from gendiff.scripts.gendiff import main


help_output = '''usage: pytest [-h] first_file second_file

Generate diff

positional arguments:
  first_file
  second_file

optional arguments:
  -h, --help   show this help message and exit
'''
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
        main(["first_file"])
    except SystemExit:
        pass
    captured = capsys.readouterr()
    assert no_second_arg_error_substring in captured.err


def test_gendiff_main_with_both_args(capsys):
    try:
        main(["first_file", "second_file"])
    except SystemExit:
        pass
    captured = capsys.readouterr()
    assert "Namespace(first_file='first_file', second_file='second_file')" in captured.out


def test_gendiff_main_call_help(capsys):
    try:
        main(["-h"])
    except SystemExit:
        pass
    captured = capsys.readouterr()
    assert help_output == captured.out
