# aiontai
Async wrapper for nhentai API

# Installation
```cmd
pip install aiontai
```

## Examples
### Get doujin
```python
import asyncio
import aiontai

api = aiontai.API(proxi="http://45.67.123.207:30001")


async def main():
    doujin = api.get_doujin(1)


if __name__ == "__main__":
    asyncio.run(main()) 
```
### Iterate of doujin pages
```python
import asyncio
import aiontai

api = aiontai.API()


async def main():
    doujin = api.get_doujin(1)
    for page in doujin:
        print(page)


if __name__ == "__main__":
    asyncio.run(main()) 
```

# Dataclasses
- ## ImageExtension
    - Enumeration, that represents an [Image](#Image) type.
    ### Enumerations
    - jpg {str} = "j"
    - png {str} = "p
    - gif {str} = "g"
- ## TagType
    - Enumeration, that represents a [Tag](#Tag) type.
    ### Enumerations
    - tag {str} = "tag"
    - category {str} = "category"
    - artist {str} = "artist"
    - parody {str} = "parody"
    - character {str} = "character"
    - group {str} = "group"
    - language {str} = "language"
- ## Title
    ### Attributes
    - english {str} -- English version of title
    - japanese {str} -- Japanese version of title
    - pretty {str} -- Short english version of title
- ## Image
    ### Attributes
    - name {str} -- Name of image
    - media_id {int} -- Media id of Doujin, for which this image belong.
    - width {int} -- Image width
    - height {int} -- Image height
    - extension {[ImageExtension](#ImageExtension)} -- type of image (jpg, png, gif)
    - url {str} -- Image URL
- ## Tag
    ### Attributes
    - id {int} -- tag id user for search
    - count {int} -- number of tag uses
    - name {str} -- tag name
    - type {[TagType](#TagType)} -- type of tag
    - url {str} -- tag URL
- ## Doujin
    ### Attributes
    - doujin_id {int} -- id of doujin
    - media_id {int} -- id for doujin's images
    - title {[Title](#Title)} -- Title of doujin
    - cover {[Image](#Image)} -- The doujin cover
    - thumbnail {[Image](#Image)} -- The doujin thumbnail
    - pages {List\[[Image](#Image)\]} -- List of images, that represents pages of doujin
    - pages_count {int} -- Count of pages
    - tags {List\[[Tag](#Tag)\]} -- List of doujin tags
    - favorites {int} -- Count of likes
    - upload_date {datetime.datetime} -- datetime, when doujin has been published
# class API
- ## async get_doujin()
    Method for search doujins by id.
    ### Args:
    - id {int} -- Doujin's id, which we get.

    ### Returns:
    - [Doujin](#Doujin).

    ### Raises:
    - DoujinDoesNotExist if doujin was not found.

    ### Usage:
    ```python
    >>> api = NHentaiAPI()
    >>> await api.get_doujin(1)
    Doujin(...)
    ```

- ## async is_exist()
    Method for checking does doujin exist.
    ### Args:
    - id {int} -- Doujin's id, which we check.

    ### Returns:
    - True if doujin is exist
    - False if doujin is not exist.

    ### Usage:
    ```python
    >>> api = NHentaiAPI()
    >>> await api.is_exist(1)
    True
    >>> await api.is_exist(-1)
    False
    ```

- ## async get_random_doujin()
    Method for getting random doujin.
    ### Returns:
    - [Doujin](#Doujin).

    ### Usage:
    ```python
    >>> api = NHentaiAPI()
    >>> await api.get_random_doujin()
    Doujin(...)
    ```

- ## async search()
    Method for search doujins.
    ### Args:
    - query {str} -- Query for search doujins.
    - page {int} -- Page, from which we return results.
    - sort_by {str} -- Sort for search.

    ### Returns:
    - List\[[Doujin](#Doujin)\]

    ### Raises:
    - IsNotValidSort if sort is not a member of SortOptions.
    - WrongPage if page less than 1 or page has no content.

    ### Usage:
    ```python
    >>> api = NHentaiAPI()
    >>> await api.search("anime", page=2, sort_by="popular")
    [Doujin(...), ...]
    ```

- ## async search_by_tag()
    Method for search doujins by tag.
    ### Args:
    - tag {int} -- Tag for search doujins.
    - page {int} -- Page, from which we return results.
    - sort_by {str} -- Sort for search.

    ### Returns:
    - List\[[Doujin](#Doujin)\]

    ### Raises:
    - IsNotValidSort if sort is not a member of SortOptions.
    - WrongPage if page less than 1 or page has no content.
    - WrongTag if tag with given id does not exist.

    ### Usage:
    ```python
    >>> api = NHentaiAPI()
    >>> await api.search_by_tag(1)
    [Doujin(...), ...]
    ```

- ## async get_homepage_doujins()
    Method for getting doujins from.
    ### Args:
    - page {int} = 1 -- Page, from which we get doujins.

    ### Returns:
    - List\[[Doujin](#Doujin)\]

    ### Raises:
    - WrongPage if page less than 1 or page has no content.

    ### Usage:
    ```python
    >>> api = NHentaiAPI()
    >>> await api.get_homepage_doujins(page=2)
    [Doujin(...), ...]
    ```

# Contributing
1. Write your code as PEP8
2. Write tests for your code
3. Dont be rude with other contributors

# Issues 
1. Before opening issue check, is it not a duplicate
2. In issue write, how to reproduce issue
