from schema import SchemaError, Schema
from . import errors


def is_valid_structure(schema: Schema, json: dict) -> bool:
    try:
        schema.validate(json)
        return True
    except SchemaError:
        raise errors.IsNotValidStructure(
            "You cant build a class from JSON, because it havent valid JSON structure."
        )
