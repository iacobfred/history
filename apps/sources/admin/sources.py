import logging
from typing import Dict, Optional

from django.forms import ModelForm
from polymorphic.admin import PolymorphicChildModelAdmin, PolymorphicParentModelAdmin

from admin import TabularInline, admin_site
from apps.search.admin import SearchableModelAdmin
from apps.sources import models
from apps.sources.admin.filters import (
    AttributeeFilter,
    HasContainerFilter,
    HasFileFilter,
    HasFilePageOffsetFilter,
    ImpreciseDateFilter,
    TypeFilter,
)
from apps.sources.admin.inlines import (
    AttributeesInline,
    ContainedSourcesInline,
    ContainersInline,
    PolymorphicAttributeesInline,
    PolymorphicContainedSourcesInline,
    PolymorphicContainersInline,
    RelatedInline,
)

INITIAL = 'initial'


class SourceForm(ModelForm):
    """Form for adding/editing sources."""

    model = models.Source

    class Meta:
        model = models.Source
        exclude = model.inapplicable_fields

    def __init__(self, *args, **kwargs):
        """Construct the source form."""
        instance: Optional[models.Source] = kwargs.get('instance', None)
        schema: Dict = (
            instance.extra_field_schema if instance else self.model.extra_field_schema
        )
        initial = kwargs.pop(INITIAL, {})
        if instance is None:
            source_type = f'sources.{self.model.__name__.lower()}'
            logging.debug(f'Setting initial type to {source_type}')
            initial['type'] = source_type
        if schema:
            extra: Dict = (instance.extra or {}) if instance else {}
            initial_extra_fields = initial.get(self.model.FieldNames.extra, {})
            for key in schema:
                initial_value = extra.get(key, None) if instance else None
                initial_extra_fields[key] = initial_value
            initial[models.Source.FieldNames.extra] = initial_extra_fields
        kwargs[INITIAL] = initial
        super().__init__(*args, **kwargs)


def rearrange_fields(fields):
    """Return reordered fields to be displayed in the admin."""
    # Fields to display at the top, in order
    top_fields = ('full_string', 'creators', 'title')
    # Fields to display at the bottom, in order
    bottom_fields = (
        'volume',
        'number',
        'page_number',
        'end_page_number',
        'container',
        'description',
        'citations',
    )
    index: int = 0
    for top_field in top_fields:
        if top_field in fields:
            fields.remove(top_field)
            fields.insert(index, top_field)
            index += 1
    for bottom_field in bottom_fields:
        if bottom_field in fields:
            fields.remove(bottom_field)
            fields.append(bottom_field)
    return fields


class PolymorphicSourceAdmin(PolymorphicParentModelAdmin, SearchableModelAdmin):

    base_model = models.PolymorphicSource
    child_models = (
        models.PolymorphicAffidavit,
        models.PolymorphicArticle,
        models.PolymorphicBook,
        models.PolymorphicCorrespondence,
        models.PolymorphicDocument,
        models.PolymorphicFilm,
        models.PolymorphicInterview,
        models.PolymorphicJournalEntry,
        models.PolymorphicPiece,
        models.PolymorphicSection,
        models.PolymorphicSpeech,
        models.PolymorphicWebPage,
    )

    list_display = [
        'pk',
        'escaped_citation_html',
        'attributee_string',
        'date_string',
        'admin_source_link',
        'slug',
        'ctype',
    ]
    list_filter = [
        models.Source.FieldNames.verified,
        # HasContainerFilter,
        # HasFileFilter,
        # HasFilePageOffsetFilter,
        # ImpreciseDateFilter,
        # models.Source.FieldNames.hidden,
        # AttributeeFilter,
        # TypeFilter,
    ]
    # https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_per_page
    list_per_page = 10
    ordering = ['date', 'citation_string']
    search_fields = base_model.searchable_fields

    def get_fields(self, request, model_instance=None):
        """Return reordered fields to be displayed in the admin."""
        fields: list(super().get_fields(request, model_instance))
        return rearrange_fields(fields)


class ChildSourceAdmin(PolymorphicChildModelAdmin):
    """ Base admin class for all child models """

    base_model = models.PolymorphicSource

    # # By using these `base_...` attributes instead of the regular ModelAdmin `form` and `fieldsets`,
    # # the additional fields of the child models are automatically added to the admin form.
    # base_form = ...
    # base_fieldsets = ...

    autocomplete_fields = ['file', 'location']
    exclude = [
        'citation_html',
        'citation_string',
    ]
    inlines = [
        PolymorphicAttributeesInline,
        PolymorphicContainersInline,
        PolymorphicContainedSourcesInline,
        RelatedInline,
    ]
    list_display = [
        item for item in PolymorphicSourceAdmin.list_display if item != 'ctype'
    ]
    # https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_per_page
    list_per_page = 15
    ordering = PolymorphicSourceAdmin.ordering
    readonly_fields = SearchableModelAdmin.readonly_fields + [
        'escaped_citation_html',
        'citation_string',
        'computations',
    ]
    # https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.save_as
    save_as = True
    # https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.save_as_continue
    save_as_continue = True
    search_fields = base_model.searchable_fields

    def get_fields(self, request, model_instance=None):
        """Return reordered fields to be displayed in the admin."""
        fields: list(super().get_fields(request, model_instance))
        return rearrange_fields(fields)


class SourcesInline(TabularInline):
    """Inline admin for sources."""

    model = models.Source
    extra = 0
    fields = [
        'verified',
        'hidden',
        'date_is_circa',
        'creators',
        model.FieldNames.url,
        'date',
        'publication_date',
    ]


admin_site.register(models.PolymorphicSource, PolymorphicSourceAdmin)

admin_site.register(models.PolymorphicAffidavit, ChildSourceAdmin)
admin_site.register(models.PolymorphicArticle, ChildSourceAdmin)
admin_site.register(models.PolymorphicBook, ChildSourceAdmin)
admin_site.register(models.PolymorphicCorrespondence, ChildSourceAdmin)
admin_site.register(models.PolymorphicDocument, ChildSourceAdmin)
admin_site.register(models.PolymorphicFilm, ChildSourceAdmin)
admin_site.register(models.PolymorphicInterview, ChildSourceAdmin)
admin_site.register(models.PolymorphicJournalEntry, ChildSourceAdmin)
admin_site.register(models.PolymorphicPiece, ChildSourceAdmin)
admin_site.register(models.PolymorphicSection, ChildSourceAdmin)
admin_site.register(models.PolymorphicSpeech, ChildSourceAdmin)
admin_site.register(models.PolymorphicWebPage, ChildSourceAdmin)