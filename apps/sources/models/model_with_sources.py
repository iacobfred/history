"""Classes for models with relations to sources."""

import logging
from typing import Dict, List, Optional, Type, Union

from celery import shared_task
from concurrency.fields import IntegerVersionField
from django.apps import apps
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models.fields.related import ManyToManyField
from django.utils.html import format_html
from django.utils.safestring import SafeString
from django.utils.translation import ugettext_lazy as _

from apps.sources.models.citation import AbstractCitation, Citation
from core.constants.strings import EMPTY_STRING
from core.fields import HTMLField
from core.fields.custom_m2m_field import CustomManyToManyField
from core.fields.json_field import JSONField
from core.models.model import Model
from core.models.model_with_computations import retrieve_or_compute


class SourcesField(CustomManyToManyField):
    """Field for sources."""

    through_model = AbstractCitation

    def __init__(self, through: Union[Type[AbstractCitation], str], **kwargs):
        kwargs['to'] = 'sources.Source'
        kwargs['through'] = through
        kwargs['verbose_name'] = _('sources')
        super().__init__(**kwargs)


class ModelWithSources(Model):
    """
    A model that has sources; e.g., a quote or occurrence.

    Ideally, this class would be a mixin, but due to Django's model magic,
    it must be defined as an abstract model class.
    """

    citations = GenericRelation('sources.Citation')

    _cached_citations = JSONField(editable=False, default=list)

    version = IntegerVersionField()

    # Admin-facing notes (not to be displayed to users)
    notes = HTMLField(
        null=True, blank=True, paragraphed=True, processed=False, verbose_name=_('note')
    )

    class Meta:
        abstract = True

    @property
    def cached_citations(self) -> list:
        if self._cached_citations or not self.sources.exists():
            return self._cached_citations
        citations = [citation.serialize() for citation in self.citations.all()]
        cache_citations.delay(
            f'{self.__class__._meta.app_label}.{self.__class__.__name__.lower()}',
            self.id,
            citations,
        )
        return citations

    @property
    def citations(self):
        """
        The `related_name` value for the intermediate citation model.

        Models inheriting from ModelWithSources must implement a m2m relationship
        with the Source model with a `through` model that inherits from
        AbstractCitation and uses `related_name='citations'`. For example:

        ``
        class Citation(AbstractCitation):
            content_object = ManyToManyForeignKey(
                to='propositions.Proposition',
                related_name='citations',
            )
        ``
        """
        raise NotImplementedError

    @property
    def sources(self) -> ManyToManyField:
        raise NotImplementedError

    @property
    def source_file_url(self) -> Optional[str]:
        """TODO: write docstring."""
        if self.citation:
            return self.citation.source_file_url
        return None

    @property
    def citation(self) -> Optional['Citation']:
        """Return the quote's primary citation, if a citation exists."""
        try:
            return self.citations.order_by('position')[0]
        except IndexError:
            return None

    @property  # type: ignore
    @retrieve_or_compute(attribute_name='serialized_citations')
    def serialized_citations(self) -> List[Dict]:
        """Return a list of dictionaries representing the instance's citations."""
        return [citation.serialize() for citation in self.citations.all()]

    @property
    def citation_html(self) -> SafeString:
        """Return the instance's full citation HTML."""
        try:
            citation_html = '; '.join(
                citation.get('html') for citation in self.serialized_citations
            )
        except Exception as error:
            logging.error(f'{error}')
            citation_html = EMPTY_STRING
        return format_html(citation_html)


@shared_task
def cache_citations(model: str, instance_id: int, citations: list):
    """Save cached citations to a model instance."""
    if not citations:
        return
    Model = apps.get_model(model)
    model_instance = Model.objects.get(pk=instance_id)
    model_instance._cached_citations = citations
    model_instance.save()
