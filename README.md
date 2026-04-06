# surety-scaffold

Code generation toolkit for the [surety](https://github.com/elenakulgavaya/surety) contract-testing framework.

Bootstraps surety schemas, contracts, callers, and test scaffolding from existing JSON payloads, JSON Schema, and OpenAPI specs — so you can start contract-based testing without writing boilerplate by hand.

---

## Installation

```bash
pip install surety-scaffold
```

Requires `surety>=0.0.4`.

---

## Features

### Extract contract from JSON

Turn a raw JSON payload into surety `Dictionary` class definitions.

**Programmatic:**

```python
import json
from surety.scaffold import extract_from_json

payload = json.dumps({
    "order_id": 42,
    "status": "pending",
    "total": 199.99,
    "is_express": False,
    "customer": {
        "customer_id": 7,
        "email": "jane@example.com"
    },
    "items": [
        {"sku": "ABC-1", "qty": 2}
    ]
})

print(extract_from_json(payload, class_name="Order"))
```

Output:

```python
from surety import Array, Bool, Dictionary, Float, Int, String


class Customer(Dictionary):
    CustomerId = Int(name='customer_id', required=True)
    Email = String(name='email', required=True)


class Items(Dictionary):
    Sku = String(name='sku', required=True)
    Qty = Int(name='qty', required=True)


class Order(Dictionary):
    OrderId = Int(name='order_id', required=True)
    Status = String(name='status', required=True)
    Total = Float(name='total', required=True)
    IsExpress = Bool(name='is_express', required=True)
    Customer = Customer(name='customer', required=True)
    Items = Array(Items, name='items', required=True)
```

**Type inference rules:**

| JSON value | Surety type |
|------------|-------------|
| `true` / `false` | `Bool` |
| integer | `Int` |
| float | `Float` |
| UUID string | `Uuid` |
| ISO 8601 datetime or date string | `DateTime` |
| any other string | `String` |
| object `{}` | nested `Dictionary` subclass |
| array of objects | `Array(NestedClass, ...)` |
| array of primitives | `Array(PrimitiveType, ...)` |
| `null` | `String(allow_none=True)` |

Nested objects produce their own `Dictionary` subclass and are always emitted before the class that references them. Arrays of objects merge all items across the array to capture the full set of fields. Duplicate class names (same key appearing at different nesting levels) are disambiguated automatically with a numeric suffix.

**Key naming:**
JSON keys are converted to `PascalCase` for both the class attribute name and the generated class name. `snake_case`, `camelCase`, and `kebab-case` are all handled.

---

**CLI:**

```bash
# Pass JSON as an argument
surety-scaffold '{"order_id": 1, "status": "pending"}' --class-name Order

# Pipe from a file or command
cat response.json | surety-scaffold --class-name Order

# Skip clipboard copy
surety-scaffold '{"x": 1}' --no-clipboard
```

The result is printed to stdout and automatically copied to the clipboard (`pbcopy` on macOS, `xclip` on Linux).

```
usage: surety-scaffold [-h] [--class-name CLASS_NAME] [--no-clipboard] [json]

positional arguments:
  json                  JSON string to extract from. Reads from stdin if omitted.

options:
  --class-name, -c      Name for the top-level generated class (default: Schema).
  --no-clipboard        Do not copy the result to the clipboard.
```

---

## Roadmap

The following features are planned for this library. They complement the core surety framework with static analysis, code generation, and developer tooling.

### In scope for surety-scaffold

| # | Feature | Status |
|---|---------|--------|
| 1 | **Extract contract from JSON** — infer surety schemas from raw API responses | done |
| 4 | **Parse JSON Schema / OpenAPI** — generate surety `Dictionary` classes from JSON Schema or OpenAPI 3.x specs, resolving `$ref` and mapping constraints | planned |
| 5 | **Generate callers** — produce `ApiContract` boilerplate and caller function stubs from OpenAPI operations | planned |
| 12 | **Generate test scenarios (basic)** — scaffold positive pytest test cases (required fields, full fields, `with_values` overrides) for a given contract | planned |
