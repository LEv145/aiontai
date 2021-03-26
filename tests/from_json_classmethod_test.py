import os
import site
site.addsitedir(os.getcwd())

import pytest
from aiontai import models


def test_image_from_json():
    test_json = {
        "h": 120,
        "w": 250,
        "t": "j"
    }

    assert models.Image.from_json(test_json)
    assert models.Cover.from_json(test_json)
    assert models.Thumbnail.from_json(test_json)
    assert models.Page.from_json(test_json)


def test_wrong_image_from_json():
    test_json = {
        "h": 120,
        "w": 250,
        "t": ""
    }

    with pytest.raises(ValueError):
        models.Image.from_json(test_json)
        models.Cover.from_json(test_json)
        models.Thumbnail.from_json(test_json)
        models.Page.from_json(test_json)


def test_tag_from_json():
    test_json = {
            "count": 0,
            "id": 0,
            "name": "name",
            "type": "tag",
            "url": "url"
    }

    assert models.Tag.from_json(test_json)


def test_wrong_tag_from_json():
    test_json = {
            "count": 0,
            "id": 0,
            "name": "name",
            "type": "type",
            "url": "url"
    }

    with pytest.raises(ValueError):
        models.Tag.from_json(test_json)
