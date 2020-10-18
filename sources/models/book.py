"""Model classes for books and sections/chapters (as sources)."""

from typing import Optional

from modularhistory.utils import soupify
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from django.utils.safestring import SafeString
from humanize import ordinal

from modularhistory.fields import ExtraField
from sources.models.textual_source import TextualSource


class Book(TextualSource):
    """A book (as a source)."""

    extra_fields = {
        'translator': 'string',
        'publisher': 'string',
        'edition_number': 'number',
        'edition_year': 'number',
        'printing_number': 'number',
        'volume_number': 'number'
    }

    # translator = jsonstore.CharField(
    #     max_length=100,
    #     null=True,
    #     blank=True,
    #     json_field_name=JSON_FIELD_NAME
    # )

    translator = ExtraField(json_field_name='extra')

    # publisher = jsonstore.CharField(
    #     max_length=100,
    #     null=True,
    #     blank=True,
    #     json_field_name=JSON_FIELD_NAME
    # )

    publisher = ExtraField(json_field_name='extra')

    # edition_number = jsonstore.PositiveSmallIntegerField(
    #     null=True,
    #     blank=True,
    #     json_field_name=JSON_FIELD_NAME
    # )

    edition_number = ExtraField(json_field_name='extra')

    # edition_year = jsonstore.CharField(
    #     null=True,
    #     blank=True,
    #     max_length=4,
    #     json_field_name=JSON_FIELD_NAME
    # )

    edition_year = ExtraField(json_field_name='extra')

    # printing_number = jsonstore.PositiveSmallIntegerField(
    #     null=True,
    #     blank=True,
    #     json_field_name=JSON_FIELD_NAME
    # )

    printing_number = ExtraField(json_field_name='extra')

    # volume_number = jsonstore.PositiveSmallIntegerField(
    #     null=True,
    #     blank=True,
    #     json_field_name=JSON_FIELD_NAME
    # )

    volume_number = ExtraField(json_field_name='extra')

    def __str__(self) -> str:
        """Returns the book's string representation."""
        return soupify(self.__html__).get_text()

    @property
    def edition_string(self) -> Optional[str]:
        """Returns a string representation of the book's edition, if it has one."""
        if self.edition_number:
            edition_string = f'{ordinal(self.edition_number)} edition'
            if self.edition_year:
                edition_string = f'{edition_string} ({self.edition_year})'
        elif self.has_edition_year:
            edition_year = self.edition_year or self.date.year
            edition_string = f'{edition_year} edition'
            if self.original_publication_date:
                edition_string = f'{edition_string} (orig. {self.original_publication_date.year})'
        else:
            return None
        return edition_string

    def get_original_publication_date(self):
        """Returns the book's original publication date."""
        return (
            self.original_edition.date if self.original_edition
            else self.original_publication_date
        )

    @property
    def has_edition_year(self) -> bool:
        """Returns True if an edition year can be determined for the book, else False."""
        return bool(
            self.edition_year or
            (self.get_original_publication_date() and not self.edition_number)
        )

    @property
    def has_printing(self) -> bool:
        """Returns True if a printing (distinct from edition) can be determined for the book, else False."""
        if self.get_original_publication_date() and self.printing_number and not self.edition_number:
            return True
        elif self.edition_year and int(self.edition_year) < self.date.year:
            return True
        return False

    @property
    def printing_string(self) -> Optional[str]:
        """Returns a string representation of the book's printing, if it has one."""
        has_printing_year = self.has_printing
        if self.printing_number and not has_printing_year:
            return f'{ordinal(self.printing_number)} printing'
        elif has_printing_year:
            printing_year_string = f'{self.date.year} printing'
            if self.original_publication_date:
                printing_year_string = f'{printing_year_string} (orig. {self.original_publication_date.year})'
            return printing_year_string
        return None

    @property
    def __html__(self) -> str:
        """Return the book's HTML representation."""
        components = [
            self.attributee_string if self.attributee_string else '',
            f'<i>{self.linked_title}</i>' if self.title else '',
            self.edition_string,
            self.printing_string,
            f'ed. {self.editors}' if self.editors else '',
            f'translated by {self.translator}' if self.translator else '',
            f'{self.publisher}' if self.publisher else '',
            f'vol. {self.volume_number}' if self.volume_number else ''
        ]
        if self.date and not self.has_edition_year and not self.has_printing:
            components.append(f'{self.date.year}')
        return self.components_to_html(components)

    def html(self) -> SafeString:
        """TODO: add docstring."""
        return format_html(self.__html__)
    html.admin_order_field = 'db_string'
    html: SafeString = property(html)  # type: ignore


class SectionSource(TextualSource):
    """A section (e.g., chapter) of a textual source (e.g., book)."""

    def __str__(self) -> str:
        """TODO: write docstring."""
        return soupify(self.html).get_text()  # type: ignore

    def html(self) -> SafeString:
        """TODO: add docstring."""
        return format_html(self.__html__)
    html.admin_order_field = 'db_string'
    html: SafeString = property(html)  # type: ignore

    def full_clean(self, exclude=None, validate_unique=True):
        """TODO: add docstring."""
        super().full_clean(exclude, validate_unique)
        if self.pk:
            if self.container and not isinstance(self.container, Book):
                raise ValidationError('Chapter container must be a book.')

    @property
    def __html__(self) -> str:
        """Return the section/chapter's HTML representation."""
        container_html = None
        if self.container:
            container_html = f'{self.container.html}'
            if self.attributee_string:
                if self.attributee_string == self.container.attributee_string:
                    container_html = container_html.replace(f'{self.attributee_string}, ', '')
        if self.attributee_string:
            attributee_string = self.attributee_string
        elif self.container:
            attributee_string = self.container.attributee_string
        else:
            attributee_string = None
        components = [item for item in (attributee_string, f'"{self.linked_title}"') if item]
        if container_html:
            components.append(f'in {container_html}')
        return ', '.join(components).replace('",', ',"')

    @property
    def string(self) -> str:
        """TODO: write docstring."""
        return soupify(self.html).get_text()  # type: ignore


class Section(SectionSource):
    """A section (e.g., of a book or article) as a source."""

    type_label = 'section'


class Chapter(SectionSource):
    """A chapter (of a book) as a source."""

    type_label = 'chapter'
