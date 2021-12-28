from typing import Any, Dict, Optional
from datetime import datetime
import json as _json

from schema import (
    Schema,
    Or as SchemaOr,
    Optional as SchemaOptional
)

from models import (
    ImageExtension,
    TagType,
    Image,
    Tag,
    Title,
    Doujin,
)


class ImageJsonConventer():
    def convert(self, json: Dict[str, Any]) -> Image:
        media_id: int = json["media_id"]
        name: str = json["name"]
        width: int = json["width"]
        height: int = json["height"]
        extension = ImageExtension(json["extension"])

        return Image(
            name=name,
            media_id=media_id,
            width=width,
            height=height,
            extension=extension,
            url=(  # TODO
                f"https://t.nhentai.net/galleries/{media_id}/{name}.{extension.name.lower()}"
                if name in ("cover", "thumb",) else
                f"https://i.nhentai.net/galleries/{media_id}/{name}.{extension.name.lower()}"
            )
        )


class TagJsonConventer():
    def convert(self, json: Dict[str, Any]) -> Tag:
        id_: int = json["id"]
        count: int = json["count"]
        name: str = json["name"]
        type = TagType(json["type"])
        url: str = json["url"]

        return Tag(
            id=id_,
            count=count,
            name=name,
            type=type,
            url=url,
        )


class TitleJsonConventer():
    def convert(self, json: Dict[str, Any]) -> Title:
        english: Optional[str] = json["english"]
        japanese: Optional[str] = json["japanese"]
        pretty: Optional[str] = json["pretty"]

        return Title(
            english=english,
            japanese=japanese,
            pretty=pretty,
        )


class DoujinJsonConventer():
    def convert(self, json: Dict[str, Any]) -> Doujin:
        doujin_id: int = json["id"]
        media_id: int = json["media_id"]
        favorites_count: int = json["favorites"]
        pages_count = len(json["pages"])
        scanlator: str = json["scanlator"]
        upload_date = datetime.utcfromtimestamp(
            json["upload_date"],
        )

        title = TitleJsonConventer().convert(json["title"])
        thumbnail = ImageJsonConventer().convert(json["thumbnail"])
        cover = ImageJsonConventer().convert(json["cover"])

        tags = [
            TagJsonConventer().convert(data)
            for data in json["tags"]
        ]  # TODO

        pages = [
            ImageJsonConventer().convert(data)
            for data in json["pages"]
        ]

        return Doujin(
            doujin_id=doujin_id,
            media_id=media_id,
            favorites_count=favorites_count,
            pages_count=pages_count,
            scanlator=scanlator,
            upload_date=upload_date,
            title=title,
            thumbnail=thumbnail,
            cover=cover,
            tags=tags,
            pages=pages,
        )
