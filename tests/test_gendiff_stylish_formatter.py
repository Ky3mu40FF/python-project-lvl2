"""tests for gendiff package."""
from gendiff.generator import generate_diff
from .conftest import (
  TEST_FILES_RELATIVE_PATHS,
  FLAT_JSON_1,
  FLAT_JSON_2,
  NESTED_JSON_1,
  NESTED_JSON_2,
  NESTED_YAML_1,
  NESTED_YAML_2,
)


FLAT_FILES_STYLISH_DIFF = """{
  - follow: false
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}"""

NESTED_FILES_STYLISH_DIFF = """{
    common: {
      + follow: false
        setting1: Value 1
      - setting2: 200
      - setting3: true
      + setting3: null
      + setting4: blah blah
      + setting5: {
            key5: value5
        }
        setting6: {
            doge: {
              - wow: 
              + wow: so much
            }
            key: value
          + ops: vops
        }
    }
    group1: {
      - baz: bas
      + baz: bars
        foo: bar
      - nest: {
            key: value
        }
      + nest: str
    }
  - group2: {
        abc: 12345
        deep: {
            id: 45
        }
    }
  + group3: {
        deep: {
            id: {
                number: 45
            }
        }
        fee: 100500
    }
}"""


def test_gendiff_flat_json_stylish_formatter():
    flat_json_stylish_diff_result = generate_diff(
        TEST_FILES_RELATIVE_PATHS[FLAT_JSON_1],
        TEST_FILES_RELATIVE_PATHS[FLAT_JSON_2],
        'stylish',
    )
    assert flat_json_stylish_diff_result == FLAT_FILES_STYLISH_DIFF


def test_gendiff_nested_json_stylish_formatter():
    nested_json_stylish_diff_result = generate_diff(
        TEST_FILES_RELATIVE_PATHS[NESTED_JSON_1],
        TEST_FILES_RELATIVE_PATHS[NESTED_JSON_2],
        'stylish',
    )
    assert nested_json_stylish_diff_result == NESTED_FILES_STYLISH_DIFF


def test_gendiff_nested_yaml_stylish_formatter():
    nested_yaml_stylish_diff_result = generate_diff(
        TEST_FILES_RELATIVE_PATHS[NESTED_YAML_1],
        TEST_FILES_RELATIVE_PATHS[NESTED_YAML_2],
        'stylish',
    )
    assert nested_yaml_stylish_diff_result == NESTED_FILES_STYLISH_DIFF
