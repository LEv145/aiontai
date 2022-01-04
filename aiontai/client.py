"""Module API wrapper impementation."""

from .api import NHentaiAPI, SortOptions
from .converter import (
    Conventer,
)
from .models import (
    Doujin,
    DoujinsResult,
)


class NHentaiClient():
    """Impementation of NHentaiAPI wrapper."""

    def __init__(
        self,
        api: NHentaiAPI,
        conventer: Conventer,
    ) -> None:
        """
        Init object.

        Args:
            api (NHentaiAPI): Low level api.
            conventer (Conventer): Raw data conventer.
        """
        self.api = api
        self.conventer = conventer

    async def close(self):
        """Close object."""
        await self.api.close()

    async def get_doujin(self, doujin_id: int) -> Doujin:
        """
        Get doujin model by id.

        Args:
            doujin_id (int): ID of doujin.

        Returns:
            models.Doujin: doujin model.
        """
        raw_data = await self.api.get_doujin(doujin_id)

        return self.conventer.convert_doujin(raw_data)

    async def is_exist(self, doujin_id: int) -> bool:
        """
        Check if the doujin exists.

        Args:
            doujin_id (int): ID of doujin.

        Returns:
            bool: The doujin is exists.
        """
        raw_data = await self.api.is_exist(doujin_id)

        return raw_data

    async def get_random_doujin(self) -> Doujin:
        """
        Get random doujin model.

        Returns:
            models.Doujin: doujin model.
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
            query (str): Query for search doujins.
            page (int, optional): Number of page from which we return the results.
                Defaults to 1.
            sort_by (api.SortOptions, optional): Sort options for search.
                Defaults to api.SortOptions.DATE.

        Returns:
            models.DoujinsResult: doujins result model.
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
            tag_id (int): Tag ID for search.
            page (int, optional): Number of page from which we return the results.
                Defaults to 1.
            sort_by (api.SortOptions, optional): Sort options for search.
                Defaults to api.SortOptions.DATE.

        Returns:
            models.DoujinsResult: doujins result model.
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
            page (int, optional):  Number of page from which we return the results.
                Defaults to 1.

        Returns:
            models.DoujinsResult: doujins result model.
        """
        result = await self.api.get_homepage_doujins(
            page=page,
        )

        return self.conventer.convert_doujins_result(result)

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
