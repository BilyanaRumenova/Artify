# Generated by Django 3.2.5 on 2021-08-05 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_profile_age'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='age',
        ),
    ]
