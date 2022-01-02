from unittest import IsolatedAsyncioTestCase

from injector import Injector
from src.client import NHentaiClient

from src.modules import ClientModule


class TestModules(IsolatedAsyncioTestCase):
    async def test__client_module(self):
        injector = Injector(ClientModule)
        client = injector.get(NHentaiClient)

        self.assertIsInstance(
            client,
            NHentaiClient,
        )
        await client.close()
