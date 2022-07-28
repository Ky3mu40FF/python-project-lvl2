import pytest

@pytest.fixture
def help_output():
    return '''[-h] [-f FORMAT] first_file second_file

Generate diff

positional arguments:
  first_file
  second_file

optional arguments:
  -h, --help            show this help message and exit
  -f FORMAT, --format FORMAT
                        set format of output'''


@pytest.fixture
def no_args_error_substring():
    return "error: the following arguments are required: first_file, second_file"


@pytest.fixture
def no_second_arg_error_substring():
    return "error: the following arguments are required: second_file"

