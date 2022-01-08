import json
from pathlib import Path
from unittest import IsolatedAsyncioTestCase
from unittest.mock import (
    AsyncMock,
    Mock,
)

from aiohttp import ClientResponseError

from aiontai.api import (
    DoujinDoesNotExistError,
    EmptyAPIResultError,
    HTTPError,
    NHentaiAPI,
    SortOptions,
)


class TestApi(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.api = NHentaiAPI(
            client_session=AsyncMock(),
        )
        self.response_mosk: AsyncMock = (
            self.api.client_session.request.return_value
        )  # response_mosk alias

    async def test__context_manager(self) -> None:
        async with self.api as client:
            self.assertIsInstance(
                client,
                type(self.api),
            )

    async def test__request(self) -> None:
        # Normal test
        self.response_mosk.status = 200

        async with self.api._request("GET", "https://nhentai.net/"):
            ...

    async def test__get_doujin(self) -> None:
        # Normal test
        with open(Path("./tests/testdata/doujin.json")) as fp:
            raw_data = json.load(fp)

        self.response_mosk.json.return_value = raw_data
        self.response_mosk.status = 200

        self.assertEqual(
            await self.api.get_doujin(123),
            raw_data,
        )

        # Test error: DoujinDoesNotExistError
        self.response_mosk.status = 404

        with self.assertRaises(DoujinDoesNotExistError):
            self.assertEqual(
                await self.api.get_doujin(123),
                raw_data,
            )

        # Test error: HTTPError
        self.response_mosk.status = 500

        with self.assertRaises(HTTPError):
            self.assertEqual(
                await self.api.get_doujin(123),
                raw_data,
            )

    async def test__is_exist(self) -> None:
        # Normal test
        with open(Path("./tests/testdata/doujin.json")) as fp:
            raw_data = json.load(fp)

        self.response_mosk.json.return_value = raw_data
        self.response_mosk.status = 200

        self.assertEqual(
            await self.api.is_exist(123),
            True,
        )

        # Test error: DoujinDoesNotExistError
        self.response_mosk.status = 404

        self.assertEqual(
            await self.api.is_exist(123),
            False,
        )

    async def test__get_random_doujin(self) -> None:
        # Normal test
        with open(Path("./tests/testdata/doujin.json")) as fp:
            raw_data = json.load(fp)

        self.response_mosk.url.human_repr = Mock(
            return_value="https://nhentai.net/g/123/",
        )
        self.response_mosk.json.return_value = raw_data
        self.response_mosk.status = 200

        self.assertEqual(
            await self.api.get_random_doujin(),
            raw_data,
        )

    async def test__search(self) -> None:
        # Normal test
        with open(Path("./tests/testdata/doujins_result.json")) as fp:
            raw_data = json.load(fp)

        self.response_mosk.json.return_value = raw_data
        self.response_mosk.status = 200

        self.assertEqual(
            await self.api.search(
                query="Omakehon 2005",
                page=1,
                sort_by=SortOptions.DATE,
            ),
            raw_data,
        )

        # Test error: ValueError
        with self.assertRaises(ValueError):
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

    async def test__search_by_tag(self) -> None:
        # Normal test
        with open(Path("./tests/testdata/doujins_result.json")) as fp:
            raw_data = json.load(fp)

        self.response_mosk.json.return_value = raw_data
        self.response_mosk.status = 200

        self.assertEqual(
            await self.api.search_by_tag(
                tag_id=7752,
                page=1,
                sort_by=SortOptions.DATE,
            ),
            raw_data,
        )

        # Test error: ValueError
        with self.assertRaises(ValueError):
            await self.api.search_by_tag(
                tag_id=7752,
                page=-1,
                sort_by=SortOptions.DATE,
            )

        with self.assertRaises(ValueError):
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

    async def test__get_homepage_doujins(self) -> None:
        with open(Path("./tests/testdata/doujins_result.json")) as fp:
            raw_data = json.load(fp)

        self.response_mosk.json.return_value = raw_data
        self.response_mosk.status = 200

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
