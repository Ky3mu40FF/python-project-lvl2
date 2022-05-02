"""general fixtures."""

import os

import pytest

JSON_FILES_RELATIVE_PATHS = {
    'flat_file1': './tests/fixtures/json_fixtures/file1.json',
    'flat_file2': './tests/fixtures/json_fixtures/file2.json',
}

YAML_FILES_RELATIVE_PATHS = {
    'flat_file1': './tests/fixtures/yaml_fixtures/file1.yml',
    'flat_file2': './tests/fixtures/yaml_fixtures/file2.yml',
}

FILE_RELATIVE_PATH_WRONG_EXTENSION = './tests/fixtures/yaml_fixtures/file1.ymi'


@pytest.fixture
def json_files_absolute_paths_fixture():
    return {
        'flat_file1': os.path.abspath(JSON_FILES_RELATIVE_PATHS['flat_file1']),
        'flat_file2': os.path.abspath(JSON_FILES_RELATIVE_PATHS['flat_file2']),
    }

@pytest.fixture
def yaml_files_absolute_paths_fixture():
    return {
        'flat_file1': os.path.abspath(YAML_FILES_RELATIVE_PATHS['flat_file1']),
        'flat_file2': os.path.abspath(YAML_FILES_RELATIVE_PATHS['flat_file2']),
    }
