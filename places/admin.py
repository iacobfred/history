from admin import ModelAdmin, TabularInline, admin_site
from places import models
from places.forms import PlaceForm


class LocationInline(TabularInline):
    """TODO: add docstring."""

    model = models.Place
    autocomplete_fields = ['location']


class LocationAdmin(ModelAdmin):
    """Admin for locations."""

    list_display = ['name', 'location']
    list_filter = ['location']
    search_fields = ['name']
    ordering = ['name', 'location__name']
    form = PlaceForm
    add_form = PlaceForm


admin_site.register(models.Place, LocationAdmin)
admin_site.register(models.Venue, LocationAdmin)
admin_site.register(models.City, LocationAdmin)
admin_site.register(models.County, LocationAdmin)
admin_site.register(models.State, LocationAdmin)
admin_site.register(models.Region, LocationAdmin)
admin_site.register(models.Country, LocationAdmin)
admin_site.register(models.Continent, LocationAdmin)
