import os
import site
import asyncio
site.addsitedir(os.getcwd())

import pytest
import aiontai
from aiontai import errors


@pytest.mark.asyncio
async def test_api_get_doujin():
    api = aiontai.API()
    doujin = await api.get_doujin(1)
    assert (
           doujin.doujin_id 
           and doujin.title
           and doujin.media_id
           and doujin.cover
           and doujin.thumbnail
           and doujin.tags
           and doujin.pages
           and doujin.pages_count
           )


@pytest.mark.asyncio
async def test_api_get_doujin_wrong():
    api = aiontai.API()
    with pytest.raises(errors.DoujinDoesNotExist):
        await api.get_doujin(0)


@pytest.mark.asyncio
async def test_api_is_exist_true():
    api = aiontai.API()
    is_exist_doujin = await api.is_exist(1)
    assert is_exist_doujin


@pytest.mark.asyncio
async def test_api_is_exist_false():
    api = aiontai.API()
    is_exist_doujin = await api.is_exist(0)
    assert not is_exist_doujin


@pytest.mark.asyncio
async def test_api_get_random_doujin():
    api = aiontai.API()
    doujin = await api.get_random_doujin()
    assert (
           doujin.doujin_id 
           and doujin.title
           and doujin.media_id
           and doujin.cover
           and doujin.thumbnail
           and doujin.tags
           and doujin.pages
           and doujin.pages_count
           )


@pytest.mark.asyncio
async def test_api_search():
    api = aiontai.API()
    doujins = await api.search("anime", page=2, sort_by="popular")
    assert doujins


@pytest.mark.asyncio
async def test_api_search_by_tag():
    api = aiontai.API()
    await api.search_by_tag(1, sort_by="popular")


@pytest.mark.asyncio
async def test_api_homepage_doujins():
    api = aiontai.API()
    doujins = await api.get_homepage_doujins(page=2)
    assert doujins
