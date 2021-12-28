"""Impementation of NHentaiAPI."""
import asyncio
from typing import Any, List, Optional
from enum import Enum

from aiohttp import ClientSession, ClientResponse

from . import errors, utils
from .config import config


class SortOptions(Enum):
    """Enumeration for sort options."""

    DATE = "date"
    POPULARITY = "popular"


class NHentaiAPI:
    """Class that represents a nhentai API."""

    def __init__(self):
        self.client_session: Optional[ClientSession] = None

    async def request(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> ClientResponse:
        if self.client_session is None:
            return  # TODO

        response = await self.client_session.request(
            method,
            url,
            **kwargs,
        )
        response.raise_for_status()
        return response

    async def get_doujin(self, doujin_id: int) -> dict:
        """Method for getting doujin by id.
        Args:
            :doujin_id int: Doujin's id, which we get.

        Returns:
            JSON of doujin.

        Raises:
            DoujinDoesNotExist if doujin was not found.
        """
        url = f"{config.api_url}/gallery/{doujin_id}"

        result = await self._get_requests(url)
        if result:
            return result
        else:
            raise errors.DoujinDoesNotExist("That doujin does not exist.")

    async def is_exist(self, doujin_id: int) -> bool:
        """Method for checking does doujin exist.
        Args:
            :doujin_id int: Doujin's id, which we check.

        Returns:
            True if doujin is exist, False if doujin is not exist.
        """
        try:
            await self.get_doujin(doujin_id)
            return True
        except errors.DoujinDoesNotExist:
            return False

    async def get_random_doujin(self) -> dict:
        """Method for getting random doujin.
        Returns:
            JSON of random doujin.
        """
        url = f"{config.base_url}/random/"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, proxy=self.proxy) as response:
                url = response.url.human_repr()
                doujin_id = int(utils.extract_digits(url))
                return await self.get_doujin(doujin_id)

    async def search(self, query: str, page: int = 1, sort_by: str = "date") -> List[dict]:
        """Method for search doujins.
        Args:
            :query str: Query for search doujins.
            :page int: Page, from which we return results.
            :sort_by str:  Sort for search (popular or date).

        Returns:
            List of doujins JSON

        Raises:
            IsNotValidSort if sort is not a member of SortOptions.
            WrongPage if page less than 1.
        """
        utils.is_valid_search_parameters(page, sort_by)

        url = f"{config.api_gallery_url}/search"
        params = {
            "query": query,
            "page": page,
            "sort": sort_by
        }

        resp = await self._get_requests(url, params=params)
        result = resp["result"]
        if result:
            return result
        else:
            raise errors.WrongSearch("Given search is wrong.")

    async def search_by_tag(self, tag_id: int, page: int = 1, sort_by: str = "date") -> List[dict]:
        """Method for search doujins by tag.
        Args:
            :tag_id int: Tag for search doujins.
            :page int: Page, from which we return results.
            :sort_by str: Sort for search (popular or date).

        Returns:
            List of doujins JSON

        Raises:
            IsNotValidSort if sort is not a member of SortOptions.
            WrongPage if page less than 1.
        """
        utils.is_valid_search_by_tag_parameters(tag_id, page, sort_by)

        url = f"{config.api_gallery_url}/tagged"
        params = {
            "tag_id": tag_id,
            "page": page,
            "sort": sort_by
        }

        resp = await self._get_requests(url, params=params)
        result = resp["result"]
        if result:
            return result
        else:
            raise errors.WrongSearch("There is no tag with given tag_id")

    async def get_homepage_doujins(self, page: int) -> List[dict]:
        """Method for getting doujins from.
        Args:
            :page int: Page, from which we get doujins.

        Returns:
            List of doujins JSON

        Raises:
            WrongPage if page less than 1 or page has no content.
        """

        url = f"{config.api_gallery_url}/all"
        params = {
            "page": page
        }

        resp = await self._get_requests(url, params=params)
        result = resp["result"]
        if result:
            return result
        else:
            raise errors.WrongPage("Given page is wrong.")

    async def search_all_by_tags(self, tag_ids: list) -> List[dict]:
        """Method for search doujins by tags.
        Args:
            :tag_ids list: List of tags

        Returns:
            List of doujins JSON

        Raises:
            IsNotValidSort if sort is not a member of SortOptions.
            WrongPage if page less than 1.
        """

        async def get_limit(tag_id: int) -> List[dict]:
            utils.is_valid_search_by_tag_parameters(tag_id, 1, "date")

            url = f"{config.api_gallery_url}/tagged"
            params = {
                "tag_id": tag_id,
                "page": 1,
                "sort_by": "date"
            }

            result = await self._get_requests(url, params=params)
            if result:
                return result["num_pages"]
            else:
                raise errors.WrongTag("There is no tag with given tag_id")


        limits = await asyncio.gather(*[get_limit(tag_id) for tag_id in tag_ids])
        limits = zip(tag_ids, limits)

        data = []

        for args in limits:
            limits  = args[1]
            tag_ids = args[0]
            for i in range(1, limits+1):
                data.append((tag_ids, i))


        pages = await asyncio.gather(*[self.search_by_tag(*args) for args in data])
        return [doujin for page in pages for doujin in page]

