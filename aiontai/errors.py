"""Errors for API and other."""


class IsNotValidStructure(Exception):
    """Exception for bad structure."""


class DoujinDoesNotExist(Exception):
    """Exception for not existing doujin."""


class WrongPage(Exception):
    """Exception for wrong page."""


class WrongSearch(Exception):
    """Exception for wrong search."""


class WrongTag(Exception):
    """Exception for wrong tag."""


class IsNotValidSort(Exception):
    """Exception not valid sort option."""
