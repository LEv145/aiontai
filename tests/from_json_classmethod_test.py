import os
import site
site.addsitedir(os.getcwd())

import pytest
from aiontai import models, errors


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

    with pytest.raises((ValueError, errors.IsNotValidStructure)):
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


def test_doujin_from_json():
    test_json = {
        "id": 0,
        "images": {
            "cover": {"h": 0, "t": "j", "w": 0},
            "pages": [
                {"h": 0, "t": "j", "w": 0},
            ],
            "thumbnail": {"h": 0, "t": "j", "w": 0},
        },
        "media_id": "0",
        "num_favorites": 0,
        "num_pages": 0,
        "scanlator": "",
        "tags": [
            {
                "count": 0,
                "id": 0,
                "name": "name",
                "type": "tag",
                "url": "url",
            },
        ],
        "title": {
            "english": "english",
            "japanese": "japanese",
            "pretty": "pretty",
        },
        "upload_date": 0,
    }

    assert models.Doujin.from_json(test_json)


def test_wrong_doujin_from_json():
    test_json = {
        "id": 0,
        "images": {
            "cover": {"h": 0, "t": "j", "w": 0},
            "pages": [
                {"h": 0, "t": "j", "w": 0},
            ],
            "thumbnail": {"h": 0, "t": "j", "w": 0},
        },
        "media_id": "0",
        "num_favorites": 0,
        "num_pages": 0,
        "scanlator": "",
        "tags": [
            {
                "count": 0,
                "id": 0,
                "name": "name",
                "type": "type",
                "url": "url",
            },
        ],
        "title": {
            "english": "english",
            "japanese": "japanese",
            "pretty": "pretty",
        },
        "upload_date": 0,
    }

    with pytest.raises((ValueError, errors.IsNotValidStructure)):
        models.Doujin.from_json(test_json)
