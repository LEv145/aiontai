import os
import site
site.addsitedir(os.getcwd())

from aiontai import models


def test_image_from_json():
    test_json = {
        "h": 120,
        "w": 250,
        "t": "j"
    }

    models.Image.from_json(test_json)
    models.Cover.from_json(test_json)
    models.Thumbnail.from_json(test_json)
    models.Page.from_json(test_json)
    print("Image from_json test is passed!")


def test_wrong_image_from_json():
    try:
        test_json = {
            "h": 120,
            "w": 250,
            "t": ""
        }

        models.Image.from_json(test_json)
        models.Cover.from_json(test_json)
        models.Thumbnail.from_json(test_json)
        models.Page.from_json(test_json)
        print("Wrong Image from_json test is not passed!")
    except ValueError:
        print("Wrong Image from_json test is passed!")


if __name__ == "__main__":
    test_image_from_json()
    test_wrong_image_from_json()
