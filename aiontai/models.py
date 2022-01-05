"""API Models."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import (
    Iterator,
    List,
    Optional,
)

from dataclasses_json import DataClassJsonMixin


class ImageExtension(str, Enum):
    """Enum for image extension."""

    JPG = "j"
    PNG = "p"
    GIF = "g"


class TagType(str, Enum):
    """Enum for tag type."""

    TAG = "tag"
    CATEGORY = "category"
    ARTIST = "artist"
    PARODY = "parody"
    CHARACTER = "character"
    GROUP = "group"
    LANGUAGE = "language"


@dataclass(frozen=True)
class Image(DataClassJsonMixin):
    """Image model."""

    name: str
    url: str
    media_id: int
    width: int
    height: int
    extension: ImageExtension


@dataclass(frozen=True)
class Tag(DataClassJsonMixin):
    """Tag model."""

    id: int
    count: int
    name: str
    type: TagType
    url: str


@dataclass(frozen=True)
class Title(DataClassJsonMixin):
    """Title model."""

    english: Optional[str]
    japanese: Optional[str]
    pretty: Optional[str]


@dataclass(frozen=True)
class Doujin(DataClassJsonMixin):
    """Doujin model."""

    id: int
    media_id: int
    title: Title
    cover: Image
    thumbnail: Image
    images: List[Image]
    tags: List[Tag]
    pages_count: int
    favorites_count: int
    scanlator: str
    upload_date: datetime

    def __iter__(self) -> Iterator[Image]:
        """Pages iterator."""
        return iter(self.images)

    def __len__(self) -> int:
        """Pages len."""
        return len(self.images)

    def __getitem__(self, key: int) -> Image:
        """Get page by key."""
        return self.images[key]


@dataclass(frozen=True)
class DoujinsResult(DataClassJsonMixin):
    """DoujinsResult model."""

    doujins: List[Doujin]
    pages_count: int
    doujins_per_page: int
