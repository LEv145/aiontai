from schema import SchemaError, Schema
from aiontai import errors, api


def is_valid_structure(schema: Schema, json: dict) -> bool:
    try:
        schema.validate(json)
        return True
    except SchemaError:
        raise errors.IsNotValidStructure(
            "You cant build a class from JSON, because it havent valid JSON structure."
        )


def extract_digits(string: str) -> str:
    return "".join([symbol for symbol in string if symbol.isdigit()])


def is_valid_search_parameters(page: int, sort_by: str) -> bool:
    try:
        api.SortOptions(sort_by)
    except ValueError:
        raise errors.IsNotValidSort(
            f"You choose sort, which not in {[option for option in api.SortOptions.__members__]}"
        )

    if 1 > page:
        raise errors.WrongPage("Page can not be less than 1")

    return True
