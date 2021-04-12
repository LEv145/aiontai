"""Module API wrapper impementation."""

__all__ = ["API"]

from typing import List
from . import api, utils, models


class API:
    """Impementation of NHentaiAPI wrapper."""

    def __init__(self, *args, **kv) -> None:
        self.nhentai = api.NHentaiAPI(*args, **kv)

    async def get_doujin(self, doujin_id: int) -> models.Doujin:
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
        response = await self.nhentai.get_doujin(doujin_id)
        json = await utils.make_doujin_json(response)

        return models.Doujin.from_json(json)

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
        response = await self.nhentai.is_exist(doujin_id)

        return response

    async def get_random_doujin(self) -> models.Doujin:
        """Method for getting random doujin.
        Returns:
            JSON of random doujin.

        Usage:
            >>> api = aiontai.API()
            >>> await api.random_doujin()
            Doujin(...)
        """
        response = await self.nhentai.get_random_doujin()
        json = await utils.make_doujin_json(response)

        return models.Doujin.from_json(json)

    async def search(self, query: str, *, page: int = 1, sort_by: str = "date") -> List[models.Doujin]:
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

        Usage:
            >>> api = aiontai.API()
            >>> await api.search("anime", page=2, sort_by="popular")
            [Doujin(...), ...]
        """
        response = await self.nhentai.search(query, page, sort_by)

        results = []
        for json in response:
            result = await utils.make_doujin_json(json)
            results.append(result)

        return [models.Doujin.from_json(json) for json in results]

    async def search_by_tag(self, tag: int, *, page: int = 1, sort_by: str = "date") -> List[models.Doujin]:
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
        response = await self.nhentai.search_by_tag(tag, page, sort_by)

        results = []
        for json in response:
            result = await utils.make_doujin_json(json)
            results.append(result)

        return [models.Doujin.from_json(json) for json in results]

    async def get_homepage_doujins(self, *, page: int = 1) -> List[models.Doujin]:
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
        response = await self.nhentai.get_homepage_doujins(page)

        results = []
        for json in response:
            result = await utils.make_doujin_json(json)
            results.append(result)

        return [models.Doujin.from_json(json) for json in results]
    
    async def close(self):
        """Method for close API Session
        Usage:
            >>> api = NHentaiAPI()
            >>> ...
            >>> await api.close()
        """
        await self.nhentai.close()

    
