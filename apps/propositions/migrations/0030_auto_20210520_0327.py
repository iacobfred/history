# Generated by Django 3.1.9 on 2021-05-20 03:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('propositions', '0029_auto_20210520_0124'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposition',
            name='_cached_citations',
        ),
        migrations.RemoveField(
            model_name='typedproposition',
            name='_cached_citations',
        ),
    ]