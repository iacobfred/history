"""Base model classes for ModularHistory."""

import re
from typing import Any, ClassVar, List, Optional, Pattern, Tuple, Type

from aenum import Constant
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model as DjangoModel
from django.urls import reverse
from django.utils.html import SafeString, format_html
from rest_framework.serializers import Serializer
from typedmodels.models import TypedModel as BaseTypedModel

from modularhistory.models.manager import Manager
from modularhistory.utils.models import get_html_for_view as get_html_for_view_

FieldList = List[str]

# TODO: Extend BaseTypedModel when it's possible.
# Currently, only one level of inheritance from BaseTypedModel is permitted, unfortunately.
TypedModel: Type[BaseTypedModel] = BaseTypedModel

# TODO: https://docs.djangoproject.com/en/3.1/topics/db/optimization/


class Views(Constant):
    """Labels of views for which model instances can generate HTML."""

    DETAIL = 'detail'
    CARD = 'card'


class Model(DjangoModel):
    """Model with additional properties used in ModularHistory apps."""

    class FieldNames(Constant):
        pk = 'pk'

    objects: Manager = Manager()
    searchable_fields: ClassVar[Optional[FieldList]] = None
    serializer: Type[Serializer]

    admin_placeholder_regex: Pattern

    class Meta:
        abstract = True

    @classmethod
    def get_searchable_fields(cls) -> FieldList:
        """Return a list of fields that can be used to search for instances of the model."""
        return cls.searchable_fields or []

    @classmethod
    def get_meta(cls):
        """
        Return the model's _meta attribute value.

        This is used purely to avoid warnings about accessing a private attribute.
        """
        return cls._meta

    @property
    def admin_url(self) -> str:
        """Return the model instance's admin URL."""
        return self.get_admin_url()

    @property
    def ctype(self) -> ContentType:
        """Return the model instance's ContentType."""
        return ContentType.objects.get_for_model(self)

    @property
    def detail_link(self) -> SafeString:
        """Return a link to the model instance's detail page."""
        return self.get_detail_link()

    @property
    def detail_url(self) -> str:
        """Return the URL of the model instance's detail page."""
        return reverse(f'{self.get_meta().app_label}:detail', args=[self.id])

    @property
    def natural_key_fields(self) -> Optional[List]:
        """Return the list of fields that comprise a natural key for the model instance."""
        unique_together = getattr(self.Meta, 'unique_together', None)
        if unique_together:
            unique_together_is_valid = isinstance(
                unique_together, (list, tuple)
            ) and all(isinstance(field_name, str) for field_name in unique_together)
            if not unique_together_is_valid:
                raise ValueError(
                    'The `unique_together` value must be an iterable containing strings.'
                )
            return list(unique_together)
        else:
            fields = self._meta.get_fields()
            unique_fields = []
            for field in fields:
                if getattr(field, 'unique', False):
                    unique_fields.append(field.name)
            if unique_fields:
                return unique_fields
        raise NotImplementedError(
            'Model must have Meta.unique_together and/or `natural_key_fields` method defined.'
        )

    def get_admin_url(self):
        """Return the URL of the model instance's admin page."""
        return reverse(
            f'admin:{self._meta.app_label}_{self._meta.model_name}_change',
            args=[self.id],
        )

    def get_detail_link(self, content: Optional[str] = None) -> SafeString:
        """Return a link to the model instance's detail page."""
        content = content or '<i class="fas fa-info-circle"></i>'
        return format_html(f'<a href="{self.detail_url}" target="_blank">{content}</a>')

    def get_html_for_view(
        self,
        view: str = Views.DETAIL,
        text_to_highlight: Optional[str] = None,
    ) -> SafeString:
        """Return HTML for the view (e.g., "card" or "detail") of the instance."""
        # model_name = f'{self.__class__.__name__}'.lower()
        # app_name = inflect.engine().plural(model_name)
        # artifacts_are_used = False
        # if artifacts_are_used:
        #     artifact_subdir = inflect.engine().plural(view)
        #     artifact_name = f'{artifact_subdir}/{self.key}.html'
        #     artifact_path = os.path.join(
        #         settings.BASE_DIR, app_name, 'artifacts', artifact_name
        #     )
        #     if os.path.exists(artifact_path):
        #         logging.info(f'Reading artifact: {artifact_name}')
        #         with open(artifact_path) as artifact:
        #             response = artifact.read()
        return get_html_for_view_(
            self, template_name=view, text_to_highlight=text_to_highlight
        )

    def natural_key(self) -> Tuple[Any, ...]:
        """Return a tuple of values comprising the model instance's natural key."""
        natural_key_values = []
        for field in self.natural_key_fields:
            value = getattr(self, field, None)
            if not value:
                raise AttributeError(f'Model has no `{field}` attribute.')
            natural_key_values.append(value)
        return tuple(natural_key_values)

    def preprocess_html(self, html: str):
        """
        Preprocess the value of an HTML field belonging to the model instance.

        This method can be used to modify the value of an HTML field
        before it is saved.  It is called when HTML fields are cleaned.
        """
        return html

    @classmethod
    def get_object_html(
        cls, match: re.Match, use_preretrieved_html: bool = False
    ) -> str:
        """Return a model instance's HTML based on a placeholder in the admin."""
        if not cls.admin_placeholder_regex.match(match.group(0)):
            raise ValueError(f'{match} does not match {cls.admin_placeholder_regex}')

        if use_preretrieved_html:
            # Return the pre-retrieved HTML (already included in placeholder)
            preretrieved_html = match.group(3)
            if preretrieved_html:
                return preretrieved_html.strip()

        key = match.group(1).strip()
        model_instance = cls.objects.get(pk=key)
        return model_instance.html
