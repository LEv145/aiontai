from schema import Schema, Use, Or


class Config:
    gallery_url = "https://i.nhentai.net/galleries"
    api_url = "https://nhentai.net/api"
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
            "images": {
                "cover": {str: Or(int, str)},
                "pages": [{str: Or(int, str)}],
                "thumbnail": {str: Or(int, str)},
            },
            "tags": [{str: Or(int, str)}],
            "favorites": int,
            "pages_count": int,
            "scanlator": str,
            "upload_date": int,
        }
    )


config = Config()
