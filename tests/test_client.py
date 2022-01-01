import json
from pathlib import Path
from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock, AsyncMock

from src.client import NHentaiClient


class TestClient(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.client = NHentaiClient(
            api=AsyncMock(),
        )

    async def test__get_doujin(self):
        with open(Path("./tests/testdata/doujin.json")) as fp:
            raw_data = json.load(fp)

        self.client.api.get_doujin.return_value = raw_data

        print(
            await self.client.get_doujin(123)
        )
