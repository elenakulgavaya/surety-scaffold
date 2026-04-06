from typing import Optional

from .base import PRIMITIVE_TYPES, ClassSpec, FieldSpec


def _collect_imports(spec: ClassSpec, imports: set) -> set:
    imports.add('Dictionary')

    for f in spec.fields:
        if f.is_array:
            imports.add('Array')
            if f.array_item_type in PRIMITIVE_TYPES:
                imports.add(f.array_item_type)

        elif f.surety_type in PRIMITIVE_TYPES:
            imports.add(f.surety_type)

    for dep in spec.dependencies:
        _collect_imports(dep, imports)

    return imports


def _render_kwargs_str(extra: Optional[dict] = None) -> str:
    extra = extra or {}
    parts = []

    for k, v in extra.items():
        if isinstance(v, bool):
            parts.append(f'{k}={v}')
        elif isinstance(v, str):
            parts.append(f"{k}='{v}'")
        else:
            parts.append(f'{k}={v}')

    return ', '.join(parts)


def _render_line(f: FieldSpec) -> str:
    name_part = f"name='{f.json_key}'"
    extra = _render_kwargs_str(f.extra_kwargs)
    kwargs = name_part + (f', {extra}' if extra else '')

    if f.is_array:
        return f'{f.attr_name} = Array({f.array_item_type}, {kwargs})'

    return f'{f.attr_name} = {f.surety_type}({kwargs})'


def _render_classes(spec: ClassSpec, seen: set, output: list) -> list:
    """Emit classes depth-first, so dependencies come before the classes that use them."""
    for dep in spec.dependencies:
        _render_classes(dep, seen, output)

    if spec.class_name in seen:
        return output

    seen.add(spec.class_name)

    lines = [f'class {spec.class_name}(Dictionary):']
    if not spec.fields:
        lines.append('    pass')
    else:
        for f in spec.fields:
            lines.append(f'    {_render_line(f)}')

    output.append('\n'.join(lines))

    return output



def render(root: ClassSpec) -> str:
    imports: set = set()
    _collect_imports(root, imports)

    import_line = f'from surety import {", ".join(sorted(imports))}'

    classes: list = []
    _render_classes(root, set(), classes)

    return '\n\n\n'.join([import_line] + classes)
