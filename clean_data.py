import os
import sys
# from glob import glob

import django
# from decouple import config
# from django.core import management
# from paramiko import SSHClient
# from scp import SCPClient

# Initialize Django
print('Initializing Django...')
my_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(my_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'history.settings')
django.setup()

# from history import settings
# from django.db import transaction
# from django.contrib.auth.models import Permission, Group
# from django.contrib.contenttypes.models import ContentType
# from sources.models import Citation, Source, PageRange
# from occurrences.models import Occurrence
# from quotes.models import QuoteRelation, Quote
# from topics.models import Topic, TopicRelation
# from images.models import Image

# occurrence_ct = ContentType.objects.get_for_model(Occurrence)
# quote_ct = ContentType.objects.get_for_model(Quote)

from django.contrib.flatpages.models import FlatPage
from staticpages.models import StaticPage

for page in FlatPage.objects.all():
    static_page = StaticPage.objects.create(
        url=page.url,
        title=page.title,
        content=page.content,
        enable_comments=page.enable_comments,
        template_name=page.template_name,
        registration_required=page.registration_required,
    )
    for site in page.sites.all():
        static_page.sites.add(site)
    static_page.save()


# mrm_topic = Topic.objects.get(key='Mormonism')
# race_topic = Topic.objects.get(key='Race')
# for q in Quote.objects.filter(verified=True):
#     print(q.text.text)
#     if input('Mormonism? [y/n] ') == 'y':
#         TopicRelation.objects.get_or_create(topic=mrm_topic, object_id=q.id, content_type=quote_ct)
#     if input('Race? [y/n] ') == 'y':
#         TopicRelation.objects.get_or_create(topic=race_topic, object_id=q.id, content_type=quote_ct)
