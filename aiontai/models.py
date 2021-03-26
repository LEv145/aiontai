from datetime import datetime
from typing import List, Optional
from enum import Enum
from dataclasses import dataclass
from functools import cached_property
from .config import config
from . import utils


Datetime = datetime


class ImageExtenstion(Enum):
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


@dataclass
class Image:
    name: str
    media_id: int
    width: int
    height: int
    extenstion: ImageExtenstion

    @classmethod
    def from_json(cls, json: dict) -> Optional["Image"]:
        if utils.is_valid_structure(config.image_structure, json):
            name = json["name"]
            media_id = json["media_id"]
            width = json["w"]
            height = json["h"]
            extenstion = ImageExtenstion(json["t"])

            return cls(name, media_id, width, height, extenstion)

    @cached_property
    def url(self) -> str:
        return f"{config.gallery_url}/{self.media_id}/{self.name}.{self.extenstion}"


@dataclass
class Tag:
    id: int
    count: int
    name: str
    type: TagType
    url: str

    @classmethod
    def from_json(cls, json: dict) -> Optional["Tag"]:
        if utils.is_valid_structure(config.tag_structure, json):
            tag_id = json["id"]
            tag_count = json["count"]
            tag_name = json["name"]
            tag_type = TagType(json["type"])
            tag_url = json["url"]

            return cls(tag_id, tag_count, tag_name, tag_type, tag_url)


@dataclass
class Title:
    english: str
    japanese: str
    pretty: str

    @classmethod
    def from_json(cls, json: dict) -> Optional["Title"]:
        if utils.is_valid_structure(config.title_structure, json):
            title_english = json["english"]
            title_japanese = json["japanese"]
            title_pretty = json["pretty"]

            return cls(title_english, title_japanese, title_pretty)


@dataclass
class Doujin:
    id: int
    media_id: int
    title: Optional[Title]
    cover: Optional[Image]
    thumbnail: Optional[Image]
    pages: List[Optional[Image]]
    tags: List[Optional[Tag]]
    pages_count: int
    favorites: int
    scanlator: str
    upload_date: Datetime
