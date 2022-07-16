"""general fixtures."""

import os

import pytest

FLAT_JSON_1 = 'fj1'
FLAT_JSON_2 = 'fj2'
NESTED_JSON_1 = 'nj1'
NESTED_JSON_2 = 'nj2'
FLAT_YAML_1 = 'fy1'
FLAT_YAML_2 = 'fy2'
NESTED_YAML_1 = 'ny1'
NESTED_YAML_2 = 'ny2'

TEST_FILES_RELATIVE_PATHS = {
    FLAT_JSON_1: './tests/fixtures/json_fixtures/file1.json',
    FLAT_JSON_2: './tests/fixtures/json_fixtures/file2.json',
    NESTED_JSON_1: './tests/fixtures/json_fixtures/file3.json',
    NESTED_JSON_2: './tests/fixtures/json_fixtures/file4.json',
    FLAT_YAML_1: './tests/fixtures/yaml_fixtures/file1.yml',
    FLAT_YAML_2: './tests/fixtures/yaml_fixtures/file2.yml',
    NESTED_YAML_1: './tests/fixtures/yaml_fixtures/file3.yml',
    NESTED_YAML_2: './tests/fixtures/yaml_fixtures/file4.yml',
}

FILE_RELATIVE_PATH_WRONG_EXTENSION = './tests/fixtures/yaml_fixtures/file1.ymi'


@pytest.fixture
def test_files_absolute_paths_fixture():
    return {
        FLAT_JSON_1: os.path.abspath(TEST_FILES_RELATIVE_PATHS[FLAT_JSON_1]),
        FLAT_JSON_2: os.path.abspath(TEST_FILES_RELATIVE_PATHS[FLAT_JSON_2]),
        NESTED_JSON_1: os.path.abspath(TEST_FILES_RELATIVE_PATHS[NESTED_JSON_1]),
        NESTED_JSON_2: os.path.abspath(TEST_FILES_RELATIVE_PATHS[NESTED_JSON_2]),
        FLAT_YAML_1: os.path.abspath(TEST_FILES_RELATIVE_PATHS[FLAT_YAML_1]),
        FLAT_YAML_2: os.path.abspath(TEST_FILES_RELATIVE_PATHS[FLAT_YAML_2]),
        NESTED_YAML_1: os.path.abspath(TEST_FILES_RELATIVE_PATHS[NESTED_YAML_1]),
        NESTED_YAML_2: os.path.abspath(TEST_FILES_RELATIVE_PATHS[NESTED_YAML_2]),
    }
