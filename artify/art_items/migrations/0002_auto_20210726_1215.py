# Generated by Django 3.2.5 on 2021-07-26 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('art_items', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artitem',
            name='user',
        ),
        migrations.AlterField(
            model_name='artitem',
            name='image',
            field=models.ImageField(upload_to='arts'),
        ),
    ]
