import json

from surety.scaffold import extract_from_json


def test_one_field_json():
    json_data = json.dumps({'name': 'Alice'})
    assert extract_from_json(json_data) == (
        "from surety import Dictionary, String\n\n\n"
        "class Schema(Dictionary):\n"
        "    Name = String(name='name')"
    )


def test_root_name():
    json_data = json.dumps({'name': 'Alice'})
    assert extract_from_json(json_data, class_name='User') == (
        "from surety import Dictionary, String\n\n\n"
        "class User(Dictionary):\n"
        "    Name = String(name='name')"
    )


def test_array():
    json_data = json.dumps({'tags': ['one', 'two']})
    assert extract_from_json(json_data) == (
        "from surety import Array, Dictionary, String\n\n\n"
        "class Schema(Dictionary):\n"
        "    Tags = Array(String, name='tags')"
    )


def test_nested_object():
    json_data = json.dumps({'customer': {'name': 'Joe', 'age': 30}})
    assert extract_from_json(json_data, class_name='Order') == (
        "from surety import Dictionary, Int, String\n\n\n"
        "class Customer(Dictionary):\n"
        "    Name = String(name='name')\n"
        "    Age = Int(name='age')\n\n\n"
        "class Order(Dictionary):\n"
        "    Customer = Customer(name='customer')"
    )


def test_array_of_objects_singular_class_name():
    json_data = json.dumps({'items': [{'sku': 'A', 'qty': 2}]})
    assert extract_from_json(json_data, class_name='Order') == (
        "from surety import Array, Dictionary, Int, String\n\n\n"
        "class Item(Dictionary):\n"
        "    Sku = String(name='sku')\n"
        "    Qty = Int(name='qty')\n\n\n"
        "class Order(Dictionary):\n"
        "    Items = Array(Item, name='items')"
    )


def test_array_of_objects_extra_items_singular_class_name():
    json_data = json.dumps({'extraItems': [{'sku': 'A'}]})
    assert extract_from_json(json_data, class_name='Order') == (
        "from surety import Array, Dictionary, String\n\n\n"
        "class ExtraItem(Dictionary):\n"
        "    Sku = String(name='sku')\n\n\n"
        "class Order(Dictionary):\n"
        "    ExtraItems = Array(ExtraItem, name='extraItems')"
    )


def test_reused_object():
    json_data = json.dumps({
        'customer': {'name': 'Joe', 'age': 30},
        'history': [{'customer': {'name': 'Alice', 'age': 20}}]
    })
    assert extract_from_json(json_data, class_name='Order') == (
        "from surety import Array, Dictionary, Int, String\n\n\n"
        "class Customer(Dictionary):\n"
        "    Name = String(name='name')\n"
        "    Age = Int(name='age')\n\n\n"
        "class Customer2(Dictionary):\n"
        "    Name = String(name='name')\n"
        "    Age = Int(name='age')\n\n\n"
        "class History(Dictionary):\n"
        "    Customer = Customer2(name='customer')\n\n\n"
        "class Order(Dictionary):\n"
        "    Customer = Customer(name='customer')\n"
        "    History = Array(History, name='history')"
    )
