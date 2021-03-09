# Generated by Django 3.0.4 on 2020-03-06 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_account', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(
                blank=True, max_length=254, unique=True, verbose_name='email address'
            ),
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together={('first_name', 'last_name')},
        ),
    ]
