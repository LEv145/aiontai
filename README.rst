Aiontai
=======

Async wrapper for nhentai API


============
Installation
============

.. code:: shell

    $ pip install git+https://github.com/LEv145/aiontai


==========
How to use
==========


Create client

.. code:: python

    import asyncio

    from aiohttp import ClientSession

    from aiontai import (
        NHentaiClient,
        NHentaiAPI,
        Conventer,
    )


    async def main():
        client_object = NHentaiClient(
            api=NHentaiAPI(
                ClientSession(),
            ),
            conventer=Conventer(),
        )

    asyncio.run(main())


Or can use ``injector`` that will create the object itself (Next examples will be using it)

.. code:: python

    import asyncio

    from injector import Injector

    from aiontai import (
        NHentaiClient,
        ClientModule,
    )


    async def main():
        injector = Injector(ClientModule())
        client_object = injector.get(NHentaiClient)

    asyncio.run(main())


Example of using the client

.. code:: python

    async def main():
        injector = Injector(ClientModule())
        client_object = injector.get(NHentaiClient)

        async with client_object as client:  # Will close the session itself
            doujin = await client.get_random_doujin()

            for page in doujin.images:
                print(page.url)

            print(doujin.to_json())

    asyncio.run(main())


Example of using the proxy

.. code:: python

    ...
    from injector import (
        provider,
        Injector,
        Module,
    )
    from aiohttp_proxy import ProxyConnector  # pip install aiohttp_proxy
    ...

    class AiohttpProxyModule(Module):
        def __init__(self, proxi_url: str) -> None:
            self._proxi_url = proxi_url

        @provider
        def provide_client_session(self) -> ClientSession:
            connector = ProxyConnector.from_url(self._proxi_url)
            return ClientSession(connector=connector)


    async def main():
        injector = Injector(
            modules=[
                ClientModule(),
                AiohttpProxyModule("http://user:password@127.0.0.1:1080"),
            ],
        )
        client_object = injector.get(NHentaiClient)

    asyncio.run(main())


Example of using the Low level api

.. code:: python

    async def main():
        injector = Injector(ClientModule())
        client_object = injector.get(NHentaiAPI)
        async with client_object as client:
            doujin = await client.get_random_doujin()  # Return: Dict[str, Any]
                                                       # from api without loss of information

            print(doujin)


    asyncio.run(main())
