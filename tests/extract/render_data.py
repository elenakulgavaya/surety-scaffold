from surety.scaffold.extract.base import PRIMITIVE_TYPES, ClassSpec, FieldSpec


EMPTY_DICT = {}
EMPTY_SPEC = ClassSpec(
    class_name='Root',
    fields=[],
    dependencies=[]
)
EMPTY_SPEC_IMPORTS = {'Dictionary'}
EMPTY_SPEC_CLASSES = ['class Root(Dictionary):\n    pass']
EMPTY_SPEC_FULL = (
    'from surety import Dictionary\n\n\n'
    f'{EMPTY_SPEC_CLASSES[0]}'
)

STRING_FIELD_SPEC = FieldSpec(
    attr_name='StringName',
    json_key='string_name',
    surety_type='String',
    extra_kwargs={'required': True}
)
STRING_FIELD_SPEC_LINE = "StringName = String(name='string_name', required=True)"

FlOAT_FIELD_SPEC = FieldSpec(
    attr_name='FloatName',
    json_key='float_name',
    surety_type='Float',
    extra_kwargs={'required': True}
)
FLOAT_FIELD_SPEC_LINE = "FloatName = Float(name='float_name', required=True)"


STRING_FIELD_SPEC_WITH_ARGS = FieldSpec(
    attr_name='StringName',
    json_key='string_name',
    surety_type='String',
    extra_kwargs={'required': False, 'max_len': 100}
)
STRING_FIELD_SPEC_WITH_ARGS_LINE = (
    "StringName = String(name='string_name', required=False, max_len=100)"
)


CUSTOM_FIELD_SPEC =  FieldSpec(
    attr_name='CustomName',
    json_key='custom_name',
    surety_type='MyObject',
)
CUSTOM_FIELD_SPEC_LINE = "CustomName = MyObject(name='custom_name')"

ARRAY_FIELD_SPEC = FieldSpec(
    attr_name='ArrayName',
    json_key='array_name',
    surety_type='Array',
    array_item_type='Int',
    extra_kwargs={'required': True}
)
ARRAY_FIELD_SPEC_LINE = "ArrayName = Array(Int, name='array_name', required=True)"


PRIMITIVES_SPEC = ClassSpec(
    class_name='Root',
    fields=[
        FieldSpec(
            attr_name=f'{primitive_type}Name',
            json_key=f'{primitive_type.lower()}_name',
            surety_type=primitive_type,
        ) for primitive_type in PRIMITIVE_TYPES
    ],
    dependencies=[]
)
PRIMITIVES_SPEC_IMPORTS = {'Dictionary'} | PRIMITIVE_TYPES

SPEC_WITH_NONE_DICT = {'none_name': None}
SPEC_WITH_NONE = ClassSpec(
        class_name='Root',
        fields=[FieldSpec(
            attr_name='NoneName',
            json_key='none_name',
            surety_type='String',
            extra_kwargs={'allow_none': True, 'required': True}
        )],
        dependencies=[]
    )

SPEC_WITH_TWO_TYPES_DICT = {'string_name': 'test', 'float_name': 1.23}
SPEC_WITH_TWO_TYPES = ClassSpec(
        class_name='Root',
        fields=[STRING_FIELD_SPEC, FlOAT_FIELD_SPEC],
        dependencies=[]
    )
SPEC_WITH_TWO_TYPES_IMPORTS = {'Dictionary', 'Float', 'String'}
SPEC_WITH_TWO_TYPES_CLASSES = [
    f"class Root(Dictionary):\n"
    f"    {STRING_FIELD_SPEC_LINE}\n"
    f"    {FLOAT_FIELD_SPEC_LINE}"

]
SPEC_WITH_TWO_TYPES_FULL = (
    'from surety import Dictionary, Float, String\n\n\n'
    f'{SPEC_WITH_TWO_TYPES_CLASSES[0]}'
)

SPEC_WITH_ARRAY_DICT = {'string_name': 'test', 'array_name': [1, 2]}
SPEC_WITH_ARRAY = ClassSpec(
    class_name='Root',
    fields=[
        STRING_FIELD_SPEC,
        ARRAY_FIELD_SPEC
    ],
    dependencies=[]
)
SPEC_WITH_ARRAY_IMPORTS = {'Array', 'Dictionary', 'Int', 'String'}


SPEC_WITH_NESTED_DICT = {'nested_name': {'string_name': 'test'}}
SPEC_WITH_NESTED = ClassSpec(
    class_name='Root',
    fields=[
        FieldSpec(
            attr_name='NestedName',
            json_key='nested_name',
            surety_type='NestedName',
            extra_kwargs={'required': True}
        )
    ],
    dependencies=[
        ClassSpec(
            class_name='NestedName',
            fields=[STRING_FIELD_SPEC]
        )
    ]
)
SPEC_WITH_NESTED_IMPORTS = {'Dictionary', 'String'}
SPEC_WITH_NESTED_CLASSES = [
    "class NestedName(Dictionary):\n"
    f"    {STRING_FIELD_SPEC_LINE}",
    "class Root(Dictionary):\n"
    "    NestedName = NestedName(name='nested_name', required=True)"
]
SPEC_WITH_NESTED_FULL = (
    'from surety import Dictionary, String\n\n\n'
    f'{SPEC_WITH_NESTED_CLASSES[0]}\n\n\n'
    f'{SPEC_WITH_NESTED_CLASSES[1]}'
)


SPEC_WITH_DUPLICATED_NESTED = ClassSpec(
    class_name='Root',
    fields=[
        FieldSpec(
            attr_name='FirstNestedName',
            json_key='first_nested_name',
            surety_type='Nested',
        ),
        FieldSpec(
            attr_name='SecondNestedName',
            json_key='second_nested_name',
            surety_type='Nested',
        )
    ],
    dependencies=[
        ClassSpec(
            class_name='Nested',
            fields=[STRING_FIELD_SPEC]
        ),
        ClassSpec(
            class_name='Nested',
            fields=[STRING_FIELD_SPEC]
        )
    ]
)
SPEC_WITH_DUPLICATED_NESTED_CLASSES = [
    "class Nested(Dictionary):\n"
    f"    {STRING_FIELD_SPEC_LINE}",
    "class Root(Dictionary):\n"
    "    FirstNestedName = Nested(name='first_nested_name')\n"
    "    SecondNestedName = Nested(name='second_nested_name')"
]

SPEC_WITH_ARRAY_OF_NESTED_DICT = {'array_name': [{'bool_name': True}]}
SPEC_WITH_ARRAY_OF_NESTED = ClassSpec(
    class_name='Root',
    fields=[
        FieldSpec(
            attr_name='ArrayName',
            json_key='array_name',
            surety_type='Array',
            array_item_type='ArrayName',
            extra_kwargs={'required': True},
        )
    ],
    dependencies=[
        ClassSpec(
            class_name='ArrayName',
            fields=[
                FieldSpec(
                    attr_name='BoolName',
                    json_key='bool_name',
                    surety_type='Bool',
                    extra_kwargs={'required': True},
                ),
            ]
        )
    ]
)
SPEC_WITH_ARAY_OF_NESTED_IMPORTS = {'Array', 'Bool', 'Dictionary'}
