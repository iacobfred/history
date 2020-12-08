# Generated by Django 3.1.4 on 2020-12-06 02:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0006_auto_20201205_1020'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='role',
            options={'verbose_name': 'role'},
        ),
        migrations.AlterModelOptions(
            name='rolefulfillment',
            options={'verbose_name': 'role fulfillment'},
        ),
        migrations.AlterField(
            model_name='entityidea',
            name='entity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entity_ideas', to='entities.entity', verbose_name='entity'),
        ),
        migrations.AlterField(
            model_name='entityidea',
            name='idea',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entity_ideas', to='entities.idea', verbose_name='idea'),
        ),
    ]