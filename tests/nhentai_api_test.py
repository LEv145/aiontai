import os
import site
import asyncio
site.addsitedir(os.getcwd())

import pytest
from aiontai import api, errors

@pytest.mark.asyncio
async def test_get_doujin():
    nhentai_api = api.NHentaiAPI()
    doujin = await nhentai_api.get_doujin(1)
    assert doujin


@pytest.mark.asyncio
async def test_get_doujin_error():
    nhentai_api = api.NHentaiAPI()
    with pytest.raises(errors.DoujinDoesNotExist):
        await nhentai_api.get_doujin(-1)


@pytest.mark.asyncio
async def test_is_exist_false():
    nhentai_api = api.NHentaiAPI()
    is_exist_doujin = await nhentai_api.is_exist(-1)
    assert not is_exist_doujin


@pytest.mark.asyncio
async def test_is_exist_true():
    nhentai_api = api.NHentaiAPI()
    is_exist_doujin = await nhentai_api.is_exist(1)
    assert is_exist_doujin


@pytest.mark.asyncio
async def test_get_random_doujin():
    nhentai_api = api.NHentaiAPI()
    random_doujin = await nhentai_api.get_random_doujin()
    assert random_doujin
