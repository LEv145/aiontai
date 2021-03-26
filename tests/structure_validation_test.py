import os
import site

from schema import SchemaError
site.addsitedir(os.getcwd())

import pytest

from aiontai import utils, errors
from aiontai.config import config


def test_doujin_structure():
    test_structure = {
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

    assert utils.is_valid_structure(config.doujin_structure, test_structure)


def test_wrong_doujin_structure():
    test_structure = {
        "test": "test"
    }

    with pytest.raises(errors.IsNotValidStructure):
        utils.is_valid_structure(config.doujin_structure, test_structure)


def test_image_structure():
    test_structure = {"name": "name", "media_id": 0, "h": 0, "t": "j", "w": 0}

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
