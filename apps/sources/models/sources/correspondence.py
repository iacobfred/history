"""Model classes for correspondence (as sources)."""

from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.sources.models import PolymorphicSource

from .document import DocumentMixin

NAME_MAX_LENGTH: int = 100
TYPE_MAX_LENGTH: int = 14
CORRESPONDENCE_TYPES = (
    ('correspondence', 'correspondence'),
    ('email', 'email'),
    ('letter', 'letter'),
    ('memorandum', 'memorandum'),
)


class PolymorphicCorrespondence(PolymorphicSource, DocumentMixin):
    """Correspondence from one entity to another."""

    type = models.CharField(
        verbose_name=_('image type'),
        max_length=TYPE_MAX_LENGTH,
        choices=CORRESPONDENCE_TYPES,
        default=CORRESPONDENCE_TYPES[0][0],
    )

    recipient = models.CharField(
        max_length=NAME_MAX_LENGTH,
        null=True,
        blank=True,
    )

    def __html__(self) -> str:
        """Return the correspondence's citation HTML string."""
        components = [
            self.attributee_html,
            f'<a href="{self.href}" target="_blank">{self.type_label} to {self.recipient or "unidentified recipient"}</a>',
            f'dated {self.date.string}' if self.date else '',
            self.descriptive_phrase,
            f'archived in {self.collection}' if self.collection else '',
        ]
        return self.components_to_html(components)