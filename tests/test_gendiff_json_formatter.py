"""tests for gendiff package."""
import json
import pytest

from gendiff.generator import generate_diff
from .conftest import (
  TEST_FILES_RELATIVE_PATHS,
  FLAT_JSON_1,
  FLAT_JSON_2,
  NESTED_JSON_1,
  NESTED_JSON_2,
)

FLAT_FILES_JSON_FORMATTER_OUTPUT_PATH = './tests/fixtures/json_formatter_output_fixtures/flat_files_output.json'
NESTED_FILES_JSON_FORMATTER_OUTPUT_PATH = './tests/fixtures/json_formatter_output_fixtures/nested_files_output.json'


@pytest.fixture
def flat_files_json_formatter_fixture():
    with open(FLAT_FILES_JSON_FORMATTER_OUTPUT_PATH, 'r') as input_file:
        parsed_file = json.dumps(json.load(input_file))
    return parsed_file


@pytest.fixture
def nested_files_json_formatter_fixture():
    with open(NESTED_FILES_JSON_FORMATTER_OUTPUT_PATH, 'r') as input_file:
        parsed_file = json.dumps(json.load(input_file))
    return parsed_file


def test_gendiff_flat_json_json_formatter(flat_files_json_formatter_fixture):
    flat_json_diff_result = generate_diff(
        TEST_FILES_RELATIVE_PATHS[FLAT_JSON_1],
        TEST_FILES_RELATIVE_PATHS[FLAT_JSON_2],
        'json',
    )
    assert flat_files_json_formatter_fixture == flat_json_diff_result


def test_gendiff_nested_json_json_formatter(nested_files_json_formatter_fixture):
    nested_json_diff_result = generate_diff(
        TEST_FILES_RELATIVE_PATHS[NESTED_JSON_1],
        TEST_FILES_RELATIVE_PATHS[NESTED_JSON_2],
        'json',
    )
    assert nested_files_json_formatter_fixture == nested_json_diff_result
