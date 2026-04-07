from surety.scaffold.extract.json_extractor import _build_class_spec
from .render_data import (
    EMPTY_DICT, EMPTY_SPEC,
    SPEC_WITH_NONE, SPEC_WITH_NONE_DICT,
    SPEC_WITH_TWO_TYPES, SPEC_WITH_TWO_TYPES_DICT,
    SPEC_WITH_ARRAY, SPEC_WITH_ARRAY_DICT,
    SPEC_WITH_NESTED, SPEC_WITH_NESTED_DICT,
    SPEC_WITH_ARRAY_OF_NESTED, SPEC_WITH_ARRAY_OF_NESTED_DICT,
)


def test_build_class_spec_empty():
    assert _build_class_spec(
        EMPTY_DICT, 'Root', {}
    ) == EMPTY_SPEC


def test_build_class_spec_none_value():
    assert _build_class_spec(
        SPEC_WITH_NONE_DICT, 'Root', {}
    ) == SPEC_WITH_NONE


def test_build_class_spec_two_primitives():
    assert _build_class_spec(
        SPEC_WITH_TWO_TYPES_DICT, 'Root', {}
    ) == SPEC_WITH_TWO_TYPES


def test_build_class_spec_array():
    assert _build_class_spec(
        SPEC_WITH_ARRAY_DICT, 'Root', {}
    ) == SPEC_WITH_ARRAY


def test_build_class_spec_with_nested():
    assert _build_class_spec(
        SPEC_WITH_NESTED_DICT, 'Root', {}
    ) == SPEC_WITH_NESTED


def test_build_class_spec_with_array_nested():
    assert _build_class_spec(
        SPEC_WITH_ARRAY_OF_NESTED_DICT, 'Root', {}
    ) == SPEC_WITH_ARRAY_OF_NESTED
