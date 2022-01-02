"""Impementation of NHentaiAPI."""
import re
from typing import (
    Any,
    Dict,
    AsyncIterator,
    Union,
)
from enum import Enum
from contextlib import asynccontextmanager

from aiohttp import (
    ClientResponseError,
    ClientSession,
    ClientResponse,
)


class SortOptions(Enum):
    """Enumeration for sort options."""

    DATE = "date"
    POPULARITY = "popular"


class NHentaiAPI():
    """Class that represents a nhentai API."""
    def __init__(self, client_session: ClientSession):
        self.client_session = client_session

    async def close(self):
        await self.client_session.close()

    @asynccontextmanager
    async def request(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> AsyncIterator[ClientResponse]:
        response = await self.client_session.request(
            method,
            url,
            **kwargs,
        )  # TODO?: Context manager
        response.raise_for_status()

        try:
            yield response
        finally:
            await response.release()

    async def get_doujin(self, doujin_id: Union[int, str]) -> Dict[str, Any]:
        """Method for getting doujin by id.
        Args:
            :doujin_id int: Doujin's id, which we get.

        Returns:
            Doujin json.

        Raises:
            DoujinDoesNotExist if doujin was not found.
        """
        url = f"https://nhentai.net/api/gallery/{doujin_id}"

        try:
            async with self.request("GET", url=url) as response:
                json = await response.json()
        except ClientResponseError as error:  # TODO
            if error.status == 404:
                raise DoujinDoesNotExist("That doujin does not exist.") from error
            else:
                raise error

        return json

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
        except DoujinDoesNotExist:
            return False

    async def get_random_doujin(self) -> Dict[str, Any]:
        """Method for getting random doujin.
        Returns:
            Doujin model.
        """
        url = "https://nhentai.net/random/"

        async with self.request("GET", url=url) as response:
            url = response.url.human_repr()
            result = re.match(r"https?://nhentai\.net/g/(\d+)/?", url)

            assert result is not None
            doujin_id = result.group(1)

        return (
            await self.get_doujin(doujin_id)
        )

    async def search(
        self,
        query: str,
        page: int = 1,
        sort_by: SortOptions = SortOptions.DATE,
    ) -> Dict[str, Any]:
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
        if page < 1:
            raise WrongPage("Page can not be less than 1")

        url = "https://nhentai.net/api/galleries/search"
        params = {
            "query": query,
            "page": page,
            "sort": sort_by.value,
        }

        async with self.request("GET", url, params=params) as responce:
            json = await responce.json()

        result = json["result"]
        if result:
            return json
        else:
            raise DoujinDoesNotExist()

    async def search_by_tag(
        self,
        tag_id: int,
        page: int = 1,
        sort_by: SortOptions = SortOptions.DATE,
    ) -> Dict[str, Any]:
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
        if page < 1:
            raise WrongPage("Page can not be less than 1")
        elif tag_id < 1:  # TODO: Better check
            raise WrongTag("Tag id can not be less than 1")

        url = "https://nhentai.net/api/galleries/tagged"

        params = {
            "tag_id": tag_id,
            "page": page,
            "sort": sort_by,
        }

        async with self.request("GET", url, params=params) as responce:
            json = await responce.json()

        result = json["result"]
        if result:
            return json
        else:
            raise DoujinDoesNotExist()

    async def get_homepage_doujins(
        self,
        page: int
    ) -> Dict[str, Any]:
        """Method for getting doujins from.
        Args:
            :page int: Page, from which we get doujins.

        Returns:
            List of doujins JSON

        Raises:
            WrongPage if page less than 1 or page has no content.
        """

        url = "https://nhentai.net/api/galleries/all"

        params = {
            "page": page
        }

        async with self.request("GET", url, params=params) as responce:
            json = await responce.json()

        result = json["result"]
        if result:
            return json
        else:
            raise DoujinDoesNotExist()


# async def search_all_by_tags(self, tag_ids: list) -> List[dict]:
#     """Method for search doujins by tags.
#     Args:
#         :tag_ids list: List of tags

#     Returns:
#         List of doujins JSON

#     Raises:
#         IsNotValidSort if sort is not a member of SortOptions.
#         WrongPage if page less than 1.
#     """

#     async def get_limit(tag_id: int) -> List[dict]:
#         utils.is_valid_search_by_tag_parameters(tag_id, 1, "date")

#         url = f"{config.api_gallery_url}/tagged"
#         params = {
#             "tag_id": tag_id,
#             "page": 1,
#             "sort_by": "date"
#         }

#         result = await self._get_requests(url, params=params)
#         if result:
#             return result["num_pages"]
#         else:
#             raise errors.WrongTag("There is no tag with given tag_id")


#     limits = await asyncio.gather(*[get_limit(tag_id) for tag_id in tag_ids])
#     limits = zip(tag_ids, limits)

#     data = []

#     for args in limits:
#         limits  = args[1]
#         tag_ids = args[0]
#         for i in range(1, limits+1):
#             data.append((tag_ids, i))


#     pages = await asyncio.gather(*[self.search_by_tag(*args) for args in data])
#     return [doujin for page in pages for doujin in page]


class WrongPage(Exception):
    """Exception for wrong page."""


class WrongSearch(Exception):
    """Exception for wrong search."""


class WrongTag(Exception):
    """Exception for wrong tag."""


class DoujinDoesNotExist(Exception):
    """Exception for not existing doujin."""