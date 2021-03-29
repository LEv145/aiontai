import os
import site
import asyncio
import dataclasses
site.addsitedir(os.getcwd())

import pytest

import aiontai
from aiontai import api


@pytest.mark.asyncio
async def test_immutable():
    api = aiontai.API()
    doujin = await api.get_doujin(1)
    
    with pytest.raises(dataclasses.FrozenInstanceError):
        doujin.pages = 1
        doujin.cover.name = "1"
