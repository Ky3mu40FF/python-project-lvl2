"""tests for generate diff module."""

import pytest
from gendiff.generator import format_diff_output, get_parsed_file, get_changes, generate_diff


FILE1_RELATIVE_PATH = './tests/fixtures/file1.json'
FILE2_RELATIVE_PATH = './tests/fixtures/file2.json'

@pytest.fixture
def file1_fixture():
    return {
        "host": "hexlet.io",
        "timeout": 50,
        "proxy": "123.234.53.22",
        "follow": False
    }


def test_get_parsed_file(file1_fixture):
    parsed_file = get_parsed_file(FILE1_RELATIVE_PATH)
    assert parsed_file == file1_fixture
