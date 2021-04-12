"""Models for API."""

from datetime import datetime
from typing import Iterator, List
from enum import Enum
from dataclasses import dataclass
from functools import cached_property
from aiontai.config import config
from aiontai import utils


Datetime = datetime


class ImageExtension(Enum):
    """Enumeration for image extension."""

    jpg = "j"
    png = "p"
    gif = "g"


class TagType(Enum):
    """Enumeration for tag type."""

    TAG = "tag"
    CATEGORY = "category"
    ARTIST = "artist"
    PARODY = "parody"
    CHARACTER = "character"
    GROUP = "group"
    LANGUAGE = "language"


@dataclass(frozen=True)
class Image:
    """Class that represents an Image."""

    name: str
    media_id: int
    width: int
    height: int
    extension: ImageExtension

    @classmethod
    def from_json(cls, json: dict) -> "Image":
        """Classmethod for creating image from JSON."""

        utils.is_valid_structure(config.image_structure, json)

        name = json["name"]
        media_id = json["media_id"]
        width = json["width"]
        height = json["height"]
        extension = ImageExtension(json["extension"])

        return cls(name, media_id, width, height, extension)

    @cached_property
    def url(self) -> str:
        """Property of url."""

        if self.name in ["cover", "thumb"]:
            return f"{config.t_gallery_url}/{self.media_id}/{self.name}.{self.extension.name}"
        else:
            return f"{config.i_gallery_url}/{self.media_id}/{self.name}.{self.extension.name}"


@dataclass(frozen=True)
class Tag:
    """Class that represents a tag."""

    id: int
    count: int
    name: str
    type: TagType
    url: str

    @classmethod
    def from_json(cls, json: dict) -> "Tag":
        """Classmethod for creating tag from JSON."""

        utils.is_valid_structure(config.tag_structure, json)

        tag_id = json["id"]
        tag_count = json["count"]
        tag_name = json["name"]
        tag_type = TagType(json["type"])
        tag_url = json["url"]

        return cls(tag_id, tag_count, tag_name, tag_type, tag_url)


@dataclass(frozen=True)
class Title:
    """Class that represents a title."""

    english: str
    japanese: str
    pretty: str

    @classmethod
    def from_json(cls, json: dict) -> "Title":
        """Classmethod for making title from JSON."""

        utils.is_valid_structure(config.title_structure, json)

        title_english = json["english"]
        title_japanese = json["japanese"]
        title_pretty = json["pretty"]

        return cls(title_english, title_japanese, title_pretty)


@dataclass(frozen=True)
class Doujin:
    """Class, that represents a doujin."""

    doujin_id: int
    media_id: int
    title: Title
    cover: Image
    thumbnail: Image
    pages: List[Image]
    tags: List[Tag]
    pages_count: int
    favorites: int
    scanlator: str
    upload_date: Datetime

    @classmethod
    def from_json(cls, json: dict) -> "Doujin":
        """Classmethod for creating doujin from JSON."""

        utils.is_valid_structure(config.doujin_structure, json)

        doujin_id = json["id"]
        media_id = json["media_id"]
        favorites = json["favorites"]
        pages_count = len(json["pages"])
        scanlator = json["scanlator"]
        upload_date = Datetime.utcfromtimestamp(json["upload_date"])

        title = Title.from_json(json["title"])
        thumbnail = Image.from_json(json["thumbnail"])
        cover = Image.from_json(json["cover"])

        tags = [Tag.from_json(data) for data in json["tags"]]
        pages = [Image.from_json(data) for data in json["pages"]]

        return cls(doujin_id, media_id, title, cover,
                   thumbnail, pages, tags, pages_count,
                   favorites, scanlator, upload_date)

    def __iter__(self) -> Iterator[Image]:
        return iter(self.pages)

    def __len__(self) -> int:
        return self.pages_count

    def __reversed__(self) -> Iterator[Image]:
        return reversed(self.pages)

    def __contains__(self, page: Image) -> bool:
        return page in self.pages

    def __getitem__(self, key) -> Image:
        return self.pages[key]
