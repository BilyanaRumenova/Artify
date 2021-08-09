# Generated by Django 3.2.5 on 2021-08-05 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('art_items', '0004_delete_portfolio'),
        ('accounts', '0016_auto_20210805_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='items_in_portfolio',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='art_items.artitem'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Portfolio',
        ),
    ]