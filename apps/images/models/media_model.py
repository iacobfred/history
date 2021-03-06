from django.db import models

from apps.dates.models import DatedModel
from apps.search.models.searchable_model import SearchableModel

from core.fields.html_field import HTMLField

PROVIDER_MAX_LENGTH: int = 200


class MediaModel(SearchableModel, DatedModel):
    """Abstract base model for media models (e.g., images and videos)."""

    caption = HTMLField(blank=True, paragraphed=False)
    description = HTMLField(blank=True)
    provider = models.CharField(max_length=PROVIDER_MAX_LENGTH, blank=True)

    class Meta:
        """Meta options for MediaModel."""

        # https://docs.djangoproject.com/en/dev/ref/models/options/#model-meta-options

        abstract = True

    slug_base_fields = ('caption',)
