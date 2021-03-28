from aiontai.config import config
from aiontai import utils, errors
import pytest
from schema import SchemaError
import os
import site

site.addsitedir(os.getcwd())


def test_doujin_structure():
    test_structure = {
        "id": 0,
        "media_id": 0,
        "title": {
            "english": "english",
            "japanese": "japanese",
            "pretty": "pretty",
        },
        "cover": {
            "name": "name",
            "extension": "j",
            "media_id": 0,
            "height": 0,
            "width": 0
        },
        "pages": [
            {
                "name": "name",
                "extension": "j",
                "media_id": 0,
                "height": 0,
                "width": 0
            }
        ],
        "thumbnail": {
            "name": "name",
            "extension": "j",
            "media_id": 0,
            "height": 0,
            "width": 0
        },
        "favorites": 0,
        "pages_count": 0,
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
        "upload_date": 0,
    }

    assert utils.is_valid_structure(config.doujin_structure, test_structure)


def test_wrong_doujin_structure():
    test_structure = {
        "test": "test"
    }

    with pytest.raises(errors.IsNotValidStructure):
        utils.is_valid_structure(config.doujin_structure, test_structure)


def test_image_structure():
    test_structure = {
        "name": "name",
        "media_id": 0,
        "height": 0,
        "extension": "j",
        "width": 0
    }

    assert utils.is_valid_structure(config.image_structure, test_structure)


def test_wrong_image_structure():
    test_structure = {0: "test"}

    with pytest.raises(errors.IsNotValidStructure):
        utils.is_valid_structure(config.image_structure, test_structure)


def test_tag_structure():
    test_structure = {
        "count": 0,
        "id": 0,
        "name": "name",
                "type": "type",
                "url": "url",
    }

    assert utils.is_valid_structure(config.tag_structure, test_structure)


def test_wrong_tag_structure():
    test_structure = {0: 0}

    with pytest.raises(errors.IsNotValidStructure):
        utils.is_valid_structure(config.tag_structure, test_structure)


def test_title_structure():
    test_structure = {
        "english": "english",
        "japanese": "japanese",
        "pretty": "pretty",
    }

    assert utils.is_valid_structure(config.title_structure, test_structure)


def test_wrong_title_structure():
    test_structure = {0: 0}

    with pytest.raises(errors.IsNotValidStructure):
        utils.is_valid_structure(config.title_structure, test_structure)
