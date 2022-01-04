from typing import Iterator
from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock

from aiontai.models import (
    Doujin,
    Image,
)


class TestDoujin(IsolatedAsyncioTestCase):
    async def test__iterable(self):
        model = Doujin(
            id=Mock(),
            media_id=Mock(),
            title=Mock(),
            cover=Mock(),
            thumbnail=Mock(),
            pages=[
                Mock(spec=Image), Mock(spec=Image), Mock(spec=Image),
            ],
            tags=Mock(),
            pages_count=Mock(),
            favorites_count=Mock(),
            scanlator=Mock(),
            upload_date=Mock(),
        )

        self.assertIsInstance(
            iter(model),
            Iterator,
        )
        self.assertIsInstance(
            next(iter(model)),
            Image,
        )
        self.assertIsInstance(
            len(model),
            int,
        )
        self.assertIsInstance(
            model[0],
            Image,
        )
