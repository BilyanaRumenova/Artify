# Generated by Django 3.2.5 on 2021-08-05 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('art_items', '0004_delete_portfolio'),
        ('accounts', '0015_portfolio_items_in_portfolio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfolio',
            name='items_in_portfolio',
        ),
        migrations.AddField(
            model_name='portfolio',
            name='items_in_portfolio',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='art_items.artitem'),
            preserve_default=False,
        ),
    ]
