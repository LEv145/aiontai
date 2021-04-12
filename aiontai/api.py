"""Impementation of NHentaiAPI."""

from enum import Enum
from typing import List, Optional
import aiohttp
from . import errors, utils
from .config import config


class SortOptions(Enum):
    """Enumeration for sort options."""

    DATE = "date"
    POPULARITY = "popular"


class NHentaiAPI:
    """Class that represents a nhentai API."""

    def __init__(self, proxy: Optional[str] = None):
        self.proxy = proxy

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

        async with aiohttp.ClientSession() as session:
            async with session.get(url, proxy=self.proxy) as response:
                if response.ok:
                    json = await response.json()
                    return json
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
        parameters = {
            "query": query,
            "page": page,
            "sort": sort_by
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=parameters, proxy=self.proxy) as response:
                results = await response.json()
                return list(results["result"])

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
        parameters = {
            "tag_id": tag_id,
            "page": page,
            "sort": sort_by
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=parameters, proxy=self.proxy) as response:
                    results = await response.json()
                    return list(results["result"])

        except KeyError as exception:
            raise errors.WrongTag("There is no tag with given tag_id") from exception

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
        parameters = {
            "page": page
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=parameters, proxy=self.proxy) as response:
                results = await response.json()
                if not results["result"]:
                    raise errors.WrongPage("Given page is wrong.")
                else:
                    return list(results["result"])

