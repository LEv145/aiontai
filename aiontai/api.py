import enum
from typing import List
import aiohttp
from aiontai import errors, utils
from aiontai.config import config


class SortOptions(enum.Enum):
    date = "date"
    popularity = "popular"


class NHentaiAPI:
    """Class that represents a nhentai API.

    TODO: Получить n-nую doujin с home page
    TODO: Поиск doujins по тегу
    """

    async def get_doujin(self, id: int) -> dict:
        """Method for getting doujin by id.
        Args:
            :id int: Doujin's id, which we get.

        Returns:
            JSON of doujin.

        Raises:
            DoujinDoesNotExist if doujin was not found.

        Usage:
            >>> api = NHentaiAPI()
            >>> api.get_doujin(1)
            {...}
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{config.api_url}/gallery/{id}") as response:
                if response.ok:
                    json: dict = await response.json()
                    return json
                else:
                    raise errors.DoujinDoesNotExist("That doujin does not exist.")

    async def is_exist(self, id: int) -> bool:
        """Method for checking does doujin exist.
        Args:
            :id int: Doujin's id, which we check.

        Returns:
            True if doujin is exist, False if doujin is not exist.

        Usage:
            >>> api = NHentaiAPI()
            >>> api.is_exist(1)
            True
        """
        try:
            await self.get_doujin(id)
            return True
        except errors.DoujinDoesNotExist:
            return False

    async def get_random_doujin(self) -> dict:
        """Method for getting random doujin.
        Returns:
            JSON of random doujin.

        Usage:
            >>> api = NHentaiAPI()
            >>> api.random_doujin()
            {...}
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{config.base_url}/random/") as response:
                url = response.url.human_repr()
                id = int(utils.extract_digits(url))
                return await self.get_doujin(id)

    async def search(self, query: str, page: int = 1, sort_by: str = "date") -> List[dict]:
        """Method for getting doujin by id.
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
            >>> api = NHentaiAPI()
            >>> api.search("anime", 2, "popular")
            [{...}, ...]
        """
        utils.is_valid_search_parameters(page, sort_by)

        async with aiohttp.ClientSession() as session:
            parameters = {
                "query": query,
                "page": page,
                "sort": sort_by
            }
            async with session.get(f"{config.api_gallery_url}/search", params=parameters) as response:
                results = await response.json()
                return [result for result in results["result"]]

    async def search_by_tag(self, tag_id: int, page: int = 1, sort_by: str = "date") -> List[dict]:
        """Method for getting doujin by id.
        Args:
            :tag id: Tag for search doujins.
            :page int: Page, from which we return results.
            :sort_by str: Sort for search.

        Returns:
            List of doujins JSON

        Raises:
            IsNotValidSort if sort is not a member of SortOptions.
            WrongPage if page less than 1.

        Usage:
            >>> api = NHentaiAPI()
            >>> api.search_by_tag(1, 2, "popular")
            [{...}, ...]
        """
        utils.is_valid_search_by_tag_parameters(tag_id, page, sort_by)

        async with aiohttp.ClientSession() as session:
            parameters = {
                "tag_id": tag_id,
                "page": page,
                "sort": sort_by
            }
            try:
                async with session.get(f"{config.api_gallery_url}/tagged", params=parameters) as response:
                    results = await response.json()
                    return [result for result in results["result"]]
            except KeyError:
                raise errors.WrongTag("There is no tag with given tag_id")

    async def get_doujins_from_homepage(self, page: int) -> List[dict]:
        async with aiohttp.ClientSession() as session:
            parameters = {
                "page": page
            }
            async with session.get(f"{config.api_gallery_url}/all", params=parameters) as response:
                results = await response.json()
                if not results["result"]:
                    raise errors.WrongPage("Given page is wrong.")
                else:
                    return [result for result in results["result"]]
