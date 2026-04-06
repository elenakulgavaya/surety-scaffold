import re
import uuid as _uuid_mod
from datetime import datetime

DATETIME_PATTERNS = [
    '%Y-%m-%dT%H:%M:%S.%fZ',
    '%Y-%m-%dT%H:%M:%S.%f',
    '%Y-%m-%dT%H:%M:%SZ',
    '%Y-%m-%dT%H:%M:%S',
    '%Y-%m-%d',
]


def to_pascal_case(key: str) -> str:
    """Convert snake_case, kebab-case, or camelCase key to PascalCase."""
    parts = re.split(r'[_\-\s]+', key)
    result = []
    for part in parts:
        if part:
            sub_parts = re.sub(r'([A-Z])', r'_\1', part).split('_')
            result.extend(s.capitalize() for s in sub_parts if s)

    return ''.join(result) or 'Field'


def is_uuid(value: str) -> bool:
    try:
        _uuid_mod.UUID(value)
        return True
    except (ValueError, AttributeError, TypeError):
        return False


def is_datetime(value: str) -> bool:
    for pattern in DATETIME_PATTERNS:
        try:
            datetime.strptime(value, pattern)
            return True
        except (ValueError, TypeError):
            continue
    return False


def get_primitive_type(value) -> str:
    """Return the surety type name for a primitive Python value."""
    if isinstance(value, bool):
        return 'Bool'
    if isinstance(value, int):
        return 'Int'
    if isinstance(value, float):
        return 'Float'
    if isinstance(value, str):
        if is_uuid(value):
            return 'Uuid'
        if is_datetime(value):
            return 'DateTime'
        return 'String'

    return 'String'
