import os
import site
site.addsitedir(os.getcwd())

from aiontai import models, errors
import pytest


def test_doujin_from_json():
    test_json = {
        "id": 0,
        "media_id": 0,
        "title": {
            "english": "english",
            "japanese": "japanese",
            "pretty": "pretty"
        },
        "cover": {
            "name": "name",
            "extension": "p",
            "media_id": 0,
            "height": 0,
            "width": 0
        },
        "pages": [
            {
                "name": "name",
                "extension": "p",
                "media_id": 0,
                "height": 0,
                "width": 0
            },
        ],
        "thumbnail": {
            "name": "name",
            "extension": "p",
            "media_id": 0,
            "height": 0,
            "width": 0
        },
        "tags": [
            {
                "count": 0,
                "id": 0,
                "name": "name",
                "type": "tag",
                "url": "url",
            }
        ],
        "favorites": 0,
        "pages_count": 1,
        "scanlator": "",
        "upload_date": 1,
    }

    assert models.Doujin.from_json(test_json)


def test_doujin_from_json_wrong():
    test_json = {
        "test": "test"
    }

    with pytest.raises(errors.IsNotValidStructure):
        models.Doujin.from_json(test_json)


def test_image_from_json():
    test_json = {
        "name": "name",
        "media_id": 0,
        "height": 120,
        "width": 250,
        "extension": "j"
    }

    assert models.Image.from_json(test_json)


def test_wrong_image_from_json():
    test_json = {
        "name": 0,
        "media_id": "0",
        "h": 120,
        "w": 250,
        "t": ""
    }

    with pytest.raises((ValueError, errors.IsNotValidStructure)):
        models.Image.from_json(test_json)


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

    with pytest.raises((ValueError, errors.IsNotValidStructure)):
        models.Tag.from_json(test_json)


def test_title_from_json():
    test_json = {
        "english": "english",
        "japanese": "japanese",
        "pretty": "pretty"
    }

    assert models.Title.from_json(test_json)


def test_wrong_title_from_json():
    test_json = {
        "english": 0,
        "japanese": 0,
        "pretty": 0
    }

    with pytest.raises((ValueError, errors.IsNotValidStructure)):
        models.Title.from_json(test_json)
