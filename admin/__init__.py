"""Admin app for ModularHistory."""

from .inlines import GenericStackedInline, GenericTabularInline, StackedInline, TabularInline
from .model_admin import ModelAdmin, SearchableModelAdmin, admin_site
