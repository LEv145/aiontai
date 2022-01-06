"""Client (High level API)."""

from types import TracebackType
from typing import (
    Type,
    TypeVar,
)

from .api import (
    NHentaiAPI,
    SortOptions,
)
from .converter import Conventer
from .models import (
    Doujin,
    DoujinsResult,
)


class NHentaiClient():
    """NHentai client (high level API)."""
    NHentaiClientType = TypeVar("NHentaiClientType", bound="NHentaiClient")

    def __init__(
        self,
        api: NHentaiAPI,
        conventer: Conventer,
    ) -> None:
        """
        Init object.

        Args:
            api: Low level api.
            conventer: Raw data conventer.
        """
        self.api = api
        self.conventer = conventer

    async def __aenter__(self: NHentaiClientType) -> NHentaiClientType:
        """
        Open async context manager.

        Returns:
            Class object.
        """
        return self

    async def __aexit__(
        self,
        _exception_type: Type[BaseException],
        _exception: BaseException,
        _traceback: TracebackType,
    ) -> None:
        """Close object from async context manager."""
        await self.close()

    async def close(self) -> None:
        """Close object."""
        await self.api.close()

    async def get_doujin(self, doujin_id: int) -> Doujin:
        """
        Get doujin model by id.

        Args:
            doujin_id: ID of doujin.

        Returns:
            Doujin model.
        """
        raw_data = await self.api.get_doujin(doujin_id)

        return self.conventer.convert_doujin(raw_data)

    async def is_exist(self, doujin_id: int) -> bool:
        """
        Check if doujin exists.

        Args:
            doujin_id: ID of doujin.

        Returns:
            Doujin is exists.
        """
        raw_data = await self.api.is_exist(doujin_id)

        return raw_data

    async def get_random_doujin(self) -> Doujin:
        """
        Get random doujin model.

        Returns:
            Doujin model.
        """
        raw_data = await self.api.get_random_doujin()

        return self.conventer.convert_doujin(raw_data)

    async def search(
        self,
        query: str,
        *,
        page: int = 1,
        sort_by: SortOptions = SortOptions.DATE,
    ) -> DoujinsResult:
        """
        Search doujins result model.

        Args:
            query: Query for search doujins.
            page: Number of page from which we return results.
                Defaults to 1.
            sort_by: Sort options for search.
                Defaults to api.SortOptions.DATE.

        Returns:
            Doujins result model.
        """
        result = await self.api.search(
            query=query,
            page=page,
            sort_by=sort_by,
        )

        return self.conventer.convert_doujins_result(result)

    async def search_by_tag(
        self,
        tag_id: int,
        *,
        page: int = 1,
        sort_by: SortOptions = SortOptions.DATE,
    ) -> DoujinsResult:
        """
        Search doujins result model by tag.

        Args:
            tag_id: Tag ID for search.
            page: Number of page from which we return results.
                Defaults to 1.
            sort_by: Sort options for search.
                Defaults to api.SortOptions.DATE.

        Returns:
            Doujins result model.
        """
        result = await self.api.search_by_tag(
            tag_id=tag_id,
            page=page,
            sort_by=sort_by,
        )

        return self.conventer.convert_doujins_result(result)

    async def get_homepage_doujins(
        self,
        *,
        page: int = 1,
    ) -> DoujinsResult:
        """
        Get doujins result model from homepage.

        Args:
            page: Number of page from which we return results.
                Defaults to 1.

        Returns:
            Doujins result model.
        """
        result = await self.api.get_homepage_doujins(
            page=page,
        )

        return self.conventer.convert_doujins_result(result)
