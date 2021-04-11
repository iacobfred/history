# Generated by Django 3.1.5 on 2021-01-30 22:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sources', '0013_auto_20210130_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citation',
            name='source',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='citations',
                to='sources.source',
            ),
        ),
    ]
