from dataclasses import dataclass, field
from typing import List, Optional

PRIMITIVE_TYPES = {'Bool', 'Int', 'Float', 'String', 'Uuid', 'DateTime'}


@dataclass
class FieldSpec:
    attr_name: str
    json_key: str
    surety_type: str
    extra_kwargs: Optional[dict] = None
    array_item_type: Optional[str] = None

    @property
    def is_array(self):
        return self.surety_type == 'Array'

@dataclass
class ClassSpec:
    class_name: str
    fields: List[FieldSpec] = field(default_factory=list)
    dependencies: List['ClassSpec'] = field(default_factory=list)

