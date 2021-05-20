# Generated by Django 3.1.9 on 2021-05-18 16:24

from django.db import migrations

import core.fields.json_field


class Migration(migrations.Migration):

    dependencies = [
        ('postulations', '0020_auto_20210517_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='postulation',
            name='cached_tags',
            field=core.fields.json_field.JSONField(default=list, editable=False),
        ),
    ]