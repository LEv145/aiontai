from schema import Schema, Use, Or


class Config:
    gallery_url = "https://i.nhentai.net/galleries"
    doujin_structure = Schema(
        {
            "id": int,
            "images": {
                "cover": {str: Or(int, str)},
                "pages": [{str: Or(int, str)}],
                "thumbnail": {str: Or(int, str)},
            },
            "media_id": Use(int),
            "num_favorites": int,
            "num_pages": int,
            "scanlator": str,
            "tags": [{str: Or(int, str)}],
            "title": {str: str},
            "upload_date": int,
        }
    )
    image_structure = Schema(
        {
            "name": str,
            "media_id": int,
            "h": int,
            "t": str,
            "w": int
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


config = Config()
