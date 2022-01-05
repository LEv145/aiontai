import json
from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock, AsyncMock
from pathlib import Path

from aiohttp import ClientResponseError

from aiontai.api import (
    EmptyAPIResultError,
    NHentaiAPI,
    DoujinDoesNotExistError,
    SortOptions,
    WrongPageError,
    WrongTagError,
)


class TestApi(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.api = NHentaiAPI(
            client_session=AsyncMock(),
        )
        self.response_mosk: AsyncMock = (
            self.api.client_session.request.return_value
        )  # response_mosk alias

    async def test__context_manager(self):
        async with self.api as client:
            self.assertIsInstance(
                client,
                type(self.api),
            )

    async def test__request(self) -> None:
        # Normal test
        self.response_mosk.raise_for_status = Mock()

        async with self.api._request("GET", "https://nhentai.net/"):
            ...

    async def test__get_doujin(self) -> None:
        # Normal test
        with open(Path("./tests/testdata/doujin.json")) as fp:
            raw_data = json.load(fp)

        self.response_mosk.json.return_value = raw_data
        self.response_mosk.raise_for_status = Mock()

        self.assertEqual(
            await self.api.get_doujin(123),
            raw_data,
        )

        # Test error: DoujinDoesNotExistError
        self.response_mosk.raise_for_status.side_effect = ClientResponseError(
            request_info=Mock(),
            history=Mock(),
            status=404,
        )

        with self.assertRaises(DoujinDoesNotExistError):
            self.assertEqual(
                await self.api.get_doujin(123),
                raw_data,
            )

        # Test error: ClientResponseError
        self.response_mosk.raise_for_status.side_effect = ClientResponseError(
            request_info=Mock(),
            history=Mock(),
            status=201,
        )

        with self.assertRaises(ClientResponseError):
            self.assertEqual(
                await self.api.get_doujin(123),
                raw_data,
            )

    async def test__is_exist(self) -> None:
        # Normal test
        with open(Path("./tests/testdata/doujin.json")) as fp:
            raw_data = json.load(fp)

        self.response_mosk.json.return_value = raw_data
        self.response_mosk.raise_for_status = Mock()

        self.assertEqual(
            await self.api.is_exist(123),
            True,
        )

        # Test error: DoujinDoesNotExistError
        self.response_mosk.raise_for_status.side_effect = ClientResponseError(
            request_info=Mock(),
            history=Mock(),
            status=404,
        )

        self.assertEqual(
            await self.api.is_exist(123),
            False,
        )

    async def test__get_random_doujin(self):
        # Normal test
        with open(Path("./tests/testdata/doujin.json")) as fp:
            raw_data = json.load(fp)

        self.response_mosk.url.human_repr = Mock(
            return_value="https://nhentai.net/g/123/",
        )
        self.response_mosk.json.return_value = raw_data
        self.response_mosk.raise_for_status = Mock()

        self.assertEqual(
            await self.api.get_random_doujin(),
            raw_data,
        )

    async def test__search(self):
        # Normal test
        with open(Path("./tests/testdata/doujins_result.json")) as fp:
            raw_data = json.load(fp)

        self.response_mosk.json.return_value = raw_data
        self.response_mosk.raise_for_status = Mock()

        self.assertEqual(
            await self.api.search(
                query="Omakehon 2005",
                page=1,
                sort_by=SortOptions.DATE,
            ),
            raw_data,
        )

        # Test error: WrongPageError
        with self.assertRaises(WrongPageError):
            await self.api.search(
                query="Omakehon 2005",
                page=-1,
                sort_by=SortOptions.DATE,
            )

        # Test error: EmptyAPIResultError
        self.response_mosk.json.return_value = {
            "result": [],
            "num_pages": 15181,
            "per_page": 25,
        }

        with self.assertRaises(EmptyAPIResultError):
            await self.api.search(
                query="Omakehon 2005",
                page=1,
                sort_by=SortOptions.DATE,
            )

    async def test__search_by_tag(self):
        # Normal test
        with open(Path("./tests/testdata/doujins_result.json")) as fp:
            raw_data = json.load(fp)

        self.response_mosk.json.return_value = raw_data
        self.response_mosk.raise_for_status = Mock()

        self.assertEqual(
            await self.api.search_by_tag(
                tag_id=7752,
                page=1,
                sort_by=SortOptions.DATE,
            ),
            raw_data,
        )

        # Test error: WrongPageError
        with self.assertRaises(WrongPageError):
            await self.api.search_by_tag(
                tag_id=7752,
                page=-1,
                sort_by=SortOptions.DATE,
            )

        # Test error: WrongTagError
        with self.assertRaises(WrongTagError):
            await self.api.search_by_tag(
                tag_id=-1,
                page=1,
                sort_by=SortOptions.DATE,
            )

        # Test error: EmptyAPIResultError
        self.response_mosk.json.return_value = {
            "result": [],
            "num_pages": 15181,
            "per_page": 25,
        }

        with self.assertRaises(EmptyAPIResultError):
            await self.api.search_by_tag(
                tag_id=66666,
                page=1,
                sort_by=SortOptions.DATE,
            )

    async def test__get_homepage_doujins(self):
        with open(Path("./tests/testdata/doujins_result.json")) as fp:
            raw_data = json.load(fp)

        self.response_mosk.json.return_value = raw_data
        self.response_mosk.raise_for_status = Mock()

        self.assertEqual(
            await self.api.get_homepage_doujins(
                page=1,
            ),
            raw_data,
        )

        # Test error: EmptyAPIResultError
        self.response_mosk.json.return_value = {
            "result": [],
            "num_pages": 15181,
            "per_page": 25,
        }

        with self.assertRaises(EmptyAPIResultError):
            await self.api.get_homepage_doujins(
                page=66666,
            )
