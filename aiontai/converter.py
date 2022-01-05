"""Conventer module."""

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


class Conventer():
    """Conventer for convert raw data to models."""

    def convert_doujins_result(
        self,
        raw_data: Dict[str, Any],
    ) -> DoujinsResult:
        """Convert raw data to DoujinsResult model."""
        doujins = [
            self.convert_doujin(doujin_raw_data)
            for doujin_raw_data in raw_data["result"]
        ]
        pages_count: int = raw_data["num_pages"]
        doujins_per_page: int = raw_data["per_page"]

        return DoujinsResult(
            doujins=doujins,
            pages_count=pages_count,
            doujins_per_page=doujins_per_page,
        )

    def convert_doujin(
        self,
        raw_data: Dict[str, Any],
    ) -> Doujin:
        """Convert raw data to Doujin model."""
        id: int = raw_data["id"]
        media_id = int(raw_data["media_id"])
        favorites_count: int = raw_data["num_favorites"]
        pages_count: int = raw_data["num_pages"]
        scanlator: str = raw_data["scanlator"]
        upload_date = datetime.utcfromtimestamp(
            raw_data["upload_date"],
        )

        title = self.convert_title(raw_data["title"])

        thumbnail = self.convert_image(
            raw_data["images"]["thumbnail"],
            name="thumb",
            media_id=media_id,
        )
        cover = self.convert_image(
            raw_data["images"]["cover"],
            name="cover",
            media_id=media_id,
        )

        tags = [
            self.convert_tag(data)
            for data in raw_data["tags"]
        ]

        images = [
            self.convert_image(
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
            images=images,
        )

    def convert_title(
        self,
        raw_data: Dict[str, Any],
    ) -> Title:
        """Convert raw data to Title model."""
        english: Optional[str] = raw_data["english"]
        japanese: Optional[str] = raw_data["japanese"]
        pretty: Optional[str] = raw_data["pretty"]

        return Title(
            english=english,
            japanese=japanese,
            pretty=pretty,
        )

    def convert_image(
        self,
        raw_data: Dict[str, Any],
        name: str,
        media_id: int,
    ) -> Image:
        """Convert raw data to Image model."""
        width: int = raw_data["w"]
        height: int = raw_data["h"]
        image_type = ImageExtension(raw_data["t"])

        return Image(
            name=name,
            media_id=media_id,
            width=width,
            height=height,
            extension=image_type,
            url=(
                f"https://t.nhentai.net/galleries/{media_id}/{name}.{image_type.name.lower()}"
                if name in ("cover", "thumb") else
                f"https://i.nhentai.net/galleries/{media_id}/{name}.{image_type.name.lower()}"
            ),
        )

    def convert_tag(
        self,
        raw_data: Dict[str, Any],
    ) -> Tag:
        """Convert raw data to Tag model."""
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
