# Generated by Django 3.1.8 on 2021-04-21 02:55

from django.db import migrations

import core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0012_quote_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='bite',
            field=core.fields.HTMLField(
                blank=True,
                null=True,
                paragraphed=None,
                processed=False,
                processor=None,
                verbose_name='bite',
            ),
        ),
        migrations.AlterField(
            model_name='quote',
            name='notes',
            field=core.fields.HTMLField(
                blank=True, null=True, paragraphed=True, processed=False, processor=None
            ),
        ),
        migrations.AlterField(
            model_name='quote',
            name='text',
            field=core.fields.HTMLField(
                paragraphed=True, processed=False, processor=None, verbose_name='text'
            ),
        ),
    ]