"""Classes for models with relations to sources."""

from typing import Any, Optional, TYPE_CHECKING

from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import CharField
from django.utils.html import SafeString, format_html

from modularhistory.models.searchable_model import SearchableModel

if TYPE_CHECKING:
    from sources.models import Citation


class ModelWithSources(SearchableModel):
    """
    A model that has sources; e.g., a quote or occurrence.

    Ideally, this class would be a mixin, but do to Django's model magic,
    it must be defined as an abstract model class.
    """

    sources: Any

    citations = GenericRelation('sources.Citation')

    class Meta:
        abstract = True

    @property
    def source_file_url(self) -> Optional[str]:
        """TODO: write docstring."""
        if self.citation:
            return self.citation.source_file_url
        return None

    @property
    def citation(self) -> Optional['Citation']:
        """TODO: write docstring."""
        if not len(self.citations.all()):
            return None
        return self.citations.order_by('position')[0]

    @property
    def citation_html(self) -> Optional[SafeString]:
        """TODO: write docstring."""
        # TODO: make sure this is updated correctly
        citation_html = self.computations.get('citation_html')
        if not citation_html:
            if self.citations.exists():
                citation_html = '; '.join([citation.html for citation in self.citations.all()])
            else:
                return None
        return format_html(citation_html)
