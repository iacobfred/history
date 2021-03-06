# Generated by Django 3.1.12 on 2021-06-27 21:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('propositions', '0010_auto_20210625_0021'),
    ]

    operations = [
        migrations.CreateModel(
            name='PremiseGroup',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'position',
                    models.PositiveSmallIntegerField(blank=True, default=0, null=True),
                ),
                (
                    'type',
                    models.CharField(
                        choices=[('all', 'all'), ('any', 'any')], default='all', max_length=3
                    ),
                ),
                (
                    'argument',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='premise_groups',
                        to='propositions.argument',
                        verbose_name='argument',
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
