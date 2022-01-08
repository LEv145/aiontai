"""Low level API."""

import re
from contextlib import asynccontextmanager
from enum import Enum
from types import TracebackType
from typing import (
    Any,
    AsyncIterator,
    Dict,
    Optional,
    Type,
    TypeVar,
)

from aiohttp import (
    ClientResponse,
    ClientSession,
)


class SortOptions(Enum):
    """Enumeration for sort options."""

    DATE = "date"
    POPULARITY = "popular"


class NHentaiAPI():
    """NHentai low level API."""
    NHentaiAPIType = TypeVar("NHentaiAPIType", bound="NHentaiAPI")

    def __init__(self, client_session: ClientSession):
        """
        Init object.

        Args:
            client_session: Aiohttp client session.
        """
        self.client_session = client_session

    async def __aenter__(self: NHentaiAPIType) -> NHentaiAPIType:
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
        await self.client_session.close()

    async def get_doujin(self, doujin_id: int) -> Dict[str, Any]:
        """
        Get doujin raw data by ID.

        Args:
            doujin_id: ID of doujin.

        Returns:
            Doujin raw data from responce.

        Raises:
            DoujinDoesNotExistError: If doujin does not exit.
            HTTPError: Error from response.
        """
        url = f"https://nhentai.net/api/gallery/{doujin_id}"

        try:
            async with self._request("GET", url=url) as response:
                json: Dict[str, Any] = await response.json()
        except HTTPError as error:
            if error.responce.status == 404:
                raise DoujinDoesNotExistError(
                    "That doujin does not exist.",
                ) from error
            else:
                raise error

        return json

    async def is_exist(self, doujin_id: int) -> bool:
        """
        Check if doujin exists.

        Args:
            doujin_id: ID of doujin.

        Returns:
            Doujin is exists.

        Raises:
            HTTPError: Error from response.
        """
        try:
            await self.get_doujin(doujin_id)
            return True
        except DoujinDoesNotExistError:
            return False

    async def get_random_doujin(self) -> Dict[str, Any]:
        """
        Get random doujin raw data.

        Returns:
            Doujin raw data from responce.

        Raises:
            HTTPError: Error from response.
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
        Search doujins raw data result.

        Args:
            query: Query for search doujins.
            page: Number of page from which we return results.
                Defaults to 1.
            sort_by: Sort options for search.
                Defaults to SortOptions.DATE.

        Returns:
            Doujins raw data result from responce.

        Raises:
            ValueError: If number of page is invalid.
            EmptyAPIResultError: If api result is empty.
            HTTPError: Error from response.
        """
        if page < 1:
            raise ValueError("Page can not be less than 1")

        url = "https://nhentai.net/api/galleries/search"
        params = {
            "query": query,
            "page": page,
            "sort": sort_by.value,
        }

        async with self._request("GET", url, params=params) as responce:
            json: Dict[str, Any] = await responce.json()

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
        Search doujins raw data result by tag.

        Args:
            tag_id: Tag ID for search.
            page: Number of page from which we return results.
                Defaults to 1.
            sort_by: Sort options for search.
                Defaults to SortOptions.DATE.

        Returns:
            Doujins raw data result from responce.

        Raises:
            ValueError: If number of page is invalid or tag ID is invalid.
            EmptyAPIResultError: If api result is empty.
            HTTPError: Error from response.
        """
        if page < 1:
            raise ValueError("Page can not be less than 1")
        elif tag_id < 1:
            raise ValueError("Tag id can not be less than 1")

        url = "https://nhentai.net/api/galleries/tagged"

        params = {
            "tag_id": tag_id,
            "page": page,
            "sort": sort_by,
        }

        async with self._request("GET", url, params=params) as responce:
            json: Dict[str, Any] = await responce.json()

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
        Get doujins raw data from homepage.

        Args:
            page: Number of page from which we return results.
                Defaults to 1.

        Returns:
            Doujins raw data result from responce.

        Raises:
            EmptyAPIResultError: If api result is empty.
            HTTPError: Error from response.
        """
        url = "https://nhentai.net/api/galleries/all"

        params = {
            "page": page,
        }

        async with self._request("GET", url, params=params) as responce:
            json: Dict[str, Any] = await responce.json()

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

        if response.status >= 400:
            response.release()
            raise HTTPError(response=response)

        try:
            yield response
        finally:
            await response.__aexit__(None, None, None)


class NHentaiError(Exception):
    """Base NHentai api error."""


class HTTPError(NHentaiError):
    """
    Error from responce.

    Attributes:
        responce: Responce object.
        message: Message about error.
    """

    def __init__(
        self,
        response: ClientResponse,
        message: Optional[str] = None,
    ) -> None:
        super().__init__(message)

        self.responce = response


class DoujinDoesNotExistError(NHentaiError):
    """Doujin does noe exist."""


class EmptyAPIResultError(NHentaiError):
    """API result is empty."""
