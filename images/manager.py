from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import QuerySet, Q
from typing import List, Optional
from history.models import Manager as BaseManager


class Manager(BaseManager):
    def search(
            self,
            query: Optional[str] = None,
            start_year: Optional[int] = None,
            end_year: Optional[int] = None,
            entity_ids: Optional[List[int]] = None,
            topic_ids: Optional[List[int]] = None,
            rank: bool = False,
            suppress_unverified: bool = True,
            db: str = 'default'
    ) -> QuerySet:
        qs = super().search(db=db, suppress_unverified=suppress_unverified)

        # Limit to specified date range
        if start_year:
            qs = qs.filter(date__year__gte=start_year)
        if end_year:
            qs = qs.filter(date__year__lte=end_year)

        # Limit to specified entities
        if entity_ids:
            qs = qs.filter(
                Q(entities__id__in=entity_ids)
            )

        # Limit to specified topics
        if topic_ids:
            qs = qs.filter(
                Q(occurrences__related_topics__id__in=topic_ids)
            )

        searchable_fields = self.model.get_searchable_fields()
        if query and searchable_fields:
            query = SearchQuery(query)
            # https://docs.djangoproject.com/en/3.0/ref/contrib/postgres/search/#weighting-queries
            vectors = []
            for searchable_field in searchable_fields:
                if isinstance(searchable_field, tuple) or isinstance(searchable_field, list):
                    field, weight = searchable_field
                    vectors.append(SearchVector(field, weight=weight))
                else:
                    vectors.append(SearchVector(searchable_field))
            vector = vectors[0]
            if len(vectors) > 1:
                for v in vectors[1:]:
                    vector += v
            annotations = {'search': vector}
            if rank:
                annotations['rank'] = SearchRank(vector, query)
            qs = qs.annotate(**annotations).filter(search=query)
        return qs.order_by('id').distinct('id')
