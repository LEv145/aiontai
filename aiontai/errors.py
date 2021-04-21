"""Errors for API and other."""


class IsNotValidStructure(Exception):
    """Exception for bad structure."""


class DoujinDoesNotExist(Exception):
    """Exception for not existing doujin."""


class IsNotValidSort(Exception):
    """Exception for bad sort option."""


class WrongPage(Exception):
    """Exception for wrong page."""

class WrongSearch(Exception):
    """Exception for wrong search."""

class WrongTag(Exception):
    """Exception for wrong tag."""
