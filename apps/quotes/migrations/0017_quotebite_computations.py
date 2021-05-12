# Generated by Django 3.1.9 on 2021-05-12 18:48

from django.db import migrations

import core.fields.json_field


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0016_remove_quote_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotebite',
            name='computations',
            field=core.fields.json_field.JSONField(blank=True, default=dict, null=True),
        ),
    ]