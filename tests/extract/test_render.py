from surety.scaffold.extract.renderer import (
    _collect_imports, _render_classes, _render_kwargs_str, _render_line, render
)
from .render_data import *

def test_collect_imports_empty():
    imports = _collect_imports(EMPTY_SPEC, set())
    assert imports == EMPTY_SPEC_IMPORTS


def test_collect_imports_flat_primitives():
    imports = _collect_imports(PRIMITIVES_SPEC, set())
    assert imports == PRIMITIVES_SPEC_IMPORTS


def test_collect_imports_with_array():
    imports = _collect_imports(SPEC_WITH_ARRAY, set())
    assert imports == SPEC_WITH_ARRAY_IMPORTS


def test_collect_imports_with_nested_class():
    imports = _collect_imports(SPEC_WITH_NESTED, set())
    assert imports == SPEC_WITH_NESTED_IMPORTS


def test_collect_imports_with_array_of_nested():
    imports = _collect_imports(SPEC_WITH_ARAY_OF_NESTED, set())
    assert imports == SPEC_WITH_ARAY_OF_NESTED_IMPORTS


def test_render_kwargs_none():
    assert _render_kwargs_str(None) == ''


def test_render_kwargs_boolean():
    kwargs = {'is_required': True}

    assert _render_kwargs_str(kwargs) == 'is_required=True'


def test_render_kwargs_string():
    kwargs = {'name': 'json_field_name'}

    assert _render_kwargs_str(kwargs) == "name='json_field_name'"


def test_render_kwargs_other():
    kwargs = {'min_len': 10}

    assert _render_kwargs_str(kwargs) == 'min_len=10'


def test_render_kwargs_mixed():
    kwargs = {
        'name': 'test_name',
        'required': True,
        'default': None,
        'max_len': 2
    }

    assert _render_kwargs_str(kwargs) == (
        "name='test_name', required=True, default=None, max_len=2"
    )


def test_render_line_primitive():
    assert _render_line(STRING_FIELD_SPEC) == STRING_FIELD_SPEC_LINE


def test_render_line_primitive_with_args():
    assert _render_line(STRING_FIELD_SPEC_WITH_ARGS) == (
        STRING_FIELD_SPEC_WITH_ARGS_LINE
    )


def test_render_line_custom_type():
    assert _render_line(CUSTOM_FIELD_SPEC) == CUSTOM_FIELD_SPEC_LINE


def test_render_line_array():
    assert _render_line(ARRAY_FIELD_SPEC) == ARRAY_FIELD_SPEC_LINE


def test_render_classes_empty():
    assert _render_classes(EMPTY_SPEC, set(), []) == EMPTY_SPEC_CLASSES


def test_render_class_with_fields():
    assert _render_classes(SPEC_WITH_TWO_TYPES, set(), []) == (
        SPEC_WITH_TWO_TYPES_CLASSES
    )


def test_render_class_with_dependencies():
    assert _render_classes(SPEC_WITH_NESTED, set(), []) == (
        SPEC_WITH_NESTED_CLASSES
    )

def test_render_class_with_duplicated_dependencies():
    assert _render_classes(SPEC_WITH_DUPLICATED_NESTED, set(), []) == (
        SPEC_WITH_DUPLICATED_NESTED_CLASSES
    )


def test_render_empty():
    assert render(EMPTY_SPEC) == EMPTY_SPEC_FULL


def test_render_primitives():
    assert render(SPEC_WITH_TWO_TYPES) == SPEC_WITH_TWO_TYPES_FULL


def test_render_with_nested():
    assert render(SPEC_WITH_NESTED) == SPEC_WITH_NESTED_FULL
