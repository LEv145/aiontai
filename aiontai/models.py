from datetime import datetime
from typing import List
from enum import Enum
from dataclasses import dataclass
from functools import cached_property
from aiontai.config import config
from aiontai import utils


Datetime = datetime


class ImageExtension(Enum):
    jpg = "j"
    png = "p"
    gif = "g"


class TagType(Enum):
    tag = "tag"
    category = "category"
    artist = "artist"
    parody = "parody"
    character = "character"
    group = "group"
    language = "language"


@dataclass(frozen=True)
class Image:
    name: str
    media_id: int
    width: int
    height: int
    extension: ImageExtension

    @classmethod
    def from_json(cls, json: dict) -> "Image":
        utils.is_valid_structure(config.image_structure, json)

        name = json["name"]
        media_id = json["media_id"]
        width = json["width"]
        height = json["height"]
        extension = ImageExtension(json["extension"])

        return cls(name, media_id, width, height, extension)

    @cached_property
    def url(self) -> str:
        if self.name in ["cover", "thumb"]:
            return f"{config.t_gallery_url}/{self.media_id}/{self.name}.{self.extension.name}"
        else:
            return f"{config.i_gallery_url}/{self.media_id}/{self.name}.{self.extension.name}"


@dataclass(frozen=True)
class Tag:
    id: int
    count: int
    name: str
    type: TagType
    url: str

    @classmethod
    def from_json(cls, json: dict) -> "Tag":
        utils.is_valid_structure(config.tag_structure, json)

        tag_id = json["id"]
        tag_count = json["count"]
        tag_name = json["name"]
        tag_type = TagType(json["type"])
        tag_url = json["url"]

        return cls(tag_id, tag_count, tag_name, tag_type, tag_url)


@dataclass(frozen=True)
class Title:
    english: str
    japanese: str
    pretty: str

    @classmethod
    def from_json(cls, json: dict) -> "Title":
        utils.is_valid_structure(config.title_structure, json)

        title_english = json["english"]
        title_japanese = json["japanese"]
        title_pretty = json["pretty"]

        return cls(title_english, title_japanese, title_pretty)


@dataclass(frozen=True)
class Doujin:
    id: int
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
        utils.is_valid_structure(config.doujin_structure, json)

        id = json["id"]
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

        return cls(id, media_id, title, cover,
                   thumbnail, pages, tags, pages_count,
                   favorites, scanlator, upload_date)
