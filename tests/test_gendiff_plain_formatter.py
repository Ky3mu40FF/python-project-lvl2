"""tests for gendiff package."""
from gendiff.generator import generate_diff
from .conftest import (
  TEST_FILES_RELATIVE_PATHS,
  FLAT_JSON_1,
  FLAT_JSON_2,
  NESTED_JSON_1,
  NESTED_JSON_2,
  NESTED_YAML_1,
  NESTED_YAML_2
)


FLAT_FILES_PLAIN_DIFF = """Property 'follow' was removed
Property 'proxy' was removed
Property 'timeout' was updated. From 50 to 20
Property 'verbose' was added with value: true"""

NESTED_FILES_PLAIN_DIFF = """Property 'common.follow' was added with value: false
Property 'common.setting2' was removed
Property 'common.setting3' was updated. From true to null
Property 'common.setting4' was added with value: 'blah blah'
Property 'common.setting5' was added with value: [complex value]
Property 'common.setting6.doge.wow' was updated. From '' to 'so much'
Property 'common.setting6.ops' was added with value: 'vops'
Property 'group1.baz' was updated. From 'bas' to 'bars'
Property 'group1.nest' was updated. From [complex value] to 'str'
Property 'group2' was removed
Property 'group3' was added with value: [complex value]"""


def test_gendiff_nested_json_plain_formatter():
    nested_json_plain_diff_result = generate_diff(
        TEST_FILES_RELATIVE_PATHS[NESTED_JSON_1],
        TEST_FILES_RELATIVE_PATHS[NESTED_JSON_2],
        'plain',
    )
    assert nested_json_plain_diff_result == NESTED_FILES_PLAIN_DIFF


def test_gendiff_flat_json_stylish_formatter():
    flat_json_plain_diff_result = generate_diff(
        TEST_FILES_RELATIVE_PATHS[FLAT_JSON_1],
        TEST_FILES_RELATIVE_PATHS[FLAT_JSON_2],
        'plain',
    )
    assert flat_json_plain_diff_result == FLAT_FILES_PLAIN_DIFF


def test_gendiff_nested_yaml_stylish_formatter():
    nested_yaml_plain_diff_result = generate_diff(
        TEST_FILES_RELATIVE_PATHS[NESTED_YAML_1],
        TEST_FILES_RELATIVE_PATHS[NESTED_YAML_2],
        'plain',
    )
    assert nested_yaml_plain_diff_result == NESTED_FILES_PLAIN_DIFF

