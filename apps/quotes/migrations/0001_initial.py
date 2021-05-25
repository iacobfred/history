# Generated by Django 3.1.9 on 2021-05-20 20:08

import autoslug.fields
import django.db.models.deletion
from django.db import migrations, models

import apps.dates.fields
import apps.quotes.models.model_with_related_quotes
import core.fields
import core.fields.html_field
import core.fields.json_field
import core.fields.m2m_foreign_key


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('images', '0001_initial'),
        ('topics', '0001_initial'),
        ('entities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Citation',
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
                    'citation_phrase',
                    models.CharField(
                        blank=True,
                        choices=[
                            (None, '-------'),
                            ('quoted in', 'quoted in'),
                            ('cited in', 'cited in'),
                            ('partially reproduced in', 'partially reproduced in'),
                        ],
                        default=None,
                        max_length=25,
                        null=True,
                    ),
                ),
                ('citation_html', models.TextField(blank=True, null=True)),
                ('pages', core.fields.json_field.JSONField(default=list)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Quote',
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
                    'cache',
                    core.fields.json_field.JSONField(
                        blank=True, default=dict, null=True
                    ),
                ),
                (
                    'slug',
                    autoslug.fields.AutoSlugField(
                        blank=True,
                        editable=True,
                        null=True,
                        populate_from='get_slug',
                        unique=True,
                        verbose_name='slug',
                    ),
                ),
                (
                    'date_is_circa',
                    models.BooleanField(
                        blank=True,
                        default=False,
                        help_text='whether the date is estimated/imprecise',
                        verbose_name='date is circa',
                    ),
                ),
                (
                    'end_date',
                    apps.dates.fields.HistoricDateTimeField(
                        blank=True, null=True, verbose_name='end date'
                    ),
                ),
                (
                    'verified',
                    models.BooleanField(default=False, verbose_name='verified'),
                ),
                (
                    'title',
                    models.CharField(
                        blank=True,
                        help_text='The title can be used for the detail page header and title tag, SERP result card header, etc.',
                        max_length=120,
                        null=True,
                        verbose_name='title',
                    ),
                ),
                (
                    'hidden',
                    models.BooleanField(
                        blank=True,
                        default=False,
                        help_text='Hide this item from search results.',
                    ),
                ),
                (
                    'version',
                    models.PositiveSmallIntegerField(
                        default=0, help_text='record revision number'
                    ),
                ),
                (
                    'notes',
                    core.fields.HTMLField(
                        blank=True,
                        null=True,
                        paragraphed=True,
                        processed=False,
                        processor=None,
                        verbose_name='note',
                    ),
                ),
                (
                    'text',
                    core.fields.HTMLField(
                        paragraphed=True,
                        processed=False,
                        processor=None,
                        verbose_name='text',
                    ),
                ),
                (
                    'bite',
                    core.fields.HTMLField(
                        blank=True,
                        null=True,
                        paragraphed=None,
                        processed=False,
                        processor=None,
                        verbose_name='bite',
                    ),
                ),
                (
                    'pretext',
                    core.fields.HTMLField(
                        blank=True,
                        help_text='Content to be displayed before the quote',
                        null=True,
                        paragraphed=False,
                        processed=True,
                        processor=core.fields.html_field.process,
                        verbose_name='pretext',
                    ),
                ),
                (
                    'context',
                    core.fields.HTMLField(
                        blank=True,
                        help_text='Content to be displayed after the quote',
                        null=True,
                        paragraphed=True,
                        processed=True,
                        processor=core.fields.html_field.process,
                        verbose_name='context',
                    ),
                ),
                ('date', apps.dates.fields.HistoricDateTimeField(null=True)),
                (
                    'attributee_html',
                    models.TextField(
                        blank=True,
                        editable=False,
                        null=True,
                        verbose_name='attributee HTML',
                    ),
                ),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='QuoteRelation',
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
                    'content_object',
                    core.fields.m2m_foreign_key.ManyToManyForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='quote_relations',
                        to='quotes.quote',
                        verbose_name='quote',
                    ),
                ),
                (
                    'quote',
                    core.fields.m2m_foreign_key.ManyToManyForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='quotes_quoterelations',
                        to='quotes.quote',
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QuoteImage',
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
                    'image',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='quote_relations',
                        to='images.image',
                        verbose_name='image',
                    ),
                ),
                (
                    'quote',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='image_relations',
                        to='quotes.quote',
                        verbose_name='quote',
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QuoteBite',
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
                    'cache',
                    core.fields.json_field.JSONField(
                        blank=True, default=dict, null=True
                    ),
                ),
                (
                    'slug',
                    autoslug.fields.AutoSlugField(
                        blank=True,
                        editable=True,
                        null=True,
                        populate_from='get_slug',
                        unique=True,
                        verbose_name='slug',
                    ),
                ),
                ('start', models.PositiveIntegerField()),
                ('end', models.PositiveIntegerField()),
                (
                    'quote',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='bites',
                        to='quotes.quote',
                    ),
                ),
                (
                    'tags',
                    models.ManyToManyField(
                        blank=True,
                        related_name='quotebite_set',
                        to='topics.Topic',
                        verbose_name='tags',
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QuoteAttribution',
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
                    'attributee',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='quote_attributions',
                        to='entities.entity',
                        verbose_name='attributee',
                    ),
                ),
                (
                    'quote',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='attributions',
                        to='quotes.quote',
                        verbose_name='quote',
                    ),
                ),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.AddField(
            model_name='quote',
            name='attributees',
            field=models.ManyToManyField(
                blank=True,
                related_name='quotes',
                through='quotes.QuoteAttribution',
                to='entities.Entity',
                verbose_name='attributees',
            ),
        ),
        migrations.AddField(
            model_name='quote',
            name='images',
            field=models.ManyToManyField(
                blank=True,
                related_name='quotes',
                through='quotes.QuoteImage',
                to='images.Image',
            ),
        ),
        migrations.AddField(
            model_name='quote',
            name='related_entities',
            field=models.ManyToManyField(
                blank=True,
                related_name='quote_set',
                to='entities.Entity',
                verbose_name='related entities',
            ),
        ),
        migrations.AddField(
            model_name='quote',
            name='related_quotes',
            field=apps.quotes.models.model_with_related_quotes.RelatedQuotesField(
                blank=True,
                related_name='quote_set',
                through='quotes.QuoteRelation',
                to='quotes.Quote',
                verbose_name='related quotes',
            ),
        ),
    ]
