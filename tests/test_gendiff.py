"""tests for gendiff package."""
import pytest

from gendiff.generator import generate_diff

TEST_PAIRS = [
    (
        './tests/fixtures/json_fixtures/flat_before.json',
        './tests/fixtures/json_fixtures/flat_after.json',
        'stylish',
        './tests/fixtures/expected/stylish_formatter_flat_files.txt',
    ),
    (
        './tests/fixtures/yaml_fixtures/flat_before.yml',
        './tests/fixtures/yaml_fixtures/flat_after.yml',
        'stylish',
        './tests/fixtures/expected/stylish_formatter_flat_files.txt',
    ),
    (
        './tests/fixtures/json_fixtures/nested_before.json',
        './tests/fixtures/json_fixtures/nested_after.json',
        'stylish',
        './tests/fixtures/expected/stylish_formatter_nested_files.txt',
    ),
    (
        './tests/fixtures/yaml_fixtures/nested_before.yml',
        './tests/fixtures/yaml_fixtures/nested_after.yml',
        'stylish',
        './tests/fixtures/expected/stylish_formatter_nested_files.txt',
    ),
    (
        './tests/fixtures/json_fixtures/flat_before.json',
        './tests/fixtures/json_fixtures/flat_after.json',
        'plain',
        './tests/fixtures/expected/plain_formatter_flat_files.txt',
    ),
    (
        './tests/fixtures/yaml_fixtures/flat_before.yml',
        './tests/fixtures/yaml_fixtures/flat_after.yml',
        'plain',
        './tests/fixtures/expected/plain_formatter_flat_files.txt',
    ),
    (
        './tests/fixtures/json_fixtures/nested_before.json',
        './tests/fixtures/json_fixtures/nested_after.json',
        'plain',
        './tests/fixtures/expected/plain_formatter_nested_files.txt',
    ),
    (
        './tests/fixtures/yaml_fixtures/nested_before.yml',
        './tests/fixtures/yaml_fixtures/nested_after.yml',
        'plain',
        './tests/fixtures/expected/plain_formatter_nested_files.txt',
    ),
    (
        './tests/fixtures/json_fixtures/flat_before.json',
        './tests/fixtures/json_fixtures/flat_after.json',
        'json',
        './tests/fixtures/expected/json_formatter_flat_files.json',
    ),
    (
        './tests/fixtures/yaml_fixtures/flat_before.yml',
        './tests/fixtures/yaml_fixtures/flat_after.yml',
        'json',
        './tests/fixtures/expected/json_formatter_flat_files.json',
    ),
    (
        './tests/fixtures/json_fixtures/nested_before.json',
        './tests/fixtures/json_fixtures/nested_after.json',
        'json',
        './tests/fixtures/expected/json_formatter_nested_files.json',
    ),
    (
        './tests/fixtures/yaml_fixtures/nested_before.yml',
        './tests/fixtures/yaml_fixtures/nested_after.yml',
        'json',
        './tests/fixtures/expected/json_formatter_nested_files.json',
    ),
    (
        './tests/fixtures/json_fixtures/file1.json',
        './tests/fixtures/json_fixtures/file2.json',
        'stylish',
        './tests/fixtures/expected/hexlet_result_stylish',
    ),
    (
        './tests/fixtures/yaml_fixtures/file1.yml',
        './tests/fixtures/yaml_fixtures/file2.yml',
        'stylish',
        './tests/fixtures/expected/hexlet_result_stylish',
    ),
    (
        './tests/fixtures/json_fixtures/file1.json',
        './tests/fixtures/json_fixtures/file2.json',
        'plain',
        './tests/fixtures/expected/hexlet_result_plain',
    ),
    (
        './tests/fixtures/yaml_fixtures/file1.yml',
        './tests/fixtures/yaml_fixtures/file2.yml',
        'plain',
        './tests/fixtures/expected/hexlet_result_plain',
    ),
]


@pytest.mark.parametrize('file_before, file_after, formatter, expected', TEST_PAIRS)
def test_gendiff(
    file_before,
    file_after,
    formatter,
    expected,
):
    with open(expected, 'r') as file:
        expected_result = file.read().strip()
    
    runtime_result = generate_diff(
        file_before,
        file_after,
        formatter,
    )
    assert runtime_result == expected_result
