from datetime import datetime
from typing import List, Optional
from enum import Enum
from dataclasses import dataclass
from .config import config
from . import utils


class ImageType(Enum):
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
    width: int
    height: int
    type: ImageType

    @classmethod
    def from_json(cls, json: dict) -> Optional["Image"]:
        if utils.is_valid_structure(config.image_structure, json):
            image_weight = json["w"]
            image_height = json["h"]
            image_type = ImageType(json["t"])

            return cls(image_weight, image_height, image_type)


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


Cover = Image
Thumbnail = Image
Page = Image
Datetime = datetime


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

    @classmethod
    def from_json(cls, json: dict) -> Optional["Doujin"]:
        if utils.is_valid_structure(config.doujin_structure, json):
            id = json["id"]
            media_id = json["media_id"]
            scanlator = json["scanlator"]
            title = Title.from_json(json["title"])

            images = json["images"]
            cover = Cover.from_json(images["cover"])
            thumbnail = Thumbnail.from_json(images["thumbnail"])

            favorites = json["num_favorites"]
            tags = [Tag.from_json(tag_json) for tag_json in json["tags"]]
            pages = [Page.from_json(page_json) for page_json in images["pages"]]
            pages_count = len(pages)

            upload_date = Datetime.utcfromtimestamp(json["upload_date"])

            return cls(id, media_id, title, cover, thumbnail, pages, tags, pages_count, favorites, scanlator, upload_date)
