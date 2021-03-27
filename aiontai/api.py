import aiohttp
from aiontai import errors
from aiontai.config import config


class NHentaiAPI:
    """Class that represents a nhentai API.

    TODO: Получение рандомного комикса
    TODO: Получение doujin по id
    TODO: Получить n-nую doujin с home page
    TODO: Поиск doujins по тегу
    TODO: Поиск doujins по запросу
    """

    async def get_doujin(self, id: int) -> dict:
        """Method for getting doujin by id.
        Args:
            :id int: Doujin's id, which we get.

        Returns:
            JSON of doujin.

        Raises:
            DoujinDoesNotExist if doujin was not found.

        Usage:
            >>> api = NHentaiAPI()
            >>> api.get_doujin(1)
            {...}
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{config.api_url}/gallery/{id}") as response:
                if response.ok:
                    json: dict = await response.json()
                    return json
                else:
                    raise errors.DoujinDoesNotExist("That doujin does not exist.")

    async def is_exist(self, id: int) -> bool:
        """Method for checking does doujin exist.
        Args:
            :id int: Doujin's id, which we check.

        Returns:
            True if doujin is exist, False if doujin is not exist.

        Usage:
            >>> api = NHentaiAPI()
            >>> api.is_exist(1)
            True
        """
        try:
            await self.get_doujin(id)
            return True
        except errors.DoujinDoesNotExist:
            return False
