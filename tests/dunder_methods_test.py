import os
import site
import asyncio
site.addsitedir(os.getcwd())
import pytest
import aiontai


@pytest.mark.asyncio
async def test_iter_doujin():
    api = aiontai.API()
    doujin = await api.get_doujin(1)

    assert iter(doujin)


@pytest.mark.asyncio
async def test_getitem_doujin():
    api = aiontai.API()
    doujin = await api.get_doujin(1)

    assert doujin[0]


@pytest.mark.asyncio
async def test_getitem_doujin_type_error():
    api = aiontai.API()
    doujin = await api.get_doujin(1)

    with pytest.raises(TypeError):
        assert doujin["type_error"]


@pytest.mark.asyncio
async def test_getitem_doujin_index_error():
    api = aiontai.API()
    doujin = await api.get_doujin(1)

    with pytest.raises(IndexError):
        assert doujin[doujin.pages_count]


@pytest.mark.asyncio
async def test_getitem_doujin_len():
    api = aiontai.API()
    doujin = await api.get_doujin(1)

    assert len(doujin)


@pytest.mark.asyncio
async def test_getitem_doujin_reversed():
    api = aiontai.API()
    doujin = await api.get_doujin(1)

    assert reversed(doujin)


@pytest.mark.asyncio
async def test_getitem_doujin_contains():
    api = aiontai.API()
    doujin = await api.get_doujin(1)
    second_doujin = await api.get_doujin(2)

    assert doujin[0] in doujin
    assert second_doujin[0] not in doujin
