"""Models for API."""

from typing import Iterator, List, Optional
from datetime import datetime
from enum import Enum
from dataclasses import dataclass


class ImageExtension(Enum):
    """Enumeration for image extension."""

    JPG = "j"
    PNG = "p"
    GIF = "g"


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
    """Class that represents an image."""

    name: str
    url: str
    media_id: int
    width: int
    height: int
    extension: ImageExtension


@dataclass(frozen=True)
class Tag:
    """Class that represents a tag."""

    id: int
    count: int
    name: str
    type: TagType
    url: str


@dataclass(frozen=True)
class Title:
    """Class that represents a title."""

    english: Optional[str]
    japanese: Optional[str]
    pretty: Optional[str]


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
    favorites_count: int
    scanlator: str
    upload_date: datetime

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
