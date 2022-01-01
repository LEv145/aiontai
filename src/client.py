"""Module API wrapper impementation."""

from typing import TYPE_CHECKING

from .api import NHentaiAPI, SortOptions
from .converters import (
    JsonConventer
)

if TYPE_CHECKING:
    from .models import (
        Doujin,
        DoujinsResult,
    )


class NHentaiClient():
    """Impementation of NHentaiAPI wrapper."""
    def __init__(self, api: NHentaiAPI) -> None:
        self.api = api

    async def get_doujin(self, doujin_id: int) -> "Doujin":
        """Method for getting doujin by id.
        Args:
            :doujin_id int: Doujin's id, which we get.

        Returns:
            JSON of doujin.

        Raises:
            DoujinDoesNotExist if doujin was not found.

        Usage:
            >>> api = aiontai.API()
            >>> await api.get_doujin(1)
            Doujin(...)
        """
        raw_data = await self.api.get_doujin(doujin_id)

        return JsonConventer.convert_doujin(raw_data)

    async def is_exist(self, doujin_id: int) -> bool:
        """Method for checking does doujin exist.
        Args:
            :doujin_id int: Doujin's id, which we check.

        Returns:
            True if doujin is exist, False if doujin is not exist.

        Usage:
            >>> api = aiontai.API()
            >>> await api.is_exist(1)
            True
        """
        raw_data = await self.api.is_exist(doujin_id)

        return raw_data

    async def get_random_doujin(self) -> "Doujin":
        """Method for getting random doujin.
        Returns:
            JSON of random doujin.

        Usage:
            >>> api = aiontai.API()
            >>> await api.random_doujin()
            Doujin(...)
        """
        raw_data = await self.api.get_random_doujin()

        return JsonConventer.convert_doujin(raw_data)

    async def search(
        self,
        query: str,
        *,
        page: int = 1,
        sort_by: SortOptions = SortOptions.DATE,
    ) -> "DoujinsResult":
        """Method for search doujins.
        Args:
            :query str: Query for search doujins.
            :page int: Page, from which we return results.
            :sort_by str: Sort for search.

        Returns:
            List of doujins JSON

        Raises:
            IsNotValidSort if sort is not a member of SortOptions.
            WrongPage if page less than 1.
            WrongSearch if any errors

        Usage:
            >>> api = aiontai.API()
            >>> await api.search("anime", page=2, sort_by="popular")
            [Doujin(...), ...]
        """
        result = await self.api.search(
            query=query,
            page=page,
            sort_by=sort_by,
        )

        return JsonConventer.convert_doujins_result(result)

    async def search_by_tag(
        self,
        tag_id: int,
        *,
        page: int = 1,
        sort_by: SortOptions = SortOptions.DATE,
    ) -> "DoujinsResult":
        """Method for search doujins by tag.
        Args:
            :tag id: Tag for search doujins.
            :page int: Page, from which we return results.
            :sort_by str: Sort for search.

        Returns:
            List of doujins JSON

        Raises:
            IsNotValidSort if sort is not a member of SortOptions.
            WrongPage if page less than 1 or page has no content.
            WrongTag if tag with given id does not exist.

        Usage:
            >>> api = aiontai.API()
            >>> await api.search_by_tag(1, page=2, sort_by="popular")
            [Doujin(...), ...]
        """
        result = await self.api.search_by_tag(
            tag_id=tag_id,
            page=page,
            sort_by=sort_by,
        )

        return JsonConventer.convert_doujins_result(result)

    async def get_homepage_doujins(
        self,
        *,
        page: int = 1
    ) -> "DoujinsResult":
        """Method for getting doujins from.
        Args:
            :page int: Page, from which we get doujins.

        Returns:
            List of doujins JSON

        Raises:
            WrongPage if page less than 1 or page has no content.

        Usage:
            >>> api = aiontai.API()
            >>> await api.get_homepage_doujins(1)
            [Doujin(...), ...]
        """
        result = await self.api.get_homepage_doujins(
            page=page,
        )

        return JsonConventer.convert_doujins_result(result)

# async def search_all_by_tags(self, tag_ids: list) -> List[models.Doujin]:
#     """Method for search doujins by tags.
#     Args:
#         :tag_ids list: List of tags

#     Returns:
#         List of doujins JSON

#     Raises:
#         IsNotValidSort if sort is not a member of SortOptions.
#         WrongPage if page less than 1.

#     Usage:
#         >>> api = aiontai.API()
#         >>> await api.search_all_by_tag([11])
#         [Doujin(...), ...]
#     """

#     result = await self.api.search_all_by_tags(tag_ids)

#     return [
#         DoujinJsonConventer().convert(raw_data)
#         for raw_data in result
#     ]
