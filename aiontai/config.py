from schema import Schema, Use, Or


class Config:
    gallery_url = "https://i.nhentai.net/galleries"
    api_url = "https://nhentai.net/api"
    api_gallery_url = "https://nhentai.net/api/galleries"
    base_url = "https://nhentai.net/"
    image_structure = Schema(
        {
            "name": str,
            "media_id": int,
            "height": int,
            "extension": str,
            "width": int
        }
    )
    tag_structure = Schema(
        {
            "count": int,
            "id": int,
            "name": str,
            "type": str,
            "url": str,
        }
    )
    title_structure = Schema(
        {
            "english": str,
            "japanese": str,
            "pretty": str
        }
    )
    doujin_structure = Schema(
        {
            "id": int,
            "media_id": Use(int),
            "title": {str: str},
            "cover": {
                "name": str,
                "extension": str,
                "media_id": int,
                "height": int,
                "width": int
            },
            "pages": [
                {
                    "name": str,
                    "extension": str,
                    "media_id": int,
                    "height": int,
                    "width": int
                },
            ],
            "thumbnail": {
                "name": str,
                "extension": str,
                "media_id": int,
                "height": int,
                "width": int
            },
            "tags": [{str: Or(int, str)}],
            "favorites": int,
            "pages_count": int,
            "scanlator": str,
            "upload_date": int,
        },
    )


config = Config()
