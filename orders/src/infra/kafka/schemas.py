order_schema_str = """
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Order",
    "type": "object",
    "properties": {
        "id": {
            "type": "string",
            "format": "uuid"
        },
        "user_id": {
            "type": "string",
            "format": "uuid"
        },
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "price": {
                        "type": "integer",
                        "minimum": 0
                    },
                    "count": {
                        "type": "integer",
                        "minimum": 1
                    }
                },
                "required": ["name", "price", "count"]
            }
        }
    },
    "required": ["id", "user_id", "items"]
}
"""