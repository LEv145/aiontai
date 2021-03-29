# aiontai
Async wrapper for nhentai API

## Installation
```cmd
pip install aiontai
```

## class API
- ### async get_doujin()
    Method for search doujins by id.
    #### Args:
    - id {int} -- Doujin's id, which we get.

    #### Returns:
    - JSON of doujin.

    #### Raises:
    - DoujinDoesNotExist if doujin was not found.

    #### Usage:
    ```python
    >>> api = NHentaiAPI()
    >>> await api.get_doujin(1)
    Doujin(...)
    ```

- ### async is_exist()
    Method for checking does doujin exist.
    #### Args:
    - id {int} -- Doujin's id, which we check.

    #### Returns:
    - True if doujin is exist
    - False if doujin is not exist.

    #### Usage:
    ```python
    >>> api = NHentaiAPI()
    >>> await api.is_exist(1)
    True
    >>> await api.is_exist(-1)
    False
    ```

- ### async get_random_doujin()
    Method for getting random doujin.
    #### Returns:
    - JSON of random doujin.

    #### Usage:
    ```python
    >>> api = NHentaiAPI()
    >>> await api.random_doujin()
    Doujin(...)
    ```

- ### async search()
    Method for search doujins.
    #### Args:
    - query {str} -- Query for search doujins.
    - page {int} -- Page, from which we return results.
    - sort_by {str} -- Sort for search.

    #### Returns:
    - List of doujins JSON

    #### Raises:
    - IsNotValidSort if sort is not a member of SortOptions.
    - WrongPage if page less than 1 or page has no content.

    #### Usage:
    ```python
    >>> api = NHentaiAPI()
    >>> await api.search("anime", page=2, sort_by="popular")
    [Doujin(...), ...]
    ```

- ### async search_by_tag()
    Method for search doujins by tag.
    #### Args:
    - tag {int} -- Tag for search doujins.
    - page {int} -- Page, from which we return results.
    - sort_by {str} -- Sort for search.

    #### Returns:
    - List of doujins JSON

    #### Raises:
    - IsNotValidSort if sort is not a member of SortOptions.
    - WrongPage if page less than 1 or page has no content.
    - WrongTag if tag with given id does not exist.

    #### Usage:
    ```python
    >>> api = NHentaiAPI()
    >>> await api.search_by_tag(1)
    [Doujin(...), ...]
    ```

- ### async get_homepage_doujins()
    Method for getting doujins from.
    #### Args:
    - page {int} = 1 -- Page, from which we get doujins.

    #### Returns:
    - List of doujins JSON

    #### Raises:
    - WrongPage if page less than 1 or page has no content.

    #### Usage:
    ```python
    >>> api = NHentaiAPI()
    >>> await api.get_homepage_doujins(page=2)
    [Doujin(...), ...]
    ```

## Example
```python
import asyncio
import aiontai

api = aiontai.API()


async def main():
    doujin = api.get_doujin(1)


if __name__ == "__main__":
    asyncio.run(main()) 
```

## Contributing
1. Write your code as PEP8
2. Write tests for your code
3. Dont be rude with other contributors

## Issues 
1. Before opening issue check, is it not a duplicate
2. In issue write, how to reproduce issue
