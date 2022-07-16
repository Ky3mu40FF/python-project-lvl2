"""tests for gendiff.parser module."""

import pytest
from gendiff.parser import get_parsed_file
from .conftest import (
    TEST_FILES_RELATIVE_PATHS,
    FILE_RELATIVE_PATH_WRONG_EXTENSION,
    test_files_absolute_paths_fixture,
    FLAT_JSON_1,
    FLAT_YAML_1,
)


@pytest.fixture
def file1_fixture():
    return {
        "host": "hexlet.io",
        "timeout": 50,
        "proxy": "123.234.53.22",
        "follow": False
    }


def test_get_parsed_file_json(file1_fixture):
    parsed_file = get_parsed_file(TEST_FILES_RELATIVE_PATHS[FLAT_JSON_1])
    assert parsed_file == file1_fixture


def test_get_parsed_file_yaml(file1_fixture):
    parsed_file = get_parsed_file(TEST_FILES_RELATIVE_PATHS[FLAT_YAML_1])
    assert parsed_file == file1_fixture


def test_get_parsed_file_wrong_extension():
    with pytest.raises(ValueError):
        get_parsed_file(FILE_RELATIVE_PATH_WRONG_EXTENSION)


def test_get_parsed_file_json_absolute_path(
        file1_fixture, 
        test_files_absolute_paths_fixture,
    ):
    parsed_file = get_parsed_file(test_files_absolute_paths_fixture[FLAT_JSON_1])
    assert parsed_file == file1_fixture
