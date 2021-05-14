"""Model classes for propositions."""

import logging
import re
from typing import Match, Optional

from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from polymorphic.models import PolymorphicModel

from apps.entities.models.model_with_related_entities import ModelWithRelatedEntities
from apps.propositions.api.serializers import PropositionSerializer
from apps.sources.models.model_with_sources import ModelWithSources
from apps.topics.models.taggable_model import TaggableModel
from apps.verifications.models import VerifiableModel
from core.fields import HTMLField
from core.fields.html_field import (
    OBJECT_PLACEHOLDER_REGEX,
    TYPE_GROUP,
    PlaceholderGroups,
)
from core.models import SluggedModel
from core.utils.html import escape_quotes
from core.utils.string import dedupe_newlines, truncate

proposition_placeholder_regex = OBJECT_PLACEHOLDER_REGEX.replace(
    TYPE_GROUP, rf'(?P<{PlaceholderGroups.MODEL_NAME}>proposition)'
)
logging.debug(f'Proposition placeholder pattern: {proposition_placeholder_regex}')


DEGREES_OF_CERTAINTY = (
    (0, 'No credible evidence'),
    (1, 'Some credible evidence'),
    (2, 'A preponderance of evidence'),
    (3, 'Beyond reasonable doubt'),
    (4, 'Beyond any shadow of a doubt'),
)


class PolymorphicProposition(PolymorphicModel, VerifiableModel, ModelWithSources):
    """
    Base model for propositions.

    Models of which instances are proposed, i.e., presented as information that
    can be analyzed and judged to be true or false with some degree of certainty,
    should inherit from this model.
    """


class Proposition(
    PolymorphicProposition,
    SluggedModel,
    TaggableModel,
    ModelWithRelatedEntities,
):
    """A proposition."""

    _summary = HTMLField(
        verbose_name=_('statement'), unique=True, paragraphed=False, processed=False
    )
    _elaboration = HTMLField(
        verbose_name=_('elaboration'), null=True, blank=True, paragraphed=True
    )
    certainty = models.PositiveSmallIntegerField(
        verbose_name=_('certainty'), null=True, choices=DEGREES_OF_CERTAINTY
    )
    premises = models.ManyToManyField(
        to='self',
        through='propositions.Support',
        related_name='conclusions',
        symmetrical=False,
        verbose_name=_('premises'),
    )

    searchable_fields = ['summary', 'elaboration']
    serializer = PropositionSerializer
    slug_base_field = 'summary'

    def __str__(self) -> str:
        """Return the proposition's string representation."""
        return self.summary.text

    @property
    def summary_link(self) -> str:
        """Return an HTML link to the proposition, containing the summary text."""
        add_elaboration_tooltip = False
        elaboration = self.elaboration.html if self.elaboration else ''
        elaboration = elaboration.replace('\n', '')
        if add_elaboration_tooltip:
            summary_link = (
                f'<a href="{reverse("propositions:detail", args=[self.pk])}" class="proposition-link" '
                f'target="_blank" title="{escape_quotes(elaboration)}" '
                f'data-toggle="tooltip" data-html="true">{self.summary.html}</a>'
            )
        else:
            summary_link = (
                f'<a href="{reverse("propositions:detail", args=[self.pk])}" class="proposition-link" '
                f'target="_blank">{self.summary.html}</a>'
            )
        return summary_link

    @classmethod
    def get_object_html(cls, match: Match, use_preretrieved_html: bool = False) -> str:
        """Return the obj's HTML based on a placeholder in the admin."""
        if not match:
            logging.error('proposition.get_object_html was called without a match')
            raise ValueError
        if use_preretrieved_html:
            # Return the pre-retrieved HTML (already included in placeholder)
            preretrieved_html = match.group(PlaceholderGroups.HTML)
            if preretrieved_html:
                return preretrieved_html.strip()
        proposition: 'Proposition' = cls.objects.get(
            pk=match.group(PlaceholderGroups.PK)
        )
        return proposition.summary_link

    @classmethod
    def get_updated_placeholder(cls, match: Match) -> str:
        """Return a placeholder for a model instance depicted in an HTML field."""
        placeholder = match.group(0)
        logging.debug(f'Looking at {truncate(placeholder)}')
        extant_html: Optional[str] = match.group(PlaceholderGroups.HTML)
        extant_html = extant_html.strip() if extant_html else extant_html
        if extant_html:

            if '<a ' not in extant_html:
                html = cls.get_object_html(match)
                html = re.sub(
                    r'(.+?">).+?(<\/a>)',  # TODO
                    rf'\g<1>{extant_html}\g<2>',
                    html,
                )
                placeholder = placeholder.replace(
                    match.group(PlaceholderGroups.HTML), html
                )
            else:
                logging.info('Returning extant placeholder')
                return placeholder
        else:
            html = cls.get_object_html(match)
            model_name = match.group(PlaceholderGroups.MODEL_NAME)
            pk = match.group(PlaceholderGroups.PK)
            placeholder = f'[[ {model_name}: {pk}: {html} ]]'
        return dedupe_newlines(placeholder)