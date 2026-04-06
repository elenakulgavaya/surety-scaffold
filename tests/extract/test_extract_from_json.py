import json

from surety.scaffold import extract_from_json


def test_one_field_json():
    json_data = json.dumps({'name': 'Alice'})
    assert extract_from_json(json_data) == (
        "from surety import Dictionary, String\n\n\n"
        "class Schema(Dictionary):\n"
        "    Name = String(name='name', required=True)"
    )


def test_root_name():
    json_data = json.dumps({'name': 'Alice'})
    assert extract_from_json(json_data, class_name='User') == (
        "from surety import Dictionary, String\n\n\n"
        "class User(Dictionary):\n"
        "    Name = String(name='name', required=True)"
    )


def test_array():
    json_data = json.dumps({'tags': ['one', 'two']})
    assert extract_from_json(json_data) == (
        "from surety import Array, Dictionary, String\n\n\n"
        "class Schema(Dictionary):\n"
        "    Tags = Array(String, name='tags', required=True)"
    )

def test_nested_object():
    json_data = json.dumps({'customer': {'name': 'Joe', 'age': 30}})
    assert extract_from_json(json_data, class_name='Order') == (
        "from surety import Dictionary, Int, String\n\n\n"
        "class Customer(Dictionary):\n"
        "    Name = String(name='name', required=True)\n"
        "    Age = Int(name='age', required=True)\n\n\n"
        "class Order(Dictionary):\n"
        "    Customer = Customer(name='customer', required=True)"
    )

def test_reused_object():
    json_data = json.dumps({
        'customer': {'name': 'Joe', 'age': 30},
        'history': [{'customer': {'name': 'Alice', 'age': 20}}]
    })
    assert extract_from_json(json_data, class_name='Order') == (
        "from surety import Array, Dictionary, Int, String\n\n\n"
        "class Customer(Dictionary):\n"
        "    Name = String(name='name', required=True)\n"
        "    Age = Int(name='age', required=True)\n\n\n"
        "class Customer2(Dictionary):\n"
        "    Name = String(name='name', required=True)\n"
        "    Age = Int(name='age', required=True)\n\n\n"
        "class History(Dictionary):\n"
        "    Customer = Customer2(name='customer', required=True)\n\n\n"
        "class Order(Dictionary):\n"
        "    Customer = Customer(name='customer', required=True)\n"
        "    History = Array(History, name='history', required=True)"
    )

#
#
# class TestNestedObjects:
# def test_nested_dict_generates_class(self):
#     code = extract_contract(
#         {'customer': {'name': 'Joe', 'age': 30}}, class_name='Order'
#     )
#     assert 'class Customer(Dictionary):' in code
#     assert 'class Order(Dictionary):' in code
#
# def test_nested_class_appears_before_parent(self):
#     code = extract_contract(
#         {'customer': {'name': 'Joe'}}, class_name='Order'
#     )
#     customer_pos = code.index('class Customer')
#     order_pos = code.index('class Order')
#     assert customer_pos < order_pos
#
# def test_nested_field_references_class(self):
#     code = extract_contract(
#         {'customer': {'name': 'Joe'}}, class_name='Order'
#     )
#     assert "Customer = Customer(name='customer')" in code
#
# def test_deeply_nested(self):
#     code = extract_contract(
#         {'a': {'b': {'c': 'value'}}}, class_name='Root'
#     )
#     assert 'class B(Dictionary):' in code
#     assert 'class A(Dictionary):' in code
#     assert 'class Root(Dictionary):' in code
#     assert code.index('class B') < code.index('class A') < code.index('class Root')
#
#
# class TestArrays:
# def test_array_of_strings(self):
#     code = extract_contract({'tags': ['a', 'b']}, class_name='Root')
#     assert "Tags = Array(String, name='tags')" in code
#
# def test_array_of_ints(self):
#     code = extract_contract({'ids': [1, 2, 3]}, class_name='Root')
#     assert "Ids = Array(Int, name='ids')" in code
#
# def test_empty_array_defaults_to_string(self):
#     code = extract_contract({'items': []}, class_name='Root')
#     assert "Items = Array(String, name='items')" in code
#
# def test_array_of_objects_generates_class(self):
#     code = extract_contract(
#         {'items': [{'sku': 'A', 'qty': 1}]}, class_name='Order'
#     )
#     assert 'class Items(Dictionary):' in code
#     assert "Items = Array(Items, name='items')" in code
#
# def test_array_of_objects_merges_all_items(self):
#     # Different items may have different keys — all should appear
#     code = extract_contract(
#         {'items': [{'sku': 'A'}, {'sku': 'B', 'qty': 2}]}, class_name='Order'
#     )
#     assert 'Sku = String' in code
#     assert 'Qty = Int' in code
#
# def test_array_of_objects_class_before_parent(self):
#     code = extract_contract(
#         {'lines': [{'amount': 1.5}]}, class_name='Invoice'
#     )
#     assert code.index('class Lines') < code.index('class Invoice')
#
#
# class TestDuplicateClassNames:
# def test_same_key_at_different_levels(self):
#     # Both 'address' keys produce PascalCase 'Address' — second gets a suffix
#     code = extract_contract(
#         {
#             'billing': {'address': {'street': 'A'}},
#             'shipping': {'address': {'street': 'B'}},
#         },
#         class_name='Order',
#     )
#     # First 'Address' class is emitted normally; second gets a unique name
#     assert code.count('class Address') >= 1
#
#
# class TestFullExample:
# def test_order_payload(self):
#     payload = {
#         'order_id': 42,
#         'status': 'pending',
#         'total': 199.99,
#         'is_express': False,
#         'customer': {
#             'customer_id': 7,
#             'email': 'jane@example.com',
#         },
#         'items': [
#             {'sku': 'ABC-1', 'qty': 2},
#         ],
#     }
#     code = extract_contract(payload, class_name='Order')
#
#     assert 'class Customer(Dictionary):' in code
#     assert 'class Items(Dictionary):' in code
#     assert 'class Order(Dictionary):' in code
#     assert 'OrderId = Int' in code
#     assert 'Status = String' in code
#     assert 'Total = Float' in code
#     assert 'IsExpress = Bool' in code
#     assert "Customer = Customer(name='customer')" in code
#     assert "Items = Array(Items, name='items')" in code
