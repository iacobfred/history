# Generated by Django 3.1.9 on 2021-05-17 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0007_auto_20210517_0151'),
    ]

    operations = [
        migrations.AddField(
            model_name='storycitation',
            name='citation_html',
            field=models.TextField(blank=True, null=True),
        ),
    ]
