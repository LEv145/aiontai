import json
from pathlib import Path
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock

from src.client import (
    NHentaiClient,
    SortOptions,
)
from src.models import (
    Doujin,
    DoujinsResult,
)


class TestClient(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.client = NHentaiClient(
            api=AsyncMock(),
        )

    async def test__get_doujin(self):
        with open(Path("./tests/testdata/doujin.json")) as fp:
            raw_data = json.load(fp)

        self.client.api.get_doujin.return_value = raw_data

        result = await self.client.get_doujin(123)

        self.assertIsInstance(
            result,
            Doujin,
        )

    async def test__is_exist(self):
        self.client.api.is_exist.return_value = False

        result = await self.client.is_exist(-1)

        self.assertEqual(
            result,
            False,
        )

        self.client.api.is_exist.return_value = True

        result = await self.client.is_exist(123)

        self.assertEqual(
            result,
            True,
        )

    async def test__get_random_doujin(self):
        with open(Path("./tests/testdata/doujin.json")) as fp:
            raw_data = json.load(fp)

        self.client.api.get_random_doujin.return_value = raw_data

        result = await self.client.get_random_doujin()

        self.assertIsInstance(
            result,
            Doujin,
        )

    async def test__search(self):
        with open(Path("./tests/testdata/doujins_result.json")) as fp:
            raw_data = json.load(fp)

        self.client.api.search.return_value = raw_data

        result = await self.client.search(
            query="Omakehon 2005",
            page=1,
            sort_by=SortOptions.DATE,
        )

        self.assertIsInstance(
            result,
            DoujinsResult,
        )

    async def test__search_by_tag(self):
        with open(Path("./tests/testdata/doujins_result.json")) as fp:
            raw_data = json.load(fp)

        self.client.api.search_by_tag.return_value = raw_data

        result = await self.client.search_by_tag(
            tag_id=7752,
            page=1,
            sort_by=SortOptions.DATE,
        )

        self.assertIsInstance(
            result,
            DoujinsResult,
        )

    async def test__get_homepage_doujins(self):
        with open(Path("./tests/testdata/doujins_result.json")) as fp:
            raw_data = json.load(fp)

        self.client.api.get_homepage_doujins.return_value = raw_data

        result = await self.client.get_homepage_doujins(
            page=1,
        )

        self.assertIsInstance(
            result,
            DoujinsResult,
        )
