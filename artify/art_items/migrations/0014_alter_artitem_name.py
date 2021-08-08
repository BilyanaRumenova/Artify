# Generated by Django 3.2.5 on 2021-08-08 17:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('art_items', '0013_alter_artitem_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artitem',
            name='name',
            field=models.CharField(max_length=25, verbose_name=django.core.validators.MinLengthValidator(2)),
        ),
    ]
