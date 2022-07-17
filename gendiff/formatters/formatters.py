"""gendiff.formatters.formatters module."""

from types import MappingProxyType  # Immutable dict for constant (WPS407)

from .json import render as json_formatter
from .plain import render as plain_formatter
from .stylish import render as stylish_formatter

FORMATTERS = MappingProxyType({
    'json': json_formatter,
    'plain': plain_formatter,
    'stylish': stylish_formatter,
})
