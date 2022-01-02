"""Models for API."""

from typing import Iterator, List, Optional
from datetime import datetime
from enum import Enum
from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin


class ImageExtension(str, Enum):
    """Enumeration for image extension."""
    JPG = "j"
    PNG = "p"
    GIF = "g"


class TagType(str, Enum):
    """Enumeration for tag type."""
    TAG = "tag"
    CATEGORY = "category"
    ARTIST = "artist"
    PARODY = "parody"
    CHARACTER = "character"
    GROUP = "group"
    LANGUAGE = "language"


@dataclass(frozen=True)
class Image(DataClassJsonMixin):  # TODO?: new name: Page
    """Class that represents an image."""
    name: str
    url: str
    media_id: int
    width: int
    height: int
    extension: ImageExtension


@dataclass(frozen=True)
class Tag(DataClassJsonMixin):
    """Class that represents a tag."""
    id: int
    count: int
    name: str
    type: TagType
    url: str


@dataclass(frozen=True)
class Title(DataClassJsonMixin):
    """Class that represents a title."""
    english: Optional[str]
    japanese: Optional[str]
    pretty: Optional[str]


@dataclass(frozen=True)
class Doujin(DataClassJsonMixin):
    """Class that represents a doujin."""
    id: int
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
        return len(self.pages)

    def __getitem__(self, key: int) -> Image:
        return self.pages[key]


@dataclass(frozen=True)
class DoujinsResult(DataClassJsonMixin):
    """Class that represents an doujins result."""
    doujins: List[Doujin]
    pages_count: int
    doujins_per_page: int
