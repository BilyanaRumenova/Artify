# Generated by Django 3.2.5 on 2021-08-05 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210805_1111'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserFollowing',
            new_name='Follow',
        ),
    ]