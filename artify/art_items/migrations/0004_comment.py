# Generated by Django 3.2.5 on 2021-07-26 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('art_items', '0003_remove_like_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='art_items.artitem')),
            ],
        ),
    ]