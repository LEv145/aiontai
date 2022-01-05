import json
from pathlib import Path
from unittest import TestCase

from tests.testdata.models import (
    doujin,
    doujins_result,
)
from aiontai.converter import (
    Conventer,
)


class TestConventer(TestCase):
    def setUp(self) -> None:
        self.conventer = Conventer()

    def test__convert_doujin(self) -> None:
        with open(Path("./tests/testdata/doujin.json")) as fp:
            raw_data = json.load(fp)

        test_doujin = self.conventer.convert_doujin(
            raw_data,
        )

        self.assertEqual(
            test_doujin,
            doujin,
        )

    def test__convert_doujins_result(self) -> None:
        with open(Path("./tests/testdata/doujins_result.json")) as fp:
            raw_data = json.load(fp)

        test_doujins_result = self.conventer.convert_doujins_result(
            raw_data,
        )

        self.assertEqual(
            test_doujins_result,
            doujins_result,
        )
