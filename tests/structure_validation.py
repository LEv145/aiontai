import os
import site
site.addsitedir(os.getcwd())

from aiontai import utils
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

    utils.is_valid_structure(config.doujin_structure, test_structure)
    print("Doujin structure test is passed")


def test_image_structure():
    test_structure = {"h": 0, "t": "j", "w": 0}

    utils.is_valid_structure(config.image_structure, test_structure)
    print("Image structure test is passed")


def test_tag_structure():
    test_structure = {
                "count": 0,
                "id": 0,
                "name": "name",
                "type": "type",
                "url": "url",
    }

    utils.is_valid_structure(config.tag_structure, test_structure)
    print("Tag structure test is passed")


def test_title_structure():
    test_structure = {
            "english": "english",
            "japanese": "japanese",
            "pretty": "pretty",
        }

    utils.is_valid_structure(config.title_structure, test_structure)
    print("Title structure test is passed")


if __name__ == "__main__":
    test_doujin_structure()
    test_image_structure()
    test_tag_structure()
    test_title_structure()
