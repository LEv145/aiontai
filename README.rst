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

Init client

.. code:: python

    import asyncio

    from aiohttp import ClientSession

    from aiontai import (
        NHentaiClient,
        NHentaiAPI,
        Conventer,
    )
    ...

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
    ...

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

            for page in doujin.pages:
                print(page.url)

            print(doujin.to_json())

    asyncio.run(main())


Example of using the proxy

.. code:: python

    ...
    from aiohttp_proxy import ProxyConnector  # pip install aiohttp_proxy
    ...

    async def main():
        injector = Injector(
            modules=[
                ClientModule(),
                AiohttpProxyModule("http://user:password@127.0.0.1:1080"),
            ],
        )
        client_object = injector.get(NHentaiClient)

    asyncio.run(main())