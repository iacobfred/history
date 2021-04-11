# Generated by Django 3.1.3 on 2020-11-29 21:15

from django.db import migrations

import modularhistory.fields
import modularhistory.fields.html_field


class Migration(migrations.Migration):

    dependencies = [
        ('occurrences', '0007_auto_20201129_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occurrence',
            name='summary',
            field=modularhistory.fields.HTMLField(
                default='',
                paragraphed=False,
                processor=modularhistory.fields.html_field.process,
                verbose_name='Summary',
            ),
            preserve_default=False,
        ),
    ]
