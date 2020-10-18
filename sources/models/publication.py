from modularhistory.utils import soupify
from django.db import models
from django.utils.safestring import SafeString
from django.utils.html import format_html
from typedmodels.models import TypedModel

from modularhistory.fields import HTMLField
from modularhistory.models import Model

PUBLICATION_TYPES = (
    ('journal', 'Journal'),
    ('newspaper', 'Newspaper'),
    ('magazine', 'Magazine'),
)


class Publication(TypedModel, Model):
    """A publication, such as a newspaper, magazine, journal, or website."""

    name = models.CharField(max_length=100, null=True, blank=True, unique=True)
    aliases = models.CharField(max_length=100, null=True, blank=True)
    description = HTMLField(null=True, blank=True)

    class Meta:
        ordering = ['name']

    searchable_fields = ['name', 'aliases']

    def __str__(self) -> str:
        """TODO: write docstring."""
        return soupify(self.__html__).get_text()

    @property
    def html(self) -> SafeString:
        """TODO: write docstring."""
        return format_html(self.__html__)

    @property
    def __html__(self) -> str:
        """TODO: write docstring."""
        return f'<i>{self.name}</i>'


class Journal(Publication):
    """A journal that publishes articles."""

    pass


class Magazine(Publication):
    """A magazine that publishes articles."""

    pass


class Newspaper(Publication):
    """A newspaper that publishes articles."""

    pass
