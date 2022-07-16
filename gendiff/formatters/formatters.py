"""gendiff.formatters.formatters module."""

from types import MappingProxyType  # Immutable dict for constant (WPS407)

from .plain import render as plain_formatter
from .stylish import render as stylish_formatter

FORMATTERS = MappingProxyType({
    'stylish': stylish_formatter,
    'plain': plain_formatter,
})
