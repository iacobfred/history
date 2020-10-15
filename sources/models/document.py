"""Model classes for documents (as sources)."""

from bs4 import BeautifulSoup
from django.db import models
from django.db.models import CASCADE, ForeignKey
from django.utils.safestring import SafeString
from django.utils.html import format_html

from modularhistory.fields import ExtraField
from modularhistory.models import Model
from sources.models.piece import SourceWithPageNumbers

NAME_MAX_LENGTH: int = 100
LOCATION_INFO_MAX_LENGTH: int = 400
DESCRIPTIVE_PHRASE_MAX_LENGTH: int = 100
URL_MAX_LENGTH: int = 100


class DocumentSource(SourceWithPageNumbers):
    """A historical document (as a source)."""

    # collection_number = jsonstore.PositiveSmallIntegerField(
    #     null=True,
    #     blank=True,
    #     help_text='aka acquisition number',
    #     json_field_name=JSON_FIELD_NAME
    # )

    collection_number = ExtraField(json_field_name='extra')

    # location_info = jsonstore.CharField(
    #     max_length=LOCATION_INFO_MAX_LENGTH,
    #     null=True,
    #     blank=True,
    #     help_text='Ex: John H. Alexander Papers, Series 1: Correspondence, 1831-1848, Folder 1',
    #     json_field_name=JSON_FIELD_NAME
    # )

    location_info = ExtraField(json_field_name='extra')

    # descriptive_phrase = jsonstore.CharField(
    #     max_length=DESCRIPTIVE_PHRASE_MAX_LENGTH,
    #     null=True,
    #     blank=True,
    #     help_text='e.g., "on such-and-such letterhead" or "signed by so-and-so"',
    #     json_field_name=JSON_FIELD_NAME
    # )

    descriptive_phrase = ExtraField(json_field_name='extra')

    # information_url = jsonstore.URLField(
    #     max_length=URL_MAX_LENGTH,
    #     null=True,
    #     blank=True,
    #     help_text='URL for information regarding the document',
    #     json_field_name=JSON_FIELD_NAME
    # )

    information_url = ExtraField(json_field_name='extra')


class Collection(Model):
    """TODO: add docstring."""

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        help_text='e.g., "Adam S. Bennion papers"',
        null=True,
        blank=True
    )
    repository = ForeignKey(
        'sources.Repository',
        on_delete=CASCADE,
        help_text='the collecting institution'
    )
    url = models.URLField(
        max_length=URL_MAX_LENGTH,
        null=True,
        blank=True
    )

    class Meta:
        unique_together = ['name', 'repository']

    def __str__(self) -> str:
        """TODO: write docstring."""
        return BeautifulSoup(self.__html__, features='lxml').get_text()

    @property
    def html(self) -> SafeString:
        """TODO: write docstring."""
        return format_html(self.__html__)

    @property
    def __html__(self) -> str:
        """TODO: write docstring."""
        components = [
            f'{self.name}' if self.name else '',
            f'{self.repository}',
        ]
        # Remove blank values
        components = [component for component in components if component]
        # Join components; rearrange commas and double quotes
        return ', '.join(components).replace('",', ',"')


class Repository(Model):
    """TODO: add docstring."""

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        null=True,
        blank=True,
        help_text='e.g., "L. Tom Perry Special Collections"'
    )
    owner = models.CharField(
        max_length=NAME_MAX_LENGTH,
        null=True,
        blank=True,
        help_text='e.g., "Harold B. Lee Library, Brigham Young University"'
    )
    location = ForeignKey(
        'places.Place',
        on_delete=models.SET_NULL,
        related_name='repositories',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name_plural = 'Repositories'

    def __str__(self) -> str:
        """TODO: write docstring."""
        location_string = self.location.string if self.location else None
        components = [self.name, self.owner, location_string]
        return ', '.join([component for component in components if component])


class Document(DocumentSource):
    """A historical document (as a source)."""

    def __str__(self) -> str:
        """TODO: write docstring."""
        return BeautifulSoup(self.__html__, features='lxml').get_text()

    @property
    def __html__(self) -> str:
        """TODO: write docstring."""
        components = [
            self.attributee_string,
            self.linked_title if self.title else 'untitled document',
            self.date.string if self.date else 'date unknown',
            self.descriptive_phrase,
            f'archived in {self.collection}' if self.collection else ''
        ]

        # Remove blank values
        components = [component for component in components if component]

        # Join components; rearrange commas and double quotes
        return ', '.join(components).replace('",', ',"')
