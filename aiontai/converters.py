from typing import Optional
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
    def convert(self, raw_data: str) -> Image:
        json = _json.loads(raw_data)

        Schema({
            "name": str,
            "media_id": int,
            "height": int,
            "extension": str,
            "width": int,
        }).validate(json)

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
            url=(
                f"https://t.nhentai.net/galleries/{media_id}/{name}.{extension.name}"
                if name in ("cover", "thumb") else
                f"https://i.nhentai.net/galleries/{media_id}/{name}.{extension.name}"
            )
        )


class TagJsonConventer():
    def convert(self, raw_data: str) -> Tag:
        json = _json.loads(raw_data)

        Schema({
            "count": int,
            "id": int,
            "name": str,
            "type": str,
            "url": str,
        }).validate(json)

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
    def convert(self, raw_data: str) -> Title:
        json = _json.loads(raw_data)

        Schema({
            SchemaOptional("english"): SchemaOr(str, None),
            SchemaOptional("japanese"): SchemaOr(str, None),
            SchemaOptional("pretty"): SchemaOr(str, None),
        }).validate(json)

        english: Optional[str] = json["english"]
        japanese: Optional[str] = json["japanese"]
        pretty: Optional[str] = json["pretty"]

        return Title(
            english=english,
            japanese=japanese,
            pretty=pretty,
        )


class DoujinJsonConventer():
    def convert(self, raw_data: str) -> Doujin:
        json = _json.loads(raw_data)

        Schema({
            "id": int,
            "media_id": int,
            "title": {SchemaOptional(str): SchemaOr(str, None)},
            "cover": {
                "name": str,
                "extension": str,
                "media_id": int,
                "height": int,
                "width": int,
            },
            "pages": [
                {
                    "name": str,
                    "extension": str,
                    "media_id": int,
                    "height": int,
                    "width": int
                },
            ],
            "thumbnail": {
                "name": str,
                "extension": str,
                "media_id": int,
                "height": int,
                "width": int
            },
            "tags": [{str: SchemaOr(int, str)}],
            "favorites": int,
            "pages_count": int,
            "scanlator": str,
            "upload_date": int,
        }).validate(json)

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
