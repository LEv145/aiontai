from datetime import datetime
from typing import List
from enum import Enum
from dataclasses import dataclass


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
    weight: int
    height: int
    type: ImageType


@dataclass
class Tag:
    id: int
    count: int
    name: str
    type: TagType
    url: str


Cover = Image
Thumbnail = Image
Page = Image


@dataclass
class Title:
    english: str
    japanese: str
    pretty: str


@dataclass
class Doujin:
    id: int
    media_id: int
    title: Title
    cover: Cover
    thumbnail: Thumbnail
    pages: List[Page]
    tags: List[Tag]
    favorites: int
    upload_date: datetime
