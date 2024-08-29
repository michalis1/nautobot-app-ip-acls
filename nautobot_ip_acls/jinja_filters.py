"""Jinja Filters Definition."""

from django_jinja import library


@library.filter
def my_uppercase(text):
    """Upper Case Filter."""
    return text.upper()
