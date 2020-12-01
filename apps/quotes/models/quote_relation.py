from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import CASCADE, ForeignKey, PositiveSmallIntegerField

from modularhistory.models import Model
from modularhistory.utils.html import soupify


class QuoteRelation(Model):
    """A relation to a quote (by any other model)."""

    quote = ForeignKey('quotes.Quote', related_name='relations', on_delete=CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')
    position = PositiveSmallIntegerField(
        null=True,
        blank=True,  # TODO: add cleaning logic
        help_text='Determines the order of quotes.',
    )

    class Meta:
        unique_together = ['quote', 'content_type', 'object_id', 'position']
        ordering = ['position', 'quote']

    def __str__(self) -> str:
        """Return the string representation of the relation."""
        return soupify(self.quote.bite.html).get_text()

    @property
    def quote_pk(self) -> str:
        """
        Return the primary key of the quote relation's quote.

        This attribute can be included in inline admins.
        """
        return self.quote.pk