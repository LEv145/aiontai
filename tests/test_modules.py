from unittest import IsolatedAsyncioTestCase

from injector import Injector

from aiontai.client import NHentaiClient
from aiontai.modules import ClientModule


class TestModules(IsolatedAsyncioTestCase):
    async def test__client_module(self) -> None:
        injector = Injector(ClientModule)
        client = injector.get(NHentaiClient)

        self.assertIsInstance(
            client,
            NHentaiClient,
        )
        await client.close()
