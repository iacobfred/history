# Generated by Django 3.0.10 on 2020-10-13 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0009_quote_db_citation_html'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='db_citation_html',
            field=models.CharField(blank=True, max_length=2000, verbose_name='database string'),
        ),
    ]
