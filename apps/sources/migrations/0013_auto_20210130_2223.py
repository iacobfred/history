# Generated by Django 3.1.5 on 2021-01-30 22:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sources', '0012_auto_20201216_0032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sourcecontainment',
            name='container',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='container_containments',
                to='sources.source',
            ),
        ),
        migrations.AlterField(
            model_name='sourcecontainment',
            name='source',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='source_containments',
                to='sources.source',
            ),
        ),
    ]