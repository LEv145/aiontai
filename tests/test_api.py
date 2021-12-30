import json
from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock, AsyncMock
from pathlib import Path

from src.api import NHentaiAPI, SortOptions


class TestApi(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.client_session_mosk = AsyncMock()
        self.response_mosk: AsyncMock = (
            self.client_session_mosk.request.return_value
        )

    async def test__request(self) -> None:
        client_session_mosk = self.client_session_mosk
        self.response_mosk.raise_for_status = Mock()

        api = NHentaiAPI(
            client_session=client_session_mosk,
        )

        async with api.request(
            "GET",
            "https://www.gnu.org/",
        ) as response:
            ...  # TODO

    async def test__get_doujin(self) -> None:
        with open(Path("./tests/testdata/doujin.json")) as fp:
            raw_data = json.load(fp)

        self.response_mosk.json.return_value = raw_data

        api = NHentaiAPI(
            client_session=self.client_session_mosk,
        )

        self.assertEqual(
            await api.get_doujin(123),
            raw_data,
        )

    async def test__is_exist(self) -> None:
        with open(Path("./tests/testdata/doujin.json")) as fp:
            raw_data = json.load(fp)

        self.response_mosk.json.return_value = raw_data

        api = NHentaiAPI(
            client_session=self.client_session_mosk,
        )

        self.assertEqual(
            await api.is_exist(123),
            True,
        )

    async def test__get_random_doujin(self):
        with open(Path("./tests/testdata/doujin.json")) as fp:
            raw_data = json.load(fp)

        self.response_mosk.url.human_repr = Mock(
            return_value="https://nhentai.net/g/123/"
        )
        self.response_mosk.json.return_value = raw_data

        api = NHentaiAPI(
            client_session=self.client_session_mosk,
        )

        self.assertEqual(
            await api.get_random_doujin(),
            raw_data,
        )

    async def test__search(self):
        with open(Path("./tests/testdata/doujins.json")) as fp:
            raw_data = json.load(fp)

        self.response_mosk.json.return_value = raw_data

        api = NHentaiAPI(
            client_session=self.client_session_mosk,
        )

        self.assertEqual(
            await api.search(
                query="Omakehon 2005",
                page=1,
                sort_by=SortOptions.DATE,
            ),
            raw_data,
        )

    async def test__search_by_tag(self):
        with open(Path("./tests/testdata/doujins.json")) as fp:
            raw_data = json.load(fp)

        self.response_mosk.json.return_value = raw_data

        api = NHentaiAPI(
            client_session=self.client_session_mosk,
        )

        self.assertEqual(
            await api.search_by_tag(
                tag_id=7752,
                page=1,
                sort_by=SortOptions.DATE,
            ),
            raw_data,
        )

    async def test__get_homepage_doujins(self):
        with open(Path("./tests/testdata/doujins.json")) as fp:
            raw_data = json.load(fp)

        self.response_mosk.json.return_value = raw_data

        api = NHentaiAPI(
            client_session=self.client_session_mosk,
        )

        self.assertEqual(
            await api.get_homepage_doujins(
                page=1
            ),
            raw_data,
        )
