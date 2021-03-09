# Generated by Django 3.0.7 on 2020-08-25 11:35

import functools

from django.db import migrations, models

import modularhistory.fields.file_field


class Migration(migrations.Migration):

    dependencies = [
        ('_account', '0008_auto_20200822_0855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=functools.partial(
                    modularhistory.fields.file_field._generate_upload_path,
                    *(),
                    **{'path': 'account/avatars'}
                ),
            ),
        ),
    ]
