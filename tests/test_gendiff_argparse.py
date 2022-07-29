"""tests for gendiff package."""
from unittest import mock
from gendiff.scripts.gendiff import main
import pytest


@pytest.fixture
def argparse_help_output_fixture():
    with open('./tests/fixtures/expected/argparse_help_output.txt', 'r') as file:
        cli_output = file.read()
    return cli_output


@pytest.fixture
def argparse_no_args_output_fixture():
    with open('./tests/fixtures/expected/argparse_no_args_output.txt', 'r') as file:
        cli_output = file.read()
    return cli_output


@pytest.fixture
def argparse_no_second_file_output_fixture():
    with open('./tests/fixtures/expected/argparse_no_second_file_output.txt', 'r') as file:
        cli_output = file.read()
    return cli_output


def test_gendiff_main_call_help(capsys, argparse_help_output_fixture):

    try:
        with mock.patch('sys.argv', ['gendiff', '--help']):
            main()
    except SystemExit:
        pass
    captured = capsys.readouterr()
    assert argparse_help_output_fixture in captured.out


def test_gendiff_main_without_args(capsys, argparse_no_args_output_fixture):
    try:
        with mock.patch('sys.argv', ['gendiff']):
            main()
    except SystemExit:
        pass
    captured = capsys.readouterr()
    assert argparse_no_args_output_fixture in captured.err


def test_gendiff_main_with_one_arg(capsys, argparse_no_second_file_output_fixture):
    try:
        with mock.patch('sys.argv', ['gendiff', './tests/fixtures/json_fixtures/flat_before.json']):
            main()
    except SystemExit:
        pass
    captured = capsys.readouterr()
    assert argparse_no_second_file_output_fixture in captured.err
