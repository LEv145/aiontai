"""Utils for api."""

from schema import SchemaError, Schema
from aiontai import errors, api


def is_valid_structure(schema: Schema, json: dict) -> bool:
    """Check, is structure valid to schema.

    Args:
        :schema Schema: -- structure schema for validation.
        :json dict: -- json of structure, which we validate.

    Exceptions:
        IsNotValidStructure if structure of json is not valid to schema.

    Returns:
        True if structure is valid to schema.
    """
    try:
        schema.validate(json)
        return True
    except SchemaError as exception:
        raise errors.IsNotValidStructure(
            "You cant build a class from JSON, because it havent valid JSON structure."
        ) from exception


def extract_digits(string: str) -> str:
    """Util for extracting digits from string.

    Args:
        :string str: -- String, from which we extract digits.

    Returns:
        str
    """
    return "".join([symbol for symbol in string if symbol.isdigit()])


def is_valid_search_parameters(page: int, sort_by: str) -> bool:
    """Check, is valid search parameters.

    Args:
        :page int: -- Page for checking.
        :sort_by str: -- Sort options for checking.

    Exceptions:
        ValueError if sort options is not valid.
        WrongPage if page is wrong.

    Returns:
        True if parameters is valid.
    """
    try:
        api.SortOptions(sort_by)
    except ValueError as exception:
        raise errors.IsNotValidSort(
            f"You choose sort, which not in {list(api.SortOptions.__members__)}"
        ) from exception

    if page < 1:
        raise errors.WrongPage("Page can not be less than 1")

    return True


def is_valid_search_by_tag_parameters(tag_id: int, page: int, sort_by: str) -> bool:
    """Check, is valid search parameters.

    Args:
        :tag_id int: -- Tag id for checking
        :page int: -- Page for checking.
        :sort_by str: -- Sort_by for checking.

    Exceptions:
        ValueError if sort options is not valid.
        WrongPage if page is wrong.
        WrongTag is tag id is wrong.

    Returns:
        True if parameters is valid.
    """
    if page < 1:
        raise errors.WrongPage("Page can not be less than 1")
    elif tag_id < 1:
        raise errors.WrongTag("Tag id can not be less than 1")

    try:
        api.SortOptions(sort_by)
    except ValueError as exception:
        raise errors.IsNotValidSort(
            f"You choose sort, which not in {list(api.SortOptions.__members__)}"
        ) from exception

    return True


async def make_doujin_json(original: dict) -> dict:
    """Convert JSON response to doujin JSON.

    Args:
        :original dict: -- JSON of response.

    Returns:
        dictionary of doujin.
    """
    doujin_id = int(original["id"])
    media_id = int(original["media_id"])
    title = original["title"]
    scanlator = original["scanlator"]
    favorites = original["num_favorites"]
    upload_date = original["upload_date"]
    cover = {
        "name": "cover",
        "media_id": media_id,
        "extension": original["images"]["cover"]["t"],
        "height": original["images"]["cover"]["h"],
        "width": original["images"]["cover"]["w"]
    }
    thumbnail = {
        "name": "thumb",
        "media_id": media_id,
        "extension": original["images"]["thumbnail"]["t"],
        "height": original["images"]["thumbnail"]["h"],
        "width": original["images"]["thumbnail"]["w"]
    }
    pages = [
        {
            "name": f"{count + 1}",
            "media_id": media_id,
            "extension": original["images"]["pages"][count]["t"],
            "height": original["images"]["pages"][count]["h"],
            "width": original["images"]["pages"][count]["w"]
        }
        for count, _ in enumerate(original["images"]["pages"])
    ]
    pages_count = len(pages)
    tags = list(original["tags"])

    json = {
        "id": doujin_id,
        "media_id": media_id,
        "title": title,
        "cover": cover,
        "thumbnail": thumbnail,
        "pages": pages,
        "tags": tags,
        "favorites": favorites,
        "pages_count": pages_count,
        "scanlator": scanlator,
        "upload_date": upload_date
    }

    return json
