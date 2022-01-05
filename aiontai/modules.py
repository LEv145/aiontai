"""Modules for automatic dependencies."""

from aiohttp import ClientSession
from injector import (
    Module,
    provider,
)

from .api import NHentaiAPI
from .client import NHentaiClient
from .converter import Conventer


class ClientModule(Module):
    """Module for automatic dependencies."""

    @provider
    def provide_client(self, api: NHentaiAPI) -> NHentaiClient:
        """Provide `NHentaiClient`."""
        return NHentaiClient(
            api=api,
            conventer=Conventer(),
        )

    @provider
    def provide_api(self, client_session: ClientSession) -> NHentaiAPI:
        """Provide `NHentaiAPI`."""
        return NHentaiAPI(
            client_session=client_session,
        )

    @provider
    def provide_client_session(self) -> ClientSession:
        """Provide `ClientSession`."""
        return ClientSession()
