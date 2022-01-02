from aiohttp import ClientSession
from injector import (
    singleton,
    provider,
    Module,
)

from .client import NHentaiClient
from .api import NHentaiAPI


class ClientModule(Module):
    @provider
    def provide_client(self, api: NHentaiAPI) -> NHentaiClient:
        return NHentaiClient(
            api=api,
        )

    @singleton
    @provider
    def provide_api(self, client_session: ClientSession) -> NHentaiAPI:
        return NHentaiAPI(
            client_session=client_session,
        )

    @provider
    def provide_client_session(self) -> ClientSession:
        return ClientSession(trust_env=True)
