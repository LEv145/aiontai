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


def is_valid_search_by_tag_parameters(tag_id: int, page: int, sort_by: str) -> bool:
    try:
        api.SortOptions(sort_by)
    except ValueError:
        raise errors.IsNotValidSort(
            f"You choose sort, which not in {[option for option in api.SortOptions.__members__]}"
        )

    if 1 > page:
        raise errors.WrongPage("Page can not be less than 1")
    elif 1 > tag_id:
        raise errors.WrongTag("Tag id can not be less than 1")

    return True


async def make_doujin_json(original: dict) -> dict:
    id = original["id"]
    media_id = original["media_id"]
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
        "name": "thumbnail",
        "media_id": media_id,
        "extension": original["images"]["thumbnail"]["t"],
        "height": original["images"]["thumbnail"]["h"],
        "width": original["images"]["thumbnail"]["w"]
    }
    pages = [
        {
            "name": count,
            "media_id": media_id,
            "extension": original["images"][count]["t"],
            "height": original["images"][count]["h"],
            "width": original["images"][count]["w"]
        }
        for count, _ in enumerate(original["images"]["pages"], start=1)
    ]
    pages_count = len(pages)
    tags = [tag for tag in original["tags"]]

    json = {
        "id": id,
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
