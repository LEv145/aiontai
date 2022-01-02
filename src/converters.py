# FIXME: WTF?!

from typing import Any, Dict, Optional
from datetime import datetime

from .models import (
    ImageExtension,
    TagType,
    Image,
    Tag,
    Title,
    Doujin,
    DoujinsResult,
)


class JsonConventer():  # Conventer namespase
    @classmethod
    def convert_doujins_result(
        cls,
        raw_data: Dict[str, Any],
    ) -> DoujinsResult:
        doujins = [
            cls.convert_doujin(doujin_raw_data)
            for doujin_raw_data in raw_data["result"]
        ]
        pages_count: int = raw_data["num_pages"]
        doujins_per_page: int = raw_data["per_page"]

        return DoujinsResult(
            doujins=doujins,
            pages_count=pages_count,
            doujins_per_page=doujins_per_page,
        )

    @classmethod
    def convert_doujin(
        cls,
        raw_data: Dict[str, Any]
    ) -> Doujin:
        id: int = raw_data["id"]
        media_id: int = raw_data["media_id"]
        favorites_count: int = raw_data["num_favorites"]
        pages_count: int = raw_data["num_pages"]
        scanlator: str = raw_data["scanlator"]
        upload_date = datetime.utcfromtimestamp(
            raw_data["upload_date"],
        )

        title = cls.convert_title(raw_data["title"])

        thumbnail = cls.convert_image(
            raw_data["images"]["thumbnail"],
            name="thumb",
            media_id=media_id,
        )
        cover = cls.convert_image(
            raw_data["images"]["cover"],
            name="cover",
            media_id=media_id,
        )

        tags = [
            cls.convert_tag(data)
            for data in raw_data["tags"]
        ]  # TODO

        pages = [
            cls.convert_image(
                raw_data,
                name=f"{index + 1}",
                media_id=media_id,
            )
            for index, raw_data in enumerate(raw_data["images"]["pages"])
        ]

        return Doujin(
            id=id,
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

    @classmethod
    def convert_title(
        cls,
        raw_data: Dict[str, Any]
    ) -> Title:
        english: Optional[str] = raw_data["english"]
        japanese: Optional[str] = raw_data["japanese"]
        pretty: Optional[str] = raw_data["pretty"]

        return Title(
            english=english,
            japanese=japanese,
            pretty=pretty,
        )

    @classmethod
    def convert_image(
        cls,
        raw_data: Dict[str, Any],
        name: str,
        media_id: int,
    ) -> Image:
        width: int = raw_data["w"]
        height: int = raw_data["h"]
        type_ = ImageExtension(raw_data["t"])

        return Image(
            name=name,
            media_id=media_id,
            width=width,
            height=height,
            extension=type_,
            url=(
                f"https://t.nhentai.net/galleries/{media_id}/{name}.{type_.name.lower()}"
                if name in ("cover", "thumb",) else
                f"https://i.nhentai.net/galleries/{media_id}/{name}.{type_.name.lower()}"
            )
        )

    @classmethod
    def convert_tag(
        cls,
        raw_data: Dict[str, Any]
    ) -> Tag:
        id_: int = raw_data["id"]
        count: int = raw_data["count"]
        name: str = raw_data["name"]
        type = TagType(raw_data["type"])
        url: str = raw_data["url"]

        return Tag(
            id=id_,
            count=count,
            name=name,
            type=type,
            url=url,
        )
