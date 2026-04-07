import pytest

from surety.scaffold.extract.type_extractor import (
    is_datetime, is_uuid, get_primitive_type, singularize, to_pascal_case,
)

def test_is_datetime_none():
    assert is_datetime(None) is False


def test_is_datetime_bool():
    assert is_datetime(True) is False


def test_is_datetime_number():
    assert is_datetime(123) is False


def test_is_datetime_string():
    assert is_datetime('test') is False


def test_is_datetime_valid_str():
    assert is_datetime('2020-01-01T00:00:00') is True


def test_is_valid_uuid_none():
    assert is_uuid(None) is False


def test_is_valid_uuid_bool():
    assert is_uuid(True) is False


def test_is_valid_uuid_number():
    assert is_uuid(123) is False


def test_is_valid_uuid_string():
    assert is_uuid('test') is False


def test_is_valid_uuid_valid_too_short_str():
    assert is_uuid('123e4567-e89b-12d3-a456-42665544000') is False


def test_is_valid_uuid_valid_str():
    assert is_uuid('123e4567-e89b-12d3-a456-426655440000') is True


def test_get_primitive_type_none():
    assert get_primitive_type(None) == 'String'


@pytest.mark.parametrize('value', [True, False])
def test_get_primitive_type_bool(value):
    assert get_primitive_type(value) == 'Bool'


@pytest.mark.parametrize('value', [0, 1234, -12])
def test_get_primitive_type_int(value):
    assert get_primitive_type(value) == 'Int'


@pytest.mark.parametrize('value', [0.0, 1.234, -1.2, 0.12])
def test_get_primitive_type_float(value):
    assert get_primitive_type(value) == 'Float'


def test_get_primitive_type_string_uuid():
    assert get_primitive_type('123e4567-e89b-12d3-a456-426655440000') == 'Uuid'


def test_get_primitive_type_string_datetime():
    assert get_primitive_type('2020-01-01') == 'DateTime'


@pytest.mark.parametrize('value', ['', 'true', '1', 'test_string'])
def test_get_primitive_type_string(value):
    assert get_primitive_type(value) == 'String'


@pytest.mark.parametrize('value', [
    'test_string',
    'TestString',
    'testString',
    'test string',
    'test-string',
])
def test_to_pascal_case(value):
    assert to_pascal_case(value) == 'TestString'


@pytest.mark.parametrize('name, expected', [
    ('Items', 'Item'),
    ('ExtraItems', 'ExtraItem'),
    ('Tags', 'Tag'),
    ('Categories', 'Category'),
    ('Addresses', 'Address'),
    ('Statuses', 'Status'),
    ('Boxes', 'Box'),
    ('History', 'History'),
    ('Address', 'Address'),
    ('Status', 'Statu'),
])
def test_singularize(name, expected):
    assert singularize(name) == expected
