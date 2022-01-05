"""Low level API."""

import re
from types import TracebackType
from typing import (
    Any,
    Dict,
    AsyncIterator,
    Type,
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
    """NHentai low level API."""

    def __init__(self, client_session: ClientSession):
        """
        Init object.

        Args:
            client_session (ClientSession): Aiohttp client session.
        """
        self.client_session = client_session

    async def __aenter__(self) -> "NHentaiAPI":
        """Return self from async context manager."""
        return self

    async def __aexit__(
        self,
        _exception_type: Type[BaseException],
        _exception: BaseException,
        _traceback: TracebackType,
    ) -> None:
        """Close object from async context manager."""
        await self.close()

    async def close(self):
        """Close object."""
        await self.client_session.close()

    async def get_doujin(self, doujin_id: int) -> Dict[str, Any]:
        """
        Get raw doujin by id.

        Args:
            doujin_id (int): ID of doujin.

        Raises:
            DoujinDoesNotExistError: If the doujin does not exit.
            ClientResponseError: Error from response.

        Returns:
            Dict[str, Any]: Raw doujin from responce.
        """
        url = f"https://nhentai.net/api/gallery/{doujin_id}"

        try:
            async with self._request("GET", url=url) as response:
                json = await response.json()
        except ClientResponseError as error:
            if error.status == 404:
                raise DoujinDoesNotExistError("That doujin does not exist.") from error
            else:
                raise error

        return json

    async def is_exist(self, doujin_id: int) -> bool:
        """
        Check if the doujin exists.

        Args:
            doujin_id (int): ID of doujin.

        Returns:
            bool: The doujin is exists.
        """
        try:
            await self.get_doujin(doujin_id)
            return True
        except DoujinDoesNotExistError:
            return False

    async def get_random_doujin(self) -> Dict[str, Any]:
        """
        Get random raw doujin.

        Returns:
            Dict[str, Any]: Raw doujin from responce.
        """
        url = "https://nhentai.net/random/"

        async with self._request("GET", url=url) as response:
            url = response.url.human_repr()
            result = re.match(r"https?://nhentai\.net/g/(\d+)/?", url)

            assert result is not None
            doujin_id = int(result.group(1))

        return (
            await self.get_doujin(doujin_id)
        )

    async def search(
        self,
        query: str,
        page: int = 1,
        sort_by: SortOptions = SortOptions.DATE,
    ) -> Dict[str, Any]:
        """
        Search raw doujins result.

        Args:
            query (str): Query for search doujins.
            page (int, optional): Number of page from which we return the results.
                Defaults to 1.
            sort_by (SortOptions, optional): Sort options for search.
                Defaults to SortOptions.DATE.

        Raises:
            WrongPageError: If number of page is invalid.
            EmptyAPIResultError: If api result is empty.

        Returns:
            Dict[str, Any]: Raw doujins result from responce.
        """
        if page < 1:
            raise WrongPageError("Page can not be less than 1")

        url = "https://nhentai.net/api/galleries/search"
        params = {
            "query": query,
            "page": page,
            "sort": sort_by.value,
        }

        async with self._request("GET", url, params=params) as responce:
            json = await responce.json()

        result = json["result"]
        if result:
            return json
        else:
            raise EmptyAPIResultError()

    async def search_by_tag(
        self,
        tag_id: int,
        page: int = 1,
        sort_by: SortOptions = SortOptions.DATE,
    ) -> Dict[str, Any]:
        """
        Search raw doujins result by tag.

        Args:
            tag_id (int): Tag ID for search.
            page (int, optional): Number of page from which we return the results.
                Defaults to 1.
            sort_by (SortOptions, optional): Sort options for search.
                Defaults to SortOptions.DATE.

        Raises:
            WrongPageError: If number of page is invalid.
            WrongTagError: If tag ID is invalid.
            EmptyAPIResultError: If api result is empty.

        Returns:
            Dict[str, Any]: Raw doujins result from responce.
        """
        if page < 1:
            raise WrongPageError("Page can not be less than 1")
        elif tag_id < 1:
            raise WrongTagError("Tag id can not be less than 1")

        url = "https://nhentai.net/api/galleries/tagged"

        params = {
            "tag_id": tag_id,
            "page": page,
            "sort": sort_by,
        }

        async with self._request("GET", url, params=params) as responce:
            json = await responce.json()

        result = json["result"]
        if result:
            return json
        else:
            raise EmptyAPIResultError()

    async def get_homepage_doujins(
        self,
        page: int = 1,
    ) -> Dict[str, Any]:
        """
        Get raw doujins from homepage.

        Args:
            page (int, optional): Number of page from which we return the results.
                Defaults to 1.

        Raises:
            EmptyAPIResultError: If api result is empty.

        Returns:
            Dict[str, Any]: Raw doujins result from responce.
        """
        url = "https://nhentai.net/api/galleries/all"

        params = {
            "page": page,
        }

        async with self._request("GET", url, params=params) as responce:
            json = await responce.json()

        result = json["result"]
        if result:
            return json
        else:
            raise EmptyAPIResultError()

    @asynccontextmanager
    async def _request(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> AsyncIterator[ClientResponse]:
        response = await self.client_session.request(
            method,
            url,
            **kwargs,
        )
        response.raise_for_status()

        try:
            yield response
        finally:
            await response.__aexit__(None, None, None)

# TODO
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


class WrongPageError(Exception):
    """Wrong page."""


class WrongSearchError(Exception):
    """Wrong search."""


class WrongTagError(Exception):
    """Wrong tag."""


class DoujinDoesNotExistError(Exception):
    """Doujin does noe exist."""


class EmptyAPIResultError(Exception):
    """API result is empty."""
