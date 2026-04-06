import json

from .base import ClassSpec, FieldSpec
from .type_extractor import get_primitive_type, to_pascal_case
from .renderer import render


def _build_class_spec(data: dict, class_name: str, seen_names: dict) -> ClassSpec:
    """Recursively build a ClassSpec tree from a parsed JSON dict."""
    # Deduplicate class names that arise from different keys with the same PascalCase
    count = seen_names.get(class_name, 0) + 1
    seen_names[class_name] = count

    if count > 1:
        class_name = f'{class_name}{count}'

    fields = []
    dependencies = []

    for key, value in data.items():
        attr_name = to_pascal_case(key)

        if value is None:
            fields.append(FieldSpec(
                attr_name=attr_name,
                json_key=key,
                surety_type='String',
                extra_kwargs={'allow_none': True, 'required': True},
            ))

        elif isinstance(value, bool):
            fields.append(FieldSpec(
                attr_name=attr_name,
                json_key=key,
                surety_type='Bool',
                extra_kwargs={'required': True},
            ))

        elif isinstance(value, dict):
            nested = _build_class_spec(value, to_pascal_case(key), seen_names)
            dependencies.append(nested)
            fields.append(FieldSpec(
                attr_name=attr_name,
                json_key=key,
                surety_type=nested.class_name,
                extra_kwargs={'required': True},
            ))

        elif isinstance(value, list):
            filtered = [v for v in value if v is not None]

            if not filtered or not isinstance(filtered[0], dict):
                item_type = get_primitive_type(filtered[0]) if filtered else 'String'
                fields.append(FieldSpec(
                    attr_name=attr_name,
                    json_key=key,
                    surety_type='Array',
                    extra_kwargs={'required': True},
                    array_item_type=item_type,
                ))
            else:
                # Merge all items to capture all possible keys across the array
                merged: dict = {}

                for item in filtered:
                    if isinstance(item, dict):
                        merged.update(item)

                nested = _build_class_spec(merged, to_pascal_case(key), seen_names)
                dependencies.append(nested)
                fields.append(FieldSpec(
                    attr_name=attr_name,
                    json_key=key,
                    surety_type='Array',
                    extra_kwargs={'required': True},
                    array_item_type=nested.class_name,
                ))

        else:
            fields.append(FieldSpec(
                attr_name=attr_name,
                json_key=key,
                surety_type=get_primitive_type(value),
                extra_kwargs={'required': True},
            ))

    return ClassSpec(
        class_name=class_name,
        fields=fields,
        dependencies=dependencies
    )



def extract_from_json(json_data: str, class_name: str = 'Schema') -> str:
    """
    Generate surety Dictionary class definitions from a JSON payload.

    Recursively walks the dict, infers surety field types, and emits
    ready-to-use Python source code.

    :param json_data: JSON containing an object.
    :param class_name: Name for the top-level generated class.
    :return: Python source code as a string.
    """
    data = json.loads(json_data)

    root = _build_class_spec(data, class_name, seen_names={})
    return render(root)

